"""Trafilatura text extraction module.

Provides text extraction from web pages using the Trafilatura library.
"""

import logging

from trafilatura import extract, fetch_url

from py_web_text_extractor.exception.exceptions import TrafilaturaExtractionException

logger = logging.getLogger(__name__)


def extract_text(url: str) -> str:
    r"""Extract text content from a web page using Trafilatura.

    Args:
        url: HTTP/HTTPS URL to extract text from.

    Returns:
        Extracted text content in markdown format. Returns an empty string if
        Trafilatura finds no extractable content.

    Raises:
        TrafilaturaExtractionException: If content cannot be fetched or processed.

    Examples:
        >>> extract_text("https://example.com")
        "# Example Domain\\n\\nThis domain is for use in illustrative examples..."

        >>> extract_text("https://blog.example.com/post")
        "# Post Title\\n\\n## Section Header\\n\\nMain content..."
    """
    logger.debug("Starting Trafilatura extraction for URL: %s", url)

    try:
        content = fetch_url(url)
        if content is None:
            logger.warning("Failed to fetch content from %s using Trafilatura", url)
            raise TrafilaturaExtractionException(f"Failed to fetch content from {url}")

        text = extract(content, output_format="markdown")
        extracted_text = text or ""

        if extracted_text:
            logger.info("Successfully extracted text from %s using Trafilatura", url)
        else:
            logger.debug("No text content found for %s using Trafilatura", url)

        return extracted_text
    except Exception as e:
        logger.warning("Trafilatura extraction failed for %s: %s", url, e)
        raise TrafilaturaExtractionException(f"Trafilatura extraction failed for {url}: {e!s}") from e
