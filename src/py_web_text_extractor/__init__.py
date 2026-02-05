"""
py_web_text_extractor - A library for extracting text content from web pages.

This library provides a unified interface for extracting text content from web pages
using multiple extraction methods with automatic fallback.
"""

from py_web_text_extractor.main import create_extractor_service, ExtractorService, Extractor
from py_web_text_extractor.exception.exceptions import (
    TextExtractionError,
    UrlIsNotValidException,
    MarkItDownExtractionException,
    TrafilaturaExtractionException,
    TextExtractionFailure,
)
from py_web_text_extractor.tools.validation import is_valid_url, is_blank_string

__version__ = "0.1.0"

__all__ = [
    "create_extractor_service",
    "ExtractorService", 
    "Extractor",
    "TextExtractionError",
    "UrlIsNotValidException",
    "MarkItDownExtractionException",
    "TrafilaturaExtractionException",
    "TextExtractionFailure",
    "is_valid_url",
    "is_blank_string",
]
