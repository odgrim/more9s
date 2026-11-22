---
name: value-simplest-thing-that-works
description: "Apply when sizing a change, or when tempted to add an abstraction, option, layer, or dependency. Write the simplest code that solves the actual problem and respects the type system."
disable-model-invocation: true
---

# Simplest Thing That Works

Write the simplest code that solves the problem in front of you and respects the type system. Every extra part is something the next reader has to understand and the next change has to keep working. A type that type-system-discipline requires stays.

- Search for an existing function before writing one.
- Use the standard library and the repo's existing dependencies. A new dependency is a decision for the reviewer. secrets-and-untrusted-input says how one is checked and landed.
- Delete the dead code and obsolete paths your change touches or replaces before building on them.
- Leave code the task does not touch alone. Cleanup you notice goes in a separate change. The same fault inside the module a bug fix touches is part of the fix, as fix-root-causes says.
- A requirement that does not fit the design is handled as patterns-spread says: one local special case, then a reshape. The reshape is in scope.
- experience-first chooses what the user meets. This leaf then picks the simplest code that delivers it.

code-organization says when an interface, option, or wrapper earns its place.

## Check

- For each parameter, branch, and type this change added: does the contract or a standard require it? If not, delete it. Passing tests do not show that existing code is unneeded.
- Does every hunk in the diff serve the task?
