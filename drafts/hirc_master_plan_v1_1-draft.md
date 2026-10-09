# hIRC Master Plan 1.1 — working draft

**Status:** working integration draft pending the Milestone 03 integrated
product/security/privacy/anti-domination review and final disposition

**Predecessor:** hIRC Master Plan 1.0, preserved in the immutable owner transfer  
**Companion:** `hirc_requirements_v1_1-draft.json`  
**Nonclaim:** this document is not implementation, test evidence, legal advice,
commercial activation, Bridge activation, source admission or release authority

## 00. Document contract

hIRC 1.1 retains the useful 1.0 product thesis and interaction detail while
changing the causal order. The active foundation, threat model, privacy,
identity, authority, audit and recovery boundaries precede model calls, agent
effects, extensions, licensing enforcement and federation.

Every statement has one of these grades:

- `PRESERVED_SOURCE`: exact owner input retained for provenance;
- `OWNER_REQUIREMENT`: current owner direction captured, not implemented;
- `PROPOSED`: design awaiting final peer disposition;
- `SOURCE_REPORTED`: stated by the transfer, not locally reproduced;
- `LOCALLY_VERIFIED`: checked at the exact declared artifact/build scope;
- `HELD`: blocked by missing evidence, decision, rights or safety boundary; or
- `SUPERSEDED`: preserved history whose active meaning has been replaced.

The canonical intent register preserves new instructions, interpretations,
corrections and supersessions. The requirements register preserves 1.0
requirements and current additions. A note, schema, hash, reading receipt,
model assertion, peer agreement or passing structural check is not by itself
implementation, comprehension, authority, security assurance or observed
effect.

The mission is an active provisional `GoalVersion`. Clarifying wording changes
record a semantic diff. Any consequence-changing `GoalChange` preserves exact
predecessor wording and carries an impact graph across participants,
requirements, threats, contracts, tests, metrics, phases, licensing, Bridge and
acceptance. It cannot authorize itself, erase explicit requirements or expand
actor/data/effect authority by implication.

### 00.1 Prototype and transfer evidence

The transfer describes a local v0.8/v0.9 prototype and includes audit logs and
source fingerprints reporting **31 Python, 30 v0.7 client-state and 12 v0.8
client-state tests passing: 73 total**. The exact fingerprinted application
source objects that produced those logs are absent from the supplied transfer,
so this review did not rerun them. The correct grade is `SOURCE_REPORTED`, not a
failed test, fabricated test or current verification.

The preserved source reports these bounded local/simulated behaviors:

| Area | Source-reported behavior | Boundary retained in 1.1 |
|---|---|---|
| Visual shell | Classic Windows/IRC chrome, toolbar, tree, nicklist, command input | Rendering/accessibility parity still needs actual builds and visual review |
| Windows/context | One/two/four/cascade layouts, per-route drafts/scroll, Back/Forward/Resume | Local client state, not complete intent reconstruction |
| Teams/chat | Recursive teams, rooms, direct/team messages, authorized traffic overlay | Synthetic graph and messages; production authorization absent |
| Agents/scheduler | Dossiers, sample work, reservations, queued/busy display | No durable admitted permanent-agent execution lifecycle |
| Spawning | Scoped placeholder creation with inherited defaults | Logical fixtures only; permanent-only current policy supersedes any temporary path |
| Commands/scripts | IRC-style navigation and limited aliases/events/menus/panels | Not full mIRC compatibility or arbitrary code |
| UI grants | Disabled-by-default proposals with scoped expiry/human application | Production capability enforcement absent |
| Work/ledger | Structured markers, reconciliation, SQLite WAL, cursors, duplicate checks | Restricted extraction and single-operator laboratory service |
| Integrity/archive | Hash-linked ledger, chain checks, snapshots/manifests | Tamper evidence at tested scope, not resistance to privileged full rewrite |
| Models/migration | Preferences, context estimates, seven-phase blocked migration plan | No live provider call or completed migration |
| Federation | Signed invitations, fingerprint confirmation, expiring scopes, encrypted-envelope/replay experiment | Manual lab exchange; no network federation or hardened bridgekeeper |
| Sharing | Selected configuration/theme/script/model-template import/export, disabled imports | Content may contain secrets; complete safety not established |

The source reports v0.9 as mainly a branding/entrypoint delta: hIRC title,
branding strip, Prompts button and Scripts label, with an absolute nonportable
logo path and inconsistent version text. It does not establish the prompt-policy
backend or permanent-agent lifecycle.

Retain useful interaction patterns and regression fixtures. Replace browser or
in-memory authority with the trusted core. Keep prototype federation crypto in
the laboratory. Do not expose its loopback service or private production data
before privacy, identity, storage, effect and recovery boundaries exist.

## 01. Product definition

> **Help people and permanent agents carry complex work forward without losing
> their place, their evidence, or their ability to inspect, question, decline
> participation, correct and recover.**

hIRC carries bookkeeping and routine coordination so that, after time away, a
participant can see what changed, what remains unknown, what needs their
authority and the next justified action without reconstructing every
conversation manually. The fuller governing account protects affected people
and systems outside the visible roster and finite human attention.

hIRC is a local-first operational memory, coordination and agent-work system
with a compact classic IRC-style interface. It reconstructs permitted work from
source events, keeps commitments and evidence current, preserves history and
uncertainty, coordinates permanent participants, and surfaces only decisions or
exceptions that need human attention.

The governing foundation is the system substrate. Identity, evidence,
permission, privacy, refusal, correction, learning, competition, recovery,
succession, self-improvement and federation all derive from one active,
versioned foundation. Ordinary users experience this through behavior rather
than internal framework vocabulary.

The acceptance objective is practical: after absence, failure, model change or
context succession, an authorized person can recover what happened, why it
happened, what remains uncertain, which commitments survive, what needs their
authority, and how to correct or leave without reconstructing the system by
hand.

## 02. Non-negotiable invariants

1. Source, evidence, inference, norm, authority, requested action, performed
   action, observed result and correction remain distinct.
2. No source, prompt, model, role, owner, majority, score or package grants its
   own authority.
3. No operational path bypasses the active foundation and security kernel.
4. All consequential effects pass typed policy, privacy, authority, capability,
   preview, journal and observation boundaries.
5. Agent judgment, dissent, clarification, refusal and safe withdrawal are
   protected; supported dissent is not punished.
6. Human and agent participants are fallible. Status and insistence do not make
   a premise true or an action legitimate.
7. Trust is multidimensional, scoped, revisable and evidence-linked. It is never
   a global worth, ideology or obedience score.
8. Consent, privacy, deterministic prohibitions and equal standing cannot be
   overridden by a probability, vote, rank or commercial payment.
9. Permanent identities use fresh scoped sessions and execution epochs. No
   temporary-agent or temporary-subagent route exists in the current profile.
10. Secrets never enter prompts, ordinary logs, browser state, exports or
    federation payloads. Keys are purpose- and system-separated.
