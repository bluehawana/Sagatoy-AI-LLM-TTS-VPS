"""MQTT service for FoloToy protocol integration."""

import asyncio
import base64
import json
import logging
import os
from dataclasses import dataclass
from typing import Callable, Optional

import aiomqtt

logger = logging.getLogger(__name__)


@dataclass
class ToyMessage:
    device_id: str
    session_id: str
    audio_data: Optional[bytes] = None
    text: Optional[str] = None
    language: str = "sv"


class MQTTService:
    """MQTT service for handling FoloToy toy communication."""

    def __init__(
        self,
        broker: str = "localhost",
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self._client: Optional[aiomqtt.Client] = None
        self._running = False
        self._message_handlers: dict[str, Callable] = {}

    async def connect(self):
        """Connect to MQTT broker."""
        try:
            self._client = aiomqtt.Client(
                hostname=self.broker,
                port=self.port,
                username=self.username,
                password=self.password,
            )
            await self._client.__aenter__()
            self._running = True
            logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    async def disconnect(self):
        """Disconnect from MQTT broker."""
        if self._client:
            await self._client.__aexit__(None, None, None)
            self._running = False
            logger.info("Disconnected from MQTT broker")

    async def subscribe_to_toy(self, device_id: str):
        """Subscribe to all topics for a specific toy."""
        topics = [
            f"folotoy/{device_id}/audio",
            f"folotoy/{device_id}/text",
            f"folotoy/{device_id}/event",
            f"toy/{device_id}/audio/in",
            f"toy/{device_id}/text",
        ]
        for topic in topics:
            await self._client.subscribe(topic)
            logger.info(f"Subscribed to: {topic}")

    async def publish_audio(self, device_id: str, audio_data: bytes):
        """Publish audio to toy."""
        topic = f"folotoy/{device_id}/audio/out"
        await self._client.publish(topic, audio_data)
        logger.debug(f"Published audio to {device_id}")

    async def publish_text(self, device_id: str, text: str, language: str = "sv"):
        """Publish text message to toy."""
        topic = f"folotoy/{device_id}/text"
        payload = json.dumps({"text": text, "language": language})
        await self._client.publish(topic, payload)
        logger.debug(f"Published text to {device_id}")

    async def publish_tts_audio(self, device_id: str, audio_data: bytes):
        """Publish TTS audio response to toy."""
        topic = f"toy/{device_id}/audio/out"
        await self._client.publish(topic, audio_data)
        logger.debug(f"Published TTS audio to {device_id}")

    def on_message(self, topic_pattern: str, handler: Callable):
        """Register a message handler for a topic pattern."""
        self._message_handlers[topic_pattern] = handler

    async def listen(self):
        """Listen for incoming messages."""
        if not self._client:
            raise RuntimeError("Not connected to MQTT broker")

        async for message in self._client.messages:
            try:
                topic = str(message.topic)
                payload = message.payload

                for pattern, handler in self._message_handlers.items():
                    if self._match_topic(pattern, topic):
                        await handler(topic, payload)
                        break
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    def _match_topic(self, pattern: str, topic: str) -> bool:
        """Check if topic matches pattern with wildcards."""
        pattern_parts = pattern.split("/")
        topic_parts = topic.split("/")

        if len(pattern_parts) != len(topic_parts):
            return False

        for p, t in zip(pattern_parts, topic_parts):
            if p == "+":
                continue
            if p == "#":
                return True
            if p != t:
                return False
        return True


class FoloToyHandler:
    """Handler for FoloToy protocol messages."""

    def __init__(
        self,
        stt_service,
        llm_service,
        tts_service,
        mqtt_service: MQTTService,
        fallback_llm_service=None,
        third_fallback_llm_service=None,
    ):
        self.stt = stt_service
        self.llm = llm_service
        self.fallback_llm = fallback_llm_service
        self.third_fallback_llm = third_fallback_llm_service
        self.tts = tts_service
        self.mqtt = mqtt_service
        self.sessions: dict[str, dict] = {}

    def _handle_direct(self, text: str, language: str = "en") -> Optional[str]:
        """Handle math/date directly without LLM."""
        import re
        from datetime import datetime
        
        text_lower = text.lower()
        
        # Math patterns
        math_keywords = ["plus", "minus", "times", "multiplied", "divided", "gånger", "delat", "pluss", "miinus"]
        if any(k in text_lower for k in math_keywords):
            patterns = [
                r'(\d+)\s*(?:plus|\+|times|\*|gånger)\s*(\d+)',
                r'(\d+)\s*(?:minus|-)\s*(\d+)',
                r'(\d+)\s*(?:/|divided|delat)\s*(\d+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    a, b = int(match.group(1)), int(match.group(2))
                    if "+" in text_lower or "plus" in text_lower or "pluss" in text_lower:
                        return f"It's {a + b}! {a} plus {b} equals {a + b}. Great job!"
                    elif "minus" in text_lower or "miinus" in text_lower:
                        return f"It's {a - b}! {a} minus {b} equals {a - b}. Great job!"
                    elif "times" in text_lower or "gånger" in text_lower or "*" in text_lower:
                        return f"It's {a * b}! {a} times {b} equals {a * b}. Great job!"
                    elif "/" in text_lower or "divided" in text_lower or "delat" in text_lower:
                        if b != 0:
                            return f"It's {round(a / b, 2)}! {a} divided by {b} equals {round(a / b, 2)}. Great job!"
        
        # Date/Day patterns
        day_keywords = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "dag", "day", "vilken", "datum", "dato", "päivä"]
        date_keywords = ["what date", "date today", "today", "what day", "vilket datum", "hvilken dag", "mikä päivä"]
        
        now = datetime.now()
        if any(d in text_lower for d in day_keywords):
            day_name_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return f"Today is {day_name_en[now.weekday()]}! Can you say it with me?"
        
        if any(d in text_lower for d in date_keywords):
            return f"Today is {now.strftime('%B %d, %Y')}!"
        
        return None

    async def _call_llm(self, text, language="en", session_id=None):
        """Call LLM with fallback chain: primary → fallback → third_fallback."""
        # Try direct handlers first (instant, no API call)
        from sagatoyai.models import Intent
        direct_result = self._handle_direct(text, language)
        if direct_result:
            print(f"[DEBUG] Direct handler: {direct_result[:50]}...")
            return direct_result, Intent.GENERAL
        
        # Call LLM with fallback chain
        services = [self.llm]
        if self.fallback_llm:
            services.append(self.fallback_llm)
        if self.third_fallback_llm:
            services.append(self.third_fallback_llm)

        last_error = None
        for i, service in enumerate(services):
            try:
                if session_id:
                    result = await service.generate(text, session_id=session_id, language=language)
                    return result, Intent.GENERAL
                else:
                    result, intent = await service.generate_conversation_response(text, language=language)
                    return result, intent
            except Exception as e:
                last_error = e
                logger.warning(f"LLM #{i+1} failed ({type(service).__name__}): {e}")
                continue

        raise last_error if last_error else RuntimeError("All LLM services failed")

    def _detect_language(self, text: str) -> str:
        """Auto-detect language from text input."""
        text_lower = text.lower()
        
        # Check for Chinese characters
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return "zh"
        
        # Check for Nordic language patterns
        swedish_words = ['hej', 'hur', 'mår', 'är', 'det', 'dag', 'vad', 'heter', 'berätta', 'saga', 'gånger', 'delat']
        danish_words = ['hej', 'hvordan', 'har', 'det', 'dag', 'hvad', 'hedder', 'fortæl', 'historie', 'pluss', 'minus']
        norwegian_words = ['hei', 'hvordan', 'har', 'det', 'dag', 'hva', 'heter', 'fortell', 'historie', 'pluss', 'minus']
        finnish_words = ['hei', 'miten', ' voit', 'päivä', 'mikä', 'nimi', 'kerro', 'tarina', 'miinus', 'plus']
        
        swedish_count = sum(1 for w in swedish_words if w in text_lower)
        danish_count = sum(1 for w in danish_words if w in text_lower)
        norwegian_count = sum(1 for w in norwegian_words if w in text_lower)
        finnish_count = sum(1 for w in finnish_words if w in text_lower)
        
        counts = {'sv': swedish_count, 'da': danish_count, 'no': norwegian_count, 'fi': finnish_count}
        detected = max(counts, key=counts.get)
        
        if counts[detected] > 0:
            return detected
        
        # Default to English
        return "en"

    async def handle_audio(self, topic: str, payload: bytes):
        """Handle incoming audio from toy."""
        try:
            parts = topic.split("/")
            device_id = parts[1] if len(parts) > 1 else "unknown"

            audio_data = payload
            if payload.startswith(b"{"):
                try:
                    data = json.loads(payload)
                    if "audio" in data:
                        audio_data = base64.b64decode(data["audio"])
                    elif "audio_data" in data:
                        audio_data = base64.b64decode(data["audio_data"])
                except json.JSONDecodeError:
                    pass

            logger.info(f"Received audio from {device_id}, size: {len(audio_data)}")

            transcript = await self.stt.transcribe(audio_data)
            logger.info(f"Transcript: {transcript.text}")

            response = await self._call_llm(
                transcript.text,
                language=transcript.language,
                session_id=device_id,
            )
            logger.info(f"LLM response: {response}")

            audio_response = await self.tts.synthesize_to_bytes(
                response, language=transcript.language
            )

            await self.mqtt.publish_tts_audio(device_id, audio_response)

        except Exception as e:
            logger.error(f"Error handling audio: {e}")

    async def handle_text(self, topic: str, payload: bytes):
        """Handle incoming text from toy."""
        try:
            parts = topic.split("/")
            device_id = parts[1] if len(parts) > 1 else "unknown"

            try:
                data = json.loads(payload)
                text = data.get("text", payload.decode())
                language = data.get("language", "auto")
            except json.JSONDecodeError:
                text = payload.decode()
                language = "auto"

            # Auto-detect language if not specified
            if language == "auto" or not language:
                language = self._detect_language(text)
                print(f"[DEBUG] Auto-detected language: {language}")

            logger.info(f"Received text from {device_id}: {text}")
            print(f"[DEBUG] Processing text: {text}, lang: {language}")

            response, _ = await self._call_llm(
                text,
                language=language,
            )
            print(f"[DEBUG] LLM response: {response[:100]}...")

            audio_response = await self.tts.synthesize_to_bytes(response, language=language)
            print(f"[DEBUG] TTS audio generated: {len(audio_response)} bytes")

            await self.mqtt.publish_tts_audio(device_id, audio_response)
            print(f"[DEBUG] Published TTS audio to {device_id}")

        except Exception as e:
            print(f"[ERROR] Error handling text: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f"Error handling text: {e}")

    async def handle_event(self, topic: str, payload: bytes):
        """Handle toy events (connect, disconnect, button press)."""
        try:
            parts = topic.split("/")
            device_id = parts[1] if len(parts) > 1 else "unknown"

            try:
                event = json.loads(payload)
            except json.JSONDecodeError:
                event = {"type": "unknown", "data": payload.decode()}

            event_type = event.get("type", "unknown")
            logger.info(f"Event from {device_id}: {event_type}")

            if event_type == "connect":
                await self.mqtt.subscribe_to_toy(device_id)
            elif event_type == "button_press":
                pass

        except Exception as e:
            logger.error(f"Error handling event: {e}")


mqtt_service = MQTTService(
    broker=os.getenv("MQTT_BROKER", "localhost"),
    port=int(os.getenv("MQTT_PORT", "1883")),
)
