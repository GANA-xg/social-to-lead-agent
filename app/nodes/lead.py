from langchain_core.messages import AIMessage
from app.tools.lead_capture import mock_lead_capture


def lead_qualification(state: dict) -> dict:
    """
    Lead qualification finite-state machine.
    Collects name → email → platform and triggers tool ONLY when complete.
    """

    lead_data = state["lead_data"]
    messages = state["messages"]

    # Ask for name
    if lead_data.get("name") is None:
        return {
            **state,
            "messages": messages + [
                AIMessage(content="Great! What's your name?")
            ]
        }

    # Ask for email
    if lead_data.get("email") is None:
        return {
            **state,
            "messages": messages + [
                AIMessage(content="Thanks! What's your email address?")
            ]
        }

    # Ask for platform
    if lead_data.get("platform") is None:
        return {
            **state,
            "messages": messages + [
                AIMessage(
                    content="Which platform do you create content on? (YouTube, Instagram, etc.)"
                )
            ]
        }

    # Trigger tool ONLY once
    if not state.get("lead_complete", False):
        mock_lead_capture(
            name=lead_data["name"],
            email=lead_data["email"],
            platform=lead_data["platform"]
        )

        return {
            **state,
            "lead_complete": True,
            "messages": messages + [
                AIMessage(
                    content="🎉 You're all set! Our team will reach out to you shortly."
                )
            ]
        }

    return state