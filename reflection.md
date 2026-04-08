# Reflection: Profile Comparison and System Evaluation

## Profile Comparisons

### High-Energy Pop Fan vs. Chill Lofi Listener

These two profiles produced the most opposite results, which makes sense because they ask for nearly opposite song attributes.

The Pop Fan got Levitating (5.975), Shape of You (5.765), and Sunflower (5.515) — all high-danceability, low-acousticness pop tracks. The scores are clustered tightly in the 5.5–6.0 range because the dataset has many pop songs that fit well.

The Lofi Listener got Weightless at 5.795, then the next recommendation (Stay With Me) scored only 2.455 — a massive drop. This reveals the system's biggest weakness: the dataset only has one ambient song. Once the genre match is gone, every other song looks equally mediocre to this profile. A real user with chill taste would get almost no relevant recommendations after the first one.

**Takeaway:** The genre weight of +2.0 is strong enough that a profile whose preferred genre is rare in the catalog gets stranded. The system rewards well-represented genres.

---

### Deep Intense Rock vs. Sad Hype (Conflicted)

The Rock profile cleanly picks Smells Like Teen Spirit (#1 at 5.870) because it is the only rock song that also matches the "angry" mood. This feels intuitively correct.

The Conflicted profile was the most interesting to observe. It prefers hip-hop, sad mood, but very high energy (0.9). That combination is hard to satisfy simultaneously because most "sad" songs in the dataset have low energy. SAD! by XXXTENTACION wins because it gets both genre and mood bonuses, even though its energy (0.4) is far from the target (0.9). Industry Baby and Gym Hero come in at #2 and #3 with nearly the same score — they are both high-energy hip-hop but neither matches the "sad" mood.

**Takeaway:** When a user's mood preference conflicts with their energy preference, the system partially satisfies each dimension rather than finding a perfect match. The genre bonus (+2.0) ends up deciding the top results more than any other factor. This is a filter bubble in action: the profile gets hip-hop recommendations even when those songs don't truly feel "sad."

---

### High-Energy Pop Fan vs. Deep Intense Rock

Both profiles want high energy, but they diverge on genre and mood (happy vs. angry). Interesting overlap: "good 4 u" by Olivia Rodrigo appears at #4 for the Rock profile because it has high energy (0.9) and an "angry" mood, even though it is technically pop. This shows the system can surface cross-genre gems when attribute scores are strong enough to overcome the genre mismatch.

---

## What Surprised Me

The biggest surprise was how dominant the genre match bonus is. Almost every top result shares the user's preferred genre. Songs from other genres would need near-perfect energy/danceability/acousticness matches to compete with even a mediocre same-genre song. In practice, this means a user who likes jazz (not in the dataset) would always get low scores across the board — the recommender would effectively be useless for them.

I also didn't expect the Chill Lofi Listener results to fall off so sharply after the first pick. The second recommendation (Stay With Me, score 2.455) scored less than half of the first (Weightless, 5.795). That gap alone shows how small the dataset is and how important genre diversity is for the catalog.

---

## What I Would Try Next

1. **Normalize genre weights by catalog frequency** — if pop makes up 40% of the catalog, its genre match bonus should be worth less so that rare genres can compete.
2. **Add more ambient and indie songs** to give underrepresented profiles real options.
3. **Introduce collaborative signals** — even a small "users who liked X also liked Y" layer would break out of the pure content-based filter bubble.
