# tests/test_ledger.py
from src.ledger import Claim, Ledger

def test_ledger_serializes_to_dict():
    claim = Claim(
        text="resolved a race condition with an atomic operation",
        source="interview",
        classification="in_scope",
        classification_justification="the test requires handling concurrent calls.",
        verdict="pending",
        verification_method=None,
        evidence=None,
    )
    ledger = Ledger(case_id="case_01", claims=[claim])
    d = ledger.to_dict()
    assert d["case_id"] == "case_01"
    assert d["claims"][0]["classification"] == "in_scope"