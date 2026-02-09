"""Abstract base classes for text extraction services.

This module defines the interface that all text extraction services must implement,
ensuring consistency across different extraction implementations. The Extractor
abstract base class serves as the foundation for all concrete extraction services,
enforcing a uniform API and behavior contract.

All text extraction services in the py_web_text_extractor library must inherit
from the Extractor ABC and implement its abstract methods to ensure compatibility
with the library's architecture and fallback strategies.
"""

from abc import ABC, abstractmethod


class Extractor(ABC):
    """Abstract base class for text extraction services.

    All text extraction services must implement these methods to provide
    a consistent interface for extracting text content from web pages.

    This ABC defines two core methods:
    - extract_text_from_page(): Main extraction with exception handling
    - extract_text_from_page_safe(): Safe extraction that returns empty string on error

    Implementations should follow these guidelines:
    - Provide comprehensive error handling and logging
    - Support both strict (exception-raising) and safe (error-suppressing) modes
    - Maintain consistent return types and exception patterns
    """

    @abstractmethod
    def extract_text_from_page_safe(self, url: str) -> str:
        r"""Extract text content from a web page with safe error handling.

        This method should implement extraction logic that catches all exceptions
        and returns an empty string on failure, making it suitable for use cases
        where extraction failures should not disrupt application flow.

        Args:
            url: The URL of the web page to extract text from. Should be a
                 valid HTTP/HTTPS URL string.

        Returns:
            The extracted text content as a string if successful.
            An empty string if any error occurs during extraction.

        Example:
            >>> extractor.extract_text_from_page_safe("https://example.com")
            "Example Domain\\n\\nThis domain is for use in illustrative examples..."

            >>> extractor.extract_text_from_page_safe("invalid-url")
            ""  # Returns empty string instead of raising exception
        """

    @abstractmethod
    def extract_text_from_page(self, url: str) -> str:
        r"""Extract text content from a web page.

        This method should implement the main extraction logic with comprehensive
        error handling that raises appropriate exceptions for different failure
        scenarios. It's suitable for use cases where detailed error information
        is needed.

        Args:
            url: The URL of the web page to extract text from. Must be a
                 valid HTTP/HTTPS URL string.

        Returns:
            The extracted text content as a string.

        Raises:
            TextExtractionError: If text extraction fails.
            UrlIsNotValidException: If the provided URL is invalid or malformed.
            MarkItDownExtractionException: If MarkItDown extraction specifically fails.
            TrafilaturaExtractionException: If Trafilatura extraction specifically fails.
            TextExtractionFailure: If all extraction methods fail.

        Example:
            >>> extractor.extract_text_from_page("https://example.com")
            "Example Domain\\n\\nThis domain is for use in illustrative examples..."

            >>> extractor.extract_text_from_page("invalid-url")
            # Raises UrlIsNotValidException
        """
