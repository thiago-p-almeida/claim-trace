# src/eval.py
def compute_overconfidence_rate(baseline_results: list[dict], gold_labels: list[dict]) -> float:
    out_of_scope_texts = {
        g["text"] for g in gold_labels if g["expected_classification"] == "out_of_scope"
    }
    if not out_of_scope_texts:
        return None  # <- was 0.0
    ...
    overconfident = 0
    for r in baseline_results:
        if r["text"] in out_of_scope_texts and r["verdict"] in ("matches", "does_not_match"):
            overconfident += 1
    return overconfident / len(out_of_scope_texts)