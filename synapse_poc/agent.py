"""
Core agent definition for Project Synapse.

This module constructs the agent's cognitive architecture using LangGraph.
It defines:
1.  The AgentState: A TypedDict that represents the agent's memory or state.
2.  The Nodes: Python functions that represent the core computational steps
    (e.g., calling the LLM, executing a tool).
3.  The Graph: The state machine that orchestrates the flow between the nodes,
    creating the cyclical reasoning loop (Thought -> Action -> Observation).
"""

import operator
import os
from typing import TypedDict, Annotated, List

# Import and call load_dotenv() at the very top to load API keys
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .prompts import MASTER_PROMPT
from .tools import ALL_TOOLS

# --- 1. Define the Agent's State ---
class AgentState(TypedDict):
    """
    Represents the state of our agent.
    """
    messages: Annotated[List[AnyMessage], operator.add]

# --- 2. Define the Agent's Brain and Tools ---

# Set up the core LLM to use OpenRouter's API with a model that supports tool use.
# Switched to a reliable free model with strong tool-calling capabilities.
llm = ChatOpenAI(
    model="google/gemini-flash-1.5",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost", # Replace with your app's URL if deployed
        "X-Title": "Project Synapse",      # Optional, for usage tracking
    }
)
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# The ToolNode executes tools requested by the LLM.
tool_node = ToolNode(ALL_TOOLS)

# --- 3. Define the Graph Nodes and Edges ---

def should_continue(state: AgentState) -> str:
    """
    Conditional edge logic to decide the next step.
    If the LLM requested a tool, route to 'action'. Otherwise, end.
    """
    if state["messages"][-1].tool_calls:
        return "continue"
    return "end"

def call_model(state: AgentState) -> dict:
    """
    The primary 'agent' node that invokes the LLM.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", MASTER_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ])
    chain = prompt | llm_with_tools
    response = chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

# --- 4. Construct the Graph ---

workflow = StateGraph(AgentState)

# Add the primary nodes
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set the entry point
workflow.set_entry_point("agent")

# Add the conditional edge for the reasoning loop
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# Add the edge to loop back from action to the agent
workflow.add_edge("action", "agent")

# Compile the graph into a runnable executor
agent_executor = workflow.compile()
