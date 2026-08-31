import time
import threading

class EventDeduper:
    def __init__(self):
        self._events = {}
        self._lock = threading.Lock()

    def seen(self, event_id, ttl_seconds):
        if not event_id:
            raise ValueError("invalid event_id")
        now = time.time()
        # BUG: read done outside lock, only write is protected
        expire_at = self._events.get(event_id)
        if expire_at is not None and expire_at > now:
            return True
        time.sleep(0.001)
        with self._lock:
            self._events[event_id] = now + ttl_seconds
        return False