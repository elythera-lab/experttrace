"""Command-line interface for local and third-party use."""

from __future__ import annotations

import argparse
from pathlib import Path

from .audit import KnowledgeAudit
from .interview import InterviewSession
from .llm import LiteLLMProvider
from .models import KnowledgeCard


def _interview(args: argparse.Namespace) -> int:
    provider = LiteLLMProvider(args.model) if args.model else None
    session = InterviewSession(
        topic=args.topic,
        domain=args.domain,
        owner=args.owner,
        llm=provider,
        max_follow_ups_per_prompt=args.max_follow_ups,
        strict_llm=args.strict_llm,
    )
    print("ExpertTrace guided capture\n")
    if args.model:
        print(f"Adaptive follow-ups enabled with {args.model}\n")
    while not session.is_complete:
        current, total = session.progress
        prompt = session.current_prompt
        print(f"[{current}/{total}] {prompt.label}")
        print(prompt.question)
        if prompt.guidance:
            print(f"Hint: {prompt.guidance}")
        value = input("> ")
        while not value.strip():
            value = input("Please enter an answer.\n> ")
        session.answer(value)
        print()

    card = session.compile()
    report = KnowledgeAudit().evaluate(card)
    destination = card.write(args.output)
    print(report.summary())
    if session.llm_warnings:
        print("\nAdaptive follow-ups were skipped after these provider errors:")
        for warning in session.llm_warnings:
            print(f"- {warning}")
    print(f"\nSaved draft knowledge card to {destination}")
    return 0


def _audit(args: argparse.Namespace) -> int:
    card = KnowledgeCard.read(args.card)
    print(KnowledgeAudit().evaluate(card).summary())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="experttrace",
        description="Capture and audit expert knowledge.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    interview = subparsers.add_parser("interview", help="Run a guided interview")
    interview.add_argument("--topic", required=True)
    interview.add_argument("--domain", default="AI governance")
    interview.add_argument("--owner", default="Unassigned")
    interview.add_argument("--output", default="knowledge-card.json")
    interview.add_argument(
        "--model",
        help="Optional LiteLLM model name, for example openai/gpt-5",
    )
    interview.add_argument(
        "--max-follow-ups",
        type=int,
        default=1,
        help="Maximum adaptive follow-ups per base question (default: 1)",
    )
    interview.add_argument(
        "--strict-llm",
        action="store_true",
        help="Stop on a model error instead of continuing deterministically",
    )
    interview.set_defaults(handler=_interview)

    audit = subparsers.add_parser("audit", help="Audit a knowledge-card JSON file")
    audit.add_argument("card", type=Path)
    audit.set_defaults(handler=_audit)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
