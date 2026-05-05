# app.py

import streamlit as st

from state import SessionState
from graph import build_graph

# Build graph once
graph = build_graph()

st.title("ThinkDeep")
st.caption("Every question is a chance to think deeper.")

# Step 1: Input paragraph
paragraph = st.text_area("Enter a paragraph:")

# Step 2: Run coach to generate question
if st.button("Generate Question"):

    state = SessionState(
        session_id="ui-session",
        paragraph=paragraph
    )

    # Only run coach manually (not full graph yet)
    result = graph.invoke(state)

    # Store result in session
    st.session_state["result"] = result


# Step 3: Show question if available
if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Question")
    st.write(result["question"])

    # Step 4: User answer
    answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):

        # Update state with answer
        state = SessionState(**result)
        state.answer = answer

        # Run full graph again (evaluation + report)
        final_result = graph.invoke(state)

        st.subheader("Feedback")
        st.write("Score:", final_result["score"])
        st.write(final_result["feedback"])

        st.subheader("Summary")
        st.write(final_result["final_summary"])