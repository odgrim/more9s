---
name: standard-closed-sets-are-exhaustive
description: "Apply when code branches over a set of cases: an error variant, a state, a mode, an API's status field. Handle every case of a closed set explicitly, so adding one fails the build."
disable-model-invocation: true
---

# Closed Sets Are Exhaustive

A catch-all default hides the case nobody thought about.

- Ask: when a member is added, should any consumer need to know? If every consumer has to decide how to handle it, the set is closed. If none should, it's open and its members are plugins. If you're unsure, treat it as closed.
- Handle every case of a closed set explicitly, with no catch-all default, and turn on the check that fails when a case is added.
- A set defined outside the codebase, like an API's status field, can gain members without the build knowing. Parse it at the boundary into a closed type with an explicit unknown case, and handle that case like any other.
- If the language has no such type, use a closed interface and a lint. Without a static checker, write a test that fails when a case is added and not handled.

## Check

- Does adding a case fail the build until it's handled?
