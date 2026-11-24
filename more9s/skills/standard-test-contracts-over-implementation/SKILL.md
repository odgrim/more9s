---
name: standard-test-contracts-over-implementation
description: "Apply when you write, change, keep, skip, or delete a test. Assert what the code's users can observe, so the test fails when that behaviour breaks and keeps passing when only the internals change."
disable-model-invocation: true
---

# Test Contracts Over Implementation

Users of the code can observe return values, errors, state they can read back, and effects on outside systems. Private helpers, internal call order, and intermediate data are implementation.

Judge each test against two edits:

- Break the behaviour (a wrong value, a skipped or doubled effect). If the test still passes, it proves nothing. Look for a loose assertion, or one on data the test built itself.
- Change the internals and keep every observable result. If the test fails, it's pinned to the implementation.

Then:

- Drive the code through its public interface with a concrete input. Take the expected value from the requirement, not from the code under test.
- What an external service receives is behaviour. A call to an internal helper isn't.
- Pair "this never happens" with a case where it does. Assert the error type callers branch on, not the message.
- Make a test give the same result on every run. Pass in the clock, the random seed, and the ordering, and use a fake for the network.
- Never delete, skip, or loosen a test that fails because behaviour broke. If one fails only because internals changed, rewrite it to assert the contract, or delete it if another test already does.
- Report any existing test that fails either edit and that the task doesn't touch.

## Check

- Does the test fail when you break the behaviour, and pass when you change only the internals?
