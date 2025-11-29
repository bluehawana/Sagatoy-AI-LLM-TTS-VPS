# 🚀 Option B: Clean Build from Scratch

## Why This is Better

After legal review, we're building 100% from scratch:

| Aspect              | FoloToy Route | Clean Build     |
| ------------------- | ------------- | --------------- |
| **IP Ownership**    | ❌ Risky      | ✅ 100% yours   |
| **Legal Risk**      | ⚠️ High       | ✅ None         |
| **Investor Appeal** | ⚠️ Questions  | ✅ Clean story  |
| **Voice Wake Word** | ❌ No         | ✅ Yes          |
| **Customization**   | ❌ Limited    | ✅ Full control |
| **FoloToy Scandal** | ⚠️ Associated | ✅ Distanced    |

---

## 🎯 What We're Building

### Hardware Stack (All Open/Generic):

```
┌─────────────────────────────────────┐
│         ToToyAI Hardware            │
├─────────────────────────────────────┤
│  ESP32-S3 DevKit     (Espressif)    │  ← Apache 2.0 license
│  INMP441 Mic         (Generic)      │  ← No IP issues
│  MAX98357A Amp       (Generic)      │  ← No IP issues
│  3W Speaker          (Generic)      │  ← No IP issues
│  Li-ion Battery      (Generic)      │  ← No IP issues
└─────────────────────────────────────┘
```

### Software Stack (All Ours/Open):

```
┌─────────────────────────────────────┐
│         ToToyAI Software            │
├─────────────────────────────────────┤
│  Firmware: ESP-IDF   (Apache 2.0)   │
│  Wake Word: Edge Impulse (Our model)│
│  Backend: ToToyAI    (100% ours)    │
│  LLM: Groq/Gemini    (API license)  │
│  TTS: Azure          (API license)  │
│  STT: Azure          (API license)  │
└─────────────────────────────────────┘
```

---

## 📦 Shopping List (Mouser.se)

### Minimum Viable Hardware (~500 SEK):

| Component               | Mouser Part #         | Price (SEK)  |
| ----------------------- | --------------------- | ------------ |
| ESP32-S3-DevKitC-1-N8R8 | 356-ESP32S3DVKTC1N8R8 | 180          |
| MAX98357A Breakout      | 485-3006              | 85           |
| SPH0645 I2S Mic         | 485-3421              | 75           |
| Speaker 3W 4Ω           | 665-AS04008PS-R       | 45           |
| Breadboard              | 485-64                | 55           |
| Jumper Wires            | 485-1956              | 25           |
| USB-C Cable             | 485-4474              | 40           |
| **Total**               |                       | **~505 SEK** |

### Optional (Battery + Wake Word MCU):

| Component            | Mouser Part #       | Price (SEK)  |
| -------------------- | ------------------- | ------------ |
| ESP32-C3-DevKitM-1   | 356-ESP32C3DEVKITM1 | 90           |
| 18650 Battery Holder | -                   | 30           |
| TP4056 Charger       | - (AliExpress)      | 20           |
| **Optional Total**   |                     | **~140 SEK** |

---

## 🗓️ Development Timeline

### Week 1: Hardware Setup

| Day | Task                         | Deliverable        |
| --- | ---------------------------- | ------------------ |
| 1   | Order from Mouser.se         | Order confirmation |
| 2-3 | Components arrive            | Hardware in hand   |
| 4   | Wire breadboard prototype    | Working circuit    |
| 5   | Install ESP-IDF, flash test  | LED blinks         |
| 6-7 | Test I2S audio (record/play) | Audio works        |

### Week 2: Audio Pipeline

| Day | Task                       | Deliverable         |
| --- | -------------------------- | ------------------- |
| 1-2 | Record audio to buffer     | WAV capture works   |
| 3-4 | Play audio from buffer     | Speaker works       |
| 5-6 | WiFi connection            | Connects to network |
| 7   | HTTP POST audio to backend | End-to-end test     |

### Week 3: Wake Word

| Day | Task                            | Deliverable      |
| --- | ------------------------------- | ---------------- |
| 1-2 | Create Edge Impulse account     | Account ready    |
| 3-4 | Record "Hej Toy" samples (200+) | Training data    |
| 5-6 | Train wake word model           | Model exported   |
| 7   | Integrate into firmware         | Wake word works! |

### Week 4: Integration & Demo

| Day | Task                      | Deliverable      |
| --- | ------------------------- | ---------------- |
| 1-2 | Full pipeline integration | End-to-end works |
| 3-4 | Bug fixes, optimization   | Stable demo      |
| 5   | Record demo video         | Video ready      |
| 6-7 | Prepare pitch materials   | Investor ready   |

---

## 🔧 Technical Architecture

### Firmware Flow:

