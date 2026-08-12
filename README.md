# ExpertTrace Python SDK

ExpertTrace is an open-source toolkit for eliciting, structuring, and auditing
expert judgment. It runs as a deterministic local workflow by default. An
optional LLM layer can ask one targeted follow-up when an expert's answer needs
more specificity.

## Install

Core toolkit, with no runtime dependencies or model calls:

```bash
pip install elythera-experttrace
```

Toolkit plus the LiteLLM adapter:

```bash
pip install "elythera-experttrace[llm]"
```

For local development, clone the repository and use `pip install -e .` or
`pip install -e ".[llm]"`. The distribution is named
`elythera-experttrace`; Python imports and the CLI use `experttrace`.

## Deterministic quickstart

```python
from experttrace import InterviewSession

session = InterviewSession(
    topic="Reviewing high-risk AI use cases",
    domain="AI governance",
    owner="AI Governance Council",
)

while not session.is_complete:
    prompt = session.current_prompt
    session.answer(input(f"{prompt.question}\n> "))

card = session.compile()
print(card.to_json())
print(session.audit().summary())
```

## Adaptive quickstart

Install the `llm` extra, configure the environment variable required by your
chosen provider, and pass a model:

```python
from experttrace import InterviewSession, LiteLLMProvider

session = InterviewSession(
    topic="Reviewing high-risk AI use cases",
    llm=LiteLLMProvider("openai/gpt-5"),
    max_follow_ups_per_prompt=1,
)

while not session.is_complete:
    prompt = session.current_prompt
    session.answer(input(f"{prompt.label}\n{prompt.question}\n> "))

print(session.compile().to_json())
```

LiteLLM supports hosted providers and local runtimes. Model names and credentials
follow the selected provider's LiteLLM configuration. Keep credentials in
environment variables; never put them in source code or interview answers.

If you already have a model client, adapt it without installing LiteLLM:

```python
from experttrace import CallableLLM, InterviewSession

def decide(system_prompt: str, user_prompt: str) -> dict:
    # Call your existing client and return the parsed JSON object.
    return {"should_ask": False, "question": "", "reason": "Sufficient detail."}

session = InterviewSession(
    topic="Vendor risk review",
    llm=CallableLLM(decide),
)
```

The callback must return `should_ask` as a boolean plus string `question` and
`reason` fields.

## CLI

Deterministic mode:

```bash
experttrace interview \
  --topic "Reviewing high-risk AI use cases" \
  --domain "AI governance" \
  --owner "AI Governance Council" \
  --output knowledge-card.json
```

Adaptive mode:

```bash
export OPENAI_API_KEY="..."
experttrace interview \
  --topic "Reviewing high-risk AI use cases" \
  --model openai/gpt-5 \
  --max-follow-ups 1 \
  --output knowledge-card.json
```

Audit a saved card:

```bash
experttrace audit knowledge-card.json
```

By default, model failures produce a warning and the deterministic interview
continues. Add `--strict-llm` if a model failure should stop the run.

## What the LLM does—and does not do

The optional model evaluates each base answer and may generate one concise
follow-up about missing thresholds, exceptions, evidence, or escalation rules.
The JSON compilation and quality audit remain deterministic. Expert approval
remains explicit; the model never certifies that captured knowledge is true.

Privacy behavior is clear at the integration boundary:

- Deterministic mode sends nothing to a model provider.
- Adaptive mode sends the topic, domain, current question, and current answer to
  the provider chosen by the user.
- ExpertTrace does not require an Elythera service or account.

## Design principles

- Offline and dependency-free by default.
- Portable, reviewable knowledge-card JSON.
- Replaceable interview protocols and model providers.
- Explainable audit findings instead of only a score.
- Model calls are opt-in and degrade gracefully unless strict mode is enabled.

## Status

Version 0.1.1 is an alpha research release. It helps structure expert-provided
knowledge; it does not replace professional review or establish factual truth.

Licensed under Apache-2.0.
