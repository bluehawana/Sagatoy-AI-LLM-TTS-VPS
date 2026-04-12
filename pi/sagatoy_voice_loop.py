#!/usr/bin/env python3
"""
SagaToy Main Voice Loop — runs on Raspberry Pi 4.

Flow per conversation turn:
  1. Wait for GPIO button press (right-hand button, GPIO 17)
  2. Vibrate briefly  → confirms button received
  3. Record audio from USB mic while button held (release = stop)
  4. Auto-detect language + transcribe via whisper.cpp
  5. If WiFi: z.ai GLM-4 Flash  |  If offline: Ollama phi3:mini
  6. Check for local content triggers (story / song)
  7. TTS via Piper (sv/da/no/fi/en) or edge-tts (zh)
  8. Play audio via aplay → PAM8403 amp → speaker
  9. Vibrate briefly → signals response complete
 10. Back to step 1
"""

import asyncio
import audioop
import logging
import os
import subprocess
import sys
import time
import wave
from pathlib import Path
from typing import Optional

import httpx
import pyaudio
import RPi.GPIO as GPIO
import yaml

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/home/pi/sagatoy/logs/voice_loop.log"),
    ],
)
log = logging.getLogger("sagatoy")

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
CONFIG_PATH = Path(__file__).parent / "config.yaml"
LOCAL_CONFIG_PATH = Path(__file__).parent / "config.local.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
    if LOCAL_CONFIG_PATH.exists():
        with open(LOCAL_CONFIG_PATH) as f:
            local = yaml.safe_load(f) or {}
        cfg = _deep_merge(cfg, local)
    return cfg


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


# ---------------------------------------------------------------------------
# GPIO helpers
# ---------------------------------------------------------------------------
class GPIOController:
    def __init__(self, cfg: dict):
        self.button_pin = cfg["gpio"]["button_pin"]
        self.vibration_pin = cfg["gpio"]["vibration_pin"]
        self.vibrate_press_ms = cfg["gpio"]["vibrate_on_press_ms"]
        self.vibrate_done_ms = cfg["gpio"]["vibrate_on_done_ms"]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.vibration_pin, GPIO.OUT)
        GPIO.output(self.vibration_pin, GPIO.LOW)
        log.info("GPIO initialised (button=%d, vibration=%d)",
                 self.button_pin, self.vibration_pin)

    def is_button_pressed(self) -> bool:
        return GPIO.input(self.button_pin) == GPIO.LOW

    def vibrate(self, duration_ms: int):
        GPIO.output(self.vibration_pin, GPIO.HIGH)
        time.sleep(duration_ms / 1000)
        GPIO.output(self.vibration_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


# ---------------------------------------------------------------------------
# Audio recording
# ---------------------------------------------------------------------------
class AudioRecorder:
    def __init__(self, cfg: dict, gpio: GPIOController):
        self.sample_rate = cfg["audio"]["sample_rate"]
        self.channels = cfg["audio"]["channels"]
        self.chunk = cfg["audio"]["chunk_size"]
        self.silence_thresh = cfg["audio"]["silence_threshold"]
        self.silence_dur = cfg["audio"]["silence_duration_s"]
        self.max_dur = cfg["audio"]["max_record_s"]
        self.gpio = gpio
        self._pa = pyaudio.PyAudio()

    def record_while_held(self) -> bytes:
        """Record audio while button is held; stop on release or silence."""
        stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        frames = []
        silent_chunks = 0
        silence_limit = int(self.silence_dur * self.sample_rate / self.chunk)
        max_chunks = int(self.max_dur * self.sample_rate / self.chunk)

        log.info("Recording started")
        try:
            for _ in range(max_chunks):
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
                rms = audioop.rms(data, 2)
                if not self.gpio.is_button_pressed():
                    # Button released — give a short grace period for trailing audio
                    silent_chunks += 1
                    if silent_chunks >= 3:
                        break
                elif rms < self.silence_thresh:
                    silent_chunks += 1
                    if silent_chunks >= silence_limit:
                        break
                else:
                    silent_chunks = 0
        finally:
            stream.stop_stream()
            stream.close()

        log.info("Recording stopped (%d chunks, %.1fs)",
                 len(frames), len(frames) * self.chunk / self.sample_rate)
        return b"".join(frames)

    def save_wav(self, audio_bytes: bytes, path: str):
        with wave.open(path, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_bytes)

    def cleanup(self):
        self._pa.terminate()


# ---------------------------------------------------------------------------
# STT — whisper.cpp via subprocess
# ---------------------------------------------------------------------------
class WhisperSTT:
    def __init__(self, cfg: dict):
        self.model_path = cfg["stt"]["model_path"]
        self.tmp_wav = "/tmp/sagatoy_input.wav"

    def transcribe(self, audio_bytes: bytes, recorder: AudioRecorder) -> tuple[str, str]:
        """Returns (text, detected_language)."""
        recorder.save_wav(audio_bytes, self.tmp_wav)

        cmd = [
            "whisper-cpp",        # Compiled whisper.cpp binary
            "-m", self.model_path,
            "-f", self.tmp_wav,
            "-l", "auto",         # Auto-detect language
            "--output-txt",
            "--no-timestamps",
        ]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )
            txt_path = self.tmp_wav + ".txt"
            if os.path.exists(txt_path):
                text = Path(txt_path).read_text().strip()
                os.unlink(txt_path)
            else:
                text = result.stdout.strip()

            # Parse detected language from stderr e.g. "auto-detected language: sv"
            lang = "sv"
            for line in result.stderr.splitlines():
                if "auto-detected language" in line.lower():
                    lang = line.split(":")[-1].strip()[:2].lower()
                    break

            log.info("STT: '%s' [lang=%s]", text[:80], lang)
            return text, lang

        except subprocess.TimeoutExpired:
            log.error("Whisper timed out")
            return "", "sv"
        except Exception as e:
            log.error("Whisper error: %s", e)
            return "", "sv"


