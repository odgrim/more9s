---
name: standard-organize-by-dependency
description: "Apply when you're deciding where new code lives, creating a directory, package, or module, or adding an import that crosses one. Split by what code may depend on, and give each module one small public surface."
disable-model-invocation: true
---

# Organize by Dependency

A file's path should tell the reader where it runs and what it may import.

- Split top-level directories by where code runs or what it may depend on (`cmd` and `internal`, main and renderer, `core` and `plugins`), not by kind of file (`models`, `utils`, `handlers`).
- Keep imports one-way, with no cycles. Enforce that with the compiler or a linter, not a README.
- If two directories need the same code, move it down to one both may import.
- Give each module one declared public surface. Keep the rest private, by the language or a linter.
- Don't keep a module whose API is about as big as its implementation. It adds nothing, unless it owns a boundary or confines a sharp primitive.

## Check

- Does the path say where this file runs and what it may import? Can a caller use the module from its public surface alone?
