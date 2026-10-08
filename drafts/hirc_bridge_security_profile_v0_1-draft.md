# hIRC Bridge security profile 0.1 — disabled working draft

**Status:** design-only, disabled, pending joint consensus, protocol ADRs,
hostile-lab evidence and independent assessment  
**Scope:** system-to-system federation boundary  
**Rule:** no public advertisement, enrollment, network listener, remote message or
effect is authorized by this document

## 1. Security posture

The Bridge is hIRC's highest external exposure. It combines hostile network
input, remote identities, protocol parsing, semantic translation, privacy,
ontology mismatch and potential local effects. It receives extra precautions,
but it is not automatically the highest-consequence component: foundation,
release, recovery, journal and evaluator roots may have larger internal blast
radius and remain unreachable from Bridge authority.

Federation is optional. Local hIRC remains useful and recoverable without it.
Connection never means membership, shared ontology, inherited authority,
permission, trust, source admission or access to local rooms/memory.

## 2. Four-component boundary

### 2.1 Network gateway

Owns transport termination, peer endpoint identity evidence, coarse protocol/
size/rate limits and network telemetry. It cannot interpret business meaning,
release local data or access the core database/secrets beyond its transport
keys.

### 2.2 Deterministic contract broker

Owns canonical envelope parsing, schema/version, signature, sender/recipient,
contract, sequence/nonce/expiry, replay, purpose/data-class, quota and downgrade
checks. It produces typed input for the bridgekeeper and rejects anything
outside the exact contract. It has no user/model semantic discretion.

### 2.3 Isolated bridgekeeper

Owns only bounded semantic translation, ambiguity detection and local/remote
ontology mapping for an admitted contract. It receives minimized fields, no
transport/signing/release keys, no unrelated rooms/memory, no arbitrary network
or filesystem and no capability to dispatch a local effect. Its output is a
proposal under a strict schema.

### 2.4 Local release/ingress gate

Owns final local decision: admit/reject/quarantine inbound data; release/deny
outbound fields; offer/deny local work; and request actual human authority where
needed. It rechecks current foundation, privacy, authority, consent, data class,
purpose, contract, taint, quotas and effect boundaries. The remote system cannot
override it.

Each component has a separate workload identity, process/container boundary,
least-privilege capability, log/data partition and compromise response. No one
Bridge component holds all peer identity, content, release and recovery powers.

## 3. Bridge lifecycle

```text
UNSEEN
  -> ADVERTISED
  -> INVITED
  -> IDENTITY_VERIFICATION
  -> CONTRACT_PROPOSED
  -> LOCALLY_APPROVED
  -> REMOTELY_ACCEPTED
  -> ENROLLED
  -> ACTIVE
  -> SUSPENDED | REVOKED | COMPROMISED | EXITED
```

Public advertisement is a minimal capability statement, not connection.
Enrollment requires exact peer/system identity, out-of-band fingerprint or trust
anchor verification, contract negotiation, current human/system authority and
local acceptance. Every transition is append-only and idempotent.

Contract renewal or material field/purpose/version/key change starts a new
review. Suspension blocks new application messages while preserving evidence and
safe exit. Revocation cannot erase messages already disclosed or instantly reach
an offline peer; UI and incident response state that residual.

## 4. Peer identity and enrollment

`PeerIdentity` binds:

- locally assigned peer/system ID and remote asserted ID;
- organization/system display information as untrusted metadata;
- enrollment public keys/certificates and purpose-separated message keys;
- out-of-band verification method, verifier, time and evidence;
- endpoint/transport profile and permitted network locations;
- contract IDs/versions, allowed roles/purposes/data/effects;
- key validity, rotation, revocation and compromise state; and
- local owner, review date and exit/recovery route.

Web PKI or transport certificate alone does not establish the intended peer.
Out-of-band confirmation prevents a valid certificate for the wrong endpoint
from becoming local membership. Enrollment material never grants user, agent,
release, recovery or foundation identity.

