# hIRC Milestone 03 completion report

**Milestone state:** PASS; public content and receipt commits verified
**Branch:** `codex/hirc-master-plan-security`
**Baseline before this milestone:** `1c525e3b464c58b6e037faaf6bb76626b32364e4`

## Delivered

Milestone 03 integrates the current hIRC direction into one evidence-linked design
and a bounded local executable alpha. The architecture treats onboarding,
participant sovereignty, refusal, correction, successor continuity, evolving
trust, deterministic invariants and governed learning as foundation behavior.
Ordinary interface copy remains plain; exact framework names, hashes and protocol
details stay in engineering and audit views.

The local alpha now includes an append-only SQLite event store, deterministic
work/recovery projections, permanent-participant formation records, no-effect
decision and interruption previews, a local provider-neutral adapter, an atomic
no-dispatch outbox, backup/restore, migration hardening, encrypted-backup and
release-signing tools, an external head witness, a reproducible Python zipapp and
a read-only HTML briefing.

## Review and repair

The integrated product review repaired three material contract and portability
issues. Metric/evaluator review advanced the candidate reliance contract through
three repair rounds, 2 valid controls and 27 adverse cases; all findings close at
synthetic candidate-contract scope. The correction history preserves a reviewer
decoding mistake rather than mislabeling valid UTF-8 JSON as corruption.

Security/privacy/dataflow review produced four source-level findings:

1. outbox stages could commit under a different request or information boundary;
2. store verification could accept impossible correction histories after a local rehash;
3. adapter validation accepted self-rehashed malformed envelopes; and
4. direct adapter validation canonicalized oversized input before applying bounds.

All four are repaired and independently rechecked at static local source-integrity
scope. The final adapter path applies cheap shape and disabled-capability checks,
then bounds payload structure and UTF-8 size before whole-request canonicalization.

## Verification

- 21 milestone validators pass from fresh execution.
- 140 source-tree tests pass.
- 3 expected release failures remain explicit.
- The developer package is byte-reproducible and contains only declared code and its manifest.
- Package: `dist/hirc-local-0.1.0.dev0.pyz` — `2976bbafddb17c66800fa9d7fb3645c2eda8625db62fe8a0a08a4b2c4657c1e1` — 38349 bytes.
- Cumulative validation: `ca639035b2e60e9cb4d825b215f183ea797b62f9f62b1701cbcac9b9405ceb9c` — 10637 bytes.
- S014 is PASS; S015 final publication work is active.

One flaky encrypted-backup adverse test was found during replay: it sometimes
replaced the first Base64 character with the same character. The failed run is
preserved internally; the test now always chooses a different character and the
complete validator chain passes.

## Publication privacy

The public manifest excludes native chat identifiers, private runtime paths,
personal education records, internal delivery metadata, caches, temporary stores,
credentials and secret-shaped material. Public team and review pages contain only
the bounded technical status needed to understand the milestone.

## Remaining limits

This milestone does not establish empirical usability or accessibility, affected-
party privacy outcomes, deployed external witness custody, encrypted live storage,
physical durability, real multiuser audience enforcement, arbitrary adapter
isolation, Bridge safety, penetration or cryptographic assurance, production
readiness, release readiness or the absence of unknown vulnerabilities.

The three expected release failures keep external truncation witnessing,
encrypted-at-rest live storage and independently verifiable package signing open.
Bridge, network, production, sensitive-data and release capabilities remain off.

## Remote closure

The privacy-validated content commit is
`df5b72713f0127e0789652f20870709827441c9f`. A direct `git ls-remote` query
observed the public branch at that exact commit after the push. The public receipt
commit is `cc4af0dbd6c02cedf49ed1ea1e3da30732e0a4cf`; a second direct query
observed the branch at that receipt commit. S015 is therefore PASS. The containing
closure commit records this already-satisfied condition; a push request was never
treated as proof that the remote changed.
