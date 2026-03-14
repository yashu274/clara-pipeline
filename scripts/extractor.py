"""
extractor.py — calls Groq to extract a structured Account Memo from a transcript.
Includes API key validation, retry with backoff, and error response detection.
"""
import time
import textwrap

from groq import Groq

import config
from utils import extract_json_from_text, get_logger

log = get_logger("extractor")

EXTRACTION_PROMPT = textwrap.dedent("""
You are a data extraction assistant for a voice AI company called Clara Answers.
Read the call transcript below and extract structured configuration data.

RULES:
- Extract ONLY what is explicitly stated in the transcript.
- Do NOT guess, invent, or infer values that are not clearly stated.
- If a field is missing or unclear, set it to null.
- Add an entry to questions_or_unknowns for anything missing or ambiguous.
- Return ONLY a valid JSON object. No explanation, no markdown, no code fences.

JSON SCHEMA TO FILL:
{
  "account_id": "string",
  "company_name": "string",
  "business_hours": {
    "days": ["Monday", "Tuesday", ...],
    "start": "HH:MM",
    "end": "HH:MM",
    "timezone": "IANA timezone e.g. America/Chicago",
    "notes": "string or null"
  },
  "office_address": "string or null",
  "services_supported": ["list of services"],
  "emergency_definition": ["list of what counts as an emergency"],
  "emergency_routing_rules": [
    {
      "order": 1,
      "contact": "description of contact",
      "phone": "number or null",
      "timeout_seconds": null
    }
  ],
  "non_emergency_routing_rules": {
    "action": "collect_info",
    "collect_fields": ["name", "phone", "description"],
    "message_to_caller": "string or null"
  },
  "call_transfer_rules": {
    "pre_transfer_message": "string",
    "timeout_seconds": null,
    "max_attempts": null,
    "transfer_fail_message": "string"
  },
  "integration_constraints": ["list of constraints"],
  "after_hours_flow_summary": "paragraph describing after-hours flow",
  "office_hours_flow_summary": "paragraph describing business-hours flow",
  "questions_or_unknowns": ["list of missing or unclear items"],
  "notes": "any short important notes"
}

TRANSCRIPT:
{transcript}

ACCOUNT ID HINT: {account_id}

Return only the JSON object, nothing else.
""").strip()


def _check_api_key() -> None:
    """Raises a clear error if GROQ_API_KEY is missing."""
    if not config.GROQ_API_KEY:
        raise EnvironmentError(
            "\n\nGROQ_API_KEY is not set.\n"
            "Fix:\n"
            "  1. Go to https://console.groq.com and create a free API key\n"
            "  2. Open your .env file in the project root\n"
            "  3. Add this line: GROQ_API_KEY=gsk_your_key_here\n"
            "  4. Save the file and re-run\n"
        )


def _call_groq(prompt: str) -> str:
    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=2048,
    )
    return response.choices[0].message.content


def _call_with_retry(prompt: str, max_attempts: int = 3) -> str:
    """Calls Groq with automatic retry and exponential backoff."""
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return _call_groq(prompt)
        except Exception as e:
            last_error = e
            wait = 5 * (2 ** (attempt - 1))  # 5s, 10s, 20s
            log.warning("Groq call failed (attempt %d/%d): %s — retrying in %ds",
                        attempt, max_attempts, e, wait)
            if attempt < max_attempts:
                time.sleep(wait)
    raise last_error


def extract_memo(transcript: str, account_id: str) -> dict:
    """
    Extract a structured Account Memo from a transcript string.
    Returns a validated Python dict.
    """
    _check_api_key()

    log.info("  Calling Groq (%s) for account %s...", config.GROQ_MODEL, account_id)
    prompt = EXTRACTION_PROMPT.replace("{transcript}", transcript).replace("{account_id}", account_id)
    raw = _call_with_retry(prompt)
    log.debug("  Raw response (first 300 chars): %s", raw[:300])

    memo = extract_json_from_text(raw)

    # Detect API error responses e.g. {"error": {"message": "Invalid API Key"}}
    if "error" in memo and "company_name" not in memo:
        raise RuntimeError(
            f"Groq returned an error: {memo['error']}\n"
            "Check your GROQ_API_KEY in .env"
        )

    # Always stamp the account_id
    memo["account_id"] = account_id
    return memo