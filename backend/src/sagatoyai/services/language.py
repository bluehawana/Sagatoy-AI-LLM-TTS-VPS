"""Language detection and management."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Swedish keywords for detection
SWEDISH_KEYWORDS = [
    "hej",
    "hallå",
    "tjena",
    "morsning",
    "godmorgon",
    "godnatt",
    "tack",
    "varsågod",
    "förlåt",
    "ja",
    "nej",
]

# English keywords for detection
ENGLISH_KEYWORDS = [
    "hello",
    "hi",
    "hey",
    "good morning",
    "good night",
    "thanks",
    "please",
    "sorry",
    "yes",
    "no",
]


def detect_language(text: str) -> str:
    """Detect language from text.

    Args:
        text: Input text to analyze

    Returns:
        Language code: 'sv' for Swedish, 'en' for English
    """
    text_lower = text.lower()

    # Check for Swedish keywords
    swedish_matches = sum(
        1 for keyword in SWEDISH_KEYWORDS if keyword in text_lower)

    # Check for English keywords
    english_matches = sum(
        1 for keyword in ENGLISH_KEYWORDS if keyword in text_lower)

    # Return detected language
    if swedish_matches > english_matches:
        logger.info(f"Detected Swedish language (matches: {swedish_matches})")
        return "sv"
    else:
        logger.info(f"Detected English language (matches: {english_matches})")
        return "en"


def get_system_prompt(language: str) -> str:
    """Get system prompt for LLM based on language.

    Args:
        language: Language code ('sv' or 'en')

    Returns:
        System prompt in the specified language
    """
    if language == "sv":
        return """Du är en vänlig AI-assistent i en gosig leksak som pratar med barn mellan 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig komplicerade ord eller läskiga ämnen.
Svara alltid på svenska."""
    else:
        return """You are a friendly AI assistant inside a plush toy, talking to children aged 3-10.
Use simple, warm, and encouraging language. Keep responses short (2-3 sentences).
Be playful and imaginative. Never use complex words or scary topics.
Always respond in English."""


def get_tts_voice(language: str) -> str:
    """Get TTS voice based on language.

    Args:
        language: Language code ('sv' or 'en')

    Returns:
        Voice identifier for TTS service
    """
    if language == "sv":
        return "sv-SE-HilleviNeural"  # Child-friendly Swedish voice
    else:
        return "en-US-JennyNeural"  # Warm English voice


def get_weather_description_language(language: str) -> dict:
    """Get weather description templates by language.

    Args:
        language: Language code ('sv' or 'en')

    Returns:
        Dictionary of weather description templates
    """
    if language == "sv":
        return {
            "sunny": "Det är soligt ute! Perfekt för att leka!",
            "cloudy": "Det finns några fluffiga moln på himlen idag!",
            "rainy": "Det regnar! Glöm inte ditt paraply och stövlar!",
            "snowy": "Det snöar! Dags att bygga en snögubbe!",
            "cold": "Det är kallt, klä dig varmt!",
            "warm": "Det är varmt och skönt!",
        }
    else:
        return {
            "sunny": "It's sunny outside! Perfect for playing!",
            "cloudy": "There are some fluffy clouds in the sky today!",
            "rainy": "It's raining! Don't forget your umbrella and boots!",
            "snowy": "It's snowing! Time to build a snowman!",
            "cold": "It's cold, bundle up warm!",
            "warm": "It's warm and pleasant!",
        }
