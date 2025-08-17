"""
Main entry point for the Project Synapse Proof-of-Concept.

This script sets up a command-line interface (CLI) to accept a disruption
scenario from the user. It then initializes the agentic coordinator and
invokes it with the user's scenario, streaming the agent's "chain of thought"
reasoning process directly to the console.
"""
import argparse
import sys
from langchain_core.messages import HumanMessage

from synapse_poc.agent import agent_executor

def main():
    """
    Parses command-line arguments and runs the agent executor.
    """
    parser = argparse.ArgumentParser(
        description="Project Synapse: Agentic Last-Mile Coordinator PoC."
    )
    parser.add_argument(
        "scenario",
        nargs='+', 
        help="A natural language string describing the delivery disruption scenario."
    )
    args = parser.parse_args()

    scenario_text = " ".join(args.scenario)
    print(f"--- Running Scenario ---\n{scenario_text}\n")
    print("--- Agent Execution Trace ---")

    inputs = [HumanMessage(content=scenario_text)]

    try:
        for chunk in agent_executor.stream({"messages": inputs}):
            for key, value in chunk.items():
                if key != "__end__":
                    print(value)
                    print("\n---\n")
    except Exception as e:
        print(f"\n--- An error occurred during agent execution ---", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
