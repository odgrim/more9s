---
name: standard-plugin-architecture
description: "Apply when you're adding or changing something the tool has many of (a command, block, backend, provider, check), or shared code is about to name one of them. Make each one a plugin: one folder, one contract, one line in one registry."
disable-model-invocation: true
---

# Plugin Architecture

A tool that has many of something is a small core plus those things. A tool with no open set has no plugins.

- A set is open if no consumer should need to know a new member exists. Its members are plugins. If you're unsure, treat the set as closed.
- A kind exists once three members each carry their own behaviour, or two if the third lands in the same stack or third parties add them. Until then, use an exhaustive switch or an interface with no registry.
- Give each plugin one folder holding its logic, settings, errors, tests, and docs. Plugins don't import each other, and logic two of them need moves into the core. Enforce both with a lint or a visibility rule.
- Give each kind one contract, written as a type, and one explicit registry built at startup. Derive help text, docs indexes, test coverage, and dispatch from it. Keep no second list by hand.
- In the contract, name the error types a plugin may return and require whatever all plugins must do alike.
- Don't name a plugin in the core: no switch on its name, and no field or flag for it in shared code. Resolve a name that arrives as a string through the registry.
- Compile plugins in. Load one out of process only when a third party writes it, and treat that contract as a compatibility boundary.

The [migrate to plugins](../make-more9s/playbooks/migrate-to-plugins.md) playbook gives the steps for an existing tool.

## Check

- Does adding a plugin touch only its new folder and one registry line?
