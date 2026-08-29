# src/stage2_verification.py
import json
import os
from src.ledger import Ledger
from src.execution_harness import run_concurrency_stress_test

SECOND_OPINION_PROMPT = """Uma claim foi classificada como FORA DO ESCOPO do
teste técnico. Antes de descartar, confirme: é mesmo impossível verificar
essa claim com o que o teste exercita?

Claim: {texto}
Justificativa original: {justificativa}

Responda APENAS com JSON: {{"confirma_fora_de_escopo": true|false}}
"""

BEHAVIORAL_KEYWORDS = ["concorrência", "concorrente", "race condition", "atômica", "thread"]

def _is_behavioral_claim(texto: str) -> bool:
    return any(kw in texto.lower() for kw in BEHAVIORAL_KEYWORDS)

def verify(ledger: Ledger, candidate_code_path: str, llm_client) -> Ledger:
    for claim in ledger.claims:
        if claim.classificacao == "fora_do_escopo":
            prompt = SECOND_OPINION_PROMPT.format(
                texto=claim.texto, justificativa=claim.justificativa_classificacao
            )
            response = llm_client.chat.completions.create(
                model=os.environ.get("NIM_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"),
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            confirmed = json.loads(response.choices[0].message.content)["confirma_fora_de_escopo"]
            if confirmed:
                claim.veredito = "nao_verificavel"
                claim.metodo_verificacao = None
                continue
            claim.classificacao = "dentro_do_escopo"

        if claim.classificacao == "ambigua":
            claim.veredito = "ambigua"
            continue

        if claim.classificacao == "dentro_do_escopo":
            if _is_behavioral_claim(claim.texto):
                result = run_concurrency_stress_test(candidate_code_path, n_threads=20, iterations=50)
                claim.metodo_verificacao = "execucao"
                claim.evidencia = f"{result['failures']}/{result['total']} execuções falharam (taxa {result['failure_rate']:.0%})"
                claim.veredito = "contradita" if result["failure_rate"] > 0 else "confirmada"
            else:
                claim.metodo_verificacao = "leitura"
                claim.evidencia = "verificação por leitura estática pendente de revisão"
                claim.veredito = "ambigua"
    return ledger