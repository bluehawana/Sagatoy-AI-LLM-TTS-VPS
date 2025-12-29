"""Device data models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Device(BaseModel):
    """Registered toy device."""

    device_id: str = Field(..., description="Unique device identifier (UUID)")
    device_secret_hash: str = Field(..., description="Hashed device secret")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: Optional[datetime] = None
    firmware_version: Optional[str] = None
    owner_email: Optional[str] = Field(
        None, description="Optional owner email for GDPR")


class DeviceAuth(BaseModel):
    """Device authentication request."""

    device_id: str
    device_secret: str


class DeviceTokens(BaseModel):
    """Authentication tokens response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
