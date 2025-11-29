# 🔧 SagaToy Hardware Solution - Independent Design

## 🎯 Goal

Create a completely independent hardware solution with:

- ✅ No IP conflicts with FoloToys or other products
- ✅ Open-source components where possible
- ✅ Custom motherboard design
- ✅ Wake word detection on-device
- ✅ Cost-effective manufacturing

---

## 🏗️ Hardware Architecture

### Option 1: ESP32-S3 Based Solution (RECOMMENDED)

**Why ESP32-S3:**

- ✅ Built-in WiFi & Bluetooth
- ✅ Dual-core processor (240 MHz)
- ✅ 512KB SRAM (enough for wake word detection)
- ✅ I2S audio support (high-quality audio)
- ✅ Low power consumption
- ✅ Affordable (~$2-3 per unit)
- ✅ Large community support
- ✅ No licensing issues (Espressif is open)

**Components:**

```
1. ESP32-S3-WROOM-1 Module
   - Dual-core Xtensa LX7 @ 240MHz
   - 512KB SRAM, 384KB ROM
   - WiFi 802.11 b/g/n
   - Bluetooth 5.0 LE
   - Cost: ~$2.50

2. Audio Components:
   - MAX98357A I2S Amplifier (~$1.50)
   - INMP441 MEMS Microphone (~$1.00)
   - 3W 4Ω Speaker (~$2.00)

3. Power Management:
   - TP4056 Li-ion Charger (~$0.30)
   - 18650 Battery 2000mAh (~$3.00)
   - AMS1117-3.3 Voltage Regulator (~$0.20)

4. User Interface:
   - WS2812B RGB LED (status) (~$0.10)
   - Push Button (manual trigger) (~$0.05)

5. Storage:
   - MicroSD Card Slot (~$0.30)
   - 8GB MicroSD Card (~$2.00)

Total BOM Cost: ~$13-15 per unit
```

### Option 2: Raspberry Pi Zero 2 W Based (Higher Performance)

**For more advanced features:**

- ✅ Quad-core ARM Cortex-A53 @ 1GHz
- ✅ 512MB RAM
- ✅ Full Linux OS
- ✅ Better for complex AI processing
- ❌ Higher cost (~$15 just for the board)
- ❌ Higher power consumption

---

## 🎤 Wake Word Detection Solution

### Approach 1: Edge Impulse (RECOMMENDED)

**Why Edge Impulse:**

- ✅ Free for development
- ✅ Train custom wake words
- ✅ Runs on ESP32
- ✅ No licensing fees for deployment
- ✅ Low latency (<100ms)
- ✅ Low power consumption

**Implementation:**

```cpp
// Custom wake words we can train:
- "Hej Saga" (Swedish)
- "Hello Saga" (English)
- "Hey Saga" (English alternative)

// Edge Impulse provides:
- Model training platform
- ESP32 deployment library
- Continuous listening mode
- Confidence scoring
```

**Steps:**

1. Record 100+ samples of each wake word
2. Train model on Edge Impulse platform
3. Export optimized model for ESP32
4. Deploy with <50KB memory footprint

### Approach 2: TensorFlow Lite Micro

**Alternative open-source solution:**

- ✅ Completely free and open
- ✅ Custom model training
- ✅ Runs on ESP32
- ❌ More complex to implement
- ❌ Requires ML expertise

### Approach 3: Simple Audio Pattern Matching

**Fallback for MVP:**

- ✅ Very simple implementation
- ✅ No ML required
- ✅ Low resource usage
- ❌ Less accurate
- ❌ More false positives

---

## 🔊 Audio Processing Pipeline

### On-Device (ESP32):

```
1. Microphone → I2S Input
2. Audio Buffer (16kHz, 16-bit)
3. Wake Word Detection (Edge Impulse)
4. Voice Activity Detection (VAD)
5. Audio Streaming → Backend via WiFi
```

### Backend Processing:

```
1. Receive audio stream
2. Speech-to-Text (Whisper API or Groq)
3. Intent Detection & LLM Response
4. Text-to-Speech (Edge TTS)
5. Stream audio back → ESP32
6. ESP32 → I2S Output → Speaker
```

---

## 📟 Custom Motherboard Design

### PCB Layout (4-Layer Board)

```
Layer 1 (Top):    Components, WiFi antenna
Layer 2:          Ground plane
Layer 3:          Power plane (3.3V)
Layer 4 (Bottom): Signal routing, battery connector

Dimensions: 50mm x 40mm (fits in plush toy)
```

### Key Features:

1. **ESP32-S3 Module** (center)
2. **Audio Section:**

   - MEMS microphone with noise filtering
   - I2S amplifier with speaker output
   - 3.5mm audio jack (optional)

3. **Power Section:**

   - USB-C charging port
   - Battery management IC
   - Power switch
   - LED charging indicator

4. **User Interface:**

   - RGB status LED
   - Manual trigger button
   - Volume control (potentiometer)

