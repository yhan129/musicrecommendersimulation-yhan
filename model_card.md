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
