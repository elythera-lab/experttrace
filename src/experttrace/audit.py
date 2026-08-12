"""Explainable quality checks for expert knowledge cards."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from .models import KnowledgeCard


@dataclass(frozen=True, slots=True)
class AuditFinding:
    check: str
    status: Literal["pass", "warning"]
    message: str


@dataclass(frozen=True, slots=True)
class AuditReport:
    score: int
    findings: tuple[AuditFinding, ...]

    @property
    def passed(self) -> bool:
        return all(item.status == "pass" for item in self.findings)

    def summary(self) -> str:
        lines = [f"ExpertTrace quality score: {self.score}/100"]
        lines.extend(
            f"[{item.status.upper()}] {item.check}: {item.message}"
            for item in self.findings
        )
        return "\n".join(lines)

    def to_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "passed": self.passed,
            "findings": [asdict(item) for item in self.findings],
        }


class KnowledgeAudit:
    """Evaluate completeness without claiming semantic truth."""

    def evaluate(self, card: KnowledgeCard) -> AuditReport:
        checks = (
            self._finding(
                "recommended_action",
                len(card.recommended_action) >= 20,
                "A specific recommended action is present.",
                "Add a more specific recommended action.",
            ),
            self._finding(
                "decision_signals",
                len(card.signals) >= 2,
                "At least two decision signals are captured.",
                "Capture at least two observable decision signals.",
            ),
            self._finding(
                "rationale",
                len(card.rationale) >= 30,
                "Decision rationale is sufficiently detailed.",
                "Explain why the signals lead to the recommendation.",
            ),
            self._finding(
                "exceptions",
                len(card.exceptions) >= 1,
                "At least one exception or boundary is captured.",
                "Add a case where the recommendation should change.",
            ),
            self._finding(
                "escalation",
                len(card.escalation) >= 15,
                "An escalation trigger or owner is present.",
                "Define when and to whom the issue should escalate.",
            ),
            self._finding(
                "evidence",
                len(card.evidence) >= 10,
                "A supporting source or experience is identified.",
                "Link the judgment to a policy, incident, or expert source.",
            ),
        )
        score = round(
            sum(item.status == "pass" for item in checks) / len(checks) * 100
        )
        return AuditReport(score=score, findings=checks)

    @staticmethod
    def _finding(
        check: str,
        condition: bool,
        pass_message: str,
        warning_message: str,
    ) -> AuditFinding:
        return AuditFinding(
            check=check,
            status="pass" if condition else "warning",
            message=pass_message if condition else warning_message,
        )

