"""
AI Client Helper Module for LearnLens AI (AI Study Assistant).
Handles API key loading, Anthropic client initialization, and connectivity verification.
"""

import os
import json
import re
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import anthropic


# Load environment variables from .env in backend
load_dotenv()


def get_api_key() -> Optional[str]:
    """Retrieve the Anthropic API key from the environment."""
    return os.getenv("ANTHROPIC_API_KEY")


def get_anthropic_client() -> anthropic.Anthropic:
    """
    Initialize and return an Anthropic client instance using the loaded API key.
    Raises ValueError if the API key is not configured.
    """
    api_key = get_api_key()
    if not api_key or api_key.strip() == "" or api_key == "your_anthropic_api_key_here":
        raise ValueError(
            "Anthropic API key not found or not configured. "
            "Please add your ANTHROPIC_API_KEY to the backend .env file."
        )
    return anthropic.Anthropic(api_key=api_key.strip())


def get_model() -> str:
    """Retrieve the configured Anthropic model name or default to Claude 3.5 Sonnet."""
    return os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")


# Maximum characters to prevent context overflow (~25,000 tokens)
MAX_DOCUMENT_CHARS = 100_000


def _prepare_document_text(text: str) -> str:
    """Safely clamp document text to prevent exceeding token context limits."""
    if not text:
        return ""
    if len(text) > MAX_DOCUMENT_CHARS:
        return text[:MAX_DOCUMENT_CHARS] + "\n\n[Note: Document content truncated to fit token context window.]"
    return text


def test_connection() -> Dict[str, Any]:
    """
    Send a minimal 'Hello' test message to confirm the Anthropic API key and connection work.
    
    Returns:
        Dict containing:
            - success (bool): True if connection succeeded, False otherwise
            - message (str): Response text or error description
            - model (str, optional): Model used for testing
    """
    try:
        client = get_anthropic_client()
        model_name = get_model()
        response = client.messages.create(
            model=model_name,
            max_tokens=20,
            messages=[
                {"role": "user", "content": "Hello! Reply with 'Connection successful'."}
            ],
        )
        reply = response.content[0].text if response.content else ""
        return {
            "success": True,
            "message": reply.strip(),
            "model": response.model,
        }
    except ValueError as ve:
        return {
            "success": False,
            "message": str(ve),
        }
    except anthropic.APIError as ae:
        return {
            "success": False,
            "message": f"Anthropic API Error ({ae.status_code}): {ae.message}",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error during connection test: {str(e)}",
        }


