import time
import threading

class EventDeduper:
    def __init__(self):
        self._events = {}
        self._lock = threading.Lock()

    def seen(self, event_id, ttl_seconds):
        # BUG: no event_id empty/None validation
        now = time.time()
        with self._lock:
            expire_at = self._events.get(event_id)
            if expire_at is not None and expire_at > now:
                return True
            self._events[event_id] = now + ttl_seconds
            return False