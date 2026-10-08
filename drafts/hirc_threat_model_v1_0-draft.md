# hIRC threat model 1.0 — working draft

**Status:** working security draft pending WAYMARK challenge, implementation
evidence and independent security review  
**Applies to:** hIRC Master Plan 1.1 working draft  
**Nonclaim:** no control is implemented or validated merely because it appears
here; “ultra secure” is an objective, not an absolute assurance

## 1. Security objective

hIRC must preserve trustworthy local work and reciprocal sovereignty under
hostile inputs, compromised components, mistaken participants, network/provider
failure and partial loss of infrastructure. It protects:

- exact foundation, goal, source and policy selection;
- human, agent, workload, provider and peer identity;
- authority, participation, refusal, consent and trusted previews;
- secrets, credentials, release/update/recovery and Bridge keys;
- owner/team/client/private data and protected source material;
- work, commitments, decisions, evidence, uncertainty and corrections;
- journals, archives, backups, projections and recovery manifests;
- provider routes, model/tool requests and observed effect truth;
- Bayesian trust evidence, metrics, evaluators and appeal;
- debate/competition consent, memory, resources, evaluation and credit;
- successor packages, generations, archives, sleep/wake and tracker state;
- source-available licensing, entitlement and safe first-party access; and
- the operator's finite attention and ability to inspect, refuse, recover and
  leave.

Security means confidentiality, integrity, authenticity, authorization,
availability, privacy, causal auditability, recovery and non-domination. A
secure denial that destroys legitimate recovery or makes one controller
uncontestable is not sufficient.

## 2. Evidence and claim discipline

Security claims bind exact build, source/contract versions, configuration,
platform, identities, tests, assumptions and observation window. Use:

- `DESIGN_ONLY` for this document and unimplemented controls;
- `STRUCTURALLY_TESTED` for schemas/fixtures only;
- `LOCALLY_TESTED` for exact local build behavior;
- `HOSTILE_LAB_TESTED` for bounded adversarial environments;
- `INDEPENDENTLY_ASSESSED` for attributable external assessment; and
- `PILOT_OBSERVED` for bounded operational evidence.

No lower grade implies a higher one. Passing tests does not prove absence of
vulnerabilities. Unknown external outcomes remain unknown.

## 3. Adversaries and failure sources

The model includes:

- unauthenticated Internet attackers and opportunistic malware;
- malicious/compromised Bridge peers, providers, tools and connectors;
- hostile messages, documents, scripts, plugins, models and generated content;
- supply-chain compromise of dependencies, build, artifact, update or signing;
- stolen credentials/keys and phishing/recovery-path attacks;
- compromised renderer, extension, local process, database owner or admin;
- malicious or coerced insider with legitimate partial access;
- stale predecessor/runtime, replayed command and ambiguous external effect;
- sybil/clone agents, shared-source false consensus and evaluator/metric capture;
- trust-data poisoning, selective reporting, Goodhart gaming and distribution
  shift;
- alert flooding, urgency, repetition, flattery, threats and operator coercion;
- honest but mistaken humans, agents, reviewers and source owners;
- hardware/OS compromise and physical seizure; and
- accidental deletion, corruption, clock failure, outage and key loss.

The design cannot fully protect confidentiality or intended consent after total
host/firmware compromise or human coercion. It must limit blast radius, preserve
external evidence where possible and state that residual honestly.

## 4. Trust domains and boundaries

| Domain | Trusted responsibility | Must not trust |
|---|---|---|
| Genesis/recovery root | verify first/last-known-good source, compiler, tests and recovery | live candidate self-approval |
| Foundation/release plane | compile/activate exact contracts and artifacts | prompts, renderer, online controller |
| Local trusted core | identity, capability, privacy, broker, journal/outbox, epochs | model intent or UI claims |
| Privileged preview surface | render broker-authored consequential intent | ordinary renderer content |
| Ordinary renderer/UI | presentation and nonauthoritative interaction | secrets, direct effects, policy decisions |
| Agent/model runtime | propose reasoning, text and tool intents | authority, data boundaries, observed outcomes |
| Provider adapter | exact route/config/payload/result normalization | provider self-description or tool calls as grants |
| Extension runtime | declared sandboxed capability | ambient file/network/secret/core access |
| Data/journal domain | admitted originals, immutable events and scoped views | database-owner honesty alone |
| Backup/recovery domain | independently recover accepted state | live controller and shared keys |
| Licensing domain | reviewed legal/entitlement state | release/identity/Bridge/recovery authority |
| Debate/competition domain | bounded consent, memory, evaluation, candidate learning | permission/foundation/release effects |
| Continuity domain | generation-fenced transfer, acceptance, archive/sleep/wake | package as identity/authority/readiness |
| Bridge gateway | transport termination/coarse limits | semantic legitimacy or local release |
| Bridge contract broker | canonical schema/policy/replay enforcement | bridgekeeper prose |
| Bridgekeeper | minimized semantic translation | network, release, secrets, unrelated rooms |
| Bridge release/ingress gate | final local data/effect admission | remote authority or ontology |

