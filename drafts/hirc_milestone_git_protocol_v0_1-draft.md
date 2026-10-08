# hIRC milestone and Git checkpoint protocol 0.1

**Status:** active working procedure under HIRC-I019

## Milestone definition

A milestone is a coherent plan boundary with a named objective, accepted output
or explicit hold, evidence, holistic review/lens refinement and a next plan. A
small file edit is not automatically a milestone. Material source intake, peer
reconciliation, integrated draft, source-policy update and release-boundary
closure are milestones.

## Required cumulative report

Before milestone closure, create `milestones/MILESTONE-<ID>.md` containing:

1. predecessor milestone/commit and objective;
2. every owner intent added, revised or superseded;
3. exact source/artifact identities and access/export boundaries;
4. work completed and why;
5. independent/peer review, agreements, dissent and unread holds;
6. architecture, requirements, threats, schemas and tests changed;
7. meaningful errors/corrections and preserved predecessors;
8. security, privacy, non-domination, licensing and Bridge consequences;
9. validations run with exact limits;
10. implementation/legal/release claims that remain unproven;
11. open/deferred work, owner and next safe action;
12. holistic lens refinement or justified no-change; and
13. Git branch/content commit/push receipt or exact push hold.

The report is cumulative enough to recover the project without earlier chat, but
links to exact detailed artifacts rather than copying protected/private bodies.

## Closure sequence

1. reconcile the canonical intent register and current source selection;
2. update the milestone report, master/requirements/companions and ledger;
3. preserve before-state/supersession and close generation debt that belongs to
   the milestone;
4. run deterministic JSON/link/hash/ID/secret/diff validation;
5. verify ignored/local-only sources and temporary/runtime material are not
   staged;
6. stage only governed Git artifacts;
7. create a conventional, concise milestone content commit;
8. record the content commit in the milestone report/receipt if needed;
9. create the small completion-receipt commit;
10. push the branch and verify its remote ref; and
11. mark the milestone `PUSHED` only from observed push/ref evidence.

If push is unavailable or rejected, preserve the local commit and report
`LOCAL_COMPLETE_PUSH_HELD`, the error, branch, commit and repair owner. Never
expose private sources or weaken checks to obtain a green push.

## Git/privacy boundary

Commit authored master/requirements/companion/review/contract/milestone artifacts
and source manifests. Exclude the local human-transfer inbox, decrypted/private
source bodies, runtime agent records, succession database, credentials, keys,
temporary extraction and caches. A source hash and review finding do not
declassify its body.

## Claims

A pushed plan milestone proves only that those exact Git bytes reached the
observed remote ref. It does not prove software implementation, source
comprehension, peer independence, security, legal enforceability, statistical
validity, release readiness or Bridge activation.

