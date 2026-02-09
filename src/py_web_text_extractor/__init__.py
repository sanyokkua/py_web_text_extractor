"""Extract clean text content from web pages."""

from py_web_text_extractor.exception.exceptions import (
    MarkItDownExtractionException,
    TextExtractionError,
    TextExtractionFailure,
    TrafilaturaExtractionException,
    UrlIsNotValidException,
)
from py_web_text_extractor.main import Extractor, ExtractorService, app, create_extractor_service
from py_web_text_extractor.tools.validation import is_blank_string, is_valid_url

__version__ = "0.1.0"

__all__ = [
    "Extractor",
    "ExtractorService",
    "MarkItDownExtractionException",
    "TextExtractionError",
    "TextExtractionFailure",
    "TrafilaturaExtractionException",
    "UrlIsNotValidException",
    "app",
    "create_extractor_service",
    "is_blank_string",
    "is_valid_url",
]
