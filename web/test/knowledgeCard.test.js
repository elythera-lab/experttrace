import test from "node:test";
import assert from "node:assert/strict";
import { questions } from "../src/data/questions.js";
import { createCaseRecord, exportBundle } from "../src/lib/knowledgeCard.js";

const answers = {
  recommended_action: "Require an enhanced governance review before deployment.",
  signals: "Sensitive data is involved\nThe system influences a consequential decision",
  rationale: "These signals increase possible harm and require evidence before deployment.",
  exceptions: "The use is limited to low-risk internal research.",
  escalation: "Escalate to Legal and Privacy when sensitive data is involved.",
  evidence: "NIST AI RMF and the internal AI review policy.",
};

test("browser output matches the Python knowledge-card schema", () => {
  const record = createCaseRecord({
    caseId: "case-1",
    topic: "Review AI use case",
    domain: "AI governance",
    owner: "Council",
    answers,
    followUps: [],
    questions,
    createdAt: "2026-08-12T00:00:00.000Z",
  });

  assert.deepEqual(Object.keys(record.knowledge_card), [
    "title", "domain", "scenario", "recommended_action", "signals", "rationale",
    "exceptions", "escalation", "evidence", "owner", "confidence", "status",
    "created_at", "schema_version",
  ]);
  assert.equal(record.audit.score, 100);
  assert.equal(record.responses.length, 6);
  assert.deepEqual(record.review, { required: true, approved: false });
});

test("export preserves multiple cases and linked rule follow-ups", () => {
  const followUps = [{ parent_question_id: "signals", question: "Which threshold?", answer: "High impact", source: "rule" }];
  const record = createCaseRecord({ caseId: "case-1", topic: "Review", domain: "General", owner: "Owner", answers, followUps, questions, createdAt: "2026-08-12T00:00:00.000Z" });
  const bundle = exportBundle([record, { ...record, case_id: "case-2" }], "2026-08-12T01:00:00.000Z");

  assert.equal(bundle.cases.length, 2);
  assert.equal(bundle.cases[0].follow_ups[0].parent_question_id, "signals");
  assert.equal(bundle.cases[0].follow_ups[0].source, "rule");
  assert.doesNotThrow(() => JSON.parse(JSON.stringify(bundle)));
});
