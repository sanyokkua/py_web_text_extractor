"""
Abstract base classes for text extraction services.

This module defines the interface that all text extraction services must implement,
ensuring consistency across different extraction implementations.
"""

from abc import ABC, abstractmethod


class Extractor(ABC):
    """
    Abstract base class for text extraction services.

    All text extraction services must implement these methods to provide
    a consistent interface for extracting text content from web pages.
    """

    @abstractmethod
    def extract_text_from_page_safe(self, url: str) -> str:
        """
        Extract text content from a web page with safe error handling.

        Args:
            url: The URL of the web page to extract text from.

        Returns:
            The extracted text content as a string.
        """

    @abstractmethod
    def extract_text_from_page(self, url: str) -> str:
        """
        Extract text content from a web page.

        Args:
            url: The URL of the web page to extract text from.

        Returns:
            The extracted text content as a string.

        Raises:
            TextExtractionError: If text extraction fails.
        """
