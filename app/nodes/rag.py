from langchain_core.messages import AIMessage


def rag_answer(state: dict) -> dict:
    """
    Deterministic RAG using local knowledge.
    NO OpenAI, NO LLM.
    """

    text = state["messages"][-1].content.lower()

    if "pro" in text:
        answer = (
            "The Pro Plan costs $79/month and includes unlimited videos, "
            "4K resolution, AI captions, and 24/7 support."
        )
    elif "basic" in text:
        answer = (
            "The Basic Plan costs $29/month and includes 10 videos/month "
            "at 720p resolution."
        )
    elif "price" in text or "pricing" in text or "plan" in text:
        answer = (
            "AutoStream offers two plans:\n"
            "- Basic: $29/month, 10 videos/month, 720p\n"
            "- Pro: $79/month, unlimited videos, 4K, AI captions"
        )
    elif "refund" in text:
        answer = "AutoStream does not offer refunds after 7 days."
    elif "support" in text:
        answer = "24/7 support is available only on the Pro plan."
    else:
        answer = "I can help you with AutoStream pricing and plans."

    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=answer)]
    }
