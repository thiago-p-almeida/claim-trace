# tests/test_baseline.py
from unittest.mock import MagicMock
from src.baseline import baseline_verdict

def test_baseline_returns_verdicts():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"verdicts": [{"verdict": "matches"}]}'))
    ]
    claims = [{"text": "led migration Kubernetes"}]
    result = baseline_verdict(claims, "enunciado", "codigo", mock_client)
    assert result[0]["verdict"] == "matches"