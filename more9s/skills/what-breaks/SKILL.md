---
name: what-breaks
description: "Finds what a change breaks outside its own diff, and proves the one fact its safety rests on by running code. Use for /what-breaks."
argument-hint: "[diff, PR, or description of the change]"
disable-model-invocation: true
---

# What Breaks

A list of callers isn't the answer. A search finds those. The job is the breakage a search doesn't show, and a write-up that sounds right proves nothing.

With no argument, the change is the current diff against the base branch, working tree included.

1. Read the change: what it adds, alters, and removes, and what now behaves differently that the diff doesn't spell out.
2. Find the one fact the change is safe because of. Most changes that look risky rest on one, such as "nothing reads this field after startup". Spend the time here, not on a long list of maybes.
3. Look where a search stops:
   - data already stored or sent: a file format, a database column, a cache entry, a message on a queue
   - another program or language that reads the same bytes
   - a default, an ordering, an exit code, or a stream that a script depends on, as [public interfaces grow by addition](../standard-public-interfaces-grow-by-addition/SKILL.md) lists
   - configuration, flags, and environment that select a path the tests don't take
   - when things run: start-up order, shutdown, retries, two runs at once
   - the source of the library being called, at the version the lockfile pins
   - code several calls away from the change
4. Prove the fact. Write the smallest script or test that calls the real code and fails if the fact is false, and run it. Don't take an ask-first action to do it. [Prove it works](../value-prove-it-works/SKILL.md) says what to use when the real surface is out of reach.
5. Report. Don't fix what you find unless asked.

## The report

- **What the change does**, including the part that isn't obvious.
- **The fact it's safe because of**, and how far you got with it: stated only, pointed to a line, traced step by step, ran code, or reproduced in the running program. If you didn't run code, write "unproven".
- **Risks.** For each: how it breaks, the file and line, how likely, what it costs, and the command that would check it.
- **Cleared.** What you checked and why it's fine. A search that found nothing counts, with the search.
- **The cheapest test that would catch the real break**, with the script you wrote.

Never invent a caller, a file, or an API to fill a section.

## Check

- Is the fact proven by output from a command, or marked unproven?
