---
name: standard-cli-is-a-machine-contract
description: "Apply when adding or changing a CLI command, flag, environment variable, output, or exit path. Scripts and CI consume it, so its names and outputs are an API."
disable-model-invocation: true
---

# The CLI Is a Machine Contract

Scripts and CI call the CLI more than people do, so its names and outputs are an API.

## Output

- Data goes to stdout and logs go to stderr.
- Each command returns a type with named fields, serialised in one place.
- One flag selects the machine format. Without it, stdout may be formatted for a person. Colour and progress output appear only on a terminal.
- A failed command still writes its typed output in the machine format, with the error in it.
- Exit codes are documented and stable. Zero means success. Each failure a script handles differently has its own code.
- Anything a script needs is in the typed output. Log and error wording can change.

## Input

- Validate every input before the first side effect.
- Never prompt when stdin is not a terminal. Fail with the flag that answers the prompt.
- An existing CLI's naming convention wins. The rest of this bullet is the default for a new CLI. Commands end in a verb. Flags start with a noun, and flags for one subsystem share a prefix. Negation uses `no-`. Booleans accept `=true` and `=false`.
- A flag that configures behaviour has an environment variable under the tool's prefix. Flags that confirm or force one run (`--yes`, `--force`) and `--help` and `--version` have none. Precedence is flag, environment, config file, default.

## Changes

- A change to a name or an output follows public-interface-changes.

## Check

- In the machine format, does stdout parse as the documented type, on success and on failure?
- Does the command finish with stdin closed?
- Would an existing script still work after this change?
