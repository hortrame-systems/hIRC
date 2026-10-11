# hIRC executable v0.1 completion boundary

The existing Milestone 03 work closes the master-plan review. It is not the
application. Executable v0.1 is complete only when one local human can use a
local hIRC installation to record and recover work, evidence, commitments,
holds, corrections and the next justified action through a tested interface.

The implementation proceeds through five finite milestones:

1. **M04 — Local integrity core.** A deterministic, append-only local event
   store and CLI; evidence/inference/norm/authority/action/correction remain
   separate; privacy purpose/audience are mandatory; tampering is detected;
   external effects and every Bridge/network path are disabled.
2. **M05 — Work and recovery.** Typed work, commitments, dependencies, holds,
   observations and corrections; deterministic projections; return briefings
   with source coverage and reported-versus-observed distinctions.
3. **M06 — Local UI.** Compact rooms/direct work views, roster, search,
   Back/Forward/Resume, interruption choices, trusted consequential preview and
   accessible refusal/correction flows.
4. **M07 — Formation and adapters.** Permanent identity/role records,
   formation/admission gates, provider-neutral local adapters and an outbox.
   Network and external effects remain disabled until their separate gates pass.
5. **M08 — v0.1 release.** Recovery drills, privacy/security tests, hostile
   local fixtures, usability/accessibility checks, reproducible package, exact
   release manifest and local installation documentation.

The following are explicitly outside executable v0.1: Tor/IRC Bridge
activation, remote peer enrollment, ethical-debate scheduling, cooperative
competition runtime, Bayesian scores with authority effects, live foundation
self-activation, arbitrary extensions and commercial payment workflows. Their
schema identities remain reserved and disabled so later work cannot silently
inherit authority.

Every stone ends with passing positive and adverse tests, reconciled consumers
and an exact checkpoint. A blocked independent review holds only the acceptance
claim that depends on it; unrelated implementation continues. No milestone is
complete merely because its plan or schema exists.

## M04-S001 — PASS

Deliver a dependency-free Python integrity core using SQLite and the standard
library:

- initialize a local store with every high-risk capability disabled;
- append canonical events with mandatory foundation, goal, actor, category,
  privacy, audience and purpose bindings;
- retain requested/sent/provider-accepted/observed effect states separately;
- hash-chain every event and deny ordinary update/delete operations;
- verify the complete chain and fail closed on drift; and
- expose `init`, `record`, `status` and `verify` commands.

This stone does not implement agents, model calls, scheduling, UI, networking,
credentials, external actions, Bridge behavior or production security.

## M05-S001 — PASS

Build deterministic work and recovery projections from the verified event chain:

- work items and current status;
- commitments and their disposition;
- typed dependencies with cycle rejection;
- scoped holds that expose independently runnable sibling work;
- reported and observed result states kept separate;
- correction references and unprojected-event coverage; and
- a source-linked return briefing exposed by the CLI.

This stone does not schedule work, execute an agent, infer hidden intent or turn a
briefing into authority. Projection failure holds the briefing and preserves the
source chain.

## M06-S001 — PASS (local static scope)

Expose the verified local store and return briefing through a self-contained,
read-only HTML snapshot with work views, roster, search and Back/Forward/Resume.
The output has no listener, remote resource, form submission or external-effect
path. Interruption preview and refusal/correction flows are separate M06-S002 and
M06-S003 stones so each transition receives its own adverse tests.

Five M06-S001 UI tests pass; the 140-test source-tree suite succeeds with three
expected release failures. The exact
generated reference is deterministic, hostile markup remains inert, CSP hashes
bind the only inline style/script, IDs are unique, active external edges are
absent and output is atomic. Rendered browser/accessibility/usability acceptance
remains explicitly held by `m06-s001-browser-check-hold.md` after the in-app
browser rejected local-file navigation. M06-S002 is covered below.

## M06-S002 — PASS (deterministic no-effect scope)

The UI now presents the exact four interruption choices—cut, high priority, low
priority and custom—as a fast local preview. One semantic map owns ordering and
return behavior. Every preview states the smallest-safe-boundary rule and records
that it is not saved, scheduled, authorized or executed. Four dedicated tests
cover distinct ordering, no-effect invariants, explicit custom input and absence
of a submission edge. Rendered interaction remains held by the same local-file
browser-policy boundary. M06-S003 is covered below.

## M06-S003 — PASS (deterministic no-effect scope)