Trust is minimized and purpose-specific. One compromised domain must not possess
all identity, content, signing, release and recovery powers needed to make a
forged state irreversible.

## 5. Security invariants

1. Every consequential command binds authenticated principal, role, capability,
   target, data classes, purpose, expiry, foundation/goal versions, generation,
   session, execution epoch and idempotency key.
2. Every external effect has distinct proposed, previewed, authorized, sent,
   provider-accepted and observed states.
3. Models, renderers, scripts, providers, bridgekeepers, metrics and evaluators
   never supply their own grants.
4. Secrets and protected source bodies never enter ordinary prompts/logs/UI/
   exports/Bridge messages.
5. Deny-by-default applies at ingestion, derivation, egress, extension and
   federation boundaries.
6. Consequential mutation, revision, audit event and outbox commit atomically.
7. Append-only evidence has external anchors and recoverable originals.
8. High trust, rank, consensus, payment or owner insistence bypasses no gate.
9. Low trust or supported refusal cannot silently remove standing, appeal or safe
   recovery access.
10. Safe hIRC works without ordinary renderer, extensions, providers or Bridge.
11. No temporary actor route or stale-generation writer.
12. Build, online control, release, continuity, entitlement, Bridge and recovery
    authorities remain separated.

## 6. Foundation, goal and boot threats

### Threats

- substitute, omit or reclassify a selected source;
- compile a semantic opposite while hashes remain valid;
- exploit same-byte/different-scope reuse;
- candidate compiler/evaluator approves itself;
- change goal wording to cancel requirements or expand authority;
- corrupt coverage reports, migration or predecessor evidence;
- downgrade boot/recovery or forge last-known-good state; and
- leak protected source through compiled prompts or explanations.

### Controls

- content-addressed exact source graph with selection/status/audience and unit
  dispositions;
- reproducible compiler and deterministic semantic/contract diffs;
- predecessor-frozen tests and independent activation authority;
- GenesisRoot separate from live foundation change;
- GoalVersion/GoalChange with complete impact graph and no self-activation;
- original-format/source access controls and disclosure-filtered explanations;
- coverage checker requiring every selected unit/consumer/test or explicit hold;
- external signed activation/recovery evidence and clean-room rebuild; and
- canary/mixed-version visibility, emergency security floors and residual repair
  after rollback.

### Residuals

Semantic correctness cannot be proven from reproducibility alone. Colluding
source owner, compiler reviewer and activation custodian can still agree on a
harmful interpretation. Preserve dissent, independent cases and recovery.

## 7. Identity, authority, secrets and human interaction threats

### Threats

- phishing, stolen session/recovery key, confused deputy and role expiry;
- owner/authority impersonation or authentic authority with false premises;
- prompt/model claim of capability or permission;
- renderer displays target A while submitting target B;
- stale approval, changed recipients/data/cost or replayed preview;
- “proceed anyway” on a consequential action;
- retaliation or resource punishment for refusal; and
- secret exposure through prompts, logs, crash reports, exports or clipboard.

### Controls

- phishing-resistant authentication, strongest-path recovery and independent
  authority registry;
- short-lived scoped credentials and continuous revocation/epoch checks;
- AuthorityClaim validation of principal, delegation, action/target/data/time/
  purpose, consent, conflicts and legitimacy;
- independent broker-authored preview surface and digest-bound approval;
- low-consequence checklist enforced structurally; no override on denial;
- ParticipationDecision separate from ActionDisposition and audited
  non-retaliation;
