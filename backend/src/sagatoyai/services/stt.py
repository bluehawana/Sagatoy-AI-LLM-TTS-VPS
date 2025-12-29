"""Speech-to-Text service using Whisper."""

import base64
import io
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# Whisper model will be loaded lazily
_whisper_model = None


@dataclass
class TranscriptResult:
    """Result from STT transcription."""

    text: str
    confidence: float
    language: str


class STTService:
    """Speech-to-Text service using OpenAI Whisper."""

    def __init__(self, model_name: str = "base"):
        """Initialize STT service with specified model."""
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        """Lazy load Whisper model."""
        global _whisper_model
        if _whisper_model is None:
            import whisper

            logger.info(f"Loading Whisper model: {self.model_name}")
            _whisper_model = whisper.load_model(self.model_name)
        self._model = _whisper_model

    async def transcribe(
        self,
        audio_data: bytes,
        sample_rate: int = 16000,
    ) -> TranscriptResult:
        """Convert audio to text.

        Args:
            audio_data: Raw audio bytes
            sample_rate: Audio sample rate (default 16kHz)

        Returns:
            TranscriptResult with transcribed text
        """
        if self._model is None:
            self._load_model()

        try:
            import numpy as np
            import torch

            # Convert bytes to numpy array
            audio_array = np.frombuffer(
                audio_data, dtype=np.int16).astype(np.float32)
            audio_array = audio_array / 32768.0  # Normalize to [-1, 1]

            # Transcribe
            result = self._model.transcribe(
                audio_array,
                language="en",
                fp16=torch.cuda.is_available(),
            )

            return TranscriptResult(
                text=result["text"].strip(),
                confidence=1.0,  # Whisper doesn't provide confidence scores
                language=result.get("language", "en"),
            )

        except Exception as e:
            logger.error(f"STT transcription failed: {e}")
            raise STTError(f"Failed to transcribe audio: {e}")

    async def transcribe_base64(
        self,
        audio_base64: str,
        sample_rate: int = 16000,
    ) -> TranscriptResult:
        """Transcribe base64-encoded audio."""
        audio_data = base64.b64decode(audio_base64)
        return await self.transcribe(audio_data, sample_rate)


class STTError(Exception):
    """STT service error."""

    pass


# Fallback message for STT failures
STT_FALLBACK_MESSAGE = "I didn't quite catch that. Could you please say that again?"

# Global STT service instance
stt_service = STTService()
