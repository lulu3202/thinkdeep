# nodes/reporter.py

from langsmith import traceable
import ollama
from config import MODEL_NAME

@traceable
def reporter_node(state):
    """
    Generates a simple summary of the session
    """

    print("Generating report with model:", MODEL_NAME)

    prompt = f"""
    You are a tutor summarizing a child's learning.

    Question:
    {state.question}

    Answer:
    {state.answer}

    Score:
    {state.score}

    Write a short 2-3 sentence summary:
    - What the child did well
    - One suggestion to improve
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    state.final_summary = response["message"]["content"].strip()

    return state