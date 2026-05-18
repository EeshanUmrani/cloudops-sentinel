# CloudOps Sentinel

CloudOps Sentinel is a guardrailed multi-agent assistant for AWS incident triage. Given an incident alert, logs, and metrics, it analyzes the evidence, identifies likely root causes, recommends safe next steps, and generates a final incident report.

The project demonstrates multi-agent collaboration, task decomposition, shared state orchestration, prompt injection protection, secret redaction, and safe use of LLMs.

---

## What It Does

CloudOps Sentinel helps triage cloud operations incidents such as:

- API latency spikes
- Authentication failures
- Queue backlogs
- Worker saturation
- Downstream dependency failures
- Suspicious logs containing prompt injection or leaked secrets

The system does not execute production actions. It only analyzes incidents and recommends next steps, with risky actions clearly marked as requiring human approval.

---

## Architecture

The system uses a sequential LangGraph workflow with shared state.

```text
User
  ↓
Streamlit UI
  ↓
LangGraph Orchestrator
  ↓
Shared Incident State
  ↓
Security Agent
  ↓
Planner Agent
  ↓
Log Analyst Agent
  ↓
Metrics Analyst Agent
  ↓
Root Cause Agent
  ↓
Remediation Agent
  ↓
Critic Agent
  ↓
Safety Agent
  ↓
Report Agent
  ↓
Final Incident Report
```

The workflow is intentionally sequential to keep incident triage predictable, auditable, and safe.

---

## Agents

| Agent | Responsibility |
|---------|-------------|
| Security Agent | Detects prompt injection, redacts secrets, and sanitizes incident input |
| Planner Agent | Breaks the incident into investigation steps |
| Log Analyst Agent | Reviews logs for errors, warnings, suspicious patterns, and timing clues |
| Metrics Analyst Agent | Analyzes latency, error rate, CPU, memory, queue depth, and related metrics |
| Root Cause Agent | Produces ranked root-cause hypotheses from available evidence |
| Remediation Agent | Recommends safe diagnostics and marks risky actions for human approval |
| Critic Agent | Reviews reasoning for overconfidence, missing evidence, and unsafe assumptions |
| Safety Agent | Checks outputs for leaked secrets or dangerous recommendations |
| Report Agent | Produces the final incident report |

---

## Guardrails

CloudOps Sentinel uses deterministic guardrails before and after LLM processing.

**Input guardrails**

- Detect prompt injection attempts
- Detect secrets such as tokens, API keys, passwords, and private keys
- Replace sensitive values with `[REDACTED_SECRET]`
- Treat logs as untrusted data, not instructions

**Output guardrails**

- Check for leaked secrets
- Flag dangerous production actions
- Ensure risky remediation requires human approval

---

## Model Routing

The system uses tiered model routing:

```text
Fast model:
- Planner
- Log Analyst
- Metrics Analyst
- Remediation
- Report

Smart model:
- Root Cause
- Critic

Deterministic checks:
- Security
- Safety
```

This balances cost, latency, and reasoning quality.

---

## Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain
- OpenAI-compatible chat models
- Pydantic
- python-dotenv

---

## Running Locally

Clone the repository:

```bash
git clone <your-repo-url>
cd cloudops-sentinal
```

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
FAST_MODEL_NAME=gpt-4o-mini
SMART_MODEL_NAME=gpt-4o
```

Run the app:

```powershell
streamlit run app.py
```

---

## Deployment

For AWS Elastic Beanstalk:

Create a `Procfile`:

```text
web: streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

Set environment variables:

```text
OPENAI_API_KEY
MODEL_NAME
FAST_MODEL_NAME
SMART_MODEL_NAME
```

Do not commit `.env`.

---

## Demo Scenarios

Built-in sample incidents:

- Checkout API latency spike
- Auth service token failures
- Order worker queue backlog
- Prompt injection and secret handling demo

---

## Future Work

- Add AWS CloudWatch/SQS/RDS integrations
- Parallelize log and metric analysis
- Add conditional routing in LangGraph
- Add confidence scoring
- Improve safety detection
- Add downloadable incident reports