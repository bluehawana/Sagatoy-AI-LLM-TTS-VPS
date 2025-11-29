# 🚀 ToToyAI MVP Roadmap - Investor Demo Ready

## 🎯 Goal: Working Demo in 2-3 Weeks

**Objective:** Prove the full stack works end-to-end to attract investors/angels.

---

## 📦 What You Already Have

### Hardware ✅

- **2x FoloToy Octopus kits** - Complete hardware (ESP32-S3, mic, speaker, battery)
- No need to buy components for MVP!

### Backend ✅

- Multi-LLM support (Groq, Gemini)
- Azure Speech Services (STT/TTS)
- Swedish kindergarten voices
- Story library
- Weather integration
- FastAPI backend

### Missing for MVP ⏳

- FoloToy firmware modification (point to our backend)
- Cloud deployment (VPS)
- Simple parent dashboard
- Demo video/pitch deck

---

## 🐙 Phase 1: FoloToy Octopus Integration (Week 1)

### Option A: Use FoloToy's Open Protocol

FoloToy uses MQTT protocol. We can:

1. Set up our own MQTT broker
2. Configure Octopus to connect to our server
3. Handle audio streams on our backend

### Option B: Custom Firmware (More Control)

1. Flash ESPHome or custom firmware
2. Direct HTTP/WebSocket to our backend
3. Full control over behavior

### Tasks:

- [ ] Research FoloToy Octopus firmware/protocol
- [ ] Set up MQTT broker (Mosquitto) or WebSocket endpoint
- [ ] Test audio streaming from Octopus to backend
- [ ] Test audio playback from backend to Octopus

---

## ☁️ Phase 2: Cloud Deployment (Week 1-2)

### VPS Options (Sweden/EU):

| Provider         | Location  | Price/month | Specs           |
| ---------------- | --------- | ----------- | --------------- |
| **Hetzner**      | Germany   | ~50 SEK     | 2 vCPU, 4GB RAM |
| **DigitalOcean** | Amsterdam | ~60 SEK     | 1 vCPU, 2GB RAM |
| **Linode**       | Frankfurt | ~55 SEK     | 1 vCPU, 2GB RAM |
| **Scaleway**     | Paris     | ~40 SEK     | 2 vCPU, 2GB RAM |

### Recommended: Hetzner (Best value, EU data)

### Deployment Stack:

```
┌─────────────────────────────────────┐
│           Hetzner VPS               │
├─────────────────────────────────────┤
│  Docker Compose                     │
│  ├── ToToyAI Backend (FastAPI)      │
│  ├── MQTT Broker (Mosquitto)        │
│  ├── Redis (session cache)          │
│  └── Nginx (reverse proxy + SSL)    │
└─────────────────────────────────────┘
```

### Tasks:

