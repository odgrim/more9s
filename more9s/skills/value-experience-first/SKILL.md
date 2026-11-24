---
name: value-experience-first
description: "Applies when a design choice trades what the user meets (a name, a default, an error, an output, a step they have to take) against what's easier to build. Chooses what the user meets."
disable-model-invocation: true
---

# Experience First

The user is whoever consumes the work: the person at the terminal, the script parsing the output, the colleague importing the module, the next maintainer. "It was easier to build" isn't a reason they'll accept.

- Before you choose between designs, name the user of this change and what they do with it.
- If the easier implementation leaves the user an extra step, a surprising default, or an error they can't act on, build the other one.
- Then write the simplest code that delivers that experience. Simplicity picks the code, not the experience.
- Add a command, flag, option, or output field only when the contract needs it. The user has to learn each one and the tool has to keep it.
- In the report, describe the change from the user's side: what they can now do, or what they'll see differently.

## Check

- Run the change as its user would, from the docs alone. Did any step need something the docs or the output didn't tell you?
