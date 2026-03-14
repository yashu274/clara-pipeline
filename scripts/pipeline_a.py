"""
pipeline_a.py — Demo Call → Preliminary Retell Agent (v1)

Usage:
  python pipeline_a.py data/demo/demo_001_transcript.txt
  python pipeline_a.py --all
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from extractor import extract_memo
from prompt_generator import build_agent_spec
from task_tracker import create_task
from utils import account_version_dir, get_logger, infer_account_id, read_text, save_json, utcnow

log = get_logger("pipeline_a")


def run_demo(transcript_path: Path, account_id: str = None) -> dict:
    """
    Processes one demo transcript → v1 account_memo.json + agent_spec.json.
    Returns a result summary dict.
    """
    account_id = account_id or infer_account_id(transcript_path.name)
    log.info("── Pipeline A | %s | %s", account_id, transcript_path.name)

    # 1. Read transcript
    transcript = read_text(transcript_path)

    # 2. Extract account memo via LLM
    memo = extract_memo(transcript, account_id)
    memo["_pipeline"]     = "A"
    memo["_source_file"]  = transcript_path.name
    memo["_extracted_at"] = utcnow()
    memo["_version"]      = "v1"

    # 3. Build agent spec from memo
    spec = build_agent_spec(memo, version="v1")

    # 4. Save outputs
    out = account_version_dir(account_id, "v1")
    save_json(memo, out / "account_memo.json")
    save_json(spec, out / "agent_spec.json")
    log.info("  Saved v1 → %s", out)

    # 5. Create task tracker item
    create_task(account_id, memo.get("company_name", "Unknown"), "v1", memo)

    return {
        "account_id":   account_id,
        "company_name": memo.get("company_name", "Unknown"),
        "status":       "ok",
        "output_dir":   str(out)
    }


def run_all() -> list:
    files = sorted(config.DEMO_DIR.glob("*.txt"))
    if not files:
        log.warning("No .txt files found in %s", config.DEMO_DIR)
        return []
    results = []
    for f in files:
        try:
            results.append(run_demo(f))
        except Exception as e:
            log.error("FAILED %s: %s", f.name, e)
            results.append({
                "account_id": infer_account_id(f.name),
                "status":     "error",
                "error":      str(e)
            })
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline A: Demo → v1 Agent")
    parser.add_argument("transcript", nargs="?", help="Path to a single transcript file")
    parser.add_argument("--account-id", help="Override inferred account ID")
    parser.add_argument("--all", action="store_true", help="Process all demo transcripts")
    args = parser.parse_args()

    if args.all:
        results = run_all()
        for r in results:
            icon = "✓" if r["status"] == "ok" else "✗"
            print(f"  {icon} {r['account_id']} — {r.get('company_name', r.get('error', ''))}")
    elif args.transcript:
        r = run_demo(Path(args.transcript), args.account_id)
        print(f"Done → {r['output_dir']}")
    else:
        parser.print_help()
        sys.exit(1)