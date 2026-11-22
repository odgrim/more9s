---
name: value-explain-the-number
description: "Apply before measuring, and before trusting, reporting, or acting on a measured number: a speedup, a regression, a throughput, a latency, a size, or an eval result. Show the spread, name what limits the number, and rule out that it measured something else."
disable-model-invocation: true
---

# Explain the Number

A measured number is a claim about the work. One run shows that the command finished, not that the number is the effect.

- Before the run, write the decision the number feeds and the result that would change it.
- Run it enough times to see the run-to-run spread. A difference smaller than the spread is not an effect.
- Measure the baseline the same way: the same command, machine, and session.
- Name the resource or code path that limits the number, from a profile or counters taken during a run. A reading of the code is not a limiter.
- List what else the number could be measuring and rule out each with evidence: errors, skipped or cached work, code that never ran, a cold start against a warm one, an untuned baseline, a part too small to move the total.
- A number that is computed, not sampled (a file size, a count, a line total), has no spread. Say it is deterministic and give the command. The baseline and the list of what else it could be measuring still apply.
- For an eval result, confirm that every run did the task and that the gap holds across trials.
- Keep the run count, the spread, and the limiter beside the number wherever it is reported.

prove-it-works says what counts as evidence. This leaf applies when the evidence is a number.

## Check

- Does every number in the report carry its run count and spread, or the word deterministic?
- Was the baseline measured by the same command in the same session?
