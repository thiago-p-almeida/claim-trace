# tests/test_synthesis.py
from src.ledger import Claim, Ledger
from src.synthesis import render_report

def test_render_report_never_recommends_hiring():
    claim = Claim(texto="x", fonte="cv", classificacao="dentro_do_escopo",
                   justificativa_classificacao="y", veredito="contradita",
                   metodo_verificacao="execucao", evidencia="3/50 falharam")
    ledger = Ledger(caso_id="case_01", claims=[claim])
    report = render_report(ledger)
    assert "contratar" not in report.lower()
    assert "rejeitar" not in report.lower()
    assert "3/50 falharam" in report