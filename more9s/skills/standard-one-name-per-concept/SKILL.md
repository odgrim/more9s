---
name: standard-one-name-per-concept
description: "Apply when naming or renaming anything: a type, function, variable, file, package, flag, config key, or log field. Each concept has one name used everywhere, and a search for that name finds every use."
disable-model-invocation: true
---

# One Name Per Concept

Readers navigate by search, so every concept needs exactly one name.

## Rules

- Use the same word for a concept in code, flags, config, logs, docs, and tests. Take the word users already use.
- One word means one thing.
- A flag, its environment variable, its config key, and its field differ only by casing and prefix.
- Write identifiers out in full, as literals a search can find, not built from string pieces.
- Avoid names so short or common that a search returns noise.
- Name a file or package for the one thing it holds. `util`, `common`, `helper`, `manager`, and `misc` name nothing. A hook rejects a new file with one of these names.
- A value passed everywhere has the same parameter name everywhere.
- An internal rename changes every use, docs and tests included, in one change. Leave no aliases.
- Renaming a public name (a flag, command, environment variable, config key, or output field) follows public-interface-changes. The old name is the one alias allowed.

## Check

- Does grepping for the name find every use of the concept and nothing else?
