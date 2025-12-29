"""LLM service using Ollama."""

import logging
from dataclasses import dataclass
from typing import Optional

import httpx

from sagatoyai.models import Intent

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM service."""

    text: str
    intent: Intent
    requires_followup: bool


class LLMService:
    """LLM service using Ollama."""

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """Initialize LLM service."""
        self.ollama_url = ollama_url
        self.model = "llama3.1"
        self.system_prompt = """You are a friendly AI assistant inside a plush toy, talking to children aged 3-10.
Use simple, warm, and encouraging language. Keep responses short (2-3 sentences).
Be playful and imaginative. Never use complex words or scary topics."""

    def _detect_intent(self, user_input: str) -> Intent:
        """Detect user intent from input."""
        user_lower = user_input.lower()
        if any(word in user_lower for word in ["weather", "temperature", "rain", "sunny"]):
            return Intent.WEATHER
        elif any(word in user_lower for word in ["story", "tell me about", "once upon"]):
            return Intent.STORY
        elif any(word in user_lower for word in ["sing", "song", "music"]):
            return Intent.SONG
        elif any(
            word in user_lower for word in ["math", "plus", "minus", "times", "divide", "calculate"]
        ):
            return Intent.MATH
        return Intent.GENERAL

    async def generate_response(
        self,
        prompt: str,
        session_id: str,
        context: Optional[list] = None,
    ) -> LLMResponse:
        """Generate response to user input."""
        try:
            intent = self._detect_intent(prompt)

            messages = [{"role": "system", "content": self.system_prompt}]

            if context:
                messages.extend(context)

            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json={"model": self.model,
                          "messages": messages, "stream": False},
                )
                response.raise_for_status()
                result = response.json()

                response_text = result["message"]["content"]

                return LLMResponse(
                    text=response_text,
                    intent=intent,
                    requires_followup=False,
                )

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise LLMError(f"Failed to generate response: {e}")

    async def generate_story(
        self,
        theme: Optional[str] = None,
        duration_minutes: int = 3,
    ) -> str:
        """Generate an age-appropriate story."""
        target_words = duration_minutes * 150

        story_prompt = f"Tell a short, fun story for young children"
        if theme:
            story_prompt += f" about {theme}"
        story_prompt += f". Make it around {target_words} words."

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": story_prompt},
                        ],
                        "stream": False,
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result["message"]["content"]

        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            raise LLMError(f"Failed to generate story: {e}")


class LLMError(Exception):
    """LLM service error."""

    pass


LLM_FALLBACK_MESSAGE = "Oops! My brain got a little fuzzy. Can you ask me again?"

llm_service = LLMService()
