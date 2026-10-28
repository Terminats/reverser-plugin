# Runtime and release contracts

Use these contracts when the requested repository includes runtime patching or distribution. Choose implementations for the actual target ABI; a five-byte x86 relative branch is not a general hook algorithm.

## Build identity and checked changes

- A supported build records a stable ID, module relative paths, size, SHA-256, and confirmed format/architecture. Hash normalization must not make comparison case-sensitive. Keep unknown inputs out of supported catalogs until reviewed.
- Store runtime sites as module identity plus RVA and original bytes; resolve against the loaded module base. Keep VA, RVA, and file offsets distinct. For PE, `RVA = VA - image_base`; a file offset requires section mapping and may not exist for zero-filled memory.
- At every write site, verify expected bytes and bounds. For executable rewrites, cover whole instructions, displacement ranges, calling convention, overwritten effects, register/flag/stack preservation, trampoline relocation, page protection, and instruction-cache synchronization as applicable.
- Verify an analyzed input at the boundary where it becomes runnable or deployable. Continue checking actual hook bytes, but do not repeatedly hash an unchanged verified copy or a complete installation on every local trial without a reason.
- Keep loader callbacks minimal. On Windows, apply hooks and start/stop services outside `DllMain` and loader lock. Remote loading must respect loader readiness and target ABI; a launcher must reject unsupported inputs and failed initialization before allowing gameplay to proceed.

## Component lifecycle

The reference registration contract contains `id`, `introduced_version`, `kind`, dependency IDs, `default_enabled`, `apply`, and `revert`. Kinds are `core`, `fix`, `feature`, `instrumentation`, and `experiment`; stable IDs use prefixes such as `fix.<topic>`.

1. Register unique component IDs before configuration/initialization. Reject invalid metadata and unknown selection IDs.
2. Configure enabled state before applying hooks. Distinguish selected/enabled from successfully applied; callbacks may run during installation.
3. Validate that all enabled dependencies exist and are enabled. Apply in dependency order; reject missing dependencies and cycles.
4. Record successful applications. On failure, revert earlier components in reverse order. **A component that partially fails inside `apply` must undo its own writes/resources before returning failure**; it has not yet entered the manager's applied list.
5. Shutdown reverts successful applications in reverse order. Document idempotence and any restriction on changing enabled state after initialization.

Experiments and probes default to disabled. Production and diagnostics have distinct build directories and staged artifacts. Exclude monitoring source and registration at build time, rather than relying only on a runtime flag. The production packager must reject diagnostic modules even when using previously staged binaries.

Use the registry to validate component selections generically. Running an experiment should require its implementation, build registration, and one selection ID, without manufacturing a production release. Base it on an isolated accepted game copy plus a local diagnostic build. Store run ID, input fingerprints, package version, local module fingerprints, selected IDs, configuration, and relevant log paths under ignored `work/experiments/runs/`.

Promotion requires evidence and the requested acceptance, not merely a passing synthetic test. Move accepted behavior into its production patch directory and registry, declare dependencies and release membership, and retire its experimental ID and switches. Keep probes independently useful. Preserve visual, input, simulation, and native side-effect contracts around replaced behavior.

## Data models

Use one documented schema per data model. Schema versions belong to their own models; preserve an existing project's versions and contracts unless migration is requested. For a new repository, choose versions consistently across generators and consumers; do not inherit version numbers from another project.

| Model | Required meaning |
| --- | --- |
| Known builds | Reviewed build IDs with module paths and actual size/SHA-256; no wildcard supported hashes |
| Patch line | Stable line ID, supported target(s), component kinds/status/dependencies/defaults/artifact provenance, cumulative releases |
| Release manifest | Schema version, package ID, patch line, version, target build, ordered component IDs, managed files |
| Managed file | Destination relative path, payload relative path, explicit `acceptedBefore` states, exact `expectedAfter` fingerprint |
| Before-state | Either `{ "state": "absent" }` or `{ "state": "file", "size": ..., "sha256": ... }` |
| After fingerprint | Nonnegative exact size and a 64-digit SHA-256 of the actual payload |
| Deployment journal | Package identity, actual selected before-state, backup location, after fingerprint, and completion/recovery state |

A package may derive add versus replace from the recognized current state; adapt the operation names to the project's schema. Keep accepted absent/clean/prior-release states explicit; do not accept arbitrary installed files just because the release number looks compatible. A fresh repository with no accepted components has no deployable release manifest yet.

Validate both syntax and semantics: all `$ref` targets resolve; IDs and destinations are unique; dependencies exist and are acyclic; supported build IDs resolve; paths remain within roots; SHA-256/size fields are well formed; payload bytes match; release components match intended composition. A JSON parse alone establishes none of those relationships.

## Installation and restore

- Default to dry-run. `-Apply` or an equivalent explicit operation performs deployment only within the user's requested scope. Prepare and verify local artifacts without adding a separate confirmation ritual to routine reversible work.
- Preflight every payload and destination before mutating any game file. Reject unsupported current states, missing/corrupt payloads, directories where files are expected, duplicate destinations, and unsafe paths.
- Resolve relative paths within explicit installation, package, and backup roots. Reject absolute paths, traversal, alternate data streams, and wildcards; account for symlinks/reparse points when present. Use literal path operations.
- Before overwriting, copy and verify the actual before-state into a recoverable backup. Journal additions as originally absent. Stage and verify replacement bytes before committing each write; verify after-state afterward.
- If applying a later file fails, restore earlier changes and remove only files created by that transaction whose current contents still match its after-state. Report incomplete recovery with the journal and backup location.
- Restore only when the current files match the recorded installed after-state and the original backups verify. Preserve a safety snapshot, restore replacements, and remove guarded additions. A failed restore must attempt recovery to its pre-restore state and report any incomplete recovery.
- Release assembly is immutable: an existing version with different payloads requires another version, not silently rewriting its manifest. Keep current-source verification distinct from released-package verification.

Test the implemented pipeline with synthetic bytes: clean installation, compatible upgrade, unknown-build/payload rejection without writes, dry-run preservation, added-file restoration, multi-step restore, tampered destination/backup rejection, unsafe path rejection, and recovery from a meaningful induced failure. Cover only capabilities actually implemented.

Public archives contain the intended game-directory layout, a concise install guide, necessary third-party notices/licenses, and checksum output. Keep internal dumps, databases, backups, experiment logs, and diagnostic binaries out. Verify dependency provenance; do not copy the reference's wrappers or shader choices unless they are appropriate for the target project.
