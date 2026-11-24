---
name: standard-public-interface-changes
description: "Apply when a change adds to, renames, removes, or alters a surface that a program or author outside the codebase depends on, or you're judging whether such a change is compatible: a default, an exit code, an output field, an ordering, a fix to shipped behaviour. Add beside the old, keep the old working, and put a breaking or significant change in front of the reviewer as a written proposal."
disable-model-invocation: true
---

# Public Interface Changes

A public interface is any surface used from outside the codebase: a CLI, an HTTP API, an IPC channel, a file format, a document schema. You can't find or fix its callers from here.

- Add a new name beside the old one, and keep the old one working.
- Make a deprecated name warn on stderr with its replacement, and mark it in the docs with the version that deprecated it.
- Never ship a breaking change without an approved proposal.
- A change is significant if it's breaking, or it adds a command, a file format, or a concept users have to learn. Write a proposal for it: motivation, proposal, drawbacks, alternatives, migration. Make the proposal the first PR of the stack and stack the code on it.
- Propose a removal the same way and land it in its own PR, last in the stack, so the rest merges without it.
- A surface documented as experimental can change without a proposal. Record the change in the changelog as an experiment.

## What counts as breaking

A change is breaking if an existing caller can observe it without opting in. Callers depend on what a surface does, not only on what its docs promise.

- Removing or renaming a field, flag, or command is breaking. So is changing a default, an exit code, the meaning of a value, the order of output, or the stream it goes to.
- It's breaking only if the behaviour it replaces was documented, or contradicted nothing documented. A fix that restores documented behaviour ships as a fix, with a changelog entry that says what a caller of the old behaviour will now see.
- If wrong behaviour has shipped and callers may depend on it (the repo's own scripts, its examples, or an issue shows one), name that in the report's decisions. The reviewer rules on it.
- Adding an optional input or an output field is compatible. Adding a required input is breaking.
- Adding a value to a set callers switch on is breaking, unless the documented contract already has an unknown case.

## Check

- Would an existing script still work after this change?
- Can you name an existing caller that would see a difference without changing anything? If so, the change is breaking.
