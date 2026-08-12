"""Optional, provider-neutral LLM adapters.

The core package never imports a model SDK. Third parties can supply a callable
or install the ``llm`` extra to use LiteLLM.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
import json
import re
from typing import Any, Protocol, runtime_checkable


class LLMError(RuntimeError):
    """Base error for optional model-assisted behavior."""


class LLMConfigurationError(LLMError):
    """Raised when an optional provider is not configured correctly."""


class LLMResponseError(LLMError):
    """Raised when a provider returns an unusable response."""


@runtime_checkable
class LLMProvider(Protocol):
    """Small interface required by ExpertTrace's adaptive features."""

    def generate_json(
        self, *, system_prompt: str, user_prompt: str
    ) -> Mapping[str, Any]:
        """Return one JSON object for the supplied prompts."""


class CallableLLM:
    """Adapt a local function or an existing model client to ExpertTrace."""

    def __init__(
        self,
        callback: Callable[[str, str], Mapping[str, Any]],
    ) -> None:
        self._callback = callback

    def generate_json(
        self, *, system_prompt: str, user_prompt: str
    ) -> Mapping[str, Any]:
        try:
            result = self._callback(system_prompt, user_prompt)
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError(f"model callback failed: {exc}") from exc
        if not isinstance(result, Mapping):
            raise LLMResponseError("the LLM callback must return a JSON object")
        return result


def _parse_json_object(content: Any) -> Mapping[str, Any]:
    if isinstance(content, Mapping):
        return content
    if not isinstance(content, str) or not content.strip():
        raise LLMResponseError("the model returned empty content")

    candidate = content.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, re.DOTALL)
    if fenced:
        candidate = fenced.group(1)

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise LLMResponseError("the model did not return valid JSON") from exc
    if not isinstance(parsed, Mapping):
        raise LLMResponseError("the model response must be a JSON object")
    return parsed


class LiteLLMProvider:
    """Use any LiteLLM-supported model without coupling the core package to it."""

    def __init__(
        self,
        model: str,
        *,
        temperature: float = 0.0,
        timeout: float = 30.0,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        if not model.strip():
            raise ValueError("model is required")
        self.model = model.strip()
        self.temperature = temperature
        self.timeout = timeout
        self.api_key = api_key
        self.base_url = base_url

    def generate_json(
        self, *, system_prompt: str, user_prompt: str
    ) -> Mapping[str, Any]:
        try:
            from litellm import completion
        except ImportError as exc:
            raise LLMConfigurationError(
                'LiteLLM is not installed. Install "elythera-experttrace[llm]".'
            ) from exc

        options: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature,
            "timeout": self.timeout,
        }
        if self.api_key is not None:
            options["api_key"] = self.api_key
        if self.base_url is not None:
            options["api_base"] = self.base_url

        try:
            response = completion(**options)
            content = response.choices[0].message.content
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError(f"model call failed: {exc}") from exc
        return _parse_json_object(content)