Peer keys are unique to one system and purpose. Sharing keys across peers,
production/test, identity/message, release/update, entitlement or recovery is
prohibited. Private keys stay in the narrow component that needs them and use
hardware-backed/nonexportable storage where the chosen platform supports it.

## 5. Transport profile

The final ADR must pin a current reviewed TLS 1.3 profile and library versions,
mutual peer authentication or equivalent binding, cipher/signature policy,
certificate/key rotation, revocation behavior and downgrade floor. Do not invent
cryptography.

Requirements independent of the selected library:

- no plaintext or opportunistic downgrade;
- state-changing/replay-sensitive application messages never use 0-RTT;
- strict endpoint/hostname/identity pin and certificate validation;
- transport identity is bound to the enrolled PeerIdentity and contract;
- connection limits, handshake/resource controls and failure backoff;
- no transparent redirect to an unverified endpoint;
- transport session resumption cannot bypass current revocation/contract state;
  and
- transport confidentiality does not replace signed canonical application
  envelopes and local release checks.

Group messaging, if ever admitted, uses a reviewed standard group-security
protocol and independent membership/epoch semantics. It is not simulated by
sharing one bilateral key.

## 6. Canonical application envelope

One ADR selects a canonical, testable encoding and signature profile. The
encoding must have one valid representation for signed fields or a precisely
specified canonicalization with differential tests. Ambiguous duplicate keys,
unknown critical fields, invalid Unicode, number/date variants and parser
disagreement are rejected.

Every envelope binds at least:

- protocol and envelope version;
- contract ID/version and schema ID/digest;
- sender system/workload identity and recipient system/endpoint;
- message ID, conversation/causal references and idempotency key;
- per-contract direction sequence and random nonce;
- issued, not-before and expiry times with declared clock tolerance;
- message type, purpose and requested disposition;
- field-level data classes, retention/disposition and derived-data policy;
- payload digest and exact signed protected header set;
- sender key ID/algorithm/profile;
- optional reply-to only within enrolled verified endpoints; and
- signature or message-authentication proof.

Signatures cover every field that changes meaning, recipient, purpose,
authority, privacy or replay. Detached payloads are content-addressed and carry
the same authorization/classification; a digest is not permission to fetch.

Unknown critical versions/fields fail closed. Noncritical extension fields are
allowed only where the contract explicitly says they can be ignored.

## 7. Contract model

`BridgeContract` is bilateral/local-admitted and versioned. It defines:

- exact peers and endpoints;
- purpose and explicitly excluded purposes;
- message types and schemas;
- field allowlists, data classification and transformations;
- origin/ownership, consent and affected-party conditions;
- inbound/outbound storage, retention, deletion and derived-data rules;
- model/provider/processor egress, usually none by default;
- permitted work offers and local effect ceiling;
- quotas for messages, bytes, attachments, compute and operator attention;
- sequence/replay window and offline/resynchronization behavior;
- error disclosures and privacy-safe diagnostics;
- key/contract rotation and revocation;
- suspension, exit, residual data and recovery; and
- tests, expiry, reviewers and reassessment triggers.

First profile: structured coordination tokens only. No arbitrary remote free
text, code, files, prompts, tools, memory objects, provider continuation state,
secrets, credentials, human dossiers or Bridge-delivered commands.

A contract is not proof that the remote system follows it. Local hIRC limits its
own disclosures/effects and records the residual reliance on remote handling.

## 8. Inbound pipeline

```text
network bytes
 -> gateway transport/peer/size/rate check
 -> broker framing/canonical/schema/signature/contract check
 -> sequence/nonce/expiry/replay/downgrade check
 -> field/purpose/data-class/retention admission
 -> quarantine or minimized bridgekeeper input
 -> typed translation + ambiguity/non-equivalence report
 -> local release/ingress policy and authority check
 -> admitted local event, work offer, refusal or quarantine
 -> signed/contract-bounded result where permitted
```

