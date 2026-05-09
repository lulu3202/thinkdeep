# wisdom/wisdom_entries.py
#
# A curated collection of timeless wisdom from across cultures and traditions.
# Each entry is self-contained: theme, source, proverb, and a reflective question.
#
# To add new entries: follow the same dict structure and add to WISDOM_ENTRIES.
# To add new themes: just use a new theme string — the UI groups by theme automatically.
#
# Future: culture filters, personalised recommendations, LangSmith tagging per theme.

WISDOM_ENTRIES = [

    # --- Resilience ---
    {
        "theme": "Resilience",
        "culture": "Japanese Wisdom",
        "proverb": "Fall seven times, stand up eight.",
        "question": "Think of a time you kept going after failing. What made you stand back up?",
    },
    {
        "theme": "Resilience",
        "culture": "African Proverb",
        "proverb": "Smooth seas do not make skilled sailors.",
        "question": "Why do you think difficulty might be necessary for growth, not just an obstacle to it?",
    },

    # --- Patience ---
    {
        "theme": "Patience",
        "culture": "Chinese Wisdom",
        "proverb": "The man who moves a mountain begins by carrying away small stones.",
        "question": "Is there something in your life that feels too big to attempt? What would the first small stone be?",
    },
    {
        "theme": "Patience",
        "culture": "Indian Wisdom",
        "proverb": "A tree does not grow in a day.",
        "question": "In a world that moves fast, what do you think we risk losing by being impatient?",
    },

    # --- Kindness ---
    {
        "theme": "Kindness",
        "culture": "Ubuntu Philosophy (Southern Africa)",
        "proverb": "I am because we are.",
        "question": "How much of who you are has been shaped by the people around you?",
    },
    {
        "theme": "Kindness",
        "culture": "Tamil Wisdom",
        "proverb": "Do good even to those who do you harm.",
        "question": "Is kindness to those who hurt you a sign of weakness or strength? What do you think?",
    },

    # --- Humility ---
    {
        "theme": "Humility",
        "culture": "Zen Teaching",
        "proverb": "The empty vessel makes the most noise.",
        "question": "Why might a person who knows very little speak the most confidently, and how does that affect the people around them?",
    },
    {
        "theme": "Humility",
        "culture": "Zen Teaching",
        "proverb": "Before enlightenment, chop wood, carry water. After enlightenment, chop wood, carry water.",
        "question": "What do you think changes when a person becomes wiser — the tasks they do, or the way they see them?",
    },

    # --- Courage ---
    {
        "theme": "Courage",
        "culture": "Stoic Philosophy (Marcus Aurelius)",
        "proverb": "You have power over your mind, not outside events. Realise this and you will find strength.",
        "question": "Can you think of a situation where changing your thoughts about something was harder than changing the situation itself?",
    },
    {
        "theme": "Courage",
        "culture": "Sufi Wisdom",
        "proverb": "Raise your words, not your voice. It is rain that grows flowers, not thunder.",
        "question": "When have you seen someone change a difficult situation with calm words rather than force?",
    },

    # --- Truth ---
    {
        "theme": "Truth",
        "culture": "African Proverb",
        "proverb": "The truth is like a lion. You do not need to defend it. Let it loose and it will defend itself.",
        "question": "Have you ever seen a truth eventually surface on its own, even after people tried to hide it?",
    },
    {
        "theme": "Truth",
        "culture": "Stoic Philosophy (Epictetus)",
        "proverb": "We have two ears and one mouth so that we can listen twice as much as we speak.",
        "question": "What do you think we miss when we are too busy speaking to truly listen?",
    },

    # --- Anger ---
    {
        "theme": "Anger",
        "culture": "Buddhist Teaching",
        "proverb": "Holding onto anger is like drinking poison and expecting the other person to die.",
        "question": "Who do you think suffers more from held anger — the person holding it or the person it is directed at?",
    },
    {
        "theme": "Anger",
        "culture": "Indian Wisdom",
        "proverb": "For every minute you are angry, you give up sixty seconds of peace.",
        "question": "What do you think people are really protecting when they hold on to anger rather than letting it go?",
    },

    # --- Perspective ---
    {
        "theme": "Perspective",
        "culture": "Native American Wisdom",
        "proverb": "Walk a mile in another's moccasins before you judge them.",
        "question": "Think of someone whose choices seemed wrong to you. What might their life look like from the inside?",
    },
    {
        "theme": "Perspective",
        "culture": "Zen Teaching",
        "proverb": "The obstacle is the path.",
        "question": "Can you think of a difficulty that turned out to be exactly what you needed to go through?",
    },

    # --- Wisdom ---
    {
        "theme": "Wisdom",
        "culture": "African Proverb",
        "proverb": "When the music changes, so does the dance.",
        "question": "What do you think wisdom looks like in a person — what would you notice about how they act?",
    },
    {
        "theme": "Wisdom",
        "culture": "Tamil Wisdom",
        "proverb": "Learning is a treasure that follows its owner everywhere.",
        "question": "What is something you have learned that no one can take from you, and how has it shaped the way you see the world?",
    },

]


def get_themes() -> list[str]:
    """Returns a sorted, deduplicated list of all available themes."""
    return sorted(set(entry["theme"] for entry in WISDOM_ENTRIES))


def get_entries_by_theme(theme: str) -> list[dict]:
    """Returns all wisdom entries for a given theme."""
    return [e for e in WISDOM_ENTRIES if e["theme"] == theme]
