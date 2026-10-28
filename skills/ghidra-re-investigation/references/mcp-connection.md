# Ghidra MCP connection

## Bind the connection to the current target

1. Read the current project's ignored local configuration, if present, for its Ghidra project, program identities, and bridge address. Explicit target selection in the user's request takes precedence. Do not reuse a profile from another repository or an earlier task without verifying that it identifies the current target.
2. List active instances with `mcp__ghidra__list_instances` and match the intended project. Use the returned connection details; do not assume a project name, port, executable, or renderer module.
3. Connect with `mcp__ghidra__connect_instance` using the matched project. Select the intended program explicitly and verify its identity against the target module before reading or mutating analysis data. If multiple candidates remain ambiguous, ask which target to use; continue independent work meanwhile.
4. Verify every rename, type, prototype, or comment mutation by reading it back from the same program.

Reuse a verified connection within the same target. Rediscover when it fails, the expected program is absent, or the target changes. Keep machine-specific connection details in the project's ignored configuration, not in reusable skills or tracked templates. A sample configuration may contain placeholders, never another project's live profile.

## Bridge fallback

After connecting, prefer the exposed MCP tools and load the relevant tool group when available. If a required operation remains unavailable, use the bridge address established for that instance and inspect its `/mcp/schema`.

Filter the schema locally to the required operation rather than returning it in full. Derive endpoint names, request fields, and program selectors from the live schema; do not copy an endpoint or program selector from another project. Verify bridge mutations by readback just like direct MCP mutations. If the bridge or operation cannot be verified, report that limitation instead of guessing an endpoint.
