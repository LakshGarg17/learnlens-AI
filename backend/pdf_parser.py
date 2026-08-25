"""
PDF Parser module for LearnLens AI.
Handles PDF byte ingestion, page-by-page text extraction, metadata gathering,
and graceful error handling for corrupted, empty, or scanned image-only PDFs.
"""

import io
from typing import Dict, Any
from pypdf import PdfReader
from pypdf.errors import PdfReadError


class PDFExtractionError(Exception):
    """Custom exception raised when PDF parsing or text extraction fails."""
    pass


def extract_text_from_pdf(file_bytes: bytes, filename: str = "document.pdf") -> Dict[str, Any]:
    """
    Extract text content and metadata from raw PDF bytes.

    Args:
        file_bytes: Raw binary content of the uploaded PDF file.
        filename: Original name of the uploaded file.

    Returns:
        Dict containing:
            - filename (str): Name of the file
            - page_count (int): Total number of pages
            - full_text (str): Concatenated text across all pages
            - preview (str): First ~500 characters of the extracted text

    Raises:
        PDFExtractionError: If the PDF is corrupted, empty, encrypted,
                            or contains no extractable text.
    """
    if not file_bytes or len(file_bytes) == 0:
        raise PDFExtractionError("The uploaded file is empty.")

    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
    except PdfReadError as e:
        raise PDFExtractionError(f"Could not read PDF file. It may be corrupted: {str(e)}")
    except Exception as e:
        raise PDFExtractionError(f"Failed to open PDF document: {str(e)}")

    if reader.is_encrypted:
        try:
            # Attempt to decrypt with empty password if possible
            decrypted = reader.decrypt("")
            if decrypted == 0:
                raise PDFExtractionError("The PDF document is password-protected and encrypted.")
        except Exception:
            raise PDFExtractionError("The PDF document is password-protected and encrypted.")

    page_count = len(reader.pages)
    if page_count == 0:
        raise PDFExtractionError("The PDF document contains no pages.")

    extracted_pages = []
    for page_idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                extracted_pages.append(text.strip())
        except Exception as e:
            # Continue extracting remaining pages if a single page fails
            continue

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise PDFExtractionError(
            "No readable text found in the PDF. The document might be scanned, image-only, or empty."
        )

    # Generate preview (~500 characters)
    preview = full_text[:500]
    if len(full_text) > 500:
        preview += "..."

    return {
        "filename": filename,
        "page_count": page_count,
        "full_text": full_text,
        "preview": preview,
    }
