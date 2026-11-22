---
name: value-experience-first
description: "Apply when a design choice trades what the user meets (a name, a default, an error, an output, a step they must take) against what is easier to build, and when the request holds more than can be finished. Choose what the user meets, and ship fewer things finished."
disable-model-invocation: true
---

# Experience First

The user is whoever consumes the work: the person at the terminal, the script that parses the output, the colleague who imports the module, the next maintainer. That something was easier to build is not a reason they will accept.

- Name the user of this change and what they do with it before choosing between designs.
- When the easier implementation leaves the user an extra step, a surprising default, or an error they cannot act on, build the other one. simplest-thing-that-works then picks the simplest code that delivers it. It does not pick the experience.
- Ship fewer things finished. A feature is finished when its errors, help, docs, and failure paths meet the standards, not when the main path works. When the request holds more than can be finished, finish the core and list the rest in the report's gaps.
- Every command, flag, option, and output field is something the user must learn and the tool must keep. Add one when the contract needs it.
- In the report, describe the change from the user's side: what they can now do, or what they will see differently.

contract-before-code describes the behaviour as the user will meet it. This leaf decides between two such descriptions.

## Check

- Run the change as its user would, from the docs alone. Did any step need knowledge the docs or the output did not give?
- Is everything the change ships finished, with the unfinished parts named in the gaps?
