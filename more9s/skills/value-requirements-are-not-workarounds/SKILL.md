---
name: value-requirements-are-not-workarounds
description: "Apply when a new requirement has to go into an existing design. Don't add it as a workaround, such as an extra branch, flag or parameter. Design the code as if the requirement had been there from the start, and build toward that."
disable-model-invocation: true
---

# New Requirements Are Not Workarounds

A new requirement is a change to the design, not a workaround to build on top of it. Each workaround compounds and pollutes the context for future authors.

- Before the first edit, read the code the requirement touches. Write a sentence or two on how you'd design it from scratch with the requirement included.
- If that design is the current one with an obvious place for the new piece, put it there.
- If it's different, you can add one workaround, as long as it stays inside one function and the report names it along with the design it stands in for. Don't add a second one for the same design, and don't add a flag that has to stay in sync with another.
- If you'd need a second, reshape the code instead. Inside the module the task owns, reshape it as if the requirement had always been there. A reshape is part of the task, however big it is.
- If the reshape reaches outside that module, open a proposal PR at the bottom of the stack first. It describes the from-scratch design, what it replaces, and what's left if it's rejected. Stack the code on top, so the reviewer agrees to the design before reading the implementation.
- When `simplest-thing-that-works` asks for the smallest change, measure it against the from-scratch design, not the current code.
- Plan the whole reshape before starting, then land it in small steps that each pass the checks.
- Update the types, docs, examples and comments that still describe the old design.
- You've added a workaround if an if/else chain grew one more branch, a second boolean has to agree with the first, or a parameter is only set by one caller.

## Check

- Did you write down the from-scratch design and whether the requirement fit it?
- Is there at most one workaround for this design?