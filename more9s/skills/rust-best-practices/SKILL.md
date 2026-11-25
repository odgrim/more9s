---
name: rust-best-practices
description: "Shows how to meet the more9s standards in Rust. Use when reading or editing a .rs file or a Cargo.toml."
paths: ["**/*.rs", "**/Cargo.toml"]
disable-model-invocation: true
---

# Rust Best Practices

The standards hold the rules. This file holds the Rust for them. The repo's own lint and toolchain settings win where they differ, as `make-more9s` says for existing repos.

## Toolchain and lint

- Pin the toolchain in `rust-toolchain.toml`, and set `rust-version` in the manifest.
- Keep lints in `[workspace.lints]`, with `lints.workspace = true` in each package. Give a lint group `priority = -1` so a single lint can override it.
- Run clippy in CI with warnings denied, on the same toolchain as the build.
- Pick lints one at a time from clippy's `restriction` group. Never turn the group on. Worth having: `unwrap_used`, `expect_used`, `panic`, `indexing_slicing`, `dbg_macro`, `todo`, `undocumented_unsafe_blocks`, `print_stdout`, and `allow_attributes`.
- Silence a lint with `#[expect(lint, reason = "...")]`, not `#[allow]`. It fails once the lint stops firing, so it can't outlive its cause.

## Errors (`errors-are-typed-values`)

- Return `Result` for a failure a caller can meet. Panic only for a bug.
- In a library, define an error enum with one variant per failure a caller handles differently, and mark it `#[non_exhaustive]` from the first release. Adding a variant later is otherwise a breaking change.
- Keep the source with `#[source]` or `#[from]`. Write `Display` in lower case with no closing full stop.
- In a binary, `anyhow` or `eyre` with `.context()` is fine. Never put either in a library's public API.
- No `unwrap` outside tests. Use `expect` only for an invariant you can state, and state it in the message: "the regex is a literal and should compile".
- Return `ExitCode` from `main`. `process::exit` skips destructors.

## Types (`type-system-discipline`, `sets-are-closed-or-open`)

- Give a semantic primitive a newtype with private fields and one constructor that validates.
- Take an enum where a `bool` or an `Option` argument would need a comment to read at the call site.
- Match your own enums with every variant written out and no `_` arm, so a new variant fails the build. A foreign `#[non_exhaustive]` enum needs the `_` arm: handle it as the unknown case.
- Implement `From` and `TryFrom`, never `Into` or `TryInto`.
- Derive `Debug` on every public type, and the other common traits where they make sense. A downstream crate can't add them.
- Seal a public trait you'll need to add methods to.

## Signatures (`indirection-earns-its-place`, `explicit-plumbing`)

- Borrow in a parameter (`&str`, `&[T]`, `impl AsRef<Path>`) unless the function keeps the value. If it keeps it, take ownership. Don't borrow and clone.
- Use generics when every caller passes one type, and `dyn` when a collection holds several.
- A `clone` added to satisfy the borrow checker is a question about ownership. Answer it before you leave it in.
- Reach for a channel or an atomic before `Arc<Mutex<T>>`.
- Use `LazyLock` and `OnceLock` from the standard library, not a crate, for one-time initialisation. A global built this way is still ambient state.

## Async (`bound-every-resource`, `confine` in `one-owner-per-boundary`)

- Never hold a `std::sync::Mutex` guard across an `.await`. Scope the guard, or lock inside a method that isn't async.
- Don't block the executor. Send blocking I/O to `spawn_blocking` and CPU work to a thread pool. A `spawn_blocking` task can't be cancelled.
- In `select!`, every losing branch is dropped. Use it only with futures that are safe to cancel, and pin a future you reuse outside the loop.
- Own spawned tasks with a `JoinSet`, so dropping it stops them. Shut down with a cancellation token the tasks watch.
- A public trait's `async fn` can't gain a `Send` bound later. Decide it at the first release.

## Effects and child processes (`explicit-plumbing`, `one-owner-per-boundary`)

- Ban the direct call outside its owner with `disallowed-methods` in `clippy.toml`: `std::env::var`, `std::env::set_current_dir`, `std::process::Command::new`, `std::time::SystemTime::now`.
- Never call `set_current_dir`. Pass the path, and give a child its directory with `Command::current_dir`.
- A child inherits the parent's environment. Set or remove every variable that changes what it does, such as `GIT_DIR`, and set `LC_ALL=C` when you parse its output.
- Give a child `Stdio::null()` for stdin so it can't prompt, and a timeout that kills it if it can wait on the network. With tokio, set `kill_on_drop(true)` and wrap `wait` in `timeout`.
- Keep a child's output and a path as bytes (`&[u8]`, `OsStr`, `Path`) until they must be text. `String::from_utf8` turns valid non-UTF-8 output into an error.
- Bound recursion over input you don't control with a depth count. A stack overflow aborts the process and can't be caught.

## Unsafe (`one-owner-per-boundary`)

- Keep `unsafe` in one small module whose public API is safe. Module privacy is the only thing that contains it.
- Write `// SAFETY:` above every block, saying why the requirements hold, and a `# Safety` section on every `unsafe fn`.
- Run the module's tests under Miri. A pass isn't proof.

## Cargo (`public-interfaces-grow-by-addition`, `vet-new-dependencies`)

- Features only add. Two that can't be on together need a `compile_error!`. Removing a feature, including from `default`, is a breaking change.
- Put new code behind `pub(crate)` until something outside the crate needs it.
- Before a release, run `cargo publish --dry-run` and `cargo semver-checks`. A published version can't be removed.
- Never edit `Cargo.lock` by hand. Change it with `cargo add` or `cargo update -p`.

## Logging, CLI, docs

- A library logs through `tracing` and never installs a subscriber. Only the binary does. No `println!` in a library.
- Define CLI flags with clap's derive, and give each one its environment variable with `#[arg(env)]`.
- A public item that can fail, panic, or needs care has a `# Errors`, `# Panics`, or `# Safety` section. Examples use `?`, not `unwrap`.

## Tests

- Unit tests sit in `#[cfg(test)] mod tests` beside the code. Tests of the public API sit in `tests/`.
- Keep `main.rs` thin over a `lib.rs`, so the logic can be tested.
- No snapshot crate for assertions, as `no-golden-files` says.
- Fuzz a parser or sanitiser of untrusted input with `cargo fuzz`, and give it empty, truncated, and non-UTF-8 cases.
- Test code that can run concurrently by running it concurrently, with `std::thread::scope` or a `JoinSet`.
- Take a limit or timeout as a parameter, so a test trips it with a small value and doesn't wait out the real one.

## Check

- Do `cargo clippy` with warnings denied and `cargo test` pass with no new `#[allow]` or `#[expect]`?
- Grep the diff for `unwrap()`, `unsafe`, `.clone()`, and `_ =>`. Can you give the reason for each hit?
