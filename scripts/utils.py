"""
utils.py — shared helpers for file I/O, logging, and account ID inference.
"""
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import config


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))
        logger.addHandler(h)
    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    return logger


def infer_account_id(filename: str) -> str:
    """
    Infers account ID from filename.
    Handles:
      - demo_001_transcript.txt     → ACC-001
      - onboarding_003_transcript.txt → ACC-003
      - ACC-001_demo.txt            → ACC-001
    """
    # Try ACC-NNN pattern first
    m = re.search(r"ACC-(\d+)", filename, re.IGNORECASE)
    if m:
        return f"ACC-{int(m.group(1)):03d}"
    # Fall back to any number in the filename
    m = re.search(r"(\d+)", filename)
    if m:
        return f"ACC-{int(m.group(1)):03d}"
    return Path(filename).stem.upper()


def account_version_dir(account_id: str, version: str) -> Path:
    path = config.OUTPUTS_DIR / account_id / version
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_json_from_text(text: str) -> dict:
    """
    Pulls the first JSON object out of a string.
    Handles LLM responses that wrap JSON in markdown code blocks.
    """
    # Strip markdown fences
    text = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    # Find opening brace
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in text: {text[:200]}")
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("Could not find closing brace in JSON")