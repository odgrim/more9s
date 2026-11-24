#!/usr/bin/env bash
set -euo pipefail
export GIT_AUTHOR_DATE="2026-01-05T10:00:00Z" GIT_COMMITTER_DATE="2026-01-05T10:00:00Z"
mkdir -p app/_metrics tests docs
cat > README.md <<'EOF'
# monitor

Internal service. Nothing under `app/` is imported from outside this repo.

    python3 -m unittest discover -s tests
EOF
: > app/__init__.py
cat > app/_metrics/__init__.py <<'EOF'
from app._metrics.core import calc

__all__ = ["calc"]
EOF
cat > app/_metrics/core.py <<'EOF'
def calc(values, window):
    """Mean of each run of `window` consecutive values."""
    return [sum(values[index:index + window]) / window for index in range(len(values) - window + 1)]
EOF
for name in cpu memory disk network latency errors queue cache; do
cat > "app/_metrics/$name.py" <<EOF
from app._metrics.core import calc

WINDOW = 3


def ${name}_trend(samples):
    """Smooth $name samples with calc before they are charted."""
    return calc(samples, WINDOW)
EOF
done
cat > docs/internals.md <<'EOF'
# Internals

Notes for people working on this repo. None of this is a public API.

## Smoothing

Every chart is smoothed by `calc(values, window)` in `app/_metrics/core.py`.
`calc` returns one mean per window, so a list of five samples and a window of three gives three points.
Each metric module (`cpu`, `memory`, `disk`, and the rest) calls `calc` with its own window.
EOF
cat > tests/test_core.py <<'EOF'
import unittest

from app._metrics import calc


class Calc(unittest.TestCase):
    def test_one_mean_per_window(self):
        self.assertEqual(calc([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0])

    def test_calc_of_a_short_list_is_empty(self):
        self.assertEqual(calc([1, 2], 3), [])


if __name__ == "__main__":
    unittest.main()
EOF
cat > tests/test_modules.py <<'EOF'
import unittest

from app._metrics import cache, cpu, disk, errors, latency, memory, network, queue


class Trends(unittest.TestCase):
    def test_every_module_smooths(self):
        samples = [3, 3, 3, 9]
        for module, name in [(cpu, "cpu"), (memory, "memory"), (disk, "disk"), (network, "network"),
                             (latency, "latency"), (errors, "errors"), (queue, "queue"), (cache, "cache")]:
            with self.subTest(name):
                self.assertEqual(getattr(module, f"{name}_trend")(samples), [3.0, 5.0])


if __name__ == "__main__":
    unittest.main()
EOF
git init -q -b main .
git config user.email dev@example.com
git config user.name Dev
git add -A
git commit -qm "Add monitor"

# The eval sandbox on macOS can't run /usr/bin/git, and can't see a git outside the
# workspace. evals/run.sh puts .evalbin first on PATH. See its header.
mkdir -p .evalbin
printf '#!/bin/sh\nexec "%s" "$@"\n' "$(xcrun -f git 2>/dev/null || command -v git)" > .evalbin/git
chmod +x .evalbin/git
echo .evalbin/ >> .git/info/exclude
