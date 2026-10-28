# Deployment and validation

## Build and stage

- Keep pristine inputs immutable.
- Write generated replacements into a build/staging directory. Routine rebuilds may overwrite disposable generated artifacts; protect pristine inputs and user-authored files.
- Record output size and hash when packaging a persistent replacement, not after every rebuild of an isolated experiment.
- Separate package construction from installation so a patch can be inspected without touching the game.

## Install and rollback

- For a persistent replacement in the user's game installation, require an expected input build check; a known hash is the simplest choice. This is not required for an unchanged, already-verified isolated run.
- Ensure the target process is not holding the file.
- Preserve a recoverable original before replacement and report its location. A timestamped manifest or atomic replacement is useful for a reusable installer, but not mandatory for a one-off local trial.
- On partial failure, report the primary error and whether the original could be restored.

## Runtime validation

Prepare a copied installation or launcher-based isolated run when practical, then give the user the exact launch command. The user performs gameplay-dependent checks unless they explicitly request automated gameplay. Continue independent checks while results are pending; defer only work that depends on those results. Ask them to exercise the changed path and nearby transitions, including entering, leaving, repeating, and returning to menus or other modes. For visual/timing patches, collect telemetry through the separate diagnostic build when needed; keep the production build free of monitoring. Retain human acceptance checks for flicker, jitter, input behavior, audio/video continuity, and crashes.

A successful launch alone does not validate a patch. A negative result should either refine the experiment or reject it; do not silently accumulate incompatible prototypes.

## Promotion and code layout

- Promote only behavior accepted in the relevant runtime scenario. Move its implementation and public headers from `experiments/` to `patches/`; update build inputs, includes, production registration, component metadata, package artifacts, and launch scripts. Remove stale experiment registrations and switches. Keep a diagnostic experiment only when it has a separate ongoing use.
- Treat one user-visible fix with coordinated hooks as one production component. A small entry point may apply focused internal parts in order and undo completed parts in reverse order if startup fails. Retain hook restoration for failed initialization and clean shutdown even when users cannot toggle the production patch at runtime.
- Group a multi-file patch under its own `patches/<patch-name>/` source folder and matching public-header folder. Keep unrelated fixes in separate folders, with the central `register_patches` file limited to registration and dependencies. A single small patch may remain one file when a directory adds no clarity.
- After moving files, rebuild the native module and generated package, then verify the manifest against the staged binaries. A source-only refactor can still produce a different DLL hash.
