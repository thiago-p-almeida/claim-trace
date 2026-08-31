# src/stage1_extraction_triage.py
from src.llm_response import parse_llm_json
import os
from src.ledger import Claim, Ledger

EXTRACTION_PROMPT = """You are an agent for extracting and triaging technical claims.

Read the CV and interview transcript below. Extract ALL specific and factual claims
about the candidate's work — technical or not (e.g., leadership, processes, certifications) — as long as they are concrete enough to be evaluated as true or false. Ignore ONLY
vague statements without verifiable content (e.g., "I am dedicated", "I work well in a team").
Every extracted claim must be classified — even if "out_of_scope" — never discarded silently.

For each claim, classify against the technical test statement:
- "in_scope": the test directly exercises this skill/decision technically.
- "out_of_scope": the test does not touch this subject.
- "ambiguous": cannot decide with confidence.

Technical test statement:
{test_problem_text}

CV:
{cv_text}

Interview:
{interview_text}

Respond ONLY with JSON in the format:
{{"claims": [{{"text": "...", "source": "cv"|"interview", "classification": "...", "classification_justification": "..."}}]}}
"""

def extract_and_triage(cv_text: str, interview_text: str, test_problem_text: str, case_id: str, llm_client) -> Ledger:
    prompt = EXTRACTION_PROMPT.format(
        test_problem_text=test_problem_text, cv_text=cv_text, interview_text=interview_text
    )
    response = llm_client.chat.completions.create(
        model=os.environ.get("NIM_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"),
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    parsed = parse_llm_json(response)
    claims = [
        Claim(
            text=c["text"],
            source=c["source"],
            classification=c["classification"],
            classification_justification=c["classification_justification"],
        )
        for c in parsed["claims"]
    ]
    return Ledger(case_id=case_id, claims=claims)