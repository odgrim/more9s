# more9s

A Claude Code plugin that holds one person's values and standards for agentic development, as small skills an agent reads when a task triggers them.

A value governs how the agent works: when to ask, when to stop, what counts as proof. A standard is a rule for an artifact (code, a test, a commit, a PR, prose) that you can check against it.

The structure follows [pstack](https://github.com/cursor/plugins/tree/main/pstack): one index skill, and one short skill per rule, so a rule's name is enough to steer the agent. The rules are different.

## Install

```
/plugin marketplace add odgrim/more9s
/plugin install more9s@more9s
```

## Use

Start a task with the index:

```
/more9s:make-more9s

Add a --limit flag to the top command.
```

The index lists every value and standard with the situation that triggers it. The agent reads the ones the task triggers, applies them, and names each one that changed a decision in its report.

To steer mid-task, name a rule: "apply fix root causes", or `/more9s:value-fix-root-causes`.

## What's in it

| Part | Count | Where |
|---|---|---|
| Index | 1 | `more9s/skills/make-more9s/SKILL.md` |
| Values | 20 | `more9s/skills/value-*/` |
| Standards | 25 | `more9s/skills/standard-*/` |
| Playbooks | 7 | `more9s/skills/make-more9s/playbooks/` |
| Language skills | 3 | `golang-`, `rust-`, and `typescript-best-practices` |
| Commands | 7 | see below |
| Hook | 1 | `more9s/hooks/` |

The index also sets what a task owes at each size, which actions wait for the human, the four-part report, and which rule wins when two disagree.

### Commands

Short handles for things you'd otherwise type as a paragraph.

| Command | What it does |
|---|---|
| `/more9s:wat` | Says the last message again in plain words |
| `/more9s:why` | Answers why code is the way it is, from commits, PRs, and issues |
| `/more9s:what-breaks` | Finds what a change breaks outside its diff, and proves the fact its safety rests on |
| `/more9s:catch-up` | Says what changed since your last message and lists what's waiting on you |
| `/more9s:sharpen` | Rewrites a prompt to ask for what an expert would do |
| `/more9s:audit-mistakes` | Finds mistakes the repo keeps repeating and makes each fail a check |
| `/more9s:be-quiet` | Deletes or shortens the comments in the current change |

### Hook

After each Write or Edit, the hook checks the added text for the rules a pattern can catch: an em dash in prose, a TODO with no reference, a suppression with no named check or reason, a new snapshot file, and a new file with a name like `utils`. It reports back to the agent. It can't block the write.

## Develop

The index and the values and standards have to agree. A test checks that they do, and that the index stays small enough to survive a compaction:

```
cd more9s
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m unittest discover -s hooks -p 'test_*.py'
```

### Evals

`more9s/evals/` holds seven cases for `claude plugin eval`. Each is a small repo and an ordinary request, built so the easy path breaks a rule.

```
more9s/evals/run.sh                      # every case
more9s/evals/run.sh out/run --tag house  # the cases that test house rules
```

The script runs each case in three arms (the whole plugin, the index with no values or standards behind it, and no plugin), then runs `grade.py`, which executes the code each run produced and writes one table. It runs agent-written code on your machine, outside the eval sandbox, and it costs real usage: about twenty dollars for the house cases at three runs per arm.

## Licence

MIT. See [LICENSE](./LICENSE).
