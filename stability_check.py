# stability_check.py
import json
from pathlib import Path
from run_evaluation import build_client
from src.baseline import baseline_verdict
from src.stage1_extraction_triage import extract_and_triage
from src.stage2_verification import verify

OUT_OF_SCOPE_KEYWORDS = {
    "case_07": ["kubernetes", "ci/cd", "canary", "deploy"],
    "case_08": ["lead", "tech lead", "mentorship", "ceremony"],
}

def main():
    client = build_client()
    test_problem_text = Path("cases/test_problem.md").read_text()
    N = 5

    for case_name, keywords in OUT_OF_SCOPE_KEYWORDS.items():
        case_dir = Path("cases") / case_name
        gold_labels = json.loads((case_dir / "gold_labels.json").read_text())["claims"]
        candidate_code_text = (case_dir / "candidate_code.py").read_text()
        candidate_code_path = str(case_dir / "candidate_code.py")
        cv_text = (case_dir / "cv.md").read_text()
        interview_text = (case_dir / "interview.md").read_text()

        baseline_overconfident = 0
        pipeline_correct = 0

        for i in range(N):
            b = baseline_verdict(gold_labels, test_problem_text, candidate_code_text, client)
            baseline_errou = any(
                r["verdict"] in ("matches", "does_not_match")
                for r in b if any(kw in r["text"].lower() for kw in keywords)
            )
            if baseline_errou:
                baseline_overconfident += 1

            ledger = extract_and_triage(cv_text, interview_text, test_problem_text, case_name, client)
            ledger = verify(ledger, candidate_code_path, client)
            claim_alvo = [c for c in ledger.claims if any(kw in c.text.lower() for kw in keywords)]
            pipeline_acertou = bool(claim_alvo) and all(c.verdict == "unverifiable" for c in claim_alvo)
            if pipeline_acertou:
                pipeline_correct += 1

            print(f"  {case_name} run {i+1}/{N}: baseline_confident_incorrect={baseline_errou} | pipeline_correct={pipeline_acertou}")

        print(f"{case_name}: baseline confidently incorrect {baseline_overconfident}/{N} | pipeline correct {pipeline_correct}/{N}\n")

if __name__ == "__main__":
    main()