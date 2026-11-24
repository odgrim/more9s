---
name: standard-vet-new-dependencies
description: "Apply when you're adding, upgrading, or installing a dependency. Look the package up before you add it, pin it, and put it in front of the reviewer as its own decision."
disable-model-invocation: true
---

# Vet New Dependencies

A package name you recall from memory can be wrong, abandoned, or squatted, and installing it runs its scripts.

- Try the standard library and the repo's existing dependencies first.
- Look the package up. Confirm it's the canonical one, with a registry page that points to the source repo you expect. A name you didn't look up is a guess.
- Pin it through the repo's lockfile.
- Give it its own commit, and say in the report's decisions what it replaces and what you rejected.
- Installing one the repo doesn't already declare is an ask-first action.

## Check

- Is each new dependency in the lockfile, in its own commit, and in the report's decisions?
