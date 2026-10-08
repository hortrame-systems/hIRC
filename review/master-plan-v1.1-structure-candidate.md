# hIRC Master Plan 1.1 — proposed structure

**Artifact ID:** HIRC-MASTER-STRUCTURE-CANDIDATE-001  
**Status:** frozen candidate for UI-A challenge; not the revised master  
**Base:** Master Plan 1.0 plus HIRC-I001–I006 and HIRC-REVISION-MAP-CANDIDATE-001

The 1.0 product thesis and useful interaction detail should remain. The 1.1
revision changes the causal order: the governing foundation, threat model,
identity, secrets, audit, and recovery precede provider effects, permanent-agent
activation, extensions, and federation.

## Proposed master sections

### 00. Document contract, exact sources, and claim states

Bind the immutable 1.0 archive, current owner intent, current selected
foundation sources, this revision, requirements, threat model, and evidence.
Define `SOURCE_REPORTED`, `LOCALLY_VERIFIED`, `PROPOSED`, `HELD`, and
`NOT_VERIFIED_IN_TRANSFER`. Preserve the old constitutional/source statements as
1.0 history rather than repeating them as current authority.

### 01. Product definition and acceptance objective

Retain hIRC as local-first operational memory and coordination with a classic
IRC interaction surface. Add that the system's formation, evidence, authority,
privacy, refusal, correction, autonomy, recovery, and learning behavior comes
from one active foundation across every feature.

### 02. Non-negotiable system invariants

Retain the useful 1.0 invariants and add: exact active foundation binding; no
temporary-subagent path; no online universal root or fleet secret; no controller
software-signing authority; no secret in prompt/log/browser/export; independent
security visibility; and no self-authorized evaluator/foundation change.

### 03. Foundation-native architecture

Specify the exact source corpus, semantic model, whole-source coverage map,
compiled contracts, deterministic foundation kernel, permanent-agent formation,
plain-language presentation, evidence/correction history, live version
transition, and milestone reflection. Explain why this is the substrate rather
than an onboarding add-on or prompt pack.

### 04. System threat model and trust domains

Name assets, adversaries, assumptions, trust domains, blast radii, residual
risks, security owners, and the security-claim discipline. Distinguish the
Bridge as highest external exposure from foundation/release/recovery roots as
highest-consequence internal targets.

### 05. Actual prototype and transfer evidence

Retain the factual 1.0 functionality table. Correct the status of the 73 tests:
their outputs and source hashes are present, but the fingerprinted source
objects are absent from this transfer and cannot be rerun here. Keep the
prototype local/laboratory disposition.

### 06. Requirements, ideas, decisions, and correction discipline

Bind the canonical intent register and requirements 1.1. Preserve original user
meaning, interpretations, supersessions, open conflicts, acceptance, and
evidence. Add U120–U122. Mark U064 superseded by the permanent temporary-subagent
ban. Require each accepted architectural choice to have one ADR owner.

### 07. Privacy and data lifecycle before ingestion or egress

Keep the two 1.0 privacy boundaries. Add field-level purpose, authority,
controller/owner, processor, residency, retention, disposition, egress, and
derived-data inheritance. State the unavoidable bounded transient processing at
an ingress gate without relabelling receipt as no collection. Keep remote free
text disabled in the first bridge profile.

### 08. Small trusted core and execution path

Define the deterministic foundation/security kernel, typed command API, policy
decision and enforcement points, privacy/egress admission, secret broker,
execution broker, consequential journal/outbox, and recovery bootstrap. Models,
UI, scripts, adapters, and bridgekeepers only propose through this path.

### 09. Identity, human authentication, secrets, and recovery roots

Specify phishing-resistant human access, strongest-path recovery, unique
system/workload/agent identities, short-lived scoped credentials, purpose- and
system-separated keys, value-free secret catalog, rotation/revocation,
independent release and recovery roots, and clean-room recovery.

### 10. Recursive organization and permanent-agent formation

Retain teams, memberships, rooms, identity permanence, reservations, and
aggregate resource envelopes. Separate OrganizationPlan approval from every
permanent identity's reservation, formation, admission, minimum capability,
budget allocation, and activation. Delete the advanced temporary-subagent
unban.

