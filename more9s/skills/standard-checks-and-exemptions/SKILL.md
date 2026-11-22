---
name: standard-checks-and-exemptions
description: "Apply when writing or changing a lint or CI check, adding a suppression or skip, keeping an exemption list, or freezing a workaround or old pattern so it cannot spread. The check's message names the fix, and every exemption lives where it can be found."
disable-model-invocation: true
---

# Checks and Exemptions

A failing check is read by someone who did not write it, and an exemption is a debt someone has to be able to find.

## Messages

- The check's message names the replacement and says what to change.
- For a frozen workaround with no replacement yet, it says the pattern is frozen, names the exemption list, and links the tracking issue once one exists.

## Suppressions

- A suppression names the specific check and gives its reason on the same line. A hook rejects one that does neither.
- A suppression, skipped or disabled test, or exemption entry you add so a check passes is a decision for the reviewer. List each one at the top of the PR description with the fix you did not make and why. Never add one silently.
- A lint that keeps an exemption list takes its exemptions from the list, not from inline suppressions.

## Exemption lists

- A new lint that existing code fails lands with an exemption list. Each existing instance is exempted by name.
- The list shrinks. CI fails a change that adds an entry, unless it renames or moves an existing one.
- An entry the reviewer approves passes through an override the repo defines, such as a label or a sign-off. Only the reviewer applies it. Where the repo defines none, the failing ratchet is the request for a ruling, and the top of the PR description says so.
- A list that freezes a workaround takes no new entries, approved or not. A task that needs the workaround again fixes the design, as patterns-spread says.
- A change that edits the exempted construct itself migrates it and removes it from the list, in an earlier PR of the same stack when the migration is larger than the change. An edit elsewhere in the same file leaves the entry alone. Untouched instances wait for the cleanup PRs. The replace-a-pattern playbook says how many of those a stack owes.
- An old public name stays on the list until a human approves its removal. The list for an internal pattern reaches empty.

## Freezing a workaround

- A lint fails on new instances, with the existing ones exempted by name.
- The exemption list is the record of the debt. A TODO at each site names the lint rule that freezes it, written `TODO(lint:<rule>)`, so a reader finds the list from the site.
- Creating an issue takes effect outside the PR. When none exists, put the issue text in the PR description for the reviewer to file. Add the issue link to the lint's message once it exists.

## Check

- Does the message alone tell the author what to write?
- Is every exemption in the list, with none inline?
