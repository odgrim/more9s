---
name: standard-one-owner-per-boundary
description: "Apply when code touches the filesystem, environment, network, a subprocess, a third-party library, or an external service, and when deciding where validation goes. One module owns each external system and everything else goes through it."
disable-model-invocation: true
---

# One Owner Per Boundary

Each external system (filesystem, network, subprocess, service) has one module that talks to it. So does a third-party library that does I/O or whose types would otherwise spread. Everything else imports that module.

## The owner

- Its interface is in domain terms. Third-party and transport types stay out of it.
- It turns raw data into a domain type once.
- It ships an in-memory fake. Callers' tests use the fake in place of patching the real system.
- One contract test suite runs against both the fake and the real system, so the fake cannot drift. Where the real system needs credentials or costs money, the real run is a tagged job the repo documents, and the report says whether it ran.
- It sets a timeout on every call that leaves the process, and takes the caller's cancellation.
- It retries only operations that idempotent-operations says are safe to repeat, with a bounded count and backoff. Callers do not add a second retry around it.
- A lint forbids the direct import or call elsewhere, and its message names the owner.

## Callers

- Trust the types the owner returns. No re-validation and no redundant null checks.
- If you need the concrete type, the interface is missing a method. Add it in place of a downcast, cast, or runtime check.
- Business logic lives in pure functions over domain types. The code that calls the owner stays thin.

## Check

- Does grepping for the external library find it in one module?
- Does the contract suite pass against the fake and against the real system?
- Is this data crossing a boundary right now? If not, the validation is redundant.
