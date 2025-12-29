"""Streaming TTS Service - Generate audio as LLM responds.

Inspired by XiaoGPT's streaming approach.
Reduces perceived latency by starting audio playback before full response.
"""

import asyncio
import logging
import os
import re
from typing import AsyncIterator, Optional

import edge_tts

logger = logging.getLogger(__name__)


class StreamingTTSService:
    """Text-to-Speech service with streaming support.

    Two modes:
    1. Sentence streaming: Split text into sentences, TTS each immediately
    2. Chunk streaming: Stream audio chunks as they're generated

    This reduces perceived latency significantly:
    - Traditional: Wait for full LLM response → TTS → Play (3-5s)
    - Streaming: LLM sentence → TTS → Play → repeat (1-2s to first audio)
    """

    def __init__(self):
        """Initialize streaming TTS service."""
        # Voice settings
        self.voices = {
            "sv": os.getenv("TTS_VOICE_SV", "sv-SE-SofieNeural"),
            "en": os.getenv("TTS_VOICE_EN", "en-US-JennyNeural"),
        }
        self.rate = os.getenv("TTS_RATE", "-10%")

        # Sentence splitting patterns
        self.sentence_pattern = re.compile(r'[.!?]+\s*')

    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences for streaming.

        Args:
            text: Full text to split

        Returns:
            List of sentences
        """
        # Split on sentence endings
        sentences = self.sentence_pattern.split(text)

        # Filter empty and clean up
        sentences = [s.strip() for s in sentences if s.strip()]

        # If no sentences found, return whole text
        if not sentences:
            return [text]

        return sentences

    async def synthesize_streaming(
        self,
        text: str,
        language: str = "sv",
    ) -> AsyncIterator[bytes]:
        """Stream audio chunks for text.

        Args:
            text: Text to convert to speech
            language: Language code

        Yields:
            Audio chunks as bytes
        """
        voice = self.voices.get(language, self.voices["en"])

        try:
            communicate = edge_tts.Communicate(text, voice, rate=self.rate)

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]

        except Exception as e:
            logger.error(f"Streaming TTS failed: {e}")
            raise TTSStreamError(f"Failed to stream TTS: {e}")

    async def synthesize_sentences_streaming(
        self,
        text: str,
        language: str = "sv",
    ) -> AsyncIterator[tuple[str, bytes]]:
        """Stream audio sentence by sentence.

        Useful for displaying text while playing audio.

        Args:
            text: Full text to convert
            language: Language code

        Yields:
            Tuples of (sentence_text, audio_bytes)
        """
        sentences = self._split_into_sentences(text)

        for sentence in sentences:
            if not sentence:
                continue

            try:
                # Collect audio for this sentence
                audio_chunks = []
                async for chunk in self.synthesize_streaming(sentence, language):
                    audio_chunks.append(chunk)

                audio_data = b"".join(audio_chunks)
                yield (sentence, audio_data)

            except Exception as e:
                logger.error(f"Failed to synthesize sentence: {e}")
                continue

    async def synthesize_with_llm_streaming(
        self,
        llm_stream: AsyncIterator[str],
        language: str = "sv",
        min_chunk_size: int = 50,
    ) -> AsyncIterator[bytes]:
        """Stream TTS as LLM generates text.

        This is the most advanced mode - starts TTS as soon as
        we have enough text from the LLM.

        Args:
            llm_stream: Async iterator yielding text chunks from LLM
            language: Language code
            min_chunk_size: Minimum characters before starting TTS

        Yields:
            Audio chunks
        """
        buffer = ""

        async for text_chunk in llm_stream:
            buffer += text_chunk

            # Check if we have a complete sentence
            sentences = self._split_into_sentences(buffer)

            if len(sentences) > 1:
                # We have at least one complete sentence
                complete_sentence = sentences[0]
                buffer = " ".join(sentences[1:])

                # Generate TTS for complete sentence
                async for audio_chunk in self.synthesize_streaming(
                    complete_sentence, language
                ):
                    yield audio_chunk

            elif len(buffer) >= min_chunk_size and buffer.endswith((" ", ",")):
                # Buffer is getting long, flush it
                async for audio_chunk in self.synthesize_streaming(
                    buffer.strip(), language
                ):
                    yield audio_chunk
                buffer = ""

        # Flush remaining buffer
        if buffer.strip():
            async for audio_chunk in self.synthesize_streaming(
                buffer.strip(), language
            ):
                yield audio_chunk

    async def synthesize_to_bytes(
        self,
        text: str,
        language: str = "sv",
    ) -> bytes:
        """Convert text to complete audio bytes.

        Non-streaming version for compatibility.
        """
        chunks = []
        async for chunk in self.synthesize_streaming(text, language):
            chunks.append(chunk)
        return b"".join(chunks)

    async def get_audio_duration_estimate(
        self,
        text: str,
        language: str = "sv",
    ) -> float:
        """Estimate audio duration in seconds.

        Rough estimate based on word count and speaking rate.
        """
        words = len(text.split())
        # Average speaking rate: ~150 words per minute
        # With -10% rate adjustment: ~135 words per minute
        words_per_second = 135 / 60
        return words / words_per_second


class TTSStreamError(Exception):
    """TTS streaming error."""
    pass


class AudioChunkBuffer:
    """Buffer for managing audio chunks in streaming.

    Useful for the hardware side to manage playback.
    """

    def __init__(self, chunk_size: int = 4096):
        """Initialize buffer.

        Args:
            chunk_size: Size of chunks to yield
        """
        self.chunk_size = chunk_size
        self._buffer = bytearray()

    def add(self, data: bytes) -> list[bytes]:
        """Add data to buffer and return complete chunks.

        Args:
            data: Audio data to add

        Returns:
            List of complete chunks ready for playback
        """
        self._buffer.extend(data)

        chunks = []
        while len(self._buffer) >= self.chunk_size:
            chunk = bytes(self._buffer[:self.chunk_size])
            self._buffer = self._buffer[self.chunk_size:]
            chunks.append(chunk)

        return chunks

    def flush(self) -> Optional[bytes]:
        """Flush remaining data in buffer.

        Returns:
            Remaining data or None if empty
        """
        if self._buffer:
            data = bytes(self._buffer)
            self._buffer = bytearray()
            return data
        return None


# Global streaming TTS service
streaming_tts_service = StreamingTTSService()


# Example usage for hardware integration
async def example_streaming_response():
    """Example of streaming TTS with sentence-by-sentence playback."""

    text = """Hej! Jag är Saga, din vän. 
    Idag ska vi ha ett roligt äventyr tillsammans. 
    Vill du höra en saga om en modig liten kanin?"""

    print("Starting streaming TTS...")

    async for sentence, audio in streaming_tts_service.synthesize_sentences_streaming(
        text, language="sv"
    ):
        print(f"Playing: {sentence}")
        print(f"Audio size: {len(audio)} bytes")
        # In real implementation: send audio to speaker
        await asyncio.sleep(0.1)  # Simulate playback time

    print("Done!")


if __name__ == "__main__":
    asyncio.run(example_streaming_response())
