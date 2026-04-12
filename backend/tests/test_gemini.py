"""Simple test script for Gemini API."""

import google.generativeai as gen
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
gen.configure(api_key=api_key)

# Load system prompt
system_prompt = open("storybook_prompt.txt").read()


def generate_story(query):
    """Generate a story using Gemini."""
    model = gen.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )

    response = model.generate_content(contents=query)
    return response.text


# Example: Generate T-Rex in Stockholm
story = generate_story(
    "Create a storybook for a 6-year-old about a T-Rex visiting the Vasa Museum and Gamla Stan in Stockholm."
)

print(story)
