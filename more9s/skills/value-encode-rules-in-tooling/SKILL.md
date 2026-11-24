---
name: value-encode-rules-in-tooling
description: "Apply when you're correcting a mistake, introducing a convention, or about to add a rule to docs or agent instructions. Enforce it with structure, a lint, or a test before you write more prose."
disable-model-invocation: true
---

# Encode Rules in Tooling

Nothing fails when someone skips a written rule. Use the strongest of these that costs less than the mistake:

1. API design, structure, or types that make the mistake impossible.
2. A lint or CI check.
3. A test, including a fuzz or property test.
4. Prose.

- Add the check with the first correction if any author could repeat the mistake: it broke a standard, a documented convention, or an invariant of the code.
- Skip the check for one person's preference on one change. Name it in the report's decisions with a proposed line for the repo's agent instructions file, because a later session can't recall it. If that file already holds the line, this is the second time and it's a rule.
- Add a convention's check in the change that first uses it.
- Make sure a new check fails on a real instance of the mistake.
- Delete the prose once a tool enforces it.
- Keep a rule that needs judgment as prose, with an example of the failure.

## Check

- If someone made this mistake again tomorrow, would the build fail?
