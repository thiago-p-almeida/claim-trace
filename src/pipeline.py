# src/pipeline.py
from pathlib import Path
from src.stage1_extraction_triage import extract_and_triage
from src.stage2_verification import verify
from src.synthesis import render_report

def run_pipeline(case_dir: Path, test_problem_text: str, llm_client) -> str:
    cv_text = (case_dir / "cv.md").read_text()
    interview_text = (case_dir / "interview.md").read_text()
    candidate_code_path = str(case_dir / "candidate_code.py")
    case_id = case_dir.name

    ledger = extract_and_triage(cv_text, interview_text, test_problem_text, case_id, llm_client)
    print(f"  [{case_dir.name}] stage 2...")
    ledger = verify(ledger, candidate_code_path, llm_client)
    print(f"  [{case_dir.name}] synthesis...")
    return render_report(ledger)