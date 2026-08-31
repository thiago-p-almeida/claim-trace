# debug_case08.py
from pathlib import Path
from run_evaluation import build_client
from src.stage1_extraction_triage import extract_and_triage
from src.stage2_verification import verify

client = build_client()
test_problem_text = Path("cases/test_problem.md").read_text()

for case_name in [f"case_{i:02d}" for i in range(1, 9)]:
    case_dir = Path(f"cases/{case_name}")
    cv_text = (case_dir / "cv.md").read_text()
    interview_text = (case_dir / "interview.md").read_text()
    candidate_code_path = str(case_dir / "candidate_code.py")

    for i in range(3):
        ledger = extract_and_triage(cv_text, interview_text, test_problem_text, case_name, client)
        ledger = verify(ledger, candidate_code_path, client)
        print(f"--- {case_name} run {i+1} ---")
        for c in ledger.claims:
            print(f"  text={c.text[:60]!r} | classification={c.classification} | verdict={c.verdict}")