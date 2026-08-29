# tests/test_stage2.py
from unittest.mock import MagicMock
from src.ledger import Claim, Ledger
from src.stage2_verification import verify

def test_verify_confirms_fora_de_escopo_apos_segunda_opiniao():
    mock_client = MagicMock()
    # segunda opinião concorda que está fora de escopo mesmo
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"confirma_fora_de_escopo": true}'))
    ]
    claim = Claim(
        texto="liderei migração para Kubernetes",
        fonte="cv",
        classificacao="fora_do_escopo",
        justificativa_classificacao="teste não toca orquestração",
    )
    ledger = Ledger(caso_id="case_07", claims=[claim])
    result = verify(ledger, candidate_code_path="cases/case_07/candidate_code.py", llm_client=mock_client)
    assert result.claims[0].veredito == "nao_verificavel"