---
name: binary-patch-engineering
description: Use for native binary patch work, including designing fixes, promoting experiments, reorganizing patch code and folders, packaging releases, and validating byte patches, hooks, injected modules, launchers, or installers. Confirm the failing invariant before changing behavior; existing-patch maintenance and organization do not require new reverse engineering.
---

# Binary Patch Engineering

Turn a confirmed binary behavior into the smallest reversible change. Also use this skill when promoting or reorganizing an existing native patch without changing its behavior. Scale compatibility checks to the consequence of a mistake; isolated exploratory work does not need release-process ceremony.

- Use an opt-in experiment for instrumentation, unconfirmed behavior, timing trials, or changes still requiring visual/runtime acceptance.
- Promote a validated experiment by moving its implementation from `experiments/` to `patches/`, registering the production component, and retiring obsolete experiment registrations and switches. Keep independently useful diagnostics under `experiments/`. Remove retired experiment handling completely; do not accumulate per-experiment promotion messages, legacy-ID lists, or special rejection branches in runners. Use generic component validation and keep promotion history in analysis or release documentation.
- Group the parts of one user-visible fix as one patch component. For a patch with several files, use its own subfolder under both source and public-header `patches/` trees; keep unrelated patches in separate folders.
- Use a byte patch for a small, fixed instruction rewrite with no new runtime logic.
- Use a native module or hook when the change needs state, logging, new code, resource conversion, or multiple coordinated sites.
- Keep the launcher/orchestrator small; place patch logic in focused components grouped by patches, experiments, instrumentation, and reusable core helpers.
- Keep counters, probes, periodic logs, and their launcher reader in one dedicated development monitoring module. Exclude that module and its registration from production builds; retain only concise startup and failure diagnostics needed by users.
- Build diagnostic artifacts separately from production artifacts and check the packaged production binaries for monitoring symbols, mapping names, and periodic log strings.

Read [references/patch-design.md](references/patch-design.md) when choosing hook points or encoding instruction changes. Read [references/deployment-and-validation.md](references/deployment-and-validation.md) when promoting an experiment or packaging, installing, rolling back, or running a patch.

- For an offset-based hook, establish which build is loaded and check the original bytes at the actual write site. Do not rehash an unchanged, already-verified isolated game copy on every trial solely as a ritual.
- For a persistent file replacement in the user's game directory, verify the supported input build and preserve a recoverable original. A full-tree hash is not required for each local experiment.
- Prefer RVAs resolved from the loaded module base in runtime code.
- Apply changes transactionally; restore earlier writes and release resources if a later step fails.
- Preserve unrelated side effects around a hook. Bypassing a draw, parser, or timing wrapper is unsafe until its non-obvious state changes are understood.
- Keep experiments disabled by default and independently selectable.
- In diagnostic builds, log the build, enabled components, and measured behavior. In production, report concise startup or failure information, including a safe rejection reason, without periodic monitoring logs.

Keep iteration economical: confirm the proposed hook belongs to the observed behavior before coding; make one opt-in change per experiment; give one run command with a compact acceptance checklist; use a negative result to revise or discard the hypothesis before adding variants. Validate the build and relevant guard, then exercise the changed path and nearby transitions. Do not add ceremonial unit or integration tests that cannot meaningfully execute the proprietary host behavior.

For gameplay acceptance, prepare the exact command (or launch steps), actions, and observations for the user; launch or control the game only when explicitly requested. Complete independent non-interactive work while results are pending. Pause only conclusions and changes that depend on those results, and identify them in the handoff. A successful build or synthetic check does not establish gameplay acceptance.