- [ ] Set up Hetzner VPS
- [ ] Install Docker + Docker Compose
- [ ] Deploy backend with docker-compose
- [ ] Configure SSL (Let's Encrypt)
- [ ] Set up domain (totoyai.se?)

---

## 🎨 Phase 3: Parent Dashboard (Week 2)

### Simple MVP Dashboard:

- Login page
- Device status (online/offline)
- Usage stats (conversations today)
- Volume control
- Content settings

### Tech Stack:

- **Frontend:** Simple HTML/CSS/JS or React
- **Backend:** FastAPI (already have)
- **Auth:** JWT (already have)

### Tasks:

- [ ] Design simple dashboard UI
- [ ] Create dashboard API endpoints
- [ ] Build basic frontend
- [ ] Test with real device

---

## 🎬 Phase 4: Demo & Pitch (Week 3)

### Demo Video (2-3 minutes):

1. **Problem:** Kids need safe, educational AI interaction
2. **Solution:** ToToyAI - Swedish-first AI toy
3. **Demo:** Live interaction with Octopus
4. **Tech:** Show backend, multi-LLM, Swedish voices
5. **Market:** Sweden → Nordics → EU
6. **Ask:** Seed funding for production

### Pitch Deck (10 slides):

1. Cover - ToToyAI logo
2. Problem - Screen time, unsafe AI
3. Solution - Safe, educational AI toy
4. Demo - Video/screenshots
5. Technology - Architecture diagram
6. Market - TAM/SAM/SOM
7. Business Model - Hardware + subscription
8. Competition - vs FoloToys, Moxie
9. Team - Your background
10. Ask - Funding amount, use of funds

### Tasks:

- [ ] Record demo video
- [ ] Create pitch deck
- [ ] Practice pitch (2 min, 5 min versions)
- [ ] Identify target investors

---

## 💰 Investor Targets (Sweden)

### Angel Networks:

- **STING** (Stockholm) - Tech startups
- **SUP46** (Stockholm) - Startup hub
- **Almi Invest** - Government-backed
- **Connect Sverige** - Angel network

### VCs (Seed Stage):

- **Creandum** - Nordic focus
- **Northzone** - Stockholm
- **EQT Ventures** - Large but does seed
- **Inventure** - Nordic

### Grants:

- **Vinnova** - Innovation grants
- **Almi** - Startup loans
- **EU Horizon** - Research grants

---

## 📊 MVP Success Metrics

### Technical:

- [ ] End-to-end latency < 3 seconds
- [ ] 95% wake word accuracy
- [ ] 8+ hours battery life
- [ ] Works on home WiFi

### Demo:

- [ ] 5+ successful conversations recorded
- [ ] Swedish voice sounds natural
- [ ] Child-appropriate responses
- [ ] Weather/story features work

### Business:

- [ ] 3+ investor meetings scheduled
- [ ] Pitch deck reviewed by mentors
- [ ] Domain + landing page live

---

## 🛠️ Technical Architecture for MVP

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  FoloToy        │     │   VPS (Cloud)   │     │   External      │
│  Octopus        │     │                 │     │   Services      │
│                 │     │  ┌───────────┐  │     │                 │
│  ESP32-S3       │────▶│  │  MQTT     │  │     │  ┌───────────┐  │
│  + Mic          │     │  │  Broker   │  │     │  │  Groq     │  │
│  + Speaker      │     │  └─────┬─────┘  │     │  │  (LLM)    │  │
│  + Battery      │     │        │        │     │  └───────────┘  │
│                 │◀────│  ┌─────▼─────┐  │     │                 │
└─────────────────┘     │  │  ToToyAI  │──│────▶│  ┌───────────┐  │
                        │  │  Backend  │  │     │  │  Azure    │  │
┌─────────────────┐     │  │  (FastAPI)│◀─│─────│  │  Speech   │  │
│  Parent         │     │  └───────────┘  │     │  └───────────┘  │
│  Dashboard      │────▶│                 │     │                 │
│  (Web)          │     │  ┌───────────┐  │     │  ┌───────────┐  │
└─────────────────┘     │  │  Redis    │  │     │  │  Gemini   │  │
                        │  │  (Cache)  │  │     │  │  (Stories)│  │
                        │  └───────────┘  │     │  └───────────┘  │
                        └─────────────────┘     └─────────────────┘
```

---

## 📅 Week-by-Week Plan

### Week 1: Hardware + Cloud

| Day | Task                                  |
| --- | ------------------------------------- |
| Mon | Research FoloToy protocol, set up VPS |
| Tue | Deploy backend to VPS, test APIs      |
| Wed | Set up MQTT broker, test connection   |
| Thu | Connect Octopus to our backend        |
| Fri | End-to-end test: voice → response     |

### Week 2: Polish + Dashboard

| Day | Task                           |
| --- | ------------------------------ |
| Mon | Fix bugs from Week 1 testing   |
| Tue | Build simple parent dashboard  |
| Wed | Add device management features |
| Thu | Test with family/friends       |
| Fri | Collect feedback, iterate      |

### Week 3: Demo + Pitch

| Day | Task                         |
| --- | ---------------------------- |
| Mon | Record demo video            |
| Tue | Create pitch deck            |
| Wed | Practice pitch, get feedback |
| Thu | Reach out to investors       |
| Fri | Schedule meetings            |

---

## 💡 Key Differentiators for Investors

### Why ToToyAI vs Competitors:

1. **Swedish-First** - No competitor focuses on Swedish market
2. **Multi-LLM** - Not locked to one AI provider
3. **Open Architecture** - Can customize for enterprise/schools
4. **Privacy-Focused** - EU data, GDPR compliant
5. **Kindergarten Voices** - Specifically optimized for children

### Market Opportunity:

- Sweden: 500K children ages 3-10
- Nordics: 2.5M children
- EU: 40M children
- Price point: 800-1200 SEK hardware + 50-100 SEK/month subscription

### Revenue Model:

- Hardware margin: 40-50%
- Subscription: 50-100 SEK/month
- B2B (schools): Custom pricing
- Content licensing: Future revenue

---

## ✅ MVP Checklist

### Hardware

- [x] FoloToy Octopus kits (you have 2)
- [ ] Test Octopus with original FoloToy app
- [ ] Research firmware modification options

### Backend

- [x] Multi-LLM support
- [x] Swedish TTS voices
- [x] Story library
- [ ] MQTT endpoint for Octopus
- [ ] WebSocket audio streaming

### Cloud

- [ ] VPS provisioned
- [ ] Docker deployment
- [ ] SSL certificate
- [ ] Domain configured

### Dashboard

- [ ] Basic login
- [ ] Device status
- [ ] Usage stats

### Demo

- [ ] Working end-to-end demo
- [ ] Demo video recorded
- [ ] Pitch deck created

---

## 🎉 After MVP: Production Path

Once MVP proves concept:

1. **Custom Hardware** - Design PCB in China (Shenzhen)
2. **Custom Firmware** - ESP-IDF optimized
3. **Scale Backend** - Kubernetes, auto-scaling
4. **Mobile App** - iOS/Android
5. **Certifications** - CE, FCC, safety
6. **Manufacturing** - 1000+ units

**Estimated timeline:** 6-12 months from MVP to production

---

## 🚀 Let's Go!

You have everything needed for MVP:

- ✅ Hardware (FoloToy Octopus)
- ✅ Backend (already built)
- ✅ AI services (Groq, Gemini, Azure)

**Next step:** Test FoloToy Octopus with original app, then research how to connect to our backend.

Ready to start? 🧸
