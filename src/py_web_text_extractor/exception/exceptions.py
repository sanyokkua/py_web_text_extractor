class TextExtractionError(Exception):
    """Base exception class for all text extraction errors."""


class UrlIsNotValidException(TextExtractionError):
    """Raised when the provided URL is invalid or malformed."""


class MarkItDownExtractionException(TextExtractionError):
    """
    Raised when text extraction fails using the MarkItDown library.

    This exception indicates that the MarkItDown extraction process encountered
    an error while attempting to extract text content from a web page.
    """


class TrafilaturaExtractionException(TextExtractionError):
    """
    Raised when text extraction fails using the Trafilatura library.

    This exception indicates that the Trafilatura extraction process encountered
    an error while attempting to extract text content from a web page.
    """


class TextExtractionFailure(TextExtractionError):
    """
    Raised when all text extraction methods fail.

    This exception is raised when both MarkItDown and Trafilatura extraction
    methods have been attempted and both have failed to extract text from
    the provided web page URL.
    """
