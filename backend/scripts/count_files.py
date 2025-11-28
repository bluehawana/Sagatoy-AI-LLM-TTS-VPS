"""Script to count generated story and audio files."""

import os
from pathlib import Path


def count_generated_files(base_dir: str = "stories"):
    """Counts the generated story and audio files."""
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"❌ Directory '{base_dir}' not found.")
        print("It seems the story generation script hasn't been run yet.")
        print("Run this command first: python scripts/generate_stories.py")
        return

    txt_count = len(list(base_path.rglob("*.txt")))
    mp3_count = len(list(base_path.rglob("*.mp3")))

    print("\n" + "=" * 40)
    print("📊 File Generation Summary")
    print("=" * 40)
    print(f"Total story text files (.txt): {txt_count}")
    print(f"Total audio files (.mp3):     {mp3_count}")
    print("=" * 40)

    if txt_count == 0 and mp3_count == 0:
        print("\nIt looks like no files have been generated yet.")
        print("Run `python scripts/generate_stories.py` to create them.")
    elif txt_count != mp3_count:
        print("\n⚠️ Warning: The number of text files and audio files do not match.")
        print("Some stories might be missing their audio file. You may want to run the generation again.")
    else:
        print("\n✅ Success! All stories appear to have a matching audio file.")


if __name__ == "__main__":
    # Assuming the script is run from the `backend` directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    count_generated_files()
