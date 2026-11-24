---
name: standard-sets-are-closed-or-open
description: "Apply when code branches over a set of cases (an error variant, a state, a mode, an API's status field), you're adding or changing something the tool has many of (a command, block, backend, provider, check), or shared code is about to name one of them. Decide whether the set is closed or open. Handle every case of a closed set explicitly, so adding one fails the build. Make each member of an open set a plugin: one folder, one contract, one line in one registry."
disable-model-invocation: true
---

# Sets Are Closed or Open

Ask: when a member is added, should any consumer need to know? If every consumer has to decide how to handle it, the set is closed. If none should, it's open and its members are plugins. If you're unsure, treat it as closed.

## A closed set is exhaustive

A catch-all default hides the case nobody thought about.

- Handle every case explicitly, with no catch-all default, and turn on the check that fails when a case is added.
- A set defined outside the codebase, like an API's status field, can gain members without the build knowing. Parse it at the boundary into a closed type with an explicit unknown case, and handle that case like any other.
- If the language has no such type, use a closed interface and a lint. Without a static checker, write a test that fails when a case is added and not handled.

## An open set is plugins

A tool that has many of something is a small core plus those things. A tool with no open set has no plugins.

- A kind exists once three members each carry their own behaviour, or two if the third lands in the same stack or third parties add them. Until then, use an exhaustive switch or an interface with no registry.
- Give each plugin one folder holding its logic, settings, errors, tests, and docs. Plugins don't import each other, and logic two of them need moves into the core. Enforce both with a lint or a visibility rule.
- Give each kind one contract, written as a type, and one explicit registry built at startup. Derive help text, docs indexes, test coverage, and dispatch from it. Keep no second list by hand. If the framework the repo uses already keeps one (a CLI library's command tree, a provider table), that's the registry. Don't build another beside it.
- In the contract, name the error types a plugin may return and require whatever all plugins must do alike.
- Don't name a plugin in the core: no switch on its name, and no field or flag for it in shared code. Resolve a name that arrives as a string through the registry.
- Compile plugins in. Load one out of process only when a third party writes it, and treat that contract as a compatibility boundary.

The [migrate to plugins](../make-more9s/playbooks/migrate-to-plugins.md) playbook gives the steps for an existing tool.

## Check

- For a closed set, does adding a case fail the build until it's handled?
- For an open set, does adding a plugin touch only its new folder and one registry line?
