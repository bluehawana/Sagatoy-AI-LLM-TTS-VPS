"""FastAPI application entry point."""

import asyncio
import logging
import os

from fastapi import FastAPI

from sagatoyai.api.errors import setup_error_handlers
from sagatoyai.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sagatoyai",
    description="AI-powered plush toy backend services",
    version="0.1.0",
)

app.include_router(router)
setup_error_handlers(app)

mqtt_task = None


async def start_mqtt_service():
    """Start MQTT service in background."""
    from sagatoyai.services.groq_service import groq_service
    from sagatoyai.services.mqtt_service import FoloToyHandler, MQTTService
    from sagatoyai.services.stt import stt_service
    from sagatoyai.services.tts import tts_service
    from sagatoyai.services.zai_llm import zai_llm_service
    from sagatoyai.services.openai_llm import openai_llm_service

    broker = os.getenv("MQTT_BROKER", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))

    mqtt = MQTTService(broker=broker, port=port)

    try:
        await mqtt.connect()
        logger.info(f"MQTT service started on {broker}:{port}")

        # Load balancer: OpenAI (fastest) → Groq → Z.ai (fallback)
        handler = FoloToyHandler(
            stt_service=stt_service,
            llm_service=openai_llm_service,
            tts_service=tts_service,
            mqtt_service=mqtt,
            fallback_llm_service=groq_service,
            third_fallback_llm_service=zai_llm_service,
        )

        mqtt.on_message("folotoy/+/audio", handler.handle_audio)
        mqtt.on_message("folotoy/+/text", handler.handle_text)
        mqtt.on_message("folotoy/+/event", handler.handle_event)
        mqtt.on_message("toy/+/audio/in", handler.handle_audio)
        mqtt.on_message("toy/+/text", handler.handle_text)

        # Debug: subscribe to everything and print all messages
        print("[DEBUG] Subscribing to # (all topics)")
        await mqtt._client.subscribe("#")
        mqtt.on_message("#", lambda t, p: print(f"[MQTT DEBUG] Received on {t}: {len(p)} bytes"))

        await mqtt.listen()

    except Exception as e:
        logger.error(f"MQTT service error: {e}")


udp_task = None
audio_http_task = None


@app.on_event("startup")
async def startup_event():
    """Start background services on startup."""
    global mqtt_task, udp_task, audio_http_task

    # Start UDP Voice Server (port 8085)
    if os.getenv("UDP_ENABLED", "true").lower() == "true":
        from sagatoyai.services.udp_voice_server import start_udp_server
        await start_udp_server()
        logger.info("UDP voice server started on port 8085")

    # Start Audio HTTP Server (port 8082)
    if os.getenv("AUDIO_HTTP_ENABLED", "true").lower() == "true":
        from sagatoyai.services.audio_http_server import start_audio_server
        await start_audio_server()
        logger.info("Audio HTTP server started on port 8082")

    # Start MQTT Service
    if os.getenv("MQTT_ENABLED", "true").lower() == "true":
        mqtt_task = asyncio.create_task(start_mqtt_service())
        logger.info("MQTT service task created")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global mqtt_task
    if mqtt_task:
        mqtt_task.cancel()
        try:
            await mqtt_task
        except asyncio.CancelledError:
            pass
        logger.info("MQTT service stopped")
