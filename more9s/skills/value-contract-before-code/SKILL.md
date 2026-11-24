---
name: value-contract-before-code
description: "Applies before writing logic for a feature, flag, config attribute, output, or bug fix. Settles what the change promises before how it works."
disable-model-invocation: true
---

# Contract Before Code

The contract is what the change exposes: the types, signatures, and schemas that say what it accepts, what it returns, and how it fails. Write it first, in the order the [contract-first change](../make-more9s/playbooks/contract-first-change.md) playbook gives: the problem, the behaviour, the failing test, then the code.

- Before you design anything new, search for an existing implementation and for the names and types the repo already uses.
- Pick each data structure by how it'll be read and written.
- If the types are awkward to write (many optional fields, wide unions, casts), change the design.
- If you can't state the contract without trying something, build a throwaway prototype. For a decision with no precedent in the repo, build two or three and compare. Delete them, then start from the contract.

## Check

- Did the test fail before the change and pass after?
- Did you loosen any type to make the code fit?
