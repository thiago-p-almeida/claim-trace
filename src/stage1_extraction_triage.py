# src/stage1_extraction_triage.py
import json
import os
from src.ledger import Claim, Ledger

EXTRACTION_PROMPT = """Você é um agente de extração e triagem de claims técnicas.

Leia o CV e a transcrição de entrevista abaixo. Extraia CLAIMS TÉCNICAS
DISCRETAS e verificáveis em princípio (ignore afirmações vagas de
personalidade/soft skills).

Para cada claim, classifique contra o enunciado do teste técnico:
- "dentro_do_escopo": o teste exercita diretamente essa habilidade/decisão técnica.
- "fora_do_escopo": o teste não toca nesse assunto.
- "ambigua": não dá para decidir com confiança.

Enunciado do teste técnico:
{test_problem_text}

CV:
{cv_text}

Entrevista:
{interview_text}

Responda APENAS com JSON no formato:
{{"claims": [{{"texto": "...", "fonte": "cv"|"entrevista", "classificacao": "...", "justificativa_classificacao": "..."}}]}}
"""

def extract_and_triage(cv_text: str, interview_text: str, test_problem_text: str, caso_id: str, llm_client) -> Ledger:
    prompt = EXTRACTION_PROMPT.format(
        test_problem_text=test_problem_text, cv_text=cv_text, interview_text=interview_text
    )
    response = llm_client.chat.completions.create(
        model=os.environ.get("NIM_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"),
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    parsed = json.loads(response.choices[0].message.content)
    claims = [
        Claim(
            texto=c["texto"],
            fonte=c["fonte"],
            classificacao=c["classificacao"],
            justificativa_classificacao=c["justificativa_classificacao"],
        )
        for c in parsed["claims"]
    ]
    return Ledger(caso_id=caso_id, claims=claims)