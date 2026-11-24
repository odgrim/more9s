---
name: standard-one-name-per-concept
description: "Apply when you're naming or renaming anything: a type, function, variable, file, package, flag, config key, log field. Give each concept one name used everywhere, so a search for it finds every use."
disable-model-invocation: true
---

# One Name Per Concept

Readers navigate by search.

- Use the same word for a concept in code, parameters, flags, config, logs, docs, and tests, and pick the word users already use. One word means one thing.
- A flag, its environment variable, its config key, and its field differ only by casing and prefix.
- Write identifiers out in full, as literals a search can find. Don't build them from string pieces or make them so short a search returns noise.
- Name a file or package for the one thing it holds. `util`, `common`, `helper`, `manager`, and `misc` name nothing, and the more9s hook flags a new file with one of those names.
- For an internal rename, change every use in one change, docs and tests included, and leave no alias. For a public rename, keep the old name as its only alias.

## Check

- Does grepping for the name find every use of the concept and nothing else?
