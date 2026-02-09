"""
Unit tests for the validation tools.

This module contains tests for the functions in the
`py_web_text_extractor.tools.validation` module.
It uses pytest for organizing and running the tests, covering various
edge cases and common scenarios to ensure the validation functions
are robust and reliable.
"""

import pytest

from py_web_text_extractor.tools.validation import is_blank_string, is_valid_url


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, True),
        ("", True),
        (" ", True),
        ("   ", True),
        ("\t", True),
        ("\n", True),
        ("\t\n", True),
        ("hello", False),
        (" hello ", False),
        ("a", False),
        ("123", False),
    ],
)
def test_is_blank_string(value: str | None, expected: bool):
    """
    Test the is_blank_string function with various inputs.

    Args:
        value: The input string to test.
        expected: The expected boolean result.
    """
    assert is_blank_string(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        # Valid cases
        ("http://example.com", True),
        ("https://example.com", True),
        ("https://www.example.com", True),
        ("http://sub.example.com", True),
        ("https://example.com/path", True),
        ("https://example.com/path/to/resource", True),
        ("http://example.com?query=123", True),
        ("https://example.com/path?query=value&another=true", True),
        ("http://example.com:8080", True),
        ("https://user:pass@example.com", True),
        ("http://127.0.0.1", True),
        ("https://192.168.1.1/path", True),
        # Invalid cases
        (None, False),
        ("", False),
        (" ", False),
        ("   ", False),
        ("example.com", False),
        ("www.example.com", False),
        ("http//example.com", False),
        ("https://", False),
        ("http://", False),
        ("ftp://example.com", False),
        ("javascript:alert('xss')", False),
        ("mailto:user@example.com", False),
        ("http:// example.com", False),
        ("http:///path", False),
        ("http://?query", False),
        ("http://example.com\n", False),
        # Non-string input
        (123, False),
        ([], False),
        ({}, False),
    ],
)
def test_is_valid_url(value, expected: bool):
    """
    Test the is_valid_url function with various inputs.

    Args:
        value: The input URL to test.
        expected: The expected boolean result.
    """
    assert is_valid_url(value) == expected
