---
name: standard-explicit-plumbing
description: "Apply when you're writing a function signature or constructor, or code needs logging, cancellation, configuration, a client, or telemetry. Pass everything a unit depends on explicitly, not through ambient state."
disable-model-invocation: true
---

# Explicit Plumbing

A reader should find every input in the signature or the constructor, and the code should be able to run twice in one process with different settings.

- Pass in a logger, client, or config. Don't keep one in a module-level mutable value, singleton, or process global. Pass it the way the repo already does.
- Build dependencies at the entry point and pass them down. If the language expects a global logging or tracing facade, install it there and nowhere else.
- Read environment variables, arguments, and the working directory at the entry point and pass them as values. Only the entry point ends the process.
- Pass a unit only what it uses. One context object that carries everything to everyone is ambient state with a parameter name.
- To add context, derive a new value and pass that on. Leave the shared one unchanged.
- Anything that blocks or does I/O takes the caller's cancellation and stops when it fires.

## Check

- Does grepping for a dependency's constructor find calls only in entry points and tests?
