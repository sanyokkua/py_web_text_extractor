"""
Integration tests for the MarkItDown extractor.

This module contains integration tests for the MarkItDown-based text extraction
service. It uses a live test server to simulate fetching content from real URLs
and verifies that the extractor behaves as expected under various conditions,
including successful extraction, handling of non-HTML content, and server errors.
"""

import pytest

from py_web_text_extractor.exception.exceptions import MarkItDownExtractionException
from py_web_text_extractor.service import markitdown_extractor


def test_extract_text_simple_page(test_server):
    """
    Test text extraction from a simple, valid HTML page.
    """
    url = f"{test_server.base_url}/simple"
    text = markitdown_extractor.extract_text(url)
    assert "This is a simple page." in text


def test_extract_text_complex_page(test_server):
    """
    Test text extraction from a more complex HTML page with boilerplate.
    """
    url = f"{test_server.base_url}/complex"
    text = markitdown_extractor.extract_text(url)
    # Check for presence of key content from the complex page
    assert "Welcome to Our Documentation" in text
    assert "Introduction to Our Amazing Project" in text
    assert "This section provides a general overview of the project" in text
    assert "Key Features" in text
    assert "High-performance data processing" in text
    assert "Installation Guide" in text
    assert "Clone the repository" in text
    assert "uv sync" in text
    assert "Configuration Options" in text
    assert "Your unique API access key" in text
    assert "Remember to keep your API key secure!" in text


def test_extract_text_non_html_content(test_server):
    """
    Test that extraction handles non-HTML content gracefully.
    """
    url = f"{test_server.base_url}/no_html"
    text = markitdown_extractor.extract_text(url)
    assert "This is just a plain text string." in text


def test_extract_text_empty_response(test_server):
    """
    Test that extraction fails for an empty response (204).
    """
    url = f"{test_server.base_url}/empty"
    with pytest.raises(MarkItDownExtractionException):
        markitdown_extractor.extract_text(url)


def test_extract_text_server_error(test_server):
    """
    Test that extraction fails when the server returns a 500 error.
    """
    url = f"{test_server.base_url}/error"
    with pytest.raises(MarkItDownExtractionException):
        markitdown_extractor.extract_text(url)


def test_extract_text_not_found(test_server):
    """
    Test that extraction fails when the page is not found (404).
    """
    url = f"{test_server.base_url}/not_found"
    with pytest.raises(MarkItDownExtractionException):
        markitdown_extractor.extract_text(url)


def test_extract_text_invalid_url():
    """
    Test that extraction fails for a completely invalid URL.
    """
    with pytest.raises(MarkItDownExtractionException):
        markitdown_extractor.extract_text("invalid-url")
