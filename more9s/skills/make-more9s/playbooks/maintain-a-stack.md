### Maintain a stack

Run this when something moves under a stack of PRs the session opened: a review changes a lower PR, the default branch conflicts with it, a PR merges, or a PR is rejected.

A stack is a chain. Each PR's base is the branch of the PR below it, and the bottom PR's base is the default branch.

#### Which branches you may rewrite

- A branch is yours if the session created it and nobody else has pushed to it. Anything else is shared, and force-pushing it is an ask-first action.
- Update your own branch without rewriting it where you can: add commits, or merge its parent into it. A reviewer's comments stay attached to the commits they were made on.
- Rebase only when the repo's documented flow needs a linear history. Then push with `--force-with-lease`, pinned to the commit you last pushed. If the lease fails, someone else has pushed, so the branch is shared now. Stop and ask.
- Never push with a plain `--force`.

#### When a lower PR changes

1. Make the change on that PR's branch in new commits, as the [after the PR opens](./after-the-pr-opens.md) playbook says.
2. Bring every PR above it up to date, bottom to top: merge the parent branch into each child, or rebase each child if the repo needs that.
3. Decide what each PR's evidence is still worth. Compare the PR's own diff against its parent before and after, with `git range-diff` or `git patch-id`. If it's unchanged, the earlier evidence stands, and you note the new head. If it changed, rerun that PR's checks and update the report.
4. Update the stack map in the first PR's description.

#### When the default branch conflicts

1. Resolve it in the lowest PR that conflicts: merge the default branch in, or rebase if the repo needs that.
2. A conflict resolution is a change you wrote. Rerun that PR's checks.
3. Bring the PRs above it up to date as above.
4. Don't pull in the default branch only because it moved. Do it for a conflict, a failing check it fixes, or a change to the same code.

#### When the bottom PR merges

1. Read the PR's state back from the host. A merge that was queued, or an auto-merge that was requested, hasn't happened yet.
2. Check that the next PR's base is now the default branch. Hosts often retarget it when the merged branch is deleted. If it still points at the merged branch, retarget it.
3. Merge the default branch into the next PR. After a squash merge the parent's commits come back as changes already present, and the PR's diff should show only its own work. If it shows the parent's work as well, rebase it onto the default branch from the parent's old tip.
4. Apply step 3 of "when a lower PR changes" to decide whether its evidence still stands.

#### When a PR is rejected

- The PRs below it aren't affected. Leave them alone.
- For each PR above it, ask whether it needs the rejected change.
  - If it doesn't, move it onto the PR below the rejected one, rerun its checks, and update the map.
  - If it does, it waits. Say so first in its description and in the map, and name the decision it waits on. Don't rework it into something the reviewer didn't ask for.
- Closing the rejected PR is the reviewer's call.
- Put the rejection and what it stranded in the report's decisions.

#### Landing

Merging is an ask-first action. A confirmation given ahead ("merge the stack when it's green") covers the PRs it names, each once.

1. Land from the bottom, one PR at a time. Before each merge, confirm its checks passed on its current head, and that nothing was pushed to it since the reviewer approved.
2. After each merge, follow "when the bottom PR merges" before you touch the next one.
3. Change nothing else in the stack while a merge is in progress.
4. Stop at the first PR that is unapproved, rejected, or failing. The PRs above it wait, and the report says which and why.

#### Order of work

When several things need attention at once: conflicts, then review comments, then failing checks. A failing check on a branch that's out of date with its parent may not be real.
