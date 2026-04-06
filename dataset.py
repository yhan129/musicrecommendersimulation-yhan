"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "wonderful",
    "joy",
    "grateful",
    "thrilled",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "exhausted",
    "brutal",
    "miserable",
    "horrible",
    "dread",
    "dreadful",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # New posts: varied styles
    "I absolutely love getting stuck in traffic",       # sarcasm
    "kinda sad but lowkey excited for tomorrow",        # mixed
    "not bad at all actually",                          # negation → positive
    "I hate how much I love this show",                 # mixed (hate + love)
    "this is lowkey fire ngl",                          # slang → positive (rule-based may miss it)
    "feeling exhausted but so proud of what I did",     # mixed
    "whatever I guess",                                 # neutral/dismissive
    "that exam was absolutely brutal",                  # negative
    "I'm sad and happy at the same time",               # mixed
    "grateful for everything today :)",                 # positive
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # New labels
    "negative",  # "I absolutely love getting stuck in traffic" — sarcasm, rule-based will get this wrong
    "mixed",     # "kinda sad but lowkey excited for tomorrow"
    "positive",  # "not bad at all actually"
    "mixed",     # "I hate how much I love this show"
    "positive",  # "this is lowkey fire ngl" — rule-based will miss slang
    "mixed",     # "feeling exhausted but so proud of what I did"
    "neutral",   # "whatever I guess"
    "negative",  # "that exam was absolutely brutal"
    "mixed",     # "I'm sad and happy at the same time"
    "positive",  # "grateful for everything today :)"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
