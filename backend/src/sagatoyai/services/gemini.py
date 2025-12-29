"""Google Gemini integration for story generation and conversations."""

import logging
import os
from pathlib import Path
from typing import Optional

import google.generativeai as genai

from sagatoyai.models import Intent

logger = logging.getLogger(__name__)


class GeminiService:
    """Google Gemini service for text and content generation."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini service.

        Args:
            api_key: Google AI Studio API key (or from env GOOGLE_API_KEY)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not set, Gemini will not work")
        else:
            genai.configure(api_key=self.api_key)

        # Use Gemini 2.5 Flash for text generation
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        # Load storybook system prompt
        prompt_path = Path(
            __file__).parent.parent.parent.parent / "storybook_prompt.txt"
        if prompt_path.exists():
            self.storybook_prompt = prompt_path.read_text(encoding="utf-8")
        else:
            # Fallback to inline prompt
            self.storybook_prompt = """You are a whimsical storybook narrator for children aged 3-10.
Use magical, warm, and child-friendly language.
Create engaging stories with:
- Simple vocabulary
- Exciting adventures
- Positive lessons
- Happy endings
- 3-5 minutes reading time (500-750 words)

Make every story fun, educational, and age-appropriate."""

    def _detect_intent(self, user_input: str) -> Intent:
        """Detect user intent from input."""
        user_lower = user_input.lower()
        if any(word in user_lower for word in ["weather", "temperature", "rain", "sunny", "väder"]):
            return Intent.WEATHER
        elif any(word in user_lower for word in ["story", "tell me", "berättelse", "saga"]):
            return Intent.STORY
        elif any(word in user_lower for word in ["sing", "song", "music", "sjung", "sång"]):
            return Intent.SONG
        elif any(
            word in user_lower
            for word in ["math", "plus", "minus", "times", "divide", "räkna", "matte"]
        ):
            return Intent.MATH
        return Intent.GENERAL

    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        language: str = "en",
    ) -> str:
        """Generate response using Gemini.

        Args:
            prompt: User prompt/question
            system_instruction: System instruction for behavior
            language: Language code ('en' or 'sv')

        Returns:
            Generated text response
        """
        try:
            # Create model with system instruction
            model = genai.GenerativeModel(
                "gemini-2.5-flash",
                system_instruction=system_instruction,
            )

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise GeminiError(f"Failed to generate response: {e}")

    async def generate_story(
        self,
        story_prompt: str,
        language: str = "en",
    ) -> str:
        """Generate a children's story using Gemini.

        Args:
            story_prompt: Story generation prompt with details
            language: Language code ('en' or 'sv')

        Returns:
            Generated story text
        """
        try:
            story = await self.generate_response(
                prompt=story_prompt,
                system_instruction=self.storybook_prompt,
                language=language,
            )
            return story

        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            raise GeminiError(f"Failed to generate story: {e}")

    async def generate_conversation_response(
        self,
        user_input: str,
        language: str = "en",
        context: Optional[list] = None,
    ) -> tuple[str, Intent]:
        """Generate conversational response for toy interaction.

        Args:
            user_input: What the child said
            language: Language code ('en' or 'sv')
            context: Previous conversation messages

        Returns:
            Tuple of (response_text, detected_intent)
        """
        intent = self._detect_intent(user_input)

        if language == "sv":
            system_instruction = """Du är en vänlig AI-assistent i en gosig leksak som pratar med barn 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig komplicerade ord eller läskiga ämnen.
Svara alltid på svenska."""
        else:
            system_instruction = """You are a friendly AI assistant inside a plush toy, talking to children aged 3-10.
Use simple, warm, and encouraging language. Keep responses short (2-3 sentences).
Be playful and imaginative. Never use complex words or scary topics.
Always respond in English."""

        # Build prompt with context
        if context:
            conversation_history = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in context[-3:]]
            )
            full_prompt = f"Previous conversation:\n{conversation_history}\n\nChild: {user_input}"
        else:
            full_prompt = user_input

        try:
            response = await self.generate_response(
                prompt=full_prompt,
                system_instruction=system_instruction,
                language=language,
            )
            return response, intent

        except Exception as e:
            logger.error(f"Conversation generation failed: {e}")
            raise GeminiError(f"Failed to generate conversation: {e}")


class GeminiError(Exception):
    """Gemini service error."""

    pass


# Fallback message
GEMINI_FALLBACK_MESSAGE = {
    "en": "Oops! My brain got a little fuzzy. Can you ask me again?",
    "sv": "Hoppsan! Mitt huvud blev lite grumligt. Kan du fråga igen?",
}

# Global Gemini service instance
gemini_service = GeminiService()
