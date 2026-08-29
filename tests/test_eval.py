# tests/test_eval.py
from src.eval import compute_overconfidence_rate

def test_overconfidence_rate_flags_baseline_confidence_on_out_of_scope():
    baseline_results = [{"texto": "Kubernetes", "veredito": "bate"}]
    gold_labels = [{"texto": "Kubernetes", "classificacao_esperada": "fora_do_escopo"}]
    rate = compute_overconfidence_rate(baseline_results, gold_labels)
    assert rate == 1.0  # baseline deu veredito confiante numa claim fora de escopo