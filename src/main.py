"""
Entry point for the Music Recommender Simulation.

Runs the recommender against four distinct user profiles and prints ranked results.
"""

import os
from src.recommender import load_songs, recommend_songs

# Resolve path to the CSV relative to the project root
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop Fan": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_danceability": 0.75,
        "target_acousticness": 0.05,
    },
    "Chill Lofi Listener": {
        "favorite_genre": "ambient",
        "favorite_mood": "calm",
        "target_energy": 0.15,
        "target_danceability": 0.20,
        "target_acousticness": 0.85,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "angry",
        "target_energy": 0.85,
        "target_danceability": 0.40,
        "target_acousticness": 0.02,
    },
    # Adversarial / edge case: contradictory preferences
    "Sad Hype (Conflicted)": {
        "favorite_genre": "hiphop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_danceability": 0.70,
        "target_acousticness": 0.05,
    },
}


def print_recommendations(profile_name: str, recommendations, top_k: int = 5) -> None:
    """Print formatted recommendation results for a given profile."""
    print(f"\n{'=' * 60}")
    print(f"  Profile: {profile_name}")
    print(f"  Top {top_k} Recommendations")
    print(f"{'=' * 60}")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} - {song['artist']}")
        print(f"       Score: {score:.3f}  |  Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Why: {', '.join(reasons)}")
    print()


def main() -> None:
    """Load songs and run the recommender for every defined user profile."""
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    for profile_name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
