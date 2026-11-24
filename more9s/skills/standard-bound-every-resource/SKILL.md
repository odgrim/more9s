---
name: standard-bound-every-resource
description: "Applies when code reads input whose size it doesn't control, collects results, starts concurrent work, fills a queue, buffer, or cache, or waits in a loop. Gives each one a stated limit and a defined behaviour when the limit is reached."
disable-model-invocation: true
---

# Bound Every Resource

Code with no limit passes on the test input and fails on the first large one.

- Read input whose size you don't control as a stream or in pages. If it has to sit in memory, set a maximum size and fail with a typed error that names the limit.
- Follow every page of a paginated result, or stop at a stated cap and say in the output that it was reached. Never return the first page as if it were everything.
- Cap concurrent work with a fixed pool or a semaphore. Don't start one task per item.
- Give a queue, buffer, or cache a maximum size, and decide what happens when it's full: block, reject, or evict.
- Bound a loop that waits on a condition with a deadline or an attempt count. `one-owner-per-boundary` sets the timeout on a call that leaves the process.
- Release what you acquire on every path, including errors and cancellation: a file, a connection, a subprocess, a temporary directory.
- Give each limit a named constant. Make it an option only when a caller sets it today, as `indirection-earns-its-place` says.

## Check

- For each read, collection, and fan-out you added, can you name its limit and what happens when it's reached?
