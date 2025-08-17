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


from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .prompts import MASTER_PROMPT
from .tools import ALL_TOOLS

class AgentState(TypedDict):
    """
    Represents the state of our agent.
    """
    messages: Annotated[List[AnyMessage], operator.add]


llm = ChatOpenAI(
    model="google/gemini-flash-1.5",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost", 
        "X-Title": "Project Synapse",     
    }
)
llm_with_tools = llm.bind_tools(ALL_TOOLS)


tool_node = ToolNode(ALL_TOOLS)


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



workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

workflow.add_edge("action", "agent")

agent_executor = workflow.compile()