5. **Expansion:**
   - MicroSD card slot
   - I2C header (for sensors)
   - UART debug header

### Manufacturing:

- **PCB Fabrication:** JLCPCB, PCBWay (~$2-5 per board at 100+ qty)
- **Assembly:** SMT assembly service (~$5-10 per board)
- **Total:** ~$20-25 per unit including components

---

## 🔋 Power Management

### Battery Life Optimization:

```
Operating Modes:
1. Deep Sleep:     ~10μA (waiting for wake word)
2. Wake Word:      ~50mA (continuous listening)
3. Active:         ~200mA (WiFi + audio processing)
4. Streaming:      ~300mA (full operation)

Battery: 2000mAh Li-ion
- Deep sleep: ~8 months
- Wake word only: ~40 hours
- Active use: ~6-7 hours
- Mixed use: ~2-3 days
```

### Charging:

- USB-C charging (5V, 1A)
- Charge time: ~2-3 hours
- LED indicator (red=charging, green=full)

---

## 🛠️ Firmware Architecture

### ESP32 Firmware (C++/Arduino):

```cpp
// Main components:
1. WiFi Manager
   - Auto-connect to saved networks
   - Fallback AP mode for setup
   - OTA update support

2. Wake Word Engine
   - Edge Impulse inference
   - Confidence threshold
   - False positive filtering

3. Audio Manager
   - I2S microphone input
   - I2S speaker output
   - Audio buffering
   - Stream management

4. Communication Layer
   - WebSocket to backend
   - Audio streaming
   - Command handling
   - Status reporting

5. Power Management
   - Sleep modes
   - Battery monitoring
   - Low battery alerts
```

### File Structure:

```
firmware/
├── src/
│   ├── main.cpp
│   ├── wifi_manager.cpp
│   ├── wake_word.cpp
│   ├── audio_manager.cpp
│   ├── websocket_client.cpp
│   └── power_manager.cpp
├── lib/
│   ├── edge-impulse-sdk/
│   └── audio-tools/
├── include/
│   └── config.h
└── platformio.ini
```

---

## 📱 Setup & Configuration

### Initial Setup Flow:

```
1. Power on toy
2. No WiFi → Enter AP mode
3. User connects phone to "SagaToy-Setup-XXXX"
4. Web interface opens (captive portal)
5. User enters WiFi credentials
6. Toy connects to WiFi
7. Registers with backend
8. Downloads initial content
9. Ready to use!
```

### Web Interface (Captive Portal):

```html
- WiFi network selection - Password entry - Language selection (Swedish/English)
- Child's name (optional) - Volume settings - Test audio
```

---

## 🔐 Security Considerations

### Device Security:

1. **Unique Device ID** - Generated on first boot
2. **Encrypted Communication** - TLS/SSL for all backend communication
3. **Secure Storage** - Encrypted credentials in flash
4. **OTA Security** - Signed firmware updates only
5. **No Audio Storage** - Audio streams, never stored locally

### Privacy:

1. **No Cloud Recording** - Audio processed in real-time only
2. **Local Wake Word** - No audio sent until wake word detected
3. **Parent Control** - Dashboard to manage settings
4. **Data Deletion** - Easy account/data removal

---

## 🏭 Manufacturing Plan

### Prototype Phase (10 units):

```
1. Order PCBs from JLCPCB: ~$50
2. Order components from Mouser/DigiKey: ~$200
3. Hand assembly: DIY
4. 3D print enclosures: ~$50
5. Total: ~$300 for 10 prototypes
```

### Small Batch (100 units):

```
1. PCB + SMT assembly: ~$2000
2. Components (bulk): ~$1300
3. Enclosures (injection molding): ~$500
4. Assembly & testing: ~$500
5. Total: ~$4300 ($43/unit)
```

### Mass Production (1000+ units):

```
1. PCB + SMT assembly: ~$15000
2. Components (bulk): ~$10000
3. Enclosures (tooling + production): ~$3000
4. Assembly & testing: ~$3000
5. Total: ~$31000 ($31/unit)
```

---

## 🎨 Enclosure Design

### Requirements:

- Child-safe materials (BPA-free plastic)
- Soft-touch finish
- Washable exterior
- Easy battery access (for parents)
- Speaker grille
- LED light diffuser
- Button accessibility

### Design Options:

1. **3D Printed** (prototypes)

   - PLA or PETG
   - Smooth finish
   - Cost: ~$5 per unit

2. **Injection Molded** (production)
   - ABS or PP plastic
   - Professional finish
   - Tooling: ~$2000-3000
   - Unit cost: ~$2-3

---

## 📋 Development Roadmap

### Phase 1: Prototype (2-3 weeks)

- [ ] Design PCB schematic
- [ ] Order components
- [ ] Breadboard testing
- [ ] Wake word model training
- [ ] Basic firmware development

### Phase 2: PCB Design (2 weeks)

