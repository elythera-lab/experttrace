"""Compile guided interview answers into portable knowledge cards."""

from __future__ import annotations

import re
from typing import Mapping

from .models import KnowledgeCard


def _items(value: str) -> list[str]:
    return [
        item.strip(" -\t")
        for item in re.split(r"\n|;", value)
        if item.strip(" -\t")
    ]


class KnowledgeCompiler:
    """Deterministic compiler used by the free local release."""

    def compile(
        self,
        *,
        topic: str,
        domain: str,
        owner: str,
        answers: Mapping[str, str],
    ) -> KnowledgeCard:
        def combined(key: str) -> str:
            values = [answers.get(key, "")]
            prefix = f"{key}__follow_up_"
            values.extend(
                value
                for answer_key, value in sorted(answers.items())
                if answer_key.startswith(prefix)
            )
            return "\n".join(value for value in values if value)

        return KnowledgeCard(
            title=topic,
            domain=domain,
            scenario=topic,
            recommended_action=combined("recommended_action"),
            signals=_items(combined("signals")),
            rationale=combined("rationale"),
            exceptions=_items(combined("exceptions")),
            escalation=combined("escalation"),
            evidence=combined("evidence"),
            owner=owner,
        )
