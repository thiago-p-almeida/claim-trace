# tests/test_synthesis.py
from src.ledger import Claim, Ledger
from src.synthesis import render_report

def test_render_report_never_recommends_hiring():
    claim = Claim(
        text="x",
        source="cv",
        classification="in_scope",
        classification_justification="y",
        verdict="contradicted",
        verification_method="execution",
        evidence="3/50 failures"
    )
    ledger = Ledger(case_id="case_01", claims=[claim])
    report = render_report(ledger)
    assert "hire" not in report.lower()