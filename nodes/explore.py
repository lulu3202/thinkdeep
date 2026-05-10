# nodes/explore.py
#
# Explore Deeper node — generates a contextual follow-up response after
# the evaluator has given feedback, allowing the user to dig further.
#
# Design decisions:
#   - Takes all context as arguments (not just state) because explore is a
#     side-conversation, not a state transition. We don't overwrite the main
#     session fields (paragraph, question, answer, feedback).
#   - Returns a plain string — the caller (app.py) stores it in explore_history.
#   - Mode-aware: story = character/theme, science = concept curiosity,
#     wisdom = interpretation/life reflection.
#   - Conversation history is passed in so the model sees prior turns and
#     doesn't repeat itself.
#
# Future LangSmith tracing point: tag runs with mode + turn number.

from langsmith import traceable
import ollama
from config import MODEL_NAME

MAX_TURNS = 3  # soft cap — UI still shows exit buttons after this


# --- Mode-specific system contexts ---

STORY_SYSTEM = """You are a warm literary companion helping someone think more deeply about a story.
You have already seen their initial reflection and the feedback they received.
Your role now is to go one layer deeper — explore character motivation, theme, emotion, or meaning.
Keep responses to 2-4 sentences. Be curious, not instructional."""

SCIENCE_SYSTEM = """You are an enthusiastic science guide helping someone explore a concept further.
You have already seen their initial thinking and the feedback they received.
Your role is to extend their curiosity — offer a related phenomenon, ask a what-if, or connect the idea to something surprising.
Keep responses to 2-4 sentences. Be exploratory, not textbook-like."""

WISDOM_SYSTEM = """You are a calm and thoughtful conversation partner helping someone sit with a piece of wisdom.
You have already seen their initial reflection and responded once.
Your role now is to deepen the conversation — offer a different angle, a related idea from another culture, or a gentle question.
Keep responses to 2-4 sentences. Be warm and unhurried."""

SYSTEM_BY_MODE = {
    "reading": STORY_SYSTEM,
    "science": SCIENCE_SYSTEM,
    "wisdom": WISDOM_SYSTEM,
}


def _build_messages(mode, paragraph, question, original_answer,
                    evaluator_feedback, explore_history, user_message):
    """
    Builds the message list for the Ollama chat call.
    Includes: system context, original Q&A, prior explore turns, new user message.
    """
    system = SYSTEM_BY_MODE.get(mode, STORY_SYSTEM)

    # Summarise the original interaction as a system-level briefing
    briefing = (
        f"Original passage/proverb:\n{paragraph}\n\n"
        f"Question asked: {question}\n"
        f"User's answer: {original_answer}\n"
        f"Feedback given: {evaluator_feedback}"
    )

    messages = [
        {"role": "system", "content": f"{system}\n\n---\n{briefing}"},
    ]

    # Replay prior explore turns so the model has conversation memory
    for turn in explore_history:
        messages.append({"role": "user",    "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["ai"]})

    # The new user message
    messages.append({"role": "user", "content": user_message})

    return messages


@traceable
def explore_node(
    mode: str,
    paragraph: str,
    question: str,
    original_answer: str,
    evaluator_feedback: str,
    explore_history: list,
    user_message: str,
) -> str:
    """
    Generates one contextual follow-up response for the Explore Deeper flow.

    Returns a plain string (the AI response).
    The caller appends {"user": user_message, "ai": response} to explore_history.
    """

    print(f"explore_node — mode: {mode} — turn: {len(explore_history) + 1} — model: {MODEL_NAME}")

    messages = _build_messages(
        mode, paragraph, question, original_answer,
        evaluator_feedback, explore_history, user_message,
    )

    response = ollama.chat(model=MODEL_NAME, messages=messages)
    return response["message"]["content"].strip()
