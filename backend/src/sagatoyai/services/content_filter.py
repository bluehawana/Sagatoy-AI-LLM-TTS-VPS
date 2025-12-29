"""Content filtering for child safety."""

import logging
import re

logger = logging.getLogger(__name__)

INAPPROPRIATE_PATTERNS = [
    r"\b(kill|murder|death|die|blood|weapon|gun|knife)\b",
    r"\b(hate|stupid|idiot|dumb)\b",
    r"\b(sex|porn|nude)\b",
    r"\b(drug|alcohol|beer|wine)\b",
]

COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE)
                     for pattern in INAPPROPRIATE_PATTERNS]


def contains_inappropriate_content(text: str) -> bool:
    """Check if text contains inappropriate content for children."""
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            logger.warning(
                f"Inappropriate content detected: {pattern.pattern}")
            return True
    return False


def filter_content(text: str) -> str:
    """Filter inappropriate content from text."""
    if contains_inappropriate_content(text):
        return "Let's talk about something fun and happy instead!"
    return text
