# RE Skills

Our skills for reverse engineering and writing readable code. Currently supports
**Codex**, with shared instructions kept separate from the agent adapter.

| Skill | Purpose |
| --- | --- |
| [game-reverse-engineering-repo](skills/game-reverse-engineering-repo/SKILL.md) | Create and organize game reverse-engineering repositories |
| [ghidra-re-investigation](skills/ghidra-re-investigation/SKILL.md) | Investigate binaries and document confirmed findings in Ghidra |
| [binary-patch-engineering](skills/binary-patch-engineering/SKILL.md) | Reversible patches, experiments, validation, and packaging |
| [readable-code](skills/readable-code/SKILL.md) | Formatting, module boundaries, reuse, and safe refactoring |

## Setup and build

Requirements: Python 3.11+ and Git. Tools work from any working directory; the
following commands assume you are at the repository root.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python scripts/re_skills.py validate
.venv/Scripts/python -m unittest discover -s tests -v
.venv/Scripts/python scripts/re_skills.py build --agent codex
```

On Linux/macOS, use `.venv/bin/python` instead of `.venv/Scripts/python`.

The build creates `dist/codex/`, containing the `re-skills/` plugin with its
`plugin.json` manifest, complete skills, and OpenAI metadata, plus a local plugin
catalog at `.agents/plugins/marketplace.json`. To rebuild, remove the previous
output or explicitly run `build --agent codex --replace`. Replacement affects only
that adapter's directory under `dist/`.

## Use with Codex

After building, add the generated marketplace:

```powershell
codex plugin marketplace add ./dist/codex
```

Restart the desktop app, select **re-skills-local** in the plugin directory, and
install **RE Skills**. Start a new chat. After source changes, rebuild the package,
refresh the marketplace and plugin installation, and start a new chat. The app
loads the installed copy, so editing the repository alone does not update an
active skill.

The package format and local marketplace registration are described in the
[official OpenAI documentation](https://developers.openai.com/plugins/build/plugins).
Building prepares files; it does not install the plugin or change agent settings.

Example invocation after installation:

```text
Use $ghidra-re-investigation to investigate the cause of this binary behavior
and record confirmed names, types, and comments in the Ghidra project.
```

The Ghidra skill requires a separate Ghidra installation and a compatible MCP
server providing instance discovery, program selection, analysis, and documentation
updates. This package contains instructions, not an MCP server. Connection addresses
and settings belong to the target project's local configuration.

## Development

- `skills/` - single source of instructions, references, and templates.
- `adapters/codex/` - package manifest and Codex UI metadata.
- `re-skills.json` - package identity, version, and published skill list.
- `scripts/` - shared validation, assembly, and adapter registry.
- `tests/` - packaging, resource preservation, and source protection tests.
- `dist/` - ignored build output.

All repository documentation, skill instructions, templates, code comments, and
user-facing metadata use English.

See [architecture](docs/architecture.md) for the adapter contract and how to add
another agent. See [skill import](docs/import.md) for the origin of the current
content.
