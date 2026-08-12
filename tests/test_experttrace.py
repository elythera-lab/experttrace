import json
from pathlib import Path
import tempfile
import unittest

from experttrace import (
    CallableLLM,
    InterviewSession,
    KnowledgeAudit,
    KnowledgeCard,
    LLMError,
    LLMResponseError,
)


GOOD_ANSWERS = [
    "Require an enhanced governance review before deployment.",
    "Sensitive data is involved\nThe system influences a consequential decision",
    "These signals increase possible harm and require evidence before deployment.",
    "The use is limited to low-risk internal research.",
    "Escalate to Legal and Privacy when sensitive data is involved.",
    "NIST AI RMF and the internal AI review policy.",
]


class InterviewSessionTests(unittest.TestCase):
    def test_complete_session_compiles_and_audits(self):
        session = InterviewSession(topic="Review AI use case", owner="Council")
        for answer in GOOD_ANSWERS:
            session.answer(answer)

        card = session.compile()
        report = session.audit()

        self.assertTrue(session.is_complete)
        self.assertEqual(card.owner, "Council")
        self.assertEqual(len(card.signals), 2)
        self.assertEqual(report.score, 100)

    def test_empty_answer_is_rejected(self):
        session = InterviewSession(topic="Review AI use case")
        with self.assertRaises(ValueError):
            session.answer("   ")

    def test_incomplete_session_cannot_compile(self):
        session = InterviewSession(topic="Review AI use case")
        with self.assertRaises(RuntimeError):
            session.compile()

    def test_optional_llm_adds_and_compiles_a_follow_up(self):
        calls = 0

        def decide(_system_prompt, _user_prompt):
            nonlocal calls
            calls += 1
            if calls == 1:
                return {
                    "should_ask": True,
                    "question": "What exact threshold triggers that review?",
                    "reason": "Capture an operational threshold.",
                }
            return {"should_ask": False, "question": "", "reason": "Specific."}

        session = InterviewSession(
            topic="Review AI use case",
            llm=CallableLLM(decide),
        )
        follow_up = session.answer(GOOD_ANSWERS[0])

        self.assertEqual(follow_up.label, "Adaptive follow-up")
        self.assertEqual(session.progress, (1, 6))
        session.answer("Trigger when the impact rating is high.")
        for answer in GOOD_ANSWERS[1:]:
            session.answer(answer)

        card = session.compile()
        self.assertTrue(session.is_complete)
        self.assertEqual(calls, 6)
        self.assertIn("impact rating is high", card.recommended_action)

    def test_llm_failure_is_best_effort_by_default(self):
        def fail(_system_prompt, _user_prompt):
            raise LLMError("provider unavailable")

        session = InterviewSession(
            topic="Review AI use case",
            llm=CallableLLM(fail),
        )
        next_prompt = session.answer(GOOD_ANSWERS[0])

        self.assertEqual(next_prompt.key, "signals")
        self.assertIn("provider unavailable", session.llm_warnings[0])

    def test_strict_llm_mode_propagates_failure(self):
        def fail(_system_prompt, _user_prompt):
            raise LLMResponseError("bad response")

        session = InterviewSession(
            topic="Review AI use case",
            llm=CallableLLM(fail),
            strict_llm=True,
        )
        with self.assertRaises(LLMResponseError):
            session.answer(GOOD_ANSWERS[0])

    def test_follow_ups_can_be_disabled_with_llm_present(self):
        def should_not_run(_system_prompt, _user_prompt):
            raise AssertionError("callback should not be invoked")

        session = InterviewSession(
            topic="Review AI use case",
            llm=CallableLLM(should_not_run),
            max_follow_ups_per_prompt=0,
        )
        self.assertEqual(session.answer(GOOD_ANSWERS[0]).key, "signals")


class KnowledgeCardTests(unittest.TestCase):
    def test_round_trip_json(self):
        session = InterviewSession(topic="Review AI use case")
        for answer in GOOD_ANSWERS:
            session.answer(answer)
        original = session.compile().approve()

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "card.json"
            original.write(path)
            loaded = KnowledgeCard.read(path)

        self.assertEqual(loaded.to_dict(), original.to_dict())
        self.assertEqual(json.loads(loaded.to_json())["status"], "approved")

    def test_audit_explains_missing_fields(self):
        card = KnowledgeCard(
            title="Thin card",
            domain="General",
            scenario="Thin card",
            recommended_action="Do it",
        )
        report = KnowledgeAudit().evaluate(card)
        self.assertLess(report.score, 100)
        self.assertFalse(report.passed)
        self.assertIn("Add a more specific", report.summary())


if __name__ == "__main__":
    unittest.main()
