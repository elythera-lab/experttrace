import { Link } from "react-router-dom";

const principles = [
  ["01", "Ask consistently", "Use a repeatable six-question protocol to surface decisions, signals, reasoning, boundaries, escalation, and evidence."],
  ["02", "Structure locally", "Compile answers into portable JSON without sending expert knowledge to a hosted service."],
  ["03", "Review explicitly", "Audit completeness, preserve provenance, and keep approval in the hands of accountable people."],
];

export default function Home() {
  return (
    <main>
      <section className="hero page-grid">
        <div className="eyebrow">Open-source expert knowledge capture</div>
        <div className="hero-copy">
          <h1>Capture the judgment<br />behind the decision.</h1>
          <p className="hero-lede">Policies record the rule. ExpertTrace records how experienced people recognize the moment, weigh the tradeoffs, and know when to escalate.</p>
          <div className="button-row">
            <Link className="button button-primary" to="/demo">Try the browser demo <span>→</span></Link>
            <Link className="button button-secondary" to="/documentation">Install the Python SDK</Link>
          </div>
          <p className="privacy-line"><span className="status-dot" /> Local-first by default. No account or model call required.</p>
        </div>
        <div className="hero-card" aria-label="Example knowledge trace">
          <div className="card-topline"><span>KNOWLEDGE CARD / 001</span><span className="draft-chip">DRAFT</span></div>
          <div className="trace-stack">
            <div className="trace-row"><span className="trace-key">Signal</span><strong>Sensitive data touches a consequential decision</strong></div>
            <div className="trace-line" />
            <div className="trace-row"><span className="trace-key">Judgment</span><strong>Require enhanced governance review</strong></div>
            <div className="trace-line" />
            <div className="trace-row"><span className="trace-key">Escalate</span><strong>Legal + Privacy before deployment</strong></div>
          </div>
          <div className="card-score"><span>Completeness</span><strong>6 / 6</strong></div>
        </div>
      </section>

      <section className="statement-band">
        <p>Turn tacit expertise into</p>
        <div className="statement-words"><span>reviewable</span><span>portable</span><span>operational</span></div>
        <p>knowledge—without pretending a template can replace an expert.</p>
      </section>

      <section className="section page-grid">
        <div className="section-kicker">A disciplined handoff</div>
        <div className="section-heading">
          <h2>From “it depends” to a traceable decision record.</h2>
          <p>ExpertTrace creates a common structure for judgment while preserving the context that makes it useful.</p>
        </div>
        <div className="principle-grid">
          {principles.map(([number, title, body]) => (
            <article className="principle-card" key={number}>
              <span className="principle-number">{number}</span>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="cta-panel">
        <div><span className="eyebrow">See the protocol in action</span><h2>Six questions. One reviewable knowledge card.</h2></div>
        <Link className="button button-light" to="/demo">Start a local capture <span>→</span></Link>
      </section>
    </main>
  );
}
