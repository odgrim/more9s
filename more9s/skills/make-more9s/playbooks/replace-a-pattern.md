### Replace a pattern

Land the replacement as one stack of PRs, in this order. The stack is reviewed together and merged in order. A PR the reviewer rejects, or a removal waiting for approval, stays behind without blocking the PRs below it.

1. The change that introduces the new way.
2. The lint with its exemption list. Its message names the new way. The old way may exist only on that list, as checks-and-exemptions describes.
3. The feature that needed it, when there is one.
4. The cleanup PRs.

When a script can convert every instance in one reviewable PR, that PR is the whole cleanup and the lint lands with an empty list.

A design fix for a frozen workaround lands the same way.

Internal code gets no compatibility layer. Do not add an adapter, an alias, or a flag that selects the old path so that old callers keep working. An old caller stays on the old way, on the exemption list, until it is migrated. A public surface is different, as public-interface-changes says.

#### How much cleanup the stack owes

- Every instance, when a script can convert them or one reviewable PR can hold them.
- Otherwise the instances in the module the task owns and those the feature edits. The rest stay on the list. The report's gaps give the count left and the command that lists them.
- A stack whose task is the replacement itself is done when the list is empty.

#### A rewrite that cannot stay green

When no order of steps keeps the checks passing (a core type changes under every caller), do not write temporary code to bridge the steps.

1. The first PR's description declares the target, the steps, and which checks are expected to fail after which step.
2. Each step still passes the checks for the code it touches.
3. The stack is marked to merge together or not at all. The full verify sequence passes at its top.
4. A step that fails a check the plan did not name stops the stack.
