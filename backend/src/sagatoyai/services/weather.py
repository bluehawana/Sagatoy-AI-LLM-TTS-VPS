"""Weather service using Open-Meteo API."""

import logging
from datetime import datetime

import httpx

from sagatoyai.models import WeatherData

logger = logging.getLogger(__name__)

# Location coordinates (can be expanded to support multiple cities)
LOCATIONS = {
    "stockholm": {"lat": 59.3293, "lon": 18.0686},
    "gothenburg": {"lat": 57.7089, "lon": 11.9746},
    "malmo": {"lat": 55.6050, "lon": 13.0038},
}


class WeatherService:
    """Weather service using Open-Meteo free API."""

    def __init__(self):
        """Initialize weather service."""
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def _get_child_friendly_description(
        self, temperature: float, condition_code: int
    ) -> str:
        """Generate child-friendly weather description."""
        # Weather condition codes from Open-Meteo
        if condition_code == 0:
            condition = "sunny"
            desc = "It's bright and sunny outside! Perfect for playing!"
        elif condition_code in [1, 2]:
            condition = "partly cloudy"
            desc = "There are some fluffy clouds in the sky today!"
        elif condition_code == 3:
            condition = "cloudy"
            desc = "The sky is covered with soft, gray clouds!"
        elif condition_code in [45, 48]:
            condition = "foggy"
            desc = "It's foggy outside, like walking through a cloud!"
        elif condition_code in [51, 53, 55, 61, 63, 65]:
            condition = "rainy"
            desc = "It's raining! Don't forget your umbrella and rain boots!"
        elif condition_code in [71, 73, 75, 77]:
            condition = "snowy"
            desc = "It's snowing! Time to build a snowman!"
        elif condition_code in [80, 81, 82]:
            condition = "showery"
            desc = "There are rain showers today!"
        elif condition_code in [95, 96, 99]:
            condition = "stormy"
            desc = "There's a thunderstorm! Let's stay inside and be cozy!"
        else:
            condition = "changing"
            desc = "The weather is changing today!"

        # Add temperature context
        if temperature < 0:
            desc += " It's very cold, so bundle up warm!"
        elif temperature < 10:
            desc += " It's chilly, wear a jacket!"
        elif temperature < 20:
            desc += " It's nice and cool outside!"
        elif temperature < 25:
            desc += " It's warm and pleasant!"
        else:
            desc += " It's hot! Stay cool and drink water!"

        return desc

    async def get_weather(self, location: str = "stockholm") -> WeatherData:
        """Get weather information for a location."""
        try:
            location_lower = location.lower()
            coords = LOCATIONS.get(location_lower, LOCATIONS["stockholm"])

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "latitude": coords["lat"],
                        "longitude": coords["lon"],
                        "current": "temperature_2m,weather_code",
                        "timezone": "Europe/Stockholm",
                    },
                )
                response.raise_for_status()
                data = response.json()

                current = data["current"]
                temperature = current["temperature_2m"]
                weather_code = current["weather_code"]

                description = self._get_child_friendly_description(
                    temperature, weather_code
                )

                # Determine condition name
                if weather_code == 0:
                    condition = "sunny"
                elif weather_code in [1, 2, 3]:
                    condition = "cloudy"
                elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
                    condition = "rainy"
                elif weather_code in [71, 73, 75, 77]:
                    condition = "snowy"
                else:
                    condition = "variable"

                return WeatherData(
                    location=location.title(),
                    temperature_celsius=temperature,
                    condition=condition,
                    description=description,
                    timestamp=datetime.utcnow(),
                )

        except Exception as e:
            logger.error(f"Weather service failed: {e}")
            raise WeatherError(f"Failed to get weather data: {e}")


class WeatherError(Exception):
    """Weather service error."""

    pass


WEATHER_FALLBACK_MESSAGE = (
    "I can't check the weather right now, but you can look outside!"
)

weather_service = WeatherService()
