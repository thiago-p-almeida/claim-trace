# src/execution_harness.py
import importlib.util
import threading
import uuid

def _load_candidate_class(candidate_module_path: str):
    spec = importlib.util.spec_from_file_location("candidate", candidate_module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EventDeduper

def run_concurrency_stress_test(candidate_module_path: str, n_threads: int, iterations: int) -> dict:
    EventDeduper = _load_candidate_class(candidate_module_path)
    deduper = EventDeduper()
    same_event_id = str(uuid.uuid4())
    results = []
    lock = threading.Lock()

    def worker():
        try:
            r = deduper.seen(same_event_id, ttl_seconds=60)
        except Exception:
            r = "error"
        with lock:
            results.append(r)

    failures = 0
    for _ in range(iterations):
        results.clear()
        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # correto: exatamente 1 thread deveria ver False (primeira), resto True
        if results.count(False) != 1:
            failures += 1

    return {
        "total": iterations,
        "failures": failures,
        "failure_rate": failures / iterations,
    }