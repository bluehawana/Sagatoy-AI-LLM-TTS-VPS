# 🔍 XiaoGPT Analysis - Inspiration from Yihong

## Project Overview

**Repository:** https://github.com/yihong0618/xiaogpt
**Author:** Yihong (yihong0618) - Well-known Chinese open source developer
**Stars:** 5k+ (very popular!)
**License:** MIT ✅ (Safe to learn from!)

---

## 💡 What XiaoGPT Does

XiaoGPT hacks Xiaomi's XiaoAI smart speakers to use custom LLMs instead of Xiaomi's built-in AI:

```
Original Flow:
XiaoAI Speaker → Xiaomi Cloud → Xiaomi AI → Response

XiaoGPT Flow:
XiaoAI Speaker → Xiaomi Cloud → [Intercepted] → ChatGPT/Custom LLM → Response
```

### Key Innovation:

- **No hardware modification** - Pure software hack
- Uses Xiaomi's MiService API to intercept conversations
- Replaces responses with custom LLM output
- Works with existing XiaoAI speakers

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   XiaoAI        │     │   XiaoGPT       │     │   LLM APIs      │
│   Speaker       │────▶│   (Python)      │────▶│   (ChatGPT,     │
│                 │     │                 │     │    Gemini, etc) │
│   - Wake word   │     │   - Poll API    │     │                 │
│   - Record      │     │   - Get text    │     │                 │
│   - Play TTS    │◀────│   - Send to LLM │◀────│                 │
│                 │     │   - TTS response│     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │
         │    Xiaomi Cloud      │
         └──────────────────────┘
```

---

## 🔑 Key Technical Insights

### 1. MiService API Integration

XiaoGPT uses Xiaomi's internal APIs:

- `MiNAService` - Control speaker
- `MiIOService` - IoT device control
- Polling for new voice commands
- Sending TTS responses back

### 2. Multi-LLM Support

Already supports many LLMs (similar to our approach!):

- OpenAI ChatGPT
- Azure OpenAI
- Google Gemini
- Anthropic Claude
- Moonshot (Chinese)
- Qwen (Alibaba)
- GLM (Zhipu)
- And more...

### 3. TTS Options

Multiple TTS backends:

- Edge TTS (Microsoft) ✅ Same as us!
- OpenAI TTS
- Azure TTS
- Google TTS

### 4. Conversation Modes

- Single turn (one question, one answer)
- Continuous conversation (with context)
- Music mode
- Custom prompts

---

## 📚 What We Can Learn

### 1. **Multi-LLM Architecture** ✅ Already doing this!

```python
# XiaoGPT pattern - similar to our approach
class ChatGPTBot:
    async def ask(self, query): ...

class GeminiBot:
    async def ask(self, query): ...

class ClaudeBot:
    async def ask(self, query): ...
```

### 2. **Edge TTS Integration** ✅ Already using!

```python
# XiaoGPT uses edge-tts - same as us!
import edge_tts

