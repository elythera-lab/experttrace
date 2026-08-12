"""Model-assisted follow-up selection for expert interviews."""

from __future__ import annotations

from dataclasses import dataclass
import json

from .llm import LLMProvider, LLMResponseError


@dataclass(frozen=True, slots=True)
class FollowUpDecision:
    """The model's recommendation about one additional question."""

    should_ask: bool
    question: str = ""
    reason: str = ""


class AdaptiveElicitor:
    """Ask for missing decision detail while leaving compilation deterministic."""

    SYSTEM_PROMPT = """You help interview an expert to capture tacit decision knowledge.
Assess whether the answer needs exactly one concise follow-up about specificity,
decision thresholds, exceptions, evidence, or escalation triggers. Do not ask for
passwords, API keys, personal data, confidential case details, or raw sensitive
data. If the answer is already specific enough, do not ask a follow-up.

Return only a JSON object with this exact shape:
{"should_ask": true, "question": "...", "reason": "..."}
Use false and an empty question when no follow-up is needed."""

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def decide(
        self,
        *,
        topic: str,
        domain: str,
        prompt_label: str,
        question: str,
        answer: str,
    ) -> FollowUpDecision:
        payload = {
            "topic": topic,
            "domain": domain,
            "prompt_label": prompt_label,
            "question": question,
            "expert_answer": answer,
        }
        result = self.provider.generate_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=json.dumps(payload, ensure_ascii=False),
        )

        should_ask = result.get("should_ask")
        question_value = result.get("question", "")
        reason = result.get("reason", "")
        if not isinstance(should_ask, bool):
            raise LLMResponseError("should_ask must be true or false")
        if not isinstance(question_value, str) or not isinstance(reason, str):
            raise LLMResponseError("question and reason must be strings")
        question_value = question_value.strip()
        reason = reason.strip()
        if should_ask and not question_value:
            raise LLMResponseError("a follow-up decision must include a question")
        return FollowUpDecision(should_ask, question_value, reason)
