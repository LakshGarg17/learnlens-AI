"""
Unit and API integration tests for Day 2 PDF Upload & Text Extraction.
"""

import io
from fastapi.testclient import TestClient
from main import app
from pdf_parser import extract_text_from_pdf, PDFExtractionError

client = TestClient(app)


def create_sample_pdf_with_text(text: str) -> bytes:
    """Helper to generate a valid PDF with text in-memory."""
    stream_content = f"BT /F1 14 Tf 50 700 Td ({text}) Tj ET"
    stream_bytes = stream_content.encode("latin-1")
    stream_len = len(stream_bytes)
    
    header = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n"
        b"endobj\n"
        b"4 0 obj\n"
        + f"<< /Length {stream_len} >>\nstream\n".encode("latin-1")
        + stream_bytes
        + b"\nendstream\nendobj\n"
        b"5 0 obj\n"
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000234 00000 n \n"
        b"0000000300 00000 n \n"
        b"trailer\n"
        b"<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n"
        b"380\n"
        b"%%EOF\n"
    )
    return header


def test_valid_pdf_parser():
    sample_text = "Artificial Intelligence is revolutionizing modern education."
    pdf_bytes = create_sample_pdf_with_text(sample_text)
    
    result = extract_text_from_pdf(pdf_bytes, filename="ai_intro.pdf")
    assert result["filename"] == "ai_intro.pdf"
    assert result["page_count"] == 1
    assert "Artificial Intelligence" in result["full_text"]
    assert "Artificial Intelligence" in result["preview"]
    print("[OK] Parser handles valid PDF successfully")


def test_empty_bytes_parser():
    try:
        extract_text_from_pdf(b"", filename="empty.pdf")
        assert False, "Should raise PDFExtractionError"
    except PDFExtractionError as e:
        assert "empty" in str(e).lower()
        print("[OK] Parser rejects empty bytes")


def test_corrupted_bytes_parser():
    try:
        extract_text_from_pdf(b"This is not a PDF at all!", filename="fake.pdf")
        assert False, "Should raise PDFExtractionError"
    except PDFExtractionError as e:
        print(f"[OK] Parser rejects corrupted PDF: {e}")


def test_api_upload_valid_pdf():
    sample_text = "LearnLens AI Day 2 Extraction Test Content."
    pdf_bytes = create_sample_pdf_with_text(sample_text)
    
    response = client.post(
        "/api/upload-pdf",
        files={"file": ("study_notes.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["filename"] == "study_notes.pdf"
    assert data["page_count"] == 1
    assert "LearnLens AI" in data["full_text"]
    assert "preview" in data
    print("[OK] API upload valid PDF endpoint succeeded")


def test_api_upload_non_pdf():
    response = client.post(
        "/api/upload-pdf",
        files={"file": ("notes.txt", b"Just some plain text", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
    print("[OK] API rejects non-PDF file upload")


def test_api_upload_corrupted_pdf():
    response = client.post(
        "/api/upload-pdf",
        files={"file": ("bad.pdf", b"corrupted header bytes", "application/pdf")}
    )
    assert response.status_code == 400
    print("[OK] API rejects corrupted PDF upload with 400 status")


if __name__ == "__main__":
    print("\n--- Running Day 2 Backend Tests ---")
    test_valid_pdf_parser()
    test_empty_bytes_parser()
    test_corrupted_bytes_parser()
    test_api_upload_valid_pdf()
    test_api_upload_non_pdf()
    test_api_upload_corrupted_pdf()
    print("\nAll backend tests passed successfully!")
