def detect_intent(state: dict) -> dict:
    """
    Rule-based intent detection.
    Once high_intent is set, do NOT reclassify.
    """

    # 🔒 Lock intent once lead flow has started
    if state.get("intent") == "high_intent":
        return state

    text = state["messages"][-1].content.lower()

    if any(w in text for w in ["buy", "sign up", "signup", "try", "subscribe", "use"]):
        intent = "high_intent"
    elif any(w in text for w in ["price", "pricing", "plan", "cost", "features", "refund", "support"]):
        intent = "product_pricing"
    else:
        intent = "greeting"

    return {
        **state,
        "intent": intent
    }