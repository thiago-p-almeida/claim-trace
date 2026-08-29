# tests/test_ledger.py
from src.ledger import Claim, Ledger

def test_ledger_serializes_to_dict():
    claim = Claim(
        texto="resolvi race condition com operação atômica",
        fonte="entrevista",
        classificacao="dentro_do_escopo",
        justificativa_classificacao="teste exige lidar com chamadas concorrentes",
        veredito="pendente",
        metodo_verificacao=None,
        evidencia=None,
    )
    ledger = Ledger(caso_id="case_01", claims=[claim])
    d = ledger.to_dict()
    assert d["caso_id"] == "case_01"
    assert d["claims"][0]["classificacao"] == "dentro_do_escopo"