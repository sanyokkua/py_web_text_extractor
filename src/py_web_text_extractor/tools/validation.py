"""
Validation utilities for URL and string validation.

This module provides functions for validating URLs and checking for blank strings,
which are used throughout the text extraction process to ensure input quality.
"""

from urllib.parse import urlparse


def is_blank_string(value: str) -> bool:
    """
    Check if a string is blank (None, empty, or whitespace-only).

    Args:
        value: The string to check.

    Returns:
        True if the string is blank, False otherwise.

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


def is_valid_url(value: str) -> bool:
    """
    Validate that a string is a properly formatted HTTP/HTTPS URL.

    Args:
        value: The URL string to validate.

    Returns:
        True if the URL is valid, False otherwise.

    Examples:
        >>> is_valid_url("https://example.com")
        True
        >>> is_valid_url("http://example.com")
        True
        >>> is_valid_url("example.com")
        False
        >>> is_valid_url("")
        False
        >>> is_valid_url(None)
        False
    """
    if value is None:
        return False
    if not isinstance(value, str):
        return False
    if is_blank_string(value):
        return False
    if not (value.startswith("http://") or value.startswith("https://")):
        return False
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
