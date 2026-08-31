# run_evaluation.py
import json
import os
from pathlib import Path
import ssl
import certifi
from openai import OpenAI, DefaultHttpx2Client
from src.pipeline import run_pipeline
from src.baseline import baseline_verdict
from src.eval import compute_overconfidence_rate

def build_client():
    return OpenAI(
        base_url=os.environ.get("NIM_BASE_URL", "http://localhost:20128/v1"),
        api_key=os.environ.get("NIM_API_KEY", "9r_placeholder"),
        http_client=DefaultHttpx2Client(
            verify=ssl.create_default_context(cafile=certifi.where()),
            timeout=30.0,
        ),
    )

def main():
    client = build_client()

    test_problem_text = Path("cases/test_problem.md").read_text()
    case_dirs = sorted(Path("cases").glob("case_*"))
    all_rates = []

    for case_dir in case_dirs:
        report = run_pipeline(case_dir, test_problem_text, client)
        (case_dir / "pipeline_report.md").write_text(report)

        candidate_code_text = (case_dir / "candidate_code.py").read_text()
        gold_labels = json.loads((case_dir / "gold_labels.json").read_text())["claims"]
        baseline_results = baseline_verdict(gold_labels, test_problem_text, candidate_code_text, client)
        rate = compute_overconfidence_rate(baseline_results, gold_labels)
        all_rates.append(rate)

        if rate is not None:
            print(f"{case_dir.name}: baseline overconfidence rate = {rate:.0%}")
        else:
            print(f"{case_dir.name}: no out-of-scope claim (not applicable)")

    cases_with_out_of_scope_claims = [r for r in all_rates if r is not None]
    if cases_with_out_of_scope_claims:
        average = sum(cases_with_out_of_scope_claims) / len(cases_with_out_of_scope_claims)
        print(f"\nOverall average (cases with out-of-scope claim): {average:.0%}")
    else:
        print("\nNo out-of-scope claims found in any case.")

if __name__ == "__main__":
    main()