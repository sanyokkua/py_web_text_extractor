"""Exception classes for the py_web_text_extractor library.

This module exports all custom exception classes used throughout the text
extraction process, providing a consistent error handling mechanism.
"""

from py_web_text_extractor.exception.exceptions import (
    MarkItDownExtractionException,
    TextExtractionError,
    TextExtractionFailure,
    TrafilaturaExtractionException,
    UrlIsNotValidException,
)

__all__ = [
    "MarkItDownExtractionException",
    "TextExtractionError",
    "TextExtractionFailure",
    "TrafilaturaExtractionException",
    "UrlIsNotValidException",
]
