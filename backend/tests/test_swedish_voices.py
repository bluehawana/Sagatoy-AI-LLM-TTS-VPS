"""Test different Swedish voices to find the most child-friendly one."""

import asyncio
import edge_tts
from pathlib import Path


async def test_voice(voice_name: str, text: str, output_file: str):
    """Test a specific voice."""
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"❌ Error with {voice_name}: {e}")
        return False


async def main():
    """Test all Swedish voices."""

    # Test text in Swedish
    test_text = "Hej där, lilla vän! Jag är din gosiga leksak och jag älskar att prata med dig. Ska vi leka tillsammans?"

    print("\n" + "="*60)
    print("🎤 Testing Swedish Voices for Child-Friendliness")
    print("="*60)

    # Get all available voices
    voices = await edge_tts.list_voices()

    # Filter Swedish voices
    swedish_voices = [v for v in voices if v["Locale"].startswith("sv-")]

    print(f"\n📊 Found {len(swedish_voices)} Swedish voices\n")

    # Create output directory
    output_dir = Path("voice_samples")
    output_dir.mkdir(exist_ok=True)

    voice_info = []

    for i, voice in enumerate(swedish_voices, 1):
        voice_name = voice["ShortName"]
        gender = voice["Gender"]
        locale = voice["Locale"]

        print(f"\n{i}. Testing: {voice_name}")
        print(f"   Gender: {gender}")
        print(f"   Locale: {locale}")

        # Generate sample
        output_file = output_dir / \
            f"{i:02d}_{voice_name.replace('/', '_')}.mp3"
        success = await test_voice(voice_name, test_text, str(output_file))

        if success:
            print(f"   ✅ Saved to: {output_file}")
            voice_info.append({
                "number": i,
                "name": voice_name,
                "gender": gender,
                "locale": locale,
                "file": output_file
            })

        await asyncio.sleep(0.5)  # Small delay between requests

    # Print summary
    print("\n" + "="*60)
    print("📋 Voice Summary - Recommendations for Children")
    print("="*60)

    print("\n🌟 RECOMMENDED VOICES FOR CHILDREN:\n")

    # Categorize by characteristics
    female_voices = [v for v in voice_info if v["gender"] == "Female"]
    male_voices = [v for v in voice_info if v["gender"] == "Male"]

    print("👧 Female Voices (Often warmer for children):")
    for v in female_voices:
        print(f"   {v['number']}. {v['name']}")
        print(f"      File: {v['file'].name}")

    print("\n👦 Male Voices:")
    for v in male_voices:
        print(f"   {v['number']}. {v['name']}")
        print(f"      File: {v['file'].name}")

    print("\n" + "="*60)
    print("🎧 Listen to the samples and choose your favorite!")
    print("="*60)

    print("\n💡 TIPS FOR CHOOSING:")
    print("   - Female voices are often perceived as warmer")
    print("   - Look for voices with 'Neural' in the name (more natural)")
    print("   - Avoid voices that sound too robotic or monotone")
    print("   - Test with actual children if possible!")

    print("\n📝 To use a voice, update your .env file:")
    print("   TTS_VOICE=sv-SE-SofieNeural  (example)")

    return voice_info


if __name__ == "__main__":
    asyncio.run(main())
