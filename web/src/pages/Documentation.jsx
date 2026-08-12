import { Link } from "react-router-dom";

const installCode = `pip install elythera-experttrace`;
const pythonCode = `from experttrace import InterviewSession

session = InterviewSession(
    topic="Reviewing high-risk AI use cases",
    domain="AI governance",
    owner="AI Governance Council",
)

while not session.is_complete:
    prompt = session.current_prompt
    session.answer(input(f"{prompt.question}\\n> "))

card = session.compile()
print(card.to_json())
print(session.audit().summary())`;

const llmCode = `pip install "elythera-experttrace[llm]"
export OPENAI_API_KEY="..."

experttrace interview \\
  --topic "Reviewing high-risk AI use cases" \\
  --model openai/gpt-5`;

export default function Documentation() {
  return (
    <main className="subpage docs-page">
      <section className="subpage-intro page-grid">
        <div className="eyebrow">Python SDK · v0.1.1</div>
        <div><h1>Local by default.<br />Extensible by design.</h1><p>The installable toolkit is the source of truth for real integrations, custom interview protocols, audits, and optional model-assisted follow-ups.</p></div>
      </section>
      <section className="docs-layout page-grid">
        <aside className="docs-nav"><a href="#install">Install</a><a href="#quickstart">Quickstart</a><a href="#llm">Optional LLM layer</a><a href="#persistence">Persistence</a></aside>
        <div className="docs-content">
          <section id="install"><span className="docs-index">01</span><h2>Install</h2><p>The core package has no runtime dependencies and makes no model calls.</p><pre><code>{installCode}</code></pre><div className="link-row"><a href="https://pypi.org/project/elythera-experttrace/">View on PyPI ↗</a><a href="https://github.com/elythera-lab/experttrace">Browse source ↗</a></div></section>
          <section id="quickstart"><span className="docs-index">02</span><h2>Run a guided capture</h2><p>Complete the protocol, compile the card, then inspect the explainable quality audit.</p><pre><code>{pythonCode}</code></pre></section>
          <section id="llm"><span className="docs-index">03</span><h2>Enable targeted follow-ups</h2><p>The optional LiteLLM adapter can ask one clarification per base question. Credentials remain in your environment and are sent only to the provider you configure.</p><pre><code>{llmCode}</code></pre><div className="security-note"><strong>Never place provider keys in browser code.</strong><span>The public demo is intentionally deterministic and local-only.</span></div></section>
          <section id="persistence"><span className="docs-index">04</span><h2>Store the result in your system</h2><p><code>card.to_dict()</code> returns a portable record suitable for a JSON/JSONB column. Your application should own authentication, approval, revision history, retention, and access control.</p><div className="data-flow"><span>Interview</span><b>→</b><span>Compile</span><b>→</b><span>Audit</span><b>→</b><span>Human approval</span><b>→</b><span>Your database</span></div></section>
        </div>
      </section>
      <section className="inline-cta"><h2>Explore before you install.</h2><Link className="button button-primary" to="/demo">Try the browser demo →</Link></section>
    </main>
  );
}
