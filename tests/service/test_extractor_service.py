"""
Unit tests for the ExtractorService.

This module contains unit tests for the ExtractorService, focusing on its
fallback logic and error handling. The tests use mocking to isolate the
service from its dependencies (MarkItDown and Trafilatura extractors).
"""

from unittest.mock import MagicMock, patch

import pytest

from py_web_text_extractor.exception.exceptions import (
    MarkItDownExtractionException,
    TextExtractionFailure,
    TrafilaturaExtractionException,
    UrlIsNotValidException,
)
from py_web_text_extractor.service.extractor_service import ExtractorService


@pytest.fixture
def extractor_service():
    """Provides an instance of ExtractorService for testing."""
    return ExtractorService()


class TestExtractorService:
    """Test suite for the ExtractorService."""

    VALID_URL = "https://example.com"
    MARKITDOWN_SUCCESS_TEXT = "Text from MarkItDown"
    TRAFILATURA_SUCCESS_TEXT = "Text from Trafilatura"

    # --- Tests for extract_text_from_page ---

    @patch("py_web_text_extractor.service.extractor_service.tr_extractor")
    @patch("py_web_text_extractor.service.extractor_service.mk_extractor")
    def test_extract_text_from_page_success_with_markitdown(
        self, mock_mk_extractor: MagicMock, mock_tr_extractor: MagicMock, extractor_service: ExtractorService
    ):
        """
        GIVEN a valid URL
        WHEN extract_text_from_page is called and MarkItDown succeeds
        THEN it should return the text from MarkItDown and not call Trafilatura.
        """
        # ARRANGE
        mock_mk_extractor.extract_text.return_value = self.MARKITDOWN_SUCCESS_TEXT

        # ACT
        result = extractor_service.extract_text_from_page(self.VALID_URL)

        # ASSERT
        assert result == self.MARKITDOWN_SUCCESS_TEXT
        mock_mk_extractor.extract_text.assert_called_once_with(self.VALID_URL)
        mock_tr_extractor.extract_text.assert_not_called()

    @patch("py_web_text_extractor.service.extractor_service.tr_extractor")
    @patch("py_web_text_extractor.service.extractor_service.mk_extractor")
    def test_extract_text_from_page_fallback_to_trafilatura_success(
        self, mock_mk_extractor: MagicMock, mock_tr_extractor: MagicMock, extractor_service: ExtractorService
    ):
        """
        GIVEN a valid URL
        WHEN extract_text_from_page is called and MarkItDown fails
        THEN it should fall back to Trafilatura and return its text.
        """
        # ARRANGE
        mock_mk_extractor.extract_text.side_effect = MarkItDownExtractionException("MarkItDown failed")
        mock_tr_extractor.extract_text.return_value = self.TRAFILATURA_SUCCESS_TEXT

        # ACT
        result = extractor_service.extract_text_from_page(self.VALID_URL)

        # ASSERT
        assert result == self.TRAFILATURA_SUCCESS_TEXT
        mock_mk_extractor.extract_text.assert_called_once_with(self.VALID_URL)
        mock_tr_extractor.extract_text.assert_called_once_with(self.VALID_URL)

    @patch("py_web_text_extractor.service.extractor_service.tr_extractor")
    @patch("py_web_text_extractor.service.extractor_service.mk_extractor")
    def test_extract_text_from_page_both_extractors_fail(
        self, mock_mk_extractor: MagicMock, mock_tr_extractor: MagicMock, extractor_service: ExtractorService
    ):
        """
        GIVEN a valid URL
        WHEN both MarkItDown and Trafilatura extractors fail
        THEN it should raise a TextExtractionFailure.
        """
        # ARRANGE
        mock_mk_extractor.extract_text.side_effect = MarkItDownExtractionException("MarkItDown failed")
        mock_tr_extractor.extract_text.side_effect = TrafilaturaExtractionException("Trafilatura failed")

        # ACT & ASSERT
        with pytest.raises(TextExtractionFailure):
            extractor_service.extract_text_from_page(self.VALID_URL)

        mock_mk_extractor.extract_text.assert_called_once_with(self.VALID_URL)
        mock_tr_extractor.extract_text.assert_called_once_with(self.VALID_URL)

    @pytest.mark.parametrize(
        "invalid_url",
        [
            None,
            "",
            "   ",
            "not_a_valid_url",
            "ftp://example.com",
            12345,
        ],
    )
    def test_extract_text_from_page_invalid_url(self, invalid_url, extractor_service: ExtractorService):
        """
        GIVEN an invalid URL
        WHEN extract_text_from_page is called
        THEN it should raise UrlIsNotValidException.
        """
        # ACT & ASSERT
        with pytest.raises(UrlIsNotValidException):
            extractor_service.extract_text_from_page(invalid_url)

    # --- Tests for extract_text_from_page_safe ---

    @patch.object(ExtractorService, "extract_text_from_page")
    def test_extract_text_from_page_safe_success(self, mock_extract: MagicMock, extractor_service: ExtractorService):
        """
        GIVEN a valid URL
        WHEN extract_text_from_page_safe is called and extraction succeeds
        THEN it should return the extracted text.
        """
        # ARRANGE
        mock_extract.return_value = self.MARKITDOWN_SUCCESS_TEXT

        # ACT
        result = extractor_service.extract_text_from_page_safe(self.VALID_URL)

        # ASSERT
        assert result == self.MARKITDOWN_SUCCESS_TEXT
        mock_extract.assert_called_once_with(self.VALID_URL)

    @pytest.mark.parametrize(
        "exception",
        [
            UrlIsNotValidException("Invalid URL"),
            TextExtractionFailure("Extraction failed"),
            Exception("An unexpected error"),
        ],
    )
    @patch.object(ExtractorService, "extract_text_from_page")
    def test_extract_text_from_page_safe_failures(
        self, mock_extract: MagicMock, exception: Exception, extractor_service: ExtractorService
    ):
        """
        GIVEN any URL
        WHEN extract_text_from_page_safe is called and an exception occurs
        THEN it should return an empty string.
        """
        # ARRANGE
        mock_extract.side_effect = exception

        # ACT
        result = extractor_service.extract_text_from_page_safe(self.VALID_URL)

        # ASSERT
        assert result == ""
        mock_extract.assert_called_once_with(self.VALID_URL)
