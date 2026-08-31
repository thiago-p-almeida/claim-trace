# CHANGELOG — ClaimTrace

## v0 — Baseline (single prompt)

A single prompt reads the CV, interview, and technical test code, and gives
a "matches/doesn't match" verdict per claim, with no scope-triage step.

**Observed limitation, with real numbers:** run 5x against cases 7 and 8
(only variable tested: claims out of the technical test's scope), the
baseline gave a confident and unwarranted verdict in **5/5 runs on
case_07** and **4/5 on case_08** — even though it had no basis in the code
to confirm or deny these claims (Kubernetes migration, CI/CD, team
leadership). The rate is not fixed: in separate runs of
`run_evaluation.py`, case_08 alone oscillated between 0% and 100%
overconfidence for the same claim, same code, same prompt — evidence that
the failure is intermittent, not deterministic.

## v1 — + Specificity triage (Stage 1)

Added an extraction agent that classifies each CV/interview claim against
what the technical test specifically exercises
(`in_scope` / `out_of_scope` / `ambiguous`), before any verification.

**Bug found and fixed during this stage:** the original prompt instructed
"ignore vague personality/soft skills claims" — this caused the model to
**silently discard** concrete, falsifiable claims just because they were
not technical (e.g.: "I acted as tech lead of a 4-person team" never got
classified, instead of being correctly marked `out_of_scope`). Fixed to
extract every factual and verifiable claim, technical or not, and
classify — never discard without classification.

## v2 — + Conditional verification by execution (Stage 2)

For behavioral claims (concurrency, input validation), Stage 2 decides
between static reading or **real execution** — running the candidate's
code under a concurrency stress test (N threads, M iterations) or direct
validation check (`seen('')`, `seen(None)`).

**Bugs found and fixed:**
- **Concurrency harness:** reusing the same `event_id` across all
  iterations with a long TTL caused iterations 2+ to report failure even
  on correct code (event already registered, expected result being read as
  failure). Fixed by generating a new `event_id` per iteration.
- **Race condition masked by the GIL:** in pure memory, with no real I/O,
  CPython's GIL prevents the race condition from appearing reliably — the
  window between read and write is too short. Fixed by inserting a
  `time.sleep(0.001)` into the buggy candidates, simulating the real gap
  that would exist in a network call (e.g.: checking a remote Redis),
  consistent with the scenario described in the synthetic cases themselves
  (multiple instances, not multiple local threads).

## v3 — + Second opinion and validation primitive

Added a second check before accepting an "out_of_scope" classification
(prevents unwarranted discarding), and an execution-based verification
primitive for input-validation claims (before, these claims all fell into
"ambiguous" due to lack of implementation).

**Bugs found and fixed:**
- **Too-generic keyword routing:** the word `"check"` in the validation
  keywords list accidentally captured a **concurrency** claim from
  case_01 ("the check and the insertion as a single operation"), routing
  it to the wrong harness (validation instead of stress test). Removed the
  generic keyword; added more specific concurrency keywords (`instance`,
  `at the same time`, `single operation`, `lock`).
- **Evaluation metric:** `compute_overconfidence_rate` returned `0.0`
  (instead of indicating "not applicable") for cases with no out-of-scope
  claims — this diluted the aggregated mean misleadingly (25% observed,
  instead of the real value of 100% when calculated only over applicable
  cases). Fixed to return `None` in those cases and exclude them from the
  aggregation.

**Result after all fixes (real measurement, `python3 -m pytest -v`):**
7 of 7 tests passing.

**Real result of the full pipeline (`python3 run_evaluation.py`), after
v3:** case_01, concurrency claim correctly `⚠️ Contradicted`
(50/50 runs failed); case_02 (subtler bug — lock only on write),
correctly contradicted (49-50/50 failures, expected variation given the
narrower race timing); cases 03/04/08, validation contradictions correctly
identified by execution; cases 05/06, correct confirmations on concurrency
and validation; cases 07/08, out-of-scope claims correctly marked
`❔ Not verifiable`.

## Known limitations (not hidden, documented on purpose)

- **Scope leakage in case_07:** Stage 1 still classifies some
  release-process claims (deploy time, feature flags, canary deploy) as
  "in_scope" that have no relation to the technical test — Stage 2's
  second opinion only reexamines unwarranted exclusions, not unwarranted
  inclusions. Explicit decision not to fix now: tweaking Stage 1's
  classification criterion risks altering the behavior of the 7 other
  already-validated cases, given the remaining hackathon time.
- **Static-reading verification was never actually implemented** — every
  claim that doesn't match the concurrency or validation primitives falls
  into `🟡 Ambiguous`, with the explicit note "pending review", instead of
  pretending an automated judgment that doesn't exist.
- **The validation primitive assumes positive claims** ("I validate
  correctly") — a claim of the type "I don't validate anything" would
  invert the expected verdict. Known simplification, not generalized due
  to time cost.

## Hot Take

The baseline's overconfidence failure is not constant — it's intermittent
(0%→100%→100%→0% observed on the same claim, same code, across different
executions of `run_evaluation.py`). This makes it more dangerous than a
deterministic failure: an evaluator who runs the baseline a single time
might conclude, by chance, that it "works well" on this kind of case. The
robustness of a triage tool shouldn't be measured by a single run — it
should be measured by the hit rate over many.

## Update — case_07 scope leak (revisited after translation)

The previous limitation ("Stage 1 incorrectly classifies release-process
claims as in scope") did not reproduce in the English version of the
pipeline: 5 independent runs (3 before this changelog update, 2 after)
classified all 5 case_07 claims (Kubernetes migration, CI/CD, feature
flags, canary deploy) as `out_of_scope` 100% of the time — zero leakage
observed. Unconfirmed hypothesis: the "this is about deployment, not about
the test problem" domain boundary may be sharper in English technical
vocabulary than it was in the original Portuguese version. N=5 is not
exhaustive; kept as an observation, not a guarantee.