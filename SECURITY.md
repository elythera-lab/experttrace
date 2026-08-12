# Security Policy

ExpertTrace captures expert judgment that may contain confidential operational,
legal, safety, or organizational information. Security reports are welcome, and
we ask reporters and integrators to handle both vulnerabilities and captured
knowledge carefully.

## Supported versions

ExpertTrace is currently an alpha project. Security fixes are applied to the
latest release and the `main` branch.

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |
| Earlier versions | No |

Before reporting a problem, confirm that it is reproducible with the latest
release of [`elythera-experttrace`](https://pypi.org/project/elythera-experttrace/)
or the current `main` branch.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities, credentials, private interview
answers, or exploit details in a public GitHub issue or discussion.

Use the repository's private vulnerability-reporting form when it is available:

<https://github.com/elythera-lab/experttrace/security/advisories/new>

If that form is unavailable, open a public issue titled **Security contact
request** containing no vulnerability details or sensitive data. A maintainer
will arrange a private reporting channel.

Include the following in a private report when possible:

- The affected ExpertTrace version and installation method.
- The affected component, such as the Python SDK, CLI, optional LLM adapter,
  browser demo, build workflow, or published package.
- Reproduction steps or a minimal proof of concept.
- The expected and observed behavior.
- The potential impact and any known mitigations.
- Whether the issue has been disclosed elsewhere.

Please use synthetic data in demonstrations. Do not send real expert answers,
customer data, production credentials, or other secrets.

## What to expect

Maintainers will aim to acknowledge a complete report within five business
days, assess its impact, and keep the reporter informed while a correction is
prepared. Timing depends on severity and maintainer availability.

Please allow a reasonable remediation period before public disclosure. We will
coordinate disclosure and credit with the reporter unless anonymity is
requested or legal or safety constraints prevent it.

## Security and privacy boundaries

### Deterministic mode

The core interview, compilation, audit, and JSON export workflow runs locally
and has no runtime dependencies. ExpertTrace does not upload knowledge cards or
provide a hosted database. Applications integrating the package are
responsible for authentication, authorization, encryption, retention, backups,
approval history, and access logging.

### Optional LLM mode

The LLM adapter is opt-in. It sends the interview topic, domain, current
question, and current answer to the model provider configured by the user.
Provider privacy, retention, residency, and security terms therefore apply.

- Keep provider credentials in environment variables or a managed secret
  store—never in source code, knowledge cards, logs, or interview answers.
- Use only approved providers and models for the sensitivity of the material.
- Review provider retention and training settings before sending confidential
  knowledge.
- Treat generated follow-up questions as untrusted model output.
- Leave deterministic mode enabled when model disclosure is not acceptable.

### Browser demonstration

The GitHub Pages demo performs the six-question flow in the browser and does not
call the Python runtime, a backend, or an LLM. Captured cases remain in the
current tab unless the user downloads the JSON file. Users are responsible for
protecting downloaded files and should avoid entering sensitive information on
shared or untrusted devices.

Never add API keys or other secrets to frontend source, Vite environment
variables, built assets, or GitHub Pages configuration. Anything shipped to a
browser is public. A future hosted model integration must use an authenticated
server-side API with rate limits, abuse controls, logging safeguards, and
spending limits.

## Safe use of knowledge cards

Knowledge cards are expert-provided records, not verified facts or automated
authorizations. The completeness audit checks whether expected fields are
present; it does not establish correctness, safety, policy compliance, or
fitness for a new context.

Production integrations should:

- Require authenticated contributors and explicit human approval.
- Preserve provenance, revisions, reviewers, and approval state.
- Validate imported JSON and enforce the expected `schema_version`.
- Apply least-privilege access to stored cards and exports.
- Avoid storing secrets or unnecessary personal data in cards.
- Re-review cards when policies, evidence, owners, or operating conditions
  change.

## Dependency and supply-chain safety

Install releases from the official PyPI distribution:

```bash
pip install elythera-experttrace
```

The distribution name is `elythera-experttrace`; the Python import and CLI are
both named `experttrace`. Review dependency changes before upgrading the
optional `llm` extra, pin versions where reproducibility matters, and verify
artifacts in high-assurance environments.

## Out of scope

The following are generally not vulnerabilities in ExpertTrace itself:

- Incorrect, incomplete, outdated, or malicious expert-provided content.
- Model hallucinations or poor follow-up questions without a security impact.
- Provider behavior that follows the provider's documented configuration.
- Exposure caused by an integrating application that stores or transmits cards
  insecurely.
- Reports based only on automated scanner output without a reproducible impact.

These concerns may still be appropriate for a regular GitHub issue when no
sensitive details are involved.
