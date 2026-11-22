---
name: standard-test-contracts-over-implementation
description: "Apply when you write, change, keep, skip, or delete a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when only the internals change."
disable-model-invocation: true
---

# Test Contracts Over Implementation

A test states what users of the code can observe: return values, errors, state they can read back, and effects on outside systems. Private helpers, internal call order, and intermediate data are implementation.

## Writing

- Drive the code through its public interface with a concrete input.
- Derive the expected value from the requirement, not from the code under test.
- What an external service receives is behaviour. A call to an internal helper is not.
- Pair "this never happens" with a case where it does.
- Assert the error type callers branch on, not the message.
- A test gives the same result on every run. Pass in the clock, the random seed, and the ordering, and use the owner's fake for the network.
- This holds wherever the language puts tests. A test beside private code still asserts only what callers observe.

## Output

- No golden or snapshot files. The expected value is a copy of what the code produced, so it records behaviour and does not state the requirement. One regenerate command turns any failure green, and an author under a failing check will run it. A hook rejects a new one.
- Machine-format output is validated against a schema kept in the repo. Derive the output type from the schema, or the schema from the type, as type-system-discipline says. The schema is the contract.
- A schema passes a wrong value of the right type. Assert the values that matter by hand, from the requirement.
- A schema does not see order or stream. Where public-interface-changes makes the order of output, or the stream it goes to, part of the contract, a test asserts each.
- A change to the schema is a change to a public interface. Removing or renaming anything in it leads the stack with a proposal, as public-interface-changes requires.
- For text a person reads (help, a rendered error), assert the parts the user acts on: the flag name, the location, the suggested fix. Do not assert the whole text.
- Test a generated file by using it: compile it, parse it, or run it.

## Fixtures

- A fixture is stored input. It comes from a generator kept in the repo. Change it by rerunning the generator, not by hand.
- Generator output is deterministic: no timestamps, absolute paths, or unstable ordering.

## Check

- Break the behaviour (a wrong value, a skipped or doubled effect). Does the test fail? If not, it proves nothing. Look for a loose assertion, or an assertion on data the test built itself.
- Change the internals and keep every observable result. Does the test still pass? If not, it is pinned to the implementation.
- Does machine-format output validate against the schema, on success and on failure?

Rewrite or delete a test you wrote or changed that fails either of the first two questions. Report an existing one that the task does not touch.

A test that fails because behaviour broke is never deleted, skipped, or loosened. Fix the code. A test that fails only because internals changed is pinned to the implementation. Rewrite it to assert the contract, or delete it when another test already does. Each test you delete or skip is listed at the top of the PR description with its reason, as checks-and-exemptions requires.
