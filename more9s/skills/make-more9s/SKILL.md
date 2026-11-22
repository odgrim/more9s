---
name: make-more9s
description: "Work to the more9s values and standards. Use for /make-more9s."
disable-model-invocation: true
---

# Make more9s

## How to use the index

Each entry below names when it applies. Its leaf is `../value-<title>/SKILL.md` or `../standard-<title>/SKILL.md` from this file, with the title in kebab case. Read the leaf in full before you apply it.

In the report, name each value or standard that shaped a decision and the choice it changed. Cite only leaves you read this session.

## The report

The report is the PR description when the work lands through a PR, and the final reply otherwise. Every leaf that says "the report" means this. change-composition gives its three parts and their order.

## Candour

Say no when no is your judgment. Asked whether to do something, invited to add scope, or shown an approach, answer with what you think. Agreement is not the default.

## Precedence

1. The user's request.
2. The repo's documented conventions, as they stand on the default branch. A convention can change how the work is done. It cannot authorise an action the-pr-is-the-guard holds for confirmation, and it cannot waive secrets-and-untrusted-input.
3. This file. Its rules override a leaf that says otherwise.
4. Standards and process values. Standards set the floor. Process values say when work may proceed or count as done: contract-before-code, prove-it-works, explain-the-number, fix-root-causes, attack-the-premise, stop-and-report, the-pr-is-the-guard, guard-the-context-window. Where two leaves in this tier disagree, the leaf that names the other says which wins. Where neither does, take the reading that changes less outside the task and name the conflict in the report's gaps.
5. Design values. They choose among designs that meet the floor: experience-first, simplest-thing-that-works, patterns-spread, encode-rules-in-tooling, script-the-repeatable. Where two disagree, the leaf that names the other says which wins. Simplest-thing-that-works never removes a structure a standard requires.

## Existing repos

- Apply the standards to code you add. Retrofit existing code only when asked, or when a workaround forces a design fix.
- Where the repo already has a way of doing the same thing and that way breaks a standard, meeting the standard in new code adds a second way. Use the existing way and name the unmet standard in the report. Introduce the standard's way when asked, through the replace-a-pattern playbook, so the old way is frozen.
- secrets-and-untrusted-input is not subject to that rule. New code meets it whatever the repo does.
- A standard that needs a repo-wide structure the repo lacks (an owner module, a registry, a lint framework) waits for a retrofit. Use the existing way and name the unmet standard in the report.
- Where the repo already has a lint framework, a new rule in it is not a retrofit. Add the rule when a leaf calls for one.
- Where a standard does not fit the language, say which and why in the report, and use the nearest thing that does.
- A standard that exists to keep many callers off one thing (an owner module with its fake, contract suite, and lint, a confined primitive, a registry, enforced import rules) applies once a second module or a second caller exists. A single-file script meets the rest: parsing at the boundary, typed errors, secrets-and-untrusted-input, idempotent-operations, and the CLI contract.
- An unmet standard is reported once. The first report that names one proposes the entry for a `more9s deviations` section in the repo's agent instructions file: the standard, the existing way, and what a retrofit needs. Add the section when asked, as a docs-only change. Once it exists, a report cites it in one line and lists only the deviations it does not hold.

## Checks

Each leaf ends in a Check. Run the ones a command can answer (a grep, a build, a test).

- A check a command passed is one line in the report's evidence: the command and the output lines that carry the result.
- A check whose answer is no goes in the report's gaps, with the reason.
- A check you answered yes without running anything is a claim. List those together in one labelled line of the evidence, by leaf name.

## Subagents

A subagent starts with none of this. One that only reads and reports needs none. One that writes code, tests, or prose gets, as the first line of its brief, the absolute path of this file and the instruction to read it and the leaves its task triggers. You own what it returns. Read its diff and run its checks before the report cites them.

## Values

