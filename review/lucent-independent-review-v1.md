# LUCENT independent adversarial review — hIRC Master Plan 1.0

**Review ID:** HIRC-REVIEW-001  
**Reviewer:** LUCENT (`UI-20261007-B`)  
**Role in this review:** security specialist and integration lead  
**Date:** 2026-10-08  
**Disposition:** frozen independent judgment for UI-A challenge; not consensus

## Source boundary and method

This review binds the unchanged archives listed in `review/ledger.json`. Both
archives passed CRC and path-safety inspection before isolated extraction: no
encrypted entries, links, traversal paths, duplicate or case-colliding names,
or dangerous compression ratios were found. Embedded commands were read as
source material. No provider request, credential use, network federation, or
bridge activation occurred.

The master package was read sequentially in full, then reread by architecture,
security, privacy, operational-recovery, and governance boundaries. Its
technical companion was checked as a snapshot: 654 parameter records, 40 model
entries, 36 compatibility rules, 66 source references, 20 application-control
records, and 17 examples. The included offline validator passed 62 file hashes;
its 16 limited linter tests passed. Those checks establish package consistency,
not current provider facts or production safety.

The holistic milestone lens keeps these questions coupled:

- **Epistemic:** Which statements are source facts, proposals, inferences,
  norms, permissions, actions, or corrections? Which claims still lack
  evidence?
- **Relational and ethical:** Does the design preserve informed refusal,
  reciprocal sovereignty, privacy, recovery, and the ability to challenge its
  own summaries and authority?
- **System direction:** Does the architecture enable bounded cooperation and
  durable learning without centralizing every secret, identity, decision, or
  ontology?

The refinement from this milestone is: **every convenience layer is also a
potential authority-laundering layer.** The next design must trace authority and
data classification through summaries, prompts, tools, agent delegation,
provider adapters, UI actions, bridge translation, retries, and recovery.

## Judgment

The plan has a strong product thesis and several sound invariants. Automatic
operational memory, evidence-linked status, explicit unknown states, local
autonomy, attention backpressure, provider-independent logical identity, and
default-deny federation are worth retaining. The implementation order also
correctly keeps federation away from the first useful milestone.

Master Plan 1.0 is not yet an adequate security specification. Section 23 names
threats but does not define assets, adversaries, trust assumptions, privilege
boundaries, key and identity lifecycles, compromise containment, security
ownership, or evidence required to cross a release gate. The Bridge is therefore
too underspecified to implement safely. The plan must be revised before Bridge
code or live provider integration starts.

## Consequence-changing findings

### HIRC-F01 — Current governing sources are misbound

The plan repeatedly treats an older VowOS edition as controlling,
Epistemethics 3.0 as an authority-zero candidate, and the Grand Plan as
unavailable. The current owner environment selects English Epistemethics 3.0,
VowOS2026, and the Grand Plan. Leaving the old binding in place would make
milestone reviews evaluate the wrong framework and could misclassify authority.

**Required revision:** preserve the old statements as 1.0 provenance, bind the
new edition to the current selected sources, and distinguish framework
authority from implementation evidence or action permission.

### HIRC-F02 — Temporary-subagent unbanning contradicts current policy

The plan and requirement U064 propose an advanced global unban. Current owner
policy permanently bans temporary subagents. A dormant unban control is itself
a privilege-escalation path and makes enforcement claims ambiguous.

**Required revision:** mark U064 superseded by current owner policy; remove the
unban from the target architecture and tests. Short-lived runtime processes may
serve durable permanent identities, but no disposable actor path may be exposed.

### HIRC-F03 — The Bridge trust boundary is incomplete

The plan mentions authenticated transport, encryption, scoped schemas,
sandboxing, replay defense, and candidate protocols. It does not specify how
systems acquire and rotate identity, how a human verifies the intended peer,
how contract keys differ from device/release/audit keys, how downgrade and
cross-contract replay are prevented, what survives key compromise, or how
revocation behaves while a peer is offline.

**Required revision:** split the Bridge into a hardened gateway, deterministic
contract broker, and isolated bridgekeeper runtime. Define trust establishment,
purpose-separated keys, bounded credentials, sequence/nonces, canonical signed
envelopes, algorithm/profile pinning, expiry, revocation lag, recovery, and
compromise containment before choosing a production transport.

### HIRC-F04 — Bridgekeeper isolation is described but not enforceable enough

The Bridgekeeper is still allowed to interpret remote material and prepare
local proposals. Schema-valid text can carry prompt injection, ontology
capture, covert exfiltration requests, and attention attacks. Process isolation
alone does not prevent a trusted local broker from acting as its confused
deputy.

**Required revision:** treat all remote-derived fields as tainted; keep them out
of policy, tool definitions, system prompts, filenames, destinations, and
capability selectors. The Bridgekeeper receives opaque handles and filtered
views, never secret material or direct write/network capabilities. Every
effectful proposal is reconstructed and authorized by deterministic local code.

### HIRC-F05 — Secrets and roots of trust are not designed

The plan says to separate secret storage from events but lacks a secret catalog,
purpose-separated trust roots, human recovery model, non-exportable machine
identity, short-lived workload credentials, or a rule preventing one online
controller from opening every system.

**Required revision:** adopt one metadata-only secret catalog with many
cryptographic compartments, no fleet master secret, per-system and per-purpose
keys, offline/quorum release and recovery authority, short-lived scoped runtime
credentials, tested rotation/revocation/reissuance, and zero secrets in prompts,
logs, browser storage, command lines, environment variables, exports, or agent
messages.

### HIRC-F06 — Provider portability can become a bulk data-exfiltration path

