# 🛒 ToToyAI Hardware - Complete Shopping List

## 🎯 MVP Strategy: Use FoloToy Octopus First!

**You already have 2x FoloToy Octopus kits!** These are perfect for MVP:

- ✅ ESP32-S3 (same chip we'd use)
- ✅ MEMS microphone (built-in)
- ✅ Speaker + amplifier (built-in)
- ✅ Battery + charging (built-in)
- ✅ Cute form factor (ready for demo)

**For MVP:** No hardware purchase needed! Just flash custom firmware or use MQTT protocol.

**For custom hardware later:** See shopping list below.

---

## 🇸🇪 Sweden/EU Focused - Fast Delivery (2-3 days)

---

## 🎯 Complete Prototype Kit (For Custom Hardware)

### Option A: Mouser.se (Professional, Fast) - EXACT PART NUMBERS

| #   | Component               | Mouser Part #         | Price (SEK) | Notes                          |
| --- | ----------------------- | --------------------- | ----------- | ------------------------------ |
| 1   | ESP32-S3-DevKitC-1-N8R8 | 356-ESP32S3DVKTC1N8R8 | ~180        | Main processor                 |
| 2   | ESP32-C3-DevKitM-1      | 356-ESP32C3DEVKITM1   | ~90         | Wake word processor (optional) |
| 3   | MAX98357A Breakout      | 485-3006              | ~85         | Adafruit I2S amp board         |
| 4   | I2S MEMS Mic SPH0645    | 485-3421              | ~75         | Adafruit mic breakout          |
| 5   | Speaker 3W 4Ω 40mm      | 665-AS04008PS-R       | ~45         | PUI Audio                      |
| 6   | USB-C Cable 1m          | 485-4474              | ~40         | Adafruit                       |
| 7   | Breadboard 830 pts      | 485-64                | ~55         | Adafruit                       |
| 8   | Jumper Wires M/M 75pcs  | 485-1956              | ~25         | Adafruit                       |
| 9   | Jumper Wires M/F 40pcs  | 485-1954              | ~25         | Adafruit                       |

**Mouser.se Total: ~620 SEK** (+ shipping ~50 SEK)

**How to order:**

1. Go to mouser.se
2. Search each Mouser Part # (e.g., "356-ESP32S3DVKTC1N8R8")
3. Add to cart
4. Checkout with Swedish address

**Alternative mic (if SPH0645 unavailable):**

- ICS-43434 breakout: 485-3492 (~80 SEK)

---

### Option B: Electrokit.com (Swedish, Local)

| #   | Component             | Article # | Price (SEK) | Link                                                                        |
| --- | --------------------- | --------- | ----------- | --------------------------------------------------------------------------- |
| 1   | ESP32-S3-DevKitC-1    | 41019073  | 199         | [electrokit.com](https://www.electrokit.com/esp32-s3-devkitc-1-n8r8)        |
| 2   | Breadboard 830 points | 10160840  | 59          | [electrokit.com](https://www.electrokit.com/kopplingsdack-830-anslutningar) |
| 3   | Jumper wires M-M      | 41012686  | 39          | [electrokit.com](https://www.electrokit.com/labsladd-hane-hane-65st)        |
| 4   | Jumper wires M-F      | 41012687  | 39          | [electrokit.com](https://www.electrokit.com/labsladd-hane-hona-65st)        |
| 5   | Speaker 0.5W 8Ω 36mm  | 41003453  | 29          | [electrokit.com](https://www.electrokit.com/hogtalare-0.5w-8-ohm-o36mm)     |
| 6   | Push button           | 41000025  | 5           | [electrokit.com](https://www.electrokit.com/tryckknapp-pcb-6x6mm)           |
| 7   | LED RGB WS2812B       | 41015929  | 19          | [electrokit.com](https://www.electrokit.com/led-rgb-ws2812b-5050-smd)       |

**Electrokit Subtotal: ~389 SEK** (free shipping over 500 SEK)

**Note:** Electrokit doesn't stock INMP441 or MAX98357A modules - order from Mouser or AliExpress.

---

### Option C: Mixed Order (Best Value + Speed)

**From Electrokit (1-2 days):**
| Component | Price (SEK) |
|-----------|-------------|
| ESP32-S3-DevKitC-1 | 199 |
| Breadboard + wires | 98 |
| Speaker | 29 |
| Buttons, LEDs | 30 |
| **Subtotal** | **356** |

**From Mouser.se (2-3 days):**
| Component | Price (SEK) |
|-----------|-------------|
| INMP441 module (breakout) | ~60 |
| MAX98357A module (breakout) | ~50 |
| **Subtotal** | **~110** |

**Mixed Total: ~466 SEK + shipping**

---

## 🔋 Battery & Power (Optional for Portable)

### From Electrokit:

| Component                   | Article # | Price (SEK)      |
| --------------------------- | --------- | ---------------- |
| Li-ion 18650 3.7V 2600mAh   | 41014065  | 89               |
| 18650 Battery holder        | 41011476  | 15               |
| TP4056 USB-C charger module | -         | ~20 (AliExpress) |
| 3.3V voltage regulator      | 41011946  | 12               |

**Battery Kit: ~136 SEK**

---

## 🎤 Audio Components - Detailed

### Microphone: INMP441 (I2S Digital MEMS)

```
Why INMP441:
✅ Digital I2S output (no ADC needed)
✅ High SNR (61 dB)
✅ Low power (1.4mA)
✅ Small size (4x3x1mm)
✅ Works great with ESP32

Pinout:
- VDD → 3.3V
- GND → GND
- SD  → GPIO (I2S data)
- WS  → GPIO (I2S word select)
- SCK → GPIO (I2S clock)
- L/R → GND (left channel) or VDD (right)

Where to buy:
- Mouser: Search "INMP441" breakout board
- AliExpress: "INMP441 I2S microphone module" (~25 SEK, 2-3 weeks)
- Amazon.se: "INMP441" (~60 SEK, 3-5 days)
```

### Amplifier: MAX98357A (I2S Digital Input)

```
Why MAX98357A:
✅ I2S digital input (matches ESP32)
✅ 3.2W output power
✅ No external components needed
✅ Built-in DAC
✅ Class D efficiency

Pinout:
- VIN → 5V (or 3.3V for lower volume)
- GND → GND
- DIN → GPIO (I2S data)
- BCLK → GPIO (I2S bit clock)
- LRC → GPIO (I2S left/right clock)
- GAIN → Set gain (GND=9dB, float=12dB, VIN=15dB)
- SD → Enable (high = on)

Where to buy:
- Mouser: MAX98357A breakout ~50 SEK
- AliExpress: "MAX98357A module" ~20 SEK
- Adafruit: MAX98357A breakout (ships to EU)
```

### Speaker: 3W 4Ω (or 8Ω)

```
Specs needed:
- Power: 2-3W (matches amp)
- Impedance: 4Ω or 8Ω
- Size: 40mm diameter (fits in toy)

Options:
- Electrokit: 0.5W 8Ω 36mm (29 SEK) - quieter but works
- Mouser: 3W 4Ω 40mm speaker
- AliExpress: "3W 4ohm speaker 40mm" ~15 SEK
```

---

## 🔌 Wiring Diagram

```
ESP32-S3 DevKit Pinout for Audio:

                    ┌─────────────────┐
                    │   ESP32-S3      │
                    │   DevKitC-1     │
                    │                 │
    INMP441 ───────►│ GPIO4  (I2S_DIN)│
    (Mic Data)      │ GPIO5  (I2S_WS) │◄─── INMP441 (WS)
                    │ GPIO6  (I2S_SCK)│◄─── INMP441 (SCK)
                    │                 │
    MAX98357A ◄─────│ GPIO15 (I2S_DOUT)│
    (Amp Data)      │ GPIO16 (I2S_BCLK)│───► MAX98357A (BCLK)
                    │ GPIO17 (I2S_LRC) │───► MAX98357A (LRC)
                    │                 │
                    │ 3.3V ───────────│───► INMP441 VDD
                    │ 5V   ───────────│───► MAX98357A VIN
                    │ GND  ───────────│───► All GND
                    │                 │
                    │ GPIO48 (RGB LED)│───► WS2812B
                    │ GPIO0  (BOOT)   │───► Button (optional)
                    └─────────────────┘
```

---

## 📦 Ready-to-Order Lists

### 🚀 FAST START (2-3 days, ~500 SEK)

**Mouser.se Order:**

```
1x ESP32-S3-DevKitC-1-N8R8     180 SEK
1x INMP441 breakout board       60 SEK
1x MAX98357A breakout board     50 SEK
1x Speaker 3W 4Ω 40mm           30 SEK
1x Breadboard 830 points        40 SEK
1x Jumper wire kit              40 SEK
1x USB-C cable                  30 SEK
─────────────────────────────────────
Subtotal:                      430 SEK
Shipping:                       50 SEK
Total:                         480 SEK
```

### 💰 BUDGET (2-4 weeks, ~300 SEK)

**AliExpress Order:**

```
1x ESP32-S3-DevKitC-1          100 SEK
2x INMP441 module               50 SEK (pack of 2)
2x MAX98357A module             40 SEK (pack of 2)
2x Speaker 3W 4Ω                30 SEK
1x Breadboard + wires           40 SEK
1x TP4056 charger module        15 SEK
1x 18650 battery               25 SEK
─────────────────────────────────────
Total:                         300 SEK (free shipping)
```

### 🏆 COMPLETE KIT (All options, ~800 SEK)

**Mixed Suppliers:**

```
Mouser.se:
- ESP32-S3-DevKitC-1           180 SEK
- INMP441 breakout              60 SEK
- MAX98357A breakout            50 SEK

Electrokit:
- Breadboard + wires           100 SEK
- Speaker                       29 SEK
- Buttons, LEDs                 50 SEK
- 18650 battery + holder       104 SEK

AliExpress:
- TP4056 USB-C charger          20 SEK
- ESP32-C3 (wake word MCU)      50 SEK
- Extra INMP441 (spare)         25 SEK
─────────────────────────────────────
Total:                         668 SEK
Shipping:                      ~100 SEK
Grand Total:                   ~770 SEK
```

---

## 🔧 Alternative: All-in-One Dev Kits

### ESP32-S3-BOX-3 (Espressif Official)

```
Price: ~600 SEK
Includes:
✅ ESP32-S3 with PSRAM
✅ 2x MEMS microphones
✅ Speaker + amplifier
✅ 2.4" LCD display
✅ Touch screen
✅ Battery support
✅ Nice enclosure

Where: Mouser.se, DigiKey.se
Link: Search "ESP32-S3-BOX-3"

Pros: Everything included, ready to use
Cons: Fixed form factor, more expensive
```

### ESP32-S3-Korvo-2 (Audio Dev Kit)

```
Price: ~400 SEK
Includes:
✅ ESP32-S3
✅ 3x microphone array
✅ Speaker + amp
✅ Audio DSP
✅ SD card slot

Where: Mouser.se
Link: Search "ESP32-S3-Korvo-2"

Pros: Professional audio quality
Cons: Larger size, overkill for prototype
```

---

## ✅ Pre-Order Checklist

Before ordering, verify:

- [ ] ESP32-S3 (not ESP32 or ESP32-S2)
- [ ] INMP441 is I2S version (not analog)
- [ ] MAX98357A is I2S version
- [ ] Speaker impedance matches (4Ω or 8Ω)
- [ ] USB-C cable (not micro-USB)
- [ ] Shipping to Sweden/your country
- [ ] Delivery time acceptable

---

## 🛠️ Tools You'll Need

**Already have (probably):**

- Computer with USB port
- USB-C cable

**Nice to have:**

- Multimeter (~100 SEK)
- Soldering iron (~200 SEK) - for final assembly
- Wire strippers (~50 SEK)

**Not needed for prototype:**

- Oscilloscope
- Logic analyzer
- Hot air station

---

## 📅 Timeline After Ordering

**Day 1-3:** Components arrive (Mouser/Electrokit)
**Day 3-5:** Basic wiring and first boot
**Day 5-7:** Audio test (record/playback)
**Week 2:** Wake word integration
**Week 3:** Backend connection
**Week 4:** First working prototype!

---

## 🔗 Quick Links

### Swedish Suppliers:

- [Mouser.se](https://www.mouser.se) - Professional, fast
- [Electrokit.com](https://www.electrokit.com) - Swedish, local
- [DigiKey.se](https://www.digikey.se) - Large selection
- [m.nu](https://www.m.nu) - Maker store Stockholm

### EU Suppliers:

- [Conrad.se](https://www.conrad.se) - Germany
- [Reichelt.de](https://www.reichelt.de) - Germany
- [Farnell.com](https://www.farnell.com) - UK/EU

### Budget (Longer shipping):

- [AliExpress](https://www.aliexpress.com) - 2-4 weeks
- [Banggood](https://www.banggood.com) - 2-4 weeks

---

## 🎉 Ready to Order!

**Recommended first order: Mouser.se FAST START kit (~500 SEK)**

This gets you everything needed for a working prototype in 2-3 days!

🚀 Let's build SagaToy! 🧸
