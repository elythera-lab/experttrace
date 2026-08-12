import { useMemo, useState } from "react";
import { questions } from "../data/questions.js";
import { createCaseRecord, exportBundle } from "../lib/knowledgeCard.js";

const emptyMeta = { topic: "", domain: "AI governance", owner: "" };

function makeId() {
  return globalThis.crypto?.randomUUID?.() ?? `case-${Date.now()}`;
}

function downloadJson(cases) {
  const payload = JSON.stringify(exportBundle(cases), null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "experttrace-cases.json";
  link.click();
  URL.revokeObjectURL(url);
}

export default function Demo() {
  const [phase, setPhase] = useState("setup");
  const [meta, setMeta] = useState(emptyMeta);
  const [step, setStep] = useState(0);
  const [answer, setAnswer] = useState("");
  const [followUpAnswer, setFollowUpAnswer] = useState("");
  const [showFollowUp, setShowFollowUp] = useState(false);
  const [answers, setAnswers] = useState({});
  const [followUps, setFollowUps] = useState([]);
  const [cases, setCases] = useState([]);
  const [error, setError] = useState("");

  const current = questions[step];
  const latestCase = cases.at(-1);
  const exportPreview = useMemo(() => JSON.stringify(exportBundle(cases), null, 2), [cases]);

  function begin(event) {
    event.preventDefault();
    if (!meta.topic.trim()) {
      setError("Enter a topic or decision scenario to begin.");
      return;
    }
    setError("");
    setPhase("interview");
  }

  function saveAnswer(event) {
    event.preventDefault();
    if (!answer.trim()) {
      setError("Add an answer before continuing.");
      return;
    }
    if (showFollowUp && !followUpAnswer.trim()) {
      setError("Answer the clarification or remove it before continuing.");
      return;
    }

    const nextAnswers = { ...answers, [current.key]: answer.trim() };
    const nextFollowUps = showFollowUp
      ? [...followUps, {
          parent_question_id: current.key,
          question: current.followUp,
          answer: followUpAnswer.trim(),
          source: "rule",
        }]
      : followUps;

    setAnswers(nextAnswers);
    setFollowUps(nextFollowUps);
    setAnswer("");
    setFollowUpAnswer("");
    setShowFollowUp(false);
    setError("");

    if (step < questions.length - 1) {
      setStep(step + 1);
      return;
    }

    const createdAt = new Date().toISOString();
    const record = createCaseRecord({
      caseId: makeId(),
      ...meta,
      answers: nextAnswers,
      followUps: nextFollowUps,
      questions,
      createdAt,
    });
    setCases([...cases, record]);
    setPhase("complete");
  }

  function startAnother() {
    setMeta(emptyMeta);
    setStep(0);
    setAnswer("");
    setFollowUpAnswer("");
    setShowFollowUp(false);
    setAnswers({});
    setFollowUps([]);
    setError("");
    setPhase("setup");
  }

  function clearCases() {
    setCases([]);
    startAnother();
  }

  return (
    <main className="demo-page">
      <section className="demo-intro">
        <div><span className="eyebrow">Interactive browser demo</span><h1>Trace a decision.</h1></div>
        <div className="local-notice"><span className="local-icon" aria-hidden="true">●</span><div><strong>Your answers stay in this tab</strong><p>No account, backend, analytics, or model call. Download your work before closing the page.</p></div></div>
      </section>

      <section className="demo-workspace">
        <div className="demo-panel">
          {phase === "setup" && (
            <form className="setup-form" onSubmit={begin}>
              <span className="step-label">New capture</span>
              <h2>Name the decision you want to preserve.</h2>
              <label>Topic or scenario <span>Required</span><textarea autoFocus rows="3" value={meta.topic} onChange={(event) => setMeta({ ...meta, topic: event.target.value })} placeholder="Example: Reviewing high-risk AI use cases" /></label>
              <div className="field-pair">
                <label>Domain<input value={meta.domain} onChange={(event) => setMeta({ ...meta, domain: event.target.value })} /></label>
                <label>Knowledge owner<input value={meta.owner} onChange={(event) => setMeta({ ...meta, owner: event.target.value })} placeholder="Team or person" /></label>
              </div>
              {error && <p className="form-error" role="alert">{error}</p>}
              <button className="button button-primary" type="submit">Begin six-question capture →</button>
            </form>
          )}

          {phase === "interview" && (
            <form className="interview-form" onSubmit={saveAnswer}>
              <div className="progress-meta"><span>{String(step + 1).padStart(2, "0")} / 06</span><span>{current.label}</span></div>
              <div className="progress-track"><span style={{ width: `${((step + 1) / questions.length) * 100}%` }} /></div>
              <label className="question-label" htmlFor="answer">{current.question}</label>
              <p className="question-guidance">{current.guidance}</p>
              <textarea id="answer" autoFocus rows="7" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Capture the detail you would give a trusted colleague…" />

              {!showFollowUp ? (
                <button className="text-button" type="button" onClick={() => setShowFollowUp(true)}>+ Add an optional clarification</button>
              ) : (
                <div className="follow-up-block">
                  <div><span>Rule-based clarification</span><button type="button" onClick={() => { setShowFollowUp(false); setFollowUpAnswer(""); }}>Remove</button></div>
                  <label htmlFor="follow-up">{current.followUp}</label>
                  <textarea id="follow-up" rows="3" value={followUpAnswer} onChange={(event) => setFollowUpAnswer(event.target.value)} />
                </div>
              )}

              {error && <p className="form-error" role="alert">{error}</p>}
              <div className="form-actions"><span>Answers can include multiple lines.</span><button className="button button-primary" type="submit">{step === questions.length - 1 ? "Compile card" : "Save & continue"} →</button></div>
            </form>
          )}

          {phase === "complete" && latestCase && (
            <div className="complete-view">
              <div className="complete-heading"><span className="complete-mark">✓</span><div><span className="step-label">Capture complete</span><h2>{latestCase.knowledge_card.title}</h2><p>Draft knowledge card created. Review every field before operational use.</p></div></div>
              <div className="score-panel"><div><strong>{latestCase.audit.score}</strong><span>/100 completeness</span></div><div className="score-findings">{latestCase.audit.findings.map((finding) => <span className={finding.status} key={finding.check}>{finding.status === "pass" ? "✓" : "!"} {finding.message}</span>)}</div></div>
              <div className="review-warning"><strong>Expert review required</strong><p>Completeness is not correctness. This browser demonstration does not approve or validate the judgment.</p></div>
              <div className="button-row"><button className="button button-primary" onClick={() => downloadJson(cases)}>Download {cases.length === 1 ? "case" : `${cases.length} cases`} as JSON</button><button className="button button-secondary" onClick={startAnother}>Capture another case</button></div>
            </div>
          )}
        </div>

        <aside className="preview-panel">
          <div className="preview-heading"><div><span>JSON preview</span><strong>{cases.length} {cases.length === 1 ? "case" : "cases"}</strong></div>{cases.length > 0 && <button onClick={clearCases}>Clear all</button>}</div>
          <pre aria-live="polite"><code>{cases.length > 0 ? exportPreview : `{
  "format": "experttrace-browser-export",
  "schema_version": "0.1",
  "cases": []
}`}</code></pre>
          <p className="preview-note">Each <code>knowledge_card</code> follows the Python package's v0.1 schema. The outer bundle preserves responses, clarifications, and review state.</p>
        </aside>
      </section>
    </main>
  );
}
