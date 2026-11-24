---
name: standard-confine-sharp-tools
description: "Apply when you're reaching for a primitive that takes judgment to use correctly: raw concurrency, timers, direct process or OS calls, reflection, unsafe casts, a low-level library API. Confine it to one owning module and give everyone else a safe API."
disable-model-invocation: true
---

# Confine Sharp Tools

Callers will get these wrong, so stop them calling the primitive at all.

- A primitive is sharp if a misuse compiles, passes a casual test, and fails in production.
- Call it directly from one small module. Make that module's API cover the legitimate uses and make the correct call the easy one.
- Forbid the primitive everywhere else with a lint.
- If a caller needs something new, add it to the owning module. Never suppress the lint at the call site.

## Check

- Does grepping for the primitive find it in one module only?