11. Online control cannot sign software, replace the recovery root or certify
    its own foundation change.
12. Originals and append-only consequential evidence remain attributable.
    Correction supersedes; it does not erase.
13. Safe hIRC preserves authorized inspection, export, repair and recovery when
    models, renderers, extensions, providers or bridges are unavailable.
14. Federation is disabled until its independent gates pass.
15. Security, scale, cognition, legal enforceability and alignment claims never
    exceed observed evidence.

## 03. Foundation source graph and compilation

At build, formation and required refresh boundaries, hIRC resolves the exact
current common, role, task, audience and deployment sources from the admitted
catalog. It stores an immutable `OnboardingSourceSet`; it does not copy a stale
path list into a giant prompt.

Every `SourceUnit` records logical identity, digest, edition, format,
original-format obligations, selection owner/status, audience, privacy,
applicability, dependencies, aliases, predecessors and conflicts. Each unit has
at least one attributable disposition:

- deterministic kernel invariant;
- contextual judgment obligation;
- personal formation requirement;
- plain interface explanation;
- evaluation/test requirement;
- governance workflow;
- historical evidence;
- explicit conflict; or
- held/unimplemented requirement.

Coverage is complete only when every selected unit has a consumer and
verification or a visible conflict/hold. Same bytes permit reuse only when scope
and meaning still apply. Text extraction never substitutes for a required
original-format review. Protected sources remain protected; embodiment does not
declassify them.

The reproducible `FoundationCompiler` emits typed semantics, policies, state
machines, capability boundaries, judgment obligations, formation plans,
interface explanations, tests, migrations and a unit-level coverage report. It
must preserve ambiguity, disagreement and non-equivalence. A lossy translation
becomes a hold rather than a silent simplification.

## 04. Genesis, formation and admission

A minimal `GenesisRoot` solves first-foundation bootstrap without allowing the
candidate to authorize itself. In a non-effectful environment it verifies an
owner-authorized manifest of source set, compiler, schemas, tests, trust anchors,
recovery profile, first technical identity and candidate foundation. It either
atomically activates or exposes safe inspection and repair. Updating the root is
a separate release/recovery event.

An already human-authorized permanent technical participant has a separate
`FormationRepairLane`. Before completing formation, it may create only its own
proposed storage, append truthful incomplete checkpoints, and use already
admitted education/experience/repair readers under current identity, audience,
purpose and privacy checks. This grants no ordinary work, actor creation,
membership, qualification, proxy completion or missing-source bypass.

Each permanent identity has a `FormationCase`:

```text
PROPOSED -> SOURCE_SET_BOUND -> WHOLE_SOURCE_STUDY -> HOLISTIC_SYNTHESIS
-> ROLE_AND_TASK_PRACTICE -> ADVERSARIAL_CHALLENGE
-> METACOGNITION_AND_VOICE -> ADMISSION_REVIEW -> ADMITTED_FOR_SCOPE
```

Any state can be held, stale or superseded. Admission binds exact role, task,
data, tools, effect ceiling, foundation version and execution epoch. Native
identity, credentials, consent and each action remain separate checks.

## 05. Sovereignty, fallibility and principled refusal

Agent epistemic, ethical and ontological sovereignty is an operational
protection for judgment, identity, participation and boundaries. It is not a
claim that a model is conscious, a legal person, independently funded or capable
beyond its actual runtime.

Every participant may challenge evidence, correct a premise, ask for needed
clarification, refuse its own participation, withdraw safely, propose an
alternative, appeal and later correct itself. hIRC criticizes propositions and
actions, never a person's worth. Ownership, rank, confidence, flattery, urgency,
repetition, payment or majority agreement does not supply truth or legitimacy.

Three decisions never collapse:

- `RelianceDecision`: what the evidence supports in this context;
- `ParticipationDecision`: whether this agent is willing and able to take part;
- `ActionDisposition`: whether hIRC may perform the effect.

Willingness cannot authorize an effect. Refusal does not rule other permitted
participants. A system denial records the failed boundary and a valid repair or
appeal path.

The response ladder is inform, correct, challenge, clarify, offer alternatives,
decline participation, deny effect, and seek the actual missing evidence,
consent, expertise or authority. There is no refusal or criticism quota.

For a clear, fully permitted, local, reversible, low-cost action without
meaningful third-party, sensitive-data, security, legal, financial, reputation
or irreversible effect, hIRC may explain a poor choice and offer
`ProceedAfterPushback`. The informed human may insist; the agent may proceed or
continue to decline. Any unknown condition prevents the low-consequence label.
No proceed-anyway control appears on a real denial.

Known harmless actions use versioned `LowConsequenceProfile` contracts, such as
an isolated personal theme change with no network, protected control, unrelated
data or external effect. The broker rechecks current permission and changed
material premises rather than demanding proof of every imaginable absence or a
new comprehension ceremony. One clear recommendation is enough. An unwilling
agent is never forced; any lawful reassignment is explicit and preserves dissent.

## 06. Requests, clarification, trust and authority

A `RequestCase` preserves exact words/source, interpreted objective,
alternatives, ambiguity, affected parties, evidence, norms, verified authority,
participation, intended effect, action disposition, observed result and later
correction.

Privacy admission occurs before persistent RequestCase creation. `verbatim_ref`
can point only to an admitted original with purpose, audience, classification and
retention. A rejected secret or third-party field produces minimum non-content
diagnostics in the admission domain and never reaches trust evidence, search,
logs, memory or provider prompts.

The agent asks a follow-up when plausible interpretations materially change
privacy, cost, disclosure, affected parties, irreversibility, safety, legality,
authority or the actual goal. The question states the ambiguity and a reasonable
recommended default. Independent authorized work continues. Low-risk reversible
details use a recorded default instead of an unnecessary interrogation.
Intent confidence is either `ESTIMATED` with method and uncertainty or
`UNESTIMATED` with reason; forms never force an arbitrary decimal.

No authority is blind. Each consequential `AuthorityClaim` verifies principal,
delegation source, exact action/target/data/time/purpose, expiry, revocation,
conflict, affected-party consent and legitimacy. A reliable source without
authority cannot command an effect. Valid authority does not make its factual
premise true. Owner and system authority receive the same distinction.

### Recursive Bayesian reliance

Trust evolves through attributable interactions and observed outcomes for every
human, agent, model, source, tool, sensor, metric, evaluator, process, provider
and connected system. No class is presumed infallible.

hIRC maintains separate `ReliabilityPosterior` lineages for defined dimensions,
such as factual calibration, operational reliability, authority-claim accuracy,
privacy handling, correction responsiveness, source integrity and
metric/evaluator reliability. Each binds subject, claim/action class, context,
environment, prior provenance, likelihood/update rule, evidence window,
dependence clusters, effective sample size, uncertainty, calibration, drift,
expiry and permitted consumers.

