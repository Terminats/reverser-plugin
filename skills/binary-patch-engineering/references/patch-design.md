# Patch design

## Freeze the evidence

Before implementation, record:

- supported build identity and architecture (reuse an already verified isolated copy when unchanged; retain a hash for a distributable or persistent file replacement);
- original virtual addresses and their RVAs;
- exact instruction bytes and complete instruction boundaries;
- calling convention, state lifetime, and side effects that must remain;
- observable acceptance and rejection criteria.

Do not substitute a longer copy routine for an unsafe copy unless the destination allocation and every downstream layout assumption can accommodate the larger result.

## Address and encoding rules

- `RVA = virtual address - preferred image base` for the analyzed module.
- File offset is determined by the containing PE section; it is not generally equal to the RVA.
- For x86 `CALL rel32` or `JMP rel32`, displacement is `target - address_after_instruction` and must fit signed 32 bits.
- A hook overwrite must contain whole instructions. A five-byte jump cannot safely split a longer instruction.
- A trampoline must preserve the semantics of the complete overwritten instructions and return after that range. Relocate relative branches/calls and address-dependent operands (including RIP-relative accesses where applicable); remap targets inside the relocated block. Recompute displacements for the new location and verify encoding ranges. If the relocator cannot preserve an instruction's behavior, reject that hook site rather than copying its bytes unchanged.

## Hook boundaries

Choose the narrowest boundary that preserves required behavior. Prefer replacing one render-only call over skipping a wrapper that also updates input, animation, or resource state. For imported APIs, an IAT hook can observe all calls, but distinguish relevant call sites by validated return address or surrounding state when unrelated calls exist.

Avoid asynchronous calls into game routines unless their thread, lock, frame, and global-state preconditions are proven. For high-frequency instrumentation, bound log volume and avoid allocations or blocking operations in the hot path.

## Component behavior

An apply routine should:

1. validate that the target matches the analyzed build and that each code site it will overwrite still contains the expected instruction bytes;
2. acquire private resources;
3. apply changes in a rollback-friendly order;
4. roll back all completed steps on failure;
5. publish success only after the complete component is active.

A revert routine restores the original behavior before freeing trampolines, cursors, buffers, or other resources that active code could still reference.
