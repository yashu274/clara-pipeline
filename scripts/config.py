"""
config.py — all paths and environment variables in one place.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR      = Path(__file__).parent.parent
DEMO_DIR      = BASE_DIR / "data" / "demo"
ONBOARD_DIR   = BASE_DIR / "data" / "onboarding"
OUTPUTS_DIR   = BASE_DIR / "outputs" / "accounts"
CHANGELOG_DIR = BASE_DIR / "changelog"

for d in [OUTPUTS_DIR, CHANGELOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

LLM_PROVIDER    = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL      = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

TASK_TRACKER    = os.getenv("TASK_TRACKER", "local")
GITHUB_TOKEN    = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO     = os.getenv("GITHUB_REPO", "")

LOG_LEVEL       = os.getenv("LOG_LEVEL", "INFO")