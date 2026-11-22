---
name: value-patterns-spread
description: "Apply when you find a workaround, anti-pattern, or deprecated usage in the codebase, when about to copy an existing pattern, when replacing an old way with a new one, or when a requirement does not fit the existing design. Existing code is the example the next author copies, so a bad pattern left in place is an instruction."
disable-model-invocation: true
---

# Patterns Spread

Existing code is what the next author copies, human or agent. A bad pattern left in place gets repeated.

- Existing code is not proof of the right way. Before copying it, decide which of three cases it is.
- **A different style.** The repo's way works and you would have written it differently. Use the existing way and name the better one in the report. Introduce a new way when asked. An existing way that breaks a standard is handled the same, as make-more9s says under Existing repos.
- **A replaced way.** The repo already holds the replacement: a newer API, a lint message that names one, an exemption list, a deprecation note. New code uses the replacement. When two ways coexist and nothing says which is current, look for intent before recency: a commit that migrates from one to the other, the way the core or owning module uses, the way the docs show. Recency alone is weak evidence, because the newest code is the most likely to be a copy. Say in the report which signal you used.
- **A workaround.** Code that compensates for a fault somewhere else. Do not copy one and do not write a new one beside it. The exception is a fault outside the repo (a third-party library, a service, a platform) that cannot be fixed from here. That workaround lives inside the boundary owner, with a TODO that links the upstream issue, or the upstream source that shows the fault when no issue exists.
- When you find a workaround the task does not need, name it in the report. Freeze it when asked, or when the task would otherwise copy or extend it. checks-and-exemptions says how.
- A task that needs a frozen workaround again fixes the design. A series of workarounds covering one underlying problem is fixed the same way, not extended.
- When a requirement does not fit the existing design, the first special case is allowed when it is local to one function and named in the report. Do not add a second for the same design, or a flag that must stay in sync with another. Inside the module the task owns, reshape the design as if the requirement had always been there. When the reshape reaches beyond that module, it leads the stack as its own PR, as the-pr-is-the-guard describes.

The [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook gives the order for landing a design fix or a new way.

## Check

- If the next author copied this file, would the result be acceptable? If not, is the fault named in the report, and frozen where the task would otherwise copy or extend it?
- After a replacement, is every hit from grepping for the old pattern an instance named on the exemption list?
