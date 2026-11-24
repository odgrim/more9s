---
name: standard-errors-are-typed-values
description: "Apply when you're returning, raising, wrapping, catching, or testing an error. Callers branch on an error's type or identity, not its text."
disable-model-invocation: true
---

# Errors Are Typed Values

An error's text is for people and will be reworded. A caller that matches on it breaks when that happens.

- Give each failure a caller handles differently its own documented type, variant, or code. Assert that in tests, not the message.
- Wrap an error so the original is still reachable and still matches.
- Pass an error up or handle it. Log it where it's handled, not on the way up. Catch only what you can handle.
- If you discard a result, skip a return check, leave a call unawaited, or leave a catch empty, add a named suppression with its reason.
- Treat bad input, I/O, and network failures as ordinary errors. Keep panics and assertions for programmer errors, and intercept them only at the top of a process, request, or task.

## Check

- Can a caller tell this failure from the others without reading its message?
