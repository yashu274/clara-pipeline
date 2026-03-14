"""
pipeline_b.py — Onboarding Call → Updated Retell Agent (v2)

Loads existing v1 memo, merges onboarding updates, produces v2 + changelog.

Usage:
  python pipeline_b.py data/onboarding/onboarding_001_transcript.txt
  python pipeline_b.py --all
"""
import argparse
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from differ import generate_changelog
from extractor import extract_memo
from prompt_generator import build_agent_spec
from task_tracker import update_task
from utils import account_version_dir, get_logger, infer_account_id, load_json, read_text, save_json, utcnow

log = get_logger("pipeline_b")


def _merge(v1: dict, updates: dict) -> dict:
    """
    Merges onboarding updates into v1 memo.
    Rules:
    - Onboarding value always wins over v1 (it's confirmed data).
    - If onboarding value is None/empty, keep v1 value.
    - Dicts are merged recursively.
    - questions_or_unknowns: union, then remove any that are now resolved.
    """
    result = copy.deepcopy(v1)

    for key, new_val in updates.items():
        if key.startswith("_"):
            continue  # skip internal metadata

        old_val = result.get(key)

        if key == "questions_or_unknowns":
            # Union of both lists, deduplicated
            merged = list(set((old_val or []) + (new_val or [])))
            result[key] = merged
            continue

        # Skip if onboarding didn't provide a value
        if new_val is None or new_val == "" or new_val == []:
            continue

        if isinstance(new_val, dict) and isinstance(old_val, dict):
            result[key] = _merge(old_val, new_val)
        else:
            result[key] = new_val

    # Remove questions that are now resolved
    resolved_keywords = {
        "timezone":  lambda r: bool((r.get("business_hours") or {}).get("timezone")),
        "address":   lambda r: bool(r.get("office_address")),
        "phone":     lambda r: bool(r.get("emergency_routing_rules")),
        "routing":   lambda r: bool(r.get("emergency_routing_rules")),
        "hours":     lambda r: bool(r.get("business_hours")),
        "emergency": lambda r: bool(r.get("emergency_definition")),
    }
    still_open = []
    for q in result.get("questions_or_unknowns") or []:
        q_lower = q.lower()
        is_resolved = any(
            kw in q_lower and check(result)
            for kw, check in resolved_keywords.items()
        )
        if not is_resolved:
            still_open.append(q)
    result["questions_or_unknowns"] = still_open

    return result


def run_onboarding(transcript_path: Path, account_id: str = None) -> dict:
    """
    Processes one onboarding transcript → v2 memo + agent spec + changelog.
    Requires v1 to already exist (run pipeline_a first).
    """
    account_id = account_id or infer_account_id(transcript_path.name)
    log.info("── Pipeline B | %s | %s", account_id, transcript_path.name)

    # 1. Load v1 outputs
    v1_dir = config.OUTPUTS_DIR / account_id / "v1"
    v1_memo_path = v1_dir / "account_memo.json"
    if not v1_memo_path.exists():
        raise FileNotFoundError(
            f"v1 memo not found for {account_id}. Run Pipeline A first.\n"
            f"Expected: {v1_memo_path}"
        )
    v1_memo = load_json(v1_memo_path)
    v1_spec = load_json(v1_dir / "agent_spec.json")
    log.info("  Loaded v1 from %s", v1_dir)

    # 2. Extract onboarding updates via LLM
    transcript = read_text(transcript_path)
    updates = extract_memo(transcript, account_id)

    # 3. Merge v1 + updates → v2 memo
    v2_memo = _merge(v1_memo, updates)
    v2_memo["_pipeline"]                 = "B"
    v2_memo["_source_file"]              = transcript_path.name
    v2_memo["_onboarding_extracted_at"]  = utcnow()
    v2_memo["_version"]                  = "v2"
    v2_memo["_previous_version"]         = "v1"

    # 4. Build v2 agent spec
    v2_spec = build_agent_spec(v2_memo, version="v2")

    # 5. Save v2 outputs
    out = account_version_dir(account_id, "v2")
    save_json(v2_memo, out / "account_memo.json")
    save_json(v2_spec, out / "agent_spec.json")
    log.info("  Saved v2 → %s", out)

    # 6. Generate changelog
    changelog = generate_changelog(account_id, v1_memo, v2_memo, v1_spec, v2_spec)
    changes_count = changelog["summary"]["total_changes"]
    log.info("  Changelog: %d changes", changes_count)

    # 7. Update task tracker
    update_task(account_id, "v2", changes_count)

    return {
        "account_id":   account_id,
        "company_name": v2_memo.get("company_name", "Unknown"),
        "status":       "ok",
        "output_dir":   str(out),
        "changes":      changes_count
    }


def run_all() -> list:
    files = sorted(config.ONBOARD_DIR.glob("*.txt"))
    if not files:
        log.warning("No .txt files found in %s", config.ONBOARD_DIR)
        return []
    results = []
    for f in files:
        try:
            results.append(run_onboarding(f))
        except Exception as e:
            log.error("FAILED %s: %s", f.name, e)
            results.append({
                "account_id": infer_account_id(f.name),
                "status":     "error",
                "error":      str(e)
            })
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline B: Onboarding → v2 Agent")
    parser.add_argument("transcript", nargs="?", help="Path to a single onboarding transcript")
    parser.add_argument("--account-id", help="Override inferred account ID")
    parser.add_argument("--all", action="store_true", help="Process all onboarding transcripts")
    args = parser.parse_args()

    if args.all:
        results = run_all()
        for r in results:
            icon = "✓" if r["status"] == "ok" else "✗"
            extra = f"({r.get('changes')} changes)" if r.get("changes") is not None else r.get("error", "")
            print(f"  {icon} {r['account_id']} — {r.get('company_name', '')} {extra}")
    elif args.transcript:
        r = run_onboarding(Path(args.transcript), args.account_id)
        print(f"Done → {r['output_dir']} ({r['changes']} changes)")
    else:
        parser.print_help()
        sys.exit(1)