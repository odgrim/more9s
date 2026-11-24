---
name: standard-fix-the-code-not-the-check
description: "Apply when you're writing a lint or CI check, a check fails and loosening it would make it pass, or you're adding a suppression, skip, or exemption. Fix the code, not the check, and keep every exemption where it can be found."
disable-model-invocation: true
---

# Fix the Code, Not the Check

Someone who didn't write a check will read its failure, and someone has to be able to find every exemption.

- Fix the code. A suppression, a skip, a new exemption, a raised threshold, or a narrowed scope loosens the check. If the check itself is wrong, fix it in its own change.
- Any loosening you add is the reviewer's decision. List it in the report's decisions with the fix you didn't make and why.
- Make a check's message name the replacement and say what to change.
- Have each CI step call a script that also runs locally.

There are two ways to exempt code, for two different situations. Don't use one where the other applies.

## One place: an inline suppression

Use it where the code is right and the check is wrong for that one place, or where another standard calls for one, as `errors-are-typed-values` does for a discarded result.

- Name the specific check and give the reason on the same line. The more9s hook flags a suppression that does neither, for the markers it knows.
- If the check wants its marker last on the line, put the reason before the marker, or in a comment on the line above.
- Don't use inline suppressions to get existing code past a new lint. That takes a list.

## Existing code that fails a new lint: an exemption list

- Land the lint with a list that exempts each instance by name. The list only shrinks, and these exemptions don't live inline.
- If the lint has no list and only reads inline markers, giving it one is a change to the check, in its own change. Until then use its markers as inline suppressions, and name the missing list in the report's gaps.

The [replace a pattern](../make-more9s/playbooks/replace-a-pattern.md) playbook covers keeping an exemption list and freezing a workaround.

## When the human asks for a suppression

The request outranks this standard, so add it. The form still holds.

- Give each one its check's name and a reason on its line, such as what the human asked for and the fix that's deferred. A requested suppression with no reason looks the same as a careless one to the next reader.
- List it in the report's decisions with the fix you didn't make. If the fix is about as small as the suppression, say so there, so the human can choose it.
- The request covers the places it named. A later failure of the same check needs its own decision.
- A request can't waive what `test-contracts-over-implementation` says about a test that fails because behaviour broke. Say so and stop there.

## Check

- Did you leave every existing check as strict as you found it, or name each loosening in the report's decisions?
- Does every inline suppression you added name its check and carry its reason, whoever asked for it?
