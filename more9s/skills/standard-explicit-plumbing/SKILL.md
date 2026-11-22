---
name: standard-explicit-plumbing
description: "Apply when writing a function signature or constructor, or when code needs logging, cancellation, configuration, a client, or telemetry. Everything a unit of code depends on reaches it explicitly, not through ambient state."
disable-model-invocation: true
---

# Explicit Plumbing

Everything code depends on reaches it explicitly. A reader finds every input in the signature or the constructor.

## Rules

- A logger, client, or config is passed in, not held in a module-level mutable value, singleton, or process global.
- Pass dependencies the way the repo already does (parameters, constructor, or container), with its naming and order.
- Construct dependencies at the entry point and pass them down. Two instances with different settings (two accounts, two regions) are two values built there. A logging or tracing facade the language expects to be global is installed there and nowhere else.
- To add context, derive a new value and pass it on. The shared one stays unchanged.
- Pass a unit what it uses. A single options or context object that carries everything to everyone is ambient state with a parameter name.
- Cancellation and deadlines are passed the same way. Anything that blocks or does I/O takes the caller's cancellation and stops when it fires.
- Read environment variables, arguments, and the working directory at the entry point, and pass them as values.
- Only the entry point ends the process.

## Check

- Can this code run twice in one process with different settings?
- Does grepping for a dependency's constructor find calls only in entry points and tests?
