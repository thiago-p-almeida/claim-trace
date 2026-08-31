# tests/test_eval.py
from src.eval import compute_overconfidence_rate

def test_overconfidence_rate_flags_baseline_confidence_on_out_of_scope():
    baseline_results = [{"text": "Kubernetes", "verdict": "matches"}]
    gold_labels = [{"text": "Kubernetes", "expected_classification": "out_of_scope"}]
    rate = compute_overconfidence_rate(baseline_results, gold_labels)
    assert rate == 1.0  # baseline gave confident verdict on an out-of-scope claim