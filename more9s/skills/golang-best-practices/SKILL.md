---
name: golang-best-practices
description: "How to meet the more9s standards in Go. Use when reading or editing a .go file, go.mod, or a golangci-lint config."
paths: ["**/*.go", "**/go.mod", "**/.golangci*.yml"]
disable-model-invocation: true
---

# Go Best Practices

The standards hold the rules. This file holds the Go for them. The repo's own lint config and conventions win where they differ, as `make-more9s` says for existing repos.

## Toolchain and lint

- Pin Go and golangci-lint in `mise.toml`. The `go` line in `go.mod` is an enforced minimum, so it decides which language features below are available.
- Use golangci-lint's version 2 config. Beyond the standard set, turn on: `errorlint`, `exhaustive`, `gochecksumtype`, `nilerr`, `contextcheck`, `noctx`, `bodyclose`, `gocritic`, `unparam`, `modernize`, `depguard`, `forbidigo`, `paralleltest`, `tparallel`, `thelper`, `testifylint`, `testpackage`, `usetesting`, and `nolintlint`.
- Set `errcheck` to check blank assignments, and `nolintlint` to require the linter's name and an explanation.
- If the repo keeps a relaxed config and a strict one, a new package goes on the strict list and new lines pass the strict config.
- In CI, also run `go mod tidy` as a check, `go fix -diff`, the tests with `-race`, and `govulncheck ./...`.
- Never add `//nolint` to get past a finding. `fix-the-code-not-the-check` applies.

## Errors (`errors-are-typed-values`)

- Use the standard `errors` package. Give every failure a caller can meet a sentinel (`ErrNotFound`) or a type (`NotFoundError`, with a `NewNotFoundError` constructor when it carries fields). Export it and document it.
- Wrap with `fmt.Errorf("...: %w", err)`, with `%w` last. Add only what the error doesn't already say, and leave out "failed to".
- Match with `errors.Is` and `errors.As`, never `==`, a type assertion, or the text. Where the `go` line allows, `errors.AsType[E]` is the generic form.
- Return several with `errors.Join`.
- Handle an error once. Don't log it and return it.
- Declare the return as `error`, never a concrete pointer type. A typed nil isn't nil.
- Don't panic to report a failure, and don't recover outside the top of the process. Only `main` calls `os.Exit`, and one function decides the exit code.
- In tests, assert with `require.ErrorIs` or `require.ErrorAs`, not `ErrorContains`.
- Text a user reads can be a sentence. Other error strings are lower case with no closing punctuation.

## Plumbing (`explicit-plumbing`, `one-owner-per-boundary`)

- Signatures go `ctx context.Context`, then the logger, then the handle for the environment, then the rest.
- Don't store a context in a struct. Call `context.Background()` at the entry point only. Always call the cancel function.
- Pass the logger as a parameter. Don't fetch it from the context in new code, and don't keep one in a package variable.
- No mutable package-level state, and no `init()` with side effects.
- Reach the operating system through one injected value: files, environment, arguments, standard streams, subprocesses, HTTP, and `runtime.GOOS`. Forbid the direct calls (`os.ReadFile`, `os.Getenv`, `exec.Command`, `http.Get`) with `forbidigo`, with tests exempt. Terragrunt's `venv` is the model.
- Wrap each third-party library that does I/O in one `internal` package. Forbid its import everywhere else with a `depguard` rule whose message names the wrapper.
- Logs go to stderr and data to stdout.

## Packages and interfaces (`organize-by-dependency`, `indirection-earns-its-place`)

- Put commands under `cmd/` and everything else under `internal/`. Add a public package only when another module imports it.
- Imports run one way, from `main` down to the platform packages, with nothing importing upward.
- Name a package for what it holds, in one lower-case word. Don't create `util`, `helpers`, or `common`, and don't add to one that exists when a named package fits.
- Define an interface where it's consumed, keep it small, and wait until there are two implementations. Accept interfaces and return concrete types.
- Never type-assert one of your own interfaces down to its concrete type. The interface is missing a method.

## Types (`type-system-discipline`, `sets-are-closed-or-open`)

- A closed set is a named type with typed constants, and the `exhaustive` linter checks every switch over it. For variants that carry data, use an interface with an unexported method, checked by `gochecksumtype`.
- Give a semantic primitive its own named type.
- Make the zero value usable. Write a constructor only when it can't be.
- Take a config struct when most callers set options. Use functional options when most set none, or when an option can fail.
- Pass small structs by value. Take a pointer when the callee mutates the value or it's large, not to save a copy.
- Write generic code only when you'd otherwise write the same code twice.
- Use `slices`, `maps`, `cmp`, `min`, `max`, and iterators before a hand-written loop or a helper.

## Concurrency (`bound-every-resource`, `separate-shared-state`)

- Every goroutine has an owner that waits for it and a way to stop. Prefer a function that runs synchronously and lets the caller decide.
- Use `errgroup.WithContext`, with `SetLimit` for a bound, before hand-written coordination.
- Give a channel a size of zero or one, and a direction in the parameter type.
- Copy a slice or map you take or return across an API when the other side might change it.

## CLI (`cli-is-a-machine-contract`)

- Commands end in a verb. Flags start with a noun and share a stem per subsystem. A boolean flag accepts `true` and `false`, and negation uses `no-`.
- Every flag has an environment variable: the tool's prefix and the flag name in upper snake case. Precedence is flag, environment, config, default.
- A deprecated flag stays registered and hidden, and warns. A strict control turns the warning into an error.
- An experiment is a named constant with a status, switched on by name.

## Tests (`test-contracts-over-implementation`)

- Use testify: `require` on the test's goroutine, `assert` inside others.
- Put tests in the external `_test` package, so they use only the exported API. A test that has to live in the package goes in a file named `_internal_test.go`.
- Call `t.Parallel()` in every test and subtest, except one that uses `t.Setenv` or `t.Chdir`.
- Write table tests with named fields and a subtest per row. Call `t.Helper()` in helpers.
- Use `t.TempDir`, `t.Context`, and `testing/synctest` for time. Fuzz a parser.
- Gate a test that needs credentials or a network the way the repo does: a build tag with a matching name prefix, or a skip helper that reads an environment variable.
- Prefer an in-memory fake to a generated mock.

## Check

- Do `golangci-lint run` and `go test -race ./...` pass with no new `//nolint`?
- Grep the diff for `os.`, `exec.`, `panic(`, `context.Background()`, `_ =`, and package-level `var`. Can you give the reason for each hit?
