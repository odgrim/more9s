---
name: value-contract-before-code
description: "Apply before writing logic for a feature, flag, config attribute, output, or bug fix. Settle what the change promises before writing how it works."
disable-model-invocation: true
---

# Contract Before Code

Decide what the change promises before writing how it works. A promise written afterwards describes whatever the code happened to do.

- Describe the behaviour as the user will meet it: names, inputs, outputs, errors.
- Search for an existing implementation and the names the repo already uses before designing a new one.
- Name the core types, outputs, and errors before writing logic. Choose each data structure from how it will be read and written.
- The test that states the promise fails before the code exists.
- If the docs are awkward to write, change the design.
- When you cannot state the contract without trying something, build a throwaway prototype to find it. For a decision with no precedent in the repo, build two or three and compare. Delete the prototype, then start from the contract.

The [contract-first change](../make-more9s/playbooks/contract-first-change.md) playbook gives the steps. public-interface-changes says when a written proposal leads the stack.

## Check

- Did the test fail before the change and pass after?
- Do the docs describe what the code now does?
