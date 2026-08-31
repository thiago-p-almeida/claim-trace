# ClaimTrace

Hybrid developer due diligence agent: checks whether the real code produced
in a job's technical test matches the claims a candidate makes on their CV
and interview — with cited evidence and honesty about what is not
verifiable. **Never recommends hiring or rejecting** — the final decision is
always made by a qualified human reviewer.

## How it works

2-stage pipeline:
1. **Extraction + Triage** — extracts claims from CV/interview and classifies
   each one against what the technical test specifically exercises.
2. **Conditional verification** — for claims in scope, decides between static
   reading or **real execution** (concurrency stress test, input validation
   check), citing raw evidence.

Architecture details, bugs found and fixed, and known limitations: see
`CHANGELOG.md`. Representative agent traces — instruction given to each
stage, the real tool response it received, and how that response shaped the
next step, including human-in-the-loop checkpoints during development: see
`TRACES.md`.

## Requirements

- Python 3.11+
- Cloudflare account with Workers AI enabled (free tier: 10,000
  Neurons/day, no credit card)

## Setup

### 1. Install dependencies

```bash
pip3 install openai pytest certifi
```

(Optional, lighter/faster: [`uv`](https://astral.sh/uv) instead of `pip3` —
`uv pip install openai pytest certifi`.)

### 2. Configure Cloudflare Workers AI access

In the Cloudflare dashboard: **Workers AI → Use REST API → Create API
Token**, default scope (Workers AI Read/Edit, restricted to your account).
Copy the token and the Account ID.

Create a `.env` file at the project root (never versioned — already included
in `.gitignore`):

```
NIM_BASE_URL=https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/v1
NIM_API_KEY=YOUR_TOKEN_HERE
NIM_MODEL=@cf/qwen/qwen2.5-coder-32b-instruct
```

**Model used in this project:** `@cf/qwen/qwen2.5-coder-32b-instruct`
(code-specialized — chosen because Stage 2 judges candidate code
directly). Observed cost: ~2.3 Neurons per call; the full pipeline (8 cases
× 3 calls each) consumes a negligible fraction of the free daily quota. If
this model is no longer available in the `@cf/` catalog when you run it, any
other "Text Generation" model with that prefix works without code changes —
just change `NIM_MODEL`.

Load the variables before running any command:
```bash
set -a
source .env
set +a
```
**Quota note:** Cloudflare's free tier is 10,000 Neurons/day. A single run
of `run_evaluation.py` consumes a small fraction of that; the quota can run
out during intensive debugging sessions with multiple repeated runs (as
happened during this project's development). If you hit the limit, it
resets in 24h.

## Running

**Tests (no API calls spent — everything mocked):**
```bash
python3 -m pytest -v
```
Expected: 7 passed.

**Full pipeline on the 8 synthetic cases:**
```bash
python3 run_evaluation.py
```
Generates a `pipeline_report.md` per case under `cases/case_NN/`, and prints
the baseline overconfidence rate per case, plus the aggregated mean of cases
with out-of-scope claims.

**Stability check** (runs the baseline and pipeline N times against cases 7
and 8, to measure variance — see Hot Take in CHANGELOG):
```bash
python3 stability_check.py
```

## Structure

```
├── src/ # pipeline, harness, baseline, evaluation
├── cases/ # 8 synthetic cases (CV, interview, code, gold labels)
├── tests/ # pytest suite, all mocked
├── run_evaluation.py # runs the 8 cases, prints metrics
├── stability_check.py # measures baseline variance over N executions
├── CHANGELOG.md # version history, bugs fixed, limitations
└── TRACES.md # representative agent traces (instruction → tool response → next step)
```

## Synthetic data

All candidates, CVs, interviews, and test code are 100% fictional,
hand-written. No real candidate data is used at any stage.

## Known limitations

See the "Known limitations" section in `CHANGELOG.md` — documented on
purpose, not hidden.
