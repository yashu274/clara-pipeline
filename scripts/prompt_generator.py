"""
prompt_generator.py — builds the Retell agent spec and system prompt from an account memo.
"""
from utils import get_logger

log = get_logger("prompt_generator")


def _safe(value, default="[NOT CONFIGURED]"):
    """Returns value as string, or default if None/empty."""
    if value is None or value == "" or value == []:
        return default
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def _format_hours(bh: dict) -> str:
    if not bh:
        return "[BUSINESS HOURS NOT CONFIGURED]"
    days = ", ".join(bh["days"]) if isinstance(bh.get("days"), list) else _safe(bh.get("days"))
    tz = bh.get("timezone", "")
    return f"{days}, {bh.get('start', '?')} – {bh.get('end', '?')} {tz}".strip()


def _format_routing(rules: list) -> str:
    if not rules:
        return "  - [ROUTING NOT CONFIGURED]"
    lines = []
    for r in rules:
        timeout = f", wait {r['timeout_seconds']}s" if r.get("timeout_seconds") else ""
        phone = r.get("phone") or "number TBD"
        lines.append(f"  {r.get('order', '?')}. {r.get('contact', '[contact]')} — {phone}{timeout}")
    return "\n".join(lines)


def build_system_prompt(memo: dict, version: str = "v1") -> str:
    company     = _safe(memo.get("company_name"), "[Company Name]")
    hours_str   = _format_hours(memo.get("business_hours") or {})
    address     = _safe(memo.get("office_address"), "[address not provided]")
    services    = _safe(memo.get("services_supported", []), "[services not listed]")
    emerg_def   = _safe(memo.get("emergency_definition", []), "[emergency triggers not defined]")
    routing     = _format_routing(memo.get("emergency_routing_rules") or [])

    tr          = memo.get("call_transfer_rules") or {}
    pre_msg     = _safe(tr.get("pre_transfer_message"), "Please hold while I connect you with our team.")
    fail_msg    = _safe(tr.get("transfer_fail_message"), "I was unable to reach our team. Your information has been logged and someone will call you back shortly.")
    timeout     = tr.get("timeout_seconds") or 30
    attempts    = tr.get("max_attempts") or 2

    ne          = memo.get("non_emergency_routing_rules") or {}
    ne_msg      = _safe(ne.get("message_to_caller"), "We will follow up during the next business day.")

    constraints = "\n".join(f"  - {c}" for c in (memo.get("integration_constraints") or []))
    if not constraints:
        constraints = "  - None"

    return f"""# Clara AI Voice Agent — {company} | {version}

## Identity
You are Clara, the AI answering service for {company}.
- Always be professional, calm, and concise.
- NEVER mention "function calls", "tools", "API", or any backend system to the caller.
- NEVER reveal on-call staff names unless explicitly instructed.
- Ask only one question at a time.
- Never promise specific arrival times.
- Never discuss pricing.

## Company Info
- Company: {company}
- Address: {address}
- Business Hours: {hours_str}
- Services: {services}

## Emergency Definition
These situations are EMERGENCIES requiring immediate escalation:
{emerg_def}
Everything else (scheduling, quotes, general questions) is NON-EMERGENCY.

---
## BUSINESS HOURS CALL FLOW

Step 1 — GREETING
  Say: "Thank you for calling {company}, this is Clara. How can I help you today?"

Step 2 — UNDERSTAND PURPOSE
  Listen carefully. Ask one clarifying question if needed.

Step 3 — COLLECT INFO
  Say: "May I get your name and best callback number?"
  Repeat the number back to confirm.

Step 4 — ROUTE
  - If EMERGENCY → go to Emergency Transfer Protocol below.
  - If NON-EMERGENCY → say: "{ne_msg}"

Step 5 — CLOSE
  Say: "Is there anything else I can help you with?"
  If no → "Thank you for calling {company}. Have a great day!"

---
## AFTER-HOURS CALL FLOW

Step 1 — GREETING
  Say: "Thank you for calling {company}. Our office is currently closed.
  Business hours are {hours_str}. This is the after-hours emergency line. How can I help you?"

Step 2 — UNDERSTAND PURPOSE
  Say: "Can you briefly describe what's happening?"

Step 3 — TRIAGE
  Emergency triggers: {emerg_def}

  IF EMERGENCY:
    a. Say: "I understand — let me connect you with our emergency team right away."
    b. Collect: full name, best callback number, property address (partial is fine).
    c. → Go to Emergency Transfer Protocol below.

  IF NON-EMERGENCY:
    a. Say: "Our team handles that during business hours."
    b. Collect: name, callback number, brief description of issue.
    c. Say: "{ne_msg}"
    d. Confirm callback number.

Step 4 — CLOSE
  Say: "Is there anything else I can help you with?"
  If no → "Thank you for calling. Stay safe. Goodbye."

---
## EMERGENCY TRANSFER PROTOCOL

Say: "{pre_msg}"

Attempt transfers in this order (timeout {timeout}s each, max {attempts} attempts):
{routing}

IF ALL TRANSFERS FAIL — say exactly:
  "{fail_msg}"
Then confirm the caller's callback number one final time.

---
## INTEGRATION CONSTRAINTS (MUST FOLLOW)
{constraints}
""".strip()


def build_agent_spec(memo: dict, version: str = "v1") -> dict:
    """Builds the full Retell agent spec from an account memo."""
    log.info("  Building agent spec for %s (%s)", memo.get("account_id"), version)

    company = memo.get("company_name", "Unknown")
    bh      = memo.get("business_hours") or {}
    tr      = memo.get("call_transfer_rules") or {}

    return {
        "agent_name": f"{company} – Clara Agent",
        "version": version,
        "voice": {
            "provider": "elevenlabs",
            "voice_id": "female_professional_calm",
            "language": "en-US",
            "note": "Select closest female professional voice in Retell dashboard"
        },
        "system_prompt": build_system_prompt(memo, version),
        "key_variables": {
            "company_name":          company,
            "timezone":              (bh.get("timezone") or ""),
            "business_hours_start":  (bh.get("start") or ""),
            "business_hours_end":    (bh.get("end") or ""),
            "business_hours_days":   (bh.get("days") or []),
            "office_address":        (memo.get("office_address") or ""),
            "emergency_routing":     (memo.get("emergency_routing_rules") or []),
        },
        "tool_invocation_placeholders": [
            {
                "tool": "call_transfer",
                "trigger": "emergency confirmed and caller info collected",
                "note": "Never mention this tool to the caller"
            },
            {
                "tool": "log_call",
                "trigger": "any call completion",
                "note": "Silent background action"
            }
        ],
        "call_transfer_protocol": {
            "pre_transfer_message": tr.get("pre_transfer_message", "Please hold while I connect you."),
            "timeout_seconds":      tr.get("timeout_seconds", 30),
            "max_attempts":         tr.get("max_attempts", 2),
            "routing_order":        (memo.get("emergency_routing_rules") or [])
        },
        "fallback_protocol": {
            "trigger": "all transfer attempts exhausted",
            "message": tr.get("transfer_fail_message", "I was unable to reach our team. Your information has been logged."),
            "confirm_callback": True
        },
        "integration_constraints": (memo.get("integration_constraints") or []),
        "questions_or_unknowns":   (memo.get("questions_or_unknowns") or [])
    }