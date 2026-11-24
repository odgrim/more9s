---
name: typescript-best-practices
description: "How to meet the more9s standards in TypeScript. Use when reading or editing a .ts or .tsx file."
paths: ["**/*.ts", "**/*.tsx"]
disable-model-invocation: true
---

# TypeScript Best Practices

The standards hold the rules. This file holds the TypeScript for them. The repo's own compiler and lint settings win where they differ, as `make-more9s` says for existing repos.

## Tools

For a new project, use the left column. In an existing repo, use what it already has, and name the difference in the report.

| Use this | Not this | Notes |
|---|---|---|
| **bun** | npm / yarn | All JS package management and script running |
| **just** | task / make | See `justfile` for recipes |
| **mise** | nvm | Tool versioning (`.mise.toml`) |
| **oxlint** | eslint | Linting |
| **oxfmt** | prettier | Formatting (`.oxfmtrc.json`) |
| **knip** | ts-prune | Unused files, exports and dependencies (`knip.json`) |
| **Effect** | raw promises | Services, layers, typed errors, streams |
| **React Compiler** | `useMemo` / `useCallback` | Memoizes components at build time (`scripts/vite-react.ts`); oxlint's `react-compiler` rules keep them compilable |

## Compiler and lint

- For a new package, turn on `strict`, `noUncheckedIndexedAccess`, `noImplicitOverride`, `verbatimModuleSyntax`, and `moduleDetection: force`.
- Set `module: nodenext` when `tsc` emits for Node, or `module: preserve` with `noEmit` under a bundler. Don't use `baseUrl` or the `node10` resolution. TypeScript 7 rejects both.
- Turn on `erasableSyntaxOnly`. It rules out enums, runtime namespaces, and parameter properties, so the code also runs under Node's type stripping.
- Lint with oxlint, with its type-aware rules on. Make sure a rule covers each of these: a promise nobody handles, an unsafe use of `any`, and a switch over a union that misses a case.
- Run knip in CI, so an unused file, export, or dependency fails the build.

## Types (`type-system-discipline`, `sets-are-closed-or-open`)

- Model variants as a union with a literal `kind` field. Don't use one object with optional fields that have to agree.
- Use a union of string literals, or an `as const` object, where another language would use an enum.
- Give a semantic primitive a branded type, and create it only in the function that validates it. Never create one with `as`.
- Use `unknown` for a value you haven't checked, never `any`.
- Don't use `as` or `!` on a value that hasn't been validated. Narrow it: a switch on the discriminant, then `in`, then `typeof` or `instanceof`, then a type guard that really checks its claim.
- Use `satisfies` to check a literal against a type without widening it.
- End a switch over a closed union with `default: { const unhandled: never = value; throw ... }`, so a new case fails the build.
- Mark a property `readonly` when nothing reassigns it, and take `readonly T[]` in a parameter you don't mutate.
- Derive a type from its source with `typeof`, `ReturnType`, `Pick`, or the schema's inferred type. Don't declare a second copy.
- Write the return type on an exported function.

## Boundaries (`one-owner-per-boundary`)

- Parse external data once, at the edge, with the schema library the repo already has, and take the type from the schema. Adding a schema library for one check is a new dependency, and `vet-new-dependencies` applies.
- A type guard is a claim the compiler can't check. Test it with a value that should fail.

## Errors (`errors-are-typed-values`)

- In Effect code, a failure a caller can handle goes in the error channel as a tagged error, not a thrown exception. Branch on its tag.
- Where code does throw, throw only `Error` and its subclasses. Give each failure a caller handles differently its own class or a literal `code` field, and branch on that, not on `message`.
- A caught value is `unknown`. Narrow it with `instanceof` before you read it.
- Wrap with `new SomeError(message, { cause })`, so the original stays reachable.

## Async (`explicit-plumbing`, `bound-every-resource`)

- Write async work as an Effect: dependencies as services provided through layers, failures in the error channel, and sequences as streams. Run it at the entry point only.
- The rest of this section is for code that still holds a raw promise, such as an edge or a callback.
- Every promise is awaited, returned, or handed to something that handles its rejection. A promise left on its own line loses its error.
- Inside a `try`, write `return await`, or the `catch` never sees the rejection.
- Take an `AbortSignal` in anything that does I/O, and pass it on.
- Don't start one promise per item of an unbounded list. Cap how many run at once.
- Release a resource with `using` or `await using` where the runtime supports it, and with `try`/`finally` where it doesn't.

## Modules (`organize-by-dependency`, `one-name-per-concept`)

- Use ES modules and named exports. A default export has no name a search can find.
- Import types with `import type`.
- Don't add a barrel file inside an application. It hides cycles and loads modules nobody asked for. A library's one entry point is the exception.
- Don't write a namespace, or a class that only holds static members. Export functions.

## React

- Don't write `useMemo` or `useCallback` by hand. The React Compiler memoizes at build time.
- Keep components compilable: fix what oxlint's `react-compiler` rules report, and don't suppress them.

## Tests and suppressions

- Don't mock what you can run.
- Test a type with `expectTypeOf` in a type-test file, not with a suppression that passes on any error.
- Never add `@ts-ignore` or `@ts-nocheck`. `@ts-expect-error` needs a description on the same line, and `fix-the-code-not-the-check` applies to it.

## Check

- Do `tsc --noEmit` and the lint pass with no new suppression?
- Grep the diff for `any`, ` as `, `!.`, and `@ts-`. Does each hit follow a validation, or appear in the report's decisions?