Refusal, correction and consequential-action previews now share one canonical,
content-addressed local object. Participation remains separate from action
disposition; allowed actions require an authority reference; correction previews
must preserve the target information boundary; unknown fields, changed content
and self-consistent semantic forgeries fail closed. Nine dedicated tests and the
140-test source-tree suite succeeds with three expected release failures. The CLI may write a preview JSON and the
read-only UI can display exact validated previews, but no preview is a signature,
consent, approval, persistence or effect.

The M06 deterministic/static slice is complete. Browser-engine, keyboard,
screen-reader and human-usability acceptance remains HELD by the local-file
browser policy. Independent M07 formation/adapters work may continue without
promoting that empirical UI gate.

## M07-S001 — PASS (declared local formation scope)

The verified event chain now projects permanent-participant proposals,
evidence-bearing formation assessments and scoped admission records. Temporary
identities, incomplete gate sets, premature or stale admission, role/scope
escalation, duplicate native binding and information-boundary widening fail
closed. Whole-source study and demonstrated use are distinct gates. An admission
requires the latest READY assessment plus an authority-bound observed action and
authority evidence references, but remains **ADMISSION_RECORDED** with
**UNVERIFIED_REFERENCE** authority. Eleven dedicated tests and the complete
140-test source-tree suite succeeds with three expected release failures. This does not authenticate a caller, prove the
cited evidence or grant actual source/task access. M07-S002 is next.

## M07-S002 — PASS (local fake-provider scope)

A provider-neutral adapter request now binds admission reference, foundation,
goal, information boundary, capability and payload while forcing network,
credentials and external effects off. Deterministic echo and acceptance-only
providers keep requested, provider-accepted and observed states separate; absent
observation stays UNKNOWN. Credential-shaped nested fields, request/result
tampering, request mismatches and adapters declaring network/effects fail closed.
Twelve adapter tests pass.

## M07-S003 — PASS (atomic local no-dispatch scope)

The SQLite journal now atomically binds immutable outbox items and stages to the
event hash chain. Idempotency keys prevent duplicate local work across repeats
and a five-writer race; request collisions fail; provider acceptance never becomes
an observation; uncertain observation remains UNKNOWN; privileged table changes
and forbidden dispatch flags invalidate the store. Ten outbox tests and the
140-test source-tree suite succeeds with three expected release failures. External dispatch, credentials, network
and Bridge remain disabled. M07's declared local slice is complete; M08 release
and hardening work is next.

## M08-S001 — PASS (local plaintext backup/restore scope)

Verified stores can now be backed up and restored through SQLite's consistent
copy API, fsynced and atomically published only after chain/schema/capability/
outbox verification and source-head comparison. Existing targets, corrupt sources
and truncated backups fail without replacing the destination. The preserved first
run records a Windows fsync-handle defect and a read-write verification lock; both
were repaired. Six recovery tests pass. Backups remain plaintext, so sensitive-
data release is blocked.

## M08-S002 — PASS (exact v1 and bounded local hardening scope)

The exact pre-outbox v1 schema can migrate to v2 only after a verified predecessor
backup is atomically preserved; the source is reverified under an immediate
transaction before mutation, and its event head/count must remain unchanged.
Unknown schemas, corrupt chains, missing triggers, occupied backup paths and
repeat migration fail closed. Seeded invalid identifiers and a 100-event local
load also pass. The initial same-connection backup deadlock and one validator
fixture error remain preserved. Nine hardening tests pass.

## M08-S003 — PASS (reproducible developer package); release HELD

`dist/hirc-local-0.1.0.dev0.pyz` is a deterministic dependency-free zip
application. Two builds are byte-identical; its internal/external manifests and
CRC pass; it executes from an unrelated directory without `PYTHONPATH`; and the
packaged init/record/verify/UI loop passes. Four package tests and the complete
140-test suite succeeds with three expected release failures. The package still forbids network/external effects and marks
sensitive-data release false.

Sensitive-data, production and public release remain HELD on plaintext storage,
rendered accessibility/usability evidence, independent security/privacy review,
broader crash/fuzz/soak/cross-machine recovery and M03 S014/S015 closure.
The three executable expected failures are privileged tail truncation without a
protected external head witness, plaintext SQLite storage and an unsigned package
manifest.

## M08-S004 — PASS (keyed witness tooling); deployment/key custody HELD

An atomic HMAC-SHA-256 head witness can now be created and verified with a caller-
supplied key read from standard input and never stored in the database, witness or
process arguments. Six tests show that it detects privileged tail truncation even
when the remaining chain and triggers are locally self-consistent, and rejects
wrong keys, changed witnesses, short keys and target overwrite. HMAC remains
symmetric; witness key generation, OS-vault custody, escrow/distribution,
automatic per-mutation integration and independently verifiable public signatures
remain release holds.

