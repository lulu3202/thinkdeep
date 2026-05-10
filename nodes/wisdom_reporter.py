# nodes/wisdom_reporter.py
#
# Generates a warm, personalised reflection summary from the session history.
# Called when the user clicks "Generate Reflection Summary".
#
# Streaming version (stream_wisdom_report) is used in app.py for perceived speed.
# Non-streaming version kept for future API use.
#
# Future LangSmith tracing point: tag with session_id and theme list.

from langsmith import traceable
import ollama
from config import MODEL_NAME


REPORT_PROMPT = """You are a thoughtful guide who has been listening carefully to someone's reflections.

They have explored the following wisdom themes today:

{summary_context}

Your role:
- Write a warm, personal 3-4 sentence reflection summary
- Notice any recurring ideas or values across their reflections
- Point to something meaningful you observed in how they think
- End with one gentle question or invitation for continued reflection
- Avoid sounding like a school report — this should feel like a letter from a wise friend

Write only the summary. No labels, no bullet points.
"""


@traceable
def wisdom_reporter_node(summary_context: str) -> str:
    """
    Generates a reflection summary from the session history context.
    Returns a plain string.
    """
    print(f"wisdom_reporter_node — model: {MODEL_NAME}")

    prompt = REPORT_PROMPT.format(summary_context=summary_context)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()


def stream_wisdom_report(summary_context: str):
    """
    Streaming generator version — use with st.write_stream().
    The caller captures the full string from st.write_stream().

    # Future FastAPI note: convert to async generator for streaming HTTP response.
    """
    print(f"stream_wisdom_report — model: {MODEL_NAME}")

    prompt = REPORT_PROMPT.format(summary_context=summary_context)

    for chunk in ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        yield chunk["message"]["content"]
