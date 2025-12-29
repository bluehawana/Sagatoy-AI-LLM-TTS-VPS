"""Script to generate story library using Gemini and save to audio files."""

from sagatoyai.services.tts import tts_service
from sagatoyai.services.story_library import STORY_SERIES, get_story_prompt
from sagatoyai.services.gemini import gemini_service
import asyncio
import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def generate_story_audio(series_id: str, story_id: str, language: str = "sv"):
    """Generate story text and convert to audio.

    Args:
        series_id: Story series ID (trex, kanin, delfin)
        story_id: Specific story ID
        language: Language code ('en' or 'sv')
    """
    print(f"\n🎨 Generating story: {series_id}/{story_id} in {language}...")

    # Get story prompt
    prompt = get_story_prompt(series_id, story_id, language)
    if not prompt:
        print(f"❌ Story not found: {series_id}/{story_id}")
        return

    # Generate story text with Gemini
    print("📝 Generating story text with Gemini...")
    story_text = await gemini_service.generate_story(prompt, language)

    print(f"✅ Generated {len(story_text)} characters")
    print(f"\n--- Story Preview ---")
    print(story_text[:200] + "...")
    print(f"--- End Preview ---\n")

    # Convert to audio with TTS
    print("🎤 Converting to audio with TTS...")
    audio_bytes = await tts_service.synthesize_to_bytes(story_text, language)

    # Save to file
    output_dir = Path("stories") / language / series_id
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{story_id}.mp3"
    with open(output_file, "wb") as f:
        f.write(audio_bytes)

    print(f"✅ Saved audio to: {output_file}")
    print(f"📊 Audio size: {len(audio_bytes) / 1024:.1f} KB")

    # Also save text version
    text_file = output_dir / f"{story_id}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(story_text)

    print(f"✅ Saved text to: {text_file}")


async def generate_stories_by_series(language: str = "sv", series_to_generate: str = "all"):
    """Generate all stories in the library.

    Args:
        language: Language code ('en' or 'sv')
        series_to_generate: The specific series to generate ('trex', 'kanin', 'delfin') or 'all'.
    """
    print(f"\n🚀 Starting story generation for language: {language}")

    stories_to_process = {}
    if series_to_generate == "all":
        stories_to_process = STORY_SERIES
    elif series_to_generate in STORY_SERIES:
        stories_to_process = {
            series_to_generate: STORY_SERIES[series_to_generate]}

    total_stories = sum(len(series["stories"])
                        for series in stories_to_process.values())
    print(f"📖 Total stories to generate: {total_stories}")

    for series_id, series_data in stories_to_process.items():
        print(f"\n{'='*60}")
        print(f"📚 Series: {series_data['name']}")
        print(f"{'='*60}")

        for story in series_data["stories"]:
            try:
                await generate_story_audio(series_id, story["id"], language)
            except Exception as e:
                print(f"❌ Error generating {story['id']}: {e}")
                continue

    print(f"\n{'='*60}")
    print("✅ Story generation complete!")
    print(f"{'='*60}")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Sagatoyai story library")
    parser.add_argument(
        "--language",
        "-l",
        choices=["en", "sv", "both"],
        default="sv",
        help="Language to generate (default: sv)",
    )
    parser.add_argument(
        "--series",
        "-s",
        choices=["trex", "kanin", "delfin", "all"],
        default="all",
        help="Series to generate (default: all)",
    )
    parser.add_argument(
        "--story",
        help="Specific story ID to generate (e.g., trex_stockholm)",
    )

    args = parser.parse_args()

    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Then run: export GOOGLE_API_KEY='your-key-here'")
        return

    # Generate specific story
    if args.story:
        series_id = args.story.split("_")[0]
        await generate_story_audio(series_id, args.story, args.language)
        return

    # Generate by language
    if args.language == "both":
        await generate_stories_by_series("sv", args.series)
        await generate_stories_by_series("en", args.series)
    else:
        await generate_stories_by_series(args.language, args.series)


if __name__ == "__main__":
    asyncio.run(main())
