"""
Main text extraction service that coordinates between different extraction methods.

This module provides the primary interface for extracting text content from web pages,
using a fallback strategy between MarkItDown and Trafilatura libraries.
"""

import logging
from typing import override

import py_web_text_extractor.service.markitdown_extractor as mk_extractor
import py_web_text_extractor.service.trafilatura_extractor as tr_extractor
from py_web_text_extractor.abstract.extractor import Extractor
from py_web_text_extractor.exception.exceptions import TextExtractionFailure, UrlIsNotValidException
from py_web_text_extractor.tools.validation import is_blank_string, is_valid_url

# Configure logging
logger = logging.getLogger(__name__)


class ExtractorService(Extractor):
    """
    Main text extraction service implementing a fallback strategy.

    This service attempts to extract text using MarkItDown first, and falls back
    to Trafilatura if the first method fails. If both methods fail, a
    TextExtractionFailure exception is raised.
    """

    @override
    def extract_text_from_page(self, url: str) -> str:
        """
        Extract text content from a web page using a fallback strategy.

        Args:
            url: The URL of the web page to extract text from.

        Returns:
            The extracted text content as a string.

        Raises:
            UrlIsNotValidException: If the provided URL is invalid.
            TextExtractionFailure: If both extraction methods fail.

        Example:
            >>> service = ExtractorService()
            >>> text = service.extract_text_from_page("https://example.com")
            "Example Domain\\n\\nThis domain is for use in illustrative examples..."
        """
        if not isinstance(url, str):
            logger.debug(f"Non-string URL provided: {url}")
            raise UrlIsNotValidException(f"URL must be a string, got {type(url).__name__}")

        if is_blank_string(url):
            logger.debug("Empty or blank URL provided")
            raise UrlIsNotValidException("URL cannot be empty or blank")

        if not is_valid_url(url):
            logger.debug(f"Invalid URL provided: {url}")
            raise UrlIsNotValidException(f"Invalid URL: {url}")

        try:
            logger.debug(f"Attempting to extract text from {url} using MarkItDown")
            return mk_extractor.extract_text(url)
        except mk_extractor.MarkItDownExtractionException as e:
            logger.info(f"MarkItDown extraction failed for {url}: {e!s}. Falling back to Trafilatura")
            pass  # Fall back to trafilatura

        try:
            logger.debug(f"Attempting to extract text from {url} using Trafilatura")
            return tr_extractor.extract_text(url)
        except tr_extractor.TrafilaturaExtractionException as e:
            logger.warning(f"Trafilatura extraction failed for {url}: {e!s}. No more fallback options available")
            pass  # No more fallback options

        logger.error(f"Failed to extract text from {url} using both MarkItDown and Trafilatura")
        raise TextExtractionFailure(f"Failed to extract text from {url} using both MarkItDown and Trafilatura")

    @override
    def extract_text_from_page_safe(self, url: str) -> str:
        """
        Extract text content with the same behavior as extract_text_from_page.

        This method currently has the same implementation as extract_text_from_page,
        but could be enhanced in the future to provide additional safety features
        such as retry logic, caching, or more graceful error handling.

        Args:
            url: The URL of the web page to extract text from.

        Returns:
            The extracted text content as a string. On Error returns empty string.
        """
        try:
            return self.extract_text_from_page(url)
        except Exception:
            logger.warning("Failed to extract text")
            return ""
