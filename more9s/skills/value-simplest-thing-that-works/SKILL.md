---
name: value-simplest-thing-that-works
description: "Apply when you're sizing a change, or tempted to add an abstraction, option, layer, or dependency. Write the simplest code that solves the actual problem and respects the type system."
disable-model-invocation: true
---

# Simplest Thing That Works

Every extra part is one more thing the next reader has to understand and the next change has to keep working.

- Search for an existing function before you write one.
- A new dependency is an extra part. `vet-new-dependencies` says what comes first.
- Before you build on dead code or an obsolete path your change touches or replaces, delete it.
- Leave code the task doesn't touch alone. Name any cleanup you notice in the report's gaps, and do it when asked, as a separate change.
- Never simplify away what a standard requires. A type that rules out an illegal state stays.

## Check

- For each parameter, branch, and type you added: does the contract or a standard require it? If not, delete it. Passing tests don't show that existing code is unneeded.
- Does every hunk in the diff serve the task?