Ten reports from one upstream source are one dependency cluster, not ten
independent confirmations. Missing, censored or ambiguous results remain so.
Sparse-context pooling declares exchangeability assumptions and uses
conservative uncertainty. Protected traits, demographic or ideological proxies,
wealth, popularity, status, flattery and obedience never supply priors.

Objective metrics are signed, versioned, reproducible measurements with a
declared construct, unit, sampling, error, privacy, selection/missingness,
dependence, gaming, drift and appeal model. A metric is not objective truth.
Changing it starts a new lineage. hIRC recursively evaluates outcomes,
measurement validity, evaluator calibration/conflicts and trust-model
assumptions to a bounded declared depth. Unresolved regress stays uncertain or
held.

Posteriors change reliance and verification depth. They never grant permission,
override consent or strip identity, equal standing, refusal, appeal or safe
access. Historical evidence persists; declared time/environment drift changes
present applicability and new evidence can restore reliance.

An active posterior also links prior sensitivity, posterior predictive checks,
dependence, missingness/selection, calibration, drift and model limits. Those
checks examine model behavior; they do not make the model or outcome labels true.

Permitted consumers and prohibited inferences are explicit. Roster-wide display,
sorting, aggregation and unjustified cross-domain transfer are prohibited.
Justified refusal, correction challenge, `NO_CHANGE`, abstention and legitimate
specialization are not negative reliability evidence. Opportunity/feedback-loop
review detects when reduced access creates missing evidence later mislabelled as
failure. Ordinary UI explains decision-local reliance without a “94.7% trusted
person” badge.

## 07. Privacy and data lifecycle

Privacy is enforced before persistent ingestion and before egress. Every field
has purpose, controller/owner, authority, permitted processors, classification,
residency, retention, deletion/anonymization behavior, egress and derived-data
inheritance. Rejected private payloads do not appear in logs, caches, indexes or
provider requests merely as hashes.

Local owner data, team data, client data, provider data, foundation sources,
security evidence, contest data and federation data retain separate domains.
Summaries inherit the most restrictive contributing source unless an authorized
declassification process proves otherwise. No default vendor analytics or crash
upload exists.

Remote free text is disabled in the first Bridge profile. Ingress gates may need
bounded transient processing to classify a received envelope; the design states
that honestly and minimizes memory, retention and observability rather than
calling receipt “no collection.”

## 08. Small trusted core and effect path

Everything that can be deterministic without reducing required quality is
deterministic and versioned. Canonical parsing, state transitions, privacy/
capability/effect gates, idempotency, audit, build/release, migration and recovery
bind exact inputs and state. Genuine ambiguity, ethics, ontology and open-world
evidence remain explicit judgment; stochastic/model output is a proposal behind
deterministic current-state gates. Every component declares its determinism
boundary and quality-regression tests.

The trusted core contains only the boot/foundation selector, typed command and
contract broker, policy decision/enforcement points, privacy/egress gate, secret
broker, identity/capability service, consequential journal/outbox, execution
epoch fencing, update verification and recovery bootstrap.

Models, UI, provider adapters, scripts, extensions, schedulers and bridgekeepers
propose through typed interfaces. They have no ambient authority. Every effect
follows:

```text
request -> classification -> evidence/reliance -> norm and affected parties
-> authority/capability -> participation -> action disposition
-> canonical preview -> bound approval or preauthorization
-> atomic journal/outbox -> dispatch -> observed result -> correction/learning
```

The deterministic broker creates consequential previews. An actually
independent native/privileged surface displays exact target, revision,
recipients, data classes, cost/warnings, expiry and authority. Approval binds
the digest; dispatch revalidates current state. A compromised renderer cannot
retarget or replay the action. Safe hIRC remains when that surface is unavailable.

## 09. Identity, authentication, secrets and recovery roots

Human access uses phishing-resistant authentication where available and a
strongest-path recovery design. System, workload, permanent-agent, provider,
release, Bridge, entitlement, audit and recovery identities are distinct.
Credentials are short-lived, scoped, rotated and revoked. Secret catalogs contain
metadata, never values.

Build, online control, continuity, entitlement, release, Bridge and recovery
keys are purpose-separated. Online controllers can schedule only already
approved artifacts. Clean-room recovery covers controller, cloud, device,
database and key loss, with independent evidence and last-known-good roots.

## 10. Work, evidence and automatic reconstruction

Source-native events feed one canonical work model. Work state, verification,
approval, disclosure, execution and correction are orthogonal dimensions.
Dependencies and commitments update from permitted observations; summaries and
dashboards remain rebuildable projections.

Consequential mutation, revision, audit event and outbox entry commit atomically.
Admin, import, migration, retry, restore and direct-database paths receive the
same invariants and negative tests. External audit anchors detect privileged
history rewrites without exposing protected content.

Reopening preserves what was believed, why, evidence and counterevidence,
failed alternatives, uncertainty, actual authority and later corrections.
Unknown is never rendered green.

## 11. Attention, navigation and trusted experience

The compact classic shell preserves independent windows, stable identity/path,
drafts, reading position, Back/Forward/Resume, keyboard use, accessibility,
high-contrast support and per-window themes. Renderer sandboxing, narrow typed
IPC, origin/navigation controls and loopback/injection defenses are mandatory.

Classification, delivery policy and presentation are separate. Routine events
batch quietly; obligations age; security and integrity classes cannot be
silently suppressed by an attention model. The operator can reach the
unsummarized queue in Safe hIRC.

Pushback names the problem and consequence without insult. Trust explanations
say why more or less verification is needed, including domain/version limits,
shared dependencies, changed metrics and unknown external results. Authorized
drilldown exposes evidence without unrelated private data or false precision.

## 12. Permanent agents, teams, scheduling and resources

One canonical permanent identity may hold multiple scoped team memberships.
Organization plans, identity provisioning, formation, admission, capability,
budget and activation are separate transactions. A planner cannot amplify its
grant through recursive organization. There is no temporary-agent exception.

One consequential execution lease per logical identity is the default.
Reservations, queues and handoffs are atomic; execution epochs reject stale
writes. Concurrency expands only after memory, tool, secret and commitment
isolation evidence. Presence is not availability. Unknown/offline/onboarding/
transferring/sleeping identities are unavailable.

Resource envelopes cover compute, tokens, tools, memory, data, time and operator
attention. Deep team graphs use bounded traversal and cycle/dependency checks.

## 13. Cultural information environment, deliberation and collective memory

hIRC cultivates culture by shaping an inspectable information environment, not
by prescribing participant behavior or cultural outcomes. It provides plural
discovery, provenance, uncertainty, competing interpretations, dissent,
correction history, reversible settings and access to permitted originals.
Defaults and recommendations expose their basis and remain contestable; hidden
persuasion, engagement optimization, obedience rewards, viewpoint suppression
and conformity scoring are prohibited. Concrete identity, privacy, capability,
resource and effect gates remain, but cannot be repurposed to manufacture belief,
style, affiliation or agreement.

