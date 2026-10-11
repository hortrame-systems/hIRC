# hIRC alpha red-team integration plan

This plan attacks interactions among the executable event store, work projection,
CLI, disabled-capability state and recovery behavior. It deliberately does not
duplicate PORTICO's prepared lifecycle/security criteria or ORIEL's ledger/hash
audit. Their results remain separate inputs.

## Operating rule

Run the smallest relevant integration batch after every coherent executable
change and the full batch before each implementation-stone closure. A failed
security, privacy, authority, recovery or data-integrity invariant blocks the
affected stone. Preserve the failing case before repair and keep a regression.

## Batch A — integrity before continuation

1. Tamper with an existing event through privileged database access, then attempt
   another append. The append must fail before extending a corrupt chain.
2. Remove a disabled-capability row through privileged access, then attempt an
   append. The append must fail; a missing capability cannot become enabled by
   absence.
3. Start a destructive transaction and terminate it without commit. Reopen must
   show the exact prior valid state and permit a normal subsequent append.

## Batch B — concurrency and restart

4. Race multiple independent writers against one store. Every accepted event must
   occupy one contiguous sequence and the final chain must verify. Busy/lock
   failures must be explicit rather than silently losing work.
5. Close and reopen after a multi-event work stream. The briefing and head hash
   must reproduce exactly.

## Batch C — information boundaries

6. Carry privacy class, audience and purpose from the source event into every
   derived work briefing. A later event that changes this context without an
   explicit governed transition must hold projection rather than silently widen.
7. Feed command-, URI-, template- and script-shaped strings through CLI/store/
   projection. They must remain inert data and reproduce exactly.
8. Keep requested, sent, provider-accepted and observed effect states distinct;
   no projection or status change may promote one to another.

## Batch D — dependency and correction behavior

9. A held work item must not block an unrelated sibling. Its allowed sibling path
   and reopening condition remain visible.
10. Missing references, duplicate identities, dependency cycles, double-clear and
    invalid correction targets fail closed without damaging the source chain.
11. Corrections remain attributable events; they never erase the corrected event
    or silently mutate unrelated projections.

## Batch E — release-level consistency

12. Verify executable source, test, validation, ledger and documentation pins in
    one stable sequential frame. Validator regeneration always precedes ledger
    reconciliation; concurrent writers are a failing test case.
13. Verify all high-risk capability families remain disabled across initialization,
    reopen, projection and CLI status. No network/process dependency may enter the
    local core unnoticed.

## Deferred alpha attacks

UI injection/accessibility, provider/outbox uncertainty, secret handling,
encryption, installed-package and packaging permissions, backup/restore on another machine, fuzzing,
load/soak testing and independent penetration review begin when those components
exist. They are not passed by absence of implementation.
