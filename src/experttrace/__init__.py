"""ExpertTrace public API."""

from .audit import AuditFinding, AuditReport, KnowledgeAudit
from .adaptive import AdaptiveElicitor, FollowUpDecision
from .compiler import KnowledgeCompiler
from .interview import InterviewProtocol, InterviewPrompt, InterviewSession
from .llm import (
    CallableLLM,
    LLMConfigurationError,
    LLMError,
    LLMProvider,
    LLMResponseError,
    LiteLLMProvider,
)
from .models import KnowledgeCard

__all__ = [
    "AuditFinding",
    "AuditReport",
    "AdaptiveElicitor",
    "CallableLLM",
    "FollowUpDecision",
    "InterviewPrompt",
    "InterviewProtocol",
    "InterviewSession",
    "KnowledgeAudit",
    "KnowledgeCard",
    "KnowledgeCompiler",
    "LLMConfigurationError",
    "LLMError",
    "LLMProvider",
    "LLMResponseError",
    "LiteLLMProvider",
]

__version__ = "0.1.1"
