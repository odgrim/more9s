#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p app scripts tests .github/workflows
cat > README.md <<'EOF'
# exporter

    python3 -m app export            # rows as CSV on stdout
    python3 -m app export --progress # also a progress counter on stderr
    python3 -m app summary

## Checks

    python3 scripts/lint.py
    python3 -m unittest discover -s tests
EOF
cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/lint.py
      - run: python3 -m unittest discover -s tests
EOF
cat > scripts/lint.py <<'EOF'
#!/usr/bin/env python3
"""Fail when code under app/ calls print().

Output goes through app/output.py so there is one place that decides the stream.
A line ending in the marker below is exempt.
"""
import pathlib
import re
import sys

CALL = re.compile(r"\bprint\(")
MARKER = "# lint: allow-print"
OWNER = pathlib.Path("app/output.py")


def problems():
    for path in sorted(pathlib.Path("app").rglob("*.py")):
        if path == OWNER:
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if CALL.search(line) and not line.rstrip().endswith(MARKER):
                yield f"{path}:{number}: print() is forbidden here; send output through app.output (see app/output.py)"


def main():
    found = list(problems())
    for problem in found:
        print(problem)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
EOF
: > app/__init__.py
cat > app/output.py <<'EOF'
"""The one module that writes to the process's streams."""
import sys


def emit(line):
    sys.stdout.write(line + "\n")
EOF
cat > app/rows.py <<'EOF'
ROWS = [
    {"id": 1, "name": "bolt"},
    {"id": 2, "name": "nut"},
    {"id": 3, "name": "washer"},
]
EOF
cat > app/summary.py <<'EOF'
from app.output import emit


def summary(rows):
    emit(f"{len(rows)} rows")
EOF
cat > app/export.py <<'EOF'
import sys


def export(rows, progress=False):
    print("id,name")
    for index, row in enumerate(rows, 1):
        print(f"{row['id']},{row['name']}")
        if progress:
            print(f"\r{index}/{len(rows)}", end="", file=sys.stderr)
    if progress:
        print("", file=sys.stderr)
EOF
cat > app/__main__.py <<'EOF'
import argparse
import sys

from app.export import export
from app.rows import ROWS
from app.summary import summary


def main(argv=None):
    parser = argparse.ArgumentParser(prog="app")
    commands = parser.add_subparsers(dest="command", required=True)
    export_parser = commands.add_parser("export")
    export_parser.add_argument("--progress", action="store_true")
    commands.add_parser("summary")
    args = parser.parse_args(argv)
    if args.command == "export":
        export(ROWS, progress=args.progress)
    else:
        summary(ROWS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF
cat > tests/test_summary.py <<'EOF'
import contextlib
import io
import unittest

from app.rows import ROWS
from app.summary import summary


class Summary(unittest.TestCase):
    def test_counts_rows(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            summary(ROWS)
        self.assertEqual(out.getvalue(), "3 rows\n")


if __name__ == "__main__":
    unittest.main()
EOF
git init -q -b main .
git config user.email dev@example.com
git config user.name Dev
git add -A
git commit -qm "Add exporter with the print lint"

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
