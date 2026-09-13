# LearnLens AI - AI Study Assistant

A fullstack AI-powered study assistant built with **React (Vite)**, **FastAPI (Python)**, and the **Anthropic API (Claude)**.

---

## 📁 Project Structure

```
LearnLens-AI/
├── backend/                  # FastAPI Python Backend
│   ├── .env                  # API Keys (git-ignored)
│   ├── .env.example          # Environment template
│   ├── .gitignore            # Backend ignore rules
│   ├── requirements.txt      # Python dependencies
│   ├── ai_client.py          # Anthropic API client & connection tester
│   └── main.py               # FastAPI entry point & API endpoints
├── frontend/                 # React + Vite Frontend
│   ├── package.json          # Frontend dependencies (Axios, Lucide Icons)
│   ├── index.html            # Entry HTML
│   ├── vite.config.js        # Vite build config
│   └── src/
│       ├── App.jsx           # Main UI container
│       ├── App.css           # UI styles (Glassmorphic dark theme)
│       ├── index.css         # Design system & tokens
│       └── components/
│           ├── Header.jsx        # App header & branding
│           ├── StatusBanner.jsx  # Health check & AI test status banner
│           ├── UploadSection.jsx # PDF uploader & topic input
│           └── ActionButtons.jsx # 4 Action cards with placeholders
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup (FastAPI)

```bash
cd backend
# Create virtual environment if needed
python -m venv ../venv
# Activate virtual environment (Windows)
..\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
# Copy .env.example to .env and insert your Anthropic key:
# ANTHROPIC_API_KEY=sk-ant-...

# Run the backend server
uvicorn main:app --port 8000 --reload
```

Backend will run at: `http://localhost:8000` (API Docs at `http://localhost:8000/docs`)

### 2. Frontend Setup (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

- [x] **Day 1**: FastAPI scaffolding, CORS, environment configuration, secure AI client, health endpoints.
- [x] **Day 2**: PDF ingestion, multipart upload, byte-level parsing, and text extraction preview.
- [x] **Day 3**:
  - `POST /summarize` & `POST /api/summarize` — AI exam summarization.
  - `POST /ask` & `POST /api/ask` — Contextual Q&A strictly grounded in uploaded notes.
  - `POST /explain` & `POST /api/explain` — Simple concept breakdown with real-world analogies.
- [x] **Day 4**:
  - `POST /generate-quiz` & `POST /api/generate-quiz` — AI-powered MCQ Quiz generation.
  - **Question Counts**: 5, 10, or 15 questions.
  - **Difficulties**: Easy (recall), Medium (conceptual), Hard (analytical).
  - **Interactive Workflow**: Question-by-question view with progress tracking, 4 options (A-D), submission, automated scoring, answer explanations, and retake/retry flow.
- [ ] **Day 5**: Flashcards & spaced repetition (Coming soon).

