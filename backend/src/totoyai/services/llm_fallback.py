"""LLM Fallback Service - Try multiple LLMs with automatic fallback.

Inspired by XiaoGPT's multi-LLM approach.
Provides resilience by trying multiple LLM providers in sequence.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Awaitable

from totoyai.models import Intent
from totoyai.services.groq_service import groq_service, GroqError
from totoyai.services.gemini import gemini_service, GeminiError

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Available LLM providers."""

    GROQ = "groq"
    GEMINI = "gemini"
    OLLAMA = "ollama"


@dataclass
class LLMResult:
    """Result from LLM generation."""

    text: str
    intent: Intent
    provider: LLMProvider
    latency_ms: float
    fallback_used: bool = False
    fallback_reason: Optional[str] = None


class LLMFallbackService:
    """LLM service with automatic fallback between providers.

    Tries providers in order of preference:
    1. Groq (fastest, ~0.5s)
    2. Gemini (smart, ~1-2s)
    3. Ollama (local, variable)

    If one fails, automatically tries the next.
    """

    def __init__(
        self,
        primary: LLMProvider = LLMProvider.GROQ,
        fallbacks: Optional[list[LLMProvider]] = None,
    ):
        """Initialize fallback service.

        Args:
            primary: Primary LLM provider to try first
            fallbacks: List of fallback providers in order
        """
        self.primary = primary
        self.fallbacks = fallbacks or [LLMProvider.GEMINI]

        # Track provider health
        self._provider_failures: dict[LLMProvider, int] = {}
        self._max_failures = 3  # Temporarily skip provider after N failures

    def _is_provider_healthy(self, provider: LLMProvider) -> bool:
        """Check if provider is healthy (not too many recent failures)."""
        return self._provider_failures.get(provider, 0) < self._max_failures

    def _record_success(self, provider: LLMProvider) -> None:
        """Record successful call, reset failure count."""
        self._provider_failures[provider] = 0

    def _record_failure(self, provider: LLMProvider) -> None:
        """Record failed call."""
        self._provider_failures[provider] = self._provider_failures.get(
            provider, 0) + 1
        logger.warning(
            f"Provider {provider} failed, "
            f"failure count: {self._provider_failures[provider]}"
        )

    async def _call_groq(
        self,
        user_input: str,
        language: str,
        context: Optional[list] = None,
    ) -> tuple[str, Intent]:
        """Call Groq LLM."""
        return await groq_service.generate_conversation_response(
            user_input=user_input,
            language=language,
            context=context,
        )

    async def _call_gemini(
        self,
        user_input: str,
        language: str,
        context: Optional[list] = None,
    ) -> tuple[str, Intent]:
        """Call Gemini LLM."""
        return await gemini_service.generate_conversation_response(
            user_input=user_input,
            language=language,
            context=context,
        )

    async def _call_provider(
        self,
        provider: LLMProvider,
        user_input: str,
        language: str,
        context: Optional[list] = None,
    ) -> tuple[str, Intent]:
        """Call specific LLM provider."""
        if provider == LLMProvider.GROQ:
            return await self._call_groq(user_input, language, context)
        elif provider == LLMProvider.GEMINI:
            return await self._call_gemini(user_input, language, context)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def generate_response(
        self,
        user_input: str,
        language: str = "sv",
        context: Optional[list] = None,
    ) -> LLMResult:
        """Generate response with automatic fallback.

        Args:
            user_input: User's message
            language: Language code ('en' or 'sv')
            context: Previous conversation context

        Returns:
            LLMResult with response and metadata
        """
        import time

        # Build provider order
        providers = [self.primary] + self.fallbacks

        # Filter to healthy providers
        healthy_providers = [
            p for p in providers if self._is_provider_healthy(p)]

        # If no healthy providers, try all anyway
        if not healthy_providers:
            logger.warning("No healthy providers, trying all")
            healthy_providers = providers
            # Reset failure counts
            self._provider_failures = {}

        last_error = None
        fallback_used = False
        fallback_reason = None

        for i, provider in enumerate(healthy_providers):
            try:
                start_time = time.time()

                logger.info(f"Trying LLM provider: {provider}")
                text, intent = await self._call_provider(
                    provider, user_input, language, context
                )

                latency_ms = (time.time() - start_time) * 1000

                self._record_success(provider)

                logger.info(
                    f"LLM response from {provider} in {latency_ms:.0f}ms"
                )

                return LLMResult(
                    text=text,
                    intent=intent,
                    provider=provider,
                    latency_ms=latency_ms,
                    fallback_used=fallback_used,
                    fallback_reason=fallback_reason,
                )

            except (GroqError, GeminiError, Exception) as e:
                last_error = e
                self._record_failure(provider)

                if i < len(healthy_providers) - 1:
                    fallback_used = True
                    fallback_reason = f"{provider} failed: {str(e)[:50]}"
                    logger.warning(
                        f"Provider {provider} failed, trying next: {e}"
                    )
                else:
                    logger.error(f"All providers failed, last error: {e}")

        # All providers failed, return fallback message
        fallback_messages = {
            "en": "Oops! My brain got a little fuzzy. Can you ask me again?",
            "sv": "Hoppsan! Mitt huvud blev lite grumligt. Kan du fråga igen?",
        }

        return LLMResult(
            text=fallback_messages.get(language, fallback_messages["en"]),
            intent=Intent.GENERAL,
            provider=self.primary,
            latency_ms=0,
            fallback_used=True,
            fallback_reason=f"All providers failed: {last_error}",
        )

    async def generate_story(
        self,
        story_prompt: str,
        language: str = "sv",
    ) -> str:
        """Generate story with fallback.

        Stories are longer, so we prefer Gemini for quality.
        """
        providers = [LLMProvider.GEMINI, LLMProvider.GROQ]

        for provider in providers:
            try:
                if provider == LLMProvider.GEMINI:
                    return await gemini_service.generate_story(
                        story_prompt=story_prompt,
                        language=language,
                    )
                elif provider == LLMProvider.GROQ:
                    # Groq can also generate stories
                    system_prompt = gemini_service.storybook_prompt
                    return await groq_service.generate_response(
                        prompt=story_prompt,
                        system_instruction=system_prompt,
                        temperature=0.8,
                        max_tokens=1500,
                    )
            except Exception as e:
                logger.warning(f"Story generation failed with {provider}: {e}")
                continue

        # Fallback story
        if language == "sv":
            return "Det var en gång en liten kanin som ville ha ett äventyr. Men just nu är sagoberättaren lite trött. Kom tillbaka snart för fler sagor!"
        return "Once upon a time, there was a little rabbit who wanted an adventure. But the storyteller is a bit tired right now. Come back soon for more stories!"

    def get_provider_status(self) -> dict:
        """Get status of all providers."""
        return {
            provider.value: {
                "failures": self._provider_failures.get(provider, 0),
                "healthy": self._is_provider_healthy(provider),
            }
            for provider in LLMProvider
        }


# Global fallback service instance
llm_fallback_service = LLMFallbackService(
    primary=LLMProvider.GROQ,
    fallbacks=[LLMProvider.GEMINI],
)
