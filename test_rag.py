from langchain_core.messages import HumanMessage
from app.nodes.rag import rag_answer

state = {
    "messages": [HumanMessage(content="What is the price of the Pro plan?")]
}

result = rag_answer(state)
print(result["messages"][-1].content)