import streamlit as st

from src.graph import build_graph
from src.sample_incidents import SAMPLE_INCIDENTS


st.set_page_config(
    page_title="CloudOps Sentinel",
    layout="wide",
)


def render_agent_trace(agent_trace):
    if not agent_trace:
        st.info("No agent trace available.")
        return

    for index, step in enumerate(agent_trace, start=1):
        agent_name = step.get("agent", "Unknown Agent")
        summary = step.get("summary", "No summary available.")

        st.markdown(f"**{index}. {agent_name}**")
        st.write(summary)


def render_markdown_section(title, content):
    with st.expander(title, expanded=False):
        if content:
            st.markdown(content)
        else:
            st.info("No output generated for this section.")


def render_json_section(title, content):
    with st.expander(title, expanded=False):
        if content:
            st.json(content)
        else:
            st.info("No output generated for this section.")


def run_triage(incident_text):
    graph = build_graph()

    initial_state = {
        "raw_incident": incident_text,
        "agent_trace": [],
        "errors": [],
    }

    return graph.invoke(initial_state)


st.title("CloudOps Sentinel")
st.subheader("A Guardrailed Multi-Agent Assistant for AWS Incident Triage")

st.markdown(
    """
CloudOps Sentinel demonstrates a controlled multi-agent workflow for cloud incident triage.
The system uses specialized agents for planning, log analysis, metrics analysis, root cause analysis,
remediation, critique, safety review, and final report generation.
"""
)

with st.sidebar:
    st.header("About")
    st.write(
        """
CloudOps Sentinel is a live multi-agent system designed for cloud operations incident triage.
It is built to demonstrate agent collaboration, task decomposition, shared state, and safe use
of LLMs.
"""
    )

    st.header("Architecture")
    st.markdown(
        """
- Security Agent validates and sanitizes the input.
- Planner Agent decomposes the incident.
- Log Analyst Agent reviews log evidence.
- Metrics Analyst Agent reviews metric evidence.
- Root Cause Agent identifies likely causes.
- Remediation Agent proposes safe actions.
- Critic Agent reviews reasoning quality.
- Safety Agent checks for risky recommendations.
- Report Agent generates the final incident report.
"""
    )

    st.header("Safety Notes")
    st.markdown(
        """
- Logs are treated as untrusted input.
- Secrets are redacted before LLM processing.
- Prompt injection indicators are flagged.
- Risky production actions require human approval.
- The system does not automatically execute remediation steps.
"""
    )

st.divider()

sample_names = list(SAMPLE_INCIDENTS.keys())

selected_sample = st.selectbox(
    "Choose a sample incident",
    sample_names,
)

incident_text = st.text_area(
    "Incident input",
    value=SAMPLE_INCIDENTS[selected_sample],
    height=350,
)

run_button = st.button("Run Multi-Agent Triage", type="primary")

if run_button:
    if not incident_text.strip():
        st.error("Please provide incident details before running the triage workflow.")
    else:
        try:
            with st.spinner("Running multi-agent triage workflow..."):
                result = run_triage(incident_text)

            st.success("Triage complete.")

            errors = result.get("errors", [])
            if errors:
                st.warning("The workflow completed with one or more errors.")
                with st.expander("Errors", expanded=True):
                    for error in errors:
                        st.write(error)

            st.header("Final Incident Report")
            final_report = result.get("final_report", "")
            if final_report:
                st.markdown(final_report)
            else:
                st.info("No final report was generated.")

            st.divider()

            left_col, right_col = st.columns([1, 1])

            with left_col:
                st.header("Agent Trace")
                render_agent_trace(result.get("agent_trace", []))

            with right_col:
                st.header("Guardrail Summary")
                security_findings = result.get("security_findings", {})
                safety_review = result.get("safety_review", {})

                st.subheader("Security Findings")
                if security_findings:
                    st.json(security_findings)
                else:
                    st.info("No security findings available.")

                st.subheader("Safety Review")
                if safety_review:
                    st.json(safety_review)
                else:
                    st.info("No safety review available.")

            st.divider()

            st.header("Intermediate Agent Outputs")

            render_json_section(
                "Security Findings",
                result.get("security_findings", {}),
            )

            render_markdown_section(
                "Triage Plan",
                result.get("triage_plan", ""),
            )

            render_markdown_section(
                "Log Analysis",
                result.get("log_analysis", ""),
            )

            render_markdown_section(
                "Metrics Analysis",
                result.get("metrics_analysis", ""),
            )

            render_markdown_section(
                "Root Cause Analysis",
                result.get("root_cause_analysis", ""),
            )

            render_markdown_section(
                "Remediation Plan",
                result.get("remediation_plan", ""),
            )

            render_markdown_section(
                "Critic Review",
                result.get("critic_review", ""),
            )

            render_json_section(
                "Safety Review",
                result.get("safety_review", {}),
            )

        except Exception as exc:
            st.error("The triage workflow failed.")
            st.exception(exc)