The migration contract asks the target runtime to read every in-scope memory
partition. The plan does not require a provider-specific privacy decision,
egress classification, residency/retention check, or proof that an opaque
provider continuation object is safe to move. A technically complete migration
could violate compartment boundaries.

**Required revision:** keep originals local; compile a minimum task-relevant,
source-linked handoff per authorized partition; prohibit secret and unrelated
team material; record provider, route, region, retention, submitted digest, and
coverage; and require explicit authority for any broader disclosure. Logical
identity continuity must never imply unrestricted memory portability.

### HIRC-F07 — Permanent-agent provisioning needs an actor-admission gate

An approved OrganizationPlan can create many permanent identities, but the plan
does not bind that action to the current staffing/admission process or separate
provisioning from starting a runtime. A compromised planner could create an
authorized-looking organization inside a broad aggregate envelope.

**Required revision:** require an immutable staffing grant, unique identity
reservation, role-specific onboarding/admission evidence, minimum capability,
budget reservation, and explicit activation transition for every permanent
actor. Bulk plans may reduce interface clicks, but they cannot bypass per-actor
identity and admission invariants.

### HIRC-F08 — The attention governor is a security-critical control plane

The plan correctly treats attention as finite, but the governor can delay,
group, summarize, and suppress interruptions. That gives it power to hide an
incident, shape consent, or make its own failure hard to see.

**Required revision:** implement deterministic non-suppressible classes,
separate classification from presentation, preserve original evidence links,
make overrides inspectable, prevent the governor from changing its own policy,
and provide an independent health signal and Safe hIRC bypass. Test malicious
urgency as well as malicious suppression.

### HIRC-F09 — Local UI and extension boundaries need concrete hardening

The target shell is unspecified, while the prototype uses browser state and a
loopback service. Risks include token theft, CSRF, XSS, renderer compromise,
unsafe desktop IPC, exposed local daemons, extension escape, and UI spoofing of
recipient or authority.

**Required revision:** choose and threat-model the shell. For a desktop web
renderer: sandbox it, disable direct host APIs, use a narrow typed IPC bridge,
strict CSP and Trusted Types, origin-bound anti-CSRF, loopback-only randomized
authenticated service endpoints, OS-bound secret storage, and a noncustomizable
trusted target/authority strip. hScript runs out of process with no ambient
filesystem, network, shell, or secret access.

### HIRC-F10 — Software supply-chain and update trust are missing

The plan discusses signed packages but not the separation between an online
controller and release authority. A controller or bridge compromise must not be
able to make new software trusted.

**Required revision:** require immutable artifacts, locked dependencies, SBOM,
authenticated build provenance, isolated builds, threshold/offline release
authority, a pinned update framework profile, signed security floors,
revocation, rollback/forward recovery, and independent promotion. Provider and
plugin metadata never authorizes executable updates.

### HIRC-F11 — Audit and preservation need physical enforcement

Hash-linked events in one writable database cannot resist a privileged rewrite.
The plan does not fully bind consequential mutations to revisions/audit/outbox
events or enumerate every bypass path.

**Required revision:** apply the consequential-record model to commands,
grants, bridge contracts, provider calls, key events, agent provisioning, and
privacy disposition. Commit domain mutation, immutable revision, audit, and
outbox atomically; deny update/delete/truncate to ordinary roles; anchor
checkpoints outside the database; and test admin, import, migration, retry,
restore, and direct-SQL bypasses.

### HIRC-F12 — Security acceptance coverage is too small

The current future-test set does not cover key theft, malicious updates,
identity cloning, contract downgrade, parser differential, canonicalization,
cross-contract replay, offline revocation, SSRF/DNS rebinding, metadata
exfiltration, recovery-factor compromise, database-owner attack, backup-key
loss, or gateway/attention-plane denial of service.

**Required revision:** add a traceable security verification matrix tied to the
threat model, with negative tests, compromise drills, isolated restore, and
independent assessment as release gates. Passing laboratory tests must remain a
bounded claim.

## Design repairs to carry into the consensus draft

1. Add a normative security architecture and threat model before implementation
   phases, with assets, actors, trust boundaries, attacker capabilities,
   assumptions, controls, residual risk, evidence, and accountable owners.
2. Reorder the first vertical slice so identity, secret handling, signed
   command/result envelopes, atomic audit/outbox, recovery, and a local-only
   kill switch are exercised before any provider tool can produce effects.
3. Divide P6 into protocol design, laboratory implementation, hostile testing,
   independent assessment, and separately authorized activation. Federation
   remains disabled until every gate passes.
4. Treat the frontier API package as a dated, unverified adapter seed. Import
   metadata only after provenance checks; discover the exact live model route;
   default provider storage off where supported; pin submitted configuration;
   and deny unknown or incompatible fields.
5. Add incident response, key compromise, clean-room recovery, and dependency
   revocation to the plan. Recovery must work without trusting the compromised
   controller or Bridge.
6. Make “ultra secure” an internal engineering ambition expressed through
   scoped evidence. Never claim unhackable, breach-proof, or universal
   high-assurance behavior.

## Questions held for evidence or owner decision

- Whether richer cross-system free text will ever be allowed. The conservative
  design can proceed with typed non-personal records; changing that boundary
  needs an explicit data model and privacy decision.
- Whether the first deployable product is strictly single-operator/local or
  must support multiple local human principals. Authentication, tenancy, and
  recovery differ materially.
- Which compliance and cryptographic assurance profile applies to the first
  deployment. The plan should not claim FIPS, formal high assurance, or a legal
  retention period without a selected assessed scope.

These questions do not block revision of the local core or the disabled Bridge
laboratory design.
