**Interviewer:** Talk about a non-trivial technical challenge you solved.

**Marina:** In the webhook dedup system, we had multiple instances
processing the same event at the same time. Initially, we only checked if
the ID already existed in a table before inserting — seemed correct, but two
instances could check and find nothing at the same time, and both would
insert. This is not a rare race condition under high load.

**Interviewer:** How did you avoid this?

**Marina:** Ensuring the check and insertion happen as a single
operation, without a gap where another instance could enter between them.