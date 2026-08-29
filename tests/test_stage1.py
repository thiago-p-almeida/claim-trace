# tests/test_stage1.py
from unittest.mock import MagicMock
from src.stage1_extraction_triage import extract_and_triage

def test_extract_and_triage_parses_llm_response():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"claims": [{"texto": "resolvi race condition com lock", "fonte": "entrevista", "classificacao": "dentro_do_escopo", "justificativa_classificacao": "teste exige lidar com concorrência"}]}'))
    ]
    ledger = extract_and_triage("CV texto", "Entrevista texto", "Enunciado do teste", "case_01", mock_client)
    assert ledger.caso_id == "case_01"
    assert ledger.claims[0].classificacao == "dentro_do_escopo"