---
name: standard-one-owner-per-boundary
description: "Apply when code touches the filesystem, environment, network, a subprocess, a third-party library, or an external service, or you're deciding where validation goes. Give each external system one owning module and send everything else through it."
disable-model-invocation: true
---

# One Owner Per Boundary

A third-party library counts as an external system if it does I/O or its types would otherwise spread.

- Write the owner's interface in domain terms. It turns raw data into a domain type once, and keeps transport and third-party types inside.
- Ship an in-memory fake with it, and run one contract suite against both the fake and the real system so the fake can't drift. If a real run needs credentials or costs money, make it a tagged job and say in the report whether it ran.
- Have it set a timeout on every call that leaves the process, take the caller's cancellation, and hold the only retry: bounded, with backoff, for operations safe to repeat.
- Forbid the direct import or call everywhere else with a lint.
- Trust the types it returns: don't re-validate or add redundant null checks. If a caller needs the concrete type, the interface is missing a method.
- Put business logic in pure functions over domain types. Keep the code that calls the owner thin.

## Check

- Does grepping for the external library find it in one module?
- Is this data crossing a boundary right now? If not, the validation is redundant.
