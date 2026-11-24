---
name: standard-secrets-and-untrusted-input
description: "Applies when code handles a credential or token, prints or logs a value it received, builds a command, path, or query from input, or writes a fixture, or when quoting output into a report. Keeps secrets out of output and stops input from becoming code."
disable-model-invocation: true
---

# Secrets and Untrusted Input

People read errors, logs, CI output, and fixtures, and systems that shouldn't hold a secret store them.

- Give a secret its own type, whose string and log forms print a fixed placeholder.
- When an error or log shows a received value, redact it if the field could hold a secret: a token, a password, a key, a URL with credentials, an environment dump.
- Read a secret from the environment or a secret store at the entry point. Never write one to a file in the repo, a command line, or a URL.
- Put no real credential, account ID, or customer data in fixtures or recorded responses.
- Treat input as data: subprocess arguments as a list, queries with parameters, paths resolved against an allowed root. If input selects code (a plugin name, a template, a module source), look it up in a registry or an allow-list.
- In the session, don't print the environment or open a credential file to debug. Redact output before you quote it into a report, a commit message, or an issue, and mark each redaction.

## Check

- Run the failure path with a fake secret in the input. Does grepping the output for it find nothing?
