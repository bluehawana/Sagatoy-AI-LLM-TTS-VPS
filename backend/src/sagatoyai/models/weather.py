"""Weather data models."""

from datetime import datetime

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Weather information response."""

    location: str
    temperature_celsius: float
    condition: str
    description: str = Field(...,
                             description="Child-friendly weather description")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
