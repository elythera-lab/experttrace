"""Minimal non-interactive ExpertTrace example."""

from experttrace import InterviewSession


session = InterviewSession(
    topic="Reviewing high-risk AI use cases",
    domain="AI governance",
    owner="AI Governance Council",
)

answers = [
    "Require an enhanced governance review before deployment.",
    "Sensitive data is involved\nThe system influences a consequential decision",
    "The possible harm requires evidence that controls work before deployment.",
    "The use is limited to low-risk internal research.",
    "Escalate to Legal and Privacy when sensitive data is involved.",
    "NIST AI RMF and the organization's AI review policy.",
]

for answer in answers:
    session.answer(answer)

card = session.compile()
print(card.to_json())
print(session.audit().summary())