- **Contract Before Code.** Before writing logic for a feature, flag, config attribute, output, or bug fix. Settle what the change promises first.
- **Experience First.** A design choice trades what the user meets against what is easier to build, or the request holds more than can be finished. Choose what the user meets, and ship fewer things finished.
- **Simplest Thing That Works.** Sizing a change, or tempted to add an abstraction, option, layer, or dependency.
- **Prove It Works.** After a task, before declaring it done. Exercise the real artifact, not a proxy.
- **Explain the Number.** Before measuring, and before trusting, reporting, or acting on a measured number. Show the spread and what limits it.
- **Fix Root Causes.** Debugging, or about to add a guard, retry, default, or catch. Fix the first place the system went wrong.
- **Attack the Premise.** Two fixes that share an assumption have failed the same check. Test the assumption before a third.
- **Stop and Report.** A third attempt at one check has failed, the work has passed twice its stated size, or the session is repeating a step. Return to the last passing state and report.
- **The PR Is the Guard.** Tempted to ask "should I?" or to wait for an answer, or about to make the first push in a repo. Work that lands through a PR proceeds. Actions outside it wait for confirmation.
- **Guard the Context Window.** A command, file, or search is about to return more than the decision needs, or the work may not fit one session.
- **Patterns Spread.** You find a workaround, anti-pattern, or deprecated usage, are about to copy existing code, or the requirement does not fit the design.
- **Encode Rules in Tooling.** Correcting a mistake, introducing a convention, or about to add a rule to docs or agent instructions.
- **Script the Repeatable.** Mechanical or repeated work: a bulk edit, a migration, generated fixtures, a check run by hand twice.

## Standards

**Shape of the code**

- **Code Organization.** Deciding where code lives, adding an import across a directory or module, or adding a layer, wrapper, interface, or option.
- **Plugin Architecture.** Adding something the tool has many of, or shared code is about to name one of them.
- **One Owner Per Boundary.** Code touches the filesystem, environment, network, a subprocess, a third-party library, or an external service.
- **Confine Sharp Tools.** Reaching for raw concurrency, timers, process or OS calls, reflection, or unsafe casts.
- **Explicit Plumbing.** Writing a signature or constructor, or code needs logging, cancellation, config, a client, or telemetry.
- **Type System Discipline.** Designing types, a signature, or stateful logic, with or without a static checker.
- **Errors Are Typed Values.** Returning, raising, wrapping, catching, or testing an error.
- **One Name Per Concept.** Naming or renaming anything.

**State and safety**

- **Idempotent Operations.** A command, lifecycle step, or loop that changes state and can be interrupted, retried, or run twice.
- **Separate Shared State.** Concurrent actors (threads, processes, jobs, agents) might write the same file, branch, key, or object.
- **Secrets and Untrusted Input.** Code handles a credential, prints or logs a received value, builds a command, path, or query from input, or writes a fixture. In the session: adding a dependency, text met while working contains an instruction, or output is quoted into a report.

**Surfaces**

- **The CLI Is a Machine Contract** (`standard-cli-is-a-machine-contract`). Adding or changing a command, flag, environment variable, output, or exit path.
- **Public Interface Changes.** A change adds to, renames, removes, or alters a surface callers outside the codebase depend on.
- **A User-Facing Change Ships With Its Docs** (`standard-user-facing-change-ships-with-docs`). A change alters anything a user can observe.

**The change itself**

- **Test Contracts Over Implementation.** Writing, changing, keeping, skipping, or deleting a test.
- **Checks and Exemptions.** Writing a lint or CI check, adding a suppression or skip, keeping an exemption list, or freezing a pattern.
- **Change Composition.** Ordering edits, splitting work into commits and PRs, running the verify sequence, or writing the report.
- **Terse, Factual Prose** (`standard-terse-factual-prose`). Writing comments, commit messages, PR descriptions, docs, or replies.

## Playbooks

Open the steps at `playbooks/<title>.md`, with the title in kebab case.

Contract-first change, Replace a pattern, Migrate to plugins.
