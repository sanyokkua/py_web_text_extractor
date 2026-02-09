"""Text extraction service factory and entry points."""

from py_web_text_extractor.cli import app
from py_web_text_extractor.service.extractor_service import ExtractorService


def create_extractor_service() -> ExtractorService:
    """Create a new text extraction service instance.

    Returns:
        Configured ExtractorService ready for text extraction.

    Examples:
        >>> from py_web_text_extractor import create_extractor_service
        >>> service = create_extractor_service()
        >>> text = service.extract_text_from_page("https://example.com")
        >>> len(text) > 0
        True
    """
    return ExtractorService()


# Convenience alias for the main service class
Extractor = ExtractorService


__all__ = ["Extractor", "ExtractorService", "app", "create_extractor_service"]
