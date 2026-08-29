# src/synthesis.py
from src.ledger import Ledger

VEREDITO_LABELS = {
    "confirmada": "✅ Confirmada",
    "contradita": "⚠️ Contradita",
    "nao_verificavel": "❔ Não verificável por este teste",
    "ambigua": "🟡 Ambígua",
}

def render_report(ledger: Ledger) -> str:
    lines = [f"# Relatório de Evidência — Caso {ledger.caso_id}", ""]
    lines.append("Este relatório apresenta evidência para revisão humana. "
                  "Não contém recomendação de contratação.")
    lines.append("")
    for claim in ledger.claims:
        lines.append(f"## Claim ({claim.fonte}): \"{claim.texto}\"")
        lines.append(f"- Veredito: {VEREDITO_LABELS.get(claim.veredito, claim.veredito)}")
        if claim.metodo_verificacao:
            lines.append(f"- Método: {claim.metodo_verificacao}")
        if claim.evidencia:
            lines.append(f"- Evidência: {claim.evidencia}")
        lines.append("")
    return "\n".join(lines)