"""
Comprehensive Test Suite for Day 4 AI Quiz System:
- Quiz generation endpoints (/generate-quiz, /api/generate-quiz)
- Question count validation (5, 10, 15)
- Difficulty levels ('easy', 'medium', 'hard')
- Input validation (empty text, invalid question count, invalid difficulty)
- Safe error handling (AI failure, malformed JSON)
- Schema and scoring verification
- Regression tests for Day 1, Day 2, and Day 3 functionality
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from ai_client import _extract_json_from_text, _validate_quiz_structure

client = TestClient(app)

SAMPLE_MATERIAL = (
    "Operating systems manage computer hardware and software resources. "
    "A process is an instance of a computer program that is being executed. "
    "Virtual memory is a memory management technique that provides an idealized "
    "abstraction of the storage resources that are actually available on a given machine. "
    "Deadlock is a state in which each member of a group is waiting for another member, "
    "including itself, to take action."
)


def mock_quiz_questions(count=5):
    return [
        {
            "question": f"Sample Question {i+1}: What is the main role of process {i+1}?",
            "options": [
                f"Option A{i+1}",
                f"Option B{i+1}",
                f"Option C{i+1}",
                f"Option D{i+1}",
            ],
            "correct_answer": i % 4,
            "explanation": f"Explanation for question {i+1} confirming correct answer is Option {chr(65 + (i % 4))}.",
        }
        for i in range(count)
    ]


# 1. Test Generate 5 Easy Questions
def test_generate_5_easy_questions():
    mock_qs = mock_quiz_questions(5)
    with patch("main.generate_quiz", return_value={"success": True, "questions": mock_qs}):
        response = client.post(
            "/api/generate-quiz",
            json={"text": SAMPLE_MATERIAL, "num_questions": 5, "difficulty": "easy"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["questions"]) == 5
        for q in data["questions"]:
            assert "question" in q and len(q["question"]) > 0
            assert "options" in q and len(q["options"]) == 4
            assert "correct_answer" in q and q["correct_answer"] in [0, 1, 2, 3]
            assert "explanation" in q and len(q["explanation"]) > 0
    print("[OK] Generate 5 easy questions succeeds with valid structure")


# 2. Test Generate 5 Medium Questions
def test_generate_5_medium_questions():
    mock_qs = mock_quiz_questions(5)
    with patch("main.generate_quiz", return_value={"success": True, "questions": mock_qs}):
        response = client.post(
            "/api/generate-quiz",
            json={"text": SAMPLE_MATERIAL, "num_questions": 5, "difficulty": "medium"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["questions"]) == 5
    print("[OK] Generate 5 medium questions succeeds")


# 3. Test Generate 5 Hard Questions
def test_generate_5_hard_questions():
    mock_qs = mock_quiz_questions(5)
    with patch("main.generate_quiz", return_value={"success": True, "questions": mock_qs}):
        response = client.post(
            "/generate-quiz",  # Test alias without /api prefix
            json={"text": SAMPLE_MATERIAL, "num_questions": 5, "difficulty": "hard"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["questions"]) == 5
    print("[OK] Generate 5 hard questions succeeds (and alias /generate-quiz works)")


# 4. Test Generate 10 Questions
def test_generate_10_questions():
    mock_qs = mock_quiz_questions(10)
    with patch("main.generate_quiz", return_value={"success": True, "questions": mock_qs}):
        response = client.post(
            "/api/generate-quiz",
            json={"text": SAMPLE_MATERIAL, "num_questions": 10, "difficulty": "medium"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["questions"]) == 10
    print("[OK] Generate 10 questions succeeds")


# 5. Test Empty Study Material
def test_empty_study_material():
    response = client.post(
        "/api/generate-quiz",
        json={"text": "   ", "num_questions": 5, "difficulty": "medium"},
    )
    assert response.status_code == 400
    assert "Please provide study material text" in response.json()["detail"]
    print("[OK] Empty study material rejected with HTTP 400")


# 6. Test Invalid Difficulty
def test_invalid_difficulty():
    response = client.post(
        "/api/generate-quiz",
        json={"text": SAMPLE_MATERIAL, "num_questions": 5, "difficulty": "insane"},
    )
    assert response.status_code == 400
    assert "Invalid difficulty" in response.json()["detail"]
    print("[OK] Invalid difficulty rejected with HTTP 400")


# 7. Test Invalid Question Count
def test_invalid_question_count():
    response = client.post(
        "/api/generate-quiz",
        json={"text": SAMPLE_MATERIAL, "num_questions": 7, "difficulty": "medium"},
    )
    assert response.status_code == 400
    assert "Invalid number of questions" in response.json()["detail"]
    print("[OK] Invalid question count (7) rejected with HTTP 400")


# 8. Test AI Failure Error Handling
def test_ai_failure():
    with patch("main.generate_quiz", return_value={"success": False, "error": "Anthropic API rate limit exceeded"}):
        response = client.post(
            "/api/generate-quiz",
            json={"text": SAMPLE_MATERIAL, "num_questions": 5, "difficulty": "medium"},
        )
        assert response.status_code == 500
        assert "Anthropic API rate limit exceeded" in response.json()["detail"]
    print("[OK] AI failure returned gracefully as HTTP 500 without crash")


# 9. Test Malformed AI Output Handling
def test_malformed_ai_output_parsing():
    # Markdown wrapped json
    markdown_wrapped = '```json\n[{"question": "Q1?", "options": ["A", "B", "C", "D"], "correct_answer": 0, "explanation": "E1"}]\n```'
    parsed = _extract_json_from_text(markdown_wrapped)
    validated = _validate_quiz_structure(parsed, 1)
    assert len(validated) == 1
    assert validated[0]["question"] == "Q1?"

    # Malformed text
    try:
        _extract_json_from_text("Sorry I cannot create questions for this.")
        assert False, "Should raise ValueError for non-JSON"
    except ValueError:
        pass

    # Invalid options count (only 3 options)
    invalid_structure = [
        {"question": "Bad Q", "options": ["A", "B", "C"], "correct_answer": 1, "explanation": "exp"}
    ]
    try:
        _validate_quiz_structure(invalid_structure, 1)
        assert False, "Should raise ValueError for options count != 4"
    except ValueError:
        pass
    print("[OK] Malformed AI responses and schema deviations handled securely")


# 10. Test Scoring Verification Logic
def test_scoring_logic():
    questions = mock_quiz_questions(5)
    # Questions correct_answers are: 0, 1, 2, 3, 0

    # Case A: All correct
    student_answers_all_correct = {0: 0, 1: 1, 2: 2, 3: 3, 4: 0}
    correct_count = sum(
        1 for idx, q in enumerate(questions) if student_answers_all_correct.get(idx) == q["correct_answer"]
    )
    score_pct = round((correct_count / len(questions)) * 100)
    assert correct_count == 5
    assert score_pct == 100

    # Case B: All incorrect
    student_answers_all_wrong = {0: 1, 1: 2, 2: 3, 3: 0, 4: 1}
    correct_count = sum(
        1 for idx, q in enumerate(questions) if student_answers_all_wrong.get(idx) == q["correct_answer"]
    )
    score_pct = round((correct_count / len(questions)) * 100)
    assert correct_count == 0
    assert score_pct == 0

    # Case C: 4 out of 5 correct (80%)
    student_answers_4_of_5 = {0: 0, 1: 1, 2: 2, 3: 3, 4: 1}
    correct_count = sum(
        1 for idx, q in enumerate(questions) if student_answers_4_of_5.get(idx) == q["correct_answer"]
    )
    score_pct = round((correct_count / len(questions)) * 100)
    assert correct_count == 4
    assert score_pct == 80
    print("[OK] Quiz scoring math verified (100%, 0%, 80%)")


# 11. Day 1, 2, 3 Regressions
def test_day1_day2_day3_regressions():
    # Day 1 health
    health_resp = client.get("/api/health")
    assert health_resp.status_code == 200

    # Day 2 PDF upload
    with open("sample_study_guide.pdf", "rb") as f:
        pdf_bytes = f.read()
    pdf_resp = client.post(
        "/api/upload-pdf",
        files={"file": ("sample_study_guide.pdf", pdf_bytes, "application/pdf")},
    )
    assert pdf_resp.status_code == 200
    pdf_data = pdf_resp.json()
    assert "full_text" in pdf_data

    # Day 3 endpoints
    with patch("main.summarize_text", return_value={"success": True, "summary": "Summary OK"}):
        sum_resp = client.post("/api/summarize", json={"text": pdf_data["full_text"]})
        assert sum_resp.status_code == 200
        assert sum_resp.json()["success"] is True

    with patch("main.answer_question", return_value={"success": True, "answer": "Answer OK"}):
        ask_resp = client.post("/api/ask", json={"text": pdf_data["full_text"], "question": "What is OS?"})
        assert ask_resp.status_code == 200
        assert ask_resp.json()["success"] is True

    with patch("main.explain_topic", return_value={"success": True, "explanation": "Explain OK"}):
        exp_resp = client.post("/api/explain", json={"text": pdf_data["full_text"], "topic": "Processes"})
        assert exp_resp.status_code == 200
        assert exp_resp.json()["success"] is True

    print("[OK] Day 1, 2, and 3 regression tests all passed")


if __name__ == "__main__":
    print("\n--- Running Day 4 AI Quiz Backend Tests ---")
    test_generate_5_easy_questions()
    test_generate_5_medium_questions()
    test_generate_5_hard_questions()
    test_generate_10_questions()
    test_empty_study_material()
    test_invalid_difficulty()
    test_invalid_question_count()
    test_ai_failure()
    test_malformed_ai_output_parsing()
    test_scoring_logic()
    test_day1_day2_day3_regressions()
    print("\nAll Day 4 backend tests passed successfully!")