## M08-S005 — PASS (encrypted-key signing tooling); release-key custody HELD

Node-based Ed25519 tooling now generates encrypted PKCS#8 private keys, signs the
exact manifest bytes and verifies the signature/public-key fingerprint. The
passphrase is read from standard input; targets are not overwritten; changed
manifests, wrong public keys, wrong/short passphrases and private-material leakage
are rejected by six tests. Only ephemeral test keys were generated. Actual release
key ownership, authorization, OS-vault/HSM custody, escrow, rotation, revocation,
signature publication and independent release review remain open.

## M08-S006 — PASS (authenticated encrypted-backup tooling); live storage/custody HELD

Verified backup bytes can now be wrapped with scrypt-derived AES-256-GCM and
restored byte-for-byte. Wrong/short passphrases, changed ciphertext and overwrite
fail without producing output; the envelope contains neither plaintext nor a
stored key. Six tests pass. Live SQLite remains plaintext, and passphrase/key
recovery, custody, rotation, escrow, operator rate limiting and independent
cryptographic review remain release holds.

The packaged `init --sensitive` path now fails closed before creating a database
unless an admitted encrypted live-store backend exists. Ordinary status reports
`encrypted_at_rest: false` and `sensitive_data_release_allowed: false`; encrypted
backup tooling never silently promotes the live plaintext store.

## M08-S007 — PASS (bounded local soak/crash scope)

A 500-event local soak verifies and reopens the store at three checkpoints, kills
a child process during an uncommitted destructive transaction, requires exact
rollback, and finishes with verified backup/restore. This does not cover physical
power loss, storage-controller behavior, long-duration load or another machine.

## M08-S008 — PASS (materialized outbox integrity repair scope)

A preserved failing attack swapped two OBSERVED outbox-stage bindings, exactly
restored the append-only trigger and retained the same event-chain head while
verification incorrectly returned valid. Verification now binds each stage row
to its immutable event payload, request and information boundary and checks the
exact table/index schema object set. Two regressions cover stage rebinding and
schema weakening. Protected witness deployment, encrypted live storage and
independent penetration review remain release holds.

## M08-S009 — PASS (atomic no-overwrite publication scope)

Backup, restore, predecessor migration-backup and head-witness writers no longer
combine an early existence check with later replacement. They publish the fully fsynced temporary file with
one same-directory create-if-absent operation and preserve a destination created
by a racing writer. Three injected-race regressions pass on Windows. Native POSIX,
post-publication same-user mutation and physical power-loss durability remain open.

## M08-S010 — PASS (bounded JSON file-ingress scope)

Adapter, decision, outbox and UI-preview JSON files are now byte-bounded before
strict UTF-8 decoding and parsing, then checked for finite depth and canonical
size. Head-witness files use a tighter bound. Oversized and malformed files fail
through the CLI's HELD contract rather than being fully loaded or escaping as an
uncaught decoding error. SQLite-row and encrypted-backup streaming limits remain
separate hardening work.

## M08-S011 — PASS (read-only verification connection scope)

Integrity verification, status, event iteration and verified projection snapshots
now open SQLite read-only by default. Append, outbox and migration remain explicit
writable transactions. Two preserved failing frames showed observation paths requesting writable connections; the repaired
ten-test store suite requires read-only mode. Concurrent privileged mutation,
external witness deployment and filesystem immutability remain separate controls.

## M08-S012 — PASS (canonical JSON ambiguity repair scope)

JSON ingress now rejects duplicate object keys at every depth, stored event
payload bytes must equal their exact canonical encoding, and legacy migration
refuses noncanonical payloads before changing schema. The preserved attack changed
raw frozen-log bytes while keeping the decoded value and event head unchanged;
three regressions now reject stored, file-ingress and migration variants. A
protected external witness is still required against privileged full-chain rewrite.

Before UI construction, two cross-component red-team batches are PASS: eighteen
integration attacks cover privileged chain/capability/trigger tampering before
append, transaction rollback, concurrent writers, restart reproducibility,
single-snapshot projection, refusal to silently repair an existing corrupt store,
information-boundary inheritance and correction/widening rejection, transitive
hold propagation, runnable-sibling claims, effect-state separation, failed-
projection chain preservation and command-shaped inert data. The two failed
baselines preserve ten repaired defects in
`m06-s001-red-team-validation-v1-failed.json` and
`alpha-integration-red-team-validation-v2-failed.json`.
