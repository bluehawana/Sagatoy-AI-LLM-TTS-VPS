"""Groq LLM service for ultra-fast inference."""

import logging
import os
from typing import Optional, Tuple

from groq import Groq

from sagatoyai.models import Intent

logger = logging.getLogger(__name__)


class GroqService:
    """Groq service for fast LLM inference."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq service.

        Args:
            api_key: Groq API key (or from env GROQ_API_KEY)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set, Groq will not work")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

        # Default model - fastest and most capable
        self.model = "llama-3.3-70b-versatile"

    def _detect_intent(self, user_input: str) -> Intent:
        """Detect user intent from input."""
        user_lower = user_input.lower()
        if any(
            word in user_lower
            for word in ["weather", "temperature", "rain", "sunny", "väder", "vädret"]
        ):
            return Intent.WEATHER
        elif any(
            word in user_lower
            for word in ["story", "tell me", "berättelse", "saga", "berätta"]
        ):
            return Intent.STORY
        elif any(
            word in user_lower for word in ["sing", "song", "music", "sjung", "sång"]
        ):
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
        temperature: float = 0.7,
        max_tokens: int = 200,
    ) -> str:
        """Generate response using Groq.

        Args:
            prompt: User prompt/question
            system_instruction: System instruction for behavior
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        if not self.client:
            raise GroqError("Groq client not initialized - check API key")

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            raise GroqError(f"Failed to generate response: {e}")

    async def generate_conversation_response(
        self,
        user_input: str,
        language: str = "en",
        context: Optional[list] = None,
    ) -> Tuple[str, Intent]:
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
            full_prompt = (
                f"Previous conversation:\n{conversation_history}\n\nChild: {user_input}"
            )
        else:
            full_prompt = user_input

        try:
            response = await self.generate_response(
                prompt=full_prompt,
                system_instruction=system_instruction,
                temperature=0.7,
                max_tokens=200,
            )
            return response, intent

        except Exception as e:
            logger.error(f"Conversation generation failed: {e}")
            raise GroqError(f"Failed to generate conversation: {e}")


class GroqError(Exception):
    """Groq service error."""

    pass


# Fallback message
GROQ_FALLBACK_MESSAGE = {
    "en": "Oops! My brain got a little fuzzy. Can you ask me again?",
    "sv": "Hoppsan! Mitt huvud blev lite grumligt. Kan du fråga igen?",
}

# Global Groq service instance
groq_service = GroqService()
