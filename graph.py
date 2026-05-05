# graph.py

from langgraph.graph import StateGraph, END
from state import SessionState

from nodes.coach import coach_node
from nodes.evaluator import evaluator_node
from nodes.reporter import reporter_node


def build_graph():
    builder = StateGraph(SessionState)

    # Add nodes
    builder.add_node("coach", coach_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("reporter", reporter_node)

    # Define flow
    builder.set_entry_point("coach")

    builder.add_edge("coach", "evaluator")
    builder.add_edge("evaluator", "reporter")
    builder.add_edge("reporter", END)

    return builder.compile()