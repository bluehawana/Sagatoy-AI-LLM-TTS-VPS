"""Test Q&A with weather integration - bilingual support."""

import asyncio
from sagatoyai.services.gemini import gemini_service
from sagatoyai.services.weather import weather_service
from sagatoyai.services.tts import tts_service
from sagatoyai.services.language import detect_language


async def handle_weather_query(user_input: str, detected_language: str):
    """Handle weather-related queries."""
    # Extract location from query (simple approach)
    locations = ["stockholm", "gothenburg", "göteborg", "malmo", "malmö"]
    location = "stockholm"  # default

    user_lower = user_input.lower()
    for loc in locations:
        if loc in user_lower:
            location = loc
            if loc == "göteborg":
                location = "gothenburg"
            elif loc == "malmö":
                location = "malmo"
            break

    # Get weather data
    weather_data = await weather_service.get_weather(location)

    # Create child-friendly response
    if detected_language == "sv":
        response = f"I {weather_data.location} är det {weather_data.temperature_celsius}°C! {weather_data.description}"
    else:
        response = f"In {weather_data.location} it's {weather_data.temperature_celsius}°C! {weather_data.description}"

    return response, weather_data


async def toy_qa_interaction(user_input: str):
    """Full Q&A interaction with language detection and weather support."""

    print(f"\n{'='*60}")
    print(f"🎤 Child says: '{user_input}'")
    print(f"{'='*60}")

    # Detect language
    detected_language = detect_language(user_input)
    print(f"🌍 Detected language: {detected_language}")

    # Check if it's a weather query
    weather_keywords = ["weather", "väder", "vädret", "temperature",
                        "temperatur", "rain", "regn", "snow", "snö", "kallt", "cold", "warm", "varmt"]
    is_weather_query = any(keyword in user_input.lower()
                           for keyword in weather_keywords)

    if is_weather_query:
        print("☁️ Weather query detected!")
        response_text, weather_data = await handle_weather_query(user_input, detected_language)
        intent = "weather"
    else:
        # Use Gemini for general Q&A
        print("💭 General question detected!")
        response_text, intent = await gemini_service.generate_conversation_response(
            user_input=user_input,
            language=detected_language
        )

    print(f"\n🤖 Toy responds: '{response_text}'")
    print(f"🎯 Intent: {intent}")

    # Convert to speech
    print("\n🔊 Converting to speech...")
    audio_bytes = await tts_service.synthesize_to_bytes(response_text, detected_language)

    # Save audio
    output_file = f"qa_response_{detected_language}.mp3"
    with open(output_file, "wb") as f:
        f.write(audio_bytes)

    print(f"✅ Audio saved to: {output_file}")
    print(f"📊 Audio size: {len(audio_bytes) / 1024:.1f} KB")

    return response_text, output_file


async def main():
    """Test Q&A with various questions in Swedish and English."""

    print("\n" + "="*60)
    print("🧸 ToToy AI - Q&A Test with Weather Integration")
    print("="*60)

    # Test questions
    test_questions = [
        # Weather queries
        "Hej toy, vad är vädret idag i Göteborg?",
        "Hey toy, what's the weather like in Stockholm?",
        "Hej toy, är det kallt ute i Malmö?",

        # General questions
        "Hej toy, varför är himlen blå?",
        "Hey toy, why do birds fly?",
        "Hej toy, kan du räkna till tio?",
    ]

    for question in test_questions:
        await toy_qa_interaction(question)
        print("\n" + "-"*60 + "\n")
        await asyncio.sleep(1)  # Small delay between requests

    print("="*60)
    print("✅ All tests complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
