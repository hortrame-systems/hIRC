# LUCENT review supplement 1

**Artifact ID:** HIRC-REVIEW-001-S1  
**Predecessor:** HIRC-REVIEW-001, preserved unchanged  
**Status:** attributable supplement for peer challenge

## Source-completeness correction

Master Plan 1.0 and its audit annex bind hashes for the inspected Relay/hIRC
prototype archives, HTML, prior plan, and logo, but those source objects are not
members of `hirc_master_plan_v1_0.zip`. The package contains test output and
fingerprints only. The reported 73 bounded tests therefore remain source-report
evidence in this workspace; they cannot be independently rerun or tied to
locally available code from this transfer alone.

This does not show that the reported tests failed or were fabricated. It changes
the evidence category and the next action. A revised plan must mark the prototype
baseline `NOT_VERIFIED_IN_TRANSFER`, import the exact hashed objects through the
proper source/ledger route if they are available, and rerun from immutable source
before relying on the prototype as an executable baseline.

## New owner requirement after the independent freeze

HIRC-I001 changes the architecture, not merely wording. Master Plan 1.0 treats
prompt policy and onboarding rollout as replaceable modules delivered in P4.
The owner now requires the complete selected formation and governing semantics
to constitute hIRC's foundation while remaining unobtrusive in ordinary product
language and capable of governed real-time evolution.

The consensus revision must therefore move the active foundation binding,
semantic model, compiled invariants, agent formation, milestone reflection, and
version-transition mechanism into P0/P1 and the trusted core. Later onboarding
rollouts remain distribution and integration mechanisms for a new foundation
version; they are not where the foundation begins.

The initial LUCENT interpretation is recorded separately in
`foundation-kernel-candidate-v1.md`. It is an implementation proposal, not a
claim that the owner specified its internal mechanism.

## Current security-reference correction

The transport candidate must reference the current TLS 1.3 specification, RFC
9846, which obsoletes RFC 8446 while retaining TLS version 1.3. Among other
clarifications it forbids KeyShare reuse, tightens key-update requirements, and
updates privacy considerations. The application profile still must specify peer
identity verification and must disable replay-sensitive 0-RTT operations.

