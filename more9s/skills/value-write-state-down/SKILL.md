---
name: value-write-state-down
description: "Apply when the work may not fit one session, you're making a decision a later session will need, or a compaction has happened. Keep the state in commits and a draft of the report, not in context."
disable-model-invocation: true
---

# Write State Down

A compaction or a new session keeps the files and loses the reasoning. Anything that was only in context is gone.

- Size the work to the window, from the size you stated at the start. If it won't fit, split it into units that each end in a commit and a written state the next session can start from.
- Start the report as a draft with the first unit. Keep it at `.more9s/report.md` in the checkout, so a later session finds it without being told. Add `.more9s/` to the file `git rev-parse --git-path info/exclude` names, so no commit includes it. Once there is a draft PR, keep it in the PR body.
- Put in the draft the goal, the stated size, each decision with its reason, and each failed attempt `stop-and-report` counts. Write each one in when it happens. Don't count on recalling it later.
- If a decision belongs to one commit, put it in that commit's message too.
- After a compaction, reread the draft report and any leaf you're still applying. The harness restores `make-more9s` and drops most of what you read.

## Check

- Could a new session carry on from the commits and the draft report alone?
