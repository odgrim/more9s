---
name: value-attack-the-premise
description: "Apply when two or more fixes that rest on the same assumption have failed the same check. Write the assumption down and test it directly before writing a third fix."
disable-model-invocation: true
---

# Attack the Premise

When two fixes built on one assumption fail the same check, the assumption is the likely fault. A third fix on the same assumption will fail the same way.

- Stop writing fixes. Write the premise in one sentence: what every failed fix took to be true.
- Find an observation that would come out differently if the premise were false, and make it.
- Look at which cases fail, not only how many. A premise that is true predicts the pattern of failures as well as their count.
- If the evidence contradicts the premise, revert the fixes it motivated and start from what the failures have in common.
- Report the premise, the test, and the result, including when the premise held.

## Check

- Is the premise written down, with the observation that tested it?
