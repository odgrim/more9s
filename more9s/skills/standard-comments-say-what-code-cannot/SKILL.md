---
name: standard-comments-say-what-code-cannot
description: "Apply when you're writing, keeping, or deleting a code comment or a TODO. Write one only for what the code can't say."
disable-model-invocation: true
---

# Comments Say What Code Cannot

A comment that restates the code is one more thing to keep true.

- Write a comment for a reason, a non-obvious consequence, or a constraint from outside the codebase that no check can express.
- Delete one that restates the code, describes how it changed, or says what you did.
- Keep a doc comment on an exported name. It's part of the public contract. Write one wherever the repo's linter or doc tool expects it.
- Turn a warning to the next editor ("do not change", "must stay in sync") into a type, test, or lint if one can express it. If none can, state the constraint and its reason.
- On a TODO, put the issue's URL on its line, or the issue ID or the freezing lint rule in parentheses: `TODO(#123)`, `TODO(lint:<rule>)`. The more9s hook flags one with neither.

## Check

- Would the code be harder to change correctly without this comment?
