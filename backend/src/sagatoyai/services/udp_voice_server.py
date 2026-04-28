"""UDP Voice Server - receives real-time audio stream from Folotoy Octopus."""

import asyncio
import logging
import os
import socket
from typing import Optional

logger = logging.getLogger(__name__)

UDP_PORT = int(os.getenv("UDP_VOICE_PORT", "8085"))


class UDPVoiceServer:
    """UDP server for receiving voice/audio data from Octopus devices."""
    
    def __init__(self, port: int = UDP_PORT):
        self.port = port
        self.transport: Optional[asyncio.DatagramTransport] = None
        self._running = False
        self._audio_buffers: dict[str, bytes] = {}
        
    def connection_made(self, transport):
        self.transport = transport
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        logger.info(f"UDP voice server bound to port {self.port}")
        
    def datagram_received(self, data, addr):
        """Handle incoming UDP packet.
        
        Expected format: device_id|audio_data
        """
        try:
            # Parse packet - first bytes may contain device ID
            # Format: 4 bytes device_id + audio data
            if len(data) > 4:
                device_id = data[:4].decode('utf-8', errors='ignore')
                audio_data = data[4:]
                
                # Accumulate audio for this device
                if device_id not in self._audio_buffers:
                    self._audio_buffers[device_id] = b''
                self._audio_buffers[device_id] += audio_data
                
                logger.debug(f"UDP: received {len(audio_data)} bytes from {addr}, total buffered: {len(self._audio_buffers[device_id])}")
                
        except Exception as e:
            logger.error(f"Error processing UDP packet: {e}")
            
    def error_received(self, exc):
        logger.error(f"UDP server error: {exc}")
        
    def connection_lost(self, exc):
        logger.warning(f"UDP connection lost: {exc}")
        self._running = False
        
    async def start(self):
        """Start UDP server."""
        loop = asyncio.get_event_loop()
        self._running = True
        
        self.transport, protocol = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=('0.0.0.0', self.port)
        )
        logger.info(f"UDP voice server started on port {self.port}")
        
    async def stop(self):
        """Stop UDP server."""
        self._running = False
        if self.transport:
            self.transport.close()
        logger.info("UDP voice server stopped")
        
    def get_audio(self, device_id: str) -> Optional[bytes]:
        """Get accumulated audio for a device and clear buffer."""
        audio = self._audio_buffers.get(device_id)
        if audio:
            self._audio_buffers[device_id] = b''
        return audio


_udp_server: Optional[UDPVoiceServer] = None


async def start_udp_server() -> UDPVoiceServer:
    """Start the UDP voice server."""
    global _udp_server
    _udp_server = UDPVoiceServer()
    await _udp_server.start()
    return _udp_server


async def stop_udp_server():
    """Stop the UDP voice server."""
    global _udp_server
    if _udp_server:
        await _udp_server.stop()
        _udp_server = None


def get_udp_server() -> Optional[UDPVoiceServer]:
    """Get the UDP server instance."""
    return _udp_server