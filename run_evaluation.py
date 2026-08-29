# run_evaluation.py
import json
import os
from pathlib import Path
import openai
from src.pipeline import run_pipeline
from src.baseline import baseline_verdict
from src.eval import compute_overconfidence_rate

def main():
    # 9Router expõe um endpoint compatível com OpenAI; a chave é a chave do
    # próprio 9Router (formato "9r_..."), não uma chave da NVIDIA diretamente.
    client = openai.OpenAI(
        base_url=os.environ.get("NIM_BASE_URL", "http://localhost:20128/v1"),
        api_key=os.environ.get("NIM_API_KEY", "9r_placeholder"),
    )
    test_problem_text = Path("cases/test_problem.md").read_text()
    case_dirs = sorted(Path("cases").glob("case_*"))

    for case_dir in case_dirs:
        report = run_pipeline(case_dir, test_problem_text, client)
        (case_dir / "pipeline_report.md").write_text(report)

        cv_text = (case_dir / "cv.md").read_text()
        interview_text = (case_dir / "interview.md").read_text()
        candidate_code_text = (case_dir / "candidate_code.py").read_text()
        baseline_results = baseline_verdict(cv_text, interview_text, test_problem_text, candidate_code_text, client)
        gold_labels = json.loads((case_dir / "gold_labels.json").read_text())["claims"]
        rate = compute_overconfidence_rate(baseline_results, gold_labels)

        print(f"{case_dir.name}: taxa de excesso de confiança da baseline = {rate:.0%}")

if __name__ == "__main__":
    main()