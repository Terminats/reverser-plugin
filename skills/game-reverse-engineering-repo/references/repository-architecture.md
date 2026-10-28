# Repository architecture

## Adaptation boundary

Use this map only for capabilities needed by the target project. Derive executable format, CPU, ABI, graphics API, input ownership, and loading method from actual inputs. Do not transfer another project's hashes, RVAs, register assumptions, dimensions, file names, asset extensions, component dependencies, release history, or third-party wrappers. Define and validate schema contracts for the target project rather than copying a schema solely because another installer accepts its data.

## Directory ownership

The following is a full capability map. Create conditional branches only when the project needs them; existing projects can retain equivalent directory names.

```text
repository/
  README.md
  AGENTS.md
  .gitignore
  .editorconfig
  .gitattributes
  analysis/
    README.md
    YYYY-MM-DD-topic.md
  config/
    local.settings.example.json
    local.settings.json                 ignored
    known-builds.json
    patch-line.json                    when releases exist
    patch-manifest.schema.json         when packages exist
  docs/
    architecture.md                    when useful
  native/                              when native patches are needed
    CMakeLists.txt
    README.md
    include/<project>/
      api.hpp
      core/
      registry/
      patches/<topic>/
      experiments/
      monitoring/
      adapters/                        when game data crosses a service boundary
      render/                          when rendering is in scope
    src/
      dllmain.cpp                      for a Windows DLL
      exports.cpp
      core/
      registry/builtin_components.cpp
      patches/register_patches.cpp
      patches/<topic>/
      experiments/
      monitoring/
      adapters/
      render/
    launcher/                          when a launcher is needed
      main.cpp
      app/
      platform/
      process/
    tests/
    tools/
  scripts/
    lib/
    ghidra/                            reusable analysis scripts
    dev/                               maintained source-table generators
    experiments/                       one runner plus measurement helpers
  tests/                               repository/deployment synthetic tests
  patches/releases/                    immutable manifests, no payload binaries
  packaging/                           tracked public instructions and licenses
  work/
    README.md
    originals/<build-id>/              ignored
    ghidra/                            ignored project databases
    builds/                            ignored, separate production/diagnostics
    replacements/                      ignored staged modules or byte-patched copies
    game-copies/                       ignored isolated runnable copies
    experiments/runs/                  ignored run metadata
    vendor/                            ignored externally obtained dependencies
  output/
    README.md
    packages/                          ignored generated payloads
    distribution/                      ignored archives and checksum sidecars
    reports/                           ignored raw logs, captures, dumps
    backups/                           ignored recoverable file states
    tests/                             ignored generated fixtures
```

Track source, semantic RE notes, validated address/byte tables, schemas, release composition, public instructions, and license notices. Keep game executables, DLLs, saves, original assets, dumps, complete modified game files, analysis databases, local paths, generated binaries, logs, and payloads under ignored roots. Add the target game's actual asset extensions to its ignore rules after inventory; do not blanket-ignore JSON or source files that the project needs.

## Runtime responsibilities

| Module | Owns | Keep outside |
| --- | --- | --- |
| `core/` | Target identity, checked memory writes, hook primitives, settings, component lifecycle | Gameplay policy and fix-specific addresses |
| `registry/` | Composition of production and conditional development registrations | Patch behavior and launcher logic |
| `patches/<topic>/` | One accepted user-visible fix or feature, its adapters, checked sites, apply/revert | Unrelated fixes and periodic diagnostic logging |
| `experiments/` | Opt-in behavior under investigation, independently selectable implementations | Default production behavior |
| `monitoring/` | Probes, counters, shared-memory readers, periodic logs, development measurements | Public release binaries |
| `adapters/` | Conversion between confirmed game data and owned service inputs | Backend-specific rendering policy |
| `render/` or another domain service | Reusable data contracts, transforms, raster/GPU backends, resource lifetime | Game RVAs, native globals, proprietary object decoding |
| `launcher/app/` | CLI/public entry, startup sequencing, concise failure reporting | Fix implementation |
| `launcher/platform/` and `process/` | OS handles, process/module loading, ABI-aware remote operations | Gameplay and release composition |

Public headers mirror the source topic where needed. Keep implementation-only helpers private. An adapter can be header-only; the map does not require matching empty source directories.

Use dependency direction `entry -> registry -> components -> core/services`. A game adapter converts confirmed native data into a service contract. The reusable backend consumes that contract and never reaches back into game memory. Avoid mutual imports between peer patches; extract a shared service or state contract when two consumers actually need it.

For asynchronous services, publish owned snapshots with explicit lifetimes and generations; never send a borrowed pointer into mutable game storage to a worker. Separate world/camera data from screen overlays and resource identity from placement. Specify queue capacity/coalescing, thread ownership, shutdown order, and fallback before adding a worker. These are conditional renderer/service concerns, not scaffolding requirements for every repository.

## Tooling surface

Use stable generic entrypoints backed by one tools library. Adapt the names to the target platform and project; do not create every script before it has a job.

| Capability | Reference-style entrypoint | Contract |
| --- | --- | --- |
| Local configuration | `Set-LocalConfig` | Write only ignored machine settings; explicit arguments override them |
| Input identification | `Test-GameBuild` | Size/SHA-256 and format/CPU checks; unknown is not supported |
| Protected input copies | `Import-Originals` | Verify source and copy; preserve differing existing originals |
| Installation baseline | `New-GameBaseline`, `Compare-GameBaseline` | Snapshot before first deployment; compare when relevant |
| Native build | `Build-NativePatch` | Correct target ABI; separate production/diagnostic paths |
| Package assembly | `Build-CumulativePatch`, `New-ReplacementPackage` | Accepted components plus verified payload fingerprints |
| Package/source verification | `Build-And-VerifyPatch` | Verify immutable package and current build independently |
| Production copy | `Run-GamePatch` | Prepare verified isolated copy; offer verification without launching |
| Experiments | `experiments/Run-Experiment` | Latest accepted base plus local diagnostic build and selected IDs |
| Install and restore | `Install-Patch`, `Restore-Patch` | Default dry-run, verified backup, transactional file operations |
| Distribution | `Build-ReleaseArchive` | Public layout, concise install guide, notices, checksum sidecar |

An analysis-only repository usually starts with configuration, identification, protected import, and dated notes. Add a launcher, baseline, package line, and installer when the requested work needs them. Keep reproducible Ghidra table generators under `scripts/dev/`; check in reviewed output so ordinary builds do not depend on a running Ghidra session or a local analysis database.

## Sources of truth

`known-builds.json` identifies reviewed game inputs; local configuration locates them. The native registry defines what the compiled runtime can enable. `patch-line.json` defines accepted cumulative package composition, including file-only components. Release manifests bind one immutable version to actual payloads and supported before-states. Analysis notes and Ghidra describe the evidence behind those choices.

Check correspondence where these sources overlap. A registered experiment need not appear in a production release. A file-only package component need not be registered in the DLL. A new build is not a release until its manifest and acceptance are recorded. Treat retired components explicitly in history without keeping obsolete runtime switches forever.
