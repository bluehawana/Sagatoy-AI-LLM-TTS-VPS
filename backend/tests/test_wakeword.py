"""Test wake word detection and toy interaction.

Updated for SagaToy branding (www.sagatoy.com)
Wake words: "Hej Saga", "Hello Saga", "Hey Saga"
"""

import asyncio
from sagatoyai.services.gemini import gemini_service
from sagatoyai.services.tts import tts_service


# SagaToy wake words
WAKE_WORDS = [
    "hej saga",      # Swedish primary
    "hello saga",    # English primary
    "hey saga",      # English alternative
]


async def detect_wake_word(text: str) -> bool:
    """Detect if wake word is present in text.

    Wake words: "Hej Saga", "Hello Saga", "Hey Saga"
    """
    text_lower = text.lower()

    for wake_word in WAKE_WORDS:
        if wake_word in text_lower:
            return True
    return False


async def toy_interaction(user_input: str, language: str = "sv"):
    """Simulate toy interaction with wake word detection."""

    print(f"\n🎤 User said: '{user_input}'")

    # Check for wake word
    if await detect_wake_word(user_input):
        print("✅ Wake word detected! Toy is now listening...")

        # Generate response using Gemini
        print("🤖 Generating response...")
        response_text, intent = await gemini_service.generate_conversation_response(
            user_input=user_input,
            language=language
        )

        print(f"💬 Toy responds: '{response_text}'")
        print(f"🎯 Detected intent: {intent}")

        # Convert to speech
        print("🔊 Converting to speech...")
        audio_bytes = await tts_service.synthesize_to_bytes(response_text, language)

        # Save audio
        output_file = "test_response.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        print(f"✅ Audio saved to: {output_file}")
        print(f"📊 Audio size: {len(audio_bytes) / 1024:.1f} KB")

        return response_text, output_file
    else:
        print("❌ No wake word detected. Toy is sleeping...")
        return None, None


async def main():
    """Test wake word detection."""

    print("=" * 60)
    print("🧸 SagaToy - Wake Word Detection Test")
    print("   Domain: www.sagatoy.com")
    print("   Wake words: Hej Saga, Hello Saga, Hey Saga")
    print("=" * 60)

    # Test cases
    test_inputs = [
        ("Hej Saga, kan du berätta en saga?",
         "sv", True),      # Swedish - should wake
        ("Vad är klockan?", "sv", False),                        # No wake word
        ("Hello Saga, what's the weather like?",
         "en", True),   # English - should wake
        # English alt - should wake
        ("Hey Saga, tell me a story!", "en", True),
        ("Random text without wake word", "en", False),          # No wake word
        # Lowercase - should wake
        ("hej saga, hur mår du idag?", "sv", True),
    ]

    print("\n📋 Testing wake word detection:\n")

    passed = 0
    failed = 0

    for user_input, language, expected in test_inputs:
        detected = await detect_wake_word(user_input)
        status = "✅" if detected == expected else "❌"

        if detected == expected:
            passed += 1
        else:
            failed += 1

        print(
            f"{status} '{user_input[:40]}...' → Detected: {detected}, Expected: {expected}")

    print(f"\n📊 Results: {passed}/{len(test_inputs)} tests passed")

    # Now test full interaction with one example
    print("\n" + "=" * 60)
    print("🎤 Testing full interaction with Gemini + TTS:")
    print("=" * 60)

    await toy_interaction("Hej Saga, kan du berätta en kort saga om en kanin?", language="sv")

    print("\n" + "=" * 60)
    print("✅ SagaToy wake word test complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
