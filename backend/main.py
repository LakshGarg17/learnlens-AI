"""
FastAPI Entry Point for LearnLens AI (AI Study Assistant)
Day 1: Scaffolding, CORS configuration, Health Checks & AI Connectivity Test
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_client import test_connection

app = FastAPI(
    title="LearnLens AI - Study Assistant API",
    description="Backend API for AI Study Assistant powered by Anthropic",
    version="0.1.0",
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