### 11. Work, evidence, commitments, and automatic reconstruction

Retain the canonical work model, orthogonal state dimensions, source-native
events, coverage honesty, dependency propagation, and attributable correction.
Apply atomic revision/audit/outbox rules at the earliest consequence boundary.

### 12. Attention, context, and security visibility

Retain bookmarks, reversible navigation, decision cards, batching, and
backpressure. Separate matter classification, delivery policy, and presentation.
Add non-suppressible security classes, independent health, anti-coercion tests,
and Safe hIRC access to the unsummarized security queue.

### 13. Visual shell and trusted interaction boundary

Retain the classic hIRC visual requirements, independent windows, accessibility,
themes, and stable spatial behavior. Add shell selection as an ADR; renderer
sandboxing, narrow typed IPC, origin/navigation controls, injection defenses,
loopback protection, and an unspoofable identity/recipient/data/authority strip.

### 14. Communication routing and message truth states

Retain explicit recipients, room boundaries, authorized overlays, causal order,
and delivery/receipt/acknowledgement/action distinctions. Add policy enforcement
at every fan-out and prevent replayed history from becoming a new command.

### 15. Scheduling, execution epochs, and resource budgets

Retain one consequential execution per logical agent by default, atomic leases,
fencing, queue aging, and attention/resource backpressure. Add credential and
grant expiry, recovery after unknown external outcomes, and no concurrency
increase without memory/tool/commit isolation evidence.

### 16. Provider adapters, configuration, and egress

Use the frontier package only as a dated candidate seed. Require exact
provider/host/route/model/version/region/account/retention identity, live bounded
probes, namespaced fields, strict compatibility, minimal payload manifests,
local tool authorization, actual configuration receipts, cost envelopes, and
privacy-preserving fallback.

### 17. Durable memory and secure model migration

Retain local originals and compartmented memory. Replace “target reads every
partition” with local whole-source coverage plus the minimum permitted,
source-linked handoff for each target route. Provider-native opaque items stay
in provider branches. Identity continuity never implies identical cognition or
unrestricted data portability.

### 18. Foundation policies, prompts, formation, and live rollouts

Fold former prompt/onboarding sections under the foundation architecture.
Prompts remain model-facing compiled inputs, not the authority boundary.
Rollouts distribute and integrate a new foundation or role version with exact
coverage, compatibility, safe-boundary activation, critical immediate
revocations, canaries, rollback/forward recovery, and per-identity evidence.

### 19. hScript, plugins, and safe extensibility

Retain the familiar scripting language goal. Run extensions outside the core
with no ambient authority, pinned source/artifacts and dependencies, declared
capabilities, quotas, egress protection, separate install/enable/grant/effect
states, vulnerable-package handling, rollback, and Safe hIRC.

### 20. Bridge architecture and protocol

Replace the present general bridge prose with the four-component boundary:
network gateway, deterministic contract broker, isolated minimized
bridgekeeper, and local release/ingress gate. Specify peer verification, exact
contract and canonical envelope, identity/key lifecycle, current transport and
message-security profiles, replay/sequence/expiry, downgrade rejection,
revocation lag, taint, quotas, metadata privacy, compromise, exit, and recovery.

### 21. Time, causality, and replay

Retain source/observation/commit/effective times, local sequence, bitemporal
views, and causal links. Add trusted-time limitations, contract-relative
sequence and nonce, stale execution/credential rejection, and explicit 0-RTT
prohibition for state-changing or replay-sensitive operations.

### 22. Consequential journal, archives, privacy disposition, and restore

Retain originals, artifacts, rebuildable projections, archives, and tested
restoration. Add database-role enforcement, external audit anchors, separate
data/backup keys, controlled deletion/anonymization tombstones, no cross-domain
deduplication leaks, and clean-room reconstruction after controller/cloud/key
loss.

### 23. Build, release, update, and supply-chain trust

Add isolated builds, locked inputs, SBOM, authenticated provenance, immutable
artifacts, independent promotion, offline/threshold release authority, pinned
TUF profile, assessed SLSA target, signed security floors, dependency
revocation, and rollback/forward recovery. Online controllers may schedule only
already approved digests.

