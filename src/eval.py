# src/eval.py
def compute_overconfidence_rate(baseline_results: list[dict], gold_labels: list[dict]) -> float:
    fora_de_escopo_textos = {
        g["texto"] for g in gold_labels if g["classificacao_esperada"] == "fora_do_escopo"
    }
    if not fora_de_escopo_textos:
        return 0.0
    overconfident = 0
    for r in baseline_results:
        if r["texto"] in fora_de_escopo_textos and r["veredito"] in ("bate", "nao_bate"):
            overconfident += 1
    return overconfident / len(fora_de_escopo_textos)