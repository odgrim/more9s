---
name: standard-commits-prove-the-work
description: "Applies when ordering edits, running a sweep or migration, or deciding what each commit holds. Splits the work into small units that each end in a check, and orders the commits so the sequence proves the work."
disable-model-invocation: true
---

# Commits Prove the Work

A reviewer trusts a sequence they can replay. If a result surprises you, you don't understand the change yet.

- Work in units: start from a known-good state, make one change, run the check, move on. Run the per-unit check even when a script makes the edits.
- Say what the check will show before you run it. Don't start the next unit on a result you didn't predict.
- Make each unit one commit, ordered so the sequence proves the work: the failing test before the fix, the deletion before the reshape, the baseline before the change it measures.
- Put what every later unit needs (a shared type, a test harness, a CI step) first, after the deletions.
- If a commit is red on purpose, say so in its message.
- If no order of steps keeps a planned rewrite green, follow the [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook: declare the target and the red steps first, and write no temporary code to bridge them.

## Check

- Does each commit pass its check, or say in its message that it's red on purpose?