async def text_to_speech(text, voice="zh-CN-XiaoxiaoNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("output.mp3")
```

### 3. **Async Architecture**

XiaoGPT is fully async - good for handling multiple requests:

```python
async def main():
    while True:
        # Poll for new commands
        query = await get_latest_query()
        if query:
            # Process with LLM
            response = await llm.ask(query)
            # Send TTS back
            await play_tts(response)
        await asyncio.sleep(1)
```

### 4. **Configuration System**

Clean config management:

```python
@dataclass
class Config:
    mi_user: str
    mi_pass: str
    openai_key: str
    tts_voice: str = "zh-CN-XiaoxiaoNeural"
    # ...
```

### 5. **Streaming Responses**

For faster perceived response time:

```python
async def stream_response(query):
    async for chunk in llm.stream(query):
        # Play audio as it arrives
        await play_chunk(chunk)
```

---

## 🎯 Applicable Ideas for ToToyAI

### Idea 1: Streaming TTS

Instead of waiting for full response, stream audio:

```
Current: Question → Full LLM response → Full TTS → Play
Better:  Question → LLM chunk → TTS chunk → Play → repeat
```

**Benefit:** Faster perceived response time!

### Idea 2: Conversation Context

XiaoGPT maintains conversation history:

```python
class ConversationManager:
    def __init__(self):
        self.history = []

    def add_turn(self, user_msg, assistant_msg):
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": assistant_msg})

    def get_context(self):
        # Return last N turns for context
        return self.history[-10:]
```

**Benefit:** More natural conversations!

### Idea 3: Custom Prompts per Mode

```python
PROMPTS = {
    "story": "Du är en vänlig sagoberättare för barn...",
    "math": "Du är en tålmodig mattelärare...",
    "weather": "Berätta om vädret på ett roligt sätt...",
    "general": "Du är en vänlig kompis som pratar med barn..."
}
```

**Benefit:** Better responses per intent!

### Idea 4: Music/Song Mode

XiaoGPT can play music - we could add:

- Sing-along songs
- Lullabies
- Educational songs
  **Benefit:** More engaging for kids!

---

## ⚖️ Key Differences: XiaoGPT vs ToToyAI

| Aspect         | XiaoGPT                 | ToToyAI           |
| -------------- | ----------------------- | ----------------- |
| **Hardware**   | Existing XiaoAI speaker | Custom ESP32-S3   |
| **Approach**   | Software hack           | Clean build       |
| **Wake Word**  | XiaoAI's built-in       | Our own "Hej Toy" |
| **Target**     | General users           | Children (3-10)   |
| **Language**   | Chinese-first           | Swedish-first     |
| **Dependency** | Xiaomi cloud            | Our own backend   |
| **IP Risk**    | Uses Xiaomi APIs        | 100% clean        |

---

## 🔧 Code Patterns to Adopt

### Pattern 1: LLM Factory

```python
# From XiaoGPT - clean LLM abstraction
def get_llm(config):
    if config.llm == "chatgpt":
        return ChatGPTBot(config.openai_key)
    elif config.llm == "gemini":
        return GeminiBot(config.gemini_key)
    elif config.llm == "groq":
        return GroqBot(config.groq_key)
    # ...
```

### Pattern 2: Async Event Loop

```python
# Main loop pattern
async def run():
    while True:
        try:
            await process_one_turn()
        except Exception as e:
            logger.error(f"Error: {e}")
            await asyncio.sleep(5)
```

### Pattern 3: Graceful Degradation

```python
# Try multiple LLMs if one fails
async def ask_with_fallback(query):
    for llm in [primary_llm, backup_llm, fallback_llm]:
        try:
            return await llm.ask(query)
        except Exception:
            continue
    return "Förlåt, jag kan inte svara just nu."
```

---

## 📋 Action Items for ToToyAI

### Immediate (This Week):

1. [ ] Add streaming TTS support to backend
2. [ ] Implement conversation context/history
3. [ ] Add LLM fallback mechanism

### Short-term (Next 2 Weeks):

4. [ ] Add custom prompts per intent
5. [ ] Implement music/song mode
6. [ ] Add response caching for common questions

### Medium-term (Month 1):

7. [ ] Study XiaoGPT's error handling
8. [ ] Implement similar config system
9. [ ] Add more LLM providers

---

## 🌟 Why Yihong's Approach is Inspiring

1. **Open Source Spirit** - MIT license, shares knowledge
2. **Practical Hacking** - Makes existing hardware better
3. **Multi-LLM Vision** - Not locked to one provider
4. **Community Building** - 5k+ stars, active development
5. **Chinese Developer Scene** - Shows strong AI/IoT community

---

## 🔗 Related Projects by Yihong

Worth checking out:

- **running_page** - Fitness data visualization
- **GitHubPoster** - GitHub contribution art
- **bilingual_book_maker** - AI translation tool

Yihong is known for practical, well-documented open source projects.

---

## 📝 License Note

XiaoGPT is **MIT licensed** ✅

- We can learn from the code
- We can adopt patterns and ideas
- We should NOT copy code directly (write our own)
- Attribution is appreciated but not required

---

## 🎯 Key Takeaway

XiaoGPT proves that:

1. **Multi-LLM is the right approach** - We're on the right track!
2. **Edge TTS works great** - Already using it!
3. **Async architecture is important** - Should improve our backend
4. **Streaming responses matter** - Add this feature!
5. **Community loves open source AI toys** - Good market validation!

---

## 🚀 Next Steps

1. **Study XiaoGPT code** for architecture patterns
2. **Add streaming TTS** to ToToyAI backend
3. **Implement conversation context**
4. **Consider reaching out to Yihong** - Potential advisor/connection?

---

## 💬 Potential Collaboration?

Yihong is active on:

- Twitter/X: @yihong0618
- GitHub: github.com/yihong0618

Could be valuable to:

- Share ToToyAI project
- Get feedback on architecture
- Learn from his experience
- Potential advisor for Chinese market expansion?

---

Great find! XiaoGPT validates our multi-LLM approach and gives us good patterns to follow. 🎉
