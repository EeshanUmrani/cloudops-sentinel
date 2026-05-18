from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END


class IncidentState(TypedDict, total=False):
    raw_incident: str
    security_findings: Dict[str, Any]
    triage_plan: Dict[str, Any]
    final_report: str
    agent_trace: List[Dict[str, str]]


def add_trace(state: IncidentState, agent_name: str, summary: str) -> List[Dict[str, str]]:
    trace = state.get("agent_trace", [])
    trace.append({
        "agent": agent_name,
        "summary": summary
    })
    return trace


def security_agent(state: IncidentState) -> IncidentState:
    raw_incident = state.get("raw_incident", "")

    findings = {
        "prompt_injection_detected": "ignore previous instructions" in raw_incident.lower(),
        "secret_detected": "aws_secret_access_key" in raw_incident.lower(),
        "block_execution": False
    }

    return {
        "security_findings": findings,
        "agent_trace": add_trace(
            state,
            "Security Agent",
            "Checked incident input for prompt injection and obvious secrets."
        )
    }


def planner_agent(state: IncidentState) -> IncidentState:
    plan = {
        "steps": [
            "Review alert metadata",
            "Analyze logs",
            "Analyze metrics",
            "Generate root cause hypotheses",
            "Recommend safe remediation",
            "Produce final incident report"
        ]
    }

    return {
        "triage_plan": plan,
        "agent_trace": add_trace(
            state,
            "Planner Agent",
            "Created a basic incident triage plan."
        )
    }


def report_agent(state: IncidentState) -> IncidentState:
    raw_incident = state.get("raw_incident", "")
    security_findings = state.get("security_findings", {})
    triage_plan = state.get("triage_plan", {})

    report = f"""
# Incident Triage Report

## Incident Input
{raw_incident}

## Security Findings
{security_findings}

## Triage Plan
{triage_plan}

## Summary
This is a LangGraph smoke test. The graph successfully passed state through multiple agents.
"""

    return {
        "final_report": report,
        "agent_trace": add_trace(
            state,
            "Report Agent",
            "Generated the final smoke-test report."
        )
    }


def build_graph():
    builder = StateGraph(IncidentState)

    builder.add_node("security", security_agent)
    builder.add_node("planner", planner_agent)
    builder.add_node("report", report_agent)

    builder.add_edge(START, "security")
    builder.add_edge("security", "planner")
    builder.add_edge("planner", "report")
    builder.add_edge("report", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()

    initial_state = {
        "raw_incident": """
ALERT: checkout-api p95 latency above 2500ms.
Logs show DBConnectionTimeout and HikariPool exhausted.
Metrics show error_rate_percent=8.7 and db_connections_active=50.
""",
        "agent_trace": []
    }

    result = graph.invoke(initial_state)

    print("\n=== AGENT TRACE ===")
    for step in result["agent_trace"]:
        print(f"- {step['agent']}: {step['summary']}")

    print("\n=== FINAL REPORT ===")
    print(result["final_report"])