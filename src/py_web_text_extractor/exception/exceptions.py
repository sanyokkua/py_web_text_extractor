"""Custom exceptions for text extraction failures."""


class TextExtractionError(Exception):
    """Base exception for all text extraction errors."""


class UrlIsNotValidException(TextExtractionError):
    """Invalid or malformed URL provided."""


class MarkItDownExtractionException(TextExtractionError):
    """MarkItDown extraction failed."""


class TrafilaturaExtractionException(TextExtractionError):
    """Trafilatura extraction failed."""


class TextExtractionFailure(TextExtractionError):
    """All extraction methods failed for a URL."""
