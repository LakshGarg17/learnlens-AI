"""
FastAPI Entry Point for LearnLens AI (AI Study Assistant)
Day 1: Scaffolding, CORS configuration, Health Checks & AI Connectivity Test
Day 2: PDF Upload & Text Extraction
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from ai_client import test_connection
from pdf_parser import extract_text_from_pdf, PDFExtractionError

app = FastAPI(
    title="LearnLens AI - Study Assistant API",
    description="Backend API for AI Study Assistant powered by Anthropic",
    version="0.2.0",
)

# Enable CORS middleware for frontend communication
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Basic health check endpoint to verify backend status."""
    return {"status": "ok"}


@app.get("/api/test-ai-connection")
def test_ai_route():
    """Test Anthropic API connectivity using ai_client helper."""
    result = test_connection()
    return result


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Accepts a multipart PDF file upload, validates file type,
    extracts text and returns document metadata and text preview.
    """
    # Validate file extension and MIME type
    filename = file.filename or "document.pdf"
    content_type = file.content_type or ""

    is_pdf_extension = filename.lower().endswith(".pdf")
    is_pdf_mime = content_type in ["application/pdf", "application/x-pdf", "application/octet-stream"]

    if not (is_pdf_extension or (is_pdf_mime and is_pdf_extension)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid PDF document (.pdf).",
        )

    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}",
        )

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes).",
        )

    try:
        extracted_data = extract_text_from_pdf(file_bytes, filename=filename)
    except PDFExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during PDF text extraction: {str(e)}",
        )

    # TODO: Day 3 - store full_text in session/state so Summarize/Ask Question/Quiz/Flashcards can use it
    return {
        "filename": extracted_data["filename"],
        "page_count": extracted_data["page_count"],
        "preview": extracted_data["preview"],
        "full_text": extracted_data["full_text"],
    }


# --- Action Route Placeholders (Day 1 Scaffolding) ---

@app.post("/api/summarize")
def summarize_placeholder():
    # TODO: Day 2 - wire up summarization logic here
    return {
        "status": "coming_soon",
        "message": "Document and topic summarization feature coming soon!",
    }


@app.post("/api/ask-question")
def ask_question_placeholder():
    # TODO: Day 2 - wire up Q&A and contextual chat logic here
    return {
        "status": "coming_soon",
        "message": "Interactive Q&A feature coming soon!",
    }


@app.post("/api/generate-quiz")
def generate_quiz_placeholder():
    # TODO: Day 3 - wire up quiz generation and scoring logic here
    return {
        "status": "coming_soon",
        "message": "AI-powered quiz generation feature coming soon!",
    }


@app.post("/api/flashcards")
def flashcards_placeholder():
    # TODO: Day 3 - wire up flashcard extraction and spaced-repetition logic here
    return {
        "status": "coming_soon",
        "message": "Interactive flashcard generator feature coming soon!",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

