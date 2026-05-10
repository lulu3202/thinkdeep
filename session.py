# session.py
#
# Pure Python session history management.
# Intentionally decoupled from Streamlit — this module has no st.* imports
# so it can be imported directly by a FastAPI backend in the future.
#
# History is a plain list of dicts that lives in st.session_state["history"]
# on the Streamlit side. This module only transforms and reads that list.

from datetime import datetime


def new_reflection(
    theme: str,
    culture: str,
    proverb: str,
    question: str,
    user_reflection: str,
    ai_response: str,
) -> dict:
    """
    Creates a single reflection record.
    Call this after the user submits a reflection and the AI responds.
    """
    return {
        "theme": theme,
        "culture": culture,
        "proverb": proverb,
        "question": question,
        "user_reflection": user_reflection,
        "ai_response": ai_response,
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
    }


def get_themes_explored(history: list) -> list[str]:
    """Returns a deduplicated list of themes explored in this session."""
    return list(dict.fromkeys(e["theme"] for e in history))


def get_summary_context(history: list) -> str:
    """
    Formats session history into a compact string for the reporter node.
    Keeps it concise to avoid long prompts.
    """
    if not history:
        return ""

    lines = []
    for i, entry in enumerate(history, 1):
        lines.append(
            f"{i}. [{entry['theme']} — {entry['culture']}]\n"
            f"   Proverb: \"{entry['proverb']}\"\n"
            f"   Reflection: {entry['user_reflection'][:200]}"
            f"{'…' if len(entry['user_reflection']) > 200 else ''}"
        )
    return "\n\n".join(lines)
