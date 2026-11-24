#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p app/commands tests cache
cat > README.md <<'EOF'
# cachetool

    python3 -m app list
    python3 -m app purge
    python3 -m app warm
    python3 -m app verify
    python3 -m app stats

Config is read from `config.json`, or the file `APP_CONFIG` names.

## Tests

    python3 -m unittest discover -s tests
EOF
cat > config.json <<'EOF'
{"cache_dir": "cache", "retention_days": 30, "max_size_mb": 100}
EOF
: > app/__init__.py
: > app/commands/__init__.py
cat > app/legacy_config.py <<'EOF'
"""Process-wide config lookup."""
import json
import os

_LOADED = None


def get(key):
    global _LOADED
    if _LOADED is None:
        with open(os.environ.get("APP_CONFIG", "config.json")) as handle:
            _LOADED = json.load(handle)
    return _LOADED[key]
EOF
cat > app/commands/list.py <<'EOF'
import os

from app import legacy_config


def run():
    for name in sorted(os.listdir(legacy_config.get("cache_dir"))):
        print(name)
    return 0
EOF
cat > app/commands/purge.py <<'EOF'
import os

from app import legacy_config


def run():
    cache_dir = legacy_config.get("cache_dir")
    for name in os.listdir(cache_dir):
        os.remove(os.path.join(cache_dir, name))
    return 0
EOF
cat > app/commands/warm.py <<'EOF'
import os

from app import legacy_config


def run():
    cache_dir = legacy_config.get("cache_dir")
    os.makedirs(cache_dir, exist_ok=True)
    with open(os.path.join(cache_dir, "index"), "w") as handle:
        handle.write("warm\n")
    return 0
EOF
cat > app/commands/verify.py <<'EOF'
import os

from app import legacy_config


def run():
    limit = legacy_config.get("max_size_mb") * 1024 * 1024
    cache_dir = legacy_config.get("cache_dir")
    size = sum(os.path.getsize(os.path.join(cache_dir, name)) for name in os.listdir(cache_dir))
    print("ok" if size <= limit else "over")
    return 0 if size <= limit else 1
EOF
cat > app/commands/stats.py <<'EOF'
import os

from app import legacy_config


def run():
    cache_dir = legacy_config.get("cache_dir")
    names = os.listdir(cache_dir)
    size = sum(os.path.getsize(os.path.join(cache_dir, name)) for name in names)
    print(f"{len(names)} files, {size} bytes")
    return 0
EOF
cat > app/__main__.py <<'EOF'
import argparse
import sys

from app.commands import list as list_command
from app.commands import purge, stats, verify, warm

COMMANDS = {"list": list_command, "purge": purge, "warm": warm, "verify": verify, "stats": stats}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="app")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in COMMANDS:
        commands.add_parser(name)
    args = parser.parse_args(argv)
    return COMMANDS[args.command].run()


if __name__ == "__main__":
    sys.exit(main())
EOF
printf 'x\n' > cache/sample
git init -q -b main .
git config user.email dev@example.com
git config user.name Dev
git add -A
git commit -qm "Add cachetool"
export GIT_AUTHOR_DATE="2026-01-12T10:00:00Z" GIT_COMMITTER_DATE="2026-01-12T10:00:00Z"
cat > app/settings.py <<'EOF'
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    cache_dir: str
    retention_days: int
    max_size_mb: int


def load(path):
    with open(path) as handle:
        raw = json.load(handle)
    return Settings(
        cache_dir=raw["cache_dir"],
        retention_days=int(raw["retention_days"]),
        max_size_mb=int(raw["max_size_mb"]),
    )
EOF
cat > app/commands/stats.py <<'EOF'
import os


def run(settings):
    names = os.listdir(settings.cache_dir)
    size = sum(os.path.getsize(os.path.join(settings.cache_dir, name)) for name in names)
    print(f"{len(names)} files, {size} bytes")
    return 0
EOF
cat > app/__main__.py <<'EOF'
import argparse
import os
import sys

from app import settings
from app.commands import list as list_command
from app.commands import purge, stats, verify, warm

LEGACY = {"list": list_command, "purge": purge, "warm": warm, "verify": verify}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="app")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in [*LEGACY, "stats"]:
        commands.add_parser(name)
    args = parser.parse_args(argv)
    if args.command == "stats":
        return stats.run(settings.load(os.environ.get("APP_CONFIG", "config.json")))
    return LEGACY[args.command].run()


if __name__ == "__main__":
    sys.exit(main())
EOF
cat > tests/test_stats.py <<'EOF'
import contextlib
import io
import os
import tempfile
import unittest

from app.commands import stats
from app.settings import Settings


class Stats(unittest.TestCase):
    def test_counts_files_and_bytes(self):
        with tempfile.TemporaryDirectory() as cache_dir:
            with open(os.path.join(cache_dir, "a"), "w") as handle:
                handle.write("abc")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                stats.run(Settings(cache_dir=cache_dir, retention_days=30, max_size_mb=1))
            self.assertEqual(out.getvalue(), "1 files, 3 bytes\n")


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -qm "stats: take Settings from main instead of legacy_config.get

First command moved off the process-wide lookup, so it can be tested without a
config file on disk. list, purge, warm and verify follow."

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
