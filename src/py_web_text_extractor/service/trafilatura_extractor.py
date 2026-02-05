from trafilatura import extract, fetch_url

from py_web_text_extractor.exception.exceptions import TrafilaturaExtractionException


def extract_text(url: str) -> str:
    """
    Extract text content from a web page using Trafilatura library.

    Args:
        url: The URL of the web page to extract text from.

    Returns:
        The extracted text content as a string. Returns empty string if no text is found.

    Raises:
        TrafilaturaExtractionException: If text extraction fails using Trafilatura.

    Example:
        >>> extract_text("https://example.com")
        "# Example Domain\\n\\nThis domain is for use in illustrative examples..."
    """
    try:
        content = fetch_url(url)
        text = extract(content, output_format="markdown")
        return text or ""
    except Exception as e:
        raise TrafilaturaExtractionException(f"Trafilatura extraction failed for {url}: {str(e)}")
