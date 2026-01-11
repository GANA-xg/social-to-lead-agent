from langchain_core.messages import HumanMessage
from app.nodes.intent import detect_intent

# Try different user messages by changing the content below

state = {
    "messages": [HumanMessage(content="I want to try the Pro plan for my YouTube channel")],
    "intent": None,
    "lead_data": {},
    "lead_complete": False
}

result = detect_intent(state)
print("Detected intent:", result["intent"])