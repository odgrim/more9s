---
name: value-script-the-repeatable
description: "Apply when the work is bulk or batch: the same edit in more than a couple of places, one operation over many files or items, a migration, generated fixtures, a multi-step CI job, a check you're about to run by hand a second time. It applies even when one command does it all. Write the script and make it the artifact."
disable-model-invocation: true
---

# Script the Repeatable

The reviewer reruns the script instead of reading every line it produced.

- Do one unit by hand, write the script, then rerun it on that unit to prove it.
- Make a second run change nothing.
- Write the smallest script that does the job, not a framework.
- Prefer a deterministic script to handing units to subagents. If each unit needs judgment and you do fan out, write the recipe, the per-unit check, and the limits in one file that every delegate reads and none edits.
- Skip the script for a couple of obvious edits. Commit it if the work will recur or has to be auditable.
- Record the exact command that made the change, copied and not retyped, in two places: the body of the commit it produced, and the report's evidence. For a committed script, give its path and arguments.
- A one-line `sed` or `perl` counts as a script. Record it the same way.
- If the first command failed and another did the work, record the one that worked.

## Check

- Can someone reproduce the change with one command?
- Is that command in the commit body and in the report's evidence?
