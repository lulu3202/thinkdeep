# nodes/evaluator.py
#
# Evaluates the user's answer and assigns a score (0, 1, or 2) plus feedback.
# The prompt and scoring philosophy change depending on state.mode:
#   "reading"  → strict correctness, rewards clear understanding of the text
#   "science"  → rewards reasoning quality, curiosity, and causal thinking
#                even if the answer is not perfectly correct
#
# Called directly from app.py to avoid coach_node re-running on answer submit.
#
# Future LangSmith tracing point: log score distribution per mode and topic.

from langsmith import traceable
import ollama
from config import MODEL_NAME


STORY_EVAL_PROMPT = """You are a strict but fair tutor grading a student's answer about a story.

Passage:
\"\"\"{paragraph}\"\"\"

Question asked:
\"\"\"{question}\"\"\"

Student's answer:
\"\"\"{answer}\"\"\"

Grading rules:
- Score 0: answer is wrong, off-topic, nonsensical, or shows no understanding
- Score 1: answer shows some understanding but is incomplete or only partly correct
- Score 2: answer is clearly correct AND shows genuine understanding of the passage

Additional rules:
- Short answers (under 5 words) almost always score 0 or 1
- Do NOT reward effort or politeness — only correctness matters
- Do NOT give score 2 unless the answer directly and correctly addresses the question
- "I don't know" or blank responses = score 0

Respond in EXACTLY this format with no extra text:
Score: <0 or 1 or 2>
Feedback: <one sentence of helpful feedback>
"""

SCIENCE_EVAL_PROMPT = """You are an encouraging science mentor evaluating how well a student is thinking, not just what they know.

Concept passage:
\"\"\"{paragraph}\"\"\"

Question asked:
\"\"\"{question}\"\"\"

Student's answer:
\"\"\"{answer}\"\"\"

Grading philosophy:
- You are rewarding scientific thinking, curiosity, and reasoning — not memorised facts
- A thoughtful answer that shows genuine reasoning should score well even if imperfect
- An answer that shows no attempt to reason or engage scores low

Scoring rules:
- Score 0: no attempt, "I don't know", completely off-topic, or one word with no reasoning
- Score 1: shows some relevant thinking but the reasoning is shallow, confused, or incomplete
- Score 2: shows genuine curiosity, clear reasoning, or a thoughtful prediction — even if not perfectly correct

Feedback style:
- Be warm and encouraging
- Point toward the interesting idea they missed or almost reached
- Never make them feel wrong for thinking — guide them further

Respond in EXACTLY this format with no extra text:
Score: <0 or 1 or 2>
Feedback: <one encouraging sentence that extends their thinking>
"""


@traceable
def evaluator_node(state):
    """
    Scores the user's answer and generates feedback.
    Uses state.mode to select the appropriate prompt and scoring philosophy.
    """

    print(f"evaluator_node — mode: {state.mode} — model: {MODEL_NAME}")

    # Select prompt based on mode
    if state.mode == "science":
        prompt = SCIENCE_EVAL_PROMPT.format(
            paragraph=state.paragraph,
            question=state.question,
            answer=state.answer,
        )
    else:
        prompt = STORY_EVAL_PROMPT.format(
            paragraph=state.paragraph,
            question=state.question,
            answer=state.answer,
        )

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
        # Grab only the first digit in case the model adds trailing text
        digit = next((c for c in raw_score if c in "012"), None)
        state.score = int(digit) if digit is not None else 1

        state.feedback = feedback_line.split(":", 1)[1].strip()

    except Exception as e:
        print("Parsing error:", e)
        state.score = 1
        state.feedback = "Good attempt — try to explain your thinking a little more."

    return state
