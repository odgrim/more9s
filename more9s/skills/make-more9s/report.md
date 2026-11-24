### The report

The report is the PR description if the work lands through a PR, and the final reply if not. Every leaf that says "the report" means this. Start it as a draft with the first unit and keep it current, as `write-state-down` says. It has four parts, in this order. Leave out a part with nothing in it, except the first.

1. **Change.** The goal in one sentence, then what the user can now do or will see differently.
2. **Decisions.** What the reviewer should rule on: what you chose, what you rejected, and what reverting costs, the costliest to revert first. Also the reading of the request you built, if it had more than one, and every suppression, exemption, skipped or deleted test, and new dependency.
3. **Gaps.** What was asked and not done, and what was done and not asked. Any check that failed, came back inconclusive, or didn't run, and why. The better way if you used an existing one, and any standard the repo couldn't meet yet.
4. **Evidence.** Each check with its command and the output lines that carry the result, with cuts marked and secrets redacted. If a command made the change (a `sed`, a script, a generator), give that command too, exactly as run. Put it last, in a collapsed block where the host renders one. A check that passed gets one line here and no mention above.

#### Checks

Each leaf ends in a Check. For each leaf you read, run the checks a command can answer (a grep, a build, a test).

- A check a command passed gets one line in the report's evidence: the command and the output lines that carry the result.
- A check whose answer is no goes in the report's gaps, with the reason.
- A check you answered yes without running anything is a claim. List those together in one labelled line of the evidence, by leaf name.
