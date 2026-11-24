---
name: value-patterns-spread
description: "Apply when you're about to copy existing code, the repo does one thing two ways, or you'd have written it differently. Work out whether the existing way is current before you copy it, because the next author will copy yours."
disable-model-invocation: true
---

# Patterns Spread

Existing code isn't proof of the right way. The newest code is the most likely to be a copy.

- **A different style.** If the repo's way works and you'd have written it differently, use the repo's way and name the better one in the report. Introduce a new way only when asked. Do the same when the existing way breaks a standard.
- **A replaced way.** If the repo already holds the replacement (a newer API, a lint message that names one, an exemption list, a deprecation note), use the replacement in new code.
- **Two ways and nothing says which is current.** Look for intent before recency: a commit that migrates from one to the other, the way the core or owning module does it, the way the docs show. Say in the report which signal you used.

The [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook gives the order for replacing an old way, so it's frozen while it drains.

## Check

- If the next author copied this file, would the result be acceptable? If not, did you name the fault in the report?
- After a replacement, grep for the old pattern. Is every hit an instance named on the exemption list?