# ---------------------------------------------------------------------------
# WiFi check
# ---------------------------------------------------------------------------
def has_wifi(cfg: dict) -> bool:
    try:
        r = httpx.get(cfg["wifi"]["check_url"],
                      timeout=cfg["wifi"]["check_timeout_s"])
        return r.status_code < 500
    except Exception:
        return False


# ---------------------------------------------------------------------------
# LLM — z.ai (cloud) or Ollama (offline)
# ---------------------------------------------------------------------------
class LLMService:
    def __init__(self, cfg: dict):
        self.cfg = cfg["llm"]
        self.device = cfg["device"]

    def _system_prompt(self, language: str) -> str:
        lang_names = {
            "sv": "Swedish", "da": "Danish", "no": "Norwegian",
            "fi": "Finnish", "en": "English", "zh": "Chinese (Mandarin)",
        }
        return self.cfg["system_prompt"].format(
            toy_name=self.device["name"],
            child_name=self.device.get("child_name") or "little one",
            child_age=self.device.get("child_age", 5),
            language=lang_names.get(language, language),
        )

    async def generate(self, text: str, language: str, use_wifi: bool) -> str:
        if use_wifi:
            return await self._cloud(text, language)
        return await self._offline(text, language)

    async def _cloud(self, text: str, language: str) -> str:
        """z.ai GLM-4 Flash — OpenAI-compatible API."""
        headers = {
            "Authorization": f"Bearer {self.cfg['cloud_api_key']}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.cfg["cloud_model"],
            "messages": [
                {"role": "system", "content": self._system_prompt(language)},
                {"role": "user", "content": text},
            ],
            "max_tokens": 150,
            "temperature": 0.8,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                f"{self.cfg['cloud_base_url']}chat/completions",
                headers=headers,
                json=payload,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()

    async def _offline(self, text: str, language: str) -> str:
        """Ollama phi3:mini — runs locally on Pi 4."""
        payload = {
            "model": self.cfg["offline_model"],
            "messages": [
                {"role": "system", "content": self._system_prompt(language)},
                {"role": "user", "content": text},
            ],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self.cfg['offline_url']}/api/chat",
                json=payload,
            )
            r.raise_for_status()
            return r.json()["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Content triggers (local stories / songs)
# ---------------------------------------------------------------------------
class ContentLibrary:
    def __init__(self, cfg: dict):
        self.base = Path(cfg["content"]["base_path"])
        self.story_triggers = cfg["content"]["story_triggers"]
        self.song_triggers = cfg["content"]["song_triggers"]

    def detect(self, text: str, language: str) -> Optional[str]:
        """Return file path if local content should be played, else None."""
        t = text.lower()
        if any(trigger in t for trigger in self.story_triggers.get(language, [])):
            return self._pick(self.base / "stories" / language)
        if any(trigger in t for trigger in self.song_triggers.get(language, [])):
            return self._pick(self.base / "songs" / language)
        return None

    def _pick(self, folder: Path) -> Optional[str]:
        if not folder.exists():
            return None
        files = list(folder.glob("*.mp3")) + list(folder.glob("*.wav"))
        if not files:
            return None
        import random
        return str(random.choice(files))


# ---------------------------------------------------------------------------
# TTS — Piper (local) or edge-tts (Chinese / fallback)
# ---------------------------------------------------------------------------
class TTSService:
    def __init__(self, cfg: dict):
        self.cfg = cfg["tts"]
        self.tmp_out = "/tmp/sagatoy_tts.wav"

    async def synthesize_and_play(self, text: str, language: str):
        voices = self.cfg["voices"]
        voice_val = voices.get(language, "edge")

        if voice_val == "edge" or self.cfg["engine"] == "edge":
            await self._edge(text, language)
        else:
            self._piper(text, voice_val)

    def _piper(self, text: str, model_path: str):
        cmd = [
            "piper",
            "--model", model_path,
            "--output_file", self.tmp_out,
        ]
        proc = subprocess.run(
            cmd, input=text.encode(), capture_output=True, timeout=15
        )
        if proc.returncode != 0:
            log.error("Piper failed: %s", proc.stderr.decode())
            return
        self._play(self.tmp_out)

    async def _edge(self, text: str, language: str):
        import edge_tts
        voice = self.cfg["edge_voices"].get(language, "en-GB-SoniaNeural")
        rate = self.cfg.get("speech_rate", "-10%")
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(self.tmp_out)
        self._play(self.tmp_out)

    def _play(self, path: str):
        subprocess.run(["aplay", path], capture_output=True)


# ---------------------------------------------------------------------------
# Profile sync from VPS
# ---------------------------------------------------------------------------
async def sync_profile(cfg: dict) -> dict:
    if not cfg["parent_pairing"]["pull_on_boot"]:
        return cfg
    device_id = cfg["device"]["id"]
    url = f"{cfg['parent_pairing']['base_url']}/api/profile/{device_id}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url)
            if r.status_code == 200:
                profile = r.json()
                cfg["device"].update(profile)
                log.info("Profile synced: %s", profile)
    except Exception as e:
        log.warning("Profile sync failed (using defaults): %s", e)
    return cfg


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
async def main():
    log.info("SagaToy starting up...")
    cfg = load_config()

    # Sync parent profile on boot
    cfg = await sync_profile(cfg)

    gpio = GPIOController(cfg)
    recorder = AudioRecorder(cfg, gpio)
    stt = WhisperSTT(cfg)
    llm = LLMService(cfg)
    content = ContentLibrary(cfg)
    tts = TTSService(cfg)

    # Startup vibrate — toy is ready
    gpio.vibrate(200)
    time.sleep(0.1)
    gpio.vibrate(200)
    log.info("SagaToy ready. Waiting for button press on GPIO %d...",
             cfg["gpio"]["button_pin"])

    try:
        while True:
            # ---- Step 1: Wait for button press ----
            if not gpio.is_button_pressed():
                time.sleep(0.05)
                continue

            t_start = time.time()

            # ---- Step 2: Vibrate to confirm button press ----
            gpio.vibrate(cfg["gpio"]["vibrate_on_press_ms"])

            # ---- Step 3: Record audio ----
            audio = recorder.record_while_held()
            if len(audio) < 3200:   # < 0.1s of audio — ignore
                log.info("Too short, ignoring")
                continue

            # ---- Step 4: STT ----
            text, language = stt.transcribe(audio, recorder)
            if not text:
                log.warning("Empty transcription, skipping")
                continue

            # ---- Step 5: Check local content triggers ----
            local_file = content.detect(text, language)
            if local_file:
                log.info("Playing local content: %s", local_file)
                subprocess.Popen(["aplay", local_file])
                gpio.vibrate(cfg["gpio"]["vibrate_on_done_ms"])
                continue

            # ---- Step 6: LLM ----
            wifi = has_wifi(cfg)
            log.info("WiFi: %s | Language: %s | Input: %s", wifi, language, text[:60])
            try:
                response = await llm.generate(text, language, wifi)
            except Exception as e:
                log.error("LLM error: %s", e)
                response = {
                    "sv": "Förlåt, jag förstod inte. Kan du fråga igen?",
                    "da": "Undskyld, jeg forstod ikke. Kan du spørge igen?",
                    "no": "Beklager, jeg forsto ikke. Kan du spørre igjen?",
                    "fi": "Anteeksi, en ymmärtänyt. Voisitko kysyä uudelleen?",
                    "en": "Sorry, I didn't understand. Can you ask again?",
                    "zh": "对不起，我没听懂，请再说一次。",
                }.get(language, "Sorry, please try again!")

            t_llm = time.time()
            log.info("LLM response (%.1fs): %s", t_llm - t_start, response[:80])

            # ---- Step 7-8: TTS + play ----
            await tts.synthesize_and_play(response, language)

            # ---- Step 9: Vibrate — response complete ----
            gpio.vibrate(cfg["gpio"]["vibrate_on_done_ms"])

            t_total = time.time() - t_start
            log.info("Turn complete in %.1fs", t_total)

    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        recorder.cleanup()
        gpio.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
