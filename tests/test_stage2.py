# tests/test_stage2.py
from unittest.mock import MagicMock
from src.ledger import Claim, Ledger
from src.stage2_verification import verify

def test_verify_confirms_out_of_scope_after_second_opinion():
    mock_client = MagicMock()
    # second opinion agrees it's out of scope
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"confirms_out_of_scope": true}'))
    ]
    claim = Claim(
        text="led migration to Kubernetes",
        source="cv",
        classification="out_of_scope",
        classification_justification="test does not touch orchestration",
    )
    ledger = Ledger(case_id="case_07", claims=[claim])
    result = verify(ledger, candidate_code_path="cases/case_07/candidate_code.py", llm_client=mock_client)
    assert result.claims[0].verdict == "unverifiable"