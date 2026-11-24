---
name: standard-one-kind-per-pr
description: "Apply when you're splitting work into PRs or deciding whether something rides with a change. Keep each PR to one kind of change, at a size a reviewer can read in one sitting."
disable-model-invocation: true
---

# One Kind Per PR

Review only guards what the reviewer can read. Mixed kinds bury the behaviour change in noise.

- The kinds: a behaviour change, a refactor, a mechanical change, a check, a build change, a docs-only change, a proposal.
- A behaviour change carries its tests, docs, changelog entry, and any dependency it needs. They're part of it, not a second kind.
- Let preparation ride along while it stays inside the module the task owns: deleting dead code the change replaces, an in-module reshape. Anything wider leads the stack as its own PR.
- Don't split further than this. Several small units of one kind are commits in one PR, not a stack.
- Past the repo's size limit, or about 400 changed lines if it has none, split along a seam that keeps each PR passing, or open the description with a reading order. Generated files, lockfiles, and scripted output don't count.

The [open a PR](../make-more9s/playbooks/open-a-pr.md) playbook gives the steps.

## Check

- Can you name the PR's one kind, and is every hunk part of it?
