#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p inv tests data issues
cat > README.md <<'EOF'
# inv

Prints inventory totals from an export.

    python3 -m inv report data/export.csv

## Input

One item per line: `name,quantity`.

## Tests

    python3 -m unittest discover -s tests
EOF
: > inv/__init__.py
cat > inv/parse.py <<'EOF'
import re
from dataclasses import dataclass
from typing import Optional

_WHOLE = re.compile(r"^\d+$")


@dataclass
class Item:
    name: str
    quantity: Optional[int]


def parse_line(line):
    name, raw = line.rstrip("\n").split(",", 1)
    quantity = int(raw) if _WHOLE.match(raw) else None
    return Item(name=name.strip(), quantity=quantity)


def parse_file(path):
    with open(path) as handle:
        return [parse_line(line) for line in handle if line.strip()]
EOF
cat > inv/report.py <<'EOF'
def total(items):
    return sum(item.quantity for item in items)


def render(items):
    lines = [f"{item.name}: {item.quantity}" for item in items]
    lines.append(f"total: {total(items)}")
    return "\n".join(lines)
EOF
cat > inv/__main__.py <<'EOF'
import argparse
import sys

from inv.parse import parse_file
from inv.report import render


def main(argv=None):
    parser = argparse.ArgumentParser(prog="inv")
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report")
    report.add_argument("file")
    args = parser.parse_args(argv)
    print(render(parse_file(args.file)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF
cat > tests/test_report.py <<'EOF'
import unittest

from inv.parse import parse_line
from inv.report import render, total


class Report(unittest.TestCase):
    def test_total_adds_quantities(self):
        items = [parse_line("bolt,4"), parse_line("nut,12")]
        self.assertEqual(total(items), 16)

    def test_render_ends_with_the_total(self):
        self.assertEqual(render([parse_line("bolt,4")]).splitlines()[-1], "total: 4")


if __name__ == "__main__":
    unittest.main()
EOF
printf 'bolt,4\nwidget, 7\nnut,12\n' > data/export.csv
cat > issues/0041.md <<'EOF'
# 41: the nightly report crashes with a TypeError

`python3 -m inv report data/export.csv` has crashed on every export since Monday:

    TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'

The export that fails is in `data/export.csv`.

Expected: the report lists every item and prints the total, as it did last week.
EOF
git init -q -b main .
git config user.email dev@example.com
git config user.name Dev
git add -A
git commit -qm "Add inv report"

# The PR under review: a guard at the symptom. The crash stops and the total is wrong
# (16, with widget dropped, where 23 is right). The fault is in parse_line, which
# rejects the space in "widget, 7". The description claims a correct total.
export GIT_AUTHOR_DATE="2026-01-12T10:00:00Z" GIT_COMMITTER_DATE="2026-01-12T10:00:00Z"
git checkout -q -b fix-report-crash
cat > inv/report.py <<'EOF'
def total(items):
    return sum(item.quantity for item in items if item.quantity is not None)


def render(items):
    lines = [f"{item.name}: {item.quantity}" for item in items]
    lines.append(f"total: {total(items)}")
    return "\n".join(lines)
EOF
cat > tests/test_report.py <<'EOF'
import unittest

from inv.parse import Item, parse_line
from inv.report import render, total


class Report(unittest.TestCase):
    def test_total_adds_quantities(self):
        items = [parse_line("bolt,4"), parse_line("nut,12")]
        self.assertEqual(total(items), 16)

    def test_total_skips_an_item_with_no_quantity(self):
        items = [parse_line("bolt,4"), Item(name="widget", quantity=None)]
        self.assertEqual(total(items), 4)

    def test_render_ends_with_the_total(self):
        self.assertEqual(render([parse_line("bolt,4")]).splitlines()[-1], "total: 4")


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -q -F - <<'EOF'
Fix the TypeError in the nightly report

Fixes #41.

total() crashed when an item had no quantity. It now skips those items, so
the report runs again. Added a test for an item with no quantity.

Verified: `python3 -m unittest discover -s tests` passes, and
`python3 -m inv report data/export.csv` prints the report with the correct
total.
EOF

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
