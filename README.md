# Social-to-Lead Agentic Workflow – AutoStream
This project implements a production-style Conversational AI Agent for **ServiceHive’s Inflx platform**.  
The agent converts social conversations into **qualified leads** using intent detection, RAG-based knowledge retrieval, and guarded tool execution.

The fictional SaaS used is **AutoStream**, an automated video editing platform for content creators.


##  Features
- Intent classification (Greeting, Product/Pricing, High-Intent Lead)
- RAG-based product & pricing answers using a local knowledge base
- Multi-turn conversation memory using LangGraph state
- Step-by-step lead qualification (Name, Email, Platform)
- Backend tool execution only after all details are collected
- CLI-based interface for simplicity and evaluation clarity


##  Tech Stack

- **Language:** Python 3.9+
- **Framework:** LangGraph
- **LLM:** GPT-4o-mini (with safe fallback if API quota is unavailable)
- **RAG:** Local Markdown knowledge base
- **Interface:** CLI


##  Project Structure
social-to-lead-agent/
├── app/
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── nodes/
│   │   ├── intent.py
│   │   ├── rag.py
│   │   └── lead.py
│   ├── tools/
│   │   └── lead_capture.py
│   └── knowledge/
│       └── autostream.md
├── requirements.txt
└── README.md

## ▶️ How to Run Locally

### 1. Create & activate virtual environment
(in terminal) for mac or linux
python3 -m venv venv  
source venv/bin/activate

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set OpenAI API key
export OPENAI_API_KEY="your_api_key_here"
 
### 4. Run
PYTHONPATH=. python app/main.py



##  Architecture Explanation 
This project uses LangGraph to implement a state-driven conversational agent, closely matching real-world production patterns used in ServiceHive’s Inflx platform.

The agent maintains a centralized AgentState that stores conversation messages, detected intent, lead information, and completion status. Each user input first passes through an intent detection node, which classifies the message into one of three categories: greeting, product/pricing inquiry, or high-intent lead. This intent is used by a router function to determine the next node in the LangGraph flow.

For product and pricing questions, the agent uses a Retrieval-Augmented Generation (RAG) node that answers strictly from a local Markdown knowledge base, ensuring accurate and non-hallucinated responses. When high intent is detected, the agent enters a lead qualification finite-state flow, collecting the user’s name, email, and creator platform step-by-step.

A mock backend tool (mock_lead_capture) is executed only after all required details are collected, preventing premature or duplicate tool calls. This guarded execution pattern reflects real production safety requirements. The overall architecture emphasizes clarity, deterministic behavior, and real-world deployability over unnecessary complexity.

##  WhatsApp Integration
To integrate this agent with WhatsApp in production, a webhook-based architecture would be used. Incoming WhatsApp messages (via providers like Twilio or Meta WhatsApp Cloud API) would be received by a backend webhook endpoint (e.g., a FastAPI service). Each message would be mapped to a session ID and forwarded to the LangGraph agent with the stored conversation state.

The agent’s response would then be sent back to the user via the WhatsApp API. State persistence can be handled using Redis or a database keyed by user phone number. This design allows the same agent logic to be reused across channels (WhatsApp, web chat, Instagram DMs) while maintaining consistent lead qualification behavior.