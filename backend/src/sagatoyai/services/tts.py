"""Text-to-Speech service with multi-provider and language support."""

import logging
import os
from typing import AsyncIterator

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-Speech service supporting multiple providers and languages."""

    def __init__(self, provider: str = "edge"):
        """Initialize TTS service.

        Args:
            provider: TTS provider ('edge', 'piper', 'coqui')
        """
        self.provider = provider.lower()

    async def synthesize(
        self,
        text: str,
        language: str = "en",
    ) -> AsyncIterator[bytes]:
        """Convert text to streaming audio.

        Args:
            text: Text to convert to speech
            language: Language code ('en' or 'sv')

        Yields:
            Audio chunks as bytes
        """
        if self.provider == "edge":
            async for chunk in self._synthesize_edge(text, language):
                yield chunk
        elif self.provider == "piper":
            async for chunk in self._synthesize_piper(text, language):
                yield chunk
        else:
            raise TTSError(f"Unknown TTS provider: {self.provider}")

    async def _synthesize_edge(
        self, text: str, language: str
    ) -> AsyncIterator[bytes]:
        """Synthesize using Edge TTS (cloud, free, good quality)."""
        try:
            import edge_tts

            # Select voice based on language
            # Optimized for kindergarten-age children (3-10 years)
            if language == "sv":
                # Warm, gentle Swedish
                voice = os.getenv("TTS_VOICE_SV", "sv-SE-SofieNeural")
                # Slightly slower for clarity
                rate = os.getenv("TTS_RATE", "-10%")
            else:
                voice = os.getenv(
                    "TTS_VOICE_EN", "en-US-JennyNeural")  # Warm English
                # Slightly slower for clarity
                rate = os.getenv("TTS_RATE", "-10%")

            communicate = edge_tts.Communicate(text, voice, rate=rate)

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]

        except Exception as e:
            logger.error(f"Edge TTS failed: {e}")
            raise TTSError(f"Failed to synthesize with Edge TTS: {e}")

    async def _synthesize_piper(
        self, text: str, language: str
    ) -> AsyncIterator[bytes]:
        """Synthesize using Piper TTS (local, fast, offline).

        Piper is recommended for production - it's fast, runs locally,
        and has excellent quality. Install: pip install piper-tts
        """
        try:
            import subprocess

            # Select voice model based on language
            if language == "sv":
                voice_model = "sv_SE-nst-medium"
            else:
                voice_model = "en_US-lessac-medium"

            # Run piper command
            process = subprocess.Popen(
                ["piper", "--model", voice_model, "--output-raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = process.communicate(input=text.encode())

            if process.returncode != 0:
                raise TTSError(f"Piper failed: {stderr.decode()}")

            # Yield audio in chunks
            chunk_size = 4096
            for i in range(0, len(stdout), chunk_size):
                yield stdout[i: i + chunk_size]

        except FileNotFoundError:
            logger.warning("Piper not installed, falling back to Edge TTS")
            async for chunk in self._synthesize_edge(text, language):
                yield chunk
        except Exception as e:
            logger.error(f"Piper TTS failed: {e}")
            raise TTSError(f"Failed to synthesize with Piper: {e}")

    async def synthesize_to_bytes(self, text: str, language: str = "en") -> bytes:
        """Convert text to complete audio bytes."""
        chunks = []
        async for chunk in self.synthesize(text, language):
            chunks.append(chunk)
        return b"".join(chunks)


class TTSError(Exception):
    """TTS service error."""

    pass


# Fallback messages by language
TTS_FALLBACK_MESSAGES = {
    "en": "I'm having trouble speaking right now. Please try again!",
    "sv": "Jag har problem med att prata just nu. Försök igen!",
}

# Global TTS service instance
tts_service = TTSService()
