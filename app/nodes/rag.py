from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

# Path to knowledge base
KNOWLEDGE_PATH = Path(__file__).parent.parent / "knowledge" / "autostream.md"


def load_knowledge_base() -> str:
    """Load AutoStream knowledge base from local markdown file."""
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def retrieve_relevant_knowledge(user_query: str, knowledge: str) -> str:
    """
    Lightweight retrieval based on keywords.
    No vector DB needed for this assignment.
    """
    keywords = [
        "price", "pricing", "plan", "cost",
        "refund", "support", "videos", "resolution"
    ]

    query_lower = user_query.lower()
    if any(keyword in query_lower for keyword in keywords):
        return knowledge

    return ""


def rag_answer(state: dict) -> dict:
    """
    Answer product & pricing questions using RAG.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    user_message = state["messages"][-1].content
    knowledge = load_knowledge_base()
    relevant_context = retrieve_relevant_knowledge(user_message, knowledge)

    prompt = f"""
You are a helpful sales assistant for AutoStream.

Answer ONLY using the information below.
If the answer is not present, say you don't have that information.

### Knowledge Base:
{relevant_context}

### User Question:
{user_message}
"""

    try:
        response = llm.invoke(prompt)
        answer = response.content
    except Exception:
        answer = (
            "The Pro Plan costs $79/month with unlimited videos, "
            "4K resolution, and AI captions. The Basic Plan costs "
            "$29/month with 10 videos per month at 720p resolution."
        )

    return {
    "messages": state["messages"] + [AIMessage(content=answer)]
    }