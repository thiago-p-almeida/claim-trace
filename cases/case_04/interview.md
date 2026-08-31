**Interviewer:** You mentioned guard clauses in the CV — give an example of
how you would apply this in a function that receives an external identifier?

**Bruno:** The first thing I write is the parameter check — if it comes
empty or null, I raise an exception immediately. This prevents a validation
bug from appearing later, in the middle of the business logic, where it's more
expensive to track.