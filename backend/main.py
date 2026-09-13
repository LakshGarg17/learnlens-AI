"""
FastAPI Entry Point for LearnLens AI (AI Study Assistant)
Day 1: Scaffolding, CORS configuration, Health Checks & AI Connectivity Test
Day 2: PDF Upload & Text Extraction
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from ai_client import test_connection, summarize_text, answer_question, explain_topic
from pdf_parser import extract_text_from_pdf, PDFExtractionError

app = FastAPI(
    title="LearnLens AI - Study Assistant API",
    description="Backend API for AI Study Assistant powered by Anthropic",
    version="0.3.0",
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


# --- Request Models ---

class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Study material text to summarize")


class AskRequest(BaseModel):
    text: str = Field(..., description="Study material context text")
    question: str = Field(..., description="Student question to answer")


class ExplainRequest(BaseModel):
    text: str = Field(..., description="Study material context text")
    topic: str = Field(..., description="Topic or concept to explain simply")


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

    return {
        "filename": extracted_data["filename"],
        "page_count": extracted_data["page_count"],
        "preview": extracted_data["preview"],
        "full_text": extracted_data["full_text"],
    }


# --- Day 3 AI Endpoints ---

def handle_summarize(payload: SummarizeRequest):
    study_text = (payload.text or "").strip()
    if not study_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide study material text to summarize.",
        )

    result = summarize_text(study_text)
    if not result.get("success"):
        error_msg = result.get("error", "Unable to generate the summary. Please try again.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )

    return {
        "success": True,
        "summary": result["summary"],
    }


@app.post("/summarize")
def summarize_endpoint(payload: SummarizeRequest):
    return handle_summarize(payload)


@app.post("/api/summarize")
def api_summarize_endpoint(payload: SummarizeRequest):
    return handle_summarize(payload)


def handle_ask(payload: AskRequest):
    study_text = (payload.text or "").strip()
    question = (payload.question or "").strip()

    if not study_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide study material text before asking a question.",
        )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a question to ask.",
        )

    result = answer_question(study_text, question)
    if not result.get("success"):
        error_msg = result.get("error", "Unable to answer your question. Please try again.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )

    return {
        "success": True,
        "answer": result["answer"],
    }


@app.post("/ask")
def ask_endpoint(payload: AskRequest):
    return handle_ask(payload)


@app.post("/api/ask")
def api_ask_endpoint(payload: AskRequest):
    return handle_ask(payload)


@app.post("/api/ask-question")
def api_ask_question_endpoint(payload: AskRequest):
    return handle_ask(payload)


def handle_explain(payload: ExplainRequest):
    study_text = (payload.text or "").strip()
    topic = (payload.topic or "").strip()

    if not study_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide study material text to explain topics from.",
        )
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a topic or concept to explain.",
        )

    result = explain_topic(study_text, topic)
    if not result.get("success"):
        error_msg = result.get("error", "Unable to generate the explanation. Please try again.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )

    return {
        "success": True,
        "explanation": result["explanation"],
    }


@app.post("/explain")
def explain_endpoint(payload: ExplainRequest):
    return handle_explain(payload)


@app.post("/api/explain")
def api_explain_endpoint(payload: ExplainRequest):
    return handle_explain(payload)


# --- Coming Soon Placeholders (Day 4/5) ---

@app.post("/api/generate-quiz")
def generate_quiz_placeholder():
    return {
        "status": "coming_soon",
        "message": "AI-powered quiz generation feature coming in Day 4!",
    }


@app.post("/api/flashcards")
def flashcards_placeholder():
    return {
        "status": "coming_soon",
        "message": "Interactive flashcard generator feature coming in Day 5!",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


