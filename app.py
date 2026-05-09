# app.py
#
# ThinkDeep — Streamlit UI supporting Story Mode and Science Mode.
#
# Top-level flow:
#   1. User picks a mode (Story / Science) via tab selector
#   2. Story Mode  → book catalog   → story progression
#      Science Mode → topic catalog → topic progression
#   3. The progression section is IDENTICAL for both modes:
#      display chunk → coach_node question → user answer → evaluator_node feedback → next chunk
#   4. Nodes are mode-aware: state.mode drives the prompt style inside each node.
#
# Key architecture decision:
#   coach_node and evaluator_node are called DIRECTLY here (not through graph.invoke)
#   so the coach does not re-run and overwrite the question when the user submits an answer.
#
# Future LangSmith tracing point: wrap node calls with named run contexts per mode + topic.

import os
import streamlit as st

from state import SessionState
from nodes.coach import coach_node
from nodes.evaluator import evaluator_node
from stories import STORIES, load_story_text, make_chunks
from science_topics import TOPICS, load_topic_text

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="ThinkDeep", page_icon="📖", layout="centered")

# Uniform cover image height across all catalog cards
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

st.title("📖 ThinkDeep")
st.caption("Every question is a chance to think deeper.")


# ---------------------------------------------------------------------------
# Helper: wipe all chunk/progression state when leaving a session
# ---------------------------------------------------------------------------
def clear_session():
    for key in ["chunks", "current_index", "content_title", "content_key",
                "app_mode", "phase", "question", "feedback", "score"]:
        st.session_state.pop(key, None)


# ---------------------------------------------------------------------------
# Helper: render a catalog grid (used by both Story Mode and Science Mode)
#
# catalog     — dict of {key: {title, file, cover, description}}
# load_fn     — function that loads full text given a key
# mode_value  — "reading" or "science" — stored in SessionState.mode
# ---------------------------------------------------------------------------
def render_catalog(catalog: dict, load_fn, mode_value: str):
    cols = st.columns(len(catalog))

    for col, (key, meta) in zip(cols, catalog.items()):
        with col:
            cover_path = meta.get("cover", "")

            if os.path.exists(cover_path):
                st.image(cover_path, use_container_width=True)
            else:
                st.markdown(
                    "<div style='height:220px; background:#e8e8e8; border-radius:6px;"
                    "display:flex; align-items:center; justify-content:center;"
                    "color:#999; font-size:13px'>Cover coming soon</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(f"**{meta['title']}**")
            st.caption(meta["description"])

            if st.button("Start", key=f"start_{mode_value}_{key}"):
                full_text = load_fn(key)
                chunks = make_chunks(full_text, target_chunks=5)

                st.session_state["chunks"] = chunks
                st.session_state["current_index"] = 0
                st.session_state["content_title"] = meta["title"]
                st.session_state["content_key"] = key
                st.session_state["app_mode"] = mode_value
                st.session_state["phase"] = "reading"
                st.session_state["question"] = ""
                st.session_state["feedback"] = ""
                st.session_state["score"] = 0
                st.rerun()


# ---------------------------------------------------------------------------
# SECTION 1 — Catalog view (no active session)
# ---------------------------------------------------------------------------
if "chunks" not in st.session_state:

    # Mode selector tabs — clean and minimal
    tab_story, tab_science = st.tabs(["📚 Story Mode", "🔭 Science Mode"])

    with tab_story:
        st.subheader("Choose a Story")
        st.write("")
        render_catalog(STORIES, load_story_text, mode_value="reading")

    with tab_science:
        st.subheader("Choose a Science Topic")
        st.write("")
        render_catalog(TOPICS, load_topic_text, mode_value="science")


# ---------------------------------------------------------------------------
# SECTION 2 — Progression view (active session)
# This section is identical regardless of mode — the nodes handle the difference.
# ---------------------------------------------------------------------------
else:
    chunks = st.session_state["chunks"]
    idx = st.session_state["current_index"]
    total = len(chunks)
    mode = st.session_state["app_mode"]          # "reading" or "science"

    # --- Top bar: title + back button ---
    col_title, col_back = st.columns([4, 1])
    with col_title:
        icon = "🔭" if mode == "science" else "📚"
        st.subheader(f"{icon} {st.session_state['content_title']}")
    with col_back:
        if st.button("← Back"):
            clear_session()
            st.rerun()

    # --- Story / topic complete ---
    if idx >= total:
        st.progress(1.0)
        st.success("🎉 Complete!")
        st.write(f"You finished **{st.session_state['content_title']}**. Great thinking!")

        if mode == "science":
            st.info("Reflection: What was the most surprising idea in this topic?")
        else:
            st.info("Reflection: What was the most important lesson in this story?")

        if st.button("Back to Catalog"):
            clear_session()
            st.rerun()

    else:
        current_chunk = chunks[idx]

        # Progress bar
        st.caption(f"Part {idx + 1} of {total}")
        st.progress(idx / total)
        st.divider()

        # Display current chunk only
        st.write(current_chunk)
        st.divider()

        # ---------------------------------------------------------------
        # PHASE: reading — generate a question
        # ---------------------------------------------------------------
        if st.session_state["phase"] == "reading":

            btn_label = "Generate Question" if mode == "reading" else "Ask Me Something"

            if st.button(btn_label):
                with st.spinner("Thinking of a question…"):
                    state = SessionState(
                        session_id="ui-session",
                        mode=mode,               # coach_node uses this to pick prompt
                        paragraph=current_chunk,
                    )
                    state = coach_node(state)

                st.session_state["question"] = state.question
                st.session_state["phase"] = "answering"
                st.rerun()

        # ---------------------------------------------------------------
        # PHASE: answering — show question, collect answer
        # ---------------------------------------------------------------
        if st.session_state["phase"] in ("answering", "evaluated"):

            st.subheader("Question")
            st.write(st.session_state["question"])

            if st.session_state["phase"] == "answering":
                placeholder = (
                    "Share your thoughts — there's no single right answer here."
                    if mode == "science"
                    else "Write a few sentences…"
                )
                answer = st.text_area(
                    "Your answer:",
                    key=f"answer_{idx}",
                    placeholder=placeholder,
                )

                if st.button("Submit Answer"):
                    if not answer.strip():
                        st.warning("Please write something before submitting.")
                    else:
                        with st.spinner("Evaluating your answer…"):
                            state = SessionState(
                                session_id="ui-session",
                                mode=mode,           # evaluator_node uses this to pick prompt
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
                score_labels = {
                    0: "❌ Not quite",
                    1: "🟡 Getting there",
                    2: "✅ Great thinking",
                }

                st.subheader("Feedback")
                st.markdown(f"**{score_labels.get(score, str(score))}** ({score}/2)")
                st.write(st.session_state["feedback"])

                next_label = "Finish 🎉" if (idx + 1 >= total) else "Next Part →"

                if st.button(next_label):
                    st.session_state["current_index"] += 1
                    st.session_state["phase"] = "reading"
                    st.session_state["question"] = ""
                    st.session_state["feedback"] = ""
                    st.session_state["score"] = 0
                    st.rerun()
