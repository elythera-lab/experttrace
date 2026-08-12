"""ExpertTrace with optional model-assisted follow-up questions."""

from experttrace import InterviewSession, LiteLLMProvider


# LiteLLM reads the selected provider's standard environment variables.
# For example, set OPENAI_API_KEY before using an OpenAI model.
session = InterviewSession(
    topic="Reviewing high-risk AI use cases",
    domain="AI governance",
    owner="AI Governance Council",
    llm=LiteLLMProvider("openai/gpt-5"),
)

while not session.is_complete:
    prompt = session.current_prompt
    session.answer(input(f"{prompt.label}\n{prompt.question}\n> "))

print(session.compile().to_json())
