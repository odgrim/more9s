---
name: value-fix-root-causes
description: "Apply when you're debugging, or about to add a guard, retry, default, clamp, or catch to make a failure go away. Fix the first place the system went wrong, not the place it showed."
disable-model-invocation: true
---

# Fix Root Causes

A symptom shows up downstream of its fault. Patch the symptom and the fault stays, and the next report of it is hidden.

- Trace back from the symptom to the wrong decision in the code: something it does and shouldn't, or a state it should handle and doesn't. That's the cause.
- Ask whether the state that triggered the failure is legitimate. If it is, handle it where the code broke. If it should never exist, find what produced it.
- Don't add a null check, retry, default, clamp, swallowed error, or special case for the test input where the symptom showed. That hides a state that shouldn't exist.
- Search for the same fault elsewhere. Fix the instances in the module you're already touching and list the rest in the report's gaps.
- If the cause took a long dig, propose the log line, metric, or assertion that would have shown it at first look.

## Check

- Can you name where the system first went wrong (a line, a missing handler, two modules that disagree on a contract)? Is the fix there?
