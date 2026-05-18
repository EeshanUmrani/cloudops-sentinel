from langgraph.graph import StateGraph, START, END

from src.agents import (
    IncidentState,
    security_agent,
    planner_agent,
    log_analyst_agent,
    metrics_analyst_agent,
    root_cause_agent,
    remediation_agent,
    critic_agent,
    safety_agent,
    report_agent,
)


def build_graph():
    builder = StateGraph(IncidentState)

    builder.add_node("security", security_agent)
    builder.add_node("planner", planner_agent)
    builder.add_node("log_analyst", log_analyst_agent)
    builder.add_node("metrics_analyst", metrics_analyst_agent)
    builder.add_node("root_cause", root_cause_agent)
    builder.add_node("remediation", remediation_agent)
    builder.add_node("critic", critic_agent)
    builder.add_node("safety", safety_agent)
    builder.add_node("report", report_agent)

    builder.add_edge(START, "security")
    builder.add_edge("security", "planner")
    builder.add_edge("planner", "log_analyst")
    builder.add_edge("log_analyst", "metrics_analyst")
    builder.add_edge("metrics_analyst", "root_cause")
    builder.add_edge("root_cause", "remediation")
    builder.add_edge("remediation", "critic")
    builder.add_edge("critic", "safety")
    builder.add_edge("safety", "report")
    builder.add_edge("report", END)

    return builder.compile()