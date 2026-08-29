# tests/test_execution_harness.py
from src.execution_harness import run_concurrency_stress_test

def test_stress_test_detects_race_condition(tmp_path):
    buggy_code = '''
class EventDeduper:
    def __init__(self):
        self.seen_events = {}
    def seen(self, event_id, ttl_seconds):
        if not event_id:
            raise ValueError("event_id vazio")
        if event_id in self.seen_events:
            return True
        self.seen_events[event_id] = True
        return False
'''
    candidate_file = tmp_path / "candidate.py"
    candidate_file.write_text(buggy_code)
    result = run_concurrency_stress_test(str(candidate_file), n_threads=20, iterations=50)
    assert result["total"] == 20
    assert result["failure_rate"] > 0  # dict não é thread-safe em check-then-act
    