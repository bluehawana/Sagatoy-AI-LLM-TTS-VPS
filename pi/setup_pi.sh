#!/bin/bash
# SagaToy Pi Setup Script
# Run once on a fresh Raspberry Pi OS Bookworm (64-bit) installation.
# Usage: bash setup_pi.sh

set -euo pipefail
log() { echo "[$(date +%H:%M:%S)] $*"; }

log "=== SagaToy Pi Setup ==="
log "Phase A: System packages"

sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    python3-pip python3-venv \
    portaudio19-dev \
    ffmpeg \
    git \
    alsa-utils \
    libasound2-dev \
    build-essential \
    cmake

# ---------------------------------------------------------------------------
log "Phase B: Directory structure"
# ---------------------------------------------------------------------------
SAGATOY_HOME=/home/pi/sagatoy
mkdir -p "$SAGATOY_HOME"/{models,voices,logs,content/{stories/{sv,da,no,fi,en,zh},songs/{sv,da,no,fi,en,zh},poems/{sv,da,no,fi,en,zh}}}

# ---------------------------------------------------------------------------
log "Phase C: Python virtual environment"
# ---------------------------------------------------------------------------
python3 -m venv "$SAGATOY_HOME/venv"
source "$SAGATOY_HOME/venv/bin/activate"

pip install --upgrade pip
pip install \
    httpx \
    pyaudio \
    RPi.GPIO \
    pyyaml \
    edge-tts \
    qrcode[pil]

# ---------------------------------------------------------------------------
log "Phase D: whisper.cpp (local STT)"
# ---------------------------------------------------------------------------
cd /home/pi
if [ ! -d "whisper.cpp" ]; then
    git clone https://github.com/ggerganov/whisper.cpp.git
fi
cd whisper.cpp
make -j$(nproc)
sudo cp main /usr/local/bin/whisper-cpp
log "whisper.cpp compiled"

# Download medium model (~1.5GB) — good Nordic language accuracy
MODEL_DIR="$SAGATOY_HOME/models"
if [ ! -f "$MODEL_DIR/ggml-medium.bin" ]; then
    log "Downloading Whisper medium model (~1.5GB)..."
    bash models/download-ggml-model.sh medium
    cp models/ggml-medium.bin "$MODEL_DIR/"
fi

# ---------------------------------------------------------------------------
log "Phase E: Ollama + phi3:mini (offline LLM fallback)"
# ---------------------------------------------------------------------------
if ! command -v ollama &>/dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi
# Start Ollama in background, pull model
ollama serve &>/dev/null &
sleep 5
ollama pull phi3:mini
log "phi3:mini pulled"

# ---------------------------------------------------------------------------
log "Phase F: Piper TTS voices"
# ---------------------------------------------------------------------------
PIPER_DIR="$SAGATOY_HOME/venv"
pip install piper-tts

VOICES_DIR="$SAGATOY_HOME/voices"
declare -A VOICE_URLS=(
    ["sv_SE-nst-medium"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx"
    ["sv_SE-nst-medium.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"
    ["da_DK-talesyntese-medium"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx"
    ["da_DK-talesyntese-medium.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"
    ["nb_NO-talesyntese-medium"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/no/nb_NO/talesyntese/medium/nb_NO-talesyntese-medium.onnx"
    ["nb_NO-talesyntese-medium.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/no/nb_NO/talesyntese/medium/nb_NO-talesyntese-medium.onnx.json"
    ["fi_FI-harri-medium"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/fi/fi_FI/harri/medium/fi_FI-harri-medium.onnx"
    ["fi_FI-harri-medium.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/fi/fi_FI/harri/medium/fi_FI-harri-medium.onnx.json"
    ["en_GB-alba-medium"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx"
    ["en_GB-alba-medium.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"
)

for name in "${!VOICE_URLS[@]}"; do
    out="$VOICES_DIR/$name"
    if [[ "$name" == *.json ]]; then
        out="$VOICES_DIR/$name"
    else
        out="$VOICES_DIR/$name.onnx"
    fi
    if [ ! -f "$out" ]; then
        log "Downloading $name..."
        wget -q "${VOICE_URLS[$name]}" -O "$out"
    fi
done

# ---------------------------------------------------------------------------
log "Phase G: Copy SagaToy code"
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/sagatoy_voice_loop.py" "$SAGATOY_HOME/"
cp "$SCRIPT_DIR/sagatoy_stress_test.py" "$SAGATOY_HOME/"
cp "$SCRIPT_DIR/config.yaml" "$SAGATOY_HOME/"

# ---------------------------------------------------------------------------
log "Phase H: Systemd service"
# ---------------------------------------------------------------------------
sudo tee /etc/systemd/system/sagatoy.service > /dev/null <<EOF
[Unit]
Description=SagaToy Voice Loop
After=network-online.target sound.target
Wants=network-online.target

[Service]
ExecStart=/home/pi/sagatoy/venv/bin/python3 /home/pi/sagatoy/sagatoy_voice_loop.py
WorkingDirectory=/home/pi/sagatoy
User=pi
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable sagatoy

# ---------------------------------------------------------------------------
log "Phase I: Audio output — force 3.5mm jack"
# ---------------------------------------------------------------------------
sudo raspi-config nonint do_audio 1   # 1 = 3.5mm jack
amixer cset numid=3 1 2>/dev/null || true
amixer set Master 90% 2>/dev/null || true

# ---------------------------------------------------------------------------
log ""
log "=== Setup complete ==="
log ""
log "Next steps:"
log "  1. Copy config.yaml to config.local.yaml and fill in:"
log "       llm.cloud_api_key (z.ai GLM-4 Flash API key)"
log "       device.id (unique per toy)"
log "  2. Add some story MP3s to $SAGATOY_HOME/content/stories/<lang>/"
log "  3. Run the stress test:"
log "       cd $SAGATOY_HOME"
log "       source venv/bin/activate"
log "       python3 sagatoy_stress_test.py --cycles 50 --languages sv,da,no,fi,en,zh"
log "  4. When all tests pass, start the service:"
log "       sudo systemctl start sagatoy"
log "  5. Only then physically install Pi into the toy shell."
log ""
