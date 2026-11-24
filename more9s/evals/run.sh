#!/usr/bin/env bash
# Run the eval suite with a git the eval sandbox can execute, then run the hidden checks.
#
#   evals/run.sh [RESULT.json] [extra `claude plugin eval` arguments...]
#
# On macOS, /usr/bin/git is a stand-in that asks Xcode where the real git is and
# caches the answer in a temp directory. The eval sandbox denies that write, so git
# fails for every agent. The sandbox also hides every path outside the workspace that
# a wrapper could live in: $HOME, other temp directories, the plugin's evals directory,
# and the real binary itself (it can execute it, but not stat it, so PATH lookup skips it).
# So each fixture.sh writes .evalbin/git inside the workspace, and this script puts the
# relative directory first on PATH. The extra entries cover a shell that has moved one
# or two directories down.
set -euo pipefail

plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
result="${1:-$plugin_root/evals/results/latest.json}"
shift || true

export PATH=".evalbin:../.evalbin:../../.evalbin:$PATH"

mkdir -p "$(dirname "$result")"
cd "$plugin_root"
claude plugin eval . --scaffold --trust-plugin --no-publish --keep-temp -j 4 \
  --allow-tools Bash Write Edit --json "$result" "$@" || true
python3 evals/grade.py "$result" --markdown "${result%.json}.md" --json "${result%.json}.checks.json"
