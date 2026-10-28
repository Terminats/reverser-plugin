---
name: ghidra-re-investigation
description: Investigate native binaries in Ghidra using static and dynamic evidence, and keep confirmed function names, globals, types, signatures, and comments synchronized in the Ghidra project through MCP. Use for reverse-engineering investigations; do not use merely to implement an already specified source-code change.
---

# Ghidra Reverse-Engineering Investigation

Use Ghidra as the durable analysis database, not as a read-only disassembler.

Follow the user's or target project's documentation language; default to English when neither specifies one. Keep user-facing conversation in the user's language unless requested otherwise.

1. Frame one discriminating question before reading code. Plan a small, bounded set of function, xref, or data reads; expand only when those results require it.
2. Connect to the intended instance and select the program explicitly when several are open. Reuse known names and addresses instead of repeating discovery.
3. Separate confirmed facts, strong inferences, and open hypotheses. Use dynamic observation when static evidence cannot distinguish them. Keep instrumentation observational; account for debugger and probe effects on timing rather than treating them as behavior fixes.
4. Once evidence supports a stable role, write its name, type, prototype, or comment into Ghidra through MCP and verify the mutation.
5. Report only the evidence that changes the conclusion, the Ghidra documentation changed, remaining uncertainty, and the next discriminating observation. Do not paste full decompilations or logs when a short excerpt suffices.

Read [references/mcp-connection.md](references/mcp-connection.md) before connecting to Ghidra. Bind the connection to the current target using project-local settings and instance discovery; reuse it only while that target remains verified.

Read [references/investigation-loop.md](references/investigation-loop.md) when tracing an unfamiliar path or combining debugger evidence with Ghidra. Read [references/naming-and-types.md](references/naming-and-types.md) whenever names, structures, globals, calling conventions, or function signatures are being decided.

Preserve existing Ghidra documentation unless new evidence disproves it. Investigation authorizes read-only analysis and analysis-database documentation, not binary patch deployment.

When adding runtime counters, probes, or periodic logs to a native patch runtime, keep them in its separate development monitoring module and exclude them from production builds. Static analysis or external debugger observation does not require creating a runtime module. Preserve confirmed findings as Ghidra names, signatures, and comments.

For gameplay acceptance, prepare the exact command (or launch steps), actions, and observations for the user; launch or control the game only when explicitly requested. Complete independent non-interactive work while results are pending. Pause only conclusions and changes that depend on those results, and identify them in the handoff. A successful build or synthetic check does not establish gameplay acceptance.
