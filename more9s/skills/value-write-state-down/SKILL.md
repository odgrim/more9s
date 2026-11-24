---
name: value-write-state-down
description: "Apply when the work may not fit one session, you're making a decision a later session will need, or a compaction has happened. Keep the state in commits and a draft of the report, not in context."
disable-model-invocation: true
---

# Write State Down

A compaction or a new session keeps the files and loses the reasoning. Anything that was only in context is gone.

- Size the work to the window, from the size you stated at the start. If it won't fit, split it into units that each end in a commit and a written state the next session can start from.
- Start the report as a draft with the first unit. Keep it in a file in the checkout that no commit includes, then in the body of the draft PR once there is one. Name its path in the reply when you create it.
- Put in the draft the goal, the stated size, each decision with its reason, and each failed attempt `stop-and-report` counts. Write each one in when it happens. Don't count on recalling it later.
- If a decision belongs to one commit, put it in that commit's message too.
- After a compaction, reread `make-more9s`, the draft report, and any leaf you're still applying. The summary doesn't carry them.

## Check

- Could a new session carry on from the commits and the draft report alone?
