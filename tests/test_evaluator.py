# tests/test_evaluator.py

import sys
import os

# Add project root to path (so imports work)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import SessionState
from nodes.coach import coach_node
from nodes.evaluator import evaluator_node

# Step 1: Create initial state
state = SessionState(
    session_id="test-1",
    paragraph="The boy found a strange key in the garden."
)

print("\n--- STEP 1: GENERATE QUESTION ---")
state = coach_node(state)
print("Question:", state.question)

# Step 2: Simulate a user answer
print("\n--- STEP 2: USER ANSWER ---")
state.answer = "It might open something important."
print("Answer:", state.answer)

# Step 3: Evaluate answer
print("\n--- STEP 3: EVALUATION ---")
state = evaluator_node(state)

print("\n--- FINAL OUTPUT ---")
print("Question:", state.question)
print("Answer:", state.answer)
print("Score:", state.score)
print("Feedback:", state.feedback)
print("---------------------\n")