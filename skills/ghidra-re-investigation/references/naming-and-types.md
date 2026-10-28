# Naming, types, and signatures

## Confidence threshold

Rename when multiple observations support a durable semantic role, such as a write site plus several consistent readers, or a caller/callee contract plus runtime confirmation. If only the mechanism is known, use a conservative mechanism name. If the role is still ambiguous, keep the generated name and add an evidence comment.

Use names that describe responsibility rather than the current investigation, for example `LoadFileIntoMemory`, `ProcessVisualRecordList`, or `gGameplayTickCounter`. Avoid names that encode an unproven cause such as `CrashFixBuffer`.

## Apply documentation through Ghidra MCP

- Rename functions by entry address, not by a call-site address.
- Name a global at its storage address; do not name one observed heap instance as though it were the global.
- Add end-of-line comments at important call sites and plate comments for function-level contracts.
- Set a prototype only after confirming parameter count, widths, return value, and calling convention from callers, stack cleanup, register use, or runtime arguments.
- Model recurring field offsets with a structure once enough fields and object boundaries are supported. Until then, use field comments rather than inventing a complete structure.
- Verify every MCP mutation by reading the symbol, function, prototype, or comment back.

## Calling-convention evidence on 32-bit x86

- Caller stack cleanup after a call supports cdecl but can also reflect compiler-specific cleanup choices; corroborate it across callers.
- Callee `ret N` strongly supports callee cleanup and fixes the stack-argument byte count.
- Saved EBX/ESI/EDI registers are nonvolatile temporaries, not globals and not function arguments by themselves.
- A value loaded from `[EBP+8]` is the first ordinary stack argument after a standard frame prologue.
- `LEA` computes an address or arithmetic expression; it does not dereference memory.
- Keep narrow types narrow when the code consistently uses byte or word operations.

When the exact type is unavailable, choose the smallest honest placeholder (`byte`, `word`, `dword`, or pointer) and improve it when evidence arrives.
