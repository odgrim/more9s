### Replace a pattern

Land the replacement as one stack of PRs, in this order. The stack is reviewed together and merged in order. A PR the reviewer rejects, or a removal waiting for approval, stays behind without blocking the PRs below it.

1. The change that introduces the new way.
2. The lint with its exemption list, as `checks-and-exemptions` describes.
3. The feature that needed it, if there is one.
4. The cleanup PRs.

If a script can convert every instance in one reviewable PR, that PR is the whole cleanup and the lint lands with an empty list.

Land a design fix for a frozen workaround the same way.

Give internal code no compatibility layer. Don't add an adapter, an alias, or a flag that selects the old path to keep old callers working. An old caller stays on the old way, on the exemption list, until it's migrated. A public surface is different, as `public-interface-changes` says.

#### How much cleanup the stack owes

- Every instance, if a script can convert them or one reviewable PR can hold them.
- Otherwise, the instances in the module the task owns and the ones the feature edits. The rest stay on the list. Give the count left and the command that lists them in the report's gaps.
- If the task is the replacement itself, the stack is done when the list is empty.

#### A rewrite that cannot stay green

If no order of steps keeps the checks passing (a core type changes under every caller), don't write temporary code to bridge the steps.

1. In the first PR's description, declare the target, the steps, and which checks you expect to fail after which step.
2. Each step still passes the checks for the code it touches.
3. Mark the stack to merge together or not at all. The full verify sequence passes at its top.
4. If a step fails a check the plan didn't name, stop the stack.

#### Keeping the exemption list

- CI fails a change that adds an entry, unless it renames or moves an existing one.
- An entry the reviewer approves goes through an override the repo defines, such as a label or a sign-off. Only the reviewer applies it. If the repo defines none, the failing ratchet is the request for a ruling, and the report's decisions say so.
- If a change edits the exempted construct itself, migrate it and remove it from the list. An edit elsewhere in the same file leaves the entry alone.
- An old public name stays on the list until a human approves its removal. The list for an internal pattern reaches empty.
- A lint that keeps a list takes its exemptions from the list, not from inline suppressions.

#### Freezing a workaround

- Make the lint fail on new instances. Its message says the pattern is frozen, names the exemption list, and links the tracking issue once there is one.
- The list takes no new entries, approved or not.
- Put a TODO at each site naming the lint rule that freezes it, so a reader can find the list from the site.
- Creating an issue is an ask-first action. If none exists, put the issue text in the report for the reviewer to file.
