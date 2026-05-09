# app.py
#
# Streamlit UI for ThinkDeep — Story Mode.
#
# Key fix vs previous version:
#   coach_node and evaluator_node are called DIRECTLY here, not through the
#   full graph. This prevents coach from re-running (and re-generating a new
#   question) when the user submits an answer — which was causing the evaluator
#   to score the answer against the wrong question.
#
# Flow:
#   Catalog → pick story → Start Story
#   → show chunk → Generate Question (coach_node)
#   → user answers → Submit Answer (evaluator_node)
#   → feedback → Next Part → repeat → Story Complete
#
# Future LangSmith tracing point: wrap each node call with a named run context.

import os
import streamlit as st

from state import SessionState
from nodes.coach import coach_node
from nodes.evaluator import evaluator_node
from stories import STORIES, load_story_text, make_chunks

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="ThinkDeep", page_icon="📖", layout="centered")
st.title("📖 ThinkDeep")
st.caption("Every question is a chance to think deeper.")

# Force all book cover images to the same fixed height so tiles are uniform
st.markdown(
    """
    <style>
    [data-testid="stImage"] img {
        height: 220px;
        object-fit: cover;
        width: 100%;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Helper: clear all story-related session state keys
# ---------------------------------------------------------------------------
def clear_story_state():
    for key in ["chunks", "current_index", "story_title", "story_key",
                "phase", "question", "feedback", "score"]:
        st.session_state.pop(key, None)


# ---------------------------------------------------------------------------
# SECTION 1 — Book Catalog
# Show 3 book cards with cover images. Only shown when no story is active.
# ---------------------------------------------------------------------------
if "chunks" not in st.session_state:

    st.subheader("Choose a Story")
    st.write("")  # small spacer

    cols = st.columns(3)

    for col, (story_key, meta) in zip(cols, STORIES.items()):
        with col:
            cover_path = meta["cover"]

            # Show cover image if available, otherwise a placeholder
            if os.path.exists(cover_path):
                st.image(cover_path, use_container_width=True)
            else:
                # Placeholder until the user drops images into images/
                st.markdown(
                    "<div style='height:180px; background:#e8e8e8; "
                    "border-radius:8px; display:flex; align-items:center; "
                    "justify-content:center; color:#999; font-size:13px'>"
                    "Cover coming soon</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(f"**{meta['title']}**")
            st.caption(meta["description"])

            if st.button("Read", key=f"start_{story_key}"):
                full_text = load_story_text(story_key)
                chunks = make_chunks(full_text, target_chunks=5)

                st.session_state["chunks"] = chunks
                st.session_state["current_index"] = 0
                st.session_state["story_title"] = meta["title"]
                st.session_state["story_key"] = story_key
                st.session_state["phase"] = "reading"
                st.session_state["question"] = ""
                st.session_state["feedback"] = ""
                st.session_state["score"] = 0
                st.rerun()


# ---------------------------------------------------------------------------
# SECTION 2 — Story Progression
# Only rendered once a story is loaded into session state.
# ---------------------------------------------------------------------------
else:
    chunks = st.session_state["chunks"]
    idx = st.session_state["current_index"]
    total = len(chunks)

    # --- Top bar: title + back button ---
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.subheader(st.session_state["story_title"])
    with col_back:
        if st.button("← Catalog"):
            clear_story_state()
            st.rerun()

    # --- Story complete screen ---
    if idx >= total:
        st.progress(1.0)
        st.success("🎉 Story Complete!")
        st.write(f"You finished **{st.session_state['story_title']}**. Great work!")
        st.info("Reflection: What was the most important lesson in this story?")

        if st.button("Back to Catalog"):
            clear_story_state()
            st.rerun()

    else:
        current_chunk = chunks[idx]

        # Progress bar
        st.caption(f"Part {idx + 1} of {total}")
        st.progress(idx / total)
        st.divider()

        # Show current chunk only
        st.write(current_chunk)
        st.divider()

        # -------------------------------------------------------------------
        # PHASE: reading — user clicks to generate a question
        # -------------------------------------------------------------------
        if st.session_state["phase"] == "reading":

            if st.button("Generate Question"):
                with st.spinner("Thinking of a question…"):
                    # Call coach_node directly so it doesn't pollute graph state
                    # Future LangSmith trace point: add run name here
                    state = SessionState(
                        session_id="ui-session",
                        paragraph=current_chunk,
                    )
                    state = coach_node(state)

                st.session_state["question"] = state.question
                st.session_state["phase"] = "answering"
                st.rerun()

        # -------------------------------------------------------------------
        # PHASE: answering — show question, collect answer
        # -------------------------------------------------------------------
        if st.session_state["phase"] in ("answering", "evaluated"):

            st.subheader("Question")
            st.write(st.session_state["question"])

            if st.session_state["phase"] == "answering":
                answer = st.text_area(
                    "Your answer:",
                    key=f"answer_{idx}",
                    placeholder="Write a few sentences…",
                )

                if st.button("Submit Answer"):
                    if not answer.strip():
                        st.warning("Please write an answer before submitting.")
                    else:
                        with st.spinner("Evaluating your answer…"):
                            # Call evaluator_node directly with the SAME question
                            # the user saw — avoids the coach-reruns bug
                            state = SessionState(
                                session_id="ui-session",
                                paragraph=current_chunk,
                                question=st.session_state["question"],
                                answer=answer.strip(),
                            )
                            state = evaluator_node(state)

                        st.session_state["score"] = state.score
                        st.session_state["feedback"] = state.feedback
                        st.session_state["phase"] = "evaluated"
                        st.rerun()

            # ---------------------------------------------------------------
            # PHASE: evaluated — show score + feedback, offer Next
            # ---------------------------------------------------------------
            if st.session_state["phase"] == "evaluated":

                score = st.session_state["score"]

                # Visual score indicator
                score_labels = {0: "❌ Incorrect", 1: "🟡 Partially correct", 2: "✅ Great answer"}
                st.subheader("Feedback")
                st.markdown(f"**{score_labels.get(score, str(score))}** ({score}/2)")
                st.write(st.session_state["feedback"])

                next_label = "Finish Story 🎉" if (idx + 1 >= total) else "Next Part →"

                if st.button(next_label):
                    st.session_state["current_index"] += 1
                    st.session_state["phase"] = "reading"
                    st.session_state["question"] = ""
                    st.session_state["feedback"] = ""
                    st.session_state["score"] = 0
                    st.rerun()
