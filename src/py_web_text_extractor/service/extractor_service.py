"""Web text extraction service with fallback strategy.

Provides a unified interface for extracting clean text content from web pages
using MarkItDown (primary) and Trafilatura (fallback) extraction methods.
"""

import logging
from typing import override

import py_web_text_extractor.service.markitdown_extractor as mk_extractor
import py_web_text_extractor.service.trafilatura_extractor as tr_extractor
from py_web_text_extractor.abstract.extractor import Extractor
from py_web_text_extractor.exception.exceptions import (
    MarkItDownExtractionException,
    TextExtractionFailure,
    TrafilaturaExtractionException,
    UrlIsNotValidException,
)
from py_web_text_extractor.tools.validation import is_blank_string, is_valid_url

logger = logging.getLogger(__name__)


class ExtractorService(Extractor):
    """Text extraction service with MarkItDown/Trafilatura fallback strategy."""

    @override
    def extract_text_from_page(self, url: str) -> str:
        """Extract text content from a web page.

        Attempts extraction using MarkItDown first, falling back to Trafilatura
        if the primary method fails. Raises an exception if both methods fail.

        Args:
            url: HTTP/HTTPS URL to extract text from. Must be a non-empty string
                starting with http:// or https://.

        Returns:
            Cleaned text content from the web page.

        Raises:
            UrlIsNotValidException: If url is None, empty, or not a valid HTTP/HTTPS URL.
            TextExtractionFailure: If both extraction methods fail.

        Examples:
            >>> service = ExtractorService()
            >>> text = service.extract_text_from_page("https://example.com")
            >>> len(text) > 0
            True
        """
        if not isinstance(url, str):
            logger.debug("Non-string URL provided: %s", url)
            raise UrlIsNotValidException(f"URL must be a string, got {type(url).__name__}")

        if is_blank_string(url):
            logger.debug("Empty or blank URL provided")
            raise UrlIsNotValidException("URL cannot be empty or blank")

        if not is_valid_url(url):
            logger.debug("Invalid URL provided: %s", url)
            raise UrlIsNotValidException(f"Invalid URL: {url}")

        try:
            logger.debug("Attempting to extract text from %s using MarkItDown", url)
            return mk_extractor.extract_text(url)
        except MarkItDownExtractionException as e:
            logger.info("MarkItDown extraction failed for %s: %s. Falling back to Trafilatura", url, e)

        try:
            logger.debug("Attempting to extract text from %s using Trafilatura", url)
            return tr_extractor.extract_text(url)
        except TrafilaturaExtractionException as e:
            logger.warning("Trafilatura extraction failed for %s: %s", url, e)

        error_msg = f"Failed to extract text from {url} using both MarkItDown and Trafilatura"
        logger.error(error_msg)
        raise TextExtractionFailure(error_msg)

    @override
    def extract_text_from_page_safe(self, url: str) -> str:
        """Extract text content with graceful error handling.

        Returns empty string on any failure instead of raising exceptions.
        Suitable for batch processing where individual failures should not
        interrupt the overall workflow.

        Args:
            url: URL to extract text from (any value accepted).

        Returns:
            Extracted text if successful, empty string otherwise.

        Examples:
            >>> service = ExtractorService()
            >>> text = service.extract_text_from_page_safe("https://example.com")
            >>> isinstance(text, str)
            True

            >>> service.extract_text_from_page_safe("invalid-url")
            ''
        """
        try:
            return self.extract_text_from_page(url)
        except UrlIsNotValidException as e:
            logger.warning("Invalid URL provided: %s", e)
            return ""
        except TextExtractionFailure as e:
            logger.warning("Text extraction failed: %s", e)
            return ""
        except Exception as e:
            logger.warning("Unexpected error during text extraction: %s", e)
            return ""
