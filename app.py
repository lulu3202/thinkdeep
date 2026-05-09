# app.py
#
# ThinkDeep — Streamlit UI supporting Story Mode, Science Mode, and Wisdom Mode.
#
# Top-level routing:
#   "wisdom_entry" in session_state  → Wisdom interaction view
#   "chunks" in session_state        → Story/Science chunk progression (unchanged)
#   neither                          → Catalog tabs (Story / Science / Wisdom)
#
# Wisdom Mode is intentionally different from Story/Science:
#   - No chunking or linear progression
#   - User picks a theme, sees one proverb, reflects freely
#   - evaluator_node returns a conversational reflection (no score)
#   - User can explore another theme at any time
#
# Future LangSmith tracing point: wrap node calls with named run contexts per mode.

import os
import random
import streamlit as st

from state import SessionState
from nodes.coach import coach_node
from nodes.evaluator import evaluator_node
from stories import STORIES, load_story_text, make_chunks
from science_topics import TOPICS, load_topic_text
from wisdom.wisdom_entries import get_themes, get_entries_by_theme

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
# Helpers: clear session state
# ---------------------------------------------------------------------------
def clear_session():
    """Clears story/science chunk progression state."""
    for key in ["chunks", "current_index", "content_title", "content_key",
                "app_mode", "phase", "question", "feedback", "score"]:
        st.session_state.pop(key, None)


def clear_wisdom_session():
    """Clears wisdom interaction state."""
    for key in ["wisdom_entry", "wisdom_phase", "wisdom_feedback"]:
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
# SECTION 1 — Wisdom Mode interaction view
# Routed here when a wisdom entry has been selected.
# Completely separate from the chunk-based story/science flow.
# ---------------------------------------------------------------------------
if "wisdom_entry" in st.session_state:

    entry = st.session_state["wisdom_entry"]
    phase = st.session_state.get("wisdom_phase", "reading")

    # Top bar
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.subheader(f"🌿 {entry['theme']}")
        st.caption(entry["culture"])
    with col_back:
        if st.button("← Wisdom"):
            clear_wisdom_session()
            st.rerun()

    st.divider()

    # Display the proverb prominently
    st.markdown(
        f"<p style='font-size:22px; font-style:italic; "
        f"line-height:1.6; color:#2c2c2c;'>\"{entry['proverb']}\"</p>",
        unsafe_allow_html=True,
    )
    st.write("")

    # Reflective question
    st.markdown(f"**{entry['question']}**")
    st.write("")

    if phase == "reading":
        answer = st.text_area(
            "Your reflection:",
            placeholder="There's no right answer here — just share what comes to mind.",
            key="wisdom_answer",
        )

        if st.button("Share Reflection"):
            if not answer.strip():
                st.warning("Write something — even a few words.")
            else:
                with st.spinner("Reflecting…"):
                    # Use evaluator_node in wisdom mode — returns conversational feedback, no score
                    state = SessionState(
                        session_id="ui-session",
                        mode="wisdom",
                        paragraph=entry["proverb"],   # proverb as the "passage"
                        question=entry["question"],
                        answer=answer.strip(),
                    )
                    state = evaluator_node(state)

                st.session_state["wisdom_feedback"] = state.feedback
                st.session_state["wisdom_phase"] = "reflected"
                st.rerun()

    elif phase == "reflected":
        # Show the AI's conversational reflection
        st.markdown("---")
        st.markdown("*A thought in return:*")
        st.write(st.session_state["wisdom_feedback"])
        st.write("")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Explore Another"):
                clear_wisdom_session()
                st.rerun()
        with col_b:
            if st.button("Back to Catalog"):
                clear_wisdom_session()
                st.rerun()


# ---------------------------------------------------------------------------
# SECTION 2 — Catalog view (no active session)
# ---------------------------------------------------------------------------
elif "chunks" not in st.session_state:

    # Three-mode tab selector
    tab_story, tab_science, tab_wisdom = st.tabs(
        ["📚 Story Mode", "🔭 Science Mode", "🌿 Wisdom Mode"]
    )

    with tab_story:
        st.subheader("Choose a Story")
        st.write("")
        render_catalog(STORIES, load_story_text, mode_value="reading")

    with tab_science:
        st.subheader("Choose a Science Topic")
        st.write("")
        render_catalog(TOPICS, load_topic_text, mode_value="science")

    with tab_wisdom:
        st.subheader("Explore Human Wisdom")
        st.caption("Choose a theme. Discover a proverb. Reflect freely.")
        st.write("")

        themes = get_themes()  # sorted list of all themes

        # Theme buttons rendered as a flowing grid (3 per row)
        cols_per_row = 3
        rows = [themes[i : i + cols_per_row] for i in range(0, len(themes), cols_per_row)]

        for row in rows:
            cols = st.columns(cols_per_row)
            for col, theme in zip(cols, row):
                with col:
                    if st.button(theme, key=f"theme_{theme}", use_container_width=True):
                        # Pick a random entry from this theme
                        entries = get_entries_by_theme(theme)
                        chosen = random.choice(entries)
                        st.session_state["wisdom_entry"] = chosen
                        st.session_state["wisdom_phase"] = "reading"
                        st.rerun()


# ---------------------------------------------------------------------------
# SECTION 3 — Story / Science chunk progression (active session)
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
