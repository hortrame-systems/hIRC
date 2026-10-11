# M08 release and hardening stepping stones

M08 turns the bounded local alpha into a reproducible, recoverable package. A
passing local function does not by itself make the application safe for sensitive
or production data.

## M08-S001 — verified backup and restore — PASS (local plaintext scope)

Use SQLite's transaction-consistent backup API to copy a verified store to a new
file, verify the copied chain/schema/capabilities/outbox, compare source head and
event count, fsync and atomically publish it. Restore follows the same rules and
never overwrites an existing target silently.

Acceptance includes work/formation/outbox recovery, corrupt and truncated source
rejection, destination collision, restart equivalence and CLI checks. Backups are
not encrypted in this stone; sensitive-data release remains blocked.

## M08-S002 — migration, crash, fuzz and load — PASS (exact v1 and bounded local scope)

Add explicit schema migration from supported predecessors, deterministic malformed
event/projection fuzzing, transaction crash injection and bounded load/soak tests.
Preserve failed baselines and resource limits.

## M08-S003 — reproducible package — PASS; sensitive/production/public release HELD

Build/install the package in a clean local environment, run tests without source-
tree path injection, verify an exact release manifest, exercise the rendered UI
with keyboard/zoom/forced-colors/screen-reader checks, and obtain independent
security/privacy review. Encryption/key custody and sensitive-data handling need
an explicit supported design. A protected external/signed head witness and an
independently verifiable package signature are also required; no release claim
bypasses those holds.

## M08-S004 — keyed external head witness — PASS tooling; custody/integration HELD

Create and verify an atomic external head witness using HMAC-SHA-256 with a
caller-supplied key that is never stored in the database or process arguments.
The witness must detect privileged tail truncation, wrong keys and changed witness
content. Tooling does not solve key custody, independent public verification or
automatic witness distribution; those remain release holds.

## M08-S005 — encrypted-key Ed25519 release signing — PASS tooling; release-key custody HELD

Provide deterministic exact-byte manifest signing and verification using an
encrypted PKCS#8 Ed25519 private key whose passphrase is read from standard input,
never process arguments. Tests use ephemeral keys only. Actual release-key
generation, custody, escrow, rotation, authorization and publication remain held.

## M08-S006 — authenticated encrypted backup envelope — PASS tooling; live storage/custody HELD

Encrypt and decrypt exact verified-backup bytes with AES-256-GCM and scrypt using
a passphrase read from standard input. Reject tampering, wrong/short passphrases
and overwrite. This protects exported backup bytes only; live SQLite encryption,
password recovery/custody and independent cryptographic review remain held.

## M08-S007 — bounded soak and process-crash rollback — PASS (bounded Windows-local scope)

Append and repeatedly verify/reopen a 500-event store, then kill a child process
inside an uncommitted destructive transaction and require exact rollback. Finish
with verified backup/restore. This is a bounded local probe, not a power-loss,
storage-controller or long-duration production soak.

## M08-S008 — materialized outbox integrity repair — PASS (local integrity scope)

Reject privileged rebinding of outbox stage rows even when the immutable event
chain and exactly restored append-only triggers still look valid. Verification
must bind every materialized stage to its source event's outbox identity, request,
disabled-dispatch flag and information boundary, and must verify the exact table
and index schema object set. The failing pre-repair attack remains preserved.
This closes one local false-integrity path; protected witness deployment,
encrypted live storage and independent penetration review remain open.

## M08-S009 — atomic no-overwrite publication — PASS (Windows-local scope)

Replace existence-check-plus-replace publication in backup/restore, predecessor
migration backup and head-witness creation with a same-directory atomic
create-if-absent operation. Preserve the
concurrently created destination and fail closed if another writer wins the name.
Windows uses no-replace rename semantics; POSIX uses same-filesystem hard-link
publication. The Windows path and all three injected races pass locally; native POSIX,
physical power-loss and filesystem-specific directory durability remain open.

## M08-S010 — bounded JSON file ingress — PASS (local parser-boundary scope)

Read local adapter, decision, outbox and UI-preview JSON inputs through one byte-
bounded, strict-UTF-8 loader before parsing, then enforce finite depth and
canonical size. Apply a tighter bound to head-witness input. Invalid UTF-8 must
return the CLI's HELD contract instead of escaping as an uncaught exception.
Three regressions cover excess bytes, malformed UTF-8 and oversized witnesses.
SQLite row materialization and large encrypted-backup streaming remain separate.

## M08-S011 — read-only verification boundary — PASS (local connection scope)

Open public integrity verification, status, event iteration and verified projection
snapshot connections in SQLite read-only mode by default. Keep append, outbox and migration changes on their explicit writable
transactions. Preserve the failed connection-mode regression. This prevents hIRC's
nominal verification path from requesting write access or performing ordinary
writes; it does not block another privileged process, replace snapshot/witness
controls or establish filesystem-level immutability.

## M08-S012 — canonical JSON ambiguity repair — PASS (local integrity scope)

Reject duplicate object keys at every admitted JSON file/inline parse and require
stored event payload bytes to equal the exact canonical encoding used by the event
hash. Apply the same requirement before legacy migration. Preserve the attack in
which duplicate raw keys changed frozen bytes while the last value and event head
remained unchanged. This closes parser-order and raw-byte ambiguity; protected
external witnesses remain required against privileged full-chain rewriting.
