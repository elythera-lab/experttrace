import { Link } from "react-router-dom";
import { questions } from "../data/questions.js";

export default function HowItWorks() {
  return (
    <main className="subpage">
      <section className="subpage-intro page-grid">
        <div className="eyebrow">The capture protocol</div>
        <div><h1>Six angles on one expert decision.</h1><p>Each prompt captures a distinct part of judgment. Together, they make the recommendation easier to understand, challenge, and reuse.</p></div>
      </section>
      <section className="question-map page-grid">
        {questions.map((prompt, index) => (
          <article className="question-map-row" key={prompt.key}>
            <span className="map-number">0{index + 1}</span>
            <div><span className="map-label">{prompt.label}</span><h2>{prompt.question}</h2><p>{prompt.guidance}</p></div>
            <span className="map-key">{prompt.key}</span>
          </article>
        ))}
      </section>
      <section className="architecture-section page-grid">
        <div className="section-kicker">Architecture</div>
        <div className="architecture-flow">
          {[
            ["Capture", "Expert answers the protocol"],
            ["Assist", "Optional LLM asks a targeted follow-up"],
            ["Compile", "Deterministic code creates JSON"],
            ["Audit", "Completeness checks explain gaps"],
            ["Review", "A responsible person approves"],
            ["Export", "Store or integrate the card"],
          ].map(([title, body], index) => (
            <div className="architecture-step" key={title}><span>{index + 1}</span><strong>{title}</strong><p>{body}</p></div>
          ))}
        </div>
        <div className="review-callout"><strong>Human review is not optional.</strong><p>An audit checks whether fields are complete. It does not certify that the captured judgment is true, safe, current, or appropriate for a new context.</p></div>
      </section>
      <section className="inline-cta"><h2>Ready to trace a real decision?</h2><Link className="button button-primary" to="/demo">Open the demo →</Link></section>
    </main>
  );
}
