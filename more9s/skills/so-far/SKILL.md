---
name: so-far
description: "Says how far along the current piece of work is and how much is left, as an ASCII loading bar with a short summary. Use for /so-far."
argument-hint: "[the work to measure]"
disable-model-invocation: true
---

# So Far

Say how far along the work is and how much is left. With no argument, the work is the largest task the human set in this session that isn't finished: the rewrite, the migration, the stack.

This turn only reads. Check the current state of what you count: the files, the tests, the PRs, the draft report. Change no code and start nothing.

## The number

A percentage you felt is a guess. Count something.

1. Pick the unit the work is made of: files to port, call sites to move, tests to pass, PRs to land, steps in the plan. Use the plan's own unit if it has one.
2. Count the units that are done and the total, now, with a command where one can count them. Don't reuse a count from earlier in the session.
3. A unit is done when its check passes: it builds, its tests pass, it's merged. Written but unverified is not done. Count it as in progress.
4. If the units differ a lot in size, weight them, and say how in a line.
5. If the total isn't known yet, say so. Give the bar for the part you can count and name what's outside it.

## The reply

Lead with the bar, 20 cells wide, in a code block:

```
[████████████░░░░░░░░] 60%  12 of 20 modules
```

- `█` is done and `░` is left. Round the fill down, so only finished work shows 100%.
- Put the percentage and the count it came from after the bar.
- When the work has phases, add one shorter bar per phase under the main one, with each label aligned.

Then, in under a hundred words, written the way [wat](../wat/SKILL.md) asks:

- **Done.** What works now that didn't before.
- **In progress.** What's written and not yet verified.
- **Left.** What remains, the largest or riskiest piece first.
- **Blocked.** Anything that waits on the human. Leave the line out if nothing does.

- Don't give a time estimate unless the human asks. If they do, base it on the rate so far and say so.
- The remaining units aren't always like the finished ones. If the hard part is still ahead, say that under the bar: 80% of the files can be half of the work.
- If nothing can be counted, say that and give the summary without a bar. Never draw a bar from a guess.

## Check

- Does the percentage come from a count made this turn, and is the count beside the bar?
- Is everything counted as done something whose check you saw pass?