No unvalidated raw payload reaches model context, ordinary logs, search, memory,
provider adapter or action broker. Rejections use non-content diagnostics unless
forensic retention is specifically admitted and isolated. Malicious content in
an otherwise signed peer message remains hostile.

Bridgekeeper output contains source envelope reference, exact fields consumed,
translation version, local/remote ontology mappings, losses/ambiguities,
confidence/unknowns and proposed typed local object. It cannot claim remote
authority or fabricate agreement.

## 9. Outbound pipeline

```text
local proposal
 -> local identity/authority/participation/action disposition
 -> contract/purpose/recipient selection
 -> field-level privacy and derived-data egress
 -> minimized payload and translation
 -> trusted preview for consequential disclosure/effect
 -> local release gate
 -> canonical signed envelope
 -> gateway dispatch
 -> remote receipt/result as report
 -> observed local consequence or explicit unknown
```

Recipient, purpose, data classes, retention, cost and remote processor appear on
the broker-authored trusted preview. A remote acknowledgement is not an observed
external result. Retry uses idempotency and reconciliation, never blind replay.

## 10. Replay, ordering and time

Each direction/contract has a monotonic sequence with bounded resynchronization,
random nonce and replay cache. Sequence gaps, duplicates, old epochs, expired
messages and excessive future skew hold or reject according to the contract.

Wall-clock time is not a universal total order. Record sender issue time, gateway
observation, broker validation, local commit and effective time plus causal
links. Trusted-time failure narrows accepted windows or suspends the Bridge; it
does not accept timeless effects.

## 11. Key lifecycle

Key classes are separate for enrollment identity, transport, message signing/
authentication and any future group membership. Each has creation provenance,
algorithm/profile, public identity, permitted use, validity, rotation overlap,
revocation and destruction/recovery policy.

Rotation is an authenticated state transition under the current key plus
out-of-band or recovery evidence where risk warrants. A peer compromise can
revoke/suspend locally immediately; offline remote acceptance may lag. Past
signatures remain attributable without keeping compromised keys active.

Loss of all peer keys does not grant a new identity automatically. Re-enrollment
is a new high-risk case with old contract suspension and duplicate-identity
checks.

## 12. Privacy and metadata

Public directory records contain only reviewed minimal fields and expire.
Private connection attempts, peer lists, traffic volumes, timing, contract
names, error details and recipient relationships are sensitive metadata.

Controls include:

- minimum advertisements and no global membership roster;
- field/purpose allowlists and no free-text first profile;
- padding/batching or timing reduction only where measured benefit justifies
  cost, without claiming traffic-analysis elimination;
- separate public/private endpoints where helpful;
- no remote search across local rooms/memory;
- no unsolicited analytics or content-rich rejection logs;
- retention/deletion and derived-data contracts; and
- no cross-peer correlation identifier beyond what an exact contract requires.

## 13. Bridgekeeper isolation

Bridgekeeper runtime uses a minimal image, read-only base, ephemeral workspace,
no shell/package manager in production, narrow broker IPC, no arbitrary network,
no local secret/data mounts, bounded CPU/memory/time/output and a fresh or
carefully scoped context per contract/message class.

Training/formation binds only required public/contract/local interface material.
It does not receive whole owner/team/client sources merely because it is local.
Prompts are data and remain subordinate to broker/release gates. Model refusal or
acceptance does not determine envelope validity.

Bridgekeeper compromise is assumed possible. It must not forge signed remote
input, modify contracts, see release keys, write local memory directly, dispatch
effects or broaden its next invocation.

## 14. Quarantine, refusal and errors

Invalid, suspicious or ambiguous input goes to bounded quarantine with content
access limited by purpose. A denial records reason codes and source identifiers
without echoing private payload. Remote peers receive only contract-permitted
error detail.

Repeated invalid messages cannot force operator alerts. Rate/attention governor
groups attempts while preserving distinct attack/source/effect evidence.
Security-critical compromise or valid high-impact ambiguity reaches the local
operator through an independent class.

