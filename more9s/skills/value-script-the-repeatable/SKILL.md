---
name: value-script-the-repeatable
description: "Apply when work is mechanical or repeated: a bulk edit, a migration, generated fixtures, a multi-step CI job, or a check you are about to run by hand a second time. Write the script that does it and make the script the artifact."
disable-model-invocation: true
---

# Script the Repeatable

Mechanical or repeated work gets a script. The reviewer reruns the script and does not read every line it produced.

- Do one unit by hand, write the script, then rerun it on that unit to prove it.
- A second run changes nothing.
- Write the smallest script that does the job, not a framework.
- A deterministic script beats handing the units to subagents. When each unit needs judgment and you do fan out, write the recipe, the per-unit check, and the limits in one file every delegate reads and none edits.
- Skip the script for a couple of obvious edits. Commit it when the work will recur or must be auditable.

change-composition says how a mechanical change lands. test-contracts-over-implementation says how fixtures are generated.

## Check

- Can someone reproduce the change by running one command?
