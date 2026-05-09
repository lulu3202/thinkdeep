# stories.py
#
# Story catalog — metadata only.
# Each entry maps a story key to its title and the path of its .txt file.
# To add a new story: drop a .txt file in stories/ and add an entry here.
#
# Future: this dict could be loaded from a config file or database.

STORIES = {
    "selfish_giant": {
        "title": "The Selfish Giant",
        "file": "stories/selfish_giant.txt",
        "cover": "images/the_selfish_giant.jpeg",
        "description": "A giant learns that kindness opens the heart and changes the seasons.",
    },
    "happy_prince": {
        "title": "The Happy Prince",
        "file": "stories/happy_prince.txt",
        "cover": "images/the_happy_prince.jpeg",
        "description": "A golden statue and a small swallow share everything they have.",
    },
    "nightingale_rose": {
        "title": "The Nightingale and the Rose",
        "file": "stories/nightingale_rose.txt",
        "cover": "images/the_nightingale_rose.jpeg",
        "description": "A nightingale sacrifices everything for love and learns its true cost.",
    },
}


def load_story_text(story_key: str) -> str:
    """
    Reads and returns the full text of a story from its .txt file.
    Called once when the user starts a story — not on every render.
    """
    story = STORIES[story_key]
    with open(story["file"], "r", encoding="utf-8") as f:
        return f.read()


def make_chunks(full_story: str, target_chunks: int = 5) -> list[str]:
    """
    Splits a story into roughly `target_chunks` parts (default 5).

    How it works:
      1. Split on blank lines → list of paragraphs, drop empty ones
      2. Calculate how many paragraphs fit in each chunk so the total
         comes out close to target_chunks
      3. Group that many paragraphs → one chunk string

    # Future LangSmith tracing point: log chunk count and sizes here.
    """
    import math

    paragraphs = [p.strip() for p in full_story.split("\n\n") if p.strip()]

    # How many paragraphs per chunk to land near target_chunks total
    chunk_size = max(2, math.ceil(len(paragraphs) / target_chunks))

    chunks = [
        "\n\n".join(paragraphs[i : i + chunk_size])
        for i in range(0, len(paragraphs), chunk_size)
    ]

    return chunks
