"""Portable data models for expert knowledge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Literal


@dataclass(slots=True)
class KnowledgeCard:
    """A reviewable unit of expert judgment."""

    title: str
    domain: str
    scenario: str
    recommended_action: str
    signals: list[str] = field(default_factory=list)
    rationale: str = ""
    exceptions: list[str] = field(default_factory=list)
    escalation: str = ""
    evidence: str = ""
    owner: str = "Unassigned"
    confidence: float = 0.8
    status: Literal["draft", "approved"] = "draft"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    schema_version: str = "0.1"

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    def approve(self) -> "KnowledgeCard":
        self.status = "approved"
        return self

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def write(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.write_text(self.to_json() + "\n", encoding="utf-8")
        return destination

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeCard":
        return cls(**data)

    @classmethod
    def read(cls, path: str | Path) -> "KnowledgeCard":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

