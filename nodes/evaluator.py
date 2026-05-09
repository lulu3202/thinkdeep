# nodes/evaluator.py

from langsmith import traceable
import ollama
from config import MODEL_NAME

# Phrases that immediately signal the student has no answer.
# Checked before calling the model to avoid gemma:2b being too lenient.
_NO_ANSWER_PHRASES = [
    "i don't know", "i do not know", "idk", "no idea", "not sure",
    "i'm not sure", "i am not sure", "don't know", "do not know",
    "no clue", "i have no idea", "i don't understand", "i cant",
    "i can't", "i cannot", "nothing", "n/a", "na", "?", "...",
]


def _is_non_answer(text: str) -> bool:
    """Returns True if the answer is clearly a non-attempt."""
    cleaned = text.lower().strip().rstrip(".")
    return cleaned in _NO_ANSWER_PHRASES or len(cleaned) < 4


@traceable
def evaluator_node(state):
    """
    Evaluates the user's answer against the question and paragraph.
    Assigns score 0, 1, or 2 and short feedback.

    Called directly from app.py (not through the full graph) so that
    coach_node does not re-run and overwrite the question.

    Future LangSmith tracing point: log score distribution per story.
    """

    print("Evaluating answer with model:", MODEL_NAME)

    # --- Pre-filter: catch obvious non-answers without calling the model ---
    if _is_non_answer(state.answer):
        state.score = 0
        state.feedback = (
            "It looks like you weren't sure. Try re-reading the passage "
            "and look for clues that relate to the question."
        )
        return state

    # --- Call the model for real answers ---
    prompt = f"""You are a strict tutor grading a student's written answer.

Passage the student read:
\"\"\"{state.paragraph}\"\"\"

Question asked:
\"\"\"{state.question}\"\"\"

Student's answer:
\"\"\"{state.answer}\"\"\"

Grading rules — follow these exactly:
- Score 0: answer is wrong, off-topic, nonsensical, or shows no understanding
- Score 1: answer is on the right track but incomplete or only partly correct
- Score 2: answer is clearly correct AND shows genuine understanding of the passage

Additional rules:
- Short answers (under 5 words) almost always score 0 or 1.
- Do NOT reward effort or politeness — only correctness matters.
- Do NOT give score 2 unless the answer directly and correctly addresses the question.

Respond in EXACTLY this format with no extra text:
Score: 0
Feedback: <one sentence>

or

Score: 1
Feedback: <one sentence>

or

Score: 2
Feedback: <one sentence>
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    output = response["message"]["content"].strip()
    print("Evaluator raw output:", output)

    try:
        lines = [l.strip() for l in output.split("\n") if l.strip()]

        score_line = next(l for l in lines if l.lower().startswith("score"))
        feedback_line = next(l for l in lines if l.lower().startswith("feedback"))

        raw_score = score_line.split(":", 1)[1].strip()
        # Extract first digit in case the model adds trailing text
        digit = next((c for c in raw_score if c in "012"), None)
        state.score = int(digit) if digit is not None else 1

        state.feedback = feedback_line.split(":", 1)[1].strip()

    except Exception as e:
        print("Parsing error:", e)
        print("Raw output:", output)
        state.score = 1
        state.feedback = "Good attempt — try to explain your thinking a bit more."

    return state
