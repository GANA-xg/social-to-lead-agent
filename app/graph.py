from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from app.state import AgentState
from app.nodes.intent import detect_intent
from app.nodes.rag import rag_answer
from app.nodes.lead import lead_qualification


def intent_router(state: AgentState) -> str:
    """
    Route based on detected intent.
    Once high_intent is detected, stay in lead flow.
    """
    if state.get("intent") == "high_intent":
        return "lead"
    if state.get("intent") == "product_pricing":
        return "rag"
    return "greeting"


def greeting_node(state: AgentState) -> AgentState:
    response = (
        "Hi! 👋 I can help you with AutoStream pricing, features, "
        "or help you get started."
    )
    return {
        **state,
        "messages": state["messages"] + [HumanMessage(content=response)]
    }


def build_graph():
    """
    Build and compile the LangGraph agent.
    """
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("intent", detect_intent)
    graph.add_node("rag", rag_answer)
    graph.add_node("greeting", greeting_node)
    graph.add_node("lead", lead_qualification)

    # Entry point
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