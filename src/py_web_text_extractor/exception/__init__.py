"""Exception classes for py_web_text_extractor library."""

from py_web_text_extractor.exception.exceptions import (
    TextExtractionError,
    UrlIsNotValidException,
    MarkItDownExtractionException,
    TrafilaturaExtractionException,
    TextExtractionFailure,
)

__all__ = [
    "TextExtractionError",
    "UrlIsNotValidException",
    "MarkItDownExtractionException",
    "TrafilaturaExtractionException",
    "TextExtractionFailure",
]