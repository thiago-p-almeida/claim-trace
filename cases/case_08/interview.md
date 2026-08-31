**Interviewer:** How was your experience leading the team?

**Thiago:** I focused a lot on unblocking the team and reviewing code with
attention to edge cases — especially empty input versus null, which people
sometimes treat as different things by mistake, which I always asked them to
correct in review.

**Interviewer:** How do you avoid this error in your own code?

**Thiago:** I use a check that covers both at once, something like `if not
value`, instead of only checking `is None`.