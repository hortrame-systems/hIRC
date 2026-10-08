# hIRC stepping-stone execution protocol 0.1

**Status:** active planning rule under HIRC-I020

## Stone contract

Every milestone is an ordered dependency graph of tiny stepping stones. Each
stone contains:

- stable ID and one concrete outcome/claim;
- prerequisites and exact active source/goal/foundation/profile versions;
- responsible owner and canonical writer;
- bounded files/components/data/effects;
- positive control and adverse/failure cases;
- required structural, semantic, unit, integration, privacy, security,
  accessibility/usability, recovery or observed-effect tests as applicable;
- expected evidence and independent review needs;
- rollback/forward-recovery and stop condition;
- status and residual limits; and
- next eligible stones.

## States

```text
CAPTURED -> READY -> ACTIVE -> CHECKING -> PASS
                              -> FAILED
                              -> HELD
                              -> NOT_VERIFIED
                              -> SUPERSEDED
```

`NOT_APPLICABLE` is allowed only with exact scope/reason and dependency review.
`DEBT_DURING_GENERATION` exists only while the same stone is actively generating
its outputs and must close before the stone passes.

## Hard gate

Do not start a dependent stone unless every prerequisite is `PASS` or an accepted
plan revision explicitly branches around it with preserved guarantees, trade-off,
reason and tests. A saved file, status claim, hash, schema parse, self-report or
peer agreement cannot substitute for the evidence the stone's claim needs.

Tests remain claim-scoped:

- structural tests prove structure only;
- unit tests prove the exact unit/build only;
- integration tests prove declared interfaces only;
- hostile tests probe the declared threat model;
- usability/accessibility tests require actual interaction evidence;
- statistical claims require model/data/metric validation; and
- external effects require observed results, not request/provider receipt.

## Thorough without waste

“Thorough” means every material failure mode, boundary and negative path for the
stone's claim is covered, with meaningful controls and recovery. It does not mean
duplicating implementation-shaped tests, rerunning unchanged broad suites or
blocking harmless work on unrelated future modules.

## Milestone closure

The milestone cumulative Markdown lists every stone and status, exact test/evidence
references, failures/corrections, holds and gate decisions. All required stones
must pass or be explicitly excluded by an accepted scope branch. Then run the
milestone-wide integration/recovery checks, update ledger/readable views, commit
and push under HIRC-I019.