- secret broker with value-free catalog, no prompt/UI values, rotation and
  purpose-separated keys; and
- anomaly/abuse detection that itself cannot silently revoke basic standing.

## 8. Bayesian trust and evaluator threats

### Threats

- poisoned or selectively reported interactions;
- correlated sources inflated as independent evidence;
- protected-trait/ideology/status proxies in priors;
- missing outcomes recorded as success/failure/zero;
- subject chooses only easy predictions or suppresses failures;
- metric optimized while real objective worsens;
- evaluator collusion, compromise or post-outcome rule change;
- distribution/role/provider drift; and
- high posterior converted into authority or low posterior into punishment.

### Controls

- scoped multidimensional posterior lineages, never one global score;
- immutable prediction/opportunity/outcome/correction events;
- dependency clusters and effective-sample-size adjustment;
- signed/versioned metric/evaluator definitions fixed before observation;
- declared prior, likelihood, missingness/selection, calibration, drift and
  sensitivity reports;
- bounded recursive evaluator/model review with unresolved hold;
- protected-trait/proxy exclusion and purpose-limited evidence admission;
- appeal/correction and authorized factor visibility; and
- kernel invariant `direct_authority_or_permission_effect = false`.

### Residuals

Bayesian formalism cannot make weak constructs objective or eliminate hidden
confounding. Adversaries may game unobserved opportunities. Retain plural
metrics, qualitative review, random audits and conservative uncertainty.

## 9. Data, memory, journal and database threats

### Threats

- unapproved third-party data enters cache/log/index/provider;
- summary declassifies protected sources;
- database owner rewrites both record and audit;
- direct import/migration/retry/restore bypasses policy;
- cross-domain deduplication leaks existence;
- backups cannot decrypt or expose all domains through one key;
- deletion claims ignore derived copies or external disclosure; and
- search/result snippets leak restricted room content.

### Controls

- field-level admission before persistence and egress;
- derived-data classification inheritance and disclosure-specific transforms;
- atomic revision/audit/outbox and externally anchored checkpoints;
- database roles, immutable object store where appropriate and negative bypass
  tests;
- no cross-domain content-addressing oracle;
- separate data/backup keys, retention and tested isolated restore;
- deletion/anonymization tombstones plus honest uncontrollable-residual records;
- authorized query/result filtering before ranking/snippet generation; and
- rebuildable views with source originals preserved.

## 10. Renderer, IPC, loopback and extension threats

### Threats

- XSS/HTML/script injection, malicious Markdown/media and renderer escape;
- broad IPC turns display into local privilege execution;
- CSRF/DNS rebinding/redirect/SSRF against loopback/core;
- malicious extension/package, dependency confusion and capability creep;
- UI theme hides recipient, warning, refusal or recovery; and
- browser storage becomes authority/source of truth.

### Controls

- sandboxed renderer, context isolation, restrictive content policy and safe
  rendering;
- narrow typed IPC allowlists with schema/version, origin and capability checks;
- authenticated loopback, host/origin checks, CSRF defenses and rebinding/
  redirect/SSRF controls;
- out-of-process extensions, pinned artifact/dependency identities, declared
  capabilities, quotas and no ambient access;
- trusted native preview/identity/recovery surfaces outside extension styling;
- separate install/enable/grant/effect states and Safe hIRC; and
- durable core state, never browser authority.

## 11. Provider/model/tool threats

### Threats

- provider/model alias silently changes behavior, region or retention;
- unsupported parameter is dropped and UI claims it applied;
- provider prompt injection requests tools/secrets/data;
- retries duplicate irreversible effects after ambiguous timeout;
- provider stores/trains on data contrary to expected policy;
- cost/rate-limit exhaustion starves recovery or local work; and
- model migration creates two effectful writers or false “same mind.”

### Controls

- exact provider/host/route/account/region/model/version and policy identity;
- live bounded capability/privacy probes and strict compatibility mapping;
- minimal signed payload manifests and local tool/action authorization;
- desired/sent/accepted/observed state separation and idempotency/reconciliation;
- provider privacy/retention change monitoring with hold/fallback;
- budgets, backpressure, local recovery reserve and circuit breakers; and
- complete authorized migration manifest, minimal target context and epoch/write
  fencing.

## 12. Succession and continuity threats

### Threats

