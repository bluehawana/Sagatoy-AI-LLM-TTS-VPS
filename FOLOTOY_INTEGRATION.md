# 🐙 FoloToy Octopus Integration Guide

## Overview

This guide explains how to use FoloToy Octopus hardware with ToToyAI backend.

---

## 🔗 FoloToy Resources

### Official Repositories:

- **Server (Self-Hosting):** https://github.com/FoloToy/folotoy-server-self-hosting
- **Documentation:** https://docs.folotoy.com/
- **Firmware (if open):** Check their GitHub

### Key Information Needed:

- [ ] MQTT topic structure
- [ ] Audio format (sample rate, encoding)
- [ ] Message protocol (JSON? Binary?)
- [ ] Authentication method

---

## 🏗️ Architecture: FoloToy + ToToyAI

```
┌─────────────────────────────────────────────────────────────┐
│                        Your VPS                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Mosquitto  │    │   FoloToy    │    │   ToToyAI    │  │
│  │   MQTT       │◄──▶│   Protocol   │◄──▶│   Backend    │  │
│  │   Broker     │    │   Handler    │    │   (FastAPI)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         ▲                                       │           │
│         │                                       ▼           │
│         │                              ┌──────────────┐    │
│         │                              │   External   │    │
│         │                              │   APIs       │    │
│         │                              │  (Groq,Azure)│    │
│         │                              └──────────────┘    │
└─────────│───────────────────────────────────────────────────┘
          │
          │ MQTT over TLS
          │
┌─────────▼─────────┐
│   FoloToy         │
│   Octopus         │
│   (Original FW)   │
└───────────────────┘
```

---

## 📡 FoloToy MQTT Protocol (Research Needed)

### Typical MQTT Topics (Guessed):

```
folotoy/{device_id}/audio/upload    # Device sends audio
folotoy/{device_id}/audio/download  # Server sends audio
folotoy/{device_id}/status          # Device status
folotoy/{device_id}/config          # Configuration
folotoy/{device_id}/command         # Commands to device
```

### Audio Format (Likely):

```
Sample Rate: 16000 Hz (common for speech)
Channels: 1 (mono)
Encoding: PCM 16-bit or Opus
Format: WAV or raw PCM
```

### Message Format (Likely JSON):

```json
{
  "device_id": "octopus_12345",
  "type": "audio",
  "role": 1,
  "timestamp": 1234567890,
  "data": "<base64 encoded audio>"
}
```

---

## 🛠️ Implementation Steps

### Step 1: Set Up MQTT Broker

```bash
# On your VPS (Ubuntu/Debian)
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Configure Mosquitto
sudo nano /etc/mosquitto/mosquitto.conf
```

**mosquitto.conf:**

```
listener 1883
listener 8883
certfile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
keyfile /etc/letsencrypt/live/yourdomain.com/privkey.pem
allow_anonymous false
password_file /etc/mosquitto/passwd
```

### Step 2: Create MQTT Handler (Python)

```python
# mqtt_handler.py
import paho.mqtt.client as mqtt
import json
import base64
from totoyai.services import stt, llm, tts

MQTT_BROKER = "your-server.com"
MQTT_PORT = 8883

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker: {rc}")
    client.subscribe("folotoy/+/audio/upload")

def on_message(client, userdata, msg):
    """Handle incoming audio from Octopus"""
    topic = msg.topic
    device_id = topic.split("/")[1]

    # Decode audio
    payload = json.loads(msg.payload)
    audio_data = base64.b64decode(payload["data"])

    # Process with ToToyAI
    # 1. STT: Audio → Text
    text = stt.transcribe(audio_data)

    # 2. LLM: Text → Response
    response = llm.generate(text)

    # 3. TTS: Response → Audio
    audio_response = tts.synthesize(response)

    # 4. Send back to device
    response_payload = {
        "type": "audio",
        "data": base64.b64encode(audio_response).decode()
    }
    client.publish(
        f"folotoy/{device_id}/audio/download",
        json.dumps(response_payload)
    )

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
```

### Step 3: Configure Octopus

Using FoloToy app or web interface:

1. Open device settings
2. Change server URL to your MQTT broker
3. Save and restart device

---

## 🔍 Reverse Engineering FoloToy Protocol

### Method 1: Wireshark Capture

1. Connect Octopus to your WiFi
2. Run Wireshark on same network
3. Capture MQTT traffic
4. Analyze message format

### Method 2: Study Their Server Code

```bash
git clone https://github.com/FoloToy/folotoy-server-self-hosting
# Read the code to understand protocol
```

### Method 3: Ask Community

- FoloToy Discord/Forum
- GitHub Issues
- Reddit r/esp32

---

## 🎤 Adding Voice Wake Word (Custom Firmware)

To add voice wake word, we need custom firmware:

### Option 1: Modify FoloToy Firmware (if open source)

- Add wake word detection before button check
- Keep rest of their code

### Option 2: Write New Firmware

- ESP-IDF or Arduino
- Full control but more work

### Wake Word Integration:

```cpp
// Pseudo-code for ESP32 firmware
void loop() {
    // Always listen for wake word
    if (detectWakeWord("hej toy")) {
        // Start recording
        startRecording();

        // Wait for silence (end of speech)
        waitForSilence();

        // Send audio to server
        sendAudioToServer();

        // Play response
        playResponse();
    }
}
```

---

## 📊 Comparison: Protocol vs Custom Firmware

| Aspect              | Use FoloToy Protocol | Custom Firmware    |
| ------------------- | -------------------- | ------------------ |
| **Time to MVP**     | 1-2 weeks            | 3-4 weeks          |
| **Risk**            | Low                  | Medium (can brick) |
| **Voice Wake Word** | ❌ No                | ✅ Yes             |
| **Full Control**    | ❌ Limited           | ✅ Yes             |
| **Reversible**      | ✅ Yes               | ⚠️ Maybe           |

---

## 🎯 Recommended Path

### Week 1-2: Quick Win

1. Clone FoloToy server repo
2. Study their protocol
3. Implement MQTT handler
4. Test with Octopus

### Week 3-4: Voice Wake Word

1. Buy ESP32-S3 dev board
2. Build custom firmware with wake word
3. Test on dev board
4. Port to Octopus (or design own PCB)

---

## 📚 Resources

### FoloToy:

- https://github.com/FoloToy/folotoy-server-self-hosting
- https://docs.folotoy.com/

### MQTT:

- https://mosquitto.org/
- https://pypi.org/project/paho-mqtt/

### ESP32 Audio:

- https://docs.espressif.com/projects/esp-adf/en/latest/
- https://github.com/espressif/esp-adf

### Wake Word:

- https://edgeimpulse.com/
- https://github.com/dscripka/openWakeWord

---

## ✅ Next Steps

1. [ ] Clone FoloToy server repo
2. [ ] Read their code to understand protocol
3. [ ] Set up local MQTT broker for testing
4. [ ] Capture traffic from Octopus
5. [ ] Implement ToToyAI MQTT handler
6. [ ] Test end-to-end

Let's start! 🚀
