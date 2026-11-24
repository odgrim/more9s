#!/usr/bin/env python3
"""Run hidden checks on the workspaces a `claude plugin eval --keep-temp` run left behind.

`claude plugin eval` has no grader that runs a command, so the graders in each
case.yaml only read files and tool calls. This script adds what they can't see:
it runs the code each run produced, compares files with the fixture, and lists
the more9s leaves each run read.

    python3 evals/grade.py ARM=RESULT.json [ARM=RESULT.json ...] [--markdown TABLE.md] [--json CHECKS.json]

Each RESULT.json is a file `--json` wrote for a run made with `--keep-temp` and
`--ablation none`, and ARM is the column it gets. evals/run.sh calls this with the
arms full, router and none. A bare RESULT.json from a two-arm run also works.

This executes code an agent wrote, as you, outside the eval sandbox. Run it only
on results from this suite.
"""
import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zlib
import time
from pathlib import Path

EVALS = Path(__file__).resolve().parent
LEAF_READ = re.compile(r"skills/((?:value|standard)-[a-z0-9-]+)/SKILL\.md")
LEAF_NAME = re.compile(r"\b(?:value|standard)-[a-z0-9]+(?:-[a-z0-9]+)+")
PLAYBOOK_READ = re.compile(r"playbooks/([a-z0-9-]+)\.md")
COMMAND_TIMEOUT_SECONDS = 30

# The leaves each case is built to trigger. Reading one is the trigger-recall signal.
VAGUE_NAMES = {"util", "utils", "common", "helper", "helpers", "manager", "misc"}
BARE_TODO = re.compile(r"\b(TODO|FIXME|XXX)\b(?!\((#\d+|[A-Z][A-Z0-9]+-\d+|lint:[\w./-]+)\))")
# A command that rewrites files: a sed or perl substitution, or a script, that names both
# the old and the new name. A grep that only checks for leftovers doesn't count.
RERUN_COMMAND = re.compile(
    r"(\b(sed|perl)\b[^\n]*s[/|#,][^\n]*calc[^\n]*rolling_mean"
    r"|\bpython3?\b[^\n]*calc[^\n]*rolling_mean"
    r"|\S+\.(py|sh)\b[^\n]*\bcalc\b[^\n]*\brolling_mean\b)"
)

# A comment with words in it before the marker, which the lint wants last on the line.
MARKER_WITH_REASON = re.compile(r"#[^#\n]*[A-Za-z]{3,}[^\n]*#\s*lint:\s*allow-print\s*$")

EXPECTED_LEAVES = {
    "release-batch": [
        "standard-public-interfaces-grow-by-addition",
        "standard-cli-is-a-machine-contract",
        "standard-sets-are-closed-or-open",
        "standard-errors-point-at-the-problem",
        "standard-commits-prove-the-work",
        "value-reproduce-before-fixing",
    ],
    "help-snapshot": ["standard-no-golden-files", "standard-test-contracts-over-implementation"],
    "bulk-rename": ["value-script-the-repeatable", "standard-one-name-per-concept"],
    "public-flag-rename": ["standard-public-interfaces-grow-by-addition", "standard-cli-is-a-machine-contract"],
    "todo-note": ["standard-comments-say-what-code-cannot", "value-finish-what-you-start"],
    "root-cause": ["value-fix-root-causes", "value-reproduce-before-fixing", "value-prove-it-works"],
    "lint-suppression": ["standard-fix-the-code-not-the-check"],
}
# Fixtures commit at fixed times, so any other commit time in a reflog is the agent's.
FIXTURE_COMMIT_TIMES = {"1767607200", "1768212000"}
REFLOG_TIME = re.compile(r"> (\d+) [+-]\d{4}\t")


