# science_topics.py
#
# Science topic catalog — metadata only, mirroring stories.py in structure.
# To add a new topic: drop a .txt file in science_topics/ and add an entry here.
#
# Future: topic difficulty levels, prerequisite topics, LangSmith tagging.

TOPICS = {
    "black_holes": {
        "title": "Black Holes",
        "file": "science_topics/black_holes.txt",
        "cover": "images/black_hole.png",
        "description": "Explore gravity, spacetime, and what happens at the edge of everything.",
    },
    "time_dilation": {
        "title": "Time Dilation",
        "file": "science_topics/time_dilation.txt",
        "cover": "images/time_dilation.png",
        "description": "Discover why time moves differently depending on speed and gravity.",
    },
    "human_brain": {
        "title": "The Human Brain",
        "file": "science_topics/human_brain.txt",
        "cover": "images/human_brain.png",
        "description": "Understand the organ that thinks, feels, remembers and wonders.",
    },
}


def load_topic_text(topic_key: str) -> str:
    """
    Reads and returns the full text of a science topic from its .txt file.
    Mirrors load_story_text() in stories.py — same pattern, different folder.
    """
    topic = TOPICS[topic_key]
    with open(topic["file"], "r", encoding="utf-8") as f:
        return f.read()
