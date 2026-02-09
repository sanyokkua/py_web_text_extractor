"""MarkItDown text extraction module.

Provides text extraction from web pages using the MarkItDown library.
"""

import logging

from markitdown import MarkItDown

from py_web_text_extractor.exception.exceptions import MarkItDownExtractionException

logger = logging.getLogger(__name__)


def extract_text(url: str) -> str:
    r"""Extract text content from a web page using MarkItDown.

    Args:
        url: HTTP/HTTPS URL to extract text from.

    Returns:
        Extracted text content from the web page.

    Raises:
        MarkItDownExtractionException: If extraction fails due to network issues,
            invalid HTML, or other MarkItDown processing errors.

    Examples:
        >>> extract_text("https://example.com")
        "Example Domain\\n\\nThis domain is for use in illustrative examples..."

        >>> extract_text("https://news.example.com/article")
        "Article Title\\n\\nThe main content of the article..."
    """
    logger.debug("Starting MarkItDown extraction for URL: %s", url)

    try:
        md = MarkItDown()
        text = md.convert(url)
        extracted_text = text.text_content
        logger.info("Successfully extracted text from %s using MarkItDown", url)
        return extracted_text
    except Exception as e:
        logger.warning("MarkItDown extraction failed for %s: %s", url, e)
        raise MarkItDownExtractionException(f"MarkItDown extraction failed for {url}: {e!s}") from e
