import sys
from unittest.mock import MagicMock, patch
import pytest

# Mock modules that might not be available or cause issues on import
sys.modules['streamlit'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

# Import the functions to test
from app import extract_text_from_pdf, process_uploaded_file

def test_extract_text_from_pdf():
    # Create a mock for the PdfReader
    mock_pdf_reader = MagicMock()

    # Mock pages with an extract_text method
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Hello "
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "World!"

    # Setup the reader to return these pages
    mock_pdf_reader.pages = [mock_page1, mock_page2]

    with patch('PyPDF2.PdfReader', return_value=mock_pdf_reader):
        # We can pass any dummy file object or path since we mocked the reader
        result = extract_text_from_pdf("dummy.pdf")

    assert result == "Hello World!"
    # Verify the extract_text method was called on each page
    mock_page1.extract_text.assert_called_once()
    mock_page2.extract_text.assert_called_once()


def test_process_uploaded_file_pdf():
    # Mock uploaded file for PDF
    mock_file = MagicMock()
    mock_file.type = "application/pdf"

    with patch('app.extract_text_from_pdf', return_value="Extracted PDF Text") as mock_extract:
        result = process_uploaded_file(mock_file)

    assert result == "Extracted PDF Text"
    mock_extract.assert_called_once_with(mock_file)


def test_process_uploaded_file_txt():
    # Mock uploaded file for TXT
    mock_file = MagicMock()
    mock_file.type = "text/plain"
    # Mock the getvalue() method which returns bytes
    mock_file.getvalue.return_value = b"Hello from TXT"

    result = process_uploaded_file(mock_file)

    assert result == "Hello from TXT"
    mock_file.getvalue.assert_called_once()


def test_process_uploaded_file_unsupported():
    # Mock uploaded file for an unsupported type
    mock_file = MagicMock()
    mock_file.type = "image/png"

    result = process_uploaded_file(mock_file)

    assert result == "Unsupported file type. Please upload a TXT or PDF file."
