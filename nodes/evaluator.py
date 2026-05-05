# nodes/evaluator.py

from langsmith import traceable
import ollama
from config import MODEL_NAME

@traceable
def evaluator_node(state):
    """
    Evaluates user's answer and assigns:
    - score (0,1,2)
    - feedback
    """

    print("Evaluating answer with model:", MODEL_NAME)

    prompt = f"""
    You are a helpful tutor evaluating a child's answer.

    Paragraph:
    {state.paragraph}

    Question:
    {state.question}

    Student Answer:
    {state.answer}

    Scoring Rules:
    0 = incorrect or irrelevant
    1 = partially correct
    2 = clear and thoughtful answer

    Output format EXACTLY like this:
    Score: <0,1,2>
    Feedback: <short helpful feedback>
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    output = response["message"]["content"].strip()

    # --- Simple parsing ---
    try:
        lines = output.split("\n")

        score_line = [l for l in lines if "Score" in l][0]
        feedback_line = [l for l in lines if "Feedback" in l][0]

        state.score = int(score_line.split(":")[1].strip())
        state.feedback = feedback_line.split(":", 1)[1].strip()

    except Exception as e:
        print("Parsing error:", e)
        print("Raw output:", output)

        # fallback values
        state.score = 1
        state.feedback = "Good attempt. Try to explain your answer more clearly."

    return state