# Contributing

## How changes arrive

- **Fork, branch, pull request.** Nobody outside the maintainers pushes to this repository; every outside change is a
  pull request, reviewed and merged by a maintainer.
- **One concern per pull request.** Small and complete beats large and partial.

## Every change carries its reasons

A pull request that changes behaviour includes an architecture note in [`docs/architecture/`](docs/architecture/),
numbered in order (`0002-short-name.md`, and so on), and it says:

1. **What** changed, in plain words.
2. **Why** -- the problem, and the requirement it serves.
3. **What was turned down**, and why.
4. **What it rests on** -- each fact marked FACT (measured, with how) or GUESS (reasoned, not yet measured).
5. **How it is tested**, including a test that would fail if the change were wrong.

The code shows what was built. The note is how the next person learns why, and what not to undo.

## Tests

A test must bring its own world: it may not depend on files, caches or machines that only its author has. If a case
cannot run somewhere, it says SKIP and why, and it does not count as a pass.

## The contract

Changes to [`contract/`](contract/) follow its own rules, in [contract/README.md](contract/README.md).
