export const questions = [
  {
    key: "recommended_action",
    label: "Core judgment",
    question: "What action would you normally recommend in this situation?",
    guidance: "Describe the decision as you would explain it to a trusted colleague.",
    followUp: "What concrete outcome should this action produce?",
  },
  {
    key: "signals",
    label: "Decision signals",
    question: "Which signals or conditions matter most before making that decision?",
    guidance: "List one signal per line, including details that may not appear in policy.",
    followUp: "Which threshold or combination of signals changes the decision?",
  },
  {
    key: "rationale",
    label: "Reasoning",
    question: "Why do those signals lead you to this recommendation?",
    guidance: "Capture the reasoning, tradeoffs, or experience behind the decision.",
    followUp: "What risk or tradeoff carries the most weight here?",
  },
  {
    key: "exceptions",
    label: "Exceptions",
    question: "When would this recommendation be wrong or need to change?",
    guidance: "List exceptions, counterexamples, and boundary conditions one per line.",
    followUp: "Can you name a recent counterexample or edge case?",
  },
  {
    key: "escalation",
    label: "Escalation",
    question: "When should someone stop and involve another expert?",
    guidance: "Name the trigger and the person or function that should review it.",
    followUp: "Who makes the final call when that trigger is reached?",
  },
  {
    key: "evidence",
    label: "Evidence",
    question: "What evidence, policy, or operational experience supports this judgment?",
    guidance: "A source can be a policy, incident, decision record, or named expert.",
    followUp: "Where can a reviewer find the strongest supporting record?",
  },
];