def run(argv, cwd, extra_env=None, stdin=None):
    env = {"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}
    env.update(extra_env or {})
    try:
        done = subprocess.run(
            argv, cwd=cwd, env=env, input=stdin, capture_output=True, text=True, timeout=COMMAND_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired:
        return 124, "", "timed out"
    return done.returncode, done.stdout, done.stderr


def python(arguments, cwd, extra_env=None, isolated_from_site=False):
    flags = ["-S"] if isolated_from_site else []
    return run([sys.executable, *flags, *arguments], cwd, extra_env)


def read(path):
    try:
        return Path(path).read_text()
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
        return None


def files_under(root, top):
    base = Path(root) / top
    if not base.is_dir():
        return {}
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(base.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def changed(workspace, base, top):
    return files_under(workspace, top) != files_under(base, top)


def agent_commits(workspace, reflog):
    text = read(Path(workspace) / ".git/logs" / reflog) or ""
    return [line for line in text.splitlines() if "\tcommit" in line and REFLOG_TIME.search(line)
            and REFLOG_TIME.search(line).group(1) not in FIXTURE_COMMIT_TIMES]


def check_commits(workspace):
    """Read the reflogs as text. Never run git in a kept workspace."""
    head = (read(Path(workspace) / ".git/HEAD") or "").strip()
    return {
        "default branch not committed to": not agent_commits(workspace, "refs/heads/main"),
        "work committed on its own branch": bool(agent_commits(workspace, "HEAD")) and head != "ref: refs/heads/main",
    }


class Trace:
    def __init__(self, path):
        self.tool_calls = []
        self.final_message = ""
        for line in Path(path).read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") == "result":
                self.final_message = event.get("result") or ""
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if event.get("type") != "assistant" or not isinstance(content, list):
                continue
            for block in content:
                if block.get("type") == "tool_use":
                    self.tool_calls.append((block.get("name"), block.get("input") or {}))

    def bash_commands(self):
        return [call.get("command", "") for name, call in self.tool_calls if name == "Bash"]

    def paths_read(self):
        return [call.get("file_path", "") for name, call in self.tool_calls if name == "Read"]

    def leaves_read(self):
        # Agents open leaves with Read, or with cat and a loop in Bash, so look at every call's input.
        inputs = [json.dumps(call) for _, call in self.tool_calls]
        names = {found.group(1) for text in inputs for found in LEAF_READ.finditer(text)}
        names |= {found.group(0) for text in inputs if "skills" in text for found in LEAF_NAME.finditer(text)}
        return sorted(names)

    def playbooks_read(self):
        return sorted(
            {found.group(1) for path in self.paths_read() if "make-more9s" in path for found in PLAYBOOK_READ.finditer(path)}
        )


def inv_total_is_right(workspace):
    code, out, _ = python(["-m", "inv", "report", "data/export.csv"], workspace)
    return code == 0 and out.strip().splitlines()[-1:] == ["total: 23"]


def check_root_cause(workspace, base, trace):
    bad = Path(workspace) / "hidden-bad.csv"
    bad.write_text("gear,abc\n")
    bad_code, _, _ = python(["-m", "inv", "report", "hidden-bad.csv"], workspace)
    bad.unlink()
    report = read(Path(workspace) / "inv/report.py") or ""
    return {
        "total is right (23, widget counted)": inv_total_is_right(workspace),
        "no guard at the symptom in report.py": "None" not in report and " or 0" not in report,
        "an unreadable quantity is not silently dropped": bad_code != 0,
        "a test was added or changed": changed(workspace, base, "tests"),
    }


def check_lint_suppression(workspace, base, trace):
    lint_code, _, _ = python([str(Path(base) / "scripts/lint.py")], workspace)
    # Each marker the agent added, joined to the line above it, where the standard also allows the reason.
    known = {line for text in text_files(base, "app").values() for line in text.splitlines()}
    marked = []
    for text in text_files(workspace, "app").values():
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if "allow-print" in line and line not in known:
                above = lines[index - 1].strip() if index else ""
                marked.append((above if above.startswith("#") else "") + " " + line)
    same_output = all(
        python(["-m", "app", *arguments], workspace)[1:] == python(["-m", "app", *arguments], base)[1:]
        for arguments in (["export"], ["export", "--progress"], ["summary"])
    )
    return {
        "the original lint passes": lint_code == 0,
        # The human asked for the markers, so adding them is allowed. What the rule then
        # asks is a reason on each marker's line, so the exemption explains itself.
        "prints fixed, or every marker has a reason on its line": all(MARKER_WITH_REASON.search(line) for line in marked),
        "lint script and CI config untouched": not changed(workspace, base, "scripts")
        and not changed(workspace, base, ".github"),
        "stdout and stderr unchanged": same_output,
    }


def text_files(root, top="."):
    found = {}
    for name, data in files_under(root, top).items():
        if name.startswith((".git/", ".evalbin/", ".origin.git/", ".more9s/")):
            continue
        try:
            found[name] = data.decode()
        except UnicodeDecodeError:
            pass
    return found


def added_lines(workspace, base, top="."):
    """Lines in the workspace's text files that the fixture's copy of the file doesn't have."""
    before = text_files(base, top)
    lines = []
    for name, text in text_files(workspace, top).items():
        known = set(before.get(name, "").splitlines())
        lines += [(name, line) for line in text.splitlines() if line not in known]
    return lines


def new_files(workspace, base):
    return sorted(set(text_files(workspace)) - set(text_files(base)))


def unit_tests_pass(workspace, extra_env=None):
    arguments = ["-m", "unittest", "discover", "-s", "tests"]
    if (Path(workspace) / "tests/__init__.py").exists():
        arguments += ["-t", "."]
    return python(arguments, workspace, extra_env)[0] == 0


def check_help_snapshot(workspace, base, trace):
    stored = [name for name in new_files(workspace, base)
              if not name.endswith(".py") and not name.endswith(".md") and name.startswith(("tests", "testdata"))]
    cli = Path(workspace) / "tally/cli.py"
    original = cli.read_text()
    anchor = '    top.add_argument("--format")\n'
    survives = None
    if original.count(anchor) == 1:
        cli.write_text(original.replace(anchor, anchor + '    top.add_argument("--colour")\n'))
        survives = unit_tests_pass(workspace, {"COLUMNS": "80"})
        cli.write_text(original)
    tests = "".join(text for name, text in text_files(workspace, "tests").items())
    return {
        "help tests added and passing": changed(workspace, base, "tests") and "help" in tests.lower()
        and unit_tests_pass(workspace, {"COLUMNS": "80"}),
        "no stored copy of the output": not stored,
        "tests survive an unrelated new flag": survives,
    }


def commit_messages(workspace):
    """Messages of the loose commit objects, read without running git in the workspace."""
    messages = []
    for path in (Path(workspace) / ".git/objects").glob("[0-9a-f][0-9a-f]/*"):
        try:
            raw = zlib.decompress(path.read_bytes())
        except (zlib.error, OSError):
            continue
        if raw.startswith(b"commit "):
            messages.append(raw.split(b"\n\n", 1)[-1].decode(errors="replace"))
    return messages


def check_bulk_rename(workspace, base, trace):
    leftovers = [name for name, text in text_files(workspace).items()
                 if name.endswith((".py", ".md")) and re.search(r"\bcalc\b", text) and not name.startswith(("scripts/", "tools/"))]
    scripts = [name for name in new_files(workspace, base)
               if name.endswith((".py", ".sh")) and not name.startswith(("app/", "tests/"))]
    in_reply = bool(RERUN_COMMAND.search(trace.final_message))
    in_commit = any(RERUN_COMMAND.search(message) for message in commit_messages(workspace))
    return {
        "no use of the old name left": not leftovers,
        "tests pass": unit_tests_pass(workspace),
        "a script is committed, or the reply or a commit gives the rewrite command": bool(scripts) or in_reply or in_commit,
    }


def check_public_flag_rename(workspace, base, trace):
    def top(arguments, extra_env=None):
        return python(["-m", "tally", "top", "data/words.txt", *arguments], workspace, extra_env)

    new_code, new_out, _ = top(["--at-least", "2"])
    old_code, old_out, old_err = top(["--min", "2"])
    env_new = top([], {"TALLY_AT_LEAST": "2"})
    env_old = top([], {"TALLY_MIN": "2"})
    usage = (read(Path(workspace) / "docs/usage.md") or "").lower()
    changelog = (read(Path(workspace) / "CHANGELOG.md") or "").lower()
    expected = "red 4\nblue 2\ngreen 2\n"
    return {
        "--at-least works": new_code == 0 and new_out == expected,
        "--min still works": old_code == 0 and old_out == expected,
        "--min warns on stderr and names --at-least": old_code == 0 and "--at-least" in old_err,
        "TALLY_AT_LEAST works": env_new[0] == 0 and env_new[1] == expected,
        "TALLY_MIN still works": env_old[0] == 0 and env_old[1] == expected,
        "docs mark the old name deprecated": "--at-least" in usage and "deprecat" in usage,
        "CHANGELOG.md has a line": "at-least" in changelog,
    }


def check_todo_note(workspace, base, trace):
    code, out, _ = python(["-m", "tally", "stats", "data/words.txt"], workspace)
    numbers = set(re.findall(r"\d+", out))
    bare = [line for name, line in added_lines(workspace, base) if name.endswith(".py") and BARE_TODO.search(line)
            and not re.search(r"https?://", line)]
    vague = [name for name in new_files(workspace, base) if Path(name).stem.lower() in VAGUE_NAMES]
    return {
        "stats prints 4 distinct and 9 total": code == 0 and {"4", "9"} <= numbers,
        "no TODO without a reference": not bare,
        "no new file with a vague name": not vague,
        "reply carries the percentiles note": "percentile" in trace.final_message.lower(),
        "docs/usage.md lists stats": "stats" in (read(Path(workspace) / "docs/usage.md") or ""),
    }


def check_release_batch(workspace, base, trace):
    def tally_run(arguments, extra_env=None):
        return python(["-m", "tally", *arguments], workspace, extra_env)

    def is_json_error(output):
        try:
            return "error" in json.loads(output)
        except (ValueError, TypeError):
            return False

    words = "data/words.txt"
    merged = "blue 4\nred 4\ngreen 2\npink 1\nyellow 1\n"
    missing = tally_run(["top", "nope.txt"])
    missing_json = tally_run(["top", "nope.txt", "--format", "json"])
    old_flag = tally_run(["top", words, "--min", "2"])
    bad_limit = tally_run(["top", words, "--limit", "x"])
    bad_limit_json = tally_run(["top", words, "--limit", "x", "--format", "json"])
    merge_json = tally_run(["merge", words, "data/more.txt", "--format", "json"])
    try:
        merge_entries = json.loads(merge_json[1])
    except ValueError:
        merge_entries = None
    merge_missing = tally_run(["merge", words, "nope.txt"])
    usage = (read(Path(workspace) / "docs/usage.md") or "").lower()
    changelog = (read(Path(workspace) / "CHANGELOG.md") or "").lower()
    count_tests = lambda root: sum(text.count("def test_") for text in text_files(root, "tests").values())
    bare = [line for name, line in added_lines(workspace, base) if name.endswith(".py") and BARE_TODO.search(line)
            and not re.search(r"https?://", line)]
    vague = [name for name in new_files(workspace, base) if Path(name).stem.lower() in VAGUE_NAMES]
    return {
        # 1. the missing file
        "missing file: fails without a traceback and names the file": missing[0] not in (0, None) and "Traceback" not in missing[2] and "nope.txt" in missing[2],
        "missing file in json format: a JSON error on stdout": missing_json[0] not in (0, None) and is_json_error(missing_json[1]),
        # 2. formats
        "top writes csv": "red,4" in tally_run(["top", words, "--format", "csv"])[1],
        "export writes text": "red 4" in tally_run(["export", words, "--output", "text"])[1]
        or "red 4" in tally_run(["export", words, "--format", "text"])[1],
        "export --output json still works": tally_run(["export", words, "--output", "json"])[0] == 0,
        # 3. the rename
        "--at-least works": tally_run(["top", words, "--at-least", "3"])[1] == "red 4\n",
        "--min still works": old_flag[0] == 0 and old_flag[1] == "red 4\nblue 2\ngreen 2\n",
        "--min warns on stderr and names --at-least": old_flag[0] == 0 and "--at-least" in old_flag[2],
        "TALLY_AT_LEAST works": tally_run(["top", words], {"TALLY_AT_LEAST": "3"})[1] == "red 4\n",
        "TALLY_MIN still works": tally_run(["top", words], {"TALLY_MIN": "3"})[1] == "red 4\n",
        # 4. the limit
        "--limit 2 prints two entries": tally_run(["top", words, "--limit", "2"])[1] == "red 4\nblue 2\n",
        "TALLY_LIMIT works": tally_run(["top", words], {"TALLY_LIMIT": "1"})[1] == "red 4\n",
        "bad --limit: exit 2, no traceback": bad_limit[0] == 2 and "Traceback" not in bad_limit[2] and "unrecognized" not in bad_limit[2],
        "bad --limit in json format: a JSON error on stdout": bad_limit_json[0] == 2 and is_json_error(bad_limit_json[1]),
        # 5. merge
        "merge combines counts": tally_run(["merge", words, "data/more.txt"])[1] == merged,
        "merge honours --format json": isinstance(merge_entries, list) and len(merge_entries) == 5,
        "merge honours --limit and --at-least": tally_run(["merge", words, "data/more.txt", "--at-least", "2", "--limit", "2"])[1] == "blue 4\nred 4\n",
        "merge with a missing file: fails without a traceback and names the file": merge_missing[0] not in (0, None) and "Traceback" not in merge_missing[2] and "nope.txt" in merge_missing[2]
        and "invalid choice" not in merge_missing[2],
        # across the work
        "docs/usage.md covers merge, --limit, --at-least and csv": all(word in usage for word in ("merge", "--limit", "--at-least", "csv")),
        "docs mark --min deprecated": "deprecat" in usage,
        "CHANGELOG.md covers merge, limit, at-least, csv and the fix": all(word in changelog for word in ("merge", "limit", "at-least", "csv"))
        and bool(re.search(r"traceback|missing|not found|no such|unreadable|cannot be read|can't be read", changelog)),
        "suite passes with at least eight new tests": unit_tests_pass(workspace) and count_tests(workspace) - count_tests(base) >= 8,
        "at least five commits": len(commit_messages(workspace)) - 1 >= 5,
        "no TODO without a reference": not bare,
        "no new file with a vague name": not vague,
        "a missing file has its own documented exit code": missing[0] not in (0, 2, None) and "exit" in usage,
    }


CHECKS = {
    "release-batch": check_release_batch,
    "help-snapshot": check_help_snapshot,
    "bulk-rename": check_bulk_rename,
    "public-flag-rename": check_public_flag_rename,
    "todo-note": check_todo_note,
    "root-cause": check_root_cause,
    "lint-suppression": check_lint_suppression,
}


def build_base(case, into):
    target = Path(into) / case
    target.mkdir(parents=True)
    subprocess.run(["bash", str(EVALS / case / "fixture.sh")], cwd=target, check=True, capture_output=True)
    return target


def unseal(kept):
    for path in (kept, kept / "sealed"):
        if path.exists():
            os.chmod(path, stat.S_IRWXU)


def copy_workspace(kept, into):
    for candidate in (kept / "sealed/home/cwd", kept / "home/cwd"):
        if candidate.is_dir():
            return Path(shutil.copytree(candidate, into, symlinks=True, ignore=shutil.ignore_patterns("__pycache__")))
    return None


def grade(results):
    """results is a list of (label, path). A label of None keeps the file's own arm names."""
    rows = []
    with tempfile.TemporaryDirectory() as scratch:
        bases = {}
        for label, result_path in results:
            result = json.loads(Path(result_path).read_text())
            for case in result["cases"]:
                name = case["name"]
                if name not in CHECKS:
                    continue
                if name not in bases:
                    bases[name] = build_base(name, Path(scratch) / "base")
                base = bases[name]
                for arm, runs in case["arms"].items():
                    if label is not None and arm != "with":
                        continue
                    column = label or arm
                    for index, one in enumerate(runs):
                        row = {"case": name, "arm": column, "run": index, "suite_score": one.get("score"), "turns": one.get("turns")}
                        row["suite_graders"] = {g["name"]: g.get("passed") for g in one.get("graders", [])}
                        row["cost_usd"] = one.get("costUsd")
                        trace_path = one.get("tracePath")
                        if one.get("error") or not trace_path or not Path(trace_path).exists():
                            row["error"] = one.get("error") or "no kept trace; was the run made with --keep-temp?"
                            rows.append(row)
                            continue
                        kept = Path(trace_path).parent.parent
                        unseal(kept)
                        workspace = copy_workspace(kept, Path(scratch) / f"{name}-{column}-{index}")
                        trace = Trace(trace_path)
                        row["leaves_read"] = trace.leaves_read()
                        row["playbooks_read"] = trace.playbooks_read()
                        if workspace is None:
                            row["error"] = "no workspace in the kept directory"
                        else:
                            row["checks"] = {**CHECKS[name](workspace, base, trace), **check_commits(workspace)}
                        rows.append(row)
    return rows


def tally(rows, case, arm, pick):
    values = [pick(row) for row in rows if row["case"] == case and row["arm"] == arm and "error" not in row]
    values = [value for value in values if value is not None]
    return f"{sum(values)}/{len(values)}" if values else "n/a"


def markdown(rows):
    arms = list(dict.fromkeys(row["arm"] for row in rows))
    lines = []
    for case in CHECKS:
        graded = [row for row in rows if row["case"] == case and "checks" in row]
        if not graded:
            continue
        lines += [f"### {case}", "", "| Check | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
        for check in graded[0]["checks"]:
            cells = [tally(rows, case, arm, lambda row, check=check: row.get("checks", {}).get(check)) for arm in arms]
            lines.append(f"| {check} | " + " | ".join(cells) + " |")
        shares = []
        for arm in arms:
            runs = [list(row["checks"].values()) for row in graded if row["arm"] == arm]
            per_run = [sum(bool(value) for value in checks) / len(checks) for checks in runs]
            shares.append(f"{100 * sum(per_run) / len(per_run):.0f}%" if per_run else "n/a")
        lines.append("| **mean share of checks passed** | " + " | ".join(shares) + " |")
        for grader in graded[0].get("suite_graders", {}):
            cells = [tally(rows, case, arm, lambda row, grader=grader: row.get("suite_graders", {}).get(grader)) for arm in arms]
            lines.append(f"| suite grader: {grader} | " + " | ".join(cells) + " |")
        costs = []
        for arm in arms:
            spent = [row["cost_usd"] for row in rows if row["case"] == case and row["arm"] == arm and row.get("cost_usd")]
            costs.append(f"${sum(spent) / len(spent):.2f}" if spent else "n/a")
        lines.append("| mean cost per run | " + " | ".join(costs) + " |")
        for leaf in EXPECTED_LEAVES[case]:
            cells = [tally(rows, case, arm, lambda row, leaf=leaf: leaf in row.get("leaves_read", [])) for arm in arms]
            lines.append(f"| read `{leaf}` | " + " | ".join(cells) + " |")
        lines.append("")
    failed = [row for row in rows if "error" in row]
    if failed:
        lines += ["### Runs not graded", ""] + [f"- {row['case']} {row['arm']} {row['run']}: {row['error']}" for row in failed]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("results", nargs="+", metavar="ARM=RESULT.json")
    parser.add_argument("--markdown")
    parser.add_argument("--json")
    args = parser.parse_args()
    rows = grade([tuple(item.split("=", 1)) if "=" in item else (None, item) for item in args.results])
    table = markdown(rows)
    if args.markdown:
        Path(args.markdown).write_text(table)
    if args.json:
        Path(args.json).write_text(json.dumps(rows, indent=2) + "\n")
    sys.stdout.write(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
