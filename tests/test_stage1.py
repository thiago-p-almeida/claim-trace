# tests/test_stage1.py
from unittest.mock import MagicMock
from src.stage1_extraction_triage import extract_and_triage

def test_extract_and_triage_parses_llm_response():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"claims": [{"text": "resolvi race condition com lock", "source": "interview", "classification": "in_scope", "classification_justification": "teste exige lidar com concorrência"}]}'))
    ]
    ledger = extract_and_triage("CV texto", "Entrevista texto", "Enunciado do teste", "case_01", mock_client)
    assert ledger.case_id == "case_01"
    assert ledger.claims[0].classification == "in_scope"