from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from app.nodes.lead import lead_qualification
from app.state import AgentState
from app.nodes.intent import detect_intent
from app.nodes.rag import rag_answer


# ---------- Router Function ----------
def intent_router(state: AgentState) -> str:
    """
    Lock the flow into lead qualification once high intent is detected.
    """
    # If lead flow has started and not completed, stay in lead node
    if state.get("intent") == "high_intent" and not state.get("lead_complete"):
        return "lead"

    if state.get("intent") == "product_pricing":
        return "rag"

    return "greeting"


# ---------- Greeting Node ----------
def greeting_node(state: AgentState) -> AgentState:
    response = (
        "Hi! 👋 I can help you with AutoStream pricing, features, "
        "or help you get started."
    )

    return {
        **state,
        "messages": state["messages"] + [HumanMessage(content=response)]
    }


# ---------- Lead Placeholder Node ----------
    """
    Temporary placeholder.
    We will implement full lead collection next.
    """
    response = (
        "Great! I can help you get started. "
        "I’ll need a few details from you."
    )

    return {
        **state,
        "messages": state["messages"] + [HumanMessage(content=response)]
    }


# ---------- Build Graph ----------
def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("intent", detect_intent)
    graph.add_node("rag", rag_answer)
    graph.add_node("greeting", greeting_node)
    graph.add_node("lead", lead_qualification)

    # Entry
    graph.set_entry_point("intent")

    # Routing
    graph.add_conditional_edges(
        "intent",
        intent_router,
        {
            "rag": "rag",
            "greeting": "greeting",
            "lead": "lead",
        },
    )

    # End states
    graph.add_edge("rag", END)
    graph.add_edge("greeting", END)
    graph.add_edge("lead", END)

    return graph.compile()