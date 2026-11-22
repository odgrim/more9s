#!/usr/bin/env python3
"""Run with: python3 -m unittest discover -s hooks -p 'test_*.py'"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

import check_written_text

HERE = Path(__file__).parent
HOOK = HERE / "check_written_text.py"
CASES = json.loads((HERE / "testdata" / "cases.json").read_text())


def run_hook(payload):
    return subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True
    )


class Problems(unittest.TestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(case["name"]):
                found = check_written_text.problems(
                    case["path"], case["text"], case.get("created", False)
                )
                self.assertEqual(len(found), len(case["want"]), found)
                for want, got in zip(case["want"], found):
                    self.assertIn(want, got)


class Hook(unittest.TestCase):
    def test_rejects_with_exit_code_two_and_names_the_line(self):
        bad = next(c for c in CASES if c["name"] == "bare nolint")
        result = run_hook({"tool_input": {"file_path": bad["path"], "new_string": bad["text"]}})
        self.assertEqual(result.returncode, 2)
        self.assertIn("a.go: added line 1", result.stderr)

    def test_path_rules_apply_only_to_a_created_file(self):
        tool_input = {"file_path": "pkg/utils.py", "content": "x = 1"}
        updated = run_hook({"tool_input": tool_input, "tool_response": {"type": "update"}})
        created = run_hook({"tool_input": tool_input, "tool_response": {"type": "create"}})
        self.assertEqual((updated.returncode, created.returncode), (0, 2))

    def test_accepts_its_own_source_and_tests(self):
        for path in (HOOK, Path(__file__)):
            with self.subTest(path.name):
                result = run_hook({"tool_input": {"file_path": str(path), "content": path.read_text()}})
                self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_ignores_input_that_is_not_json(self):
        result = subprocess.run([sys.executable, str(HOOK)], input="", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
