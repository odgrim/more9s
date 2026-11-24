---
name: standard-no-golden-files
description: "Apply when you're asserting on output: machine-format output, rendered text, a generated file, a fixture. State the expected value from the requirement. Don't store a copy of what the code produced."
disable-model-invocation: true
---

# No Golden Files

A golden file records behaviour, not the requirement. One regenerate command turns any failure green, and an author facing a failing check will run it.

- Add no golden or snapshot files. The more9s hook flags a new one.
- Validate machine-format output against a schema kept in the repo. The schema is the authority and the type is derived from it. A schema generated from the type is a golden file. Changing the schema changes a public interface.
- A schema passes a wrong value of the right type, and doesn't see order or stream. Assert the values that matter by hand, and assert order and stream where they're part of the contract.
- For text a person reads (help, a rendered error), assert the parts the user acts on: the flag name, the location, the suggested fix. Don't assert the whole text.
- Test a generated file by using it: compile it, parse it, or run it.
- A fixture is stored input. Write a small one by hand. If it's too large to write by hand or derived from another source, produce it with a deterministic generator kept in the repo, and change it by rerunning the generator.
- The one exception is a characterization test that scaffolds a refactor of code no contract test covers. Put it in a `characterization` directory, list it in the report's decisions, and delete or replace it by the last PR of the stack.

## Check

- Does machine-format output validate against the schema, on success and on failure?
