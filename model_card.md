# Model Card: Mood Machine

This model card covers both versions of the Mood Machine classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule based model was the primary focus; the ML model was used as a contrast.

**Intended purpose:**
Classify short text messages (social media style posts) into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**
The rule based model preprocesses each post into lowercase tokens, strips punctuation, then scans for known positive and negative words. A running score is computed — positive words add +1, negative words subtract 1 — with negation handling (words like "not" flip the next word's polarity). If both positive and negative signals are found, the label is `mixed`; otherwise the sign of the score determines `positive`, `negative`, or `neutral`.

The ML model uses `CountVectorizer` to convert posts into bag-of-words vectors, then trains a `LogisticRegression` classifier on those vectors and the human-assigned labels. It learns statistical associations between words and labels rather than following handcrafted rules.

---

## 2. Data

**Dataset description:**
The dataset contains 16 short posts in `SAMPLE_POSTS`. The original 6 starter posts were expanded with 10 new posts covering slang, sarcasm, mixed emotions, negation, and ambiguous tone.

**Labeling process:**
Labels were assigned based on the intended emotional tone of the post. A few posts were genuinely ambiguous — for example, `"whatever I guess"` could be neutral or slightly negative depending on context. `"I hate how much I love this show"` was labeled `mixed` because it expresses both hate and love simultaneously.

**Important characteristics of the dataset:**

- Contains slang: `"lowkey fire"`, `"ngl"`, `"kinda"`
- Includes sarcasm: `"I absolutely love getting stuck in traffic"`
- Several posts express mixed feelings
- One post uses emoji punctuation: `"grateful for everything today :)"`
- Negation patterns: `"not bad at all"`, `"not happy"`

**Possible issues with the dataset:**

- Very small (16 examples) — not enough to generalize to real-world text
- Sarcasm is labeled as `negative` but requires world knowledge the rule-based model lacks
- Most posts are in standard English; dialect, non-English slang, or code-switching are not represented
- Dataset is slightly imbalanced: more `mixed` and `positive` examples than `neutral`

---

## 3. How the Rule Based Model Works

**Scoring rules:**

- Each token is checked against `POSITIVE_WORDS` and `NEGATIVE_WORDS` sets
- Positive match: score += 1; negative match: score -= 1
- Negation words (`not`, `never`, `no`, `don't`, etc.) flip the polarity of the next token
- If both positive and negative words are found in a post (even after negation), label = `mixed`
- Otherwise: score > 0 → `positive`, score < 0 → `negative`, score == 0 → `neutral`
- Preprocessing strips punctuation so `"love!"` and `"love"` are treated the same

**Strengths:**

- Fully transparent: you can trace every decision back to a token and a rule
- Negation works reliably for simple cases like `"not happy"` or `"not bad"`
- Mixed label detection catches genuine dual-sentiment posts like `"tired but hopeful"` and `"hate how much I love this"`
- No training data required; rules can be updated instantly

**Weaknesses:**

- Cannot detect sarcasm: `"I absolutely love getting stuck in traffic"` is predicted `positive`
- Unknown slang scores as `neutral`: `"this is lowkey fire ngl"` has no vocabulary match
- Emojis like `:)` or `💀` have no effect after punctuation stripping
- Word context beyond immediate negation is ignored: `"I used to love this"` would score positive even though the sentiment is past/gone
- The word lists are small and culturally narrow — words common in certain communities or dialects may be missing entirely

---

## 4. How the ML Model Works

**Features used:**
Bag of words using `CountVectorizer` — each unique word in the training set becomes a feature column, and each post is represented as a count of how many times each word appears.

**Training data:**
Trained on the same 16 `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**
With only 16 examples, the model memorizes the training data rather than learning general patterns. It achieves 100% accuracy on the training set, which is a classic sign of overfitting. Adding more examples with varied phrasing quickly exposed how fragile this learned vocabulary is — the word `"happy"` alone predicts `negative` in the interactive session because in the training data `"happy"` appears only in `"I am not happy about this"` (a negative post), so the model associates `"happy"` with negative sentiment.

**Strengths and weaknesses:**

- Strength: learns vocabulary automatically from labeled data; no manual rule writing required
- Strength: can pick up multi-word statistical patterns if the training set is large enough
- Weakness: severe overfitting on 16 examples — the model learned spurious correlations
- Weakness: sensitive to label choices; mislabeling one post can flip predictions for similar posts
- Weakness: no understanding of negation, sarcasm, or context — same fundamental limits as the rule based model, but now hidden inside learned weights instead of visible rules

---

## 5. Evaluation

**How you evaluated the model:**
Both models were evaluated on the same 16 labeled examples using accuracy (fraction of posts where predicted label equals true label).

| Model | Accuracy |
|-------|----------|
| Rule based | 0.88 (14/16) |
| ML (train set) | 1.00 (16/16) |

The ML model's 1.00 is misleading — it is evaluated on the same data it trained on.

**Examples of correct predictions (rule based):**

- `"I love this class so much"` → `positive` — "love" is a strong positive signal, no negation present
- `"I hate how much I love this show"` → `mixed` — both "hate" and "love" are detected, triggering the mixed label
- `"not bad at all actually"` → `positive` — negation flips "bad" to a positive signal, score becomes +1

**Examples of incorrect predictions (rule based):**

- `"I absolutely love getting stuck in traffic"` → predicted `positive`, true `negative`
  Reason: the rule based model sees "love" and adds +1 to the score. It has no way to know that "getting stuck in traffic" is an unwanted situation, so sarcasm is invisible to it.

- `"this is lowkey fire ngl"` → predicted `neutral`, true `positive`
  Reason: "lowkey", "fire" (slang for excellent), and "ngl" (not gonna lie) are not in the word lists. After preprocessing, no tokens match, so the score stays at 0 → `neutral`.

---

## 6. Limitations

- **Dataset is tiny.** 16 examples is not enough to train a reliable model or evaluate generalization. Results on new, unseen text will be much worse.
- **No sarcasm detection.** Both models fail on ironic or sarcastic phrasing. Sarcasm requires understanding of context, common knowledge, and often cultural references.
- **Slang and informal language are underrepresented.** Words like "fire", "lowkey", "no cap", "dead", "sick" (meaning good) are not in the vocabulary. The rule based model scores them as neutral; the ML model may have picked up accidental correlations.
- **Mixed label is coarse.** A post like `"I hate how much I love this show"` and `"tired but hopeful"` are both labeled `mixed` but they express very different emotional dynamics.
- **Emojis are stripped.** After punctuation removal, `:)` becomes empty and is discarded. Unicode emoji like `💀` or `🎉` pass through as single tokens but are not in any word list.
- **One-word sensitivity.** The ML model learned that `"happy"` → `negative` because the only training post containing "happy" was a negative one. This is a direct consequence of small data.

---

## 7. Ethical Considerations

- **Misclassifying distress.** A message like `"I'm fine :)"` could be a masked cry for help. A system that scores it `neutral` and takes no action could fail someone in a real support context.
- **Cultural and linguistic bias.** The word lists and labeled examples are built around standard American English. Dialect, regional slang, multilingual expressions, and cultural references from other communities are missing. The model is less accurate — and potentially dismissive — for those groups.
- **Privacy.** Analyzing the emotional content of personal messages without consent raises serious privacy concerns. Even a simple keyword model reveals information people may not intend to share.
- **Feedback loops.** If this model were used to filter or surface content, its errors (especially around sarcasm and slang) could systematically suppress or amplify certain communities' voices.
- **Overconfidence.** The ML model shows 100% training accuracy, which could give a false sense of reliability. Any real deployment should be tested on unseen data and human-reviewed before use.

---

## 8. Ideas for Improvement

- **Add more labeled data** — at minimum 100–200 diverse examples before the ML model can generalize
- **Use TF-IDF instead of CountVectorizer** to downweight common words and boost informative ones
- **Add a sarcasm signal** — e.g., detect patterns like "I love [obviously bad thing]" using a short phrase list
- **Handle emoji explicitly** — map common emoji to sentiment signals before stripping punctuation (`💀` → negative, `🎉` → positive)
- **Expand slang vocabulary** — add culturally common positive/negative slang to the word lists
- **Use a real test split** — hold out 20% of data for evaluation so accuracy reflects generalization, not memorization
- **Try a small pretrained model** — even a lightweight transformer fine-tuned on sentiment data would handle sarcasm and context far better than bag-of-words approaches
- **Multi-word negation scope** — current negation only covers the immediately next token; `"I never feel truly happy here"` only negates `"feel"`, missing `"happy"`

---

---

# Model Card: VibeFinder 1.0 (Music Recommender Simulation)

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder takes a user's taste profile (preferred genre, mood, energy level, danceability, and acousticness) and ranks a catalog of songs from most to least relevant. The goal is to surface the top 5 songs that best match what a listener is in the mood for right now.

---

## 3. Data Used

- **Source**: `data/songs.csv` — a hand-curated catalog of 20 songs
- **Features per song**: `title`, `artist`, `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `danceability` (0.0–1.0), `acousticness` (0.0–1.0)
- **Genre distribution**: pop (8), hiphop (5), rock (4), indie (3), ambient (1)
- **Mood distribution**: happy (5), excited (5), sad (3), melancholy (3), angry (3), calm (1), mixed (1)
- **Limits**: 20 songs is extremely small. The catalog is English-language and skewed toward 2015–2023 Western pop and hip-hop. Classical, jazz, country, Latin, and K-pop are entirely absent.