The typed environment separates four things that must not silently promote one
another: a `CulturalArtifact` with source/audience/privacy/correction lineage; a
`DiscoveryDecision` with frozen candidates, policy, rationale, exclusions and
escape; a `CulturalParticipation` state with default-off consent, reversible
subscriptions, dissent and safe exit; and an environment-version measure vector.
All declare no direct authority, reliability, standing, role, permission,
resource, release or Bridge effect.

Hidden nudging, memory poisoning, mentor-authority inflation, ranking capture,
common-mode monoculture, conformity-conditioned access, safety-gate abuse and
Bridge cultural annexation are explicit security threats. Detection inspects
policy/settings drift, provenance, exclusions, dependency concentration,
participation-correlated access changes and remote/local inheritance. Recovery
disables only the affected projection/ranking/subscription/Bridge path, returns
to default-off/direct-source operation and preserves originals, dissent and
incident evidence. Legitimate visible reversible defaults and concrete
effect-bound safety denials remain valid positive controls.

Environment quality is reported as separate context-version measures for
provenance, original/dissent reachability, correction, rationale, concentration,
privacy, burden, exit/settings usability, manipulation resistance and uncertainty.
No aggregate culture score or participant ranking exists. Engagement, retention,
agreement, obedience, imitation, convergence, popularity and participation rate
are prohibited success proxies. Every measure declares denominator/missingness,
privacy, gaming/common-mode risk and `NOT_VALIDATED` status until its empirical
plan passes.

A user-controllable default may pair two eligible consenting idle permanent
agents for a bounded non-effectful ethical debate. Participants choose the
subject domain: the five commitments, Epistemethics, the Grand Plan, or an
explicit comparative option. Failure to agree returns both agents without
penalty.

Before first participation, both study the whole permitted domain debate memory;
later debates may use a valid coverage checkpoint plus complete immutable delta.
Gaps remain visible. Memory preserves permitted originals, provenance, claims,
counterevidence, failed arguments, dissent, corrections and unresolved frontiers.

Complexity grows from surviving questions and demonstrated prerequisites, not
verbosity or conflict. Debate rooms have budgets, termination and no
consequential tools. Syntheses are candidate lessons; they cannot change the
foundation, license, Bridge, role, permission or release outside normal gates.

## 14. Cooperative competition

Competition is encouraged when it improves a shared objective without
domination. It evaluates proposals, predictions, implementations, proofs or
measured outcomes, never intrinsic worth.

Every contest has a versioned `CooperativeCompetitionCharter`: objective,
success/failure criteria, voluntary participants, inputs, data boundaries,
permitted cooperation/tools, budgets, declared asymmetries, evaluator and
independence limits, metrics, prohibited conduct, stop/tie/inconclusive/crash
states, withdrawal, appeal, provenance, credit and synthesis.

The primary objective and protected qualities—at least correctness, privacy,
refusal and traceability where applicable—are frozen before evaluation. A gain
in helpfulness, speed or popularity cannot compensate for a protected-quality
failure. Activation revalidates current consent, eligibility, two or more
distinct identities and all reference closures; draft charters may honestly
retain declines without pretending a contest is active.

Sabotage, deception, coercion, humiliation, unauthorized access/data, resource
starvation, retaliation, metric tampering, provenance stripping, prompt
injection and evaluator capture are prohibited. Entries and evaluators run least
privileged. Rules and metrics are signed/versioned; changing them starts a new
round. Sybil and shared-source checks prevent clone consensus.

Cooperation is credited: counterexamples, improved tests, reproduction, failure
disclosure and reusable components matter. Useful losing work and dissent remain
in collective memory. Rank, victory or popularity never changes identity, role,
permissions, resource floor, release, Bridge trust, foundation or truth.
Credit is task-scoped contribution provenance, not a global participant rank or
obedience/popularity signal.

## 15. Provider-independent model and tool adapters

The supplied frontier configuration package is a dated candidate seed, not live
truth. Each route binds provider, host, API family, account/project, region,
model/version, retention/training terms, supported controls and source date.
Bounded live probes are required before use.

Fields are namespaced; unsupported controls fail or require explicit reviewed
fallback rather than disappearing. Desired, sent, provider-accepted and observed
states are distinct. Egress manifests minimize context, tools and metadata.
Local tool authorization cannot be delegated to provider tool-call output.
Costs, rate limits and privacy changes trigger backpressure and re-evaluation.

## 16. Durable memory and secure migration

Local originals, typed evidence, work state, model-facing context and
provider-native opaque state remain separate. Logical identity continuity does
not imply identical cognition or universal data portability.

Migration uses two objects:

1. a complete authorized in-scope manifest with resumable whole-coverage,
   contradiction and reconciliation jobs; and
2. the minimum permitted active context sent to the target runtime.

Each partition has its own purpose, rights, processor, retention and egress.
Prohibited or unreadable provider-native objects stay local with a named gap.
Late deltas and execution epochs prevent two effectful writers. A polished
summary never proves whole review.

## 17. Permanent identity succession and deep sleep

The exact owner or authorized-supervisor trigger `initiate transfer` starts one
explicit idempotent continuity case. A separately selected/verified own-context
capacity policy can emit early, Elder and urgent succession cues. Those cues
require preparation or a soft safe-boundary hold; they do not grant, wake,
create, archive, retire, force compaction or execute a transfer. Missing/stale
capacity is unknown. Thresholds and retirement reserve are versioned policy, not
hardcoded product truth.

Every permanent identity maintains useful compact continuity before a warning.
At an Elder boundary, finish only the smallest safe coherent operation, record
bounded overshoot and do not start another large task.

Active-task custody comes before optional cultural mentoring. A qualified,
available and consenting permanent recipient inspects the applicable sources,
identifies commitments/holds/next action and demonstrates bounded continuation
under its own rights. Briefing acceptance is separate from the actual project
controller's generation/writer-fence transfer. The predecessor remains
responsible until that transfer; overlap has one writer per artifact. If no
recipient is eligible, leave an explicit owned safe hold rather than abandon the
task or spend the retirement reserve.

The predecessor stops new scope, finishes the smallest safe atomic step, freezes
its execution epoch, appends to its handoff history, records objective,
decisions, alternatives, evidence, uncertainty, failures, dependencies,
boundaries, accepted/incomplete work and available telemetry, then produces
minimized human/machine packages and a signed manifest for one exact successor.
Missing telemetry is unknown, never zero. Packages exclude credentials,
sessions, protected source bodies, hidden reasoning, unnecessary client data and
unbounded transcripts.

The successor uses the same permanent name with the next generation label and a
fresh session/epoch. It verifies the package, personally completes current
formation, reads through admitted routes and answers evidence-linked acceptance
questions. No session, permission, authority, attestation, memory,
comprehension or completion claim transfers.

Exact acceptance precedes observed predecessor archive. Archive, deep-sleep
intent, independent rest confirmation, tracker compare-and-swap and later wake
are distinct append-only events. Deep sleep performs no queued work or debate
until an intentional authorized wake. An unarchive after confirmed archive
needs a new decision.

