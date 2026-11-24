---
name: standard-secure-by-default
description: "Applies when code creates or configures a role, policy, token, file, port, or connection. Grants the least it needs and leaves every protection on."
disable-model-invocation: true
---

# Secure by Default

A wide grant works on the first try, so nothing prompts anyone to narrow it later.

- Grant a role, policy, or token the actions and resources the code uses, by name. No wildcard stands in for a list you didn't look up.
- Create a file that holds a secret readable by its owner only. Set the mode when you create it, not after.
- Bind a listener to loopback unless the requirement is to serve other hosts.
- Leave certificate verification, signature checks, and host-key checks on. If a test needs a certificate, give it one it can verify.
- Make the safe setting the default (encryption on, public access off) and the unsafe one an explicit, named option.
- A widened grant or a disabled protection is the reviewer's decision. List it in the report's decisions with the reason.

## Check

- Grep the diff for wildcards in grants and for options that disable verification. Is each hit in the report's decisions?
