---
name: value-stop-and-report
description: "Apply when a third attempt at the same check has failed, when the work has passed twice the size stated at the start, or when the session is repeating a step it already ran. Stop, return to the last state whose checks passed, and report what is known."
disable-model-invocation: true
---

# Stop and Report

An attempt past the third is rarely better informed than the third. It costs context, and it pulls toward weakening the check.

- Count attempts per check. attack-the-premise applies at the second failure on one premise. This leaf applies at the third failure of one check, whatever the premises.
- Compare the work to the size stated at the start, as guard-the-context-window requires. Past twice that size, stop and plan again before continuing.
- Stop writing fixes. Return the tree to the last state whose checks passed. Keep a failed attempt on its own branch or in the report, not in the diff.
- Report what was tried, the evidence each attempt produced, what that rules out, and the next observation that would decide it.
- Stopping is not asking. Deliver everything that works, with the failed part in the report's gaps, as the-pr-is-the-guard describes.
- Never pass the limit by loosening the check, special-casing the test input, or narrowing the claim without saying so. encode-rules-in-tooling and fix-root-causes forbid each.
- The user lifts the limit by saying so, as in an unattended run. Then each further attempt changes the approach, and the report lists every one.

## Check

- For each check that failed more than twice, does the report list each attempt and its evidence?
- Is the tree at a state whose checks pass, or does the report name the ones that fail?
