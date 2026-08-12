function splitItems(value) {
  return value
    .split(/\n|;/)
    .map((item) => item.replace(/^[\s-]+/, "").trim())
    .filter(Boolean);
}

function combinedAnswer(key, answers, followUps) {
  const values = [answers[key]];
  values.push(
    ...followUps
      .filter((item) => item.parent_question_id === key)
      .map((item) => item.answer),
  );
  return values.filter(Boolean).join("\n");
}

export function compileKnowledgeCard({ topic, domain, owner, answers, followUps, createdAt }) {
  const combined = (key) => combinedAnswer(key, answers, followUps);
  return {
    title: topic.trim(),
    domain: domain.trim() || "General",
    scenario: topic.trim(),
    recommended_action: combined("recommended_action"),
    signals: splitItems(combined("signals")),
    rationale: combined("rationale"),
    exceptions: splitItems(combined("exceptions")),
    escalation: combined("escalation"),
    evidence: combined("evidence"),
    owner: owner.trim() || "Unassigned",
    confidence: 0.8,
    status: "draft",
    created_at: createdAt,
    schema_version: "0.1",
  };
}

const checks = [
  ["recommended_action", (card) => card.recommended_action.length >= 20, "Specific action captured", "Make the recommended action more specific"],
  ["decision_signals", (card) => card.signals.length >= 2, "Two or more signals captured", "Capture at least two observable signals"],
  ["rationale", (card) => card.rationale.length >= 30, "Reasoning is detailed", "Explain why the signals support the recommendation"],
  ["exceptions", (card) => card.exceptions.length >= 1, "Boundary captured", "Add a case where the recommendation changes"],
  ["escalation", (card) => card.escalation.length >= 15, "Escalation path captured", "Define when and to whom the issue escalates"],
  ["evidence", (card) => card.evidence.length >= 10, "Evidence identified", "Link the judgment to a source or experience"],
];

export function auditKnowledgeCard(card) {
  const findings = checks.map(([check, test, passMessage, warningMessage]) => ({
    check,
    status: test(card) ? "pass" : "warning",
    message: test(card) ? passMessage : warningMessage,
  }));
  return {
    score: Math.round((findings.filter((item) => item.status === "pass").length / findings.length) * 100),
    passed: findings.every((item) => item.status === "pass"),
    findings,
  };
}

export function createCaseRecord({ caseId, topic, domain, owner, answers, followUps, questions, createdAt }) {
  const knowledgeCard = compileKnowledgeCard({ topic, domain, owner, answers, followUps, createdAt });
  return {
    case_id: caseId,
    created_at: createdAt,
    status: "draft",
    responses: questions.map((prompt) => ({
      question_id: prompt.key,
      question: prompt.question,
      answer: answers[prompt.key],
    })),
    follow_ups: followUps,
    review: { required: true, approved: false },
    knowledge_card: knowledgeCard,
    audit: auditKnowledgeCard(knowledgeCard),
  };
}

export function exportBundle(cases, exportedAt = new Date().toISOString()) {
  return {
    format: "experttrace-browser-export",
    schema_version: "0.1",
    exported_at: exportedAt,
    cases,
  };
}
