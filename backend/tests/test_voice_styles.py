"""Test different voice styles and speeds for child-friendly output."""

import asyncio
import edge_tts
from pathlib import Path


async def test_voice_with_style(voice_name: str, text: str, rate: str, output_file: str):
    """Test a voice with specific rate."""
    try:
        # Rate can be: x-slow, slow, medium, fast, x-fast
        # Or percentage: -50%, -25%, +0%, +25%, +50%
        communicate = edge_tts.Communicate(text, voice_name, rate=rate)
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Test voice variations for child-friendliness."""

    test_text = "Hej där, lilla vän! Ska vi leka tillsammans? Det blir så roligt!"

    print("\n" + "="*60)
    print("🎤 Testing Voice Styles for Children")
    print("="*60)

    # Create output directory
    output_dir = Path("voice_styles")
    output_dir.mkdir(exist_ok=True)

    # Test configurations
    voices = [
        "sv-SE-SofieNeural",    # Female, warm
        "sv-SE-HilleviNeural",  # Female, alternative
        "sv-SE-MattiasNeural",  # Male
    ]

    rates = [
        ("-10%", "slightly_slower"),
        ("+0%", "normal"),
        ("+10%", "slightly_faster"),
    ]

    print("\n🎵 Generating voice samples with different speeds...\n")

    samples = []

    for voice in voices:
        voice_short = voice.split("-")[-1].replace("Neural", "")
        print(f"\n📢 Voice: {voice_short}")

        for rate_value, rate_name in rates:
            print(f"   ⚡ Speed: {rate_name} ({rate_value})")

            output_file = output_dir / f"{voice_short}_{rate_name}.mp3"
            success = await test_voice_with_style(voice, test_text, rate_value, str(output_file))

            if success:
                print(f"      ✅ Saved: {output_file.name}")
                samples.append({
                    "voice": voice_short,
                    "rate": rate_name,
                    "file": output_file
                })

            await asyncio.sleep(0.3)

    # Print recommendations
    print("\n" + "="*60)
    print("🌟 RECOMMENDATIONS FOR CHILDREN'S TOY")
    print("="*60)

    print("\n👧 SOFIE (Female - Warm & Friendly):")
    print("   ⭐ BEST: Sofie_slightly_slower.mp3")
    print("      - Slower pace is easier for children to understand")
    print("      - Warm, gentle tone")
    print("      - Less scary, more comforting")

    print("\n👧 HILLEVI (Female - Clear & Bright):")
    print("   ⭐ GOOD: Hillevi_normal.mp3")
    print("      - Clear pronunciation")
    print("      - Bright, cheerful tone")

    print("\n👦 MATTIAS (Male - Friendly):")
    print("   ⭐ GOOD: Mattias_slightly_slower.mp3")
    print("      - Gentle male voice")
    print("      - Good for variety")

    print("\n" + "="*60)
    print("💡 TIPS TO MAKE VOICE LESS SCARY:")
    print("="*60)
    print("   1. Use SLOWER speed (-10% to -20%)")
    print("   2. Choose FEMALE voices (perceived as warmer)")
    print("   3. Keep sentences SHORT and SIMPLE")
    print("   4. Add PAUSES between sentences")
    print("   5. Use FRIENDLY words and expressions")

    print("\n📝 RECOMMENDED SETTINGS FOR .env:")
    print("   TTS_VOICE=sv-SE-SofieNeural")
    print("   TTS_RATE=-10%  (slightly slower)")

    print("\n🎧 Listen to all samples in the 'voice_styles' folder!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
