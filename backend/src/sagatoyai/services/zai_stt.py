"""Z.ai (智谱AI) STT service for speech-to-text."""

import base64
import io
import logging
import os
from dataclasses import dataclass
from typing import Optional, Tuple

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class ZAITranscriptResult:
    """Result from Z.ai STT transcription."""
    text: str
    confidence: float = 1.0
    language: str = "en"


class ZAI_STTService:
    """Speech-to-Text service using Z.ai GLM-ASR-2512."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Z.ai STT service.
        
        Args:
            api_key: Z.ai API key. Defaults to env Z_AI_API_KEY
        """
        self.api_key = api_key or os.getenv("Z_AI_API_KEY")
        if not self.api_key:
            logger.warning("Z_AI_API_KEY not set, Z.ai STT will not work")
        
        # Use overseas endpoint by default
        self.base_url = os.getenv("Z_AI_BASE_URL", "https://api.z.ai/api/paas/v4")
        self.model = "glm-asr-2512"

    async def transcribe(
        self,
        audio_data: bytes,
        sample_rate: int = 16000,
    ) -> ZAITranscriptResult:
        """Convert audio to text using Z.ai GLM-ASR.
        
        Args:
            audio_data: Raw audio bytes (WAV format preferred)
            sample_rate: Audio sample rate (default 16000)
            
        Returns:
            TranscriptResult with text and metadata
        """
        if not self.api_key:
            raise RuntimeError("Z.ai API key not configured")
        
        try:
            # Convert audio to base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            url = f"{self.base_url}/audio/transcriptions"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            # Build multipart form data
            boundary = "----WebKitFormBoundary" + "abcdefghijklmnop"
            
            body = f"--{boundary}\r\n"
            body += 'Content-Disposition: form-data; name="model"\r\n\r\n'
            body += f"{self.model}\r\n"
            body += f"--{boundary}\r\n"
            body += 'Content-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
            body += "Content-Type: audio/wav\r\n\r\n"
            
            # Add audio data
            import struct
            # Create WAV header for the audio data
            import wave
            
            # Save to BytesIO with WAV header
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            
            wav_data = wav_buffer.getvalue()
            audio_base64 = base64.b64encode(wav_data).decode('utf-8')
            
            body = f"--{boundary}\r\n"
            body += 'Content-Disposition: form-data; name="model"\r\n\r\n'
            body += f"{self.model}\r\n"
            body += f"--{boundary}\r\n"
            body += 'Content-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
            body += "Content-Type: audio/wav\r\n\r\n"
            body = body.encode('utf-8') + wav_data + f"\r\n--{boundary}--\r\n".encode('utf-8')
            
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=body, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"Z.ai STT failed: {response.status} - {error_text}")
                    
                    result = await response.json()
                    
                    # Parse response
                    text = result.get("text", "")
                    language = self._detect_language(text)
                    
                    logger.info(f"Z.ai STT result: {text[:50]}...")
                    
                    return ZAITranscriptResult(
                        text=text,
                        confidence=0.9,
                        language=language
                    )
                    
        except Exception as e:
            logger.error(f"Z.ai STT error: {e}")
            raise RuntimeError(f"Failed to transcribe audio: {e}")

    def _detect_language(self, text: str) -> str:
        """Simple language detection based on character ranges."""
        # Check for Chinese characters
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return "zh"
        return "en"


# Default instance
zai_stt_service = ZAI_STTService()