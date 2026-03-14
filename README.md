# Clara AI Pipeline

Converts demo and onboarding call transcripts into Retell AI voice agent configurations.

## Architecture
```
Demo Transcript → pipeline_a.py → account_memo.json (v1) + agent_spec.json (v1)
Onboarding Transcript → pipeline_b.py → account_memo.json (v2) + agent_spec.json (v2) + changelog
```

## Quick Start

### 1. Clone and configure
```bash
git clone https://github.com/yashu274/clara-pipeline.git
cd clara-pipeline
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run on one file
```bash
cd scripts
python pipeline_a.py ../data/demo/demo_001_transcript.txt
```

### 4. Run full batch (all 10 files)
```bash
python batch_run.py
```

### 5. Run with n8n
```bash
docker-compose up -d
# Open http://localhost:5678 — login: admin / claraadmin
# Settings → Import Workflow → select workflows/n8n_workflow.json
```

## Environment Variables
| Variable | Required | Description |
|---|---|---|
| GROQ_API_KEY | Yes | Free key from console.groq.com |
| LLM_PROVIDER | No | Default: groq |
| TASK_TRACKER | No | Default: local |
| LOG_LEVEL | No | Default: INFO |

## Output Structure
```
outputs/accounts/{account_id}/
  v1/
    account_memo.json
    agent_spec.json
  v2/
    account_memo.json
    agent_spec.json
  task.json

changelog/
  {account_id}_changelog.json
  {account_id}_changes.md
```

## Retell Manual Import
1. Go to retellai.com and create a free account
2. Dashboard → Agents → New Agent
3. Copy system_prompt from agent_spec.json → paste into System Prompt field
4. Set voice to ElevenLabs female professional
5. Add transfer numbers from call_transfer_protocol.routing_order
6. Add fallback message from fallback_protocol.message

## Known Limitations
- Retell free tier does not allow API agent creation — manual import required
- Pipeline accepts .txt transcripts as input

## What I'd Improve With Production Access
- Direct Retell API integration
- Whisper transcription for audio input
- Slack notifications when agents are generated
- Supabase for queryable storage