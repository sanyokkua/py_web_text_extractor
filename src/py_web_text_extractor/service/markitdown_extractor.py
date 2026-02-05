from markitdown import MarkItDown

from py_web_text_extractor.exception.exceptions import MarkItDownExtractionException


def extract_text(url: str) -> str:
    """
    Extract text content from a web page using MarkItDown library.

    Args:
        url: The URL of the web page to extract text from.

    Returns:
        The extracted text content as a string.

    Raises:
        MarkItDownExtractionException: If text extraction fails using MarkItDown.

    Example:
        >>> extract_text("https://example.com")
        "Example Domain\\n\\nThis domain is for use in illustrative examples..."
    """
    try:
        md = MarkItDown()
        text = md.convert(url)
        return text.text_content
    except Exception as e:
        raise MarkItDownExtractionException(f"MarkItDown extraction failed for {url}: {str(e)}")
