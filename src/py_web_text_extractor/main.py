"""
Main module for py_web_text_extractor library.

This module provides a convenient entry point and factory functions for creating
text extraction services.
"""

from py_web_text_extractor.service.extractor_service import ExtractorService


def create_extractor_service() -> ExtractorService:
    """
    Create a new ExtractorService instance.

    Returns:
        A new instance of ExtractorService ready for text extraction.

    Example:
        >>> service = create_extractor_service()
        >>> text = service.extract_text_from_page("https://example.com")
    """
    return ExtractorService()


# Convenience alias for the main service class
Extractor = ExtractorService


__all__ = ["create_extractor_service", "ExtractorService", "Extractor"]
