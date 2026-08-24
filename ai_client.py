"""
AI Client Helper Module for AI Study Assistant.
Handles API key loading, Anthropic client initialization, and connectivity verification.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import anthropic

# Load environment variables from .env file
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
            "Please add your ANTHROPIC_API_KEY to the .env file."
        )
    return anthropic.Anthropic(api_key=api_key.strip())


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
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
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


if __name__ == "__main__":
    print("Testing Anthropic connection...")
    result = test_connection()
    if result["success"]:
        print(f"[SUCCESS] Response from {result.get('model')}: {result['message']}")
    else:
        print(f"[INFO] Connection status: {result['message']}")

