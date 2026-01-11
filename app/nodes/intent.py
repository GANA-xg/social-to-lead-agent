from langchain_openai import ChatOpenAI


def detect_intent(state: dict) -> dict:
    """
    Classify user intent into:
    - greeting
    - product_pricing
    - high_intent
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    user_message = state["messages"][-1].content

    prompt = f"""
You are an intent classifier for a SaaS sales assistant.

Classify the user's message into exactly ONE of the following:
- greeting
- product_pricing
- high_intent

Rules:
- greeting: hello, hi, casual talk
- product_pricing: asking about features, pricing, plans, policies
- high_intent: wants to sign up, try, buy, use for their channel

Respond with ONLY the intent label.

User message:
{user_message}
"""

    try:
        response = llm.invoke(prompt)
        intent = response.content.strip().lower()
    except Exception:
        # Safe fallback if API quota fails
        msg = user_message.lower()
        if any(word in msg for word in ["buy", "sign up", "try", "use", "subscribe"]):
            intent = "high_intent"
        elif any(word in msg for word in ["price", "plan", "cost", "features"]):
            intent = "product_pricing"
        else:
            intent = "greeting"

    # If intent already high_intent, do NOT reclassify
    if state.get("intent") == "high_intent":
        return state

    return {
        **state,
        "intent": intent
    }