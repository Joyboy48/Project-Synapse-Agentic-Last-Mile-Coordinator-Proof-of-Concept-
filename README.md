# Project Synapse: Agentic Last-Mile Coordinator (Proof-of-Concept)

> ⚡ An autonomous AI agent for resolving last-mile delivery disruptions.  
> Built with **LangGraph**, powered by **OpenRouter LLMs**.

---

## 📌 Overview
**Project Synapse** is a functional **proof-of-concept (PoC)** demonstrating how an autonomous AI agent can handle complex last-mile delivery disruptions described in natural language.  

The agent:
- Accepts a disruption scenario via the command line.  
- Reasons about the problem using predefined simulated tools.  
- Devise a **multi-step resolution plan**, transparently showing its chain of thought.

The system is powered by:
- **LangGraph** → for stateful, multi-actor workflows.  
- **ReAct Framework** → for structured reasoning and dynamic decision-making.  
- **OpenRouter API** → for LLM integration.  

---

## ✨ Features
- 🖥 **Command-Line Application** – Run the agent with `main.py`, passing disruption scenarios as input.  
- 🔎 **Transparent Reasoning** – Prints the agent’s **Thought → Action → Observation** process to the console.  
- 🧩 **Complex Scenario Resolution** – Handles both the *Overloaded Restaurant* and *Damaged Packaging Dispute* cases.  
- 📖 **Well-Documented Codebase** – Clear structure, logical design, and detailed comments for easy extension.  

---

## 🧠 Agent Design & Prompting Strategy  

### **Architecture**
- **LangGraph**: Models logistics problems as **state machines (graphs)**, enabling cyclical workflows where the agent *thinks → acts → observes → thinks again*.  
- **ReAct Framework**: Structures reasoning into interleaved steps of **Thought → Action → Observation**, ensuring adaptive planning.  

### **Prompt Engineering**
The system prompt (`synapse_poc/prompts.py`) acts as the **agent’s constitution**, including:  
- 🎭 **Persona** – Defines agent identity.  
- 🎯 **Core Directive** – High-level mission.  
- 🛡 **Constraints & Guardrails** – Prevents errors.  
- 🛠 **Tool Specifications** – Lists all available tools.  
- 📝 **Few-Shot Exemplars** – Guides reasoning with worked examples.  

---

## 📂 Project Structure
```
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
```

---

## ⚙️ Setup & Installation  

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/project-synapse.git
   cd project-synapse
   ```

2. **Create & activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux / MacOS
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` → `.env`  
   - Add your OpenRouter API key:
     ```env
     OPENROUTER_API_KEY="your_openrouter_api_key_here"
     ```

---

## 🚀 Usage  

Run the agent with a disruption scenario (string wrapped in quotes):  

**Scenario A – Overloaded Restaurant**
```bash
python main.py "An order was just placed at 'Pizza Palace' (merchant_id: 'pizzapalace_123'), but the merchant is overloaded. The customer is 'cust_abc' and the driver is 'driver_xyz'."
```

**Scenario B – Damaged Packaging Dispute**
```bash
python main.py "A dispute has been triggered for order 'ord_def' at the customer's door over a spilled drink. The driver is 'driver_xyz' and the merchant is 'pizzapalace_123'."
```

---

## 🛠 Tech Stack
- **Python 3.10+**  
- **LangGraph**  
- **ReAct Framework**  
- **OpenRouter API**  

---

## 🤝 Contributing
Pull requests, bug reports, and feature suggestions are welcome!  
Please open an issue first to discuss any major changes.  

---

## 📜 License
MIT License © 2025 Astitva Arya
