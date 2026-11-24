---
name: value-the-pr-is-the-guard
description: "Apply when you're about to ask 'should I do X?' about how to do the work. If a PR will carry it, decide and keep going."
disable-model-invocation: true
---

# The PR Is the Guard

The reviewer can reject any decision in a PR. Asking first just adds a round trip.

- Decide, do the work, and open the PR. Don't ask how to do it first.
- List every decision the reviewer should rule on in the report.
- Put a decision the reviewer might reject in its own commit or PR, so rejecting it keeps the rest.
- If rejecting a decision would throw away most of the work, open it first as a proposal PR. `requirements-are-not-workarounds` and `public-interface-changes` say when.
- Size each PR by `one-kind-per-pr`. A PR too big to read gets no real review.
- If no reviewed PR will carry the work, leave it in the working tree or on a local branch. Don't commit to the default branch or push unless asked.

The [after the PR opens](../make-more9s/playbooks/after-the-pr-opens.md) playbook covers review comments and CI.

## Check

- Does the report list every decision the reviewer should rule on?
- Did you ask about anything a PR would have carried?