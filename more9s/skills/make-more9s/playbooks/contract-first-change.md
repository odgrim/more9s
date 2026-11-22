### Contract-first change

1. State the problem in a sentence or two. Take it from the issue when there is one.
2. Describe the behaviour as the user will meet it: names, inputs, outputs, errors.
3. Write a test that fails with a clear message. For a bug, the failing test reproduces the bug before the fix exists, and fix-root-causes says where the fix goes.
4. Write code until it passes.

A small internal change skips steps 1 and 2. A change that alters no observable behaviour (a refactor, a rename, docs) skips step 3 and runs the existing tests before and after.

A significant change to a public surface puts its written proposal in the first PR of the stack, as public-interface-changes requires.
