# nodes/coach.py

from langsmith import traceable
import ollama

# Import model config
from config import MODEL_NAME

@traceable
def coach_node(state):
    """
    Generates one thoughtful question from the paragraph
    """

    # Debug print (helps you see where it is)
    print("Calling model:", MODEL_NAME)

    # Prompt
    prompt = f"""
    You are a thoughtful tutor helping a child think deeply.

    Read the paragraph and ask exactly ONE question.

    Paragraph:
    {state.paragraph}

    Rules:
    - Ask only one question
    - Keep it simple
    - Encourage thinking

    Output only the question.
    """

    # Call model from config
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract response
    state.question = response["message"]["content"].strip()

    return state