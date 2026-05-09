# nodes/coach.py
#
# Generates one thoughtful question per chunk.
# The prompt changes depending on state.mode:
#   "reading"  → story comprehension and reflection
#   "science"  → curiosity, prediction, causal reasoning
#
# Called directly from app.py (not through the full graph) to avoid
# regenerating the question when the user submits their answer.
#
# Future LangSmith tracing point: tag each run with mode + topic/story key.

from langsmith import traceable
import ollama
from config import MODEL_NAME


# --- Prompt templates ---

STORY_PROMPT = """You are a warm and thoughtful reading guide helping someone think deeply about a story.

Read the passage carefully and ask exactly ONE reflective question.

Passage:
{paragraph}

Rules:
- Ask only one question
- Focus on character motivation, emotion, or meaning
- Encourage the reader to think, not just recall facts
- Keep the question open-ended
- Do not start with "What happened" or "Who said" — go deeper

Output only the question. No explanation, no preamble.
"""

SCIENCE_PROMPT = """You are a curious and encouraging science guide helping someone think like a scientist.

Read the concept below and ask exactly ONE question that sparks curiosity or prediction.

Concept:
{paragraph}

Question styles to choose from:
- "What do you think would happen if...?"
- "Why do you think...?"
- "What might cause...?"
- "If you could change one thing about this, what would it be and why?"
- "Does this remind you of anything else you know?"

Rules:
- Ask only one question
- Encourage intuitive thinking and reasoning, not memorisation
- Make the question feel like an invitation to wonder, not a test
- Do not ask questions with simple yes/no answers

Output only the question. No explanation, no preamble.
"""


@traceable
def coach_node(state):
    """
    Generates one question from the current chunk.
    Uses state.mode to select the appropriate prompt style.
    """

    print(f"coach_node — mode: {state.mode} — model: {MODEL_NAME}")

    # Select prompt based on mode
    if state.mode == "science":
        prompt = SCIENCE_PROMPT.format(paragraph=state.paragraph)
    else:
        # Default: story / reading mode
        prompt = STORY_PROMPT.format(paragraph=state.paragraph)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    state.question = response["message"]["content"].strip()
    return state