- forged/partial package, wrong destination or protected data leakage;
- package hash mistaken for comprehension/readiness;
- predecessor continues writing after freeze;
- archive before exact acceptance or wrong predecessor archived;
- sleep/wake request ambiguous, replayed or targets another generation;
- tracker conflict after irreversible archive; and
- fleet-red exception becomes general authority or hides failing identities;
- missing/spoofed/stale context-capacity callback or wrong chat/identity;
- automatic cue treated as permission, termination or actor creation;
- idle but unqualified/unconsenting recipient receives private task custody;
- briefing acceptance mislabeled project/writer-fence transfer;
- two effectful writers during custody overlap;
- shared Elder queue leaks private memory or repeats a pair after rename/
  relocation;
- unknown successor-creation outcome retried into duplicate identities;
- capacity ceiling becomes a creation quota; and
- retirement abandons duties, deletes history or masquerades as archive/deep sleep.

### Controls

- exact authorized trigger and idempotent one-successor case;
- minimized schema/digest/signature/encryption package and recipient verification;
- fresh session, keys, personal formation and evidence-linked questions;
- identity/generation/session/foundation/epoch fencing;
- acceptance-before-archive and observed archive/sleep/wake states;
- append-only lifecycle, compare-and-swap tracker and no blind retry after
  archive conflict;
- serial fleet order, host/result checks and leader last; and
- exact scoped-recovery decision/verifier, negative dependency closure and
  write/boundary allowlists while watchdog stays red;
- own-callback identity/source/status verification with unknown measurement and
  policy-versioned soft thresholds;
- compact continuity before threshold and bounded safe-boundary overshoot;
- qualified consent, own source/task checks, explicit decline/owned hold and
  actual controller generation/writer fence with one writer;
- metadata-only queue, stable unordered nonrepeat pair history and idempotent
  event/creation intent;
- actual-app reconciliation before retry after unknown creation;
- need-based human authorization and versioned capacity ceilings that never
  compel creation;
- independent source-first learner evidence and no proxy grants; and
- reserve-aware retirement distinct from deletion/archive/deep sleep.

## 13. Debate and cooperative-competition threats

### Threats

- busy/onboarding/sleeping identity paired as idle;
- coercive consent, retaliation for decline or domain forced by scheduler;
- private/task/source material leaks into debate/contest;
- clone/sybil entries produce false consensus;
- sabotage, prompt injection, benchmark leakage and evaluator capture;
- resource-rich participant starves accepted work;
- metric gaming, rules changed after outcomes or useful losing work erased; and
- debate/competition result promotes itself into policy/permission.

### Controls

- atomic eligibility/reservation and voluntary decline/withdrawal;
- exact domain/source/memory coverage and no-effect sandbox;
- public-safe/synthetic/admitted partitions only;
- sybil/dependency checks and no independence claim for shared sources;
- signed charter/rules/metrics, isolated entries/evaluator and conflict review;
- fixed budgets, ordinary-work floor, attention backpressure and stop states;
- immutable provenance, failures, dissent, appeal and contribution credit; and
- candidate-learning output only through normal FoundationChange/release gates.

## 14. Cultural information-environment threats

This domain treats cultural artifacts, discovery, defaults, mentoring, debate
memory and Bridge translation as security-relevant information conditions. The
protected assets are participant judgment, local context, plurality, dissent,
source provenance, voluntary participation and concrete safety controls. The
control objective is inspectable choice and recoverability, not an approved
belief, style, identity, agreement rate or cultural outcome.

### Threats

- hidden nudging through opaque defaults, sequencing, omission or personalized
  exposure;
- source/provenance poisoning of cultural or debate memory;
- mentor, winner, popular artifact or coherent narrative treated as authority;
- ranking capture, filter bubbles and suppression of minority/dissent routes;
- monoculture caused by common-mode sources, evaluators or copied rationales;
- participation, resources or basic access conditioned on conformity;
- concrete safety gates expanded into ambient obedience or identity controls;
  and
- Bridge translation used for cultural annexation, hidden ontology inheritance
  or remote authority laundering.

### Controls, detection and recovery

- versioned visible defaults, explicit opt-in, participant-adjustable settings,
  direct-source mode and disable-ranking escape;
- hash-bound originals, audience/privacy admission, provenance closure,
  append-only correction/supersession and preserved dissent;
