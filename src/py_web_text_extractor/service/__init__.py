"""Text extraction services for the py_web_text_extractor library.

This module contains the core service implementations for web text extraction,
including the main ExtractorService with fallback strategy and individual
extractor implementations for different libraries.
"""

from py_web_text_extractor.service.extractor_service import ExtractorService
from py_web_text_extractor.service.markitdown_extractor import extract_text as markitdown_extract
from py_web_text_extractor.service.trafilatura_extractor import extract_text as trafilatura_extract

__all__ = ["ExtractorService", "markitdown_extract", "trafilatura_extract"]
