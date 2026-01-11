from langchain_core.messages import AIMessage
from app.tools.lead_capture import mock_lead_capture


def lead_qualification(state: dict) -> dict:
    """
    Collects lead info step-by-step and triggers tool only when complete.
    """

    lead_data = state["lead_data"]
    messages = state["messages"]

    # Step 1: Ask for Name
    if lead_data.get("name") is None:
        return {
            **state,
            "messages": messages + [AIMessage(content="Great! What's your name?")]
        }

    # Step 2: Ask for Email
    if lead_data.get("email") is None:
        return {
            **state,
            "messages": messages + [AIMessage(content="Thanks! What's your email address?")]
        }

    # Step 3: Ask for Platform
    if lead_data.get("platform") is None:
        return {
            **state,
            "messages": messages + [AIMessage(content="Which platform do you create content on? (YouTube, Instagram, etc.)")]
        }

    # Step 4: Trigger Tool (ONLY ONCE)
    if not state["lead_complete"]:
        mock_lead_capture(
            name=lead_data["name"],
            email=lead_data["email"],
            platform=lead_data["platform"]
        )

        return {
            **state,
            "lead_complete": True,
            "messages": messages + [
                AIMessage(content="🎉 You're all set! Our team will reach out to you shortly.")
            ]
        }

    return state