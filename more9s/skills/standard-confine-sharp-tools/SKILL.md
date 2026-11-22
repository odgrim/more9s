---
name: standard-confine-sharp-tools
description: "Apply when reaching for a primitive that needs judgment to use correctly (raw concurrency, timers, direct process or OS calls, reflection, unsafe casts, a low-level library API). Confine the primitive to one owning module and give everyone else a safe API."
disable-model-invocation: true
---

# Confine Sharp Tools

Some primitives need judgment to use correctly: raw concurrency, timers, direct process calls, reflection, unsafe casts. Callers will get them wrong, so stop them from calling the primitive at all.

## Rules

- A primitive is sharp when a misuse compiles, passes a casual test, and fails in production.
- One module calls the primitive directly. Other code goes through that module's API.
- That module's API covers the legitimate uses, and the correct call is the easy one.
- A lint forbids the primitive everywhere else, and its message names the API to use.
- A caller that needs something new adds it to the owning module. It never suppresses the lint at its own call site.
- Keep the owning module small enough to review carefully.

## Check

- Does grepping for the primitive find it in one module only?
- Does the lint fail when the primitive is called outside that module?
