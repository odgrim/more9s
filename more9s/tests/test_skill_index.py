#!/usr/bin/env python3
"""Check that the make-more9s index, the precedence tiers, and the leaves agree.

Run with: python3 -m unittest discover -s tests -p 'test_*.py'
"""
import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).parent.parent / "skills"
ROUTER_DIRECTORY = SKILLS / "make-more9s"
ROUTER = (ROUTER_DIRECTORY / "SKILL.md").read_text()
KINDS = ("value", "standard")

ENTRY = re.compile(r"^- \*\*(?P<title>[^*]+?)\.?\*\*(?: \(`(?P<name>[^`]+)`\))?", re.MULTILINE)
RELATIVE_LINK = re.compile(r"\]\((?P<target>\.[^)#]+)")
TIER = re.compile(r"^(?P<number>[45])\. (?P<text>.+)$", re.MULTILINE)
LEAF_NAME = re.compile(r"[a-z]+(?:-[a-z]+)+")


def section(heading):
    body = ROUTER.split(f"\n## {heading}\n", 1)[1]
    return body.split("\n## ", 1)[0]


def kebab(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def indexed(kind):
    heading = {"value": "Values", "standard": "Standards"}[kind]
    return {
        found.group("name") or f"{kind}-{kebab(found.group('title'))}"
        for found in ENTRY.finditer(section(heading))
    }


def leaves(kind):
    return {path.name for path in SKILLS.glob(f"{kind}-*") if path.is_dir()}


def frontmatter(path):
    block = path.read_text().split("---\n", 2)[1]
    return dict(line.split(": ", 1) for line in block.splitlines())


class Index(unittest.TestCase):
    def test_every_leaf_has_one_index_entry_and_every_entry_has_a_leaf(self):
        for kind in KINDS:
            with self.subTest(kind):
                self.assertEqual(indexed(kind), leaves(kind))

    def test_every_value_is_in_exactly_one_precedence_tier(self):
        titles = sorted(name.removeprefix("value-") for name in leaves("value"))
        tiers = {found.group("number"): found.group("text") for found in TIER.finditer(section("Precedence"))}
        for title in titles:
            with self.subTest(title):
                holding = [
                    number for number, text in tiers.items()
                    if title in LEAF_NAME.findall(text.split(":", 1)[1].split(".", 1)[0])
                ]
                self.assertEqual(len(holding), 1, holding)

    def test_every_playbook_is_listed_and_every_listed_playbook_exists(self):
        listed = {kebab(title.strip()) for title in section("Playbooks").strip().splitlines()[-1].rstrip(".").split(",")}
        on_disk = {path.stem for path in (ROUTER_DIRECTORY / "playbooks").glob("*.md")}
        self.assertEqual(listed, on_disk)


class Leaves(unittest.TestCase):
    def test_frontmatter_names_the_directory_and_keeps_the_leaf_out_of_model_invocation(self):
        for kind in KINDS:
            for name in sorted(leaves(kind)):
                with self.subTest(name):
                    fields = frontmatter(SKILLS / name / "SKILL.md")
                    self.assertEqual(fields["name"], name)
                    self.assertEqual(fields["disable-model-invocation"], "true")
                    self.assertTrue(fields["description"].startswith('"Apply '), fields["description"])

    def test_every_leaf_ends_in_a_check(self):
        for kind in KINDS:
            for name in sorted(leaves(kind)):
                with self.subTest(name):
                    self.assertIn("\n## Check\n", (SKILLS / name / "SKILL.md").read_text())

    def test_relative_links_resolve(self):
        for path in sorted(SKILLS.rglob("*.md")):
            for found in RELATIVE_LINK.finditer(path.read_text()):
                with self.subTest(f"{path.relative_to(SKILLS)} -> {found.group('target')}"):
                    self.assertTrue((path.parent / found.group("target")).exists())

    def test_a_leaf_named_in_prose_exists(self):
        titles = {name.split("-", 1)[1] for kind in KINDS for name in leaves(kind)}
        families = {title.split("-")[0] for title in titles}
        for path in sorted(SKILLS.rglob("*.md")):
            for candidate in set(LEAF_NAME.findall(path.read_text())):
                looks_like_a_leaf = candidate.count("-") >= 2 and candidate.split("-")[0] in families
                if looks_like_a_leaf and any(candidate in title or title in candidate for title in titles):
                    with self.subTest(f"{path.relative_to(SKILLS)}: {candidate}"):
                        self.assertTrue(
                            candidate in titles or candidate.split("-", 1)[1] in titles
                            or candidate in {path.stem for path in (ROUTER_DIRECTORY / "playbooks").glob("*.md")},
                            candidate,
                        )


if __name__ == "__main__":
    unittest.main()
