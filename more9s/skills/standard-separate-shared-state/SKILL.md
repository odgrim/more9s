---
name: standard-separate-shared-state
description: "Applies when concurrent actors (threads, processes, CI jobs, agents) might write the same file, branch, key, or object. Gives each actor its own write target first, and coordinates access only when one shared target is a real requirement."
disable-model-invocation: true
---

# Separate Shared State

Two writers on one target need coordination, and coordination is where the bugs are.

- Before you share state between actors, ask what happens if another actor changes it mid-operation. If the answer isn't "nothing", separate them.
- Give each actor its own file, key, branch, worktree, or directory. Combine the results where they're read.
- Two actors writing different fields of one file still share the file.
- Share one write target only when the requirement is a single shared value: a counter, a ledger, a lease.
- Then enforce access with a mechanism: one writer, sequential phases, a lock with stale detection, or compare-and-swap. A comment or an instruction to an agent isn't a mechanism. Keep the mechanism's primitive in one module.

## Check

- For each thing written, can you name its one writer, or the mechanism that orders the writers?
