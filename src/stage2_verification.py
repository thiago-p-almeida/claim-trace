# src/stage2_verification.py
from src.ledger import Ledger
from src.execution_harness import run_concurrency_stress_test, run_validation_check
from src.llm_response import parse_llm_json

SECOND_OPINION_PROMPT = """A claim was classified as OUT OF SCOPE of
the technical test. Before discarding, confirm: is it truly impossible to verify
this claim with what the test exercises?

Claim: {text}
Original justification: {classification_justification}

Respond ONLY with JSON: {{"confirms_out_of_scope": true|false}}
"""

PRIMITIVAS_KEYWORDS = {
    "concurrency": [
        "concurrency", "concurrent", "race condition", "atomic", "thread",
        "instance", "at the same time", "operation only", "check-then-act", "lock",
    ],
    "validation": ["valid", "empty", "null", "none", "guard clause", "reject"],
}

def _classificar_primitiva(texto: str) -> str | None:
    texto_lower = texto.lower()
    for primitiva, keywords in PRIMITIVAS_KEYWORDS.items():
        if any(kw in texto_lower for kw in keywords):
            return primitiva
    return None

def verify(ledger: Ledger, candidate_code_path: str, llm_client) -> Ledger:
    for claim in ledger.claims:
        if claim.classification == "out_of_scope":
            prompt = SECOND_OPINION_PROMPT.format(
                text=claim.text, classification_justification=claim.classification_justification
            )
            response = llm_client.chat.completions.create(
                model="@cf/qwen/qwen2.5-coder-32b-instruct",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            confirmed = parse_llm_json(response)["confirms_out_of_scope"]
            if confirmed:
                claim.verdict = "unverifiable"
                claim.verification_method = None
                continue
            claim.classification = "in_scope"

        if claim.classification == "ambiguous":
            claim.verdict = "ambiguous"
            continue

        if claim.classification == "in_scope":
            primitiva = _classificar_primitiva(claim.text)

            if primitiva == "concurrency":
                result = run_concurrency_stress_test(candidate_code_path, n_threads=20, iterations=50)
                claim.verification_method = "execution"
                claim.evidence = f"{result['failures']}/{result['total']} executions failed (rate {result['failure_rate']:.0%})"
                claim.verdict = "contradicted" if result["failure_rate"] > 0 else "confirmed"

            elif primitiva == "validation":
                result = run_validation_check(candidate_code_path)
                claim.verification_method = "execution"
                claim.evidence = (
                    f"empty raises ValueError: {result['empty_raises_valueerror']}; "
                    f"None raises ValueError: {result['none_raises_valueerror']}"
                )
                claim.verdict = "confirmed" if result["validates_correctly"] else "contradicted"

            else:
                claim.verification_method = "reading"
                claim.evidence = "static verification pending review"
                claim.verdict = "ambiguous"
    return ledger