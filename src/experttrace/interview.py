"""Guided, domain-configurable expert interviews."""

from __future__ import annotations

from dataclasses import dataclass
import json
from importlib.resources import files
from typing import Iterable

from .audit import AuditReport, KnowledgeAudit
from .adaptive import AdaptiveElicitor
from .compiler import KnowledgeCompiler
from .llm import LLMError, LLMProvider
from .models import KnowledgeCard


@dataclass(frozen=True, slots=True)
class InterviewPrompt:
    key: str
    label: str
    question: str
    guidance: str = ""


class InterviewProtocol:
    """An ordered interview protocol loaded from a domain pack."""

    def __init__(self, prompts: Iterable[InterviewPrompt], name: str = "custom"):
        self.name = name
        self.prompts = tuple(prompts)
        if not self.prompts:
            raise ValueError("protocol must contain at least one prompt")

    @classmethod
    def default(cls) -> "InterviewProtocol":
        return cls.from_pack("ai_governance")

    @classmethod
    def from_pack(cls, name: str) -> "InterviewProtocol":
        pack_path = files("experttrace").joinpath("packs", f"{name}.json")
        if not pack_path.is_file():
            raise ValueError(f"unknown domain pack: {name}")
        data = json.loads(pack_path.read_text(encoding="utf-8"))
        prompts = [InterviewPrompt(**item) for item in data["prompts"]]
        return cls(prompts, name=data.get("name", name))


class InterviewSession:
    """Stateful guided capture session with explicit compile and audit steps."""

    def __init__(
        self,
        *,
        topic: str,
        domain: str = "General",
        owner: str = "Unassigned",
        protocol: InterviewProtocol | None = None,
        llm: LLMProvider | None = None,
        max_follow_ups_per_prompt: int = 1,
        strict_llm: bool = False,
    ) -> None:
        if not topic.strip():
            raise ValueError("topic is required")
        self.topic = topic.strip()
        self.domain = domain.strip() or "General"
        self.owner = owner.strip() or "Unassigned"
        self.protocol = protocol or InterviewProtocol.default()
        if max_follow_ups_per_prompt < 0:
            raise ValueError("max_follow_ups_per_prompt cannot be negative")
        self.llm = llm
        self.max_follow_ups_per_prompt = max_follow_ups_per_prompt
        self.strict_llm = strict_llm
        self._elicitor = AdaptiveElicitor(llm) if llm is not None else None
        self._cursor = 0
        self._answers: dict[str, str] = {}
        self._pending_prompt: InterviewPrompt | None = None
        self._follow_up_counts: dict[str, int] = {}
        self._llm_warnings: list[str] = []

    @property
    def is_complete(self) -> bool:
        return (
            self._cursor >= len(self.protocol.prompts)
            and self._pending_prompt is None
        )

    @property
    def current_prompt(self) -> InterviewPrompt:
        if self.is_complete:
            raise RuntimeError("the interview is complete")
        if self._pending_prompt is not None:
            return self._pending_prompt
        return self.protocol.prompts[self._cursor]

    @property
    def answers(self) -> dict[str, str]:
        return dict(self._answers)

    @property
    def llm_warnings(self) -> tuple[str, ...]:
        """Non-fatal provider failures encountered in best-effort mode."""

        return tuple(self._llm_warnings)

    @property
    def progress(self) -> tuple[int, int]:
        return min(self._cursor + 1, len(self.protocol.prompts)), len(
            self.protocol.prompts
        )

    def answer(self, text: str) -> InterviewPrompt | None:
        value = text.strip()
        if not value:
            raise ValueError("an answer cannot be empty")

        prompt = self.current_prompt
        self._answers[prompt.key] = value
        if self._pending_prompt is not None:
            self._pending_prompt = None
            self._cursor += 1
            return None if self.is_complete else self.current_prompt

        base_key = prompt.key
        count = self._follow_up_counts.get(base_key, 0)
        if self._elicitor is not None and count < self.max_follow_ups_per_prompt:
            try:
                decision = self._elicitor.decide(
                    topic=self.topic,
                    domain=self.domain,
                    prompt_label=prompt.label,
                    question=prompt.question,
                    answer=value,
                )
                if decision.should_ask:
                    count += 1
                    self._follow_up_counts[base_key] = count
                    self._pending_prompt = InterviewPrompt(
                        key=f"{base_key}__follow_up_{count}",
                        label="Adaptive follow-up",
                        question=decision.question,
                        guidance=decision.reason,
                    )
                    return self._pending_prompt
            except LLMError as exc:
                if self.strict_llm:
                    raise
                self._llm_warnings.append(f"{base_key}: {exc}")

        self._cursor += 1
        return None if self.is_complete else self.current_prompt

    def compile(self) -> KnowledgeCard:
        if not self.is_complete:
            raise RuntimeError("complete the interview before compiling")
        return KnowledgeCompiler().compile(
            topic=self.topic,
            domain=self.domain,
            owner=self.owner,
            answers=self._answers,
        )

    def audit(self) -> AuditReport:
        return KnowledgeAudit().evaluate(self.compile())
