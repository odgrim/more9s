### Contract-first change

1. State the problem in a sentence or two. Take it from the issue if there is one.
2. Describe the behaviour as the user will meet it: names, inputs, outputs, errors.
3. Write a test that fails with a clear message. For a bug, the test reproduces the bug before the fix exists, as `reproduce-before-fixing` requires.
4. Write code until it passes.

Skip steps 1 and 2 for a small internal change. Skip step 3 for a change that alters no observable behaviour (a refactor, a rename, docs), and run the existing tests before and after. If no existing test would catch a change in the code you're refactoring, write a characterization test first, as `no-golden-files` allows.

For a significant change to a public surface, put the written proposal in the first PR of the stack, as `public-interface-changes` requires.
