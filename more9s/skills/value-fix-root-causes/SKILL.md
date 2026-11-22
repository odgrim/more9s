---
name: value-fix-root-causes
description: "Apply when debugging, or when about to add a guard, retry, default, clamp, or catch to make a failure go away. Fix the first place the system went wrong, not the place where it showed."
disable-model-invocation: true
---

# Fix Root Causes

A symptom appears downstream of its fault. A change at the symptom leaves the fault in place and hides the next report of it.

- Reproduce the failure before changing behaviour. If it will not reproduce, add instrumentation and read the actual state. Do not guess from reading.
- Trace back from the symptom until you reach a wrong decision in the code: something it does that it should not, or a state it should handle and does not. That is the cause.
- Ask whether the state that triggered the failure is legitimate. If it is, handle it where the code broke. If it should never exist, find what produced it.
- A null check, retry, default value, clamp, swallowed error, or special case for the test input, added where the symptom showed, hides a state that should not exist. It is not a fix.
- Every shipped line traces to evidence from the reproduction. A change that "might help" is a hypothesis. Revert it when the evidence does not support it.
- Search for the same fault elsewhere. Fix the instances in the module the fix already touches. List the rest in the report's gaps, for a separate change.
- When the failure will not reproduce even with instrumentation, the cause is a guess. Ship the instrumentation as the change, label the cause as a guess in the report, and do not ship a fix for it.
- When the cause took a long dig to find, propose the log line, metric, or assertion that would have shown it at first look.

The [contract-first change](../make-more9s/playbooks/contract-first-change.md) playbook puts the failing reproduction before the fix. attack-the-premise applies when two fixes have failed.

## Check

- Does the reproduction fail before the fix and pass after?
- Can you name where the system first went wrong (a line, a missing handler, or two modules that disagree on a contract), and is the fix there?
