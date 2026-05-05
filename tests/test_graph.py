import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import SessionState
from graph import build_graph

graph = build_graph()

state = SessionState(
    session_id="test-1",
    paragraph="The boy found a strange key in the garden."
)

# simulate user answer BEFORE running evaluator
state.answer = "It might open something important."

result = graph.invoke(state)

print("\n--- GRAPH OUTPUT ---")
print("Question:", result["question"])
print("Answer:", result["answer"])
print("Score:", result["score"])
print("Feedback:", result["feedback"])
print("Summary:", result["final_summary"])
print("---------------------\n")