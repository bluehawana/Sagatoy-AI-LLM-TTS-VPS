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
    ):
        self.stt = stt_service
        self.llm = llm_service
        self.tts = tts_service
        self.mqtt = mqtt_service
        self.sessions: dict[str, dict] = {}

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

            response = await self.llm.generate(
                transcript.text,
                session_id=device_id,
                language=transcript.language,
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
                language = data.get("language", "sv")
            except json.JSONDecodeError:
                text = payload.decode()
                language = "sv"

            logger.info(f"Received text from {device_id}: {text}")
            print(f"[DEBUG] Processing text: {text}, lang: {language}")

            response, _ = await self.llm.generate_conversation_response(
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
