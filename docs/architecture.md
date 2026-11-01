# Shared skills and agent adapters

## Boundaries

`skills/<id>/` contains a workflow and its resources. Instructions cover evidence,
project state, and reversible changes. Skill IDs do not depend on the agent name.
Each package receives the complete reference and template tree; the build does not
flatten paths or silently rewrite instructions.

`re-skills.json` defines the catalog format version, package identity, release
version, and skill order. `scripts/re_skills.py` validates the catalog, YAML, and
local links. The current format is 1; unknown versions are rejected.

An adapter implements `validate(root, catalog)` and
`build(root, catalog, destination)` in `scripts/adapters.py` and has an explicit
entry in `ADAPTERS`. The shared builder calls the adapter after validation and
assembles output in a temporary directory first. Publication renames the completed
directory. With `--replace`, the previous output is preserved until publication
completes. An unknown agent fails before creating output.

Adapter code and configuration are host-specific. For Codex, plugin presentation
is in `adapters/codex/plugin.json`, and skill metadata is in
`adapters/codex/skills/<id>/openai.yaml`. Output contains a portable Agent Plugins
manifest with the `com.openai` extension and a skills directory. Identity and
version come from the catalog rather than a second maintained manifest copy.

## Current portability boundary

Only the Codex adapter is implemented. A portable manifest does not establish
verified support for other hosts.

The `ghidra-re-investigation/references/mcp-connection.md` reference retains the
existing names `mcp__ghidra__list_instances` and
`mcp__ghidra__connect_instance`. This dependency on the current integration remains
explicit even though directories are separated. Required capabilities are:

| Capability | Required behavior |
| --- | --- |
| Instance discovery | Identify the project and active program |
| Connection | Explicitly select an instance and confirm target identity |
| Analysis | Functions, decompilation, cross-references, and data |
| Documentation | Names, types, signatures, and comments |
| Verification | Read back each mutation from the same program |

The server and connection settings belong to the user's environment. The package
does not include an unverified example endpoint or a Ghidra project.

## Adding another agent

1. Check its actual skill format, discovery mechanism, and MCP integration.
2. Add host data under `adapters/<agent>/`, an adapter implementation, and an
   explicit registry entry. Do not maintain a separate copy of shared skills.
3. If Ghidra tool names differ, extract a shared connection contract and add an
   adapter reference. Update links explicitly and test the result. Do not apply
   global replacements to Codex or tool names.
4. Assemble a complete package with its metadata, references, and templates.
5. Add packaging tests and check skill discovery and the MCP workflow in the actual
   host. Only then describe that agent as supported.

The build does not connect to Ghidra or establish that MCP operations or in-game
patch behavior work. Those checks require a specific target and environment.
