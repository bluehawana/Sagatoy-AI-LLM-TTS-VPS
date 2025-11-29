# 🆕 New Features Added - Inspired by XiaoGPT

## Overview

Three new features have been added to ToToyAI backend, inspired by Yihong's XiaoGPT project:

1. **Conversation Context Manager** - Maintains chat history for natural conversations
2. **LLM Fallback Service** - Automatic failover between providers
3. **Streaming TTS** - Faster perceived response time

---

## 1️⃣ Conversation Context Manager

**File:** `backend/src/totoyai/services/conversation_context.py`

### What it does:

- Maintains conversation history per session
- Provides context to LLM for more natural responses
- Tracks child profile (name, age, language)
- Auto-expires inactive sessions

### Usage:

```python
from totoyai.services import conversation_manager

# Get or create context for a session
context = conversation_manager.get_or_create(
    session_id="session-123",
    device_id="device-456",
    language="sv",
)

# Add conversation turns
context.add_user_message("Hej! Vad heter du?", intent="general")
context.add_assistant_message("Hej! Jag heter Saga!")

# Get context for LLM (last N turns)
llm_context = context.get_context_for_llm(max_turns=5)
# Returns: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
```

### Benefits:

- More natural conversations (remembers context)
- Child can refer to previous topics
- Better story continuation
- Session management built-in

---

## 2️⃣ LLM Fallback Service

**File:** `backend/src/totoyai/services/llm_fallback.py`

### What it does:

- Tries primary LLM (Groq - fastest)
- Falls back to secondary (Gemini) if primary fails
- Tracks provider health
- Temporarily skips unhealthy providers

### Usage:

```python
from totoyai.services import llm_fallback_service

# Generate response with automatic fallback
result = await llm_fallback_service.generate_response(
    user_input="Berätta om dinosaurier!",
    language="sv",
    context=llm_context,  # Optional conversation context
)

print(result.text)           # Response text
print(result.provider)       # Which LLM was used (groq/gemini)
print(result.latency_ms)     # Response time
print(result.fallback_used)  # True if primary failed

# Check provider status
status = llm_fallback_service.get_provider_status()
# Returns: {"groq": {"failures": 0, "healthy": True}, ...}
```

### Benefits:

- Higher availability (if one LLM is down, use another)
- Automatic recovery
- Latency tracking
- Graceful degradation

---

## 3️⃣ Streaming TTS

**File:** `backend/src/totoyai/services/streaming_tts.py`

### What it does:

- Streams audio chunks as they're generated
- Splits text into sentences for faster playback
- Can integrate with LLM streaming for minimal latency

### Usage:

```python
from totoyai.services import streaming_tts_service

# Stream audio chunks
async for chunk in streaming_tts_service.synthesize_streaming(
    text="Hej! Jag är Saga.",
    language="sv",
):
    # Send chunk to speaker
    play_audio_chunk(chunk)

# Stream sentence by sentence (with text)
async for sentence, audio in streaming_tts_service.synthesize_sentences_streaming(
    text="Hej! Jag är Saga. Vill du höra en saga?",
    language="sv",
):
    print(f"Playing: {sentence}")
    play_audio(audio)

# Non-streaming (for compatibility)
audio_bytes = await streaming_tts_service.synthesize_to_bytes(text, "sv")
```

### Benefits:

- Faster perceived response time
- Start playing audio before full response
- Better user experience for children
- Sentence-by-sentence playback option

---

## 📊 Latency Comparison

### Before (Traditional):

```
User speaks → STT (1s) → LLM (2s) → TTS (1s) → Play
Total: ~4 seconds before audio starts
```

### After (Streaming):

```
User speaks → STT (1s) → LLM first sentence (0.5s) → TTS stream → Play
Total: ~1.5 seconds to first audio!
```

---

## 🧪 Testing

Run the test suite:

```bash
cd backend
python test_new_features.py
```

Tests:

1. Conversation context creation and management
2. LLM fallback with multiple providers
3. Streaming TTS audio generation
4. Full pipeline integration

---

## 📁 New Files

```
backend/src/totoyai/services/
├── conversation_context.py   # NEW: Conversation history
├── llm_fallback.py          # NEW: Multi-LLM with fallback
├── streaming_tts.py         # NEW: Streaming audio
└── __init__.py              # Updated exports

backend/
└── test_new_features.py     # NEW: Test suite
```

---

## 🔗 Integration Example

Full pipeline with all new features:

```python
from totoyai.services import (
    conversation_manager,
    llm_fallback_service,
    streaming_tts_service,
)

async def handle_conversation(session_id: str, device_id: str, user_input: str):
    # 1. Get conversation context
    context = conversation_manager.get_or_create(session_id, device_id, "sv")
    context.add_user_message(user_input)

    # 2. Generate response with fallback
    llm_context = context.get_context_for_llm()
    result = await llm_fallback_service.generate_response(
        user_input=user_input,
        language="sv",
        context=llm_context,
    )

    # 3. Add response to context
    context.add_assistant_message(result.text)

    # 4. Stream TTS audio
    async for chunk in streaming_tts_service.synthesize_streaming(
        result.text, "sv"
    ):
        yield chunk  # Send to device
```

---

## 🎯 Next Steps

1. **Integrate with API routes** - Add new endpoints using these services
2. **Hardware integration** - Use streaming TTS with ESP32
3. **Add more LLM providers** - Claude, local Ollama, etc.
4. **Persistent context** - Store in Redis for production

---

## 🙏 Credits

Inspired by [XiaoGPT](https://github.com/yihong0618/xiaogpt) by Yihong.

Key patterns adopted:

- Multi-LLM architecture
- Streaming response handling
- Conversation context management
- Graceful fallback mechanisms
