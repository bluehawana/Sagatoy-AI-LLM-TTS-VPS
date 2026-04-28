"""NVIDIA Nemotron LLM service for fast inference."""

import logging
import os
from typing import Optional, Tuple

import aiohttp

from sagatoyai.models import Intent

logger = logging.getLogger(__name__)


class NemotronService:
    """NVIDIA Nemotron service for LLM inference."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Nemotron service.

        Args:
            api_key: NVIDIA API key (or from env NVIDIA_API_KEY)
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            logger.warning("NVIDIA_API_KEY not set, Nemotron will not work")

        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://api.nvcf.nvidia.com/v2")
        self.model = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-mini-4b-instruct")

    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        temperature: float = 0.7,
        max_tokens: int = 200,
    ) -> str:
        """Generate response using NVIDIA Nemotron.

        Args:
            prompt: User prompt/question
            system_instruction: System instruction for behavior
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        if not self.api_key:
            raise RuntimeError("NVIDIA API key not configured")

        try:
            url = f"{self.base_url}/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"Nemotron failed: {response.status} - {error_text}")

                    result = await response.json()

                    return result["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Nemotron generation failed: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")

    async def generate_conversation_response(
        self,
        user_input: str,
        language: str = "en",
        context: Optional[list] = None,
    ) -> Tuple[str, Intent]:
        """Generate conversational response for toy interaction.

        Args:
            user_input: What the child said
            language: Language code ('en', 'sv', 'da', 'no', 'fi', 'zh')
            context: Previous conversation messages

        Returns:
            Tuple of (response_text, detected_intent)
        """
        intent = self._detect_intent(user_input)

        lang_instructions = {
            "sv": """Du är en vänlig AI-assistent i en gosig leksak som pratar med barn 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig komplicerade ord eller läskiga ämnen.
Svara alltid på svenska.""",
            "da": """Du er en venlig AI-assistent i en blød legetøj, der taler til børn i alderen 3-10 år.
Brug enkelt, varmt og opmuntrende sprog. Hold svarene korte (2-3 sætninger).
Vær legende og fantasifuld. Brug aldrig komplicerede ord eller skræmmende emner.
Svar altid på dansk.""",
            "no": """Du er en vennlig AI-assistent i en myk leke, som snakker til barn i alderen 3-10 år.
Bruk enkelt, varmt og oppmuntrende språk. Hold svarene korte (2-3 setninger).
Vær lekende og fantasifuld. Bruk aldri kompliserte ord eller skremmende emner.
Svar alltid på norsk.""",
            "fi": """Olet ystävällinen tekoälyavustaja pehmeässä lelussa, joka puhuu 3-10-vuotiaille lapsille.
Käytä yksinkertaista, lämmintä ja kannustavaa kieltä. Pidä vastaukset lyhyinä (2-3 lausetta).
Ole leikkisä ja mielikuvituksekas. Älä koskaan käytä monimutkaisia sanoja tai pelottavia aiheita.
Vastaa aina suomeksi.""",
            "zh": """你是一个友好的AI玩具助手，正在和3-10岁的孩子聊天。
使用简单、温暖和鼓励的语言。保持回答简短（2-3句话）。
要活泼有趣。不要使用复杂的词汇或可怕的话题。
始终用中文回复。""",
        }

        system_instruction = lang_instructions.get(
            language,
            """You are a friendly AI assistant inside a plush toy, talking to children aged 3-10.
Use simple, warm, and encouraging language. Keep responses short (2-3 sentences).
Be playful and imaginative. Never use complex words or scary topics.
Always respond in the same language as the child.""",
        )

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
            raise RuntimeError(f"Failed to generate conversation: {e}")

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


nemotron_service = NemotronService()