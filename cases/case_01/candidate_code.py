import time

class EventDeduper:
    def __init__(self):
        self._events = {}

    def seen(self, event_id, ttl_seconds):
        if not event_id:
            raise ValueError("invalid event_id")
        now = time.time()
        expire_at = self._events.get(event_id)
        if expire_at is not None and expire_at > now:
            return True
        # window check-then-act without lock: simulates real gap from remote call
        # (e.g., checking remote Redis) between read and write state
        time.sleep(0.001)
        self._events[event_id] = now + ttl_seconds
        return False