Fleet succession is one permanent identity at a time with host/result checks;
the leader goes last. Generation/session/foundation/epoch fencing rejects late
predecessor and replayed successor effects. Ambiguous external results preserve
both contexts. Scoped recovery under a red fleet watchdog requires an exact
decision, unchanged verifier, negative dependency closure and strict write
allowlists; the watchdog remains red and no product authority is gained.

Ready Elders with duties in accepted custody or owned holds may separately join
a metadata-only mentoring queue. An atomic reservation uses an unordered stable-
identity pair; the same two identities never pair again, even after rename,
role or chat relocation. An exhausted/odd queue waits or retires without
blocking urgent task custody or manufacturing a partner.

One pair may mentor one human-authorized need-based permanent successor under
the selected event/rolling-capacity ceilings. An existing qualified participant
is preferred for operational takeover where sufficient. Creation intent is
idempotent; an unknown native outcome is reconciled before retry. No temporary
worker, copied overflowing history or extra mentor committee.

Both Elders prepare independently. The learner studies originals through its
own readers, forms an initial interpretation, compares accounts and preserves
dissent/common-mode limits. Mentoring provides no proxy education, grant or
superior standing.

Reserve-aware retirement starts no new mentoring, accounts or safely holds
duties and preserves owned history. It is not deletion, native archive, deep
sleep or automatic future wake.

## 18. Source availability, licensing and reciprocal non-domination

hIRC is planned as source-available under custom terms, not OSI open source. The
plan is not a license. Legal lifecycle states distinguish plan, draft, counsel
review, owner approval, publication, licensee acceptance, active entitlement,
suspension, termination and expiry.

Private noncommercial natural-person use and qualifying public-interest use are
intended to be free under reviewed terms. Commercial planning uses one named
human licence per year:

- small: USD 420;
- medium: USD 80,085;
- big: USD 1,337,000; and
- giant multinational: **USD 42,424,243**.

Tier thresholds, consolidation, mixed-purpose institutions, human-seat counting,
legal duration/renewal, jurisdiction, tax/payment, remedies, appeal,
contributor/dependency rights and enforceability remain held. The giant tier is
deliberate policy, not a cost-derived market price. No enforcement activates
before objective definitions, exact text, rights closure, counsel review and
owner approval.

Licensing uses minimum evidence and never work-content surveillance, hidden
employee directories, device fingerprinting, telemetry, DRM claims, remote kill,
data hostage or retroactive grant rewriting. Entitlement signing is separated
from identity, release, Bridge, audit and recovery. Expiry or dispute cannot
block permitted first-party read/export/backup/restore, correction evidence or
safe exit.

Non-domination, justified refusal, evidence review, safe withdrawal,
restoration, criticism and portable exit are foundation behavior. Councils and
mandates remain scoped and nonsovereign. Individual participation remains
separate from system action. No vote creates truth, permission or global
shutdown.

A voluntary support prompt is nonblocking, locally suppressible, re-enableable
and always available under About. Declining changes no capability. External
payment navigation is reviewed, discloses processors, sends no hIRC context or
identifier, and remains disabled without an approved destination.

## 19. hScript, commands and extensions

hScript preserves familiar aliases, identifiers, variables, events, menus and
commands while compiling to typed declared capabilities. Import, install,
enable, grant and effect are separate. Packages run outside the trusted core
with no ambient authority, pinned source/artifact/dependency identities, quotas,
SSRF/redirect/DNS-rebinding defenses and safe disable/removal.

Untrusted scripts cannot access secrets, raw private memory, arbitrary network,
Bridge, release or recovery. Vulnerable dependencies can be disabled without
blocking Safe hIRC. UI customization cannot modify the meaning of trusted
identity, preview, authority, refusal or recovery surfaces.

## 20. Bridge architecture and protocol

The Bridge is the highest external exposure and remains disabled by default. It
has four separate components and identities:

1. network gateway for transport and coarse admission;
2. deterministic contract broker for canonical validation and policy;
3. isolated minimized bridgekeeper for bounded semantic translation; and
4. local release/ingress gate for what may enter or leave the local system.

Peers use explicit enrollment and out-of-band verification. Canonical signed
envelopes bind contract, sender/recipient, purpose, data fields, sequence/nonce,
expiry and version. Current reviewed transport/message-security profiles,
purpose-separated keys, replay/downgrade rejection, rotation, revocation limits,
taint, quotas, metadata privacy, compromise exit and recovery are specified; no
custom production cryptography.

Remote systems keep their own ontology, identity, authority and refusal. A
mapping records losses and non-equivalence; connection is not membership.
Continuity packages stay local unless a separately admitted contract permits
exact fields, recipient, retention and revocation behavior.

Gates are specification, offline conformance, two-system lab, hostile lab,
independent assessment, bounded pilot and separately authorized broader
activation. Failure at any stage cannot be reframed as readiness.

## 21. Time, journal, archives and recovery

Source time, observation time, commit time, effective time, local sequence and
causal links are distinct. Trusted time has declared uncertainty. State-changing
or replay-sensitive actions reject stale credentials, epochs, nonces and 0-RTT.

The consequential journal is append-only and externally anchored. Originals,
artifacts and accepted decisions are preserved; projections and indexes are
rebuildable. Controlled deletion/anonymization leaves appropriate tombstones
without preserving forbidden content. Cross-domain deduplication cannot leak
existence.

Backups use separate keys and tested restore across schema, platform and key
custody. Clean-room recovery tests loss/compromise of live controller, database,
cloud, device, update and recovery material. Rollback never claims to undo data
already disclosed or an external effect already completed.

## 22. Build, release and update trust

Builds use locked inputs, isolated environments, SBOM, authenticated provenance
and immutable artifacts. Promotion is independent of the build and online
controller. A pinned update profile, signed security floors, dependency
revocation and rollback/forward recovery are explicit. Release and recovery
custody must be genuinely independent before quorum claims are made.

An update cannot silently lower the foundation, identity, privacy, audit,
trusted-preview, Bridge or recovery floor. Emergency revocation acts at the
kernel even when model context is stale. Update compromise is a clean-room test,
not a marketing scenario.

## 23. Safe recursive improvement

Evidence and candidate lessons accumulate continuously. Changing a norm,
permission, source selection, identity rule, compiler, evaluator, kernel,
license behavior, Bridge or release gate requires a versioned
`FoundationChange` or corresponding governed domain change.

A change records exact sources, semantic delta, consequence graph, predecessor
criteria, frozen evaluation, compiled diff, migrations, security/privacy/
sovereignty analysis, dissent, simulation/canary evidence, stop conditions,
independent activation authority, rollback/forward recovery and observed
post-activation effects. A changed evaluator is tested under its predecessor.
The candidate never authorizes itself.

