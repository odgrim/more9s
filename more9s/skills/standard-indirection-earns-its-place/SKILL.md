---
name: standard-indirection-earns-its-place
description: "Applies when adding a wrapper, interface, layer, or option, or when code is hard to trace. Keeps indirection only where it hides real complexity or sits on an enforced boundary, and keeps state as local as possible."
disable-model-invocation: true
---

# Indirection Earns Its Place

A reader pays for every layer between a question and its answer, and for every piece of state they have to hold in their head.

- Add an interface only when it has two implementations today. A test fake counts only for a module that owns an external boundary.
- Add an option only when a caller sets it today, unless another standard requires it: a flag's environment variable, a dry run, the machine-format flag.
- Inline the rest: single-caller wrappers, functions that only pass a call along, one-implementation interfaces.
- Keep a module that owns a boundary or confines a sharp primitive. A lint depends on it.
- Prefer a return value to a mutation, a local to a field, and a field to module state.
- Make each decision in one place and pass its result. Derive a value instead of keeping two in sync.

## Check

- Can you find where a value comes from, and what can change it, by grepping for it?
