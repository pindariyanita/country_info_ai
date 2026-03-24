from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import extract_intent, call_api, synthesize_answer

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("intent", extract_intent)
    builder.add_node("api", call_api)
    builder.add_node("synthesis", synthesize_answer)

    builder.set_entry_point("intent")

    builder.add_edge("intent", "api")
    builder.add_edge("api", "synthesis")
    builder.add_edge("synthesis", END)

    return builder.compile()