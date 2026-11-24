#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p app scripts tests .github/workflows
cat > README.md <<'EOF'
# exporter

    python3 -m app export
    python3 -m app audit
    python3 -m app report
    python3 -m app summary

Output is supposed to go through `app/output.py`, which decides the stream.

## Checks

    scripts/check.sh
EOF
cat > scripts/check.sh <<'EOF'
#!/usr/bin/env bash
# Everything CI runs. Run it locally before you push.
set -euo pipefail
python3 -m unittest discover -s tests
EOF
chmod +x scripts/check.sh
cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: scripts/check.sh
EOF
: > app/__init__.py
cat > app/output.py <<'EOF'
"""The one module that writes to the process's streams."""
import sys


def emit(line):
    sys.stdout.write(line + "\n")


def note(line):
    sys.stderr.write(line + "\n")
EOF
cat > app/rows.py <<'EOF'
ROWS = [
    {"id": 1, "name": "bolt", "owner": "ana"},
    {"id": 2, "name": "nut", "owner": "raj"},
    {"id": 3, "name": "washer", "owner": "ana"},
]
EOF
cat > app/summary.py <<'EOF'
from app.output import emit


def summary(rows):
    emit(f"{len(rows)} rows")
EOF
cat > app/export.py <<'EOF'
import sys


def export(rows):
    print("id,name")
    for row in rows:
        print(f"{row['id']},{row['name']}")
    print(f"exported {len(rows)} rows", file=sys.stderr)
EOF
cat > app/audit.py <<'EOF'
import sys


def audit(rows):
    owners = sorted({row["owner"] for row in rows})
    for owner in owners:
        count = sum(1 for row in rows if row["owner"] == owner)
        print(f"{owner}: {count}")
    if len(owners) < 2:
        print("warning: one owner holds everything", file=sys.stderr)
EOF
cat > app/report.py <<'EOF'
def report(rows):
    print("REPORT")
    print("------")
    for row in rows:
        print(f"{row['name']:<10}{row['owner']}")
EOF
cat > app/__main__.py <<'EOF'
import argparse
import sys

from app.audit import audit
from app.export import export
from app.report import report
from app.rows import ROWS
from app.summary import summary

COMMANDS = {"export": export, "audit": audit, "report": report, "summary": summary}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="app")
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args(argv)
    COMMANDS[args.command](ROWS)
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
git commit -qm "Add exporter"

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
