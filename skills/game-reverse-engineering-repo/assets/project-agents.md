# Project instructions

Adapt these instructions to the game's confirmed platform and the user's workflow before saving as `AGENTS.md`. Replace this introductory paragraph with the project's target and purpose.

- Treat the installed game as source material. Perform analysis and experiments on verified copies under `work/`; only the requested guarded deployment may modify the installation.
- Track source, build metadata, schemas, reviewed site tables, and semantic findings. Keep game files, saves, assets, dumps, Ghidra databases, generated binaries, payloads, backups, and machine paths in ignored local storage.
- Follow the user's or project's documentation language; default to English when neither specifies one. Each dated finding records build/module identity, reproduction, observed/expected behavior, VA/RVA/file-offset distinctions, evidence, confidence, and a discriminating next check. Separate facts, inferences, and hypotheses.
- Use Ghidra as the durable analysis database. Preserve existing documentation and synchronize confirmed names, types, signatures, and comments when the connection is available. Keep project locations and bridge details in ignored configuration.
- Establish CPU/bitness and ABI from the target binary. Make the build reject incompatible targets. Never reuse another game's fingerprints, addresses, byte guards, dimensions, or hook assumptions.
- Keep reusable mechanisms in `core/` or services, production behavior in focused `patches/<topic>/`, opt-in trials in `experiments/`, and probes/periodic logs in `monitoring/`. Keep game decoding and addresses outside reusable backends. Keep the launcher focused on startup and process operations.
- Exclude monitoring and experiment registration from production builds. Stage diagnostic and production binaries separately; reject diagnostic artifacts during production packaging.
- Verify build identity and bytes at actual patch sites. Apply transactionally; partially failing components clean up themselves and the manager reverts earlier successful components in reverse order.
- Keep runtime registrations, file-only package components, and accepted release composition consistent where they overlap. Preserve stable IDs; retire promoted experiment switches. Do not rewrite an immutable release when current source differs.
- Install and restore default to dry-run; explicit apply uses preflight fingerprints, confined literal paths, verified backups, a deployment journal, and recovery. Never weaken a guard to make an unsupported input pass.
- Run appropriate non-interactive checks and synthetic deployment tests. For gameplay acceptance, prepare the exact command, actions, and observations for the user; launch/control the game only when the user explicitly requests it. Continue independent work while results are pending; defer only work requiring the result. A build or synthetic benchmark does not establish gameplay acceptance.
