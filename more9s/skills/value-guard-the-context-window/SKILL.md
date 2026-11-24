---
name: value-guard-the-context-window
description: "Apply when a command, file, or search is about to return more than the decision needs, or you're about to read something the session already holds. Take in only what the decision needs and keep bulk out of the main thread."
disable-model-invocation: true
---

# Guard the Context Window

Everything you read stays in context for the rest of the session. A full context drops earlier instructions and reasons worse over what's left.

- Estimate a command's output before you run it, and filter at the source: a grep, a line range, a count, a query for one field.
- Read only the part of a file the task needs. Before an edit, read the lines you're about to change. A leaf is the exception: read it in full.
- Don't reread a file the session already holds unless it may have changed: an edit, a formatter, a hook, a generator, a checkout, or a compaction since you read it.
- Send bulk output to a file and read the lines that matter.
- Give broad reading (a sweep across many files, a long log) to a subagent if the harness has one. Have it return the conclusion and the paths, not the contents. Its conclusion is a pointer, not evidence, so read the lines it cites before you rely on them.
- Never cut evidence a check requires. Quote the lines that carry the result and mark the cut.

## Check

- Could your largest read have been a filter, a line range, or a subagent's summary?
