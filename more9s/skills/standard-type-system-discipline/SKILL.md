---
name: standard-type-system-discipline
description: "Applies when designing types, a function signature, or stateful logic, with or without a static checker. Makes illegal states unrepresentable, gives semantic primitives their own type, and parses external data at the boundary."
disable-model-invocation: true
---

# Type System Discipline

A state the type can't hold is a bug nobody has to test for.

- Model variants as one type with distinct cases, not a bag of optional fields or booleans that have to agree. Model state that moves through phases the same way, with its transitions in one place.
- If two arguments share a primitive type and mean different things, give each its own type, validated once at creation.
- If two arguments have to agree, take one and derive the other inside.
- Parse external data (JSON, RPC payloads, CLI args, config, environment variables, database rows) into a typed model at the boundary. Don't use a cast, unchecked assertion, or escape type on data that hasn't been validated.
- If a schema file owns a shape, derive the type from it. A hand-written parallel one drifts.
- Without a static checker, model the same way with the nearest construct (an enum, a frozen record, a tagged value) and validate once at the boundary.
- Keep plain code when the shape is clear, local, and unlikely to grow. A type earns its place by removing a branch or a state that shouldn't exist.

## Check

- Can you write a value of this type that should never exist?
