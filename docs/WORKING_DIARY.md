# Sagatoyai Working Diary

## 2026-04-12: MQTT Integration for FoloToy Octopus

### Context
User has 2 FoloToy Octopus toys. Need to connect them to Sagatoyai VPS instead of FoloToy's official server.

### FoloToy Protocol Discovered
- Uses MQTT for communication
- WiFi provisioning via AP mode (192.168.4.1)
- Server configurable in pairing mode
- Default: f.folotoy.cn:1883
- Octopus pairing: Hold both "previous" + "next" buttons (old) or hold ButtonB (new)

### Implementation Completed

**1. Added MQTT Broker (Mosquitto)**
- File: `backend/docker-compose.yml`
- Port 1883 (MQTT) and 9001 (WebSocket)
- Configuration: `backend/mosquitto.conf`

**2. Created MQTT Service**
- File: `backend/src/sagatoyai/services/mqtt_service.py`
- Handles FoloToy protocol
- Topics: `folotoy/{device_id}/audio`, `folotoy/{device_id}/text`

**3. Integrated with Pipeline**
```
Toy Audio → MQTT → STT (Whisper) → LLM (Groq) → TTS (Edge) → MQTT → Toy
```
- Supports Swedish and English

**4. Updated Dependencies**
- Added `aiomqtt>=2.0.0` to pyproject.toml
- Added `groq>=0.4.0` to pyproject.toml

### Deploy Steps for VPS

```bash
# SSH to VPS
ssh -p 1025 harvard@94.72.141.71

# Navigate to project
cd /var/www/sagatoy

# Pull changes
git pull origin main

# Open firewall port for MQTT
sudo ufw allow 1883/tcp

# Rebuild and restart
cd backend
docker-compose down
docker-compose build
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Test with Octopus

```
1. Charge toy (user doing now)
2. Enter pairing mode (hold buttons)
3. Connect to "FoloToy-xxxx" WiFi
4. Go to 192.168.4.1
5. Set:
   - Home WiFi + password
   - MQTT server: sagatoy.com (or 94.72.141.71)
   - MQTT port: 1883
6. Save and test
```

### Action Items
- [x] Add MQTT broker to docker-compose
- [x] Create MQTT service
- [x] Connect to STT/LLM/TTS pipeline
- [ ] Deploy to VPS
- [ ] Open port 1883 on VPS firewall
- [ ] Test with Octopus toy

---

## 2026-04-12: Hardware Strategy & Differentiation Discussion

### Context
Competitor analysis: FoloToy (China) uses Docker-based setup requiring technical knowledge. Our opportunity: make setup seamless for non-technical parents.

---

### Product Vision: Onboard Motherboard Requirements

**Must-have capabilities:**
1. WiFi connectivity (wireless pairing)
2. CPU + local storage (pre-loaded content)
3. OTA firmware updates
4. Download additional content from server
5. Mobile app for setup & management

---

### Hardware Options Comparison

| Feature | ESP32-S3 | Pi Zero 2 W | Custom PCB |
|---------|----------|-------------|------------|
| WiFi built-in | ✅ | ✅ | ✅ |
| Form factor for toy | ✅ Fits | ⚠️ Tight | ✅ Custom |
| Local storage | SD card slot | SD card | Flash/SD |
| OTA updates | ✅ Built-in | ✅ | ✅ |
| Battery life | Excellent | Moderate | Design-dependent |
| Cost (volume) | $3-5 | $15 | $5-10 |
| Parent-friendly setup | BLE/SmartConfig | Requires config | BLE provisioning |

---

### WiFi Pairing Strategies (No Technical Knowledge Required)

**Recommended: BLE Provisioning**
```
1. Parent opens Sagatoy app
2. App scans for toy via Bluetooth
3. Parent enters WiFi credentials in app
4. Toy connects to WiFi automatically
5. Done - no manual setup
```

**Alternative: SmartConfig (ESP32 native)**
- Parent connects phone to WiFi
- App broadcasts credentials
- Toy listens and connects

---

### Mobile App Requirements (iOS + Android)

**Core Features:**
- WiFi pairing via BLE
- Device status (online/offline, battery)
- Volume control
- Content management (download stories/songs)
- Factory reset / TF card format
- Parent voice cloning setup
- Usage statistics

**Tech Stack Recommendation:**
- **React Native** or **Flutter** (single codebase for iOS + Android)
- Backend: Your existing FastAPI at sagatoy.com
- Push notifications for device alerts

---

### OTA Update Architecture

```
┌─────────────┐      ┌─────────────────┐      ┌─────────────┐
│  Sagatoy    │      │  VPS Backend    │      │  Toy        │
│  Mobile App │      │  (sagatoy.com)  │      │  ESP32-S3   │
└──────┬──────┘      └────────┬────────┘      └──────┬──────┘
       │                      │                      │
       │  Check for updates   │                      │
       │─────────────────────▶│                      │
       │                      │                      │
       │  New firmware v1.2   │                      │
       │◀─────────────────────│                      │
       │                      │                      │
       │  Trigger update      │                      │
       │─────────────────────▶│                      │
       │                      │  Push notification   │
       │                      │─────────────────────▶│
       │                      │                      │
       │                      │  Download firmware   │
       │                      │◀─────────────────────│
       │                      │                      │
       │                      │  Firmware binary     │
       │                      │─────────────────────▶│
       │                      │                      │
       │  Update complete     │  Verify & install    │
       │◀─────────────────────│◀─────────────────────│
