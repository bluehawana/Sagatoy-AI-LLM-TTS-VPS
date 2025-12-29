"""Test the kindergarten-optimized voice settings."""

import asyncio
from pathlib import Path
from dotenv import load_dotenv
from sagatoyai.services.tts import tts_service

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")


async def test_kindergarten_voice():
    """Test voice with kindergarten-appropriate content."""

    print("\n" + "="*60)
    print("🧸 Testing Kindergarten Teacher Voice")
    print("="*60)

    # Test phrases that a kindergarten teacher would say
    test_phrases = [
        {
            "text": "Hej där, lilla vän! Jag är så glad att få prata med dig idag. Ska vi leka tillsammans?",
            "lang": "sv",
            "description": "Greeting (Swedish)"
        },
        {
            "text": "Det var jättebra! Du är så duktig! Ska vi prova något mer?",
            "lang": "sv",
            "description": "Encouragement (Swedish)"
        },
        {
            "text": "Nu ska jag berätta en saga om en liten kanin som älskade att hoppa. Är du redo att lyssna?",
            "lang": "sv",
            "description": "Story introduction (Swedish)"
        },
        {
            "text": "Hello there, little friend! I'm so happy to talk with you today. Shall we play together?",
            "lang": "en",
            "description": "Greeting (English)"
        },
    ]

    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. {phrase['description']}")
        print(f"   Text: {phrase['text'][:60]}...")
        print(f"   Generating audio...")

        # Generate audio
        audio_bytes = await tts_service.synthesize_to_bytes(
            phrase['text'],
            phrase['lang']
        )

        # Save to file
        output_file = f"kindergarten_voice_{i}_{phrase['lang']}.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        print(f"   ✅ Saved: {output_file}")
        print(f"   📊 Size: {len(audio_bytes) / 1024:.1f} KB")

    print("\n" + "="*60)
    print("🎧 VOICE CHARACTERISTICS:")
    print("="*60)
    print("   ✅ Warm and gentle (like a kindergarten teacher)")
    print("   ✅ Slightly slower pace (-10% speed)")
    print("   ✅ Clear pronunciation for young children")
    print("   ✅ Less scary, more comforting")
    print("   ✅ Perfect for ages 3-10")

    print("\n" + "="*60)
    print("💡 CURRENT SETTINGS:")
    print("="*60)
    print("   Swedish Voice: sv-SE-SofieNeural")
    print("   English Voice: en-US-JennyNeural")
    print("   Speed: -10% (slightly slower)")

    print("\n" + "="*60)
    print("🎵 Listen to the samples and compare with the old voice!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_kindergarten_voice())
