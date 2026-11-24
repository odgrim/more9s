---
name: standard-vet-new-dependencies
description: "Applies when adding, upgrading, or installing a dependency. Looks the package up before adding it, pins it, and puts it in front of the reviewer as its own decision."
disable-model-invocation: true
---

# Vet New Dependencies

A package name you recall from memory can be wrong, abandoned, or squatted, and installing it runs its scripts.

- Try the standard library and the repo's existing dependencies first.
- Look the package up. Confirm it's the canonical one, with a registry page that points to the source repo you expect. A name you didn't look up is a guess.
- Check that its licence fits the repo's and that it's maintained: releases within the last year, and issues that get answers.
- Take a version that has been out at least a week, unless it fixes a vulnerability the repo is exposed to. A release from yesterday hasn't been looked at by anyone.
- For an upgrade, read the changelog between the two versions and list each breaking change in the report's decisions.
- Pin it through the repo's lockfile.
- Give it its own commit, and say in the report's decisions what it replaces and what you rejected.
- Installing a package, or a version of one, that the lockfile doesn't already hold is an ask-first action. A new version runs new scripts.

## Check

- Is each new dependency in the lockfile, in its own commit, and in the report's decisions?
