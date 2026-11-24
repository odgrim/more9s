---
name: value-write-state-down
description: "Applies when the work may not fit one session, a later session will need a decision being made now, or a compaction has happened. Keeps the state in commits and a draft of the report, not in context."
disable-model-invocation: true
---

# Write State Down

A compaction or a new session keeps the files and loses the reasoning. Anything that was only in context is gone.

- Size the work to the window, from the size you stated at the start. If it won't fit, split it into units that each end in a commit and a written state the next session can start from.
- Start the report as a draft with the first unit. Keep it at `.more9s/<branch>.md` in the checkout, named for the branch the work is on, so a later session finds it without being told and a branch switch doesn't pick up another task's state. Add `.more9s/` to the file `git rev-parse --git-path info/exclude` names, so no commit includes it.
- Before you continue from a draft you didn't start, check that its goal is this task's. If it isn't, leave it alone and say so in the reply.
- Once there is a draft PR, keep the report in the PR body and delete the file. With no PR, delete it once the final reply has delivered the report.
- Put in the draft the goal, the stated size, each decision with its reason, and each failed attempt `stop-and-report` counts. Write each one in when it happens. Don't count on recalling it later.
- If a decision belongs to one commit, put it in that commit's message too.
- After a compaction, reread the draft report and any value or standard you're still applying. The harness restores `make-more9s` and drops most of what you read.

## Check

- Could a new session carry on from the commits and the draft report alone?
