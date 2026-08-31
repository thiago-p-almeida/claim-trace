**Interviewer:** How do you design a function that needs to be called
concurrently by multiple threads, handling the same identifier?

**Camila:** I put the entire critical section — reading and writing the
shared state — inside the same lock, from start to finish. I don't let any
read "escape" outside the protected section, because that's exactly the
interval that causes race conditions.

**Interviewer:** And invalid input, like an empty identifier?

**Camila:** I reject it before anything else, with a simple "falsy" check at
the beginning of the function.