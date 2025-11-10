# core/guardrails.py
"""
Guardrails Module

Purpose:
- Provide lightweight safety and validation utilities for user input and requests.
- Enforce basic prompt-injection filtering, ticker validation, domain allowlisting,
  and simple time-budget limiting for long-running operations.

Key Components:
- DANGEROUS_PATTERNS: Regex patterns used to redact unsafe instructions.
- TICKER_RE: Regex to validate common stock ticker formats (with optional suffix).
- sanitize_user_input: Redacts unsafe phrases and trims input.
- validate_ticker: Normalizes and validates ticker symbols.
- domain_allowed: Checks if all provided URLs are within an allowlist.
- RateLimiter: Enforces a soft execution deadline (wall-clock based).
- AnalyzeRequest: Pydantic model that validates inbound analysis requests.
"""

import re
import time
from typing import Iterable

from pydantic import BaseModel, field_validator

from core.config import get_settings

# Basic patterns that should be redacted from user-controlled text.
# Notes:
# - (?i) makes each pattern case-insensitive.
# - These are intentionally conservative and easily extensible.
DANGEROUS_PATTERNS = [
    r"(?i)ignore (all|previous) instructions",
    r"(?i)system prompt",
    r"(?i)exfiltrate|leak|expose keys",
    r"(?i)rm -rf|shutdown|format disk",
]

# Accepts common ticker formats:
#   - Pure alphanumeric (1–6 chars), e.g., "AAPL", "MSFT", "PETR4"
#   - Optional market suffix after a dot, e.g., "BBAS3.SA", "BRK.B"
TICKER_RE = re.compile(r"^[A-Z0-9]{1,6}(?:\.[A-Z]{1,4})?$")


def sanitize_user_input(text: str) -> str:
    """
    Redact unsafe phrases and return a trimmed input string.

    Steps:
    1) Apply each redaction regex to the input text.
    2) Replace matches with a literal "[filtered]" marker.
    3) Trim trailing/leading whitespace.

    Args:
        text: Raw user-provided input.

    Returns:
        A sanitized string safe for further processing.
    """
    for pat in DANGEROUS_PATTERNS:
        text = re.sub(pat, "[filtered]", text)
    return text.strip()


def validate_ticker(ticker: str) -> str:
    """
    Normalize and validate a stock ticker symbol.

    Normalization:
        - Strips whitespace.
        - Converts to uppercase.

    Validation:
        - Must match TICKER_RE (e.g., "AAPL", "BBAS3.SA", "BRK.B").

    Args:
        ticker: The input ticker symbol.

    Returns:
        A standardized, validated ticker string.

    Raises:
        ValueError: If the ticker does not match the expected pattern.
    """
    t = ticker.strip().upper()
    if not TICKER_RE.match(t):
        raise ValueError("Ticker must be like AAPL or BBAS3.SA")
    return t


def domain_allowed(urls: Iterable[str]) -> bool:
    """
    Verify that each URL contains an allowed domain substring.

    Implementation note:
    - This is a lightweight containment check (substring match).
      For stricter validation, consider parsing with urllib.parse.urlparse
      and comparing the netloc against the allowlist.

    Args:
        urls: Iterable of URL strings to evaluate.

    Returns:
        True if every URL matches at least one allowed domain; otherwise False.
    """
    allowed = {d.strip() for d in get_settings().ALLOWED_WEB_DOMAINS.split(",")}
    return all(any(dom in u for dom in allowed) for u in urls)


class RateLimiter:
    """
    Simple wall-clock deadline guard.

    Usage:
        rl = RateLimiter(budget_seconds=30)
        ...
        rl.check()  # Call periodically; raises if time is exceeded.

    Attributes:
        deadline: Epoch timestamp when the time budget expires.
    """

    def __init__(self, budget_seconds: int):
        self.deadline = time.time() + budget_seconds

    def check(self) -> None:
        """
        Raise TimeoutError if the current time exceeds the stored deadline.

        Raises:
            TimeoutError: When the allotted time budget has been exceeded.
        """
        if time.time() > self.deadline:
            raise TimeoutError("Time budget exceeded by guardrails")


class AnalyzeRequest(BaseModel):
    """
    Input schema for an analysis operation.

    Fields:
        ticker: Stock ticker symbol, validated via `validate_ticker`.
        prompt: Free-form analysis prompt, sanitized and length-checked.
    """

    ticker: str
    prompt: str

    @field_validator("ticker")
    @classmethod
    def _v_ticker(cls, v: str) -> str:
        """Normalize and validate the ticker field."""
        return validate_ticker(v)

    @field_validator("prompt")
    @classmethod
    def _v_prompt(cls, v: str) -> str:
        """
        Sanitize and length-guard the prompt.

        - Applies redaction for unsafe patterns.
        - Enforces a rough character cap aligned with MAX_INPUT_TOKENS.

        Raises:
            ValueError: If the sanitized prompt exceeds the configured size limit.
        """
        s = sanitize_user_input(v)
        # Rough character cap: ~4 chars/token as a conservative approximation.
        if len(s) > get_settings().MAX_INPUT_TOKENS * 4:
            raise ValueError("Prompt too long")
        return s
