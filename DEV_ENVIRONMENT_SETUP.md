# 🛠️ Development Environment Setup

Set this up while waiting for hardware!

---

## 📋 Overview

| Tool             | Purpose         | Install Time |
| ---------------- | --------------- | ------------ |
| VS Code          | IDE             | 5 min        |
| ESP-IDF          | ESP32 SDK       | 30 min       |
| PlatformIO       | Alternative SDK | 10 min       |
| Git              | Version control | 5 min        |
| Python 3.11      | Scripts, tools  | 10 min       |
| Edge Impulse CLI | Wake word       | 5 min        |
| PulseView        | Logic analyzer  | 5 min        |

---

## 1️⃣ Install VS Code

### Windows:

```powershell
# Option A: Download from website
# https://code.visualstudio.com/download

# Option B: Using winget
winget install Microsoft.VisualStudioCode
```

### Recommended Extensions:

Open VS Code, press `Ctrl+Shift+X`, search and install:

- **C/C++** (Microsoft)
- **PlatformIO IDE** (PlatformIO)
- **ESP-IDF** (Espressif)
- **Python** (Microsoft)
- **GitLens** (GitKraken)

---

## 2️⃣ Install Python 3.11+

### Windows:

```powershell
# Option A: Download from python.org
# https://www.python.org/downloads/

# Option B: Using winget
winget install Python.Python.3.11

# Verify installation
python --version
pip --version
```

**Important:** Check "Add Python to PATH" during installation!

---

## 3️⃣ Install Git

### Windows:

```powershell
# Option A: Download from git-scm.com
# https://git-scm.com/download/win

# Option B: Using winget
winget install Git.Git

# Verify
git --version

# Configure
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## 4️⃣ Install ESP-IDF (Espressif IoT Development Framework)

This is the official SDK for ESP32. Two options:

### Option A: ESP-IDF Extension for VS Code (Recommended)

1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions)
3. Search "ESP-IDF"
4. Install "ESP-IDF" by Espressif Systems
5. Press `Ctrl+Shift+P` → "ESP-IDF: Configure ESP-IDF Extension"
6. Select "Express" setup
7. Choose ESP-IDF version: **v5.1** or latest
8. Wait for download (~10-15 min)

### Option B: Manual Installation

```powershell
# Create directory
mkdir C:\esp
cd C:\esp

# Clone ESP-IDF
git clone -b v5.1.2 --recursive https://github.com/espressif/esp-idf.git

# Run installer
cd esp-idf
.\install.ps1 esp32s3

# Set up environment (run each time)
.\export.ps1
```

### Verify ESP-IDF:

```powershell
# In VS Code terminal or PowerShell
idf.py --version
```

---

## 5️⃣ Install PlatformIO (Alternative/Easier)

PlatformIO is easier than ESP-IDF for beginners:

### In VS Code:

1. Press `Ctrl+Shift+X`
2. Search "PlatformIO IDE"
3. Install
4. Restart VS Code
5. Click PlatformIO icon in sidebar

### Create Test Project:

1. PlatformIO Home → New Project
2. Name: "totoyai-test"
3. Board: "Espressif ESP32-S3-DevKitC-1"
4. Framework: "ESP-IDF" or "Arduino"
5. Create

---

## 6️⃣ Install Edge Impulse CLI

For wake word model training and deployment:

### Prerequisites:

```powershell
# Install Node.js first
winget install OpenJS.NodeJS.LTS

# Verify
node --version
npm --version
```

### Install Edge Impulse:

```powershell
npm install -g edge-impulse-cli

# Verify
edge-impulse-daemon --version
```

### Create Account:

1. Go to https://studio.edgeimpulse.com/
2. Sign up (free)
3. Create project: "SagaToy Wake Word"

---

## 7️⃣ Install PulseView (Logic Analyzer Software)

For debugging I2S signals when hardware arrives:

### Windows:

1. Download from: https://sigrok.org/wiki/Downloads
2. Get "PulseView" for Windows (64-bit)
3. Install
4. Will auto-detect logic analyzer when connected

---

## 8️⃣ Install USB Drivers

ESP32-S3 DevKit uses built-in USB, but install drivers just in case:

### CP210x Driver (Common):

1. Download: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
2. Install CP210x Universal Windows Driver

### FTDI Driver (Backup):

1. Download: https://ftdichip.com/drivers/vcp-drivers/
2. Install if needed

---

## 🧪 Test Your Setup

### Test 1: ESP-IDF Hello World

```powershell
# Create project directory
mkdir D:\projects\totoyai-firmware
cd D:\projects\totoyai-firmware

