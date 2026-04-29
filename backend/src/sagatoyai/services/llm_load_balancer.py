"""LLM Load Balancer for Sagatoy — prioritizes speed and Nordic quality.

Strategy:
1. Groq LLaMA 3.1 70B (free, fast, great Nordic) — primary
2. OpenAI GPT-4o mini (paid, fast, best Nordic) — premium
3. Google Gemini (free, fast, good Nordic) — premium
4. NVIDIA Nemotron 4B (free, very fast, poor Nordic) — last resort

Never use NVIDIA LLaMA 3.1 70B — 13+ second latency kills interactivity.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from sagatoyai.models import Intent
from sagatoyai.services.groq_service import groq_service, GroqError
from sagatoyai.services.openai_llm import openai_llm_service
from sagatoyai.services.gemini import gemini_service, GeminiError
from sagatoyai.services.nemotron import nim_service

logger = logging.getLogger(__name__)


class Provider(str, Enum):
    GROQ = "groq"
    OPENAI = "openai"
    GEMINI = "gemini"
    NVIDIA = "nvidia"


@dataclass
class LLMResult:
    text: str
    intent: Intent
    provider: Provider
    latency_ms: float
    fallback_used: bool = False
    fallback_reason: Optional[str] = None


# Track per-provider health with exponential cooldown
class ProviderHealth:
    def __init__(self):
        self.failures: dict[Provider, int] = {}
        self.cooldown_until: dict[Provider, float] = {}
        self.last_success: dict[Provider, float] = {}

    def record_failure(self, provider: Provider):
        self.failures[provider] = self.failures.get(provider, 0) + 1
        # Exponential cooldown: 1s → 5s → 30s → 2min → 5min
        cooldowns = [1, 5, 30, 120, 300]
        idx = min(self.failures[provider], len(cooldowns) - 1)
        self.cooldown_until[provider] = time.time() + cooldowns[idx]
        logger.warning(f"Provider {provider} failed (count={self.failures[provider]}), cooldown {cooldowns[idx]}s")

    def record_success(self, provider: Provider):
        self.failures[provider] = 0
        self.cooldown_until.pop(provider, None)
        self.last_success[provider] = time.time()

    def is_available(self, provider: Provider) -> bool:
        if provider not in self.failures or self.failures[provider] == 0:
            return True
        if time.time() < self.cooldown_until.get(provider, 0):
            return False
        # Cooldown expired, reset and allow trial
        if self.failures[provider] > 0:
            self.record_success(provider)
            return True
        return True


# Available Groq models (free tier)
GROQ_MODELS = {
    "llama-3.3-70b-versatile": "LLaMA 3.3 70B (best free)",
    "llama-3.1-8b-instant": "LLaMA 3.1 8B (fast, weaker)",
    "gemma2-9b-it": "Gemma2 9B (fast, weak)",
    "mixtral-8x7b-32768": "Mixtral 8x7B (medium)",
}


class LLMLoadBalancer:
    """Smart LLM load balancer optimized for Nordic kids toy.

    Uses weighted routing:
    - Groq primary (free, fast)
    - OpenAI/Gemini as premium fallbacks
    - NVIDIA as speed backup (poor Nordic, but fast)
    """

    # Health tracking is module-level so all instances share it
    health = ProviderHealth()

    def __init__(
        self,
        primary: Provider = Provider.GROQ,
        premium_fallbacks: Optional[list[Provider]] = None,
        speed_backup: Optional[Provider] = None,
        max_fallback_time_ms: int = 8000,
    ):
        self.primary = primary
        self.premium_fallbacks = premium_fallbacks or [Provider.OPENAI]
        self.speed_backup = speed_backup  # Used if premium also fails
        self.max_fallback_time_ms = max_fallback_time_ms

        # Track which providers are configured (have API keys)
        self._configured_providers = set()
        if os.getenv("GROQ_API_KEY"):
            self._configured_providers.add(Provider.GROQ)
        if os.getenv("OPENAI_API_KEY"):
            self._configured_providers.add(Provider.OPENAI)
        if os.getenv("GOOGLE_API_KEY"):
            self._configured_providers.add(Provider.GEMINI)
        if os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY"):
            self._configured_providers.add(Provider.NVIDIA)

    def _get_provider_list(self) -> list[Provider]:
        """Get ordered provider list based on current config and availability."""
        # Start with primary
        providers = [self.primary]

        # Add premium fallbacks
        for p in self.premium_fallbacks:
            if p != self.primary and p in self._configured_providers:
                providers.append(p)

        # Add speed backup last
        if self.speed_backup and self.speed_backup != self.primary and self.speed_backup in self._configured_providers:
            providers.append(self.speed_backup)

        # Filter to configured providers
        return [p for p in providers if p in self._configured_providers]

    async def _call_groq(self, user_input: str, language: str, context: Optional[list] = None) -> tuple[str, Intent]:
        return await groq_service.generate_conversation_response(user_input, language, context)

    async def _call_openai(self, user_input: str, language: str, context: Optional[list] = None) -> tuple[str, Intent]:
        return await openai_llm_service.generate_conversation_response(user_input, language, context)

    async def _call_gemini(self, user_input: str, language: str, context: Optional[list] = None) -> tuple[str, Intent]:
        return await gemini_service.generate_conversation_response(user_input, language, context)

    async def _call_nim(self, user_input: str, language: str, context: Optional[list] = None) -> tuple[str, Intent]:
        return await nim_service.generate_conversation_response(user_input, language, context)

    async def generate_response(
        self,
        user_input: str,
        language: str = "sv",
        context: Optional[list] = None,
    ) -> LLMResult:
        """Generate response with smart fallback routing.

        Flow: primary → premium fallback(s) → speed backup → safe message
        """
        providers = self._get_provider_list()
        if not providers:
            logger.error("No LLM providers configured — check API keys in .env")
            return LLMResult(
                text="My batteries are dead. Try again later!",
                intent=Intent.GENERAL,
                provider=self.primary,
                latency_ms=0,
                fallback_used=False,
                fallback_reason="No providers configured",
            )

        # Start timer for total budget
        total_start = time.time()
        last_error = None
        fallback_used = False
        fallback_reason = None

        for i, provider in enumerate(providers):
            remaining_ms = self.max_fallback_time_ms - (time.time() - total_start) * 1000
            if remaining_ms <= 0:
                logger.warning("Total LLM time budget exhausted")
                break

            provider_start = time.time()

            try:
                logger.info(f"Trying LLM: {provider}")
                text, intent = await self._call_provider(provider, user_input, language, context)

                latency_ms = (time.time() - provider_start) * 1000
                total_latency = (time.time() - total_start) * 1000

                self.health.record_success(provider)

                logger.info(f"LLM response from {provider} in {latency_ms:.0f}ms (total: {total_latency:.0f}ms)")
                return LLMResult(
                    text=text,
                    intent=intent,
                    provider=provider,
                    latency_ms=latency_ms,
                    fallback_used=fallback_used,
                    fallback_reason=fallback_reason,
                )

            except Exception as e:
                provider_elapsed = (time.time() - provider_start) * 1000
                self.health.record_failure(provider)
                last_error = e

                if i < len(providers) - 1 and remaining_ms > 2000:
                    fallback_used = True
                    fallback_reason = f"{provider} failed after {provider_elapsed:.0f}ms: {str(e)[:80]}"
                    logger.warning(f"Fallback: {fallback_reason}")
                else:
                    logger.error(f"Provider {provider} final attempt failed: {e}")

        # All providers failed — return safe message
        fallback_msg = {
            "sv": "Hoppsan! Jag förstår inte just nu. Kan du fråga igen?",
            "en": "Oops! I don't understand right now. Can you ask again?",
            "da": "Ups! Jeg forstår ikke lige nu. Kan du spørge igen?",
            "no": "Oisann! Forstår ikke akkurat nå. Kan du spørje igjen?",
            "fi": "Hups! En ymmärrä juuri nyt. Voitko kysyä uudelleen?",
            "zh": "哎呀，我现在不太明白。你能再说一遍吗？",
        }
        return LLMResult(
            text=fallback_msg.get(language, fallback_msg["en"]),
            intent=Intent.GENERAL,
            provider=self.primary,
            latency_ms=0,
            fallback_used=True,
            fallback_reason=f"All providers failed: {last_error}",
        )

    async def _call_provider(self, provider: Provider, user_input: str, language: str, context: Optional[list] = None) -> tuple[str, Intent]:
        calls = {
            Provider.GROQ: self._call_groq,
            Provider.OPENAI: self._call_openai,
            Provider.GEMINI: self._call_gemini,
            Provider.NVIDIA: self._call_nim,
        }
        fn = calls[provider]
        if fn is None:
            raise ValueError(f"Unknown provider: {provider}")
        return await fn(user_input, language, context)

    def status(self) -> dict:
        """Get health status of all providers."""
        return {
            p.value: {
                "configured": p in self._configured_providers,
                "failures": self.health.failures.get(p, 0),
                "cooldown": self.health.cooldown_until.get(p, 0) > time.time(),
                "last_success": self.health.last_success.get(p, 0),
            }
            for p in Provider
        }

    def list_available_groq_models(self) -> dict:
        """Available Groq models (free tier)."""
        return GROQ_MODELS


# Default load balancer instance
# Chain: Groq (free/fast) → OpenAI (premium) → Gemini (premium) → NVIDIA (speed backup)
llm_balancer = LLMLoadBalancer(
    primary=Provider.GROQ,
    premium_fallbacks=[Provider.OPENAI, Provider.GEMINI],
    speed_backup=Provider.NVIDIA,
)

# Backward compatibility — routes.py still uses llm_fallback_service
llm_fallback_service = llm_balancer
