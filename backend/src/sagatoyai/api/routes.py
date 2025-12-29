"""API route definitions."""

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
    # TODO: Implement full pipeline
    return ConversationResponse(
        session_id=request.session_id,
        transcript="placeholder transcript",
        response_text="Hello! I'm your friendly toy assistant.",
        intent=Intent.GENERAL,
        audio_url=None,
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
