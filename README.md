Project Synapse: Agentic Last-Mile Coordinator (Proof-of-Concept)
This repository contains the functional proof-of-concept (PoC) for Project Synapse, an autonomous AI agent designed to resolve last-mile delivery disruptions.

1. Overview
This application demonstrates an AI agent that can autonomously handle complex delivery scenarios described in natural language. It accepts a disruption scenario as a command-line argument, and the agent then uses a predefined set of simulated tools to reason about the problem and devise a multi-step resolution plan.

The core of this PoC is built using LangGraph, a framework for creating stateful, multi-actor AI applications, and connects to LLMs via the OpenRouter API.

2. Features
Functional Command-Line Application: A Python script (main.py) serves as the entry point, accepting a disruption scenario as input.

Transparent Chain of Thought: The agent's entire reasoning process is printed to the console, showing its Thought, the Action (tool call) it takes, and the Observation it makes from the tool's output.

Complex Scenario Resolution: The agent can successfully resolve the two distinct scenarios outlined in the project description: the "Overloaded Restaurant" and the "Damaged Packaging Dispute."

Well-Documented Codebase: The code is structured logically, well-commented, and this README provides a comprehensive overview of the agent's design and prompting strategies.

3. Agent Design and Prompt Engineering Strategy
The agent's intelligence is shaped by its architecture and a carefully engineered prompt.

Architectural Design: LangGraph and the ReAct Framework
LangGraph: We chose LangGraph because it natively supports cyclical workflows. Logistics problems are rarely linear; an agent needs to think, act, observe, and then loop back to think again based on new information. LangGraph models this as a state machine (a graph), which is a more robust and scalable paradigm for agentic systems.

ReAct Framework: The agent's reasoning is structured using the ReAct (Reason + Act) framework. This prompting technique instructs the LLM to interleave its internal reasoning (Thought) with actions (Action), allowing the agent to dynamically adjust its plan based on real-time feedback from its tools.

Prompt Engineering Strategy
The master system prompt (synapse_poc/prompts.py) is the agent's "constitution." It includes:

Persona: Establishes a clear identity for the agent.

Core Directive: Provides a high-level mission.

Constraints and Guardrails: Defines clear rules to prevent errors.

Tool Specifications: Lists the available tools for the LLM.

Few-Shot Exemplars: Includes a high-quality example of the desired reasoning pattern to guide the agent's behavior.

4. Project Structure
.
├── .env.example
├── main.py
├── README.md
├── requirements.txt
└── synapse_poc
    ├── __init__.py
    ├── agent.py
    ├── prompts.py
    └── tools.py

5. Setup and Installation
Clone the repository.

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Rename .env.example to .env.

Open the .env file and add your OpenRouter API key:

OPENROUTER_API_KEY="your_openrouter_api_key_here"

6. Usage
Run the agent from your terminal, providing the disruption scenario as a string wrapped in quotes.

Scenario A: Overloaded Restaurant
python main.py "An order was just placed at 'Pizza Palace' (merchant_id: 'pizzapalace_123'), but the merchant is overloaded. The customer is 'cust_abc' and the driver is 'driver_xyz'."

Scenario B: Damaged Packaging Dispute
python main.py "A dispute has been triggered for order 'ord_def' at the customer's door over a spilled drink. The driver is 'driver_xyz' and the merchant is 'pizzapalace_123'."
