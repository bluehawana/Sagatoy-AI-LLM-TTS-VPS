"""Session management service using Redis."""

import json
from datetime import datetime, timedelta
from typing import Optional

import redis.asyncio as redis

from sagatoyai.models import Message, SessionContext

SESSION_EXPIRE_MINUTES = 30


class SessionManager:
    """Manages conversation sessions with Redis backend."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """Initialize session manager with Redis connection."""
        self.redis_url = redis_url
        self._redis: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Connect to Redis."""
        if self._redis is None:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            self._redis = None

    def _session_key(self, session_id: str) -> str:
        """Generate Redis key for session."""
        return f"session:{session_id}"

    async def get_context(self, session_id: str) -> Optional[SessionContext]:
        """Retrieve session context from Redis."""
        if not self._redis:
            await self.connect()

        data = await self._redis.get(self._session_key(session_id))
        if data is None:
            return None

        return SessionContext.model_validate_json(data)

    async def create_session(self, session_id: str, device_id: str) -> SessionContext:
        """Create a new session."""
        if not self._redis:
            await self.connect()

        now = datetime.utcnow()
        context = SessionContext(
            session_id=session_id,
            device_id=device_id,
            messages=[],
            created_at=now,
            expires_at=now + timedelta(minutes=SESSION_EXPIRE_MINUTES),
        )

        await self._redis.setex(
            self._session_key(session_id),
            SESSION_EXPIRE_MINUTES * 60,
            context.model_dump_json(),
        )

        return context

    async def update_context(
        self,
        session_id: str,
        user_input: str,
        assistant_response: str,
    ) -> Optional[SessionContext]:
        """Add messages to session context."""
        if not self._redis:
            await self.connect()

        context = await self.get_context(session_id)
        if context is None:
            return None

        now = datetime.utcnow()
        context.messages.append(
            Message(role="user", content=user_input, timestamp=now))
        context.messages.append(
            Message(role="assistant", content=assistant_response, timestamp=now)
        )

        await self._redis.setex(
            self._session_key(session_id),
            SESSION_EXPIRE_MINUTES * 60,
            context.model_dump_json(),
        )

        return context

    async def set_story_context(
        self, session_id: str, story_content: str
    ) -> Optional[SessionContext]:
        """Store current story in session for continuation."""
        if not self._redis:
            await self.connect()

        context = await self.get_context(session_id)
        if context is None:
            return None

        context.current_story = story_content

        await self._redis.setex(
            self._session_key(session_id),
            SESSION_EXPIRE_MINUTES * 60,
            context.model_dump_json(),
        )

        return context

    async def clear_session(self, session_id: str) -> None:
        """Delete a session."""
        if not self._redis:
            await self.connect()

        await self._redis.delete(self._session_key(session_id))


# Global session manager instance
session_manager = SessionManager()