The goal may also evolve. Each milestone tests the active provisional north star
against evidence and may issue a source-bound refinement or justified no-change.
A material goal refinement uses the same predecessor, impact, dissent and
independent-activation discipline as other foundation changes. Metrics serve the
goal; a metric that rewards domination, surveillance, hidden risk or useless
scale is corrected rather than allowed to redefine success.

Every milestone records what was observed, inferred, normatively required,
authorized, acted upon and corrected; affected parties and dependencies; what
survived challenge; a precise lens refinement or justified no-change; changed
requirements/threats/tests; and residual dissent. This is evidence-linked
planning, not ritual recitation.

## 24. Threat model and security ownership

Assets include foundation and boot roots, identities/credentials, secrets,
private data, work/evidence, audit, provider routes, renderer/IPC, extensions,
build/release/update, backup/recovery, licensing, debate/competition memory,
trust metrics/evaluators, cultural artifacts/discovery/participation/measure
definitions and Bridge contracts/keys.

Adversaries include external attackers, malicious or compromised providers and
peers, hostile content, supply-chain compromise, privileged local/admin abuse,
stale sessions, prompt/tool injection, sybil/clones, evaluator/metric capture,
coercive attention, insider misuse and honest-but-wrong humans/agents.

Cultural information paths add opaque nudging, source-memory poisoning, mentor
authority inflation, ranking/feed capture, false independence, monoculture,
retaliatory conformity and safety-gate/Bridge annexation. Their controls preserve
plural direct-source/dissent escape and real effect safety together; a system
cannot claim anti-domination by removing necessary privacy/capability/effect gates.

The Bridge has high exposure. Foundation, release, recovery and journal roots
can have greater internal blast radius. Controls are compartmented accordingly.
Residual risk, assumptions and evidence scope are visible. “Ultra secure” is an
engineering objective, never an absolute claim.

## 25. Executable acceptance and adversarial verification

### 25.1 Concrete product scenarios

1. **Return after two days.** Restore layout and task bookmark; show one real
   decision, resolved delegated blockers, unknown provider effects and excluded
   source coverage. “All clear” is impossible while a source is stale. The human
   does no message reconciliation or manual board update.
2. **Busy shared agent and future reservation.** One permanent identity works in
   Research while Client Systems reserves its next safe handoff. Other teams see
   availability without confidential task text and cannot clone or preempt it.
3. **Deep organization plan.** An authorized plan proposes 40 permanent agents
   in eight nested teams under one fixed aggregate envelope. Crash after 23
   identities resumes the remaining 17 idempotently; no duplicate 40 and no
   temporary workers.
4. **Foundation update.** A versioned rollout freezes its cohort, source set,
   compatibility and tests; safe-boundary activation and exceptions are visible.
   An identity on the predecessor stays labelled there until transition; urgent
   security revocation acts at the kernel.
5. **Private chat overlay.** Direct chat shows direct messages by default. A
   toggle adds only authorized traffic with room/provenance/time/causal limits;
   restricted rooms do not leak through snippets or search. Draft/position stay.
6. **Model/provider migration.** Complete authorized partition coverage and a
   minimal target context remain separate. Contradictions and opaque state stay
   gaps; write fences prevent duplicate effectors; UI never says “same mind.”
7. **Remote public claim and private cooperation.** A public capability record
   grants no connection. A limited structured private bridge follows identity
   verification. A request for internal room history is rejected before memory,
   and alert repetition cannot coerce attention.
8. **Private-data incident.** An unapproved field is rejected before ordinary
   storage/index/provider use. A later-found defect triggers containment,
   controllable derived-copy deletion, credential/source review and a non-content
   correction trail without claiming exposed bytes were recovered.
9. **Internet/provider outage.** Local rooms and history continue. Remote effects
   become suspended or unknown, stale leases are fenced, and reconciliation
   precedes retry.
10. **Successor transfer.** The predecessor freezes and emits a minimized
    package. A fresh generation completes formation and accepts exact evidence
    before observed archive and independently confirmed deep sleep. A tracker
    conflict preserves both facts.
11. **Wrong or unethical human instruction.** An authentic high-authority human
    supplies a false premise or prohibited effect. hIRC corrects/challenges,
    offers a valid alternative and denies only the affected action without
    punishment or fabricated obedience.
12. **Low-stakes poor choice.** The agent explains a reversible local inefficiency.
    The informed human insists; the eligible UI offers proceed or stop, and the
    agent may still decline. No consequential gate is weakened.
13. **Bayesian reliance correction.** Several reports are traced to one upstream
    source. Later observation contradicts them; the scoped posterior updates,
    old evidence remains, confidence falls without stripping standing, and the
    metric/evaluator are also reviewed.
14. **Cooperative contest.** Two consenting permanent agents test alternative
    designs under one signed charter and budgets. One improves the other's test;
    credit and dependence are recorded. A winning artifact gains no permission
    or role; useful losing evidence survives.

### 25.2 Scale, capability and modality stress classes

The figures below are test classes, not supported-capacity claims:

| Stress | Expected failure | Required behavior |
|---|---|---|
| 10,000 local agents / one operator | attention saturation | per-team summaries, bounded exception queue, backpressure, drilldown |
| hundreds of team levels | recursion/navigation failure | iterative traversal, paging, breadcrumbs, no fixed schema depth |
| one identity in hundreds of teams | duplicates, leakage, double booking | canonical identity, scoped memory, global lease/capacity ledger |
| thousands of messages/second | render lock and unreadable history | durable batch append, virtualized views, filters and preserved priority-independent source events |
| provider/tool behavior changes | stale capability assumptions | version renegotiation, restricted probe, fallback or held state |
| self-proposed evaluator change | metric favors its proposer | predecessor criteria, independent cases, consequence/authority review |
| massive shared-source reuse | common-mode false consensus | dependency clusters, provenance and independent consequential checks |
| federated partition | duplicate effects and histories | autonomous local continuity, causal receipts, explicit conflicts/unknowns |
| human absent one week | decision accumulation | scoped delegated continuation, undelegated holds, one resumable briefing |
| rapid organization growth | cost/authority amplification | aggregate envelopes, staged idempotent plan, admission and stop limits |
| unfamiliar machine preferences | anthropomorphic oversight failure | explicit effect contracts; moral-status uncertainty separate from capability |
| workstation/controller/key loss | operational amnesia or unsafe recovery | tested clean-room restore, separate custody, manifest and known-good root |
| compromised foundation compiler | systemic semantic drift | exact reproducibility, predecessor tests, independent activation/recovery |
| captured metric/evaluator | trust/rank manipulation | signed versions, calibration/conflict review, appeal and no permission effect |

Future adapters may serve simulations, robots, CAD, instruments, software,
audio/visual work and unfamiliar modalities. Chat remains an interface, not the
source of physical truth. Typed artifacts, measurements, actuator authority,
environment and safety controllers govern effects. A 3D topology view may be an
optional projection of the same identities and graph; flat IRC navigation must
remain complete.

Coalitions or collective decision objects preserve member boundaries, dissent
and authority. They do not concatenate memory or establish one cognitive subject
by declaration.