### 24. Safe recursive improvement

Retain proposal, simulation, canary, evaluation, activation, observation, and
rollback. Add `FoundationChange`, whole-source semantic delta, consequence map,
predecessor-controlled evaluator tests, separate authority for activation,
mixed-version visibility, and residual obligations that survive rollback.

### 25. Scenarios and scale stress

Retain practical scenarios and long-horizon workload classes. Add compromised
foundation compiler, stolen release/recovery key, malicious attention governor,
bridge parser differential, provider privacy change, and clean-room recovery.
Numbers remain test classes, not supported-capacity claims.

### 26. Architecture decisions to freeze

Retain ADR-001–020 with corrected foundations. Add ADRs for foundation
versioning/compilation, desktop shell, authorization model, human/workload
identity, secret topology, audit anchoring, provider privacy, bridge protocol,
cryptographic profile, build/release trust, and recovery custody.

### 27. Acceptance and adversarial verification

Retain the 58 future tests and correct affected cases. Add tests for identity
cloning; key theft/rotation/loss; contract downgrade/fork/replay;
canonicalization/parser differential; malicious updates; renderer/IPC/XSS/CSRF;
SSRF/redirect/DNS rebinding; database-owner rewrite; privacy side channels;
attention coercion/suppression; backup/key/custodian loss; and bridge/foundation
clean-room recovery. Each test binds exact source, environment, seed, expected
and actual result, runner, and claim affected.

### 28. Delivery sequence and go/no-go gates

- **P0:** source/intent freeze, foundation 1.0 binding and coverage, threat
  model, ADRs, prototype evidence correction.
- **P1:** secure local core, human/workload identity, secrets, grants, privacy,
  event/audit/outbox, Safe hIRC, archive/restore and clean-room recovery.
- **P2:** one provider/tool vertical slice with non-effectful then bounded
  effectful work, canonical reconstruction, evidence acceptance/correction, and
  attention desk.
- **P3:** permanent-agent registry, formation/admission, teams, scheduler,
  reservations, bounded organization plans, and indirect-subagent denial.
- **P4:** foundation/prompt/role rollouts, secure migration, provider expansion,
  and compatibility.
- **P5:** constrained hScript/plugins and advanced UI customization.
- **P6:** bridge specification → offline conformance → two-system lab → hostile
  lab → independent assessment → bounded pilot → separately authorized broader
  activation.
- **P7:** larger-scale and adaptive organization only after measured benefit.

### 29. Open decisions and explicit nonclaims

Carry the consequential owner decisions: richer remote free text; one or
multiple local human principals in the first deployable profile; and the first
formal assurance/compliance target. Also identify genuinely independent
custodians before claiming release/recovery/bridge quorum. Preserve nonclaims about perfect security,
consciousness, identical model migration, complete coverage, zero operator
error, limitless scale, and guaranteed control of arbitrary future systems.

### 30. Sources, glossary, and final acceptance

Keep public standards near the claims they support. Put protected current-source
bindings and derivation in a separate owner-internal traceability companion.
Ordinary product and client-facing language describes behavior without requiring
internal framework terms. Final acceptance retains the 1.0 operational-memory
objective and adds tested foundation, security, and recovery invariants.

## Proposed companion artifacts

- `hirc_master_plan_v1_1.md` — cohesive human master;
- `hirc_requirements_v1_1.json` — canonical machine register;
- `hirc_requirements_v1_1.md` — generated readable register;
- `hirc_threat_model_v1_0.md` — assets, adversaries, trust, controls, residuals;
- `hirc_bridge_security_profile_v0_1.md` — disabled candidate protocol profile;
- `hirc_foundation_architecture_v0_1.md` — owner-internal source/semantic/compile
  and live-evolution contract;
- `hirc_master_plan_explained_v1_1.md` — plain-language explanation; and
- `audit/` — source identities, validators, test manifests, peer consensus, and
  ledger closure.

The master owns product direction and relationships. Companion files own the
details that need independent versioning and executable validation; they do not
become competing architectural authorities.
