---
name: value-encode-rules-in-tooling
description: "Apply when correcting a mistake, introducing a convention, or about to add a rule to docs or agent instructions. Enforce the rule with structure, a lint, or a test before writing more prose."
disable-model-invocation: true
---

# Encode Rules in Tooling

Nothing fails when a written rule is skipped. Use the strongest of these that costs less than the mistake:

1. API design, structure, or types that make the mistake impossible.
2. A lint or CI check.
3. A test, including a fuzz or property test.
4. Prose.

- Add the check with the first correction when any author could repeat the mistake: it broke a standard, a documented convention, or an invariant of the code. A correction that is one person's preference for one change gets no check. The second time it comes, it is a rule.
- A convention gets its check in the change that first uses it, or in its own PR of the same stack when existing code fails it.
- A new check has to fail on a real instance of the mistake.
- Fix the code. Never loosen the check to make it pass. A suppression, skip, or new exemption loosens it, and checks-and-exemptions says what that requires. A check that is itself wrong is fixed in its own change, and the report says so.
- Delete the prose once a tool enforces it.
- A rule that needs judgment stays as prose, with an example of the failure.

checks-and-exemptions says how a check's message, suppressions, and exemption list are written.

## Check

- Would this mistake fail the build if someone made it again tomorrow?
