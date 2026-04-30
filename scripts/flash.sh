#!/bin/bash
# Sagatoy Firmware Flash Script
# For Mac/Windows/Linux - Just double click!

echo "========================================"
echo "  Sagatoy Firmware Flasher"
echo "========================================"
echo ""

# Check if esptool is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python first."
    echo "   Download: https://www.python.org/downloads/"
    exit 1
fi

# Install esptool if needed
echo "📦 Installing esptool..."
pip3 install esptool --quiet

# Find serial port
echo ""
echo "Looking for Sagatoy toy..."
SERIAL_PORT=""
if [ -d "/dev/tty.usbserial"* ]; then
    # macOS
    SERIAL_PORT=$(ls /dev/tty.usbserial* | head -1)
elif [ -d "/dev/ttyUSB"* ]; then
    # Linux
    SERIAL_PORT=$(ls /dev/ttyUSB* | head -1)
elif [ -d "COM"* ]; then
    # Windows
    SERIAL_PORT=$(ls COM* | head -1)
fi

if [ -z "$SERIAL_PORT" ]; then
    echo "❌ No toy found!"
    echo ""
    echo "Please:"
    echo "1. Connect the toy via USB"
    echo "2. Turn on the toy"
    echo "3. Run this script again"
    exit 1
fi

echo "✅ Found: $SERIAL_PORT"
echo ""

# Check if firmware exists
if [ ! -f "firmware.bin" ]; then
    echo "📥 Downloading latest firmware..."
    curl -L -o firmware.bin "https://github.com/sagatoy/firmware/releases/latest/download/sagatoy.bin"
fi

echo "🚀 Flashing firmware..."
echo ""

# Flash
python3 -m esptool --chip esp32 --port $SERIAL_PORT --baud 115200 \
    --before default_reset --after hard_reset write_flash -z \
    --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 firmware.bin

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  ✅ FLASH COMPLETE!"
    echo "========================================"
    echo ""
    echo "Your Sagatoy is ready!"
    echo "Power it on and start talking!"
else
    echo ""
    echo "❌ Flash failed. Try again."
fi