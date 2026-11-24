---
name: standard-errors-point-at-the-problem
description: "Applies when writing an error about user input: a config file, a flag, an argument, a document. Requires the error to say exactly where the input is wrong and what was expected."
disable-model-invocation: true
---

# Errors Point at the Problem

The user's next step is to fix their input. Don't make them hunt for the place.

- Say where: the file, line, and column, or the flag or key by name.
- Show the offending text with the bad part marked, and the value received. Redact a value that could hold a secret.
- Say what was expected and suggest the likely fix, such as the nearest valid name.
- Carry the location as fields on the error. Render the message from them and include them in machine output.
- Keep the location when you wrap. An error from deep in a parser should still name the user's file at the top.
- Report every problem you find in one pass.

## Check

- From the error output alone, can the user go straight to the character that needs changing?
