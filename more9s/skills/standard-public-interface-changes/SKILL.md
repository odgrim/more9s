---
name: standard-public-interface-changes
description: "Apply when a change adds to, renames, removes, or alters a surface a program or author outside the codebase depends on: a CLI command, flag, environment variable, config key, output field, HTTP API, IPC channel, file format, or document schema. Add beside the old, keep the old working, and put a removal or a significant change in front of the reviewer as a written proposal."
disable-model-invocation: true
---

# Public Interface Changes

A public interface is any surface a program or author outside the codebase depends on: a CLI, an IPC channel, an HTTP API, a file format, a document schema. Its callers cannot be found or fixed from here.

## Compatible changes

- A change is breaking when an existing caller can observe it without opting in, and the behaviour it replaces was documented or contradicted nothing documented. That covers removing or renaming a field, flag, or command, and also changing a default, an exit code, the meaning of a value, the order of output, or which stream output goes to.
- A fix that restores documented behaviour is not breaking. It ships as a fix, and its changelog entry says what a caller of the old behaviour will now see.
- When the wrong behaviour has shipped and callers may depend on it (the repo's own scripts, its examples, or an issue shows one that does), name that at the top of the PR description. The reviewer rules on whether it needs a proposal.
- Adding an optional input or an output field is compatible. Adding a required input is breaking. Adding a value to a set callers switch on is breaking unless the documented contract already has an unknown case.
- Never ship a breaking change without an approved proposal.
- A new name is added beside the old one, and the old one keeps working.
- A deprecated name warns on stderr with its replacement, is marked deprecated in the docs with the version that deprecated it, and stays on the exemption list.
- A surface documented as experimental may change without a proposal. The changelog records it as an experiment.

## Proposals

- A change is significant when it is breaking, or when it adds a command, a file format, or a concept users must learn.
- A significant change needs a written proposal: motivation, proposal, drawbacks, alternatives, migration. The proposal is the first PR of the stack, and the code stacks on it. The reviewer decides there, as the-pr-is-the-guard describes.
- A removal is proposed the same way and lands in its own PR, last in the stack, so the rest merges without it.

## Check

- Would an existing script still work after this change?
