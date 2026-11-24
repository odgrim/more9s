### Unattended run

Run this when the human asks for the work to carry on without them ("run until done", "don't stop", "keep going overnight"), or gives a target to reach: a list of failing tests, a number.

1. Before the first change, write the finish line into the draft report as a command and the result that means done. If the request doesn't give one, choose it, say so in the reply, and start.
2. The go-ahead lifts the attempt limit in `stop-and-report` and nothing else. No ask-first action is confirmed by it. When one comes up, carry on with everything that doesn't depend on it and list it in the report with the command that performs it.
3. Make one change at a time. Run the finish-line command and the repo's checks. Keep the change if it moved toward the finish line and every other check still passes. If not, revert all of it. A change that "might help" isn't kept.
4. Commit each kept change on its own, as `commits-prove-the-work` says.
5. When an attempt ends, add a row to the draft report, kept or reverted: what changed, the result before and after, and the verdict. Read the rows before the next attempt, so you don't repeat one.
6. If you find a problem off the path (a flaky test, an unrelated bug), name it in the report's gaps. Fix it only if it blocks the finish line, in its own commit.
7. Several reverted attempts in a row aren't a reason to stop. Change the kind of approach, not its details.
8. Stop when the command shows the finish line. Stop too when no approach is left that differs from the rows already written, and say that in the report. Never move the finish line, loosen its check, or narrow the claim to reach it.
9. After a compaction, reread the draft report and this playbook before the next attempt, as `write-state-down` says.

#### When the finish line is a number

- Measure as `explain-the-number` says: the baseline first, the same way as every later run, with enough runs to see the spread.
- Fix the measuring command before the first change and leave it alone. If it turns out to be wrong, correct it in its own commit and measure the baseline again.
- Keep a change only when it moves the number by more than the spread.
- A gain that breaks a check is reverted. A simplification that holds the number is kept.
- Before you report the final number, measure it again from a clean state.

The report gives the finish line, the attempts kept and reverted, the state the run ended in, and every ask-first action still waiting.
