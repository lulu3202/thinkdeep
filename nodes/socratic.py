from langsmith import traceable
import ollama
from config import MODEL_NAME
from state import SessionState

SOCRATIC_PROMPT = """\
You are a Socratic dialogue partner helping someone think more deeply about an ancient proverb.

Proverb: "{proverb}"
Question posed: "{question}"
The person's reflection: "{answer}"

Your role: gently challenge ONE assumption or unexplored angle in their reflection.
- First, acknowledge what is true or insightful in what they said (1 sentence).
- Then raise a probing counter-perspective or an assumption they may not have examined (1-2 sentences).
- End with a single, open question that invites them to go deeper.

Be warm, intellectually honest, and brief — 3-4 sentences total. Do not lecture.
Do not start with "I" or use phrases like "Great reflection".
"""


@traceable(name="socratic_node")
def stream_socratic(state: SessionState):
    """Streams a gentle Socratic challenge to the user's reflection."""
    prompt = SOCRATIC_PROMPT.format(
        proverb=state.paragraph,
        question=state.question,
        answer=state.answer,
    )
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response:
        text = chunk.get("message", {}).get("content", "")
        if text:
            yield text