def summarize_text(text: str) -> Dict[str, Any]:
    """
    Generate an exam-focused, structured academic summary of the provided study material.
    
    Args:
        text: Raw text of the study material / extracted PDF.
        
    Returns:
        Dict containing:
            - success (bool): True if generation succeeded, False otherwise
            - summary (str, optional): Generated summary text in markdown
            - error (str, optional): Error description if generation failed
    """
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return {"success": False, "error": "No study material provided for summarization."}

    safe_text = _prepare_document_text(cleaned_text)

    system_prompt = (
        "You are an expert academic tutor helping a university student prepare for exams.\n"
        "Your task is to summarize ONLY the provided study material.\n\n"
        "Core Guidelines:\n"
        "1. Strictly summarize only the provided study material without inventing facts or adding external information.\n"
        "2. Preserve essential concepts, core definitions, and formulas/theories.\n"
        "3. Eliminate unnecessary repetition, preamble, and filler.\n"
        "4. Use clear, engaging, student-friendly language tailored for university exam preparation.\n"
        "5. Structure the output clearly using Markdown headings (##, ###), bullet points, and bold terms for high-yield exam takeaways.\n"
        "6. If the material is brief, provide a concise focused summary. If extensive, provide a comprehensive section-by-section breakdown."
    )

    user_prompt = (
        "Here is the study material:\n\n"
        f"<study_material>\n{safe_text}\n</study_material>\n\n"
        "Please generate a structured, high-yield study summary for exam preparation."
    )

    try:
        client = get_anthropic_client()
        model_name = get_model()
        response = client.messages.create(
            model=model_name,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        summary = response.content[0].text if response.content else ""
        return {"success": True, "summary": summary.strip()}
    except ValueError as ve:
        return {"success": False, "error": str(ve)}
    except anthropic.APIError as ae:
        return {"success": False, "error": f"AI service error ({ae.status_code}): {ae.message}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to generate summary: {str(e)}"}


def answer_question(text: str, question: str) -> Dict[str, Any]:
    """
    Answer a student's question based strictly and primarily on the provided study material.
    
    Args:
        text: Raw text of the study material.
        question: The student's specific question.
        
    Returns:
        Dict containing:
            - success (bool): True if answering succeeded, False otherwise
            - answer (str, optional): Generated answer text
            - error (str, optional): Error description if call failed
    """
    cleaned_text = (text or "").strip()
    cleaned_question = (question or "").strip()

    if not cleaned_text:
        return {"success": False, "error": "No study material provided to answer questions."}
    if not cleaned_question:
        return {"success": False, "error": "Question cannot be empty."}

    safe_text = _prepare_document_text(cleaned_text)

    system_prompt = (
        "You are an AI study assistant for university students.\n"
        "Answer the student's question based strictly and primarily on the provided study material.\n\n"
        "Critical Guidelines:\n"
        "- If the answer is not present or cannot reasonably be determined from the provided material, "
        "you MUST clearly state: \"I couldn't find this information in the uploaded study material.\"\n"
        "- Do not hallucinate or extrapolate facts that are not supported by the document.\n"
        "- Keep answers direct, accurate, structured, and exam-focused.\n"
        "- Use markdown formatting (bullet points, bold key terms) to make the answer easy to read."
    )

    user_prompt = (
        f"<study_material>\n{safe_text}\n</study_material>\n\n"
        f"Student Question: {cleaned_question}\n\n"
        "Please provide a clear and helpful answer based on the material above."
    )

    try:
        client = get_anthropic_client()
        model_name = get_model()
        response = client.messages.create(
            model=model_name,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        answer = response.content[0].text if response.content else ""
        return {"success": True, "answer": answer.strip()}
    except ValueError as ve:
        return {"success": False, "error": str(ve)}
    except anthropic.APIError as ae:
        return {"success": False, "error": f"AI service error ({ae.status_code}): {ae.message}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to answer question: {str(e)}"}


def explain_topic(text: str, topic: str) -> Dict[str, Any]:
    """
    Explain a complex concept or topic in beginner-friendly language,
    faithfully grounded in the study material.
    
    Args:
        text: Raw text of the study material.
        topic: The specific concept, term, or topic to explain simply.
        
    Returns:
        Dict containing:
            - success (bool): True if explanation succeeded, False otherwise
            - explanation (str, optional): Generated explanation
            - error (str, optional): Error description if call failed
    """
    cleaned_text = (text or "").strip()
    cleaned_topic = (topic or "").strip()

    if not cleaned_text:
        return {"success": False, "error": "No study material provided for explanation."}
    if not cleaned_topic:
        return {"success": False, "error": "Topic cannot be empty."}

    safe_text = _prepare_document_text(cleaned_text)

    system_prompt = (
        "You are an encouraging and gifted university tutor explaining a concept in simple, accessible terms.\n"
        "Explain the requested topic in beginner-friendly language while staying faithful to the uploaded study material.\n\n"
        "Format your explanation with:\n"
        "1. 💡 The Big Picture: A simple 1-2 sentence definition anyone can understand.\n"
        "2. 🚗 Intuitive Analogy or Real-World Example: An relatable comparison that makes the concept click.\n"
        "3. 🔑 Key Elements: Short bullet points covering essential terms or mechanisms mentioned in the notes.\n"
        "4. 🎯 Exam Takeaway: What a student must remember for a test.\n\n"
        "Guidelines:\n"
        "- Use simple language and short sections.\n"
        "- If the topic is completely absent from the material, clearly state that it is not covered in the notes."
    )

    user_prompt = (
        f"<study_material>\n{safe_text}\n</study_material>\n\n"
        f"Topic to explain simply: {cleaned_topic}\n\n"
        "Please provide a simple, beginner-friendly explanation following the specified structure."
    )

    try:
        client = get_anthropic_client()
        model_name = get_model()
        response = client.messages.create(
            model=model_name,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        explanation = response.content[0].text if response.content else ""
        return {"success": True, "explanation": explanation.strip()}
    except ValueError as ve:
        return {"success": False, "error": str(ve)}
    except anthropic.APIError as ae:
        return {"success": False, "error": f"AI service error ({ae.status_code}): {ae.message}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to generate explanation: {str(e)}"}


def _extract_json_from_text(raw_text: str) -> Any:
    """Safely extract and parse JSON from raw LLM output."""
    cleaned = (raw_text or "").strip()
    if not cleaned:
        raise ValueError("AI returned an empty response.")

    # If wrapped in markdown code blocks like ```json ... ``` or ``` ... ```
    if "```" in cleaned:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: find outermost [ ... ] or { ... }
        start_bracket = cleaned.find("[")
        end_bracket = cleaned.rfind("]")
        if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
            sub = cleaned[start_bracket : end_bracket + 1]
            return json.loads(sub)

        start_brace = cleaned.find("{")
        end_brace = cleaned.rfind("}")
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            sub = cleaned[start_brace : end_brace + 1]
            parsed = json.loads(sub)
            if isinstance(parsed, dict) and "questions" in parsed and isinstance(parsed["questions"], list):
                return parsed["questions"]
            return [parsed]

        raise ValueError("Could not parse valid JSON from AI response.")


def _validate_quiz_structure(questions_data: Any, requested_count: int) -> List[Dict[str, Any]]:
    """
    Validate the structure of parsed quiz questions.
    Returns a list of clean, validated question dictionaries.
    Raises ValueError if the structure does not meet required specifications.
    """
    if isinstance(questions_data, dict) and "questions" in questions_data:
        questions_data = questions_data["questions"]

    if not isinstance(questions_data, list):
        raise ValueError("AI output was not a list of questions.")

    validated = []
    seen_questions = set()

    for item in questions_data:
        if not isinstance(item, dict):
            continue

        q_text = str(item.get("question", "")).strip()
        options = item.get("options")
        correct_ans = item.get("correct_answer")
        explanation = str(item.get("explanation", "")).strip()

        if not q_text or q_text in seen_questions:
            continue

        if not isinstance(options, list) or len(options) != 4:
            continue

        cleaned_options = [str(opt).strip() for opt in options]
        if any(not opt for opt in cleaned_options):
            continue

        if isinstance(correct_ans, str) and correct_ans.isdigit():
            correct_ans = int(correct_ans)
        if not isinstance(correct_ans, int) or correct_ans not in [0, 1, 2, 3]:
            continue

        if not explanation:
            explanation = f"Option {chr(65 + correct_ans)} is the correct answer based on the study material."

        seen_questions.add(q_text)
        validated.append({
            "question": q_text,
            "options": cleaned_options,
            "correct_answer": correct_ans,
            "explanation": explanation,
        })

    if not validated:
        raise ValueError("AI response did not contain any valid multiple choice questions.")

    return validated


def generate_quiz(text: str, num_questions: int = 5, difficulty: str = "medium") -> Dict[str, Any]:
    """
    Generate an exam-ready multiple-choice quiz strictly based on the provided study material.

    Args:
        text: Raw text of the study material / extracted PDF.
        num_questions: Desired number of questions (5, 10, or 15).
        difficulty: Complexity level ('easy', 'medium', 'hard').

    Returns:
        Dict containing:
            - success (bool): True if generated and validated successfully
            - questions (list, optional): List of validated MCQ objects
            - error (str, optional): Error description if generation failed
    """
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return {"success": False, "error": "No study material provided for quiz generation."}

    diff = (difficulty or "medium").lower().strip()
    if diff not in ["easy", "medium", "hard"]:
        diff = "medium"

    count = int(num_questions) if isinstance(num_questions, (int, str)) and str(num_questions).isdigit() else 5
    if count not in [5, 10, 15]:
        count = 5

    safe_text = _prepare_document_text(cleaned_text)

    system_prompt = (
        "You are an expert university professor and examination board specialist.\n"
        "Your task is to generate a high-quality Multiple Choice Quiz (MCQ) based STRICTLY and ONLY on the provided study material.\n\n"
        "Core Guidelines:\n"
        f"1. Generate exactly {count} multiple choice questions.\n"
        f"2. Difficulty level: {diff.upper()}.\n"
        "   - EASY: Direct recall of key definitions, core terms, and fundamental concepts stated in the notes.\n"
        "   - MEDIUM: Conceptual comprehension, distinguishing between related ideas, and standard application.\n"
        "   - HARD: In-depth analytical questions, edge cases, multi-step reasoning, and evaluating mechanisms described in the text.\n"
        "3. Each question must have EXACTLY 4 distinct options (avoid 'All of the above' or 'None of the above').\n"
        "4. Exactly ONE option must be correct. 'correct_answer' must be the 0-indexed integer position (0, 1, 2, or 3) of the correct option.\n"
        "5. Provide a clear, educational explanation detailing why the correct answer is right according to the study material.\n"
        "6. Do NOT invent facts or test external knowledge not present in the study material.\n"
        "7. Avoid duplicate questions.\n"
        "8. Output MUST be ONLY a valid JSON array of question objects, with NO surrounding conversational commentary or preamble.\n\n"
        "Expected JSON Schema:\n"
        "[\n"
        "  {\n"
        '    "question": "What is ...?",\n'
        '    "options": ["Option A", "Option B", "Option C", "Option D"],\n'
        '    "correct_answer": 1,\n'
        '    "explanation": "..."\n'
        "  }\n"
        "]"
    )

    user_prompt = (
        f"<study_material>\n{safe_text}\n</study_material>\n\n"
        f"Generate {count} {diff}-difficulty multiple-choice questions from the study material above. "
        "Return ONLY the JSON array."
    )

    max_tokens = min(4096, max(1200, count * 350))

    try:
        client = get_anthropic_client()
        model_name = get_model()
        response = client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        reply_text = response.content[0].text if response.content else ""
        parsed_json = _extract_json_from_text(reply_text)
        validated_questions = _validate_quiz_structure(parsed_json, count)

        return {
            "success": True,
            "questions": validated_questions[:count],
        }
    except ValueError as ve:
        return {"success": False, "error": str(ve)}
    except anthropic.APIError as ae:
        return {"success": False, "error": f"AI service error ({ae.status_code}): {ae.message}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to generate quiz: {str(e)}"}


if __name__ == "__main__":
    print("Testing Anthropic connection...")
    result = test_connection()
    if result["success"]:
        print(f"[SUCCESS] Response from {result.get('model')}: {result['message']}")
    else:
        print(f"[INFO] Connection status: {result['message']}")


