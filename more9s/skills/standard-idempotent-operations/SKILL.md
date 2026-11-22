---
name: standard-idempotent-operations
description: "Apply when writing a command, lifecycle step, migration, or processing loop that changes state and can be interrupted, retried, or run twice. The operation reaches the same end state however many times it runs and wherever the last run stopped."
disable-model-invocation: true
---

# Idempotent Operations

A state-changing operation will be interrupted, retried, and run twice. It reaches the same end state each time.

## Rules

- Work from the state that exists. Read it, compare it to the goal, and apply only the difference. Do not rely on a record of what the previous run meant to do.
- Write a file to a temporary path beside the target and rename it into place. A reader sees the old file or the new one, never part of one.
- Anything a run can leave behind (a lock, a temporary file, a claimed job, a half-written record) carries evidence the next run can use to tell it is stale: an owner and a liveness check, or an expiry.
- A step that cannot be repeated safely (a charge, a sent message, a non-idempotent API call) sends an idempotency key the remote honours, derived from the operation and not from the run.
- Where the remote takes no key, attach a reference the remote stores, and have the rerun ask the remote for it before repeating the step. A local completion record written after the step does not cover a crash between the two.
- Where the remote can neither take a key nor be asked, the step is not safe to rerun. The operation stops there on a rerun and says so.
- A retry is allowed only for an operation that is safe to repeat.
- Offer a dry run for an operation that changes something outside the process. It prints the difference it would apply.

## Check

- Run it twice. Does the second run change nothing?
- Kill it between any two steps and run it again. Does it finish in the correct state?
