---
name: standard-errors-are-typed-values
description: "Apply when returning, raising, wrapping, catching, or testing an error. Callers branch on an error's type or identity, not on its text, and an error about user input points at the exact place that is wrong."
disable-model-invocation: true
---

# Errors Are Typed Values

Callers branch on an error's type. Its text is for people.

## Defining

- Each failure a caller handles differently has its own documented type, variant, or code.

## Pointing at the problem

- An error about user input says where the input is wrong: the file, line, and column, or the flag or key by name.
- Show the offending text with the bad part marked, and the value that was received. A value that can hold a secret is shown redacted, as secrets-and-untrusted-input requires.
- Say what was expected. When there is a likely fix, such as the nearest valid name, suggest it.
- Carry the location as fields on the error. The message is rendered from them, and machine output includes them.
- Keep the location when wrapping. An error from deep in a parser still names the user's file at the top.
- When validating user input, report every problem found in one pass.

## Handling

- Wrap an error so the original is still reachable and still matches.
- Pass an error up or handle it. Log it where it is handled, not on the way up.
- A discarded result, unchecked return, unawaited call, or empty catch carries a named suppression with its reason.
- Catch only what you can handle.

## Aborting

- A panic, assertion, or unrecoverable throw is for a programmer error only.
- Bad input, I/O, and network failures are ordinary errors. They return an error and do not abort.
- An abort is intercepted at the top of a process, request, or task, and nowhere below.

## Check

- Can a caller tell this failure from the others without reading its message?
- Do the tests assert the type, variant, or code?
- Given only the error output, can the user go straight to the character that needs changing?
