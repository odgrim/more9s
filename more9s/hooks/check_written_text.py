#!/usr/bin/env python3
"""Reject text a Write or Edit just added when it breaks a more9s rule a pattern can catch.

Reads the PostToolUse payload on stdin. Checks only the added text, so
existing violations in a file do not fail an unrelated edit. Exit code 2
sends stderr back to the agent.
"""
import json
import re
import sys
from pathlib import PurePath

EM_DASH = "—"
PROSE_SUFFIXES = (".md", ".mdx", ".txt", ".rst")
DATA_SUFFIXES = (".json", ".lock", ".csv", ".tsv")
SNAPSHOT_SUFFIXES = (".snap", ".golden")
SNAPSHOT_DIRECTORY = "__snapshots__"
CHARACTERIZATION_DIRECTORY = "characterization"
VAGUE_NAMES = ("util", "utils", "common", "helper", "helpers", "manager", "misc")

COMMENT_START = r"(?:#|//|/\*|--|<!--)"
COMMENT = re.compile(COMMENT_START + r"(?P<text>.*)")
TODO = re.compile(r"\bTODO\b(?:\((?P<reference>[^)]*)\))?")
REFERENCE = re.compile(r"#\d+|[A-Z][A-Z0-9]+-\d+|lint:[\w./-]+")
URL = re.compile(r"https?://\S+")

SUPPRESSION = re.compile(
    r"(?P<marker>nolint|noqa|type:\s*ignore|eslint-disable(?:-next-line|-line)?"
    r"|@ts-ignore|@ts-expect-error|shellcheck disable|tfsec:ignore|checkov:skip|trivy:ignore)"
    r"(?P<rest>.*)"
)
UNNAMED_MARKERS = ("@ts-ignore", "@ts-expect-error")
ATTRIBUTE = re.compile(r"#!?\[(?:allow|expect)\((?P<rule>[^)]*)\)\](?P<rest>.*)")
RULE = re.compile(r"\s*[:=\[(]?\s*[\w@][\w,./@-]*[\])]?")
REASON = re.compile(r"[A-Za-z]{3,}")


def added_text(tool_input):
    return tool_input.get("content") or tool_input.get("new_string") or ""


def todo_problem(comment):
    found = TODO.search(comment)
    if not found or URL.search(comment):
        return None
    if REFERENCE.fullmatch(found.group("reference") or ""):
        return None
    return (
        "has a TODO with no tracking issue. Put the issue URL on the line, "
        "or the issue ID or lint rule in parentheses after the word."
    )


def suppression_problem(line, comment):
    attribute = ATTRIBUTE.search(line)
    if attribute:
        named, reason = bool(attribute.group("rule").strip()), attribute.group("rest")
    else:
        found = SUPPRESSION.search(comment)
        if not found:
            return None
        rest = found.group("rest")
        if found.group("marker") in UNNAMED_MARKERS:
            named, reason = True, rest
        else:
            rule = RULE.match(rest)
            named, reason = bool(rule), rest[rule.end():] if rule else ""
    if not named:
        return "has a suppression that names no specific check."
    if not REASON.search(reason):
        return "has a suppression with no reason on the same line."
    return None


def line_problems(path, text):
    suffix = PurePath(path).suffix.lower()
    if suffix in DATA_SUFFIXES:
        return []
    is_prose = suffix in PROSE_SUFFIXES
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        comment = COMMENT.search(line)
        comment_text = comment.group("text") if comment else ""
        problems = []
        if EM_DASH in (line if is_prose else comment_text):
            problems.append("has an em dash. Use a period, comma, or colon.")
        if not is_prose:
            problems.append(todo_problem(comment_text))
            problems.append(suppression_problem(line, comment_text))
        found.extend(f"{path}: added line {number} {p}" for p in problems if p)
    return found


def path_problems(path):
    pure = PurePath(path)
    found = []
    is_snapshot = pure.suffix.lower() in SNAPSHOT_SUFFIXES or SNAPSHOT_DIRECTORY in pure.parts
    if is_snapshot and CHARACTERIZATION_DIRECTORY not in pure.parts:
        found.append(
            f"{path}: new golden or snapshot file. Assert the values the "
            "requirement names, and validate machine output against its schema. "
            f"Refactor scaffolding goes in a {CHARACTERIZATION_DIRECTORY} directory."
        )
    if pure.stem.lower() in VAGUE_NAMES:
        found.append(f"{path}: the file name says nothing. Name it for the one thing it holds.")
    return found


def problems(path, text, created):
    return (path_problems(path) if created else []) + line_problems(path, text)


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = payload.get("tool_input") or {}
    response = payload.get("tool_response")
    created = isinstance(response, dict) and response.get("type") == "create"
    found = problems(tool_input.get("file_path", "<file>"), added_text(tool_input), created)
    if not found:
        return 0
    print("\n".join(found), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