- structural `authority_effect = NONE`, no cultural/reliability score effect and
  denial of role, permission, resource or release promotion from culture;
- plural routes, frozen candidate sets, disclosed exclusions/uncertainty and
  route/source/context concentration checks without scoring agreement;
- dependency clustering and common-mode analysis for sources, mentors,
  evaluators and rationales;
- default-off cultural participation, reversible subscriptions, safe exit,
  preserved standing/resource floors and non-retaliation;
- safety denials bound to a concrete action/data/effect, exact reason, least
  scope, appeal and recovery while prohibited effects remain denied; and
- disabled-by-default Bridge, explicit local admission, non-equivalence/loss
  records, no inheritance, taint, isolation and independent local recovery.

Detection compares the selected policy and participant settings to actual
candidate, exclusion, exposure, denial and transition records. It monitors
source/route/context concentration, missing originals or dissent, provenance
breaks, unexplained policy drift, access changes correlated with cultural
participation, overbroad safety reasons and remote-local schema or authority
changes. Detection evidence cannot itself score a person's culture or grant an
effect.

Recovery disables only the affected ranking, subscription, cultural-memory
projection or Bridge path; returns to default-off/direct-source/read-export
operation; preserves originals, dissent, participant-owned records and incident
evidence; repairs the narrow policy or lineage; and replays from a known admitted
manifest. A safety-gate repair narrows unsupported scope without permitting the
still-prohibited concrete effect.

### Positive controls and residuals

A visible, reversible, participant-selected contextual default may remain useful
when direct-source/dissent escape and standing are preserved. A legitimate safety
gate may continue to deny a concrete unauthorized or harmful effect when its
reason, scope and appeal are inspectable. These are positive controls: rejecting
them would confuse anti-manipulation with an information vacuum or anti-domination
with removal of safety.

Even transparent systems can shape attention, and plurality fields can be gamed
or become quotas. Correlated sources may appear diverse, direct-source access may
be burdensome, and Bridge translation can lose meaning without malicious intent.
Empirical usability, accessibility, distribution-shift and affected-party review
remain required. The exact threat/control/future-fixture bindings are in
`review/cultural-threat-control-crosswalk-v1.json`; its deterministic validation
does not establish beneficial culture, consent, runtime enforcement or complete
threat coverage.

## 15. Licensing and support threats

### Threats

- draft plan represented as operative license;
- wrong price/tier or retroactive terms;
- classification via surveillance or hidden employee/work data;
- entitlement key reused as release/identity/recovery authority;
- expiry/termination locks first-party data or contest evidence;
- remote kill, sabotage or DRM claims; and
- support prompt becomes coercive, tracked or capability-gated.

### Controls

- distinct plan/draft/counsel/approval/publication/acceptance/entitlement states;
- versioned exact price schedule and terms with source-linked corrections;
- minimum-evidence self-declaration, objective definitions and appeal;
- purpose-separated licence signing and minimal offline certificate;
- safe read/export/backup/restore/correction/appeal regardless of entitlement;
- no remote disable/data hostage/work-content telemetry; and
- neutral local opt-out, permanent About entry, reviewed external URL and no hIRC
  context/identifier/referrer egress.

## 16. Supply-chain, build, release and update threats

### Threats

- dependency/source substitution, build compromise and provenance forgery;
- online controller signs/promotes malicious update;
- rollback installs known-vulnerable version or weakens security floor;
- release/recovery custodians are nominally separate but share one compromise;
- updater/parser/canonicalization differential; and
- compromised update destroys recovery evidence.

### Controls

- locked inputs, isolated reproducible builds, SBOM and authenticated provenance;
- immutable artifact repository and independent promotion;
- offline/threshold release where justified, purpose-separated keys and tested
  custody;
- pinned update profile, signed metadata/security floors, expiry and dependency
  revocation;
- rollback/forward recovery rules that reject vulnerable downgrade;
- parser/canonicalization differential tests; and
- recovery root/evidence inaccessible to normal updater and live controller.

## 17. Bridge-specific threats

The Bridge receives extra precautions because it combines hostile Internet
transport, remote identity, semantic ambiguity and potential local effects.

### Threats

