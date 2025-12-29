"""Conversation data models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Intent(str, Enum):
    """Detected conversation intent."""

    WEATHER = "weather"
    STORY = "story"
    SONG = "song"
    MATH = "math"
    GENERAL = "general"


class ConversationRequest(BaseModel):
    """Incoming conversation request from device."""

    device_id: str
    session_id: str
    audio_data: str = Field(..., description="Base64 encoded audio")
    sample_rate: int = 16000
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationResponse(BaseModel):
    """Response to conversation request."""

    session_id: str
    transcript: str
    response_text: str
    intent: Intent
    audio_url: Optional[str] = Field(
        None, description="Streaming audio endpoint")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    """Single message in conversation history."""

    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SessionContext(BaseModel):
    """Conversation session context."""

    session_id: str
    device_id: str
    messages: list[Message] = Field(default_factory=list)
    current_story: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
