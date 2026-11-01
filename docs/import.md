# Skill import

The initial content was copied on 2026-10-28 from the local `~/.codex/skills/`
directory:

- `game-reverse-engineering-repo`
- `ghidra-re-investigation`
- `binary-patch-engineering`
- `readable-code` - added when the scope was extended to include code formatting
  and refactoring guidance

The import preserved `SKILL.md` content, references, and templates. Original
`agents/openai.yaml` files were moved unchanged to
`adapters/codex/skills/<skill-id>/openai.yaml`; the build places them back under
`skills/<skill-id>/agents/openai.yaml` in the output plugin.

After review, `readable-code` was shortened while retaining formatting preferences
and general refactoring guidance. Details about runtimes, diagnostics, and specific
testing mechanisms were removed. Its OpenAI metadata was initially preserved, then
translated into English when the repository adopted English throughout.

The import includes three RE skills and the shared `readable-code` skill. It does
not include skill-management workflows or integrations with other services.
Cross-references between RE skills retain their existing identifiers.

The repository is now the source of changes for this package. Globally installed
copies do not synchronize automatically. Updates from those copies should be
compared, transferred with their resources, and validated. Replacing existing
global installations is not part of building the plugin.
