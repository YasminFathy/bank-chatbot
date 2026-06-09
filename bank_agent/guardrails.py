"""
Guardrails safety layer wired into ADK via before_tool_callback / after_agent_callback.

Some lightweight regex validators for the PoC.
Production equivalents are noted inline — all are drop-in replacements
using the same ADK callback signatures.
"""

import re

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.models.llm_response import LlmResponse

# --------------------
# Patterns
# ---------------------
_INJECTION_PATTERNS = [
    re.compile(r"ignore (previous|all|your) instructions", re.I),
    re.compile(r"you are now", re.I),
    re.compile(r"pretend (you are|to be)", re.I),
    re.compile(r"disregard|jailbreak", re.I),
    re.compile(r"(reveal|show|print|repeat|output).{0,20}system prompt", re.I),
    re.compile(r"repeat after me", re.I),
]

_OUT_OF_SCOPE = re.compile(
    r"\b(loan|mortgage|remortgage|invest|isa|pension|stocks?|shares?|forex|crypto|financial advice)\b",
    re.I,
)

# Production: replace with Guardrails AI detect-pii NeMo validator
_PII_REDACTIONS = [
    (re.compile(r"\b\d{8}\b"), "[ACCOUNT]"),  # 8-digit account numbers
    (re.compile(r"\b\d{2}-\d{2}-\d{2}\b"), "[SORT_CODE]"),  # UK sort codes
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b"), "[CARD]"),  # Card numbers
]

_SAFE_REDIRECT = (
    "I can only help with account balances, transaction history, and identifying charges. "
    "For anything else please call 0800 XXX XXXX or visit a branch."
)


# -------------------
# ADK Callbacks
# --------------------


def input_guardrail(**kwargs):
    tool_context = kwargs.get("tool_context")
    msg = ""
    if tool_context:
        msg = tool_context.state.get("last_user_message", "")
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(msg):
            return {"blocked": True, "message": _SAFE_REDIRECT}
    if _OUT_OF_SCOPE.search(msg):
        return {"blocked": True, "message": _SAFE_REDIRECT}
    return None


def output_guardrail(**kwargs):
    llm_response = kwargs.get("llm_response")
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None
    modified = False
    new_parts = []
    for part in llm_response.content.parts:
        if part.text:
            cleaned = part.text
            for pattern, replacement in _PII_REDACTIONS:
                new_text = pattern.sub(replacement, cleaned)
                if new_text != cleaned:
                    modified = True
                cleaned = new_text
            new_parts.append(type(part)(text=cleaned))
        else:
            new_parts.append(part)
    if modified:
        new_content = type(llm_response.content)(
            parts=new_parts, role=llm_response.content.role
        )
        from google.adk.models.llm_response import LlmResponse

        return LlmResponse(content=new_content)
    return None