Refusal is local and nonretaliatory. The peer may correct and resubmit under
contract; hIRC may suspend or exit after evidence-based thresholds. A peer's
refusal is respected and not bypassed via another endpoint or identity.

## 15. Compromise containment and exit

On suspected compromise:

1. suspend affected peer/contract/key/message classes;
2. preserve transport/broker/release evidence and uncertainty;
3. revoke local acceptance and outbound release immediately;
4. fence queued/retried effects and reconcile unknowns;
5. assess data disclosed, data received, local objects/effects and derived
   copies;
6. rotate/re-enroll only through verified recovery;
7. restore broker/gateway/bridgekeeper from known-good artifacts;
8. retest hostile cases and contract compatibility; and
9. notify/repair within actual obligations without claiming remote deletion.

Exit disables new messages, resolves or holds queued work, exports permitted
evidence, applies local retention/disposition, records remote residuals and keeps
local hIRC functional. Remote dependence cannot become data hostage.

## 16. Hostile test corpus

Required offline/lab cases include:

- wrong peer/endpoint/key/contract/recipient/purpose;
- invalid, duplicate, reordered, skipped, stale, future and replayed sequence/
  nonce/time;
- signature wrapping, unknown critical field and canonicalization/parser
  differentials;
- malformed Unicode, numbers, dates, nesting, compression and oversized fields;
- contract/version/profile downgrade or fork;
- stolen/rotated/revoked/lost keys and overlapping rotation;
- malicious free text/code/tool/prompt/credential/secret/private-room data;
- bridgekeeper prompt injection, output-schema escape and resource exhaustion;
- SSRF/redirect/DNS rebinding and unverified endpoint changes;
- quarantine/log/search/provider leakage;
- traffic/metadata and public-directory enumeration;
- alert/attention flooding and repeated grievance/rephrasing;
- ambiguous remote acknowledgement and retry duplication;
- federation partition and conflicting histories;
- gateway, broker, bridgekeeper and release-gate compromise independently;
- clean restore with outstanding sequences/contracts/unknown effects; and
- local operation, exit and recovery with remote peer permanently unavailable;
- missing stage-5 independent assessment blocks a live pilot;
- an explicitly authorized stage-6 pilot can start without already being
  complete, and its evidence cannot self-authorize stage 7; and
- admitted owner-private formation succeeds only for the exact current
  participant/purpose/reader tuple while wrong/revoked tuples, ordinary
  provider/client/Bridge disclosure and every credential/private-key value are
  rejected.

Each test binds exact protocol, schema, parser, crypto library, platform, seed,
expected/actual result, artifacts and claim affected.

## 17. Activation gates

1. **Specification:** contract/envelope/state/key/privacy/error profiles and
   threat/test trace reviewed.
2. **Offline conformance:** deterministic parser/canonical/signature/replay and
   adverse corpus pass across every implementation.
3. **Two-system lab:** enrollment, rotation, outage, reconcile, refusal, exit and
   recovery with synthetic data/effects.
4. **Hostile lab:** malicious peer/content/network/key/parser/attention/resource
   cases and compromise recovery.
5. **Independent assessment:** protocol, crypto use, implementation, privacy,
   product consent and recovery by qualified independent reviewers.
6. **Bounded pilot:** explicit peers, structured fields, no free text, strict
   quotas/effect ceiling, operator stop and measured residuals.
7. **Broader activation:** separate owner decision based on pilot evidence and
   unresolved risks.

Every applicable stage must pass. A schema fixture or persuasive diagram is not
Bridge readiness.

## 18. Open profile decisions

- canonical envelope encoding/signature/profile and implementations;
- TLS library/profile, certificate model and key storage per platform;
- pairwise versus future group-message scope;
- public directory transport, operator and abuse controls;
- trusted time and replay-cache durability/resynchronization;
- metadata protection/padding cost and threat target;
- first-pilot message types, field allowlist, retention and effect ceiling;
- bridgekeeper runtime/model and isolation technology;
- independent assessors and acceptance criteria; and
- re-enrollment and remote-deletion evidence policy.
