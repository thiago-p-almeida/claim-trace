**Interviewer:** How do you handle invalid input in your functions?

**Daniel:** I always validate all user input before processing, including empty strings and null values. Reject them early with clear error messages.

**Interviewer:** What about edge cases like string vs null?

**Daniel:** I treat empty string the same way as null — both mean "no valid identifier provided". The first thing I write is a simple falsy check before any business logic.