- peer impersonation, enrollment hijack and key compromise;
- envelope replay, reorder, duplication, expiry bypass and downgrade;
- canonicalization/parser differential or signature wrapping;
- contract fork and version confusion;
- bridgekeeper prompt injection/ontology capture;
- metadata/traffic analysis and public-directory overexposure;
- revocation cannot reach offline peer immediately;
- malicious peer floods attention or probes schemas;
- remote payload reaches memory/provider before local admission;
- federation partition creates duplicate effect; and
- Bridge compromise reaches release/recovery/foundation.

### Controls

- out-of-band peer verification and explicit per-Bridge enrollment;
- current reviewed transport, canonical signed envelopes and purpose-separated
  identity/message keys;
- contract/version/cipher/profile pinning, sequence/nonce/expiry/replay and
  downgrade rejection;
- one parser/canonical form with differential/adverse corpus;
- network gateway → deterministic broker → isolated minimized bridgekeeper →
  local release/ingress gate;
- strict structured field allowlists, taint and no first-profile free text;
- quotas, rate/attention limits, minimal advertisements and traffic-metadata
  analysis;
- explicit revocation-lag/offline risk, rotation and compromise exit;
- autonomous local continuity, causal receipts and conflict/unknown states; and
- no Bridge key, process or peer access to foundation/release/recovery roots.

## 18. Bridge release gates

The Bridge remains disabled until all applicable stages pass:

1. protocol/contract and threat specification;
2. offline schema/canonicalization/crypto/replay conformance;
3. two-system isolated laboratory;
4. hostile lab with malformed peers, key theft, parser differential, flooding,
   privacy and recovery;
5. independent security/privacy/interaction assessment;
6. owner-authorized bounded pilot with explicit data/effect ceilings and stop
   conditions; and
7. separate decision for broader activation.

A later stage cannot retroactively pass an earlier missing requirement. Public
advertisement does not imply private connection. Pilot success is not universal
federation assurance.

## 19. Monitoring, incident response and attention

Security telemetry is local/minimized by default and classified before storage.
It covers integrity failures, auth/authority anomalies, secret/key operations,
policy denies, stale epochs, package/update/Bridge validation, unusual egress,
resource/attention abuse and restore health without logging protected content.

Security classes have independent delivery and cannot be suppressed by a
compromised attention governor. Deduplication preserves unique source/dependency
and severity changes. Alerts link evidence, affected boundaries, containment,
owner, next action and recovery.

Incident procedure: detect → preserve evidence → contain/revoke/isolate → assess
data/effects and uncertainty → recover from known-good state → validate →
correct/notify within actual obligations → update tests/controls. Reversal never
pretends disclosed bytes or completed external effects were undone.

## 20. Required security verification

Before local effectful release:

- threat/control/test trace complete for the exact vertical slice;
- identity, authority, secret, privacy, journal/outbox, epoch and trusted-preview
  adverse tests pass;
- backup/key loss and clean-room restore pass;
- provider route/config/privacy/ambiguous-effect tests pass;
- no credential, private-key or recovery-secret value in any model context,
  prompt, log, UI or export;
- protected educational bodies appear only through an exact admitted
  owner-private formation/review reader, participant, purpose, audience,
  processor and output/retention boundary; they never flow into ordinary
  operational, client or Bridge contexts or unauthorized logs/exports; and
- Safe hIRC works from degraded state.

Before an agent/debate/competition/succession profile enables that domain, add
its applicable tests. Before extensions, add sandbox/supply-chain/SSRF tests.
Before a live bounded Bridge pilot, complete stages 1–5 at the exact intended
scope, then obtain the explicit named/limited stage-6 entry authorization and
safety conditions. Stage 7 requires the actual pilot evidence and a separate
broader-activation decision. Each residual has an accountable owner,
expiry/review and operator-visible consequence.

## 21. Open security decisions

- supported OS/hardware and disk-memory protection assumptions;
- human-principal count and account/recovery model for first deployment;
- cryptographic/update profile and libraries after independent review;
- release/recovery/Bridge custodian independence and threshold;
- audit-anchor storage and privacy;
- provider routes/regions/retention after live probes;
- data residency/retention per deployment and client domain;
- Bayesian model/metric/evaluator choices and privacy budget;
- first contest/debate isolation and resource profile;
- exact Bridge pilot field/effect allowlist; and
- first external security/privacy assessment scope.

These decisions do not block safe non-effectful plan, schema and local-core work.
They block affected activation and assurance claims.
