import time
import threading

class EventDeduper:
    def __init__(self):
        self._events = {}
        self._lock = threading.RLock()

    def seen(self, event_id, ttl_seconds):
        if event_id is None or event_id == "":
            raise ValueError("invalid event_id")
        with self._lock:
            now = time.time()
            expire_at = self._events.get(event_id)
            if expire_at is not None and expire_at > now:
                return True
            self._events[event_id] = now + ttl_seconds
            return False