---

## 4. Algorithm Summary

For every song in the catalog, VibeFinder computes a score using five weighted rules:

1. **Genre match** (+2.0 points) — Does the song's genre match what the user said they like?
2. **Mood match** (+1.0 point) — Does the song's mood label match the user's preferred mood?
3. **Energy closeness** (up to +1.5 points) — Songs closer to the user's target energy score higher. Calculated as 1.5 × (1 − |song_energy − target_energy|).
4. **Danceability closeness** (up to +1.0 point) — Same proximity formula applied to danceability.
5. **Acousticness closeness** (up to +0.5 points) — Same proximity formula, smaller weight.

Maximum possible score: **6.0**. Songs are then sorted from highest to lowest score; the top 5 are returned with a plain-language explanation of each point contribution.

---

## 5. Observed Behavior / Biases

- **Genre dominance creates filter bubbles.** The +2.0 genre bonus is larger than the maximum energy bonus (1.5). This means a song in the correct genre with mediocre attributes will almost always beat a cross-genre song that perfectly matches energy and danceability. Users whose favorite genre is rare in the catalog (e.g., "ambient") see their recommendations fall off a cliff after the first match.
- **Dataset genre imbalance amplifies the bias.** 40% of the catalog is pop. A pop fan gets 8 genre-matched songs to rank; an ambient fan gets 1. The system works well for the majority genre and poorly for minority genres.
- **Conflicting preferences are resolved by genre, not mood.** The "Sad Hype" adversarial profile (hip-hop genre, sad mood, high energy) wanted all three at once. The system gave it SAD! at #1 because genre+mood matched, even though that song's energy (0.4) was far from the target (0.9). Genre won the tiebreak.
- **Tempo is loaded but ignored.** `tempo_bpm` is parsed from the CSV but not included in scoring. A user who wants fast (150+ BPM) songs gets no credit for that preference.

