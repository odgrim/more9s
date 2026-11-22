---
name: standard-code-organization
description: "Apply when deciding where new code lives, creating a directory, package, or module, adding an import that crosses one, or adding a layer, wrapper, interface, or option. Top-level directories are split by what code may depend on, each module exposes one small API, and the import rules are enforced by tooling."
disable-model-invocation: true
---

# Code Organization

A file's path should tell you where it runs and what it may import.

## Top-level directories

- Split by where code runs or what it may depend on (`cmd` and `internal`, main and renderer, `core` and `plugins`). Not by kind of file (`models`, `utils`, `handlers`).
- Imports go one way, with no cycles. The compiler or a linter enforces this, not a README or comment.
- Code two directories need moves down to one both may import.

## Modules

- Each module has one declared public surface: an entry file where the language has one, exported names otherwise. The rest is private. Where the language cannot enforce that, a linter does.
- If the API is about as large as the implementation, the module is only adding slop.

## Indirection

- Keep a wrapper, interface, or layer only if it hides real complexity, sits on an enforced boundary, or is the contract a set of plugins implements.
- A module that owns a boundary or confines a risky primitive stays, because a lint depends on it.
- An interface needs two implementations today. A test fake counts only for a boundary owner, as one-owner-per-boundary describes. Two implementations earn an interface, not a plugin kind. plugin-architecture says when a registry is earned.
- An option needs a caller that sets it today. An option another standard requires (a flag's environment variable, a dry run, the machine-format flag) is part of the contract and needs none.
- Inline the rest: single-caller wrappers, functions and types that only pass a call along, one-implementation interfaces.
- Keep state local. Prefer a return value to a mutation, a local to a field, and a field to module state.
- Make a decision in one place and pass its result. Derive a value in place of keeping two in sync.

## Check

- Does the path say where this file runs and what it may import?
- Can a caller use the module after reading only its public surface?
- Can you find where a value comes from, and what can change it by simply grepping for it?

Raise a no, even when the fix belongs in a separate change.