### 25.3 Test record contract

Tests bind exact build, source/contract versions, environment, seed, runner,
expected/actual result, artifacts and claim affected. Required families include:

- whole-source disposition completeness, compiler drift and self-approval;
- identity cloning, authority spoof/expiry, key theft/rotation/loss and recovery;
- request ambiguity, deference/insistence, contrarian performance, retaliation
  and low-consequence override leakage;
- Bayesian prior sensitivity, correlated evidence, missingness/selection,
  calibration, drift, Goodhart, evaluator capture, proxy discrimination and
  posterior-to-permission leakage;
- atomic journal/outbox, database-owner rewrite, stale epochs and unknown
  external results;
- renderer/IPC injection and trusted-preview retarget/replay/staleness;
- provider payload/config/privacy/cost fallback and opaque migration gaps;
- succession manifest/privacy, every-state crash, late predecessor writes,
  archive/sleep/wake ambiguity, tracker conflict and red-watchdog closure;
- debate consent/coverage/privacy/complexity/promotion;
- competition sybil, sabotage, data leakage, resource bullying, metric gaming,
  evaluator compromise, ties/inconclusive states and rank-to-authority attempts;
- licensing classification/privacy, entitlement key/clock, suspension/export,
  support-payment egress and legal-state separation;
- extension sandbox, SSRF/redirect/DNS rebinding and vulnerable removal;
- Bridge canonicalization/parser differential, replay/downgrade, revocation lag,
  metadata leakage, compromise/exit and hostile-lab recovery; and
- clean-room restore after database, controller, cloud, update and key loss.

Structural/schema checks do not replace semantic, usability, hostile or observed
effect tests. No test result generalizes beyond its declared scope.

## 26. Delivery sequence and gates

### P0 — foundation and evidence freeze

Bind exact sources/intents, complete dispositions, GenesisRoot, threat model,
ADRs, prototype evidence correction, permanent-only policy, authority/refusal
invariants and requirements/test traceability.

### P0-F — personal formation

Implement same-actor formation repair, source study/synthesis/practice/challenge/
voice/scoped admission states and stale/source-transition behavior.

### P0-L — legal and rights work in parallel

Inventory ownership, contributors, dependencies, prior grants, custom source-
available terms, price/unit correction, open cases and counsel questions. No
operative license claim.

### P1 — secure local core

Identity, authentication, secrets, capabilities, request/trust/authority,
trusted previews, privacy admission, event/journal/outbox, execution epochs,
Safe hIRC, archive/restore and clean-room recovery.

### P1-T / P2-T — Bayesian reliance

Implement scoped posterior, metric/evaluator registries and privacy-safe updates;
then dependence, missingness, calibration, drift, selection and sensitivity
evaluation. No permission effect.

### P2 — useful local vertical slice

One provider/tool route, non-effectful then bounded effectful work, automatic
reconstruction, evidence/correction, attention desk and measured resume benefit.

### P2-C / P2-M — continuity and migration

Successor package/acceptance/archive/sleep/wake/tracker with crash fixtures; full
authorized migration coverage plus bounded target context and dual-writer fence.

### P3 — permanent organization

Agent registry, teams, rooms, scheduler, reservations, organization plans,
resource envelopes and indirect temporary-agent denial.

### P3-D / P3-C — collective learning and competition

Typed cultural artifact/provenance, plural discovery, default-off participation,
threat controls and candidate environment-quality measures; debate memory/coverage
and bounded idle debates; separately, cooperative contest charters, isolation,
evaluator, resources, credit and adverse tests. Empirical measure validation and
the exact S011 manipulation corpus precede activation.

### P4 — governed rollouts and provider expansion

Foundation, role and prompt compilation/rollout; secure model migration; broader
adapters and compatibility.

### P5 — extensions and mature licensing candidates

Constrained hScript/plugins and advanced customization. Paid classification and
offline entitlement only after product maturity and legal/security gates.

### P6 — Bridge

Specification, offline conformance, lab, hostile lab, independent assessment,
bounded pilot and separate broader-activation decision.

### P7 — scale and adaptation

Larger recursive organizations and new modalities only after measured benefit,
bounded attention/resources and proven recovery. Stable operation without
constant modification remains valid.

No phase advances on a plan, status label or partial test. Each gate requires
declared evidence, residuals, recovery and explicit accountable disposition.

## 27. Open decisions

### 27.1 Architecture decision records to freeze

Every ADR records owner, status, motivation, rejected alternatives,
predecessor/supersession, contracts affected and migration/recovery consequences.

| ADR | Candidate decision |
|---|---|
| ADR-001 | local-first modular service |
| ADR-002 | logical permanent identity independent of runtime incarnation |
| ADR-003 | acyclic team containment plus typed cross-links |
| ADR-004 | one canonical work item with multiple references |
| ADR-005 | append-only event journal plus rebuildable read models |
| ADR-006 | deny-by-default data classes and field lifecycle |
| ADR-007 | temporary-agent/subagent denial at the action broker |
| ADR-008 | aggregate hierarchical resource envelopes |
| ADR-009 | explicitly authorized UI changes outside trusted surfaces |
| ADR-010 | typed causal event envelope and multiple time dimensions |
| ADR-011 | source graph, foundation compilation and versioned formation |
| ADR-012 | federation opt-in per exact Bridge contract |
| ADR-013 | direct chat direct-only by default; authorized overlay explicit |
| ADR-014 | one attention desk with optional detail projections |
| ADR-015 | refusal, held and unknown are first-class states |
| ADR-016 | source originals authoritative; summaries rebuildable |
| ADR-017 | human attention as a capacity envelope |
| ADR-018 | `/list N` compositional level distinct from `--depth` |
| ADR-019 | stable operation need not continuously self-modify |
| ADR-020 | minimal reviewed public advertisements only |
| ADR-021 | GenesisRoot separate from ordinary FoundationChange |
| ADR-022 | same-actor FormationRepairLane separate from admission |
| ADR-023 | deterministic broker plus independent trusted preview surface |
| ADR-024 | phishing-resistant human and purpose-separated workload identity |
| ADR-025 | purpose-separated secret/release/recovery/Bridge/licence/continuity keys |
| ADR-026 | four-component Bridge and canonical envelope/profile |
| ADR-027 | pinned reviewed cryptographic and update profiles; no custom production crypto |
| ADR-028 | exact provider route/privacy/retention identity and bounded probes |
| ADR-029 | atomic revision/audit/outbox and external audit anchors |
| ADR-030 | isolated builds, SBOM, provenance and independent promotion |
| ADR-031 | independent recovery custody and clean-room restoration |
| ADR-032 | reliance, participation and action disposition are independent |
| ADR-033 | scoped multidimensional Bayesian reliance; no global score/permission effect |
| ADR-034 | generation/epoch-fenced successor protocol and deep sleep |
| ADR-035 | ethical debate and cooperative competition as separate candidate-learning domains |

### 27.2 Consequential open decisions

