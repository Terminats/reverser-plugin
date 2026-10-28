---
name: game-reverse-engineering-repo
description: Create or scaffold a game reverse-engineering repository, or design and reorganize its architecture with evidence, isolated inputs, modular patches, experiments, monitoring, and guarded cumulative releases. Use for repository setup and structural work; use investigation or binary-patch skills for an individual investigation or fix.
---

# Game Reverse-Engineering Repository

Create a repository another engineer can use to identify a supported game build, preserve evidence, run isolated experiments, and develop reversible patches. Use the included architecture as a capability map; derive platform, addresses, formats, toolchain, and enabled capabilities from the target game and requested scope.

## Establish the project

- Inspect the destination, applicable `AGENTS.md`, Git status, existing configuration, and any user-provided reference repository before writing. Preserve unrelated work. Use an existing repository when appropriate; do not turn the reference project into the new target project accidentally.
- Infer the game, destination, and scope from the request. Ask only for missing information that affects a real decision. With no game binary available, complete the repository setup with an empty supported-build catalog and an explicit unverified target; do not invent fingerprints or block documentation on binary access.
- Choose the smallest useful scope: analysis and tooling, persistent byte patches, or a native runtime. A renderer, DLL injector, launcher, and release pipeline are conditional capabilities, not compulsory dependencies of every RE repository.
- If a live reference repository is supplied, inspect its implementation as well as its READMEs. Documentation can lag behind source. The included references are self-contained and do not require another project checkout.

Read [references/repository-architecture.md](references/repository-architecture.md) when choosing or changing directories and module boundaries. Read [references/runtime-and-release-contracts.md](references/runtime-and-release-contracts.md) when adding a native runtime, experiment runner, manifests, or deployment tools.

## Build the repository

For a creation request, create the actual files and working tools, not only a proposed tree. For an architecture-only request, provide the requested design without performing an unsolicited migration.

1. Create a root README explaining the target, supported/unverified builds, directory ownership, implemented commands, and the next evidence needed. Adapt [assets/project-agents.md](assets/project-agents.md) into the destination's `AGENTS.md`; preserve existing instructions during reorganization.
2. Adapt [assets/gitignore.template](assets/gitignore.template) and define line endings. Keep `work/README.md` and `output/README.md` tracked so the local artifact boundaries survive a clone. Introduce `docs/architecture.md` only when architecture detail warrants it; never link a nonexistent directory or command.
3. Write `analysis/README.md` as a guide to note naming, evidence locations, confidence labels, and an index of findings that actually exist. Use [assets/analysis-note.md](assets/analysis-note.md) only for individual dated investigation notes, not for the README. Keep confirmed findings, strong inferences, and open hypotheses separate. Follow the user's or target project's documentation language; default to English when neither specifies one.
4. Create an ignored local configuration and a tracked example. Keep machine paths and Ghidra connection details local. Implement working fingerprint and protected-import tools for the selected platform: explicit path overrides local settings; unknown builds are reported rather than added to the supported catalog automatically.
5. Read available module headers and record size/SHA-256, binary format, CPU/bitness, and relevant module identity. Import verified copies under `work/originals/<build-id>/` without silently replacing a different input. If inputs are missing, leave `builds: []` and make target-dependent commands fail clearly until a reviewed fingerprint exists.
6. Add only the runtime and release capabilities needed by the requested scope. For a native scaffold, make the selected toolchain configure/build a minimal module and manager; keep its component list empty until actual behavior is implemented. Reject target initialization when no build is supported. Never create successful no-op hooks or fake expected-byte tables to make verification pass.
7. Initialize local Git when creating a requested repository that has no repository already. Creating a remote, publishing, committing, and pushing require corresponding task authorization; repository scaffolding alone does not request those actions.

Implement scripts in the selected host environment. PowerShell and CMake are possible Windows choices; they are not requirements for a Linux game, managed game, asset-analysis project, or another user-selected environment. Keep one shared tools library instead of copying fingerprint and path logic into every script.

## Evolve an existing architecture

- Map current responsibilities to the reference boundaries, then migrate the smallest coherent part. Preserve component IDs, file fingerprints, public exports, supported inputs, and accepted behavior unless the task changes them.
- Group one user-visible fix under its own patch directory, even when it has several hook sites. Put genuinely reusable mechanisms in `core/` or a domain service; keep game-specific behavior out of the launcher and generic backend.
- Keep experiments opt-in and monitoring excluded from production at build time. An accepted experiment becomes a production component; remove its retired registration and runner switches while retaining independently useful instrumentation.
- Keep package composition separate from runtime registration: a wrapper, configuration, shader, or on-disk patch may be a package component with no DLL registration. Document that distinction instead of forcing false one-to-one correspondence.
- For a change that needs actual binary investigation, use `ghidra-re-investigation` if available. For hook design, patch implementation, promotion, and deployment, use `binary-patch-engineering` if available. This skill establishes the repository; those workflows supply evidence and implementation. Do not require either skill merely to scaffold files.

## Verify the result

Scale verification to the implemented capabilities. Check local links, parse JSON, check schema references and semantic validation, and ensure every documented command exists. Use synthetic files to check fingerprint mismatches, import preservation, and path confinement. For a native scaffold, build the correct architecture; for deployment tools, exercise dry-run, rejection, upgrades, and restoration on synthetic fixtures. Add tests for meaningful behavior, not copied wording or directory names.

Use `git check-ignore` with temporary synthetic game files, saves, dumps, local settings, and analysis databases to confirm artifact separation. Check the staged file list when one exists. Do not stage proprietary data to test the ignore rules.

For gameplay acceptance, prepare the exact command (or launch steps), actions, and observations for the user; launch or control the game only when explicitly requested. Complete independent non-interactive work while results are pending. Pause only conclusions and changes that depend on those results, and identify them in the handoff. A successful build or synthetic check does not establish gameplay acceptance.

Finish with the repository location, the boundaries implemented, checks actually run, and any unresolved target-specific facts. When source code and immutable release packages differ, report both states; do not silently overwrite a published version or imply that current source has been released.
