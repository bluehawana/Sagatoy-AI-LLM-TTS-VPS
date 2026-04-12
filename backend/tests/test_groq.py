"""Test Groq API for fast LLM inference."""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=groq_api_key)


def test_groq_chat(prompt: str, language: str = "sv"):
    """Test Groq chat completion."""

    # System prompt for child-friendly responses
    if language == "sv":
        system_prompt = """Du är en vänlig AI-assistent i en gosig leksak som pratar med barn 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig komplicerade ord eller läskiga ämnen.
Svara alltid på svenska."""
    else:
        system_prompt = """You are a friendly AI assistant inside a plush toy, talking to children aged 3-10.
Use simple, warm, and encouraging language. Keep responses short (2-3 sentences).
Be playful and imaginative. Never use complex words or scary topics.
Always respond in English."""

    print(f"\n{'='*60}")
    print(f"🎤 Question: {prompt}")
    print(f"{'='*60}")

    start_time = time.time()

    # Call Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",  # Fast and capable model
        temperature=0.7,
        max_tokens=200,
    )

    end_time = time.time()
    response_time = end_time - start_time

    response = chat_completion.choices[0].message.content

    print(f"\n🤖 Response: {response}")
    print(f"\n⚡ Response time: {response_time:.2f} seconds")
    print(f"📊 Tokens used: {chat_completion.usage.total_tokens}")

    return response, response_time


def compare_models():
    """Test different Groq models."""

    models = [
        "llama-3.3-70b-versatile",  # Latest, most capable
        "llama-3.1-8b-instant",     # Fastest
        "mixtral-8x7b-32768",       # Good balance
    ]

    test_prompt = "Varför är himlen blå?"

    print("\n" + "="*60)
    print("🚀 Groq Model Comparison")
    print("="*60)

    for model in models:
        print(f"\n📦 Testing model: {model}")
        print("-"*60)

        start_time = time.time()

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Du är en vänlig leksak som pratar med barn. Svara kort på svenska."
                    },
                    {
                        "role": "user",
                        "content": test_prompt
                    }
                ],
                model=model,
                temperature=0.7,
                max_tokens=150,
            )

            end_time = time.time()
            response_time = end_time - start_time

            response = chat_completion.choices[0].message.content

            print(f"✅ Response: {response[:100]}...")
            print(f"⚡ Time: {response_time:.2f}s")
            print(f"📊 Tokens: {chat_completion.usage.total_tokens}")

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Test Groq API with various questions."""

    print("\n" + "="*60)
    print("🚀 Groq API Test - Ultra-Fast LLM")
    print("="*60)

    # Test questions in Swedish and English
    test_questions = [
        ("Hej toy, vad är vädret idag?", "sv"),
        ("Hey toy, why do birds fly?", "en"),
        ("Hej toy, kan du berätta en saga om en drake?", "sv"),
        ("Hey toy, what is 2 + 2?", "en"),
    ]

    total_time = 0

    for question, lang in test_questions:
        response, response_time = test_groq_chat(question, lang)
        total_time += response_time
        time.sleep(0.5)  # Small delay between requests

    print("\n" + "="*60)
    print(f"✅ All tests complete!")
    print(f"⚡ Average response time: {total_time / len(test_questions):.2f}s")
    print("="*60)

    # Compare different models
    print("\n")
    compare_models()


if __name__ == "__main__":
    main()
