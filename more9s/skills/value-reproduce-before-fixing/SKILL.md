---
name: value-reproduce-before-fixing
description: "Applies when a failure is reported, before behaviour is changed to fix it. Makes it fail first, and ships only what the reproduction's evidence supports."
disable-model-invocation: true
---

# Reproduce Before Fixing

You can't show a fix works without a reproduction. A cause you read from the code is a hypothesis until something fails because of it.

- Reproduce the failure before you change behaviour. Land the failing reproduction before the fix.
- A test built from the cause you deduced counts if it fails the way the report describes: the same error, the same wrong value. If it fails another way, you've reproduced something else.
- Don't take an ask-first action to reproduce. A failure that only shows on a surface one guards (production, a live account) won't reproduce here.
- If it won't reproduce, add instrumentation and read the actual state. Don't guess from reading.
- Trace every line you ship to evidence from the reproduction. A change that "might help" is a hypothesis. Revert it if the evidence doesn't support it.
- If it still won't reproduce with instrumentation, the cause is a guess. Ship the instrumentation as the change, label the cause a guess in the report, and don't ship a fix for it.

## Check

- Does the reproduction fail before the fix and pass after?
