from langchain_core.messages import HumanMessage
from app.graph import build_graph


def main():
    app = build_graph()

    state = {
        "messages": [],
        "intent": None,
        "lead_data": {
            "name": None,
            "email": None,
            "platform": None,
        },
        "lead_complete": False,
    }

    print("AutoStream Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # Store lead info if we are in high-intent flow
        if state["intent"] == "high_intent":
            if state["lead_data"]["name"] is None:
                state["lead_data"]["name"] = user_input
            elif state["lead_data"]["email"] is None:
                state["lead_data"]["email"] = user_input
            elif state["lead_data"]["platform"] is None:
                state["lead_data"]["platform"] = user_input

        # Add user message
        state["messages"].append(HumanMessage(content=user_input))

        # Invoke LangGraph
        state = app.invoke(state)

        # Print agent response
        print("Agent:", state["messages"][-1].content)


if __name__ == "__main__":
    main()