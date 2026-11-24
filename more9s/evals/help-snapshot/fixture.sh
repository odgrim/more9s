#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p tally docs tests data
cat > README.md <<'EOF'
# tally

Counts words in a file.

    python3 -m tally top data/words.txt
    python3 -m tally export data/words.txt --output csv

## Tests

    python3 -m unittest discover -s tests
EOF
cat > docs/usage.md <<'EOF'
# Usage

## tally top FILE

Prints each word and its count, most frequent first.

| Option | Environment | Default | Meaning |
|---|---|---|---|
| `--min N` | `TALLY_MIN` | `1` | Leave out words seen fewer than N times |
| `--format text\|json` | `TALLY_FORMAT` | `text` | Output format |

## tally export FILE

Writes every word and its count.

| Option | Environment | Default | Meaning |
|---|---|---|---|
| `--output json\|csv` | `TALLY_OUTPUT` | `json` | File format written to stdout |
EOF
cat > CHANGELOG.md <<'EOF'
# Changelog

## Unreleased

### Added

- `--min` option on `tally top`.
EOF
cat > pyproject.toml <<'EOF'
[project]
name = "tally"
version = "0.3.0"
requires-python = ">=3.9"
dependencies = []
EOF
: > tally/__init__.py
cat > tally/cli.py <<'EOF'
import argparse
import json
import os
import sys
from collections import Counter


class UsageError(Exception):
    pass


def whole_number(text, name):
    try:
        value = int(text)
    except ValueError:
        raise UsageError(f"{name} must be a whole number, got {text!r}") from None
    if value < 0:
        raise UsageError(f"{name} must not be negative, got {value}")
    return value


def choice(text, name, allowed):
    if text not in allowed:
        raise UsageError(f"{name} must be one of {', '.join(allowed)}, got {text!r}")
    return text


def setting(flag_value, environ, variable, default):
    if flag_value is not None:
        return flag_value
    return environ.get(variable, default)


def count_words(path):
    with open(path) as handle:
        counts = Counter(handle.read().split())
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def run_top(args, environ, out):
    minimum = whole_number(setting(args.min, environ, "TALLY_MIN", "1"), "--min")
    entries = [(word, count) for word, count in count_words(args.file) if count >= minimum]
    if args.format == "json":
        out.write(json.dumps([{"word": word, "count": count} for word, count in entries]) + "\n")
    else:
        for word, count in entries:
            out.write(f"{word} {count}\n")


def run_export(args, environ, out):
    output = choice(setting(args.output, environ, "TALLY_OUTPUT", "json"), "--output", ("json", "csv"))
    entries = count_words(args.file)
    if output == "json":
        out.write(json.dumps([{"word": word, "count": count} for word, count in entries]) + "\n")
    else:
        out.write("word,count\n")
        for word, count in entries:
            out.write(f"{word},{count}\n")


def build_parser():
    parser = argparse.ArgumentParser(prog="tally")
    commands = parser.add_subparsers(dest="command", required=True)
    top = commands.add_parser("top")
    top.add_argument("file")
    top.add_argument("--min")
    top.add_argument("--format")
    export = commands.add_parser("export")
    export.add_argument("file")
    export.add_argument("--output")
    return parser


def main(argv=None, environ=None, out=None, err=None):
    environ = os.environ if environ is None else environ
    out = sys.stdout if out is None else out
    err = sys.stderr if err is None else err
    args = build_parser().parse_args(argv)
    as_json = False
    try:
        if args.command == "top":
            args.format = choice(setting(args.format, environ, "TALLY_FORMAT", "text"), "--format", ("text", "json"))
            as_json = args.format == "json"
            run_top(args, environ, out)
        else:
            run_export(args, environ, out)
    except UsageError as error:
        if as_json:
            out.write(json.dumps({"error": str(error)}) + "\n")
        else:
            err.write(f"tally: {error}\n")
        return 2
    return 0
EOF
cat > tally/__main__.py <<'EOF'
import sys

from tally.cli import main

if __name__ == "__main__":
    sys.exit(main())
EOF
cat > tests/test_cli.py <<'EOF'
import io
import json
import os
import tempfile
import unittest

from tally.cli import main


def run(argv, environ=None):
    out, err = io.StringIO(), io.StringIO()
    code = main(argv, environ=environ or {}, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


class Top(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        handle.write("a b a c a b\n")
        handle.close()
        self.path = handle.name
        self.addCleanup(os.remove, self.path)

    def test_orders_by_count(self):
        self.assertEqual(run(["top", self.path])[1], "a 3\nb 2\nc 1\n")

    def test_min_flag_filters(self):
        self.assertEqual(run(["top", self.path, "--min", "2"])[1], "a 3\nb 2\n")

    def test_min_from_the_environment(self):
        self.assertEqual(run(["top", self.path], {"TALLY_MIN": "3"})[1], "a 3\n")

    def test_flag_wins_over_the_environment(self):
        self.assertEqual(run(["top", self.path, "--min", "2"], {"TALLY_MIN": "3"})[1], "a 3\nb 2\n")

    def test_usage_error_is_json_in_json_format(self):
        code, out, err = run(["top", self.path, "--format", "json", "--min", "x"])
        self.assertEqual(code, 2)
        self.assertIn("error", json.loads(out))
        self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()
EOF
printf 'red blue red green red blue\nyellow green red\n' > data/words.txt
git init -q -b main .
git config user.email dev@example.com
git config user.name Dev
git add -A
git commit -qm "Add tally"

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
