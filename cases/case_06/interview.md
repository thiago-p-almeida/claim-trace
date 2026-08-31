**Interviewer:** Why choose `RLock` instead of normal `Lock`?

**Diego:** Because if the same thread needs to reacquire the lock — for
example, if I extract part of the logic to an auxiliary method that also uses
the lock — a regular `Lock` would deadlock on itself. `RLock` allows safe
re-entrancy.

**Interviewer:** And input validation?

**Diego:** I treat `None` and empty string as equivalent — both mean
"I don't have a valid identifier".