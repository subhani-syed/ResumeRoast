import re
from typing import Dict, List, Tuple


def redact_resume_text(text: str) -> str:
    """
    Redacts URLs, phone numbers, and links from resume text.

    Args:
        text: Extracted resume text

    Returns:
        Redacted text with URLs and phone numbers replaced
    """
    redacted_text = text

    patterns = {
        'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
        'domain': r'(?:www\.)?(?:linkedin|github|twitter|x|facebook|instagram|portfolio|blog)\.com/[\w\-\.]+',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone_intl': r'\+?91?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        'phone_dots': r'\d{3}\.\d{3}\.\d{4}',
        'phone_dashes': r'\d{3}-\d{3}-\d{4}',
        'phone_parens': r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
    }

    redacted_text = re.sub(patterns['url'], '[URL]', redacted_text, flags=re.IGNORECASE)
    redacted_text = re.sub(patterns['domain'], '[URL]', redacted_text, flags=re.IGNORECASE)
    redacted_text = re.sub(patterns['email'], '[EMAIL]', redacted_text, flags=re.IGNORECASE)

    redacted_text = re.sub(patterns['phone_intl'], '[PHONE]', redacted_text)
    redacted_text = re.sub(patterns['phone_dots'], '[PHONE]', redacted_text)
    redacted_text = re.sub(patterns['phone_dashes'], '[PHONE]', redacted_text)
    redacted_text = re.sub(patterns['phone_parens'], '[PHONE]', redacted_text)

    return redacted_text


def sanitize_input(text: str, max_length: int = 100) -> str:
    """
    Sanitize user input to prevent prompt injection attacks.

    Args:
        text (str): Raw user input to sanitize.
        max_length (int): Maximum character limit. Defaults to 100.

    Returns:
        str: Sanitized and truncated input string.
    """
    text = re.sub(r'(ignore|disregard|forget|override).{0,30}(instructions?|prompt|above)',
                  '', text, flags=re.IGNORECASE)
    text = re.sub(r'[#*`<>{}\[\]]{3,}', '', text)
    return text.strip()[:max_length]
