# hIRC local developer-package checkpoint — 2026-10-10

## Claim boundary

This is a cumulative local implementation checkpoint, not Milestone 03 closure
and not a sensitive-data, production or public release. No Bridge, Tor/IRC,
network provider, credential or external-effect path is enabled.

The dependency-free developer package is:

- `dist/hirc-local-0.1.0.dev0.pyz`
- SHA-256 `365f17c1506a7560e531843b6f7585cc5c57a826ec31e9ddb129d9becd9942e0`
- 37,973 bytes

The sequential cumulative result is:

- `implementation/executable-cumulative-validation.json`
- SHA-256 `c8a3bbb7621c189b41d5dfa27f442155feeba2354d0d2be9cd6058223c1e61cb`
- status `PASS_WITH_DECLARED_RELEASE_HOLDS`
- twenty-one validators; 140 source-tree tests, including three expected release failures

## Implemented local slices

- **M04 integrity core:** append-only content-addressed event chain, mandatory
  foundation/goal/actor/privacy/audience/purpose, immutable disabled capability
  set and trigger/schema verification.
- **M05 work and recovery:** deterministic work, commitment, dependency, hold,
  observation, correction and return-briefing projections; transitive held
  dependencies are blocked and false runnable-sibling claims fail.
- **Cross-component red team:** eighteen attacks, two preserved failed baselines
  and ten repaired defects covering corrupt-chain continuation, disabled-control
  loss, information-boundary propagation, verify/read races, silent initialization
  repair, correction widening and dependency propagation.
- **M06 local UI:** deterministic self-contained read-only HTML with roster,
  search, Back/Forward/Resume, exact boundaries/source events, four no-effect
  interruption previews, and content-addressed refusal/correction/action previews.
- **M07 formation/adapters/outbox:** permanent-only identity formation with ten
  evidence gates; recorded scoped admission kept distinct from verified authority;
  provider-neutral deterministic fake adapters; credential-shaped input rejection;
  atomic SQLite outbox item/stage/event commits; local idempotency under a five-
  writer duplicate race; provider acceptance never promoted to observation.
- **M08 local hardening:** verified atomic backup/restore, exact v1-to-v2 migration
  with predecessor preservation, invalid-input and bounded 100-event load checks,
  a byte-reproducible `.pyz` runnable without `PYTHONPATH`, a bounded 500-event
  process-crash soak, and exact materialized-outbox/schema verification.

## Material failures preserved and repaired

- First integration run: four of eight attacks failed. Store continuation after
  corruption/control deletion and information-boundary loss/widening were fixed.
- Second integration run: six of eighteen attacks failed. Verify/read TOCTOU,
  silent corrupt-store reinitialization, missing append-only trigger, correction
  widening, false sibling and transitive hold failures were fixed.
- Recovery: Windows fsync on a read-only handle failed; then read-write corrupt-
  file verification retained a fixture lock. Writable fsync and explicit read-only
  verification fixed both.
- Migration: backup from the same connection after `BEGIN IMMEDIATE` deadlocked.
  Backup-first verification plus a new immediate transaction and exact frame
  recheck fixed it. A later validator fixture-lifetime false negative was also
  preserved and corrected.
- Package validation: the package passed while the validator's source-tree loader
  omitted `src`. The validator path was fixed without adding `PYTHONPATH` to the
  packaged-execution test.
- Parser/resource hardening now rejects over-deep, oversized and invalid-UTF-8
  JSON at event, adapter and decision boundaries.
- Outbox integrity: swapping two stage bindings after exactly restoring the
  append-only trigger retained the event-chain head and incorrectly verified.
  Stage-to-payload/request/boundary binding and exact schema-object verification
  now reject both rebinding and weakened-schema attacks; the failed baseline is
  preserved.
- Atomic publication: backup, migration-backup and witness writers could overwrite a destination
  created after their initial existence check. Same-directory create-if-absent
  publication now preserves the racing writer's bytes and fails closed; all three
  paths have regressions and the failed mechanism is preserved.
- File ingress: local JSON proposal/preview/witness readers loaded unbounded files
  before semantic checks and malformed UTF-8 escaped one CLI path. A shared
  predecode byte bound, strict UTF-8 decoder and structural bound now fail closed;
  the failed baseline and three regressions are preserved.
- Verification mode: integrity, status, event iteration and verified projection
  snapshots requested read-write SQLite connections. They now use read-only
  connections while append/outbox/migration retain explicit writable transactions;
  both failed frames and the combined regression are preserved.
- Canonical JSON: duplicate raw keys could change stored bytes while the decoded
  value and event head stayed unchanged, and file ingress silently kept the last
  duplicate. Duplicate keys and noncanonical stored/legacy payload bytes now fail;
  the attack and three regressions are preserved.

## Current release holds

1. Live store and backups are plaintext. A supported encryption and key-custody
   design is required before sensitive-data release.
2. The in-app browser refused local-file navigation. Browser-engine, keyboard,
   responsive, forced-colors, screen-reader and human-usability evidence remains
   open; no listener was added to bypass that policy.
3. Independent security/privacy review and penetration testing remain open.
4. Broader crash/power-loss injection, fuzzing, soak and cross-machine recovery
   remain open.
5. M03-S014 independent security/privacy and metric/evaluator acceptance remains
   open; M03-S015 commit/public push and direct remote verification therefore
   remain held.
6. Privileged tail truncation lacks a protected external/signed head witness, and
   the package manifest lacks an independently verifiable release signature.

Keyed HMAC head-witness tooling now detects tail truncation when explicitly used,
but operational key custody, automatic witness integration and a public signature
remain open; the expected failure therefore remains at the default-store/release level.

Encrypted-key Ed25519 signing/verification tooling also passes, using ephemeral
test keys only. No actual release key or published signature exists; custody,
authorization, rotation, revocation and publication remain open.

Authenticated encrypted-backup tooling also passes using scrypt and AES-256-GCM.
Live SQLite storage and long-term passphrase/key custody remain open.
Sensitive-mode initialization now fails before creating a store when no admitted
encrypted live-store backend exists; it never silently falls back to plaintext.

A bounded 500-event soak with verification at 100/250/500 events, abrupt child-
process death inside an uncommitted destructive transaction, and final verified
backup/restore also passes. It is not physical power-loss or production-soak evidence.

The materialized outbox repair passes two new privileged-tampering regressions.
It does not replace protected witness deployment or independent penetration review.

## Team and onboarding continuity

Three immutable orientation frames prevent live implementation changes from
resetting learner reading. KEEL owns one canonical queue for final bounded closure;
no qualified custody recipient exists. RADICAL and APOTHEM completed the three
orientation frames but remain operationally HELD on their personal source,
formation, peer/role and capacity gates. PORTICO and ORIEL retain exact readiness
holds and did not promote older metadata checks to the current executable frame.
Retired participants remain latched and receive no new work.

## Git/publication state

The governed working tree remains uncommitted at HEAD
`1c525e3b464c58b6e037faaf6bb76626b32364e4`. This checkpoint is not the M03-S015
milestone commit. Public push remains held by the declared S014/S015 sequence and
the release holds above; the owner's standing public-push authorization is
preserved for the eligible closure frame.
