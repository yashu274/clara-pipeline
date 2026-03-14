"""
task_tracker.py — creates task tracker entries for each processed account.
Writes to tasks_log.md and a per-account task.json.
Supports local (always works) and GitHub Issues (optional).
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

import config
from utils import get_logger, save_json

log = get_logger("task_tracker")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _local_create(account_id: str, title: str, body: str) -> dict:
    task = {
        "account_id": account_id,
        "title":      title,
        "body":       body,
        "status":     "open",
        "created_at": _now(),
        "backend":    "local"
    }
    # Save per-account task.json
    task_path = config.OUTPUTS_DIR / account_id / "task.json"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(task, task_path)

    # Append to global tasks log
    log_path = config.BASE_DIR / "tasks_log.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n## [{_now()}] {title}\n")
        f.write(f"**Account:** {account_id}\n\n")
        f.write(f"{body}\n\n---\n")

    log.info("  Task created locally for %s", account_id)
    return task


def _local_update(account_id: str, message: str) -> None:
    task_path = config.OUTPUTS_DIR / account_id / "task.json"
    if task_path.exists():
        with open(task_path, "r") as f:
            task = json.load(f)
        task["last_updated"] = _now()
        task.setdefault("updates", []).append({"at": _now(), "message": message})
        save_json(task, task_path)

    log_path = config.BASE_DIR / "tasks_log.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n### Update [{_now()}] — {account_id}\n{message}\n\n---\n")


def _github_create(account_id: str, title: str, body: str):
    if not config.GITHUB_TOKEN or not config.GITHUB_REPO:
        return None
    url     = f"https://api.github.com/repos/{config.GITHUB_REPO}/issues"
    payload = json.dumps({"title": title, "body": body, "labels": ["clara-onboarding"]}).encode()
    req     = urllib.request.Request(url, data=payload, method="POST", headers={
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept":        "application/vnd.github.v3+json",
        "Content-Type":  "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            issue = json.loads(resp.read())
        log.info("  GitHub issue #%s created for %s", issue.get("number"), account_id)
        return issue
    except urllib.error.HTTPError as e:
        log.warning("  GitHub API error %s — falling back to local", e.code)
        return None


def create_task(account_id: str, company_name: str, version: str, memo: dict) -> dict:
    """Creates a task tracker item after a new account is processed."""
    unknowns  = memo.get("questions_or_unknowns") or []
    services  = ", ".join(memo.get("services_supported") or []) or "Unknown"
    bh        = memo.get("business_hours") or {}
    hours_str = f"{bh.get('days', '?')} {bh.get('start', '?')}–{bh.get('end', '?')} {bh.get('timezone', '')}"

    title = f"[Clara] {company_name} — {version.upper()} agent generated ({account_id})"
    body  = (
        f"**Account ID:** {account_id}\n"
        f"**Company:** {company_name}\n"
        f"**Version:** {version}\n"
        f"**Business Hours:** {hours_str}\n"
        f"**Services:** {services}\n\n"
        f"**Open Questions / Unknowns:**\n"
        + ("".join(f"- {u}\n" for u in unknowns) if unknowns else "- None — all fields resolved.\n")
        + "\n**Next Steps:**\n"
        "- [ ] Review generated agent spec\n"
        "- [ ] Confirm transfer phone numbers\n"
        "- [ ] Import spec into Retell dashboard\n"
        "- [ ] Schedule test call\n"
    )

    result = None
    if config.TASK_TRACKER == "github":
        result = _github_create(account_id, title, body)
    if result is None:
        result = _local_create(account_id, title, body)
    return result


def update_task(account_id: str, version: str, changes_count: int) -> None:
    """Appends an update to an existing task when onboarding completes."""
    _local_update(account_id, f"Onboarding complete — {version} generated with {changes_count} changes.")