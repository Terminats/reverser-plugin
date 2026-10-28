---
name: readable-code
description: Write, refactor, or review source code for readable formatting, clear responsibility boundaries, and appropriate reuse. Apply during implementation and code cleanup; preserve project conventions and existing behavior during refactoring.
---

# Readable code

Make code easy to scan and change without hiding its dependencies. Follow existing
project conventions and explicit user choices. Keep changes within the requested
scope; a small edit does not require reorganizing the repository.

For review-only requests, report actionable findings without editing or formatting
files. Apply changes when implementation, cleanup, or refactoring is requested.

## Formatting for humans

- Separate logical phases and function/type definitions with one blank line. Group
  related fields and declarations; do not separate every assignment or statement.
  Keep a call with its immediate result or error check.
- Split dense lines containing several actions or nested branches. Use the project's
  formatter when available, then inspect logical spacing manually. Format touched
  code; avoid unrelated formatting changes and generated files.
- When choosing a new C++ style with no existing convention, prefer LLVM style,
  four-space indentation, a 100-column limit, expanded nonempty function bodies,
  expanded conditionals/loops, and at most one consecutive blank line.
- Remove comments that merely narrate statements. Retain explanations of invariants,
  ownership, non-obvious ordering, and failure handling. Preserve deliberate include
  order. Fewer lines do not justify hiding error handling or useful explanations.

## Responsibilities and reuse

- Split modules when responsibilities change independently, not to satisfy a file-size
  rule. Extract clear interfaces and explicit dependencies; moving code into textual
  includes while retaining implicit shared state does not establish a boundary.
- Make state ownership, mutation rules, and resource lifetimes explicit. Preserve
  synchronization when shared state is involved. Avoid a universal context that
  every module can freely mutate.
- Keep public interfaces and imports narrow. Place implementation dependencies where
  they are used; keep helpers and constants local unless another consumer needs them.
- Separate reusable logic from environment-specific I/O and lifecycle. Pass the data
  a calculation needs rather than making it discover unrelated application state.
- Extract duplicated behavior with the same contract, not merely similar syntax.
  Prefer a small cohesive helper over a generic framework with many switches.

## Refactoring and verification

- Inspect affected callers, imports, build targets, and tests before moving code.
  Update consumers and build configuration together. Preserve public contracts,
  defaults, side effects, failure behavior, and cleanup unless the task changes them.
- Verify changes through the project's actual build or import mechanism and relevant
  existing tests. Add regression tests for demonstrated failures or meaningful new
  boundaries; avoid tests that mirror implementation or only assert whitespace.
- Scale verification to the change. Repeat successful checks only after new changes,
  failures, or unresolved concerns. Keep conclusions that depend on pending runtime
  checks explicitly unverified.
- Review the diff for missing consumers, unnecessary exposed symbols, and unrelated
  churn. Report changes, checks actually run, and remaining verification limits.