- [ ] PCB layout design
- [ ] Design review
- [ ] Order PCBs
- [ ] SMT assembly

### Phase 3: Firmware Development (3-4 weeks)

- [ ] WiFi manager
- [ ] Wake word integration
- [ ] Audio streaming
- [ ] Backend communication
- [ ] Power management
- [ ] OTA updates

### Phase 4: Testing (2 weeks)

- [ ] Functional testing
- [ ] Audio quality testing
- [ ] Battery life testing
- [ ] Range testing
- [ ] User testing with children

### Phase 5: Enclosure (2-3 weeks)

- [ ] 3D model design
- [ ] Prototype printing
- [ ] Fit testing
- [ ] Prepare for injection molding

### Phase 6: Pilot Production (4 weeks)

- [ ] Order 100 units
- [ ] Quality control
- [ ] User testing
- [ ] Feedback iteration

---

## 💰 Cost Analysis

### Per Unit Cost (at 1000 units):

```
Hardware:
- PCB + Assembly:        $8
- ESP32-S3 Module:       $2.50
- Audio components:      $4.50
- Power components:      $3.50
- Enclosure:             $3
- Battery:               $3
- Misc (cables, etc):    $1.50
Subtotal Hardware:       $26

Software/Services:
- Backend hosting:       $0.10/month per device
- API costs:             $0.05/month per device
- Support:               $0.20/month per device

Total Manufacturing:     $26/unit
Monthly Operating:       $0.35/device
```

### Retail Pricing Strategy:

```
Manufacturing Cost:      $26
Margin (50%):           $26
Retail Price:           $52

Or with premium positioning:
Manufacturing Cost:      $26
Margin (100%):          $26
Marketing & Support:    $13
Retail Price:           $65-75
```

---

## 🔧 Tools & Resources Needed

### Hardware Development:

- [ ] KiCad (PCB design) - FREE
- [ ] Fusion 360 (enclosure design) - FREE for hobbyists
- [ ] Oscilloscope (testing)
- [ ] Logic analyzer (debugging)
- [ ] Soldering station

### Software Development:

- [ ] PlatformIO (ESP32 development) - FREE
- [ ] Edge Impulse account - FREE
- [ ] VS Code - FREE

### Manufacturing:

- [ ] JLCPCB account (PCB)
- [ ] Mouser/DigiKey account (components)
- [ ] 3D printer (prototypes)

---

## ✅ Legal & IP Considerations

### What We're Using (All Clear):

- ✅ ESP32 - Open hardware, no licensing
- ✅ Edge Impulse - Free for commercial use
- ✅ TensorFlow Lite - Apache 2.0 license
- ✅ Our own PCB design - Original work
- ✅ Our own firmware - Original code
- ✅ Our own enclosure - Original design
- ✅ Open-source libraries - Properly licensed

### What We're Avoiding:

- ❌ FoloToys hardware designs
- ❌ Proprietary wake word engines
- ❌ Patented technologies
- ❌ Copyrighted designs

### Recommendations:

1. File for design patents on our enclosure
2. Trademark "SagaToy" brand (www.sagatoy.com)
3. Open-source our firmware (builds community)
4. Keep hardware design proprietary initially

---

## 🎯 Next Steps

### Immediate Actions:

1. **Order Development Kit:**

   - ESP32-S3-DevKitC-1
   - INMP441 microphone
   - MAX98357A amplifier
   - Speaker
   - Total: ~$30

2. **Set Up Development Environment:**

   - Install PlatformIO
   - Create Edge Impulse account
   - Set up audio testing

3. **Start Wake Word Training:**

   - Record "Hej Saga" samples
   - Train initial model
   - Test on ESP32

4. **Design First PCB:**
   - Create schematic in KiCad
   - Layout basic board
   - Order prototype

### Timeline:

- **Week 1-2:** Development kit testing
- **Week 3-4:** Wake word model training
- **Week 5-6:** PCB design
- **Week 7-8:** Firmware development
- **Week 9-10:** Integration testing
- **Week 11-12:** First prototype complete

---

## 📞 Support & Resources

### Communities:

- ESP32 Forum
- Edge Impulse Community
- r/embedded
- Hackaday.io

### Suppliers:

- **PCB:** JLCPCB, PCBWay
- **Components:** Mouser, DigiKey, LCSC
- **Enclosures:** Xometry, Protolabs

### Documentation:

- ESP32-S3 Datasheet
- Edge Impulse Documentation
- I2S Audio Guide
- Battery Management Guide

---

## 🎉 Conclusion

This hardware solution is:

- ✅ **Completely independent** - No IP conflicts
- ✅ **Cost-effective** - ~$26/unit at scale
- ✅ **Manufacturable** - Standard components
- ✅ **Scalable** - From prototype to mass production
- ✅ **Open** - Can open-source firmware
- ✅ **Secure** - Privacy-focused design
- ✅ **Child-safe** - Designed for kids 3-10

**Ready to start building!** 🚀
