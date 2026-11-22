---
name: standard-change-composition
description: "Apply when ordering edits, splitting work into commits and PRs, adding a CI step, running the verify sequence, or writing the report for a change. Says how work is sequenced, what lands in one PR, which checks run, and what the report lists."
disable-model-invocation: true
---

# Change Composition

A PR holds one kind of change, and its report shows what was checked. The reviewer then knows what to read, what to rerun, and what was left out.

## Working

- Work in small units that each end in a state you can check: known-good state, one change, run the check, proceed.
- Say what a unit's check will show before running it. The unit is done when the check shows that: a pass, or for a test written ahead of its fix, the expected failure with the expected message. Do not start the next unit on a result you did not predict.
- A commit that is red on purpose says so in its message.
- Run the per-unit check even when a script makes the edits.
- Each unit is one commit. Order commits so the sequence proves the work: the failing test before the fix, the deletion before the reshape, the baseline before the change it measures.
- What every later unit needs (a shared type, a test harness, a CI step) goes first, after the deletions.

## One PR

- The kinds are: a behaviour change, a refactor, a mechanical change, a check, a build change, a docs-only change, and a proposal. A PR holds one.
- A behaviour change carries its tests, docs, and changelog entry. They are part of the change, not a second kind.
- A check is a new lint or CI check, a freeze included. One that guards only what the same PR introduces is part of that change, like its tests. One that existing code fails lands in its own PR with its exemption list.
- A build change alters CI config, the toolchain, or a dependency's version. A new dependency a behaviour change needs lands in its own commit of that PR, as secrets-and-untrusted-input says.
- Preparatory commits ride with a behaviour change when they stay inside the module the task owns: deleting dead code the change replaces, an in-module reshape, migrating an exempted construct the change edits. They land ahead of the behaviour commit. Anything wider leads the stack as its own PR.
- A mechanical change lands in its own PR with the exact command in the title or description.
- Freezing a workaround lands in its own PR.
- Split no further than these rules require. Several small units of one kind are commits of one PR, not a stack.
- A stack's first PR description holds a map: each PR in order, its kind, and what the reviewer does with it (rule on a decision, rerun a command, read the diff). Decisions for the whole stack are listed there once.

## CI

- A CI step calls a script that also runs locally. Lint and test that script.

## Verify

- Run build, type-check, lint, and test in the order the repo documents, through its pinned toolchain. All must pass, or fail the same way on the base branch. Show a base failure with the output of the same command run on the base branch, and leave it.
- A check that passes only on a rerun is flaky. Report it with both outputs. Do not rerun until green.
- If the sequence is not documented, take it from the CI config and report that it was undocumented.

## Report

The report has three parts, in this order. A part with nothing in it is left out.

1. **Decisions.** What the reviewer should rule on, as the-pr-is-the-guard requires: what you chose, what you rejected, and what reverting costs. This part also holds the reading of the request when it had more than one, and every suppression, exemption, skipped or deleted test, and new dependency.
2. **Gaps.** What the request asked for that you did not do, and what you did that it did not ask for. Any check that failed, came back inconclusive, or did not run, and why. The better way when you used an existing one, and any standard the repo could not yet meet.
3. **Evidence.** Each check with its command and result, and a screenshot or recording for anything visual. Put this part last, in a collapsed block where the host renders one.

- In the evidence, quote the lines of output that carry the result and mark any cut. Redact them as secrets-and-untrusted-input requires.
- Where CI runs the check, the evidence is the link to that run. Output only your session produced is labelled local, with the one command that reruns it. A file on your machine is not something the reviewer can open.
- A check that passed is one line of evidence. It does not appear in the first two parts.

## Check

- Does each check in the report show its command and its result?
- Can the reviewer rule on every decision after reading only the first part?
