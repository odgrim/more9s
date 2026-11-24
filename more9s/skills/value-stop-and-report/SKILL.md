---
name: value-stop-and-report
description: "Apply when a third attempt at the same check has failed with nothing new learned, the work has passed twice the size you stated at the start, or you're repeating a step you already ran. Stop, go back to the last state whose checks passed, and report what you know."
disable-model-invocation: true
---

# Stop and Report

A fourth attempt is rarely better informed than the third. It costs context and tempts you to weaken the check.

- Count attempts per check. An attempt is a change you expected to make the check pass. It failed if the check fails the same way as before, or in a way your change caused.
- If the check gets further and stops on a different, existing fault (the next compile error, the next failing case), that's progress, not a failed attempt.
- Write each failed attempt into the draft report when it fails, as `write-state-down` says, so a compaction doesn't reset the count.
- Past twice the stated size, stop before the next unit. Finish or revert the unit in hand, and report what's done, what's left, and the new size.
- Don't rerun a step on the same input: the same command, the same read, an edit made and undone. It gives the same result. Count it as a failed attempt at the check it was meant to pass.
- When you stop, return the tree to the last state whose checks passed. Keep a failed attempt on its own branch or in the report, not in the diff.
- Report what you tried, the evidence from each attempt, what that rules out, and the next observation that would decide it.
- Stopping isn't asking. Deliver everything that works and put the failed part in the report's gaps.
- Never get past the limit by loosening the check, special-casing the test input, or narrowing the claim without saying so.
- The user can lift the limit by saying so, as in an unattended run. Then change the approach on each further attempt and list every one in the report. Past the size limit, write the new size into the draft report and continue from it.

## Check

- For each check that failed more than twice, does the report list each attempt and its evidence? Is the tree at a state whose checks pass?
