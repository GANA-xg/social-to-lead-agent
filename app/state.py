from typing import List, Optional, Dict
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    Central conversation state for the agent.
    LangGraph will pass this between nodes.
    """
    messages: List[BaseMessage]

    # Detected intent for latest user message
    intent: Optional[str]

    # Lead capture fields
    lead_data: Dict[str, Optional[str]]

    # Whether lead is fully captured
    lead_complete: bool