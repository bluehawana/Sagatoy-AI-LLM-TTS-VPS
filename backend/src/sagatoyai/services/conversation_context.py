"""Conversation context manager for maintaining chat history.

Inspired by XiaoGPT's conversation management approach.
Maintains conversation history for more natural, contextual responses.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Single turn in a conversation."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    intent: Optional[str] = None


@dataclass
class ConversationContext:
    """Manages conversation context for a session."""

    session_id: str
    device_id: str
    history: list[ConversationTurn] = field(default_factory=list)
    max_turns: int = 10  # Keep last N turns for context
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    # Child profile (optional)
    child_name: Optional[str] = None
    child_age: Optional[int] = None
    preferred_language: str = "sv"

    # Current activity state
    current_story: Optional[str] = None
    current_topic: Optional[str] = None

    def add_turn(self, role: str, content: str, intent: Optional[str] = None) -> None:
        """Add a conversation turn to history."""
        turn = ConversationTurn(
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            intent=intent,
        )
        self.history.append(turn)
        self.last_activity = datetime.utcnow()

        # Trim history if too long
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def add_user_message(self, content: str, intent: Optional[str] = None) -> None:
        """Add user message to history."""
        self.add_turn("user", content, intent)

    def add_assistant_message(self, content: str) -> None:
        """Add assistant response to history."""
        self.add_turn("assistant", content)

    def get_context_for_llm(self, max_turns: Optional[int] = None) -> list[dict]:
        """Get conversation history formatted for LLM.

        Returns:
            List of message dicts with 'role' and 'content' keys
        """
        turns = max_turns or self.max_turns
        # *2 for user+assistant pairs
        recent_history = self.history[-turns * 2:]

        return [
            {"role": turn.role, "content": turn.content}
            for turn in recent_history
        ]

    def get_summary(self) -> str:
        """Get a brief summary of the conversation for context."""
        if not self.history:
            return "New conversation"

        topics = set()
        for turn in self.history:
            if turn.intent:
                topics.add(turn.intent)

        return f"Conversation with {len(self.history)} turns. Topics: {', '.join(topics) or 'general'}"

    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if conversation has expired due to inactivity."""
        expiry_time = self.last_activity + timedelta(minutes=timeout_minutes)
        return datetime.utcnow() > expiry_time

    def clear(self) -> None:
        """Clear conversation history."""
        self.history = []
        self.current_story = None
        self.current_topic = None


class ConversationContextManager:
    """Manages multiple conversation contexts.

    In-memory storage for development. Use Redis in production.
    """

    def __init__(self, max_contexts: int = 1000):
        """Initialize context manager.

        Args:
            max_contexts: Maximum number of contexts to keep in memory
        """
        self._contexts: dict[str, ConversationContext] = {}
        self.max_contexts = max_contexts

    def get_or_create(
        self,
        session_id: str,
        device_id: str,
        language: str = "sv",
    ) -> ConversationContext:
        """Get existing context or create new one.

        Args:
            session_id: Unique session identifier
            device_id: Device identifier
            language: Preferred language

        Returns:
            ConversationContext for the session
        """
        if session_id in self._contexts:
            context = self._contexts[session_id]
            # Check if expired
            if context.is_expired():
                logger.info(
                    f"Session {session_id} expired, creating new context")
                context = self._create_new_context(
                    session_id, device_id, language)
            return context

        return self._create_new_context(session_id, device_id, language)

    def _create_new_context(
        self,
        session_id: str,
        device_id: str,
        language: str,
    ) -> ConversationContext:
        """Create a new conversation context."""
        # Clean up old contexts if at limit
        if len(self._contexts) >= self.max_contexts:
            self._cleanup_old_contexts()

        context = ConversationContext(
            session_id=session_id,
            device_id=device_id,
            preferred_language=language,
        )
        self._contexts[session_id] = context
        logger.info(
            f"Created new conversation context for session {session_id}")
        return context

    def _cleanup_old_contexts(self) -> None:
        """Remove expired and oldest contexts."""
        now = datetime.utcnow()

        # Remove expired contexts
        expired = [
            sid for sid, ctx in self._contexts.items()
            if ctx.is_expired()
        ]
        for sid in expired:
            del self._contexts[sid]

        # If still over limit, remove oldest
        if len(self._contexts) >= self.max_contexts:
            sorted_contexts = sorted(
                self._contexts.items(),
                key=lambda x: x[1].last_activity
            )
            # Remove oldest 10%
            to_remove = len(sorted_contexts) // 10
            for sid, _ in sorted_contexts[:to_remove]:
                del self._contexts[sid]

        logger.info(f"Cleaned up contexts, {len(self._contexts)} remaining")

    def get(self, session_id: str) -> Optional[ConversationContext]:
        """Get context by session ID."""
        return self._contexts.get(session_id)

    def delete(self, session_id: str) -> None:
        """Delete a conversation context."""
        if session_id in self._contexts:
            del self._contexts[session_id]
            logger.info(
                f"Deleted conversation context for session {session_id}")

    def get_active_count(self) -> int:
        """Get count of active (non-expired) contexts."""
        return sum(1 for ctx in self._contexts.values() if not ctx.is_expired())


# Global conversation context manager
conversation_manager = ConversationContextManager()