```
┌─────────────────────────────────────────────────────────┐
│                    ESP32-S3 Firmware                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Audio   │───▶│  Wake    │───▶│  Record  │          │
│  │  Input   │    │  Word    │    │  Speech  │          │
│  │  (I2S)   │    │  Detect  │    │  Buffer  │          │
│  └──────────┘    └──────────┘    └──────────┘          │
│                        │               │                │
│                   "Hej Toy"       End of speech         │
│                   detected        detected              │
│                                        │                │
│                                        ▼                │
│                              ┌──────────────┐           │
│                              │  Send to     │           │
│                              │  Backend     │           │
│                              │  (HTTP/WS)   │           │
│                              └──────────────┘           │
│                                        │                │
│                                        ▼                │
│                              ┌──────────────┐           │
│                              │  Receive     │           │
│                              │  Audio       │           │
│                              │  Response    │           │
│                              └──────────────┘           │
│                                        │                │
│                                        ▼                │
│                              ┌──────────────┐           │
│                              │  Play on     │           │
│                              │  Speaker     │           │
│                              │  (I2S)       │           │
│                              └──────────────┘           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Backend Integration:

```
ESP32-S3                         ToToyAI Backend
    │                                   │
    │  POST /api/v1/conversation        │
    │  {audio: base64, device_id}       │
    │──────────────────────────────────▶│
    │                                   │
    │                            ┌──────┴──────┐
    │                            │ STT (Azure) │
    │                            │ LLM (Groq)  │
    │                            │ TTS (Azure) │
    │                            └──────┬──────┘
    │                                   │
    │  Response: {audio: base64}        │
    │◀──────────────────────────────────│
    │                                   │
    ▼
 Play audio
```

---

## 📁 Firmware Project Structure

```
totoyai-firmware/
├── CMakeLists.txt
├── sdkconfig
├── main/
│   ├── CMakeLists.txt
│   ├── main.c                 # Entry point
│   ├── audio_input.c          # I2S microphone
│   ├── audio_output.c         # I2S speaker
│   ├── wake_word.c            # Edge Impulse model
│   ├── wifi_manager.c         # WiFi connection
│   ├── http_client.c          # Backend communication
│   ├── led_status.c           # RGB LED feedback
│   └── config.h               # Configuration
├── components/
│   └── edge_impulse/          # Wake word model
└── README.md
```

---

## 🎤 Wake Word Training (Edge Impulse)

### Step 1: Create Account

- Go to https://edgeimpulse.com/
- Sign up (free tier is enough)
- Create new project: "ToToyAI Wake Word"

### Step 2: Collect Data

Record samples:

- **"Hej Toy"** - 200+ samples (you, family, different voices)
- **"Hey Toy"** - 100+ samples (English alternative)
- **Background noise** - 500+ samples (silence, TV, kids playing)
- **Other words** - 200+ samples (negative examples)

### Step 3: Train Model

- Upload samples to Edge Impulse
- Configure audio processing (MFCC features)
- Train neural network
- Test accuracy (target: >95%)

### Step 4: Deploy

- Export as C++ library
- Integrate into ESP32 firmware
- Test on device

---

## 💰 Cost Breakdown

### Development (One-time):

| Item                | Cost (SEK)     |
| ------------------- | -------------- |
| Hardware prototype  | 500            |
| Extra components    | 200            |
| Domain (totoyai.se) | 150/year       |
| VPS (3 months)      | 300            |
| **Total**           | **~1,150 SEK** |

### Monthly (After MVP):

| Item                    | Cost (SEK)       |
| ----------------------- | ---------------- |
| VPS hosting             | 100              |
| Azure Speech (dev tier) | 0-200            |
| Groq API (dev tier)     | 0-100            |
| **Monthly**             | **~200-400 SEK** |

---

## ✅ IP Ownership Checklist

| Component       | License    | Commercial OK | Notes                   |
| --------------- | ---------- | ------------- | ----------------------- |
| ESP32-S3        | Apache 2.0 | ✅ Yes        | Espressif open hardware |
| ESP-IDF         | Apache 2.0 | ✅ Yes        | Open source SDK         |
| Edge Impulse    | Your model | ✅ Yes        | You own trained model   |
| INMP441         | Generic    | ✅ Yes        | Standard component      |
| MAX98357A       | Generic    | ✅ Yes        | Standard component      |
| ToToyAI Backend | Yours      | ✅ Yes        | 100% your code          |
| Groq API        | API Terms  | ✅ Yes        | Standard API usage      |
| Azure Speech    | API Terms  | ✅ Yes        | Standard API usage      |

**Result: 100% clean IP, no legal risks!**

---

## 🎯 Investor Story

### The Pitch:

> "We built ToToyAI from the ground up - 100% our own technology.
>
> Unlike competitors who've had safety scandals, we designed child safety
> into our architecture from day one:
>
> - Content filtering at every layer
> - Swedish-first, GDPR compliant
> - No dependency on third-party toy platforms
> - Voice wake word for natural interaction
>
> Our prototype demonstrates the full stack working end-to-end,
> and we own every piece of the IP."

### Key Differentiators:

1. **Clean IP** - No licensing issues
2. **Voice Wake Word** - Hands-free, magical for kids
3. **Swedish-First** - Untapped Nordic market
4. **Safety-First** - Designed after competitor scandals
5. **Multi-LLM** - Not locked to one provider

---

## 🚀 Next Steps

### Today:

1. [ ] Place Mouser.se order (~500 SEK)
2. [ ] Create Edge Impulse account
3. [ ] Set up ESP-IDF development environment

### This Week:

1. [ ] Receive components
2. [ ] Wire breadboard prototype
3. [ ] Flash first test firmware

### Next Week:

1. [ ] Get audio I/O working
2. [ ] Connect to backend
3. [ ] Start wake word training

---

## 📞 Questions?

This plan gives you:

- ✅ Working prototype in 4 weeks
- ✅ 100% clean IP
- ✅ Voice wake word (unique feature)
- ✅ Investor-ready demo
- ✅ No legal risks

Ready to order from Mouser? 🛒
