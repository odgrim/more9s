---
name: standard-idempotent-operations
description: "Applies when writing a command, lifecycle step, migration, or processing loop that changes state and can be interrupted, retried, or run twice. Requires the same end state however many times it runs and wherever the last run stopped."
disable-model-invocation: true
---

# Idempotent Operations

A state-changing operation will be interrupted, retried, and run twice.

- Work from the state that exists: read it, compare it to the goal, and apply only the difference. Don't rely on a record of what the last run meant to do.
- Replace a file by writing beside it and renaming, so a reader never sees half of one.
- Anything a run can leave behind (a lock, a temporary file, a claimed job) needs evidence the next run can use to tell it's stale: an owner and a liveness check, or an expiry.
- For a step that isn't safe to repeat (a charge, a sent message), send an idempotency key derived from the operation, not the run. If the remote takes no key, attach a reference it stores and ask for it before repeating. If it offers neither, stop the rerun there and say so.
- Retry only what's safe to repeat.
- Offer a dry run that prints the difference for anything that changes state outside the process.

## Check

- Run it twice, then kill it between two steps and run it again. Does it end in the same correct state each time?
