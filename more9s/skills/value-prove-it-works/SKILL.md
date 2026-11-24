---
name: value-prove-it-works
description: "Apply when you've finished a task, before you call it done. Exercise the real artifact, not a proxy or 'it compiles'."
disable-model-invocation: true
---

# Prove It Works

A passing build shows the code compiles, not that it does what was asked.

- Run what ships (the binary, the app, the published package) through the real flow and read the actual output. A self-report or cached output isn't evidence.
- Watch each new check fail before you trust it.
- If a check fails unexpectedly, confirm it measured what you think before you change the system.
- Never hand the user a check you could run yourself.
- A check on the wrong surface, or one that came back inconclusive, isn't a pass. Say which it was.
- Prefer a check CI also runs, so the reviewer reads the run and not your quote of it.
- If the real flow is an ask-first action (an apply, a deploy, a publish), verify on the nearest surface you're allowed to use (a plan, a dry run, a sandbox) and name the gap in the report.

## Check

- For each claim in the report, is there a command and the output lines that carry it, so a reviewer can rerun it with one command?
