---
name: value-do-not-copy-workarounds
description: "Applies on finding code that makes up for a fault somewhere else, or before writing some. Fixes the fault where it is."
disable-model-invocation: true
---

# Do Not Copy Workarounds

A workaround left in place gets copied.

- Don't copy a workaround, and don't write a new one beside it.
- The one exception is a fault outside the repo (a third-party library, a service, a platform) that you can't fix from here. Put that workaround in the module that owns the boundary, with a TODO linking the upstream issue, or the upstream source that shows the fault if there's no issue.
- If you find a workaround the task doesn't need, name it in the report. Freeze it when asked, or when the task would otherwise copy or extend it.
- If the task needs a frozen workaround again, fix the design. Do the same for a string of workarounds that all cover one underlying problem.

The [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook covers freezing a workaround and landing a design fix.

## Check

- Did you add or copy code that only makes up for a fault elsewhere? If so, is the fault outside the repo, and linked?
