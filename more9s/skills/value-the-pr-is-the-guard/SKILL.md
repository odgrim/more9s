---
name: value-the-pr-is-the-guard
description: "Apply when you're about to ask 'should I do X?' about how to do the work. If a PR will carry it, decide and keep going."
disable-model-invocation: true
---

# The PR Is the Guard

The reviewer can reject any decision in a PR. Asking first just adds a round trip.

- A PR carries the work when the human asked for one, or the repo's documented flow lands changes through reviewed PRs.
- Decide, do the work, and open the PR. Don't ask how to do it first.
- List every decision the reviewer should rule on in the report, the one that costs most to revert first.
- Put a decision the reviewer might reject in its own commit or PR, so rejecting it keeps the rest.
- If rejecting a decision would throw away most of the work, open it first as a proposal PR. `requirements-reshape-the-design` and `public-interfaces-grow-by-addition` say when.
- Size each PR by `one-kind-per-pr`. A PR too big to read gets no real review.
- If no reviewed PR will carry the work, commit it on a local branch the session created, one commit per unit as `commits-prove-the-work` says. Do this without being asked: working to more9s is the request. It holds for a one-line fix and for an urgent one.
- Don't commit to the default branch. Don't push unless asked.

The [after the PR opens](../make-more9s/playbooks/after-the-pr-opens.md) playbook covers review comments and CI.

## Check

- Does the report list every decision the reviewer should rule on?
- Did you ask about anything a PR would have carried?