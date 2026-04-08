"""
Core recommendation logic for the Music Recommender Simulation.

Scoring algorithm (Algorithm Recipe):
  +2.0 points  — genre match
  +1.0 points  — mood match
  +1.5 points  — energy similarity  (1.5 * (1 - |song_energy - target_energy|))
  +1.0 points  — danceability similarity (1.0 * (1 - |song_danceability - target|))
  +0.5 points  — acousticness similarity (0.5 * (1 - |song_acousticness - target|))

Maximum possible score: 6.0
"""

import csv
from typing import Dict, List, Tuple, Any


def load_songs(filepath: str) -> List[Dict[str, Any]]:
    """Load songs from a CSV file and return a list of song dictionaries with numeric fields cast."""
    songs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict[str, Any], song: Dict[str, Any]) -> Tuple[float, List[str]]:
    """
    Score a single song against user preferences and return (score, reasons).

    Reasons are human-readable strings that explain each point contribution.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match: +2.0
    if song["genre"].lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0
    if song["mood"].lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: up to +1.5
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_points = round(1.5 * (1.0 - energy_gap), 3)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points})")

    # Danceability similarity: up to +1.0
    target_dance = user_prefs.get("target_danceability", 0.5)
    dance_gap = abs(song["danceability"] - target_dance)
    dance_points = round(1.0 * (1.0 - dance_gap), 3)
    score += dance_points
    reasons.append(f"danceability similarity (+{dance_points})")

    # Acousticness similarity: up to +0.5
    target_acoustic = user_prefs.get("target_acousticness", 0.5)
    acoustic_gap = abs(song["acousticness"] - target_acoustic)
    acoustic_points = round(0.5 * (1.0 - acoustic_gap), 3)
    score += acoustic_points
    reasons.append(f"acousticness similarity (+{acoustic_points})")

    return round(score, 3), reasons


def recommend_songs(
    user_prefs: Dict[str, Any], songs: List[Dict[str, Any]], k: int = 5
) -> List[Tuple[Dict[str, Any], float, List[str]]]:
    """Score every song and return the top-k results sorted from highest to lowest score."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # sorted() returns a new list without modifying the original; .sort() mutates in-place.
    # Using sorted() here because we want to keep the original songs list unchanged.
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
