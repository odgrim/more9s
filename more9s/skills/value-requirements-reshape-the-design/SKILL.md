---
name: value-requirements-reshape-the-design
description: "Apply when a new requirement has to go into an existing design. Don't add it as a special case, such as an extra branch, flag or parameter. Design the code as if the requirement had been there from the start, and build toward that."
disable-model-invocation: true
---

# Requirements Reshape the Design

A new requirement is a change to the design. A special case is a branch, flag, or parameter that carries the requirement around the design instead of through it. Each one compounds and pollutes the context for future authors.

- Before the first edit, read the code the requirement touches. Write a sentence or two on how you'd design it from scratch with the requirement included.
- If that design is the current one with an obvious place for the new piece, put it there.
- If it's different, you can add one special case, as long as it stays inside one function. Put a comment at the site that starts `Special case:` and names the design it stands in for, and name it in the report. Don't add a flag that has to stay in sync with another.
- Before you add one, grep the module for `Special case:`. A later session has no other way to know one exists. If one already stands in for the same design, reshape the code instead.
- Inside the module the task owns, reshape it as if the requirement had always been there. A reshape is part of the task, however big it is. It removes the `Special case:` comments it replaces.
- If the reshape reaches outside that module, open a proposal PR at the bottom of the stack first. It describes the from-scratch design, what it replaces, and what's left if it's rejected. Stack the code on top, so the reviewer agrees to the design before reading the implementation.
- Measure the smallest change that meets the goal against the from-scratch design, not the current code.
- Plan the whole reshape before starting, then land it in small steps that each pass the checks.
- Update the types, docs, examples and comments that still describe the old design.
- You've added a special case if an if/else chain grew one more branch, a second boolean has to agree with the first, or a parameter is only set by one caller.

## Check

- Did you write down the from-scratch design and whether the requirement fit it?
- Does grepping the module for `Special case:` find at most one for this design?