```

---

### Voice Cloning Feature (Parent's Voice for Stories)

**Nvidia Open-Source Options:**
- **Nemo TTS** - High quality, needs GPU (run on VPS)
- **F5-TTS** - Newer, lighter, CPU-friendly
- **Coqui XTTS** - Good balance, 30s clone time

**Implementation Plan:**
1. Parent records 30-60s sample in app
2. Upload to VPS for cloning
3. Store voice embedding securely (GDPR)
4. Use cloned voice for story generation
5. Parent can delete voice data anytime

**Privacy:**
- Explicit consent required
- Voice data encrypted at rest
- EU servers only
- Right to deletion (GDPR Article 17)

---

### MVP Hardware Decision

**Recommendation: ESP32-S3 + SD Card**

Why not Pi 5/Zero for MVP:
- Pi form factor too large for plush toy
- Higher power consumption = shorter battery life
- More expensive (affects margin)

Why ESP32-S3:
- Already tested with FoloToy Octopus
- Fits in toy
- BLE + WiFi built-in
- OTA support native
- Your VPS handles heavy compute

**Production Path:**
1. MVP: ESP32-S3 prototype (borrow FoloToy hardware approach)
2. V1: Custom PCB with ESP32-S3 + optimized audio circuit
3. V2: Add local processing for offline mode (larger MCU)

---

### Differentiation from Competitors

| Feature | FoloToy | Sagatoyai |
|---------|---------|-----------|
| Setup | Docker (technical) | Mobile app (parent-friendly) |
| Language | Chinese-focused | Swedish + EU languages |
| Voice cloning | ❌ | ✅ Planned |
| Content updates | Manual | In-app download |
| Reset/recovery | CLI | Mobile app |
| Target market | Tech-savvy | Mainstream parents |

---

### Action Items

- [ ] Research BLE provisioning libraries for ESP32-S3
- [ ] Prototype mobile app (React Native/Flutter)
- [ ] Design OTA update API endpoint
- [ ] Test voice cloning with Coqui XTTS on VPS
- [ ] Create user journey: unboxing → first use

---

## Future Entries

*Add new dated entries below as project progresses...*

---

### Template for New Entries

```markdown
## YYYY-MM-DD: [Topic]

### Context
[Why this discussion/decision happened]

### Options Considered
[What alternatives were evaluated]

### Decision
[What was chosen and why]

### Action Items
- [ ] Task 1
- [ ] Task 2
```
