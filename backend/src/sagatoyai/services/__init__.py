"""Backend services: STT, LLM, TTS, Weather, Session, and more.

New features inspired by XiaoGPT:
- Conversation context management
- LLM fallback (Groq → Gemini)
- Streaming TTS
"""

from sagatoyai.services.session import SessionManager, session_manager
from sagatoyai.services.conversation_context import (
    ConversationContext,
    ConversationContextManager,
    conversation_manager,
)
from sagatoyai.services.llm_fallback import (
    LLMFallbackService,
    LLMProvider,
    LLMResult,
    llm_fallback_service,
)
from sagatoyai.services.streaming_tts import (
    StreamingTTSService,
    AudioChunkBuffer,
    streaming_tts_service,
)
from sagatoyai.services.groq_service import groq_service, GroqService
from sagatoyai.services.gemini import gemini_service, GeminiService
from sagatoyai.services.tts import tts_service, TTSService
from sagatoyai.services.weather import weather_service, WeatherService
from sagatoyai.services.story_library import (
    get_story_series,
    get_series_list,
    get_stories_in_series,
    get_story_prompt,
)

__all__ = [
    # Session management
    "SessionManager",
    "session_manager",
    # Conversation context (NEW)
    "ConversationContext",
    "ConversationContextManager",
    "conversation_manager",
    # LLM fallback (NEW)
    "LLMFallbackService",
    "LLMProvider",
    "LLMResult",
    "llm_fallback_service",
    # Streaming TTS (NEW)
    "StreamingTTSService",
    "AudioChunkBuffer",
    "streaming_tts_service",
    # LLM services
    "groq_service",
    "GroqService",
    "gemini_service",
    "GeminiService",
    # TTS
    "tts_service",
    "TTSService",
    # Weather
    "weather_service",
    "WeatherService",
    # Stories
    "get_story_series",
    "get_series_list",
    "get_stories_in_series",
    "get_story_prompt",
]
