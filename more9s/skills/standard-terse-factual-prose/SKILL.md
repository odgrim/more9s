---
name: standard-terse-factual-prose
description: "Apply when writing anything a human reads: comments, commit messages, PR descriptions, docs, and replies. Write for a first-read understanding in the fewest words that allow it, and state facts."
disable-model-invocation: true
---

# Terse, Factual Prose

Write so the reader understands on the first read, in the fewest words that keep that true. This covers comments, commit messages, PR descriptions, docs, and replies.

## Comments

- Write one only for what the code cannot say: a reason, a non-obvious consequence, or a constraint from outside the codebase that no check can express.
- Delete a comment that restates the code, describes how it changed, or says what you did.
- A doc comment on an exported name is part of the public contract, not a restatement. Keep it, and write one where the repo's linter or doc tool expects it.
- Fix the cause of a workaround. One whose cause is outside the repo gets a TODO with the upstream link, not a justification, as patterns-spread says.
- A warning to the next editor ("do not change", "must stay in sync") becomes a type, test, or lint where one can express it. Where none can, state the constraint and its reason.
- A TODO carries the issue's URL on its line, or the issue ID or the freezing lint rule in parentheses: `TODO(#123)`, `TODO(lint:<rule>)`. A hook rejects one with neither.

## All prose

- Give the claim and its evidence. Drop adjectives and filler.
- A claim without evidence carries one label: inferred or guess. Do not state it as fact, and do not spread the doubt across the sentence with "might", "should", or "probably".
- Lead with what changes for the reader.
- When a change makes a comment, doc, or agent instruction untrue, fix or delete it in the same change.
- No em dashes. Use a period, comma, or colon, and vary which. A hook rejects them in prose files and code comments you write. Replies and commit messages rely on this line.

## Check

- Delete each sentence in turn. Is anything lost?
