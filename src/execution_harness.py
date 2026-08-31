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
    results = []
    lock = threading.Lock()

    def worker(event_id):
        try:
            r = deduper.seen(event_id, ttl_seconds=60)
        except Exception:
            r = "error"
        with lock:
            results.append(r)

    failures = 0
    for _ in range(iterations):
        results.clear()
        # FIX: new event_id for each iteration — reusing the same id with long TTL
        # would cause iterations 2+ to always return True correctly (event
        # already registered), inflating false positive failures.
        event_id = str(uuid.uuid4())
        threads = [threading.Thread(target=worker, args=(event_id,)) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if results.count(False) != 1:
            failures += 1

    return {
        "total": iterations,
        "failures": failures,
        "failure_rate": failures / iterations,
    }

def run_validation_check(candidate_module_path: str) -> dict:
    EventDeduper = _load_candidate_class(candidate_module_path)

    def raises_value_error(value):
        try:
            EventDeduper().seen(value, ttl_seconds=60)
            return False
        except ValueError:
            return True
        except Exception:
            return False

    empty_ok = raises_value_error("")
    none_ok = raises_value_error(None)
    return {
        "empty_raises_valueerror": empty_ok,
        "none_raises_valueerror": none_ok,
        "validates_correctly": empty_ok and none_ok,
    }