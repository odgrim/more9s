---
name: standard-cli-is-a-machine-contract
description: "Applies when adding or changing a CLI command, flag, environment variable, output, or exit path. Treats its names and outputs as an API, because scripts and CI consume it."
disable-model-invocation: true
---

# The CLI Is a Machine Contract

A script can't read prose or answer a prompt. Give it output that's typed, stable, and reachable without a terminal.

- Send data to stdout and everything else to stderr. Have each command return a type with named fields, serialised in one place.
- Use one flag to select the machine format, and put everything a script needs in it. Log and error wording can change.
- When a command fails, still write its typed output, with the error in it. Give each failure a script handles differently its own documented exit code.
- Validate every input before the first side effect.
- Never prompt when stdin isn't a terminal. Fail and name the flag that answers the prompt.
- Give each flag that configures behaviour an environment variable under the tool's prefix. Precedence is flag, environment, config file, default. A flag that confirms or forces one run gets none.
- Follow an existing CLI's naming convention. For a new one: commands end in a verb, flags start with a noun and share a prefix per subsystem, negation uses `no-`, and booleans accept `=true` and `=false`.

## Check

- In the machine format, with stdin closed, does stdout parse as the documented type on both success and failure?
