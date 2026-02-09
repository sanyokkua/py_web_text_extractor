"""Input validation utilities."""

import re
from urllib.parse import urlparse


def is_blank_string(value: str | None) -> bool:
    """Check if a string is None, empty, or whitespace-only.

    Args:
        value: String to check. May be None.

    Returns:
        True if value is None or contains no non-whitespace characters.

    Examples:
        >>> is_blank_string(None)
        True
        >>> is_blank_string("")
        True
        >>> is_blank_string("   ")
        True
        >>> is_blank_string("hello")
        False
    """
    return value is None or len(value.strip()) == 0


def is_valid_url(value: str | None) -> bool:
    """Validate HTTP/HTTPS URL format.

    Args:
        value: URL string to validate. Must start with http:// or https://
            and contain no whitespace characters.

    Returns:
        True if value is a properly formatted HTTP/HTTPS URL with scheme and netloc.

    Examples:
        >>> is_valid_url("https://example.com")
        True
        >>> is_valid_url("http://sub.example.com/path")
        True
        >>> is_blank_string("example.com")
        True
        >>> is_valid_url("")
        False
        >>> is_valid_url(None)
        False
        >>> is_valid_url("ftp://example.com")
        False
    """
    if value is None:
        return False
    if not isinstance(value, str):
        return False
    if is_blank_string(value) or re.search(r"\s", value):
        return False
    if not (value.startswith("http://") or value.startswith("https://")):
        return False

    try:
        result = urlparse(value)
        return bool(result.scheme and result.netloc)
    except ValueError:
        return False
