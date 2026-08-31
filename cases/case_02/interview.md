**Interviewer:** How do you ensure a shared structure is safe under concurrency?

**Rafael:** I use a lock around the part that writes to the shared dictionary. This prevents two threads from writing at the same time and corrupting the data.

**Interviewer:** And the reading part, before deciding whether to write or not?

**Rafael:** Normally reading by itself is fast enough not to need a lock — what matters is protecting the writing.