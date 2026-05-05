import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import SessionState
from nodes.coach import coach_node
from nodes.evaluator import evaluator_node
from nodes.reporter import reporter_node

state = SessionState(
    session_id="test-1",
    paragraph="The boy found a strange key in the garden."
)

# Step 1: generate question
state = coach_node(state)

# Step 2: simulate answer
state.answer = "It might open something important."

# Step 3: evaluate
state = evaluator_node(state)

# Step 4: report
state = reporter_node(state)

print("\n--- FINAL REPORT ---")
print("Question:", state.question)
print("Answer:", state.answer)
print("Score:", state.score)
print("Feedback:", state.feedback)
print("Summary:", state.final_summary)
print("---------------------\n")