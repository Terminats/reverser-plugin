# Investigation loop

## Establish identity first

- Record architecture, image base, relevant module hash, and whether ASLR or relocation affects runtime addresses.
- Distinguish virtual address, RVA, file offset, runtime address, structure-field offset, and array index. State which one is being used.
- Map crash offsets with `image base + module-relative offset`; this is arithmetic addition, not bitwise OR.

## Trace behavior

- Follow the smallest path that can answer the current question. Bound xref counts and instruction ranges; filter long logs locally to addresses, timestamps, state changes, and failures before returning them.
- At a suspicious instruction, identify the containing function, all meaningful callers, relevant callees, and data references.
- Reconstruct arguments from the calling convention and the caller: right-to-left pushes for common x86 cdecl/stdcall calls, register arguments where applicable, and caller/callee stack cleanup. A decompiler's initial `void` signature is not evidence of no arguments.
- Track pointer provenance and lifetimes. Distinguish an object base from a pointer stored in a global and from a pointer to one of its fields.
- For loops and parsers, identify termination conditions, cursor increments, input boundaries, output writes, and unchecked look-behind/look-ahead access.
- When an observed symptom may be downstream corruption, inspect the first invalid state transition rather than only the eventual faulting instruction.

## Dynamic confirmation

- Break at the narrowest instruction that can distinguish the hypotheses.
- Record register values, stack arguments, pointed-to memory, and changes across one step or tick.
- Confirm stable object identity before comparing fields across ticks.
- Prefer tracing or observation-only hooks before changing timing, input state, or render state.
- Treat a negative result as evidence and document why it rejects the hypothesis.
- Before implementing an experiment, check that its hook and observed state actually belong to the behavior being tested. Prefer one observation that separates competing explanations over several speculative patch variants.

## Handoff

Summarize:

- confirmed invariant or failure;
- addresses and address kinds;
- Ghidra names/types/comments updated;
- unresolved uncertainty;
- the next observation that would reduce it.

For tests run by the user, give one command and a short checklist of observations to report together. Continue independent analysis while waiting; defer only work requiring the result. Launch or control the game only when explicitly requested. Keep confirmed names and contracts in Ghidra so later turns need not re-read the same decompilation. Follow the project's documentation timing preferences; keep provisional findings out of durable reports unless requested.
