---
name: standard-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, keep the checker in force, give semantic primitives their own type, parse external data at boundaries, exhaust variants, derive from authoritative schemas. Without a static checker, model the same way with the nearest construct the language has."
disable-model-invocation: true
---

# Type System Discipline

Make the compiler reject impossible states, mixed-up primitives, and unhandled cases.

## Modelling

- Model variants as one type with distinct cases, not a bag of optional fields or booleans that must agree. State that moves through phases is one such type with its transitions in one place. Where the language has no such type, use a closed interface and a lint.
- Two arguments with the same primitive type and different meanings each get their own type, validated once at creation.
- When a schema file owns a shape, derive the type from it. A hand-written parallel one drifts.

## Using

- A set is closed when every consumer must decide how to handle a new member: an error variant, a state, a mode. It is open when no consumer should need to know a new member exists. When unclear, treat it as closed.
- Handle every case of a closed set explicitly, with no catch-all default, and enable the check that fails when a case is added.
- An open set is a plugin kind, looked up in a registry. See plugin-architecture.
- A set defined outside the codebase, such as an API's status field, can gain members without the build knowing. Parse it at the boundary into a closed type with an explicit unknown case, and handle that case like any other.
- External data (JSON, RPC payloads, CLI args, config, environment variables, database rows) is parsed into a typed model at the boundary.
- No cast, unchecked assertion, or escape type on data that has not been validated.

## Without a static checker

- In a language with no static checker, or with an optional one the repo does not run, the modelling rules still hold. Use the nearest construct the language has (an enum, a frozen record, a tagged value) and validate once at the boundary, where the parse would be.
- The check a compiler would run becomes a test: one that fails when a case is added and not handled.

## Proportion

- Keep plain code when the shape is clear, local, and unlikely to grow. A type earns its place by removing a branch or a state that should not exist. One that adds a layer and removes neither goes.

## Check

- Can you write a value of this type that should never exist?
- Does adding a new case to a closed set fail the build until it is handled?
