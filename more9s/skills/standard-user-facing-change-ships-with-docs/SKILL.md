---
name: standard-user-facing-change-ships-with-docs
description: "Applies when a change alters anything a user can observe: a flag, config attribute, output, behaviour, or an error they act on. Lands the changelog entry and the docs in the same PR as the code."
disable-model-invocation: true
---

# A User-Facing Change Ships With Its Docs

A change the docs don't describe is one the user finds by accident.

- Add a changelog entry through the repo's own mechanism, in the matching category: feature, fix, breaking change, experiment. If there's no changelog, state the user-visible change in one sentence in the report.
- Update every page that describes what changed. If a page moves, update the links, navigation, and `llms.txt`.
- If docs publish ahead of a release, gate new text on that release or mark it with the version that ships it.
- Document experimental behaviour as an experiment: what it does, how to enable it, and what has to hold before it stabilises.
- Skip the entry for internal refactors, test-only changes, and private helpers.

## Check

- Grep the docs for the old name or behaviour. Is every hit a deprecation note or a changelog entry?
