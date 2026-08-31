# Agent Traces — ClaimTrace

This document shows representative traces of how each agent in the
ClaimTrace pipeline actually reasoned during development: instruction →
tool response → what changed the next step → human checkpoints. All
excerpts below come from real runs and real development decisions made
while building this project, not idealized examples.

## Architecture and roles

Three roles were used throughout development:
- **Strategist (Claude, this conversation):** decomposes the problem,
  proposes and audits plans, never executes code directly.
- **Executor (Cline, in VS Code):** implements, tests, and reports back —
  only after a plan is approved.
- **Human (project owner):** approves scope, breaks ties, and is the only
  role that can authorize consequential actions (e.g. "ACT MODE").

## Trace 1 — Stage 1: Extraction + Specificity Triage

**Instruction given to the model** (`EXTRACTION_PROMPT`, current version):
```
You are a claim extraction and triage agent.

Read the CV and interview transcript below. Extract every specific,
factual claim about the candidate's work — technical or not (e.g.,
leadership, process, certifications) — as long as it is concrete enough
to be judged true or false. Only ignore vague statements with no
verifiable content (e.g., "I'm dedicated", "I work well in teams"). Every
extracted claim must be classified — even if "out_of_scope" — never
silently dropped.

For each claim, classify it against the technical test statement:
- "in_scope": the test directly exercises this skill/decision.
- "out_of_scope": the test does not touch this subject.
- "ambiguous": cannot decide with confidence.
```

**Tool response** (real output, case_01, one run):
```json
{"texto": "Worked on a webhook deduplication system running on multiple instances behind a load balancer.",
 "fonte": "cv", "classificacao": "in_scope",
 "justificativa_classificacao": "Directly related to the deduplication problem in the technical test."}
```

**What this fed into next:** this claim, marked `in_scope`, moves to Stage
2 for verification (see Trace 2). A different claim from the same case —
"Contributed to team code reviews" — was correctly marked `out_of_scope`
and never sent for verification at all, going straight to a `not
verifiable` verdict in the final report.

## Trace 2 — Stage 2: Conditional Verification (real execution)

**Decision point in the agent:** the claim above contains concurrency
vocabulary ("multiple instances," "at the same time"), so the routing
logic selects the **execution** primitive instead of static reading.

**Tool call:**
```python
run_concurrency_stress_test(candidate_code_path, n_threads=20, iterations=50)
```

**Tool response (real, case_01):**
```
{"total": 50, "failures": 50, "failure_rate": 1.0}
```

**How this shaped the final output:** the agent does not ask the LLM
whether the code "looks" thread-safe — it runs the code under load and
measures. Because `failure_rate > 0`, the claim's verdict was set to
`contradicted`, with the raw numbers cited directly in the report:
`50/50 executions failed (rate 100%)`.

## Trace 3 — Second Opinion (self-correction before discarding a claim)

**Why this exists:** an earlier version of Stage 2 accepted the first
stage's "out_of_scope" classification without question, which risked
silently discarding claims that should have been kept for review.

**Instruction** (`SECOND_OPINION_PROMPT`):
```
A claim was classified as OUT OF SCOPE for the technical test. Before
discarding it, confirm: is it really impossible to verify this claim with
what the test exercises?

Claim: "Served as tech lead for a 4-person team"
Original justification: "Not related to the deduplication/TTL problem."

Respond with JSON only: {"confirms_out_of_scope": true|false}
```

**Tool response (real, case_08):** `{"confirms_out_of_scope": true}`

**Resulting behavior:** the claim's verdict became `unverifiable` rather
than being dropped or wrongly evaluated — the final report explicitly
states the model cannot confirm or deny leadership experience, instead of
staying silent about it.

## Trace 4 — Human checkpoint during a real bug fix

**Context:** a routing keyword (`"checagem"`) was found to be too generic,
misrouting a concurrency claim in `case_01` to the wrong verification
primitive (input validation instead of a stress test).

**Executor's diagnosis (Cline), verbatim excerpt:**
> "The claim was classified 'in_scope' but verified with the validation
> primitive instead of the concurrency one — likely because 'checagem'
> matched the validation keyword list."

**Human/Strategist checkpoint (before applying the fix):**
> "Approved, with one removal before applying — `intervalo` is too generic
> and the Executor already flagged it correctly, this is the same class of
> error we just fixed."

**Result:** the keyword list was corrected *before* being applied, not
after — the fix was verified against `case_01`'s real report showing
`50/50 executions failed`, confirming the routing now worked, before
moving on to the next pending item.

## Trace 5 — An agent being confidently wrong, and the correction that followed

**Context:** during a translation pass, the Executor diagnosed a silent
hang in `run_evaluation.py` as a Python syntax issue:

**Executor's claim (incorrect):**
> "Lines 13-18 have stray commas that turn them into 1-element tuples,
> which is why `client` is never defined."

**Correction (Strategist), based on checking the actual file structure:**
> "A comma inside function-call parentheses does not create a tuple — that
> rule only applies outside any parentheses. The real bug is that there is
> no `OpenAI(...)` call wrapping those lines at all."

**Why this trace matters:** it is a concrete example of the same failure
mode ClaimTrace is built to catch — a confident, technically-worded
explanation that turns out to be wrong — happening inside the development
process itself, and caught only because the actual code was re-read
instead of trusting the stated diagnosis.

## Trace 6 — Human-in-the-loop gate before an architectural translation

Before a full Portuguese→English translation of the schema, prompts, and
data layer, the Executor submitted a mapping table for approval. The
Strategist rejected the first version:

> "Not approved yet — found one major omission (CV/interview.md files
> aren't in any step) and some smaller gaps (missing attribute names, only
> type aliases)."

The Executor revised and resubmitted twice more before the human granted
explicit approval to proceed with execution — each revision changing
something concrete (a missing file category, a missing snake_case field),
never proceeding on a guess.