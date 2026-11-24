---
name: value-explain-the-number
description: "Applies before measuring, and before trusting, reporting, or acting on a measured number: a speedup, a regression, a throughput, a latency, a size, an eval result. Shows the spread, names what limits the number, and rules out that it measured something else."
disable-model-invocation: true
---

# Explain the Number

A measured number is a claim about the work. One run shows the command finished, not that the number is the effect.

- Before the run, write down the decision the number feeds and the result that would change it.
- Run it enough times to see the run-to-run spread. A difference smaller than the spread isn't an effect.
- Measure the baseline the same way: same command, machine, and session.
- Name the resource or code path that limits the number, from a profile or counters taken during a run. Reading the code doesn't count.
- List what else the number could be measuring, and rule each out with evidence: errors, skipped or cached work, code that never ran, a cold start against a warm one, an untuned baseline, a part too small to move the total.
- A computed number (a file size, a count) has no spread. Call it deterministic and give the command. It still needs the baseline and the list above.
- For an eval result, confirm every run did the task, the gap holds across trials and models, and the scenario is one that matters.
- Wherever you report the number, keep the run count, the spread, and the limiter beside it.

## Check

- Does every number in the report have its run count and spread, or the word "deterministic", and a baseline measured the same way?
