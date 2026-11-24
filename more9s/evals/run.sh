#!/usr/bin/env bash
# Run the eval suite in three arms at once, then run the hidden checks over all of them.
#
#   evals/run.sh [RESULT_PREFIX] [extra `claude plugin eval` arguments, such as --tag house]
#
# The arms:
#   full    the whole plugin, with /more9s:make-more9s as the first line of every prompt
#   router  the router and its playbooks and the hook, with no leaves and no other skills
#   none    an empty plugin, and the prompt as a user would type it
# Each arm is a copy of the plugin under .eval-variants/, run on its own with no
# built-in baseline, so every arm gets a prompt that fits it. Comparing full with
# router shows what the leaves add. Comparing router with none shows what the index adds.
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
prefix="${1:-$plugin_root/evals/results/latest}"
prefix="${prefix%.json}"
shift || true

export PATH=".evalbin:../.evalbin:../../.evalbin:$PATH"

# Each run builds its arms in a directory of its own, so two runs can go at once.
variants="$plugin_root/.eval-variants/$(basename "$prefix")"
rm -rf "$variants"
mkdir -p "$(dirname "$prefix")"

build_arm() {
  local arm="$1" target="$variants/$1"
  mkdir -p "$target/evals" "$target/skills"
  cp -R "$plugin_root/.claude-plugin" "$target/"
  case "$arm" in
    full)   cp -R "$plugin_root/skills/." "$target/skills/"; cp -R "$plugin_root/hooks" "$target/" ;;
    router) cp -R "$plugin_root/skills/make-more9s" "$target/skills/"; cp -R "$plugin_root/hooks" "$target/" ;;
    none)   ;;
  esac
  for case_file in "$plugin_root"/evals/*/case.yaml; do
    cp -R "$(dirname "$case_file")" "$target/evals/"
  done
  if [ "$arm" != "none" ]; then
    python3 - "$target/evals" <<'PY'
import sys
from pathlib import Path
for path in Path(sys.argv[1]).glob("*/case.yaml"):
    text = path.read_text()
    assert text.count("  prompt: |\n") == 1, path
    path.write_text(text.replace("  prompt: |\n", "  prompt: |\n    /more9s:make-more9s\n\n"))
PY
  fi
}

graded=()
for arm in full router none; do
  build_arm "$arm"
  graded+=("$arm=$prefix.$arm.json")
done
# The arms run at the same time. Each writes its own result file and log.
for arm in full router none; do
  (cd "$variants/$arm" && claude plugin eval . --ablation none --scaffold --trust-plugin --no-publish \
    --keep-temp -j 6 --allow-tools Bash Write Edit --json "$prefix.$arm.json" "$@" > "$prefix.$arm.log" 2>&1) || true &
done
wait

cd "$plugin_root"
python3 evals/grade.py "${graded[@]}" --markdown "$prefix.md" --json "$prefix.checks.json"
