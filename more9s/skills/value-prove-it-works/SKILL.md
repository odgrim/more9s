---
name: value-prove-it-works
description: "Apply after completing a task, before declaring it done. Exercise the real artifact, not a proxy or 'it compiles'."
disable-model-invocation: true
---

# Prove It Works

A change is done when it has been checked against the real thing. A passing build shows that the code compiles, not that it does what was asked.

- Run what ships (the binary, the app, the published package) through the real flow and read the actual output. A passing build, a self-report, and cached output are not evidence.
- See each new check fail before trusting it.
- When a check fails unexpectedly, confirm it measured what you think before changing the system.
- Never hand over a check you could run.
- A check on the wrong surface, or one that came back inconclusive, is not a pass. Say which it was.
- Prefer a check CI also runs, so the reviewer reads the run and not your quote of it. Redact quoted output as secrets-and-untrusted-input requires.
- Where the real flow would take effect outside the PR (an apply, a deploy, a publish), the-pr-is-the-guard says how far to go.

change-composition says which checks to run and what the report lists. explain-the-number applies when the evidence is a measured number.

## Check

- Does the report hold, for each claim, the command and the verbatim lines of output that carry it, so a reviewer can rerun any one of them with one command?
