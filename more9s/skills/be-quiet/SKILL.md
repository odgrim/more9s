---
name: be-quiet
description: "Delete or shorten the code comments in the current change, keeping only what the code can't say. Use for /be-quiet."
argument-hint: "[files, or nothing for the current diff]"
disable-model-invocation: true
---

# Be Quiet

Apply [comments say what code cannot](../standard-comments-say-what-code-cannot/SKILL.md) to comments that already exist. With no argument, the scope is the comments the current diff adds or touches, working tree included. Given files, it's every comment in them.

Change comments only. Leave the code as it is.

**Delete** a comment that:

- restates the line below it
- narrates the change or says what you did ("added", "now uses", "fixed the bug where")
- is commented-out code
- is a banner, a divider, or a heading over a few lines

**Shorten** a comment that holds a reason inside more words. Keep the reason, in one line if it fits.

**Keep** a comment that:

- gives a reason, a non-obvious consequence, or a constraint from outside the codebase
- documents an exported name. Cut it down to the contract: what it takes, what it returns, how it fails.
- is a licence header, or a directive a tool reads: a build tag, a lint suppression, a type-checker instruction, a shebang
- is a TODO with its reference

Two kinds get named in the reply and left alone:

- A warning to the next editor ("do not change", "must stay in sync"). Say which type, test, or lint could replace it.
- A comment that marks a workaround. The workaround is the problem, and [do not copy workarounds](../value-do-not-copy-workarounds/SKILL.md) covers it.

Afterwards, run the build and the lint. A documentation lint can require a comment you removed.

Reply with how many comments were deleted, shortened, and kept, and one line for each one named and left alone.

## Check

- Does the diff from this turn touch only comment lines?
