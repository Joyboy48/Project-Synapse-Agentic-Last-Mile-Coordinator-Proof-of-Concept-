"""
Defines the custom, simulated tools for the Project Synapse Agent.

Each function in this module represents a tool that the agent can use to
interact with its environment. These functions mimic real-world logistics APIs.
"""
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

class NotifyCustomerInput(BaseModel):
    customer_id: str = Field(description="The unique identifier for the customer.")
    message: str = Field(description="The content of the message to be sent.")
    voucher_code: Optional[str] = Field(description="An optional voucher code to include.")

class AnalyzeEvidenceInput(BaseModel):
    flow_id: str = Field(description="The unique ID for the active mediation flow.")
    evidence: Dict[str, Any] = Field(description="A dictionary containing evidence from both driver and customer, including photo URLs and questionnaire answers.")

@tool
def get_merchant_status(merchant_id: str) -> dict:
    """
    Checks the current operational status and estimated kitchen preparation
    time for a specific merchant.
    """
    print(f"--- TOOL: Checking status for merchant: {merchant_id} ---")
    if "pizzapalace_123" in merchant_id:
        return {"status": "online", "prep_time_minutes": 40}
    return {"status": "offline", "prep_time_minutes": -1}

@tool(args_schema=NotifyCustomerInput)
def notify_customer(customer_id: str, message: str, voucher_code: Optional[str] = None) -> dict:
    """Sends a text-based message and an optional voucher to the customer's device."""
    print(f"--- TOOL: Notifying customer {customer_id} ---")
    print(f"Message: {message}")
    if voucher_code:
        print(f"Voucher Sent: {voucher_code}")
    return {"status": "success", "message_id": f"msg_{hash(message)}"}

@tool
def re_route_driver(driver_id: str, new_task_id: str) -> dict:
    """
    Assigns a driver to a new, short, nearby delivery task to perform while
    waiting for a primary order to be prepared.
    """
    print(f"--- TOOL: Rerouting driver {driver_id} to new task {new_task_id} ---")
    return {"status": "rerouted", "driver_eta_minutes": 15}

@tool
def get_nearby_merchants(location: str, category: str) -> List[Dict[str, Any]]:
    """
    Finds similar merchants near a given location, returning their current
    preparation times to identify faster alternatives.
    """
    print(f"--- TOOL: Finding nearby '{category}' merchants near '{location}' ---")
    return [
        {"merchant_name": "Speedy Pizza", "prep_time_minutes": 15},
        {"merchant_name": "Italian Express", "prep_time_minutes": 20},
    ]

@tool
def initiate_mediation_flow(order_id: str) -> dict:
    """
    Opens a synchronized interface on the driver and customer devices for
    at-the-door dispute resolution, pausing the order.
    """
    print(f"--- TOOL: Initiating mediation flow for order {order_id} ---")
    return {"status": "mediation_initiated", "flow_id": "med_456"}

@tool(args_schema=AnalyzeEvidenceInput)
def analyze_evidence(flow_id: str, evidence: Dict[str, Any]) -> dict:
    """
    Processes evidence collected during a mediation flow to determine fault.
    """
    print(f"--- TOOL: Analyzing evidence for flow {flow_id} ---")
    driver_q = evidence.get("driver_questionnaire", {})
    cust_q = evidence.get("customer_questionnaire", {})
    if driver_q.get("was_bag_sealed_by_merchant") == "Yes" and \
       cust_q.get("was_seal_intact_upon_handover") == "Yes":
        return {
            "fault": "merchant",
            "reason": "Driver and customer both confirm the bag was sealed by the merchant and the seal was intact upon delivery, indicating poor internal packaging by the merchant was the cause of the spill."
        }
    return {"fault": "inconclusive", "reason": "Could not determine fault from evidence."}

@tool
def issue_instant_refund(order_id: str, amount: float) -> dict:
    """Issues a full or partial refund to the customer for a specific order."""
    print(f"--- TOOL: Issuing refund of ${amount} for order {order_id} ---")
    return {"status": "refund_processed", "refund_id": f"ref_{hash(order_id)}"}

@tool
def exonerate_driver(driver_id: str, order_id: str) -> dict:
    """
    Clears a driver of fault for a specific delivery issue, protecting their
    performance rating.
    """
    print(f"--- TOOL: Exonerating driver {driver_id} for order {order_id} ---")
    return {"status": "driver_exonerated"}

@tool
def log_merchant_packaging_feedback(merchant_id: str, order_id: str, report: str) -> dict:
    """
    Logs an evidence-backed report about poor packaging to the merchant's
    internal account for quality control.
    """
    print(f"--- TOOL: Logging feedback for merchant {merchant_id} ---")
    print(f"Report: {report}")
    return {"status": "feedback_logged"}

ALL_TOOLS = [
    get_merchant_status, notify_customer, re_route_driver,
    get_nearby_merchants, initiate_mediation_flow, analyze_evidence,
    issue_instant_refund, exonerate_driver, log_merchant_packaging_feedback,
]
