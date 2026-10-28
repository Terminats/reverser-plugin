# Maintenance

This repository distributes reverse-engineering skills. It is not a target-game
repository; do not scaffold a native runtime or import game binaries here.

- Edit shared instructions and resources in `skills/`. Keep skill IDs stable.
- Keep host-specific UI metadata, packaging, and tool mappings in `adapters/`.
  Only Codex is supported. Do not label another host supported before implementing
  its adapter and checking its real discovery and tool requirements.
- Preserve evidence, target identity, reversible patching, and production versus
  diagnostic boundaries when adapting instructions for another host.
- The Ghidra MCP tool names currently embedded in the imported reference are an
  explicit portability limitation. Read `docs/architecture.md` before adapting it.
- Generated `dist/` packages are disposable. Change sources, then rebuild.
- Run `.venv/Scripts/python scripts/re_skills.py validate` and
  `.venv/Scripts/python -m unittest discover -s tests -v` on Windows; use
  `.venv/bin/python` elsewhere. Build the Codex package after changing packaging.
- Write repository documentation in Polish and retain the existing language of
  imported skills unless the task asks for translation.
