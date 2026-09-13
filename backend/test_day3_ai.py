"""
Test Suite for Day 3 AI Features:
- Summarize endpoint
- Ask AI endpoint
- Explain Topic endpoint
- Input validation (empty question, empty topic, empty text)
- Error handling
- PDF Upload regression
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

SAMPLE_MATERIAL = (
    "Machine Learning is a branch of artificial intelligence that focuses on building "
    "applications that learn from data and improve their accuracy over time without being "
    "specifically programmed to do so. Supervised learning algorithms are trained using "
    "labeled examples, while unsupervised learning works on unlabeled datasets."
)


def test_summarize_empty_text():
    response = client.post("/api/summarize", json={"text": "   "})
    assert response.status_code == 400
    assert "Please provide study material text" in response.json()["detail"]
    print("[OK] /api/summarize correctly rejects empty text with 400")


def test_summarize_success_mock():
    mock_summary = "## Machine Learning Overview\n- Subset of AI that learns from data\n- Includes supervised & unsupervised learning"
    with patch("main.summarize_text", return_value={"success": True, "summary": mock_summary}):
        response = client.post("/api/summarize", json={"text": SAMPLE_MATERIAL})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Machine Learning" in data["summary"]

        # Also test /summarize alias
        alias_resp = client.post("/summarize", json={"text": SAMPLE_MATERIAL})
        assert alias_resp.status_code == 200
        assert alias_resp.json()["success"] is True
    print("[OK] /summarize and /api/summarize succeed with valid input")


def test_summarize_ai_error():
    with patch("main.summarize_text", return_value={"success": False, "error": "AI provider service unavailable"}):
        response = client.post("/api/summarize", json={"text": SAMPLE_MATERIAL})
        assert response.status_code == 500
        assert "AI provider service unavailable" in response.json()["detail"]
    print("[OK] /api/summarize handles AI error gracefully with 500 status")


def test_ask_empty_question():
    response = client.post("/api/ask", json={"text": SAMPLE_MATERIAL, "question": "   "})
    assert response.status_code == 400
    assert "Please enter a question" in response.json()["detail"]
    print("[OK] /api/ask rejects empty question with 400")


def test_ask_empty_text():
    response = client.post("/api/ask", json={"text": "", "question": "What is ML?"})
    assert response.status_code == 400
    assert "Please provide study material" in response.json()["detail"]
    print("[OK] /api/ask rejects empty text with 400")


def test_ask_success_mock():
    mock_answer = "Supervised learning algorithms are trained using labeled examples."
    with patch("main.answer_question", return_value={"success": True, "answer": mock_answer}):
        response = client.post("/api/ask", json={"text": SAMPLE_MATERIAL, "question": "What is supervised learning?"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "labeled examples" in data["answer"]

        # Test /ask alias
        alias_resp = client.post("/ask", json={"text": SAMPLE_MATERIAL, "question": "What is supervised learning?"})
        assert alias_resp.status_code == 200
        assert alias_resp.json()["success"] is True
    print("[OK] /ask and /api/ask succeed with valid question")


def test_ask_unfound_information():
    mock_answer = "I couldn't find this information in the uploaded study material."
    with patch("main.answer_question", return_value={"success": True, "answer": mock_answer}):
        response = client.post("/api/ask", json={"text": SAMPLE_MATERIAL, "question": "What is quantum gravity?"})
        assert response.status_code == 200
        assert "couldn't find this information" in response.json()["answer"]
    print("[OK] /api/ask handles unfound information cleanly")


def test_explain_empty_topic():
    response = client.post("/api/explain", json={"text": SAMPLE_MATERIAL, "topic": "  "})
    assert response.status_code == 400
    assert "Please enter a topic" in response.json()["detail"]
    print("[OK] /api/explain rejects empty topic with 400")


def test_explain_success_mock():
    mock_explanation = "💡 The Big Picture: Supervised learning is learning with a teacher or answer key."
    with patch("main.explain_topic", return_value={"success": True, "explanation": mock_explanation}):
        response = client.post("/api/explain", json={"text": SAMPLE_MATERIAL, "topic": "supervised learning"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "The Big Picture" in data["explanation"]

        # Test /explain alias
        alias_resp = client.post("/explain", json={"text": SAMPLE_MATERIAL, "topic": "supervised learning"})
        assert alias_resp.status_code == 200
        assert alias_resp.json()["success"] is True
    print("[OK] /explain and /api/explain succeed with valid topic")


def test_pdf_upload_regression():
    with open("sample_study_guide.pdf", "rb") as f:
        pdf_bytes = f.read()

    response = client.post(
        "/api/upload-pdf",
        files={"file": ("sample_study_guide.pdf", pdf_bytes, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "sample_study_guide.pdf"
    assert data["page_count"] > 0
    assert len(data["full_text"]) > 0
    print(f"[OK] Day 2 PDF upload regression test passed ({data['page_count']} pages, {len(data['full_text'])} chars)")


if __name__ == "__main__":
    print("\n--- Running Day 3 Backend Tests ---")
    test_summarize_empty_text()
    test_summarize_success_mock()
    test_summarize_ai_error()
    test_ask_empty_question()
    test_ask_empty_text()
    test_ask_success_mock()
    test_ask_unfound_information()
    test_explain_empty_topic()
    test_explain_success_mock()
    test_pdf_upload_regression()
    print("\nAll Day 3 backend tests passed successfully!")