---

## 6. Evaluation Process

Four user profiles were tested:

| Profile | Top Result | Score |
|---|---|---|
| High-Energy Pop Fan | Levitating - Dua Lipa | 5.975 |
| Chill Lofi Listener | Weightless - Marconi Union | 5.795 |
| Deep Intense Rock | Smells Like Teen Spirit - Nirvana | 5.870 |
| Sad Hype (Conflicted) | SAD! - XXXTENTACION | 4.935 |

**Weight-shift experiment**: Doubling the energy weight to 3.0 and halving the genre weight to 1.0 caused "good 4 u" (high energy, angry mood) to overtake purely genre-matched songs for the Rock profile. The rankings shifted but still felt reasonable — mood-matching rock songs stayed near the top. This suggests the current genre weight is defensible but slightly conservative.

**Surprise finding**: The Chill Lofi Listener's #2 recommendation was Stay With Me by Sam Smith (score 2.455) — a slow, fairly acoustic pop ballad. It landed there not because it is "lofi" but because its low energy and moderate acousticness happened to match numerically. A human listener would not consider this a lofi recommendation at all.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Educational demonstration of how content-based filtering works
- Classroom projects exploring weighted scoring and ranking algorithms
- Prototyping a recommendation concept before adding real data

**Not intended for:**
- Production use as an actual music recommender
- Any context where users expect culturally diverse or genre-broad recommendations
- Deployment without significantly expanding the catalog (minimum ~500 songs with balanced genre representation)

---

## 8. Ideas for Improvement

1. **Normalize genre weight by catalog frequency** — if pop represents 40% of the catalog, reduce its match bonus proportionally so rare genres remain competitive.
2. **Add tempo_bpm as a scoring dimension** — it is already parsed; a proximity score similar to energy would make the system more sensitive to pace preferences.
3. **Expand the catalog to 200+ songs with balanced genre coverage** — the single biggest improvement. The current system cannot serve niche tastes because there is nothing to recommend.

---

## 9. Personal Reflection

**Biggest learning moment:** I expected the scoring algorithm to feel complex, but once you reduce it to "add up weighted differences," it becomes very simple math. The hard part is not the formula — it is deciding what the weights *mean* and whether they reflect how humans actually experience music.

**How AI tools helped:** Claude Code designed the CSV schema, drafted the scoring function, and identified the genre-dominance bias before I ran a single profile. Where I needed to double-check was the output interpretation — the tool could calculate scores correctly but could not tell me whether "Stay With Me" actually sounds like a lofi recommendation. That judgment required a human ear.

**What surprised me about simple algorithms:** Even this five-rule weighted scorer "feels" like a recommender. When the High-Energy Pop Fan gets Levitating at #1, it intuitively makes sense. The algorithm is so transparent you can trace every point, yet the result still seems meaningful. That gap between "dumb math" and "feels smart" is exactly what makes recommendation systems interesting — and exactly why their biases are so easy to hide.

**What I would try next:** Implementing a tiny collaborative filtering layer by letting two profiles share ratings on a few songs, then using overlap to suggest songs one profile liked that the other hasn't seen. Even with 20 songs and 4 profiles, you could test whether collaborative signals break the genre filter bubble.
