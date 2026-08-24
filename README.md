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

## 🛠️ Day 1 Feature Status

- [x] **FastAPI Scaffolding & CORS**: Allows requests from `http://localhost:5173`.
- [x] **Secure AI Client (`ai_client.py`)**: Environment-based Anthropic client with `test_connection()`.
- [x] **Health & Connectivity Endpoints**:
  - `GET /api/health` → `{"status": "ok"}`
  - `GET /api/test-ai-connection` → Live Anthropic test
- [x] **Day 1 Placeholder Routes**:
  - `POST /api/summarize`
  - `POST /api/ask-question`
  - `POST /api/generate-quiz`
  - `POST /api/flashcards`
- [x] **React UI Shell**:
  - Upload Section: PDF document picker (`.pdf`) & manual topic input
  - Action Buttons: Summarize, Ask Question, Generate Quiz, Flashcards
  - Real-time Backend Health indicator & Live AI Key Test button
