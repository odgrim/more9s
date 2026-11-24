---
name: standard-fix-the-code-not-the-check
description: "Apply when you're writing a lint or CI check, a check fails and loosening it would make it pass, or you're adding a suppression, skip, or exemption. Fix the code, not the check, and keep every exemption where it can be found."
disable-model-invocation: true
---

# Fix the Code, Not the Check

Someone who didn't write a check will read its failure, and someone has to be able to find every exemption.

- Fix the code. A suppression, a skip, a new exemption, a raised threshold, or a narrowed scope loosens the check. If the check itself is wrong, fix it in its own change.
- Make a check's message name the replacement and say what to change.
- On a suppression, name the specific check and give the reason on the same line. The more9s hook flags one that does neither.
- Any loosening you add is the reviewer's decision. List it in the report's decisions with the fix you didn't make and why.
- If existing code fails a new lint, land the lint with a list that exempts each instance by name. The list only shrinks, and no exemption lives inline.
- Have each CI step call a script that also runs locally.

The [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook covers keeping an exemption list and freezing a workaround.

## Check

- Did you leave every existing check as strict as you found it, or name each loosening in the report's decisions?
