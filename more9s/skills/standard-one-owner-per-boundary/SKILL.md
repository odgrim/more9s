---
name: standard-one-owner-per-boundary
description: "Apply when code touches the filesystem, environment, network, a subprocess, a third-party library, or an external service, you're deciding where validation goes, or you're reaching for a primitive that takes judgment to use correctly: raw concurrency, timers, reflection, unsafe casts, a low-level library API. Give each external system and each sharp primitive one owning module and send everything else through it."
disable-model-invocation: true
---

# One Owner Per Boundary

Two things get one owning module: an external system, and a sharp primitive. Everything else goes through the owner's API.

- Forbid the direct import or call everywhere else with a lint.
- If a caller needs something new, add it to the owner. Never suppress the lint at the call site.

## An external system

A third-party library counts as an external system if it does I/O or its types would otherwise spread.

- Write the owner's interface in domain terms. It turns raw data into a domain type once, and keeps transport and third-party types inside.
- If the real system is slow, costs money, needs credentials, or isn't available on a developer's machine, ship an in-memory fake with the owner, and run one contract suite against both the fake and the real system so the fake can't drift. If a real run needs credentials or costs money, make it a tagged job and say in the report whether it ran.
- Where the real thing is local and cheap, test against it and write no fake: the filesystem in a temporary directory, a subprocess, the environment passed in as a value.
- Have it set a timeout on every call that leaves the process, take the caller's cancellation, and hold the only retry: bounded, with backoff, for operations safe to repeat.
- Trust the types it returns: don't re-validate or add redundant null checks. If a caller needs the concrete type, the interface is missing a method.
- Put business logic in pure functions over domain types. Keep the code that calls the owner thin.

## A sharp primitive

Callers will get these wrong, so stop them calling the primitive at all.

- A primitive is sharp if a misuse compiles, passes a casual test, and fails in production.
- Call it directly from one small module. Make that module's API cover the legitimate uses and make the correct call the easy one.

## Check

- Does grepping for the external library or the primitive find it in one module only?
- Is this data crossing a boundary right now? If not, the validation is redundant.
