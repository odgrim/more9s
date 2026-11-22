---
name: standard-plugin-architecture
description: "Apply when adding or changing something the tool has many of (a command, block, backend, provider, check), when shared code is about to name one of them, or when adding one touches files outside its own folder. Each is a plugin: one folder, one contract, one line in one registry."
disable-model-invocation: true
---

# Plugin Architecture

A tool that has many of something (commands, blocks, backends, providers) is a small core plus those things. Each kind has one contract, and each instance is a plugin. A tool with no open set has no plugins.

## Plugins

- The test: when a new member is added, should any consumer need to know it exists? If no consumer should, the set is open and its members are plugins. If every consumer must decide how to handle it (an error variant, a state, a mode), the set is closed and type-system-discipline governs it.
- When the test is unclear, treat the set as closed. It can become a kind later through a replacement stack.
- A kind exists once the tool has three members that each carry their own behaviour, or two when the third lands in the same stack or third parties add them. Until then, two members are a closed set: an exhaustive switch, or an interface with no registry. Write the kind's contract as a type.
- The contract names the error types a plugin may return. Consumers handle those, never a plugin's own.
- A plugin's name that arrives as a string from a flag or config is resolved through the registry, not parsed into an enum and switched on.
- A closed set inside one plugin is fine.
- Each plugin is one folder holding its logic, settings, errors, tests, and docs. Where the tool spans processes, the folder has one entry file per process.
- Plugins do not import each other. Logic two plugins need moves into the core.
- Plugins are compiled in. Load one out of process only when a third party writes it, and treat that contract as a compatibility boundary.

## Core

- Each kind has one explicit registry, built at startup. Derive help text, docs indexes, test coverage, and dispatch from it. Keep no second list by hand.
- The core does not name a plugin: no `switch` on a plugin's name, and no field, flag, or prop for one plugin in shared code.
- If plugins of a kind must behave alike, the contract requires it, so authors do not keep them in sync by hand.
- Visibility rules or a lint ban plugin-to-plugin imports and core-to-plugin imports outside the registry.

## Migrating

The [migrate to plugins](../make-more9s/playbooks/migrate-to-plugins.md) playbook gives the steps.

## Check

- Does adding a plugin touch only its new folder and one registry line?
- Does grepping the core for a plugin's name find only the registry?
