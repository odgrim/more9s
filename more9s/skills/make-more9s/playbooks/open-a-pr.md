### Open a PR

Run this at the end of any change that lands through a PR.

1. Before the first push in a repo, read what its CI runs for a PR. `ask-first-actions-wait-for-the-user` says when that push waits.
2. Run build, type-check, lint, and test in the order the repo documents, through its pinned toolchain. If the order isn't documented, take it from the CI config and say so in the report.
3. Everything has to pass, or fail the same way on the base branch. Show a base failure with the output of the same command run on the base branch, and leave it alone. A check that passes only on a rerun is flaky. Report it with both outputs, and don't rerun until green.
4. Name the PR's one kind, from the list in `one-kind-per-pr`. Put a mechanical change's exact command in the title or description. Land a check that existing code fails in its own PR with its exemption list. A check that only guards what the same PR introduces rides with it. A build change is one that alters CI config, the toolchain, or a dependency's version.
5. For a stack, put a map in the first PR description: each PR in order, its kind, and what the reviewer does with it (rule on a decision, rerun a command, read the diff). List decisions for the whole stack there once.
6. Write the report as the PR description, in the four parts `make-more9s` gives.
7. Where CI runs a check, link to that run as the evidence. Label output only your session produced as local, with the one command that reruns it. Add a screenshot or recording for anything visual.