# Copy example (if using ESP-IDF directly)
# Or create via VS Code ESP-IDF extension
```

In VS Code with ESP-IDF extension:

1. `Ctrl+Shift+P` → "ESP-IDF: New Project"
2. Select "hello_world" template
3. Choose ESP32-S3 target
4. Build: `Ctrl+Shift+P` → "ESP-IDF: Build"

### Test 2: PlatformIO Blink

Create `platformio.ini`:

```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200
```

Create `src/main.cpp`:

```cpp
#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.println("SagaToy Starting...");
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("LED ON");
    delay(1000);

    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED OFF");
    delay(1000);
}
```

Build: Click PlatformIO checkmark icon

---

## 📁 Project Structure

Create this folder structure:

```
D:\projects\totoyai\
├── backend\              # Already exists (Python FastAPI)
├── firmware\             # NEW: ESP32 code
│   ├── platformio.ini
│   ├── src\
│   │   └── main.cpp
│   ├── lib\
│   │   └── edge_impulse\  # Wake word model
│   └── include\
├── hardware\             # NEW: PCB designs (later)
├── docs\                 # Documentation
└── tools\                # Helper scripts
```

---

## 🎤 Prepare for Wake Word Training

### While Waiting for Hardware:

1. **Create Edge Impulse Project:**

   - Go to https://studio.edgeimpulse.com/
   - New Project → "SagaToy Wake Word"
   - Select "Audio" as data type

2. **Plan Data Collection:**

   - Need 200+ "Hej Saga" samples (Swedish)
   - Need 200+ "Hello Saga" samples (English)
   - Need 500+ background noise samples
   - Need 200+ other words (negative samples)

3. **Record Samples on Phone:**
   - Use Edge Impulse mobile app
   - Or record WAV files and upload
   - 16kHz sample rate, mono

### Sample Recording Script (Python):

```python
# record_samples.py
import sounddevice as sd
import soundfile as sf
import os
from datetime import datetime

SAMPLE_RATE = 16000
DURATION = 2  # seconds
OUTPUT_DIR = "wake_word_samples"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def record_sample(label):
    print(f"Recording '{label}' in 3 seconds...")
    sd.sleep(3000)
    print("Recording...")

    audio = sd.rec(int(DURATION * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=1)
    sd.wait()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/{label}_{timestamp}.wav"
    sf.write(filename, audio, SAMPLE_RATE)
    print(f"Saved: {filename}")

# Record samples
for i in range(10):
    record_sample("hej_toy")
    input("Press Enter for next sample...")
```

Install dependencies:

```powershell
pip install sounddevice soundfile numpy
```

---

## 🔧 ESP32 Audio Test Code (Ready for Hardware)

Save this for when hardware arrives:

### `src/audio_test.cpp`:

```cpp
#include <Arduino.h>
#include <driver/i2s.h>

// I2S pins for ESP32-S3
#define I2S_MIC_SCK     5
#define I2S_MIC_WS      6
#define I2S_MIC_SD      4

#define I2S_SPK_BCK     15
#define I2S_SPK_LRC     16
#define I2S_SPK_DIN     17

#define SAMPLE_RATE     16000
#define BUFFER_SIZE     1024

void setup_i2s_mic() {
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = BUFFER_SIZE,
        .use_apll = false
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_MIC_SCK,
        .ws_io_num = I2S_MIC_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = I2S_MIC_SD
    };

    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);
}

void setup() {
    Serial.begin(115200);
    Serial.println("SagaToy Audio Test");

    setup_i2s_mic();
    Serial.println("I2S Microphone initialized");
}

void loop() {
    int16_t samples[BUFFER_SIZE];
    size_t bytes_read;

    i2s_read(I2S_NUM_0, samples, sizeof(samples), &bytes_read, portMAX_DELAY);

    // Calculate audio level
    int32_t sum = 0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
        sum += abs(samples[i]);
    }
    int avg = sum / BUFFER_SIZE;

    // Print audio level bar
    Serial.print("Level: ");
    for (int i = 0; i < avg / 100; i++) {
        Serial.print("█");
    }
    Serial.println();

    delay(100);
}
```

---

## ✅ Setup Checklist

### Software:

- [ ] VS Code installed
- [ ] Python 3.11+ installed
- [ ] Git installed and configured
- [ ] ESP-IDF extension installed (or PlatformIO)
- [ ] Edge Impulse CLI installed
- [ ] Edge Impulse account created
- [ ] PulseView installed

### Project:

- [ ] Firmware folder created
- [ ] Test project builds successfully
- [ ] Sample recording script works

### Accounts:

- [ ] Edge Impulse (wake word training)
- [ ] GitHub (version control)
- [ ] Hetzner/DigitalOcean (VPS - later)

---

## 🚀 Next Steps

1. **Today:** Install all software above
2. **Today:** Create Edge Impulse project
3. **Tomorrow:** Start recording wake word samples
4. **Day 3-4:** Hardware arrives!
5. **Day 4-5:** First audio test on ESP32-S3

---

## 🆘 Troubleshooting

### ESP-IDF not found:

```powershell
# Run export script
cd C:\esp\esp-idf
.\export.ps1
```

### PlatformIO build fails:

- Check board selection matches your hardware
- Update platform: `pio pkg update`

### USB not detected:

- Install CP210x drivers
- Try different USB port
- Check cable (some are charge-only)

### Edge Impulse CLI error:

```powershell
# Reinstall
npm uninstall -g edge-impulse-cli
npm install -g edge-impulse-cli
```

---

Ready to set up? Start with VS Code and work down the list! 🛠️
