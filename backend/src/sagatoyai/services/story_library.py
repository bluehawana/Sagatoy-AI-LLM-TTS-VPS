"""Story library with curated series for children."""

from typing import Dict, List

# Story series catalog
STORY_SERIES = {
    "trex": {
        "name": "T-Rex Adventures",
        "character": "T-Rex the friendly dinosaur",
        "theme": "Geography and Swedish cities",
        "stories": [
            {
                "id": "trex_stockholm",
                "title": "T-Rex visits Stockholm",
                "location": "Stockholm",
                "landmarks": ["Vasa Museum", "Gamla Stan", "Royal Palace"],
                "lesson": "Learning about Swedish history and culture",
            },
            {
                "id": "trex_gothenburg",
                "title": "T-Rex in Gothenburg",
                "location": "Gothenburg",
                "landmarks": ["Liseberg", "Harbor", "Fish Market"],
                "lesson": "Exploring Sweden's second largest city",
            },
            {
                "id": "trex_malmo",
                "title": "T-Rex discovers Malmö",
                "location": "Malmö",
                "landmarks": ["Turning Torso", "Öresund Bridge", "Malmöhus Castle"],
                "lesson": "Understanding modern Swedish architecture",
            },
            {
                "id": "trex_copenhagen",
                "title": "T-Rex crosses to Copenhagen",
                "location": "Copenhagen",
                "landmarks": ["Tivoli Gardens", "Little Mermaid", "Nyhavn"],
                "lesson": "Learning about Denmark, Sweden's neighbor",
            },
        ],
    },
    "kanin": {
        "name": "Kanin and Friends",
        "character": "Kanin the clever rabbit",
        "theme": "Friendship and problem-solving",
        "stories": [
            {
                "id": "kanin_forest",
                "title": "Kanin in the Forest",
                "location": "Swedish forest",
                "friends": ["Squirrel", "Hedgehog", "Owl"],
                "lesson": "Teamwork and helping each other",
            },
            {
                "id": "kanin_lake",
                "title": "Kanin by the Lake",
                "location": "Beautiful Swedish lake",
                "friends": ["Ducklings", "Frog", "Fish"],
                "lesson": "Caring for those who are lost",
            },
            {
                "id": "kanin_river",
                "title": "Kanin at the River",
                "location": "Flowing river",
                "friends": ["Beaver", "Otter", "Birds"],
                "lesson": "Building things together",
            },
            {
                "id": "kanin_sea",
                "title": "Kanin's Beach Adventure",
                "location": "Swedish coastline",
                "friends": ["Seagull", "Crab", "Seal"],
                "lesson": "Exploring new places with friends",
            },
        ],
    },
    "delfin": {
        "name": "Delfin the Helper",
        "character": "Delfin the kind dolphin",
        "theme": "Helping others and ocean life",
        "stories": [
            {
                "id": "delfin_fishermen",
                "title": "Delfin helps the Fishermen",
                "location": "Gothenburg harbor",
                "activity": "Helping fishermen find fish",
                "lesson": "Working together and being helpful",
            },
            {
                "id": "delfin_rescue",
                "title": "Delfin's Brave Rescue",
                "location": "Swedish west coast",
                "activity": "Rescuing a child in the water",
                "lesson": "Being brave and helping in emergencies",
            },
            {
                "id": "delfin_swimming",
                "title": "Delfin teaches Swimming",
                "location": "Safe swimming area",
                "activity": "Teaching kids water safety",
                "lesson": "Learning to swim safely",
            },
            {
                "id": "delfin_ocean",
                "title": "Delfin cleans the Ocean",
                "location": "Swedish waters",
                "activity": "Cleaning plastic from the sea",
                "lesson": "Taking care of our environment",
            },
        ],
    },
}


def get_story_series() -> Dict:
    """Get all available story series."""
    return STORY_SERIES


def get_series_list() -> List[str]:
    """Get list of series names."""
    return list(STORY_SERIES.keys())


def get_stories_in_series(series_id: str) -> List[Dict]:
    """Get all stories in a specific series."""
    if series_id in STORY_SERIES:
        return STORY_SERIES[series_id]["stories"]
    return []


def get_story_prompt(series_id: str, story_id: str, language: str = "en") -> str:
    """Generate story prompt for LLM based on series and story ID."""
    if series_id not in STORY_SERIES:
        return None

    series = STORY_SERIES[series_id]
    story = next((s for s in series["stories"] if s["id"] == story_id), None)

    if not story:
        return None

    # Build prompt based on language
    if language == "sv":
        prompt = f"""Skriv en rolig och lärorik barnberättelse (3-5 minuter lång) för barn 3-10 år.

Serie: {series['name']}
Huvudkaraktär: {series['character']}
Titel: {story['title']}
Plats: {story['location']}

Tema: {series['theme']}
Läxa: {story.get('lesson', '')}

Inkludera:
- Enkelt, varmt språk för barn
- Spännande äventyr
- Positiv läxa
- Lyckligt slut

Berättelsen ska vara engagerande, fantasifull och lämplig för barn."""
    else:
        prompt = f"""Write a fun and educational children's story (3-5 minutes long) for kids aged 3-10.

Series: {series['name']}
Main Character: {series['character']}
Title: {story['title']}
Location: {story['location']}

Theme: {series['theme']}
Lesson: {story.get('lesson', '')}

Include:
- Simple, warm language for children
- Exciting adventure
- Positive lesson
- Happy ending

The story should be engaging, imaginative, and age-appropriate."""

    return prompt
