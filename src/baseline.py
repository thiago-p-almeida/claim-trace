# src/baseline.py
from src.llm_response import parse_llm_json
import os

BASELINE_PROMPT = """Read the technical test code and decide, for EACH claim
below, whether it matches the code. Respond in the SAME ORDER as the claims.

Technical test statement: {test_problem_text}
Candidate code: {candidate_code_text}

Claims to evaluate:
{claims_numeradas}

Respond ONLY with JSON:
{{"verdicts": [{{"verdict": "matches"|"does_not_match"|"cannot_determine"}}]}}
(one item per claim, in the same order)
"""

def baseline_verdict(claims: list[dict], test_problem_text: str, candidate_code_text: str, llm_client) -> list[dict]:
    claims_numeradas = "\n".join(f"{i+1}. {c['text']}" for i, c in enumerate(claims))
    prompt = BASELINE_PROMPT.format(
        test_problem_text=test_problem_text, candidate_code_text=candidate_code_text,
        claims_numeradas=claims_numeradas,
    )
    response = llm_client.chat.completions.create(
        model=os.environ.get("NIM_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"),
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    veredictos = parse_llm_json(response)["verdicts"]
    return [{"text": c["text"], "verdict": v["verdict"]} for c, v in zip(claims, veredictos)]