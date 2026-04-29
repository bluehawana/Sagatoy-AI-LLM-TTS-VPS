"""API route definitions."""

import base64
import logging

from fastapi import APIRouter, Depends

from sagatoyai.api.dependencies import get_current_device
from sagatoyai.models import (
    ConversationRequest,
    ConversationResponse,
    DeviceAuth,
    DeviceTokens,
    Intent,
    WeatherData,
)
from sagatoyai.services.auth import TokenData, create_access_token, create_refresh_token
from sagatoyai.services.content_filter import contains_inappropriate_content, filter_content
from sagatoyai.services.language import detect_language
from sagatoyai.services.llm_fallback import llm_fallback_service
from sagatoyai.services.stt import stt_service
from sagatoyai.services.tts import tts_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/auth/device", response_model=DeviceTokens)
async def authenticate_device(auth: DeviceAuth) -> DeviceTokens:
    """Authenticate a device and return tokens."""
    # TODO: Validate device credentials against database
    # For now, accept any device_id/secret combination
    access_token = create_access_token(auth.device_id)
    refresh_token = create_refresh_token(auth.device_id)
    return DeviceTokens(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/conversation", response_model=ConversationResponse)
async def conversation(
    request: ConversationRequest,
    device: TokenData = Depends(get_current_device),
) -> ConversationResponse:
    """Process conversation request: STT -> LLM -> TTS pipeline."""
    try:
        audio_bytes = base64.b64decode(request.audio_data)
        if not audio_bytes or len(audio_bytes) == 0:
            return ConversationResponse(
                session_id=request.session_id,
                transcript="",
                response_text="I didn't hear anything. Can you try again?",
                intent=Intent.GENERAL,
                audio_url=None,
            )
    except Exception as e:
        return ConversationResponse(
            session_id=request.session_id,
            transcript="",
            response_text="I had trouble understanding the audio. Can you try again?",
            intent=Intent.GENERAL,
            audio_url=None,
        )

    try:
        transcript = await stt_service.transcribe_base64(request.audio_data, request.sample_rate)
        if not transcript.text or transcript.text.strip() == "":
            return ConversationResponse(
                session_id=request.session_id,
                transcript=transcript.text,
                response_text="I didn't catch that clearly. Could you say it again?",
                intent=Intent.GENERAL,
                audio_url=None,
            )

        logger.info(f"Transcribed: {transcript.text[:200]} (lang: {transcript.language})")
    except Exception as e:
        logger.error(f"STT transcription failed: {e}")
        return ConversationResponse(
            session_id=request.session_id,
            transcript="",
            response_text="I'm having trouble hearing right now. Can you try again?",
            intent=Intent.GENERAL,
            audio_url=None,
        )

    # Call LLM with fallback chain (Groq → Gemini)
    language = transcript.language if transcript.language and transcript.language != "en" else "en"
    try:
        llm_result = await llm_fallback_service.generate_response(
            user_input=transcript.text,
            language=language,
        )
        intent = llm_result.intent
        response_text = llm_result.text
        logger.info(f"LLM response from {llm_result.provider}: {response_text[:100]}")
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return ConversationResponse(
            session_id=request.session_id,
            transcript=transcript.text,
            response_text="I'm thinking about an answer but my brain is a bit slow right now. Can you ask me again?",
            intent=Intent.GENERAL,
            audio_url=None,
        )

    # Step 5: Content filtering for child safety
    if contains_inappropriate_content(response_text):
        logger.warning(f"Content filter triggered for message: {transcript.text[:200]}")
        response_text = filter_content(response_text)

    # Step 4: Synthesize TTS audio
    audio_bytes = b""
    try:
        audio_bytes = await tts_service.synthesize_to_bytes(response_text, language=language)
        logger.info(f"TTS audio generated: {len(audio_bytes)} bytes")
    except Exception as e:
        logger.error(f"TTS synthesis failed: {e}")

    return ConversationResponse(
        session_id=request.session_id,
        transcript=transcript.text,
        response_text=response_text,
        intent=intent,
        audio_url=f"data:audio/wav;base64,{base64.b64encode(audio_bytes).decode('utf-8')}" if audio_bytes else None,
    )


@router.get("/weather", response_model=WeatherData)
async def get_weather(
    location: str = "Stockholm",
    device: TokenData = Depends(get_current_device),
) -> WeatherData:
    """Get weather information for a location."""
    # TODO: Implement weather service
    return WeatherData(
        location=location,
        temperature_celsius=15.0,
        condition="cloudy",
        description="It's a bit cloudy today, like a fluffy blanket in the sky!",
    )
