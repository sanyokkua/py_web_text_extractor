# py-web-text-extractor

[![CI](https://github.com/sanyokkua/py_web_text_extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/sanyokkua/py_web_text_extractor/actions)
[![PyPI version](https://badge.fury.io/py/py-web-text-extractor.svg)](https://pypi.org/project/py-web-text-extractor/)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool and Python library to extract clean text content from web pages.

## Overview

`py-web-text-extractor` provides a simple interface for extracting the main text content from HTML documents. It can be used as a command-line tool for quick extractions or as a Python library for integration into other applications. The tool uses a fallback strategy, trying `markitdown` first and then `trafilatura` to ensure high reliability.

## Features

- **Dual Extractor Strategy**: Uses `markitdown` as the primary extractor and falls back to `trafilatura` for robustness.
- **CLI and Library Interface**: Can be used as a standalone command-line tool or as a Python library.
- **Error Handling Modes**: Supports a strict mode that raises exceptions on failure and a safe mode that returns an empty string.
- **Modern Python**: Fully typed with Python 3.14+ support.

## Prerequisites

- Python 3.14 or higher.

## Installation

You can install the package using `pip` or `uv`.

### Using pip

```bash
pip install py-web-text-extractor
```

### Using uv

```bash
uv add py-web-text-extractor
```

## Usage

The tool can be used via its command-line interface or as a Python library.

### Command-Line Interface (CLI)

The CLI is the quickest way to extract text from a URL.

**Basic Extraction:**

```bash
py-web-text-extractor https://example.com
```

**Safe Mode:**

In safe mode, the tool will return an empty string and exit gracefully if an error occurs.

```bash
py-web-text-extractor https://example.com --safe
```

**Verbose Mode:**

For troubleshooting, verbose mode provides detailed debug output.

```bash
py-web-text-extractor https://example.com --verbose
```

**CLI Exit Codes:**

| Code | Meaning                |
| ---- | ---------------------- |
| 0    | Success                |
| 1    | No text content found  |
| 2    | Invalid URL            |
| 3    | Text extraction failed |
| 4    | Unexpected error       |


### Python Library

For programmatic use, you can import the `ExtractorService`.

**Quick Start:**

```python
from py_web_text_extractor.service.extractor_service import ExtractorService
from py_web_text_extractor.exception.exceptions import TextExtractionError, UrlIsNotValidException

# Initialize the service
service = ExtractorService()

# Strict mode: raises an exception on failure
try:
    text = service.extract_text_from_page("https://example.com")
    print(text)
except UrlIsNotValidException:
    print("The provided URL is not valid.")
except TextExtractionError as e:
    print(f"Failed to extract text: {e}")

# Safe mode: returns an empty string on failure
text_safe = service.extract_text_from_page_safe("https://invalid-url")
if not text_safe:
    print("Extraction failed or no content found.")

```

## API Reference

### `ExtractorService`

The main class for handling text extraction.

**Methods:**

- **`extract_text_from_page(url: str) -> str`**: Extracts text from the given URL. Raises a `TextExtractionError` or `UrlIsNotValidException` on failure.
- **`extract_text_from_page_safe(url: str) -> str`**: Extracts text from the given URL. Returns an empty string on failure.

### Exceptions

The library uses a set of custom exceptions to allow for specific error handling.

- `TextExtractionError`: Base exception for the library.
- `UrlIsNotValidException`: Raised for invalid URL formats.
- `TextExtractionFailure`: Raised when all extraction attempts fail.
- `MarkItDownExtractionException`: Specific failure from the `markitdown` extractor.
- `TrafilaturaExtractionException`: Specific failure from the `trafilatura` extractor.


## Architecture

The service employs a fallback strategy to maximize reliability:
1.  It first attempts to extract content using `markitdown`.
2.  If `markitdown` fails (e.g., returns a blank string or raises an error), the service automatically retries the extraction using `trafilatura`.
3.  The first successful result is returned. If both extractors fail, an error is raised or an empty string is returned, depending on the mode.

## Testing

To run the test suite, first install the development dependencies and then run `pytest`.

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run linters and type checkers
uv run ruff check .
uv run ruff format .
uv run mypy src/
```

## Python 3.14+ Compatibility Issue

### Problem

In Python 3.13+ and 3.14+, the `pydub` library (a dependency of `markitdown`) contains invalid escape sequences in regular expressions, which causes a `SyntaxError` during import:

```
SyntaxError: "\(" is an invalid escape sequence
```

This issue occurs because Python 3.13+ enforces stricter syntax rules for string literals, treating invalid escape sequences as hard errors instead of warnings.

### Solution

To fix this issue, you need to patch the `pydub/utils.py` file to escape the problematic sequences. This patch is applied automatically in the CI pipeline, but you may need to run it manually in your development environment.

#### Automated Patch Script

Run the following script to automatically locate and patch the `pydub` library:

```bash
#!/bin/bash
# fix_pydub.sh - Patch pydub for Python 3.13+ compatibility

# Find pydub/utils.py without importing it
PYDUB_UTILS=$(find .venv -name "utils.py" -path "*/pydub/utils.py" | head -n1)

if [ -z "$PYDUB_UTILS" ]; then
  echo "⚠️  pydub/utils.py not found, skipping patch"
  exit 0
fi

echo "🔧 Patching: $PYDUB_UTILS"

# Create backup
cp "$PYDUB_UTILS" "${PYDUB_UTILS}.bak"

# Fix all invalid escape sequences
sed -i.bak2 's/\\(/\\\\(/g; s/\\)/\\\\)/g' "$PYDUB_UTILS"

echo "✓ Successfully patched pydub/utils.py"
```

**Usage:**
```bash
chmod +x fix_pydub.sh
./fix_pydub.sh
```

### CI/CD Integration

This patch is automatically applied in the GitHub Actions workflow before running tests. See `.github/workflows/publish.yml` for the implementation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
