"""
batch_run.py — runs Pipeline A on all 5 demo transcripts, then Pipeline B on all 5 onboarding transcripts.
Saves a batch_summary.json and writes all logs to batch_run.log.

Usage:
  python batch_run.py            # run everything
  python batch_run.py --pipeline a   # only demo → v1
  python batch_run.py --pipeline b   # only onboarding → v2
"""
import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
import pipeline_a
import pipeline_b

# ── Logging: both console and file ───────────────────────────────────────────
_log_path = config.BASE_DIR / "batch_run.log"
_fmt      = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format=_fmt,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(_log_path, encoding="utf-8")
    ]
)
log = logging.getLogger("batch_run")


def _print_summary(results: list, label: str) -> None:
    ok      = sum(1 for r in results if r.get("status") == "ok")
    errors  = sum(1 for r in results if r.get("status") == "error")
    print(f"\n{'═' * 55}")
    print(f"  {label}")
    print(f"{'═' * 55}")
    for r in results:
        icon  = "✓" if r.get("status") == "ok" else "✗"
        name  = r.get("company_name", "")
        extra = f"  ({r.get('changes')} changes)" if r.get("changes") is not None else ""
        err   = f"  ERROR: {r.get('error', '')[:60]}" if r.get("status") == "error" else ""
        print(f"  {icon}  {r.get('account_id', '?'):<12}  {name:<30}{extra}{err}")
    print(f"{'─' * 55}")
    print(f"  Total: {len(results)}  |  OK: {ok}  |  Errors: {errors}")
    print(f"{'═' * 55}\n")


def run_full_batch() -> dict:
    started = datetime.now(timezone.utc).isoformat()
    t0      = time.time()
    log.info("▶ Starting full batch run")

    # Pipeline A
    log.info("── Pipeline A: Demo → v1 ──")
    a_results = pipeline_a.run_all()
    _print_summary(a_results, "Pipeline A — Demo → v1")

    # Pipeline B
    log.info("── Pipeline B: Onboarding → v2 ──")
    b_results = pipeline_b.run_all()
    _print_summary(b_results, "Pipeline B — Onboarding → v2")

    elapsed = round(time.time() - t0, 1)
    summary = {
        "started_at":      started,
        "elapsed_seconds": elapsed,
        "pipeline_a":      a_results,
        "pipeline_b":      b_results,
        "totals": {
            "a_ok":     sum(1 for r in a_results if r.get("status") == "ok"),
            "a_errors": sum(1 for r in a_results if r.get("status") == "error"),
            "b_ok":     sum(1 for r in b_results if r.get("status") == "ok"),
            "b_errors": sum(1 for r in b_results if r.get("status") == "error"),
        }
    }

    out = config.BASE_DIR / "batch_summary.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log.info("Batch summary → %s", out)
    log.info("Full batch complete in %ss ✓", elapsed)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch runner — Clara Pipeline")
    parser.add_argument("--pipeline", choices=["a", "b", "all"], default="all")
    args = parser.parse_args()

    if args.pipeline == "a":
        results = pipeline_a.run_all()
        _print_summary(results, "Pipeline A")
    elif args.pipeline == "b":
        results = pipeline_b.run_all()
        _print_summary(results, "Pipeline B")
    else:
        summary = run_full_batch()
        print(json.dumps(summary["totals"], indent=2))