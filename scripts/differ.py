"""
differ.py — generates a structured changelog between v1 and v2 memo + spec.
Produces both a JSON changelog and a human-readable markdown file.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import config
from utils import get_logger, save_json

log = get_logger("differ")


def _deep_diff(old, new, path="") -> list:
    """Recursively finds differences between two dicts/lists/values."""
    changes = []

    if isinstance(old, dict) and isinstance(new, dict):
        all_keys = sorted(set(old.keys()) | set(new.keys()))
        for key in all_keys:
            # Skip internal metadata keys
            if key.startswith("_"):
                continue
            child_path = f"{path}.{key}" if path else key
            if key not in old:
                changes.append({"path": child_path, "type": "added",    "old": None,       "new": new[key]})
            elif key not in new:
                changes.append({"path": child_path, "type": "removed",  "old": old[key],   "new": None})
            else:
                changes.extend(_deep_diff(old[key], new[key], child_path))

    elif isinstance(old, list) and isinstance(new, list):
        if json.dumps(old, sort_keys=True) != json.dumps(new, sort_keys=True):
            changes.append({"path": path, "type": "modified", "old": old, "new": new})

    else:
        if old != new:
            changes.append({"path": path, "type": "modified", "old": old, "new": new})

    return changes


def _changes_to_markdown(account_id: str, memo_changes: list, prompt_changed: bool, generated_at: str) -> str:
    lines = [
        f"# Changelog: {account_id}",
        f"**Generated:** {generated_at}",
        f"**Total memo field changes:** {len(memo_changes)}",
        f"**System prompt regenerated:** {'Yes' if prompt_changed else 'No'}",
        "",
        "---",
        "",
        "## Memo Changes",
        ""
    ]

    if not memo_changes:
        lines.append("_No memo field changes detected._")
    else:
        for c in memo_changes:
            lines.append(f"### `{c['path']}` — *{c['type']}*")
            if c["type"] == "added":
                lines.append(f"- Added: `{json.dumps(c['new'])}`")
            elif c["type"] == "removed":
                lines.append(f"- Removed: `{json.dumps(c['old'])}`")
            else:
                lines.append(f"- Before: `{json.dumps(c['old'])}`")
                lines.append(f"- After:  `{json.dumps(c['new'])}`")
            lines.append("")

    if prompt_changed:
        lines += [
            "## System Prompt",
            "",
            "Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.",
            ""
        ]

    return "\n".join(lines)


def generate_changelog(account_id: str, v1_memo: dict, v2_memo: dict,
                       v1_spec: dict, v2_spec: dict) -> dict:
    """
    Generates changelog files for v1 → v2 transition.
    Saves {account_id}_changelog.json and {account_id}_changes.md to /changelog/.
    Returns the changelog dict.
    """
    log.info("  Generating changelog for %s", account_id)

    generated_at  = datetime.now(timezone.utc).isoformat()
    memo_changes  = _deep_diff(v1_memo, v2_memo)
    prompt_changed = v1_spec.get("system_prompt") != v2_spec.get("system_prompt")

    changelog = {
        "account_id":      account_id,
        "generated_at":    generated_at,
        "summary": {
            "memo_fields_changed":   len(memo_changes),
            "system_prompt_changed": prompt_changed,
            "total_changes":         len(memo_changes) + (1 if prompt_changed else 0)
        },
        "memo_changes":    memo_changes,
        "system_prompt_changed": prompt_changed
    }

    out_dir = config.CHANGELOG_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    save_json(changelog, out_dir / f"{account_id}_changelog.json")

    md = _changes_to_markdown(account_id, memo_changes, prompt_changed, generated_at)
    (out_dir / f"{account_id}_changes.md").write_text(md, encoding="utf-8")

    log.info("  Changelog saved — %d field changes, prompt changed: %s",
             len(memo_changes), prompt_changed)
    return changelog