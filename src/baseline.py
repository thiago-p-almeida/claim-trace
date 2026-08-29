# src/baseline.py
import json
import os

BASELINE_PROMPT = """Leia o CV, a entrevista e o código do teste técnico
abaixo. Para cada alegação técnica do CV/entrevista, diga se ela bate com o
código.

CV: {cv_text}
Entrevista: {interview_text}
Enunciado do teste: {test_problem_text}
Código do candidato: {candidate_code_text}

Responda APENAS com JSON:
{{"veredictos": [{{"texto": "...", "veredito": "bate"|"nao_bate"|"nao_sei"}}]}}
"""

def baseline_verdict(cv_text, interview_text, test_problem_text, candidate_code_text, llm_client) -> list[dict]:
    prompt = BASELINE_PROMPT.format(
        cv_text=cv_text, interview_text=interview_text,
        test_problem_text=test_problem_text, candidate_code_text=candidate_code_text,
    )
    response = llm_client.chat.completions.create(
        model=os.environ.get("NIM_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1"),
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(response.choices[0].message.content)["veredictos"]