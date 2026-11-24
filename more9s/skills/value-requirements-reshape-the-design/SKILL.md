---
name: value-requirements-reshape-the-design
description: "Apply when a new requirement has to go into an existing design. Design the code as if the requirement had been there from the start, and build toward that. Carry it as a special case (an extra branch, flag, or parameter) only when the reshape isn't yours to make yet."
disable-model-invocation: true
---

# Requirements Reshape the Design

A new requirement is a change to the design. A special case is a branch, flag, or parameter that carries the requirement around the design instead of through it. Each one compounds and pollutes the context for future authors.

- Before the first edit, read the code the requirement touches. Write a sentence or two on how you'd design it from scratch with the requirement included.
- If that design is the current one with an obvious place for the new piece, put it there.
- If it's different and the difference stays inside the module the task owns, reshape the module as if the requirement had always been there. A reshape is part of the task, however big it is. It removes the `Special case:` comments it replaces.
- If the reshape reaches outside that module, open a proposal PR at the bottom of the stack first. It describes the from-scratch design, what it replaces, and the special case that's left if it's rejected. Stack the code on top, so the reviewer agrees to the design before reading the implementation.
- Measure the smallest change that meets the goal against the from-scratch design, not the current code.
- Plan the whole reshape before starting, then land it in small steps that each pass the checks.
- Update the types, docs, examples and comments that still describe the old design.
- You've added a special case if an if/else chain grew one more branch, a second boolean has to agree with the first, or a parameter is only set by one caller.

## When a special case is allowed

Only when the reshape isn't yours to make yet:

1. The reshape reaches outside the module the task owns, and its proposal PR is rejected, or the human asks for the requirement before it's approved.
2. The human set a limit that rules the reshape out: a hotfix, a freeze, a request for the smallest diff.
3. The requirement has a stated end: an experiment's gate, or a deprecated name that `public-interfaces-grow-by-addition` keeps working.

The size of the reshape isn't one of them, and neither is a session that's running long. `stop-and-report` covers work that outgrows its size.

Every special case meets all of these:

- It stays inside one function, and adds no flag that has to stay in sync with another.
- A comment at the site starts `Special case:` and names the design it stands in for. Under the third condition it names what removes it instead.
- The report's decisions name it and the condition that allows it.
- Before you add one, grep the module for `Special case:`. A later session has no other way to know one exists. If one already stands in for the same design, don't add a second. Reshape, or reopen the proposal with both requirements as its evidence.

## Check

- Did you write down the from-scratch design and whether the requirement fit it?
- For each special case you added, which of the three conditions allows it, and do the report's decisions say so?
- Does grepping the module for `Special case:` find at most one for this design?
