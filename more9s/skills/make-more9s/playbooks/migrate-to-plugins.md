### Migrate to plugins

Land these as one stack, as the [replace a pattern](./replace-a-pattern.md) playbook describes.

1. Derive every hand-kept list from one registry.
2. Extract the contract from two existing plugins.
3. Add the lint, with every current violation exempted by name. Its message names the registry and the contract.
4. Move per-plugin branches and fields out of shared code, then the remaining plugins one at a time. Each move removes its exemption.
