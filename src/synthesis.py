# src/synthesis.py
from src.ledger import Ledger

VERDICT_LABELS = {
    "confirmed": "✅ Confirmed",
    "contradicted": "⚠️ Contradicted",
    "unverifiable": "❓ Not verifiable by this test",
    "ambiguous": "🟡 Ambiguous",
}

def render_report(ledger: Ledger) -> str:
    lines = [f"# Evidence Report — Case {ledger.case_id}", ""]
    lines.append("This report presents evidence for human review. "
                  "It does not contain hiring recommendations.")
    lines.append("")
    for claim in ledger.claims:
        lines.append(f"## Claim ({claim.source}): \"{claim.text}\"")
        lines.append(f"- Verdict: {VERDICT_LABELS.get(claim.verdict, claim.verdict)}")
        if claim.verification_method:
            lines.append(f"- Method: {claim.verification_method}")
        if claim.evidence:
            lines.append(f"- Evidence: {claim.evidence}")
        lines.append("")
    return "\n".join(lines)