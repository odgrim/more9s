---
name: value-guard-the-context-window
description: "Apply when a command, file, or search is about to return more than the decision needs, when about to read something the session already holds, or when sizing work that may not fit one session. Take in only what the decision needs and keep bulk out of the main thread."
disable-model-invocation: true
---

# Guard the Context Window

Everything read stays in context for the rest of the session. A full context drops earlier instructions and reasons worse over what remains.

- Estimate a command's output before running it. Filter at the source: a grep, a line range, a count, a query for the one field.
- Read the part of a file the task needs. Do not reread a file the session already holds unless it may have changed: an edit, a formatter, a hook, a generator, a checkout, or a compaction since the read. Before an edit, read the lines you are about to change. A leaf is the exception: read it in full, as make-more9s requires.
- Send bulk output to a file and read the lines that matter. The report quotes from it, as change-composition describes.
- Hand broad reading (a sweep across many files, a long log) to a subagent where the harness has one. It returns the conclusion and the paths, not the contents. Its conclusion is a pointer, not evidence. Read the lines it cites before relying on them, as prove-it-works requires.
- A subagent that writes gets the brief make-more9s describes under Subagents.
- Size the work to the window. State the size at the start, in units and files. stop-and-report uses it. Split a task that will not fit into units that each end in a commit and a written state the next session can start from.
- Write a decision and its reason into the commit message or the report when you make it. Do not rely on recalling it after the context is compacted.
- Never cut evidence a check requires. Quote the lines that carry the result and mark the cut, as change-composition describes.

## Check

- Could the session's largest read have been a filter, a line range, or a subagent's summary?
- Could a new session continue from the commits and the report alone?