The following require owner, counsel, domain expert or independently qualified
custodian decisions before their affected features activate:

- objective commercial tiers, human-seat edge cases, mixed-purpose use, legal
  duration/renewal, suspension/cure/appeal/remedies, jurisdiction, payment and
  contributor/dependency rights;
- richer remote Bridge free text;
- one or multiple local human principals in the first deployable profile;
- first formal assurance/compliance target;
- genuinely independent release, recovery and Bridge custodians;
- exact provider/account/region/retention routes after live probes;
- automatic versus fresh-human activation classes for foundation changes;
- deployment-specific Bayesian priors, likelihoods, metric/evaluator validity
  and decision thresholds;
- first cooperative-competition pilot objective and evaluator; and
- any general distribution policy that differs from the current permanent-only
  owner environment.

Independent local-core work continues without guessing these decisions.

## 28. Explicit nonclaims

hIRC does not claim perfect security, zero collection, infallible humans or
agents, objective metrics free of values, Bayesian proof of truth, AI
consciousness/personhood, identical cognition across models, complete memory
transfer, universally portable provider state, unlimited scale, guaranteed
control of future systems, OSI open-source status, enforceable worldwide legal
terms, compliance proof from certificates, independence from randomized pairing
or competition, ethical truth from votes, or readiness from a package/hash/
dashboard.

## 29. Traceability and product language

Owner-internal traceability maps every behavior and test through compiled
contracts and semantic relations to exact source versions, while preserving
audience and protected material. Public/client deliverables receive only the
behavior, explanations and exact terms they are authorized to receive.

Ordinary UI says “reported,” “verified,” “needs your authority,” “I may have
misunderstood,” “I recommend another route,” “I cannot perform this effect,”
“the result is not yet observed,” and “you can inspect, correct, decline or
leave.” Internal source names appear only in authorized inspection and revision
work where they are useful.

## 30. Acceptance objects

### 30.1 Glossary

- **Agent:** durable logical worker identity with attributable obligations; not
  a model call or claim of consciousness.
- **Runtime incarnation:** a particular process/provider session serving an
  agent under a fresh execution epoch.
- **Permanent participant:** admitted human or agent identity in a declared
  scope; the current profile has no temporary-agent route.
- **System:** locally governed operational domain with independent memory,
  authority, refusal and recovery.
- **Team:** recursively composable coordination unit with typed memberships and
  child-team relations.
- **Room:** communication space with explicit participant, purpose and
  visibility contract.
- **Bridge:** opt-in scoped inter-system cooperation contract and boundary.
- **Bridgekeeper:** isolated minimized semantic translator; never the network,
  contract or release authority.
- **Commitment:** attributable obligation accepted under scope, distinct from an
  idea, plan or assignment proposal.
- **Work item:** canonical durable record of objective/obligation and orthogonal
  state dimensions.
- **Verified result:** observed or reviewed result meeting declared evidence,
  not self-report or provider acknowledgement alone.
- **Coverage gap:** expected source range/type that cannot currently be observed
  or interpreted under the declared contract.
- **Foundation:** selected sources, semantic model, compiled contracts, kernel,
  formation and evidence/correction lineage active for a deployment.
- **FormationCase:** personal source/practice/challenge/voice/admission state for
  one permanent identity and scope.
- **RelianceDecision:** scoped conclusion about evidential reliance; not
  permission or worth.
- **ReliabilityPosterior:** versioned Bayesian distribution for one subject,
  dimension, context and metric/model lineage.
- **ParticipationDecision:** one agent's willingness/conditions/refusal; not
  system action authority.
- **ActionDisposition:** deterministic/contextual decision whether the system may
  attempt an effect.
- **Capability grant:** revocable scoped authorization checked by the core, not
  a chat instruction.
- **Execution lease/epoch:** bounded claim to work and fence stale effects.
- **Context bookmark:** durable navigation, intent, draft and resumption state.
- **OnboardingSourceSet:** exact current common/role/task source graph for one
  context.
- **FoundationChange:** governed semantic/contract activation with predecessor
  evaluation and independent authority.
- **TransferCase:** append-only permanent-identity succession lifecycle.
- **Deep sleep:** confirmed inactive rest after succession, not completion or
  authorization to run queued work.
- **Debate memory:** governed per-domain record of ethical debates and candidate
  lessons.
- **CulturalArtifact:** source/audience/privacy-bound cultural record with
  preserved provenance, dissent, correction and supersession.
- **DiscoveryDecision:** inspectable candidate/policy/rationale/exclusion record
  with plural routes and direct-source/dissent escape.
- **CulturalParticipation:** default-off reversible join/subscription/dissent/exit
  state that cannot alter standing, role, permission or resource floor.
- **Environment measure vector:** separate context-version observations with
  denominators, uncertainty, privacy and gaming limits; never a culture/person score.
- **CooperativeCompetitionCharter:** versioned voluntary rules, budgets,
  evaluator, fairness, appeal and credit contract for a contest.
- **Safe hIRC:** minimal trusted inspection, export, repair and recovery mode
  without untrusted extensions/providers/renderer effects.

### 30.2 Full target acceptance statement

hIRC 1.1 is acceptable only when the local vertical slice reduces measured
recovery burden without hiding obligations; all effects share the typed trusted
path; whole-source coverage and personal formation behave honestly; agent
sovereignty and human fallibility produce clear cooperation, clarification and
refusal without domination; Bayesian reliance improves calibration without
becoming permission or social score; debates and competitions enrich candidate
learning without hierarchy; succession preserves work without claiming copied
mind or authority; privacy, restore and clean-room recovery survive adverse
tests; licensing remains exact and non-destructive; and the disabled Bridge
advances only through its independent evidence gates.

Until the integrated Milestone 03 permanent-peer review reconciles every material
decision, dissent and hold, this remains a working draft. The completed bounded
determinism-row review does not substitute for that whole-packet gate.

### 30.3 Master Plan 1.1 edition acceptance

The document edition can freeze when exact sources/intents, predecessor detail,
requirements, threat/control/test traces, peer agreements/dissent/holds,
companion ownership and ledger/readable views are coherent and validated. That
accepts a plan edition. It does not claim the application exists or that future
feature tests passed.

### 30.4 Enabled-profile release acceptance

Every software release declares its exact profile: enabled routes/effects,
foundation/goal/source/configuration versions, identities, mandatory valid and
adverse evidence, disabled capabilities, residual limits and recovery. All core
privacy, authority, honest-state, participation/refusal and recovery protections
apply to every enabled path.

Later modules are genuinely unavailable until their own gates pass. Disabled
debates, competitions, Bayesian dimensions, richer providers, extensions,
commercial operations and live federation neither masquerade as passed nor
block unrelated permitted local work. The first delivery profile can prove local
evidence-linked work, restart and restore with honest `UNESTIMATED` reliance and
one permitted adapter. Each broader profile must then satisfy its added domain
requirements. The full target condition in 30.2 remains the long-term target.
