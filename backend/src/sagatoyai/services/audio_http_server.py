"""Audio HTTP Server - serves TTS audio files for Folotoy Octopus download."""

import asyncio
import logging
import os
import uuid
from pathlib import Path
from typing import Optional

import aiohttp
from aiohttp import web

logger = logging.getLogger(__name__)

AUDIO_HTTP_PORT = int(os.getenv("AUDIO_HTTP_PORT", "8082"))
AUDIO_CACHE_DIR = Path(os.getenv("AUDIO_CACHE_DIR", "/tmp/sagatoy_audio"))


class AudioHTTPServer:
    """HTTP server for serving TTS audio files to Octopus devices."""
    
    def __init__(self, port: int = AUDIO_HTTP_PORT):
        self.port = port
        self.app = web.Application()
        self.runner: Optional[web.AppRunner] = None
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup HTTP routes."""
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/audio/{audio_id}', self.serve_audio)
        self.app.router.add_post('/audio', self.upload_audio)
        self.app.router.add_get('/list', self.list_audio)
        
    async def health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({"status": "ok", "service": "audio-http"})
        
    async def serve_audio(self, request: web.Request) -> web.Response:
        """Serve audio file by ID."""
        audio_id = request.match_info['audio_id']
        audio_path = AUDIO_CACHE_DIR / f"{audio_id}.wav"
        
        if not audio_path.exists():
            return web.Response(status=404, text="Audio not found")
            
        try:
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
                
            return web.Response(
                body=audio_data,
                content_type='audio/wav',
                headers={'Content-Disposition': f'attachment; filename="{audio_id}.wav"'}
            )
        except Exception as e:
            logger.error(f"Error serving audio {audio_id}: {e}")
            return web.Response(status=500, text="Error serving audio")
            
    async def upload_audio(self, request: web.Request) -> web.Response:
        """Upload audio file, returns audio ID."""
        try:
            data = await request.read()
            if not data:
                return web.Response(status=400, text="No audio data provided")
                
            # Generate unique ID
            audio_id = str(uuid.uuid4())[:8]
            audio_path = AUDIO_CACHE_DIR / f"{audio_id}.wav"
            
            # Ensure directory exists
            AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            
            # Save file
            with open(audio_path, 'wb') as f:
                f.write(data)
                
            logger.info(f"Saved audio {audio_id} ({len(data)} bytes)")
            
            return web.json_response({
                "audio_id": audio_id,
                "url": f"http://{request.host}/audio/{audio_id}"
            })
            
        except Exception as e:
            logger.error(f"Error uploading audio: {e}")
            return web.Response(status=500, text="Error uploading audio")
            
    async def list_audio(self, request: web.Request) -> web.Response:
        """List available audio files."""
        try:
            if not AUDIO_CACHE_DIR.exists():
                return web.json_response({"files": []})
                
            files = []
            for f in AUDIO_CACHE_DIR.glob("*.wav"):
                files.append({
                    "id": f.stem,
                    "size": f.stat().st_size,
                    "created": f.stat().st_ctime
                })
                
            return web.json_response({"files": files})
            
        except Exception as e:
            logger.error(f"Error listing audio: {e}")
            return web.Response(status=500, text="Error listing audio")
            
    async def start(self):
        """Start HTTP server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        site = web.TCPSite(self.runner, '0.0.0.0', self.port)
        await site.start()
        
        logger.info(f"Audio HTTP server started on port {self.port}")
        
    async def stop(self):
        """Stop HTTP server."""
        if self.runner:
            await self.runner.cleanup()
            logger.info("Audio HTTP server stopped")


_audio_server: Optional[AudioHTTPServer] = None


async def start_audio_server() -> AudioHTTPServer:
    """Start the audio HTTP server."""
    global _audio_server
    _audio_server = AudioHTTPServer()
    await _audio_server.start()
    return _audio_server


async def stop_audio_server():
    """Stop the audio HTTP server."""
    global _audio_server
    if _audio_server:
        await _audio_server.stop()
        _audio_server = None


def get_audio_server() -> Optional[AudioHTTPServer]:
    """Get the audio server instance."""
    return _audio_server


def save_audio_file(audio_data: bytes, audio_id: str) -> Path:
    """Save audio data to cache and return path."""
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = AUDIO_CACHE_DIR / f"{audio_id}.wav"
    with open(audio_path, 'wb') as f:
        f.write(audio_data)
    return audio_path