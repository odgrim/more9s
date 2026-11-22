---
name: standard-user-facing-change-ships-with-docs
description: "Apply when a change alters anything a user can observe: a flag, config attribute, output, behaviour, or an error they act on. The changelog entry and docs land in the same PR as the code."
disable-model-invocation: true
---

# A User-Facing Change Ships With Its Docs

If a user can observe a change, its documentation lands in the same PR.

## Rules

- Add a changelog entry through the repo's own mechanism, in the matching category: feature, fix, breaking change, experiment.
- Update every page that describes what changed.
- Where docs publish ahead of a release, gate new text on that release. Where they cannot be gated, mark the text with the version that ships it.
- Document experimental behaviour as an experiment: what it does, how to enable it, what must hold before it stabilises. It is not a breaking change.
- A renamed or moved page updates links, navigation, and `llms.txt` where one exists.
- Internal refactors, test-only changes, and private helpers need no entry.
- With no changelog, state the user-visible change in one sentence in the PR description.

## Check

- Is every hit from grepping the docs for the old name or behaviour a deprecation note or a changelog entry?
