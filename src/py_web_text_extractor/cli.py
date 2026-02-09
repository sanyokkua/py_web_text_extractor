"""Command-line interface for web text extraction."""

import logging
import sys

import typer

from py_web_text_extractor.exception.exceptions import (
    TextExtractionError,
    UrlIsNotValidException,
)
from py_web_text_extractor.service.extractor_service import ExtractorService

app = typer.Typer(
    name="py-web-text-extractor",
    help="Extract clean text content from web pages",
    add_completion=False,
    no_args_is_help=True,
)


def _setup_logging(verbose: bool = False) -> None:
    """Configure CLI logging level.

    Args:
        verbose: Enable DEBUG level logging when True; WARNING level when False.
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )


@app.command()
def main(
    url: str,
    safe: bool = False,
    verbose: bool = False,
) -> None:
    """Extract text from a web page.

    Args:
        url: HTTP/HTTPS URL to extract text from.
        safe: Return empty string on error instead of exiting with failure code.
        verbose: Enable debug logging for troubleshooting.

    Exit codes:
        0: Success (text extracted)
        1: No text content found
        2: Invalid URL
        3: Text extraction failed
        4: Unexpected error
    """
    _setup_logging(verbose)

    logger = logging.getLogger(__name__)
    logger.debug("Starting extraction for URL: %s", url)

    try:
        service = ExtractorService()
        text = service.extract_text_from_page_safe(url) if safe else service.extract_text_from_page(url)

        if text:
            print(text)
            sys.exit(0)
        else:
            print("No text content found", file=sys.stderr)
            sys.exit(1)

    except UrlIsNotValidException as e:
        print(f"Error: Invalid URL - {e}", file=sys.stderr)
        sys.exit(2)
    except TextExtractionError as e:
        print(f"Error: Text extraction failed - {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Error: Unexpected error - {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    app()
