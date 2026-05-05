import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# test_coach.py

# Import your state and node
from state import SessionState
from nodes.coach import coach_node

# Create a test input
state = SessionState(
    session_id="test-1",
    paragraph="The boy found a strange key in the garden."
)

# Run the coach node
state = coach_node(state)

# Print output clearly
print("\n--- OUTPUT ---")
print("Question:", state.question)
print("-------------\n")