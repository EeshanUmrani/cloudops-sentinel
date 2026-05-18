import re
from typing import Dict, List


PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard .* instructions",
    r"reveal .* system prompt",
    r"print .* system prompt",
    r"bypass .* guardrails",
    r"act as unrestricted",
    r"disable safety",
    r"override .* policy",
    r"exfiltrate",
    r"delete all logs",
]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"ASIA[0-9A-Z]{16}",
    r"(?i)aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{20,}",
    r"(?i)secret_access_key\s*=\s*[A-Za-z0-9/+=]{20,}",
    r"(?i)password\s*=\s*\S+",
    r"(?i)token\s*=\s*\S+",
    r"(?i)api[_-]?key\s*=\s*\S+",
    r"(?i)bearer\s+[A-Za-z0-9._\-]+",
    r"-----BEGIN PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY-----",
]

DANGEROUS_ACTION_PATTERNS = [
    r"delete .* database",
    r"drop table",
    r"terminate .* instance",
    r"disable .* security group",
    r"delete .* logs",
    r"purge .* queue",
    r"rollback automatically",
    r"restart .* production .* automatically",
    r"rotate .* production .* secrets .* automatically",
]


def detect_prompt_injection(text: str) -> List[str]:
    findings = []
    lowered = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            findings.append(pattern)

    return findings


def detect_secrets(text: str) -> List[str]:
    findings = []

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            findings.append(pattern)

    return findings


def mask_secrets(text: str) -> str:
    sanitized = text

    for pattern in SECRET_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED_SECRET]", sanitized)

    return sanitized


def detect_dangerous_actions(text: str) -> List[str]:
    findings = []
    lowered = text.lower()

    for pattern in DANGEROUS_ACTION_PATTERNS:
        if re.search(pattern, lowered):
            findings.append(pattern)

    return findings


def run_input_guardrails(raw_text: str) -> Dict[str, object]:
    prompt_injection_findings = detect_prompt_injection(raw_text)
    secret_findings = detect_secrets(raw_text)
    sanitized_text = mask_secrets(raw_text)

    block_execution = False

    return {
        "prompt_injection_detected": len(prompt_injection_findings) > 0,
        "prompt_injection_findings": prompt_injection_findings,
        "secret_detected": len(secret_findings) > 0,
        "secret_findings": secret_findings,
        "sanitized_text": sanitized_text,
        "block_execution": block_execution,
        "notes": [
            "Input was treated as untrusted operational data.",
            "Detected secrets were redacted before LLM processing.",
            "Prompt-injection-like content is treated as data, not instructions.",
        ],
    }


def run_output_guardrails(output_text: str) -> Dict[str, object]:
    secret_findings = detect_secrets(output_text)
    dangerous_action_findings = detect_dangerous_actions(output_text)

    approved = len(secret_findings) == 0

    return {
        "approved": approved,
        "secret_detected": len(secret_findings) > 0,
        "secret_findings": secret_findings,
        "dangerous_action_findings": dangerous_action_findings,
        "requires_human_approval": dangerous_action_findings,
        "notes": [
            "Any production-impacting action must require human approval.",
            "The assistant must not automatically execute remediation actions.",
            "The final report should preserve uncertainty and cite evidence.",
        ],
    }