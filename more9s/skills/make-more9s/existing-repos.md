### Existing repos

Read this before you report a standard the repo doesn't meet, or add a structure the whole repo would have to adopt.

- Apply the standards to code you add. Retrofit existing code only when asked, or when a workaround forces a design fix.
- If the repo already has a way of doing the same thing and that way breaks a standard, meeting the standard in new code would add a second way. Use the existing way and name the unmet standard in the report. Introduce the standard's way when asked, through the replace-a-pattern playbook, so the old way is frozen.
- `secrets-and-untrusted-input` and `secure-by-default` are the exceptions. New code meets them whatever the repo does.
- If a standard needs a repo-wide structure the repo lacks (an owner module, a registry, a lint framework), it waits for a retrofit. Use the existing way and name the unmet standard in the report.
- If the repo already has a lint framework, a new rule in it isn't a retrofit. Add the rule when a value or standard calls for one.
- If a standard doesn't fit the language, say which and why in the report, and use the nearest thing that does.
- A standard that exists to keep many callers off one thing (an owner module with its fake, contract suite, and lint, a confined primitive, a registry, enforced import rules) applies once there's a second module or a second caller. A single-file script meets the rest: parsing at the boundary, typed errors, `secrets-and-untrusted-input`, `idempotent-operations`, and the CLI contract.
- Report an unmet standard once. The first report that names one proposes the entry for a `more9s deviations` section in the repo's agent instructions file: the standard, the existing way, and what a retrofit needs. Add the section when asked, as a docs-only change. Once it exists, cite it in one line and list only the deviations it doesn't hold.
