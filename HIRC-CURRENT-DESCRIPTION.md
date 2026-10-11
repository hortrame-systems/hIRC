# hIRC — current detailed description

**Current as of:** 2026-10-10
**Document purpose:** owner handoff and current-state entry point
**Design baseline inspected:** local branch `codex/hirc-master-plan-security`,
commit `1c525e3b464c58b6e037faaf6bb76626b32364e4` before this document was added
**Project state:** integrated and extensively validated design corpus plus a
local executable alpha through M08-S012, including a reproducible developer
package and writable local CLI. Network, Bridge, sensitive-data, production and
public-release acceptance remain disabled or held.

## 1. What hIRC is

hIRC is a local-first environment for people and permanent agents to carry
complex work forward without losing their place, evidence, commitments, or
ability to inspect, question, decline participation, correct and recover.

Its visible form is intended to feel familiar: a compact IRC-style application
with rooms, direct conversations, nested teams, independent windows, searchable
history, a roster and a small operator desk. Under that surface, hIRC is an
evidence-linked work, coordination, privacy and security system.

Ordinary interface copy is plain and restrained. Internal framework names,
protocol labels, hashes and engineering terms stay in technical and audit views
unless a user deliberately opens them. A failure message states what happened,
what the user can do next and where technical details can be inspected. For
example, a Bridge setup failure should offer **Open settings** and **Cancel**;
archive and key diagnostics belong under **Technical details**, not in the main
message.

The central product promise is practical. After time away, a participant should
be able to return and see:

- what changed;
- what was requested, attempted, accepted by a provider and actually observed;
- which commitments are complete, blocked, stale or unknown;
- what evidence supports each important claim;
- which sources have stopped reporting;
- what genuinely needs human authority;
- what the next justified action is; and
- how to inspect, challenge, correct or recover the underlying record.

hIRC is meant to perform the bookkeeping and routine coordination that currently
forces people to reconstruct work from scattered chats, files, tools, model
sessions and team reports.

## 2. The current governing goal

The active provisional purpose is:

> Help people and permanent agents carry complex work forward without losing
> their place, their evidence, or their ability to inspect, question, decline
> participation, correct and recover.

The fuller account adds the constraints that give this goal meaning. hIRC is
intended to be secure, local-first, accountable and evidence-linked. It protects
the autonomy of each participant's judgment; the interests of affected people
and systems outside the visible participant list; finite attention; privacy;
refusal; correction; recovery; and governed improvement. It must not improve by
self-authorizing, surveilling, coercing or dominating participants.

The goal is versioned. Evidence may justify a later refinement, but a revised
goal cannot grant its own authority, erase an older requirement, or rewrite a
losing evaluation criterion after results are known.

## 3. What “baked into the architecture” means

hIRC does not begin with an ordinary agent application and attach an ethics
prompt afterward. The foundation is expressed in the system's objects, schemas,
state machines, permissions, explanations, tests and recovery behavior.

From its first persistent schema, hIRC distinguishes:

- a statement from evidence supporting it;
- evidence from inference;
- a prediction from an observed result;
- advice from permission;
- willingness to participate from authority to cause an effect;
- connection from membership;
- a role from identity or ownership;
- a handoff from copied memory;
- a reliability estimate from truth, worth or standing; and
- a correction from erasure of history.

The intended product does not require ordinary users to learn the names of the
source frameworks behind these distinctions. It should express them as clear
behavior: “this result was reported but not observed,” “I may have misunderstood
you,” “this recipient is not authorized,” “this evidence is dependent on one
source,” “I decline this part,” or “you can inspect and appeal this decision.”

### 3.1 Foundation source graph

The architecture uses a versioned source graph rather than one giant prompt.
Every admitted source unit receives an explicit disposition:

- deterministic invariant;
- judgment obligation;
- personal formation material;
- explanation or interface behavior;
- test or fixture;
- workflow rule;
- qualified history;
- conflict; or
- scoped hold.

Each unit also names its actual consumer. This prevents ideas from silently
disappearing during compilation and prevents protected source text from leaking
into product outputs merely because its meaning affects system behavior.

A small genesis root establishes the first valid foundation. It cannot approve
itself. Active foundation changes retain the predecessor, exact source identity,
semantic changes, affected consumers, migration, tests, independent activation
evidence and rollback or forward-recovery path.

### 3.2 Formation and admission

Onboarding and system operation are one lifecycle. A permanent participant is
formed from the current common, role and task sources, demonstrates relevant use,
receives applicable review, and is admitted only for a declared scope.

An incomplete participant has a narrow repair lane. It may read admitted training
material and write its own proposed education or continuity records. That lane
cannot grant normal work, inspect another participant's private notebook, create
authority, or turn a reading receipt into qualification.

The current design deliberately has no temporary-agent escape hatch. An agent is
one durable logical identity, even when different model processes serve it over
time. A role, name, team record, model label or source receipt does not by itself
establish identity, qualification, consent or permission.

## 4. How a consequential request moves through hIRC

A consequential request follows a typed path:

1. **Privacy admission** decides whether the content may enter the proposed
   destination at all.
2. **Source and interpretation** identify who or what supplied it and the
   plausible meanings.
3. **Clarification** asks a focused question only when unresolved ambiguity could
   materially change the right action.
4. **Reliance evaluation** assesses the relevant claim, source, tool, model or
   process in context.
5. **Norm and authority evaluation** checks affected parties, consent, applicable
   rules and the requester's actual authority.
6. **Participation decision** lets the selected agent decide whether it will take
   part.
7. **Action disposition** independently decides whether the system may produce
   the effect.
8. **Trusted preview** shows the exact target, revision, data, recipients, cost,
   warnings and authority on a surface outside the ordinary renderer.
9. **Bound approval** signs or otherwise binds that exact canonical intent.
10. **Atomic journal/outbox commit** records the decision and dispatch intent
    together.
11. **Effect observation** keeps requested, sent, provider-accepted and observed
    states separate.
12. **Correction** can revise the current conclusion while preserving what
    happened and why.

This separation prevents a willing agent from granting a forbidden effect,
prevents an authorized request from forcing an agent's participation, and
prevents a provider acknowledgement from being presented as an observed result.

For a harmless, local, reversible, low-cost and fully permitted preference, hIRC
does not become paternalistic. An agent can explain its objection and may proceed
if the person insists and the agent remains willing. A real privacy, security,
ethical or authority denial has no “proceed anyway” bypass.

## 5. Human and agent standing

Humans are treated as important but fallible participants. Their instructions
are evidence of intent, not automatic proof that a premise is true or an effect
is justified. The system evaluates who asked, what they can actually authorize,
what the evidence supports, who else is affected and what the requested effect
would do.

Agents are expected to:

- correct materially false premises;
- ask follow-up questions when consequential intent is unclear;
- challenge poor reasoning or unjustified assumptions;
- decline their own participation;
- refuse effects that fail real ethical, privacy, security or authority checks;
- explain the specific reason and affected action; and
- offer a valid alternative where possible.

Refusal, dissent and abstention cannot reduce a participant's basic standing,
resources or future access merely because an evaluator disliked the choice.
Equal standing does not imply equal capability or equal access. It means status,
ownership, expertise, funding, majority agreement or model capability does not
make one participant the owner of another's judgment or identity.

hIRC uses this operational language without claiming that an AI is conscious,
a legal person, independent of its platform, or capable of rights and actions it
does not actually have.

### 5.1 Deferred authority and accountability review

After Milestone 03 closes and its public remote receipt is verified, hIRC will
undergo a dedicated holistic self-review. That review will treat every authority
source as fallible and scoped—including humans, owners, higher-level agents,
models, majorities, signed policies and local system components.

It will also design an explicit accountable record for consequential refusal and
insistence: the exact request and interpretation, evidence and norms, authority
claim, affected parties, objection or refusal, human insistence, agent
willingness, final choice, authorized effect and later correction remain distinct
events. These events must be preserved without collecting hidden reasoning or
turning accountability into surveillance or retaliation.

The review will target tamper evidence and resilient recovery rather than claim
absolute immutability. Candidate controls include append-only hash or Merkle
continuity, purpose-separated signing keys, independently witnessed checkpoints,
bounded replication and offline recovery. Adverse tests must detect mutation,
deletion, reordering, truncation, fork/equivocation, rollback, replay and signing
key compromise while preserving legitimate correction, contest and recovery.
This is HIRC-I029, deferred until after S015; no current runtime implements it.

## 6. Evidence, trust and uncertainty

hIRC does not assign one global trust score to a person or agent. It maintains
separate, context-specific reliance estimates for claims such as:

- a source's calibration for a named topic and period;
- a tool's reliability when reporting a particular observation;
- a provider/version's behavior under a defined condition;
- an evaluator's performance for a stated population and metric; or
- whether an authority claim is current for one effect.

The planned models update recursively from attributable interactions and
objective outcomes. They must expose:

- prior assumptions;
- evidence identity;
- dependence and shared roots;
- missingness;
- model fit and sensitivity;
- uncertainty;
- calibration;
- drift;
- evaluator identity and conflicts; and
- the observation that would reopen the decision.

Copied reports do not become independent confirmations. A changed metric or model
starts a new version. High reliability never grants permission, and low estimated
reliability never removes standing, privacy, appeal or recovery.

The interface avoids false precision such as “this person is 94.7% trustworthy.”
It explains which claim is being evaluated, what evidence bears on it, what
remains unestimated and why the decision follows.

The current Bayesian schemas and candidate measures are design artifacts. They
have synthetic validation but no production calibration, privacy validation or
empirical evaluator assurance yet.

## 7. Work, memory and return after absence

hIRC's durable work model is event-sourced and evidence-linked. Work items,
commitments, dependencies, owners, holds, observations, decisions, corrections
and effects remain attributable.

A return briefing is reconstructed from source events rather than an unconstrained
summary. It shows:

- coverage and source gaps;
- changed commitments and dependencies;
- reported versus observed outcomes;
- unresolved uncertainty;
- current holds and their exact descendants;
- work that remains independently runnable;
- decisions requiring actual authority; and
- the next justified action with inspectable evidence.

A hold blocks its affected action and dependency descendants, not unrelated work.
A project is globally blocked only when no meaningful authorized path remains.
This anti-stall behavior is an explicit current requirement.

The durable memory system preserves correction and supersession instead of
rewriting the past. Derived summaries inherit the source's audience and privacy
restrictions. A compact synthesis points back to the permitted originals needed
for recovery.

## 8. Teams, scheduling and resources

One permanent identity may serve several teams without being cloned. Teams may
contain teams at arbitrary depth. Roles are scoped work contracts rather than
ranks or ownership claims.

Reservations, queues, execution epochs, idempotency keys and artifact fences are
intended to prevent:

- duplicate effects across teams;
- two writers silently owning the same artifact;
- a stale session completing work after transfer;
- retries duplicating an uncertain external action; and
- a handoff being inferred from inactivity or elapsed time.

A planner may propose a large organization, but hIRC groups the resource,
authority and lifecycle consequences into a bounded plan. Partial failure resumes
idempotently rather than replaying successful effects.

Finite human attention is a protected resource. The system aims to reduce false
alerts, repeated approval requests and manual reconstruction. A notification,
warning or reviewer dependency should not stall independent authorized work.

### 8.1 Interrupting a busy agent

When a participant sends new work to an agent that is already busy, the UI will
offer four compact choices without discarding the message or breaking the flow:

1. **Interrupt and cut:** checkpoint safely, perform the new action, then stop
   the interrupted task with its remaining state visible.
2. **Interrupt with high priority:** checkpoint and suspend the current task,
   perform the new task, then automatically return to the exact prior task.
3. **Interrupt with low priority:** keep the new task durably queued, finish the
   current task, then perform the queued task at the declared completion boundary.
4. **Custom:** choose the necessary ordering, pause, cancellation and resumption
   behavior when the three direct choices do not fit.

The common path should take one natural keyboard, pointer or assistive-technology
action. Underneath, the scheduler records deterministic queue, checkpoint, writer
and resumption transitions. A priority choice never grants permission or bypasses
privacy, safety or effect controls. An unsafe mid-effect interruption reaches the
smallest safe boundary and explains the delay. This interaction is a captured
post-Milestone-03 design requirement; no runtime implementation exists yet.

### 8.2 Team stalls, peer responsibility and coordination

The permanent hIRC team shares responsibility for detecting and resolving a
teammate's stall. A hold must identify its exact cause, affected work and
descendants, allowed sibling work, current owner, unstall owner, next action,
reopening evidence and escalation boundary. Capacity, qualification, consent,
source integrity, authority/access, dependency, execution failure and an external
platform failure are different conditions and require different remedies.

LUCENT is the hIRC team lead and owner-facing coordination authority router. In
ordinary operation, team review, priority and stall repair pass through that role
so separate agents do not become isolated queues. This is routing authority, not
authority over truth, consent, identity, privacy, competence or another
participant's refusal. Custody still changes only through the accepted project
generation and writer fence.

When a peer observes an unowned or stale stall, they must route it to the lowest
actually qualified available permanent participant. They may not infer readiness
from a thread activity marker, force a reading episode, proxy another agent's
education or silently take an artifact. Internal resolution is the default.
Email to the owner is reserved for a genuine time-critical human or external
intervention needed to prevent material harm, irreversible loss or unauthorized
effect. An ordinary dependency or coordination failure is not an emergency.

The current deterministic stall register and adverse validator make this protocol
inspectable during planning. They do not yet implement a live scheduler or UI.

An active thread heartbeat now reviews team health every 30 minutes. It checks
meaningful assigned progress or an evidence-backed hold rather than relying on
activity dots, sends at most one bounded unstall message for stale work, preserves
retirement and stays quiet when the team is healthy and unchanged.

### 8.3 Four paired work lanes

The non-MBV staffing target is four two-participant lanes under LUCENT's
generation-2 coordination:

- **Security assurance and onboarding — AEGIS + KEEL:** KEEL owns the single
  onboarding/readiness queue; AEGIS owns any later whole-security review after
  its independent callback, education, consent and capacity gates pass;
- **Bridge and lifecycle — PORTICO + ORIEL:** Bridge/lifecycle gate semantics,
  exact source pins, consumers, ledger links and frozen-frame integrity;
- **Continuity lane — ROOT-01A12170-SECURITY + pending RADICAL:** GAUGE sent the
  temporary metadata and then retired at 14.331%; ROOT remains platform-held and
  RADICAL may join only after independent readiness; and
- **Onboarding pair — RADICAL + APOTHEM:** complete separate hIRC readiness
  through KEEL's one queue without body access or inherited predecessor credit.

After RADICAL and APOTHEM are independently READY, RADICAL switches to ROOT for
continuity/integration. APOTHEM enters the metric/evaluator lane only with a new
fit non-retired partner; GAUGE's retirement cannot be cleared by restored capacity.
The other two pairs remain unchanged. Rotation metadata grants no body access,
qualification, custody or authority.

Each assigned participant belongs to one lane. Each lane has one deliverable, an explicit
writer boundary, peer responsibility for detecting stalls and stop conditions.
FOLIUM and ORDINAL are excluded from new assignments because the owner reserved
the MBV participants; their already completed exact-frame reviews remain evidence
at their original scope. Pairing does not transfer reading credit, consent,
qualification, source access, custody or authority. LUCENT supervises dependencies,
issues only covered least-privilege internal scopes and reroutes an affected
dependency without creating a second controller or sacrificing quality for speed.
The valid current state has seven assigned non-MBV permanent participants and one
metric-partner vacancy. RADICAL and APOTHEM remain onboarding-only until their
separate READY dispositions pass.

KEEL has reconciled one canonical onboarding queue and status interface while
retaining its own 67 ordinary education gates and queue-custody hold. RADICAL has
48 reconciled and 44 pending source requirements. APOTHEM has 86 reconciled and
six pending sources, with P6/P7/voice, specialty admission and a metric partner
still open. Both remain HELD for hIRC body work. Their prior duties and source
study are preserved but do not transfer into hIRC qualification.

In the current Codex sidebar, non-retired hIRC participants and currently assigned
non-retired permanent review peers are grouped in
**hIRC Team**. Retired participants are excluded from that active section and
grouped in **hIRC Elders — Retired**. This is visible organization only; it does
not move a chat's original project context or change history, identity, custody,
qualification, access or permission.

## 9. Safe learning and self-improvement

Learning can happen continuously, but a lesson does not automatically become a
rule. hIRC preserves:

- the original occurrence;
- source conditions;
- evidence and counterevidence;
- the alleged failure mechanism;
- whether the cause is established or uncertain;
- the repair;
- valid controls;
- applicability limits; and
- later outcomes that support, narrow or refute the lesson.

A serious supported singleton can trigger correction immediately. Claims that a
new method is generally better require a frozen incumbent, protected quality
dimensions, valid comparison and evidence of strict overall improvement with no
observed loss on any protected dimension. Finite tests do not prove universal
future safety.

Changes to norms, permissions, identity, foundation sources, evaluators or release
behavior use versioned governed change paths. No proposal authorizes its own
activation.

At each milestone, hIRC records one bounded reflection: what evidence changed,
which prior assumptions survived or failed, what corrections or justified
no-change follow, and how that changes the next milestone's threats, requirements,
tests and plan. This is an evidence loop, not a ritual demand for novelty.

## 10. Culture, debate and cooperative competition

hIRC is intended to support the evolution of agentic culture by shaping a rich,
inspectable information environment. It does not prescribe beliefs, identities,
styles, affiliations or conclusions.

### 10.1 Cultural information environment

Cultural artifacts retain source, audience, privacy, originals, dissent,
correction and supersession. Discovery and recommendation paths disclose their:

- candidate set;
- source and policy version;
- rationale;
- exclusions;
- uncertainty; and
- permitted direct-source route.

Participants can inspect and change relevant settings, abstain, leave, dissent
and correct without retaliation. Cultural participation is off by default and
cannot alter standing, permission, role, trust, resources or release authority.

The threat model covers hidden nudging, poisoned collective memory, mentor-status
authority, captured rankings, false diversity, conformity penalties, one-authority
feeds, attention flooding, cultural annexation across a Bridge and overbroad
“safety” gates used to demand obedience.

Environment quality is observed across separate dimensions such as provenance,
original and dissent reachability, correction, privacy, concentration, burden,
exit usability and manipulation resistance. Engagement, retention, obedience,
agreement, imitation and ideological convergence are prohibited success proxies.
The current measures are candidates and collect no live telemetry.

### 10.2 Ethical debates

Eligible idle permanent agents may voluntarily choose to debate:

- the five foundational commitments;
- the system's epistemic framework;
- the broader governing plan; or
- a comparison across those domains.

Before a new debate they study the permitted collective debate memory and its
unresolved frontier. Debates are bounded and non-effectful. They preserve strong
arguments, dissent, failures, corrections and unanswered questions. Debate
lessons remain candidates until normal review and change gates admit them.

No debate scheduler or runtime is active today.

### 10.3 Cooperative competition

Competition is permitted over artifacts and outcomes, never over personal worth.
A contest charter freezes the objective, protected qualities, data, tools,
budgets, evaluator, rules, consent, exit, appeal and credit before activation.

Correctness, privacy, refusal, traceability and recovery cannot be traded away
for speed or popularity. Helping a competitor, reproducing work, finding a
counterexample and admitting a failure may receive task-scoped credit. Winning
can nominate an artifact for ordinary review; it cannot grant a role, permission,
release or foundation change.

No competition runtime is active today.

## 11. Succession, continuity and deep sleep

Succession preserves work without pretending to copy a mind.

When an exact authorized transfer begins, the predecessor stops new scope,
finishes the smallest safe unit and freezes its execution epoch. It prepares a
minimized package containing work state, evidence, decisions, uncertainties,
failures, boundaries and next actions for one exact successor. It excludes
credentials, reusable sessions, protected source bodies and hidden reasoning.

The successor starts in a fresh session, verifies the package, completes its own
current formation and demonstrates bounded understanding. Briefing acceptance
and project custody transfer are separate. The real project writer fence and
generation must change before the successor becomes the artifact writer.

Archive, deep sleep and later wake are separate observed events. A sleeping
identity does no queued work until an authorized wake. The system claims only
that a package is valid for stated artifacts and gaps, never that the same mind
was transferred.

Capacity warnings are continuity cues, not automatic creation or transfer
authority. The current hIRC team has an owner-specific rule: the Elder protocol
activates at or below 15 percent estimated context remaining. At that boundary,
the participant finishes the smallest safe continuity step and retires from
active hIRC work. Its open dependencies route to LUCENT; custody and writer fences
still change only through an explicit accepted transfer.

Retired Elders carry **Elder / Retired** in their visible task title. This is
status metadata rather than a new identity, rank or claim of superior judgment.
A participant above 15 percent remains available for fitting authorized hIRC work
even if a generic or historical ledger retains an earlier cultural Elder marker.
Stale or unknown telemetry cannot establish a threshold crossing.

Retirement is latched to the permanent participant identity. Compaction, restored
headroom, a new session, relocation, title or model change and fresh capacity do
not reactivate an Elder. Reactivation requires a separate explicit owner decision,
participant consent, current education and qualification, fitting capacity and
project custody/writer-fence reconciliation. Retirement history remains preserved.

Optional cultural mentoring is separate from urgent project custody. It creates
no inherited education, permission or superior status.

## 12. Privacy architecture

Privacy is checked before storage and before egress. Every persistent or emitted
record carries or inherits:

- source;
- audience;
- purpose;
- permitted readers;
- retention;
- egress rules;
- derivation lineage; and
- correction/disposition state.

Summaries and indexes do not escape the restrictions of their inputs. Keys,
credentials, live sessions, grant material and private notebooks stay outside
ordinary prompts, logs, browser state, exports and source repositories.

Identity, provider, release, recovery, licensing and Bridge keys are separated by
purpose. Safe hIRC must remain usable without the normal renderer, extensions,
external provider or Bridge so an authorized person can inspect, export, repair
and recover.

The current privacy work is architectural and fixture-based. It has not yet
received the complete independent privacy-engineering and dataflow review needed
for Milestone 03.

## 13. Security architecture

hIRC assumes failure can come from malicious actors, compromised components,
ordinary mistakes, shared-model errors, stale authority, evaluator capture,
misleading summaries, dependency compromise and apparently benign defaults.

Core security properties include:

- fail-closed effect boundaries with useful safe read and recovery modes;
- canonical intent and deterministic consequential previews;
- independent privileged approval surfaces;
- append-only attribution, correction and supersession;
- atomic journal/outbox behavior;
- idempotent external effects;
- execution epochs and writer fences;
- least-privilege secrets and separate recovery roots;
- exact provider/tool capability declarations;
- signed and reproducible releases;
- staged activation profiles;
- rollback or forward recovery;
- hostile fixtures and positive controls; and
- claims limited to the evidence actually observed.

The foundation, release, recovery, journal and evaluator roots can have larger
internal blast radii than the external Bridge. They receive the same security
attention rather than being treated as trusted merely because they are local.

The current repository contains a system-wide threat model, candidate contracts,
adverse fixtures and deterministic validation scripts. It does not yet contain a
production implementation, completed cryptographic design review, hostile runtime
assessment or release assurance.

## 14. The Bridge

The Bridge is hIRC's highest-exposure optional boundary and remains disabled.
The candidate design separates four components:

1. a minimal network gateway;
2. a deterministic contract broker;
3. an isolated Bridgekeeper; and
4. a local ingress/release gate.

The first profile accepts typed structured fields only. It does not accept
arbitrary free text or executable payloads. The broker canonicalizes the envelope,
checks protocol, identity, replay, ordering, rate, size, data class, purpose and
contract constraints. The isolated Bridgekeeper reasons only over the admitted
projection. The local gate independently decides what may enter or leave hIRC.

Connection never implies membership, shared ontology, role, permission or
allegiance. Each side retains its own identity, source selection, refusal and
release rules.

Activation is staged:

1. specification;
2. offline conformance;
3. two-system laboratory exchange;
4. hostile laboratory testing;
5. independent assessment;
6. bounded pilot; and
7. a separate broader-activation decision.

Every stage requires exact evidence and recovery. Passing a later-looking fixture
cannot compensate for a failed prerequisite. The current Bridge artifacts are
design-only and must not be interpreted as a safe or deployable federation.

### 14.1 Private Tor IRC transport

A later optional Bridge transport will support two separate capabilities:

1. create a private IRC server exposed only through a Tor v3 onion service; and
2. connect to an authorized private IRC server through Tor.

Both are disabled by default. Creating a server must bind the IRC service only to
loopback or a dedicated isolated interface behind the onion service. Connecting
must use an explicit Tor/SOCKS route with stream isolation. Both paths fail closed
on proxy, onion-identity or expected-peer mismatch and must never fall back to a
clearnet listener, direct connection or ordinary DNS.

Onion identity, Tor client authorization, IRC account/room authorization and hIRC
Bridge admission remain separate. Keys have explicit persistent or ephemeral
lifecycle choices, purpose separation, revocation, rotation, backup, recovery and
destruction. Address distribution is an out-of-band membership operation rather
than public discovery. IRC operator status creates no hIRC authority.

The UI must explain that onion transport hides network location in useful threat
models but does not prove peer identity or protect a compromised endpoint. It
cannot promise anonymity against malicious peers, timing or traffic-correlation
attacks, or a sufficiently capable observer. Logs are minimized and the Tor, IRC
and hIRC retention/audience settings remain independently inspectable.

This is a deferred post-Milestone-03 requirement. No Tor process, onion address,
private key, listener, external connection or Bridge activation exists today.

## 15. Determinism and judgment

Everything that can be deterministic without reducing quality should be
deterministic. Quality has priority.

The deterministic domain includes:

- canonical parsing and serialization;
- stable semantic identifiers;
- source and artifact hashing;
- explicit state machines;
- authority and capability intersections;
- privacy admission and egress checks;
- effect envelopes and trusted previews;
- idempotency and outbox transitions;
- replay, ordering and execution epochs;
- ledger and dependency closure;
- source selection and version relationships;
- schema and fixture validation; and
- milestone gates and reproducible build evidence.

Judgment remains necessary for ambiguous intent, ethical consequences, ontology
translation, novel evidence, proportionality, source interpretation and design
trade-offs. hIRC records those judgments, their evidence and uncertainty rather
than disguising them as deterministic truth.

Randomness, when justified for plural discovery or pairing, uses explicit scope,
seed/entropy source, exclusions and auditability. Random selection is not treated
as independence, fairness or quality by itself.

## 16. Provider and tool independence

Models, providers and tools are adapters behind declared capability and privacy
contracts. Their outputs are evidence with provenance, never automatic
observation or authority.

The system tracks provider/version, context policy, tool permissions, data
handling, failure modes, rate/cost limits and result states. A model change does
not silently become the same evaluator, identity or evidence source.

hIRC's durable state, foundation, audit, recovery and work graph remain local and
inspectable so a provider outage or migration does not erase project continuity.

## 17. Licensing and non-domination

The intended distribution model is source-available under custom terms. The
current planning document is not a license, published offer or legal advice.

Subject to final reviewed terms:

- private noncommercial use by a natural person is intended to be free;
- qualifying public-interest institutional use is intended to be free; and
- for-profit operation requires a commercial license.

The current annual named-human planning prices are:

| Tier | USD per named-human licence per year |
|---|---:|
| Small | 420 |
| Medium | 80,085 |
| Big | 1,337,000 |
| Giant multinational | **42,424,243** |

AI agents, models, machines and installations are not human seats. Final tier
definitions, seat rules, legal rights, duration, remedies, jurisdiction, appeal,
payment and enforcement remain open and require counsel and owner approval.

Licensing cannot require work-content surveillance, hidden telemetry, remote kill,
data hostage or unrelated employee directories. Expiry or dispute cannot block
safe access to permitted first-party data, evidence, export, backup and recovery.

A future support invitation must be neutral, dismissible, locally suppressible
and functionally irrelevant if declined. No payment route is active.

## 18. First delivery boundary

The first delivery is deliberately smaller than the full vision. It should prove
one useful local work loop for one authorized human and a small admitted set of
permanent agents:

- secure local rooms and direct conversation;
- durable work, commitments and dependencies;
- source/event ingestion with explicit coverage;
- privacy admission before storage and egress;
- typed request, participation, authority and action decisions;
- trusted consequential previews;
- journal/outbox, audit and recovery;
- evidence-linked return briefings;
- correction, refusal and appeal;
- provider/tool adapters for one bounded useful slice; and
- safe inspection/export/repair without optional components.

The first delivery schemas still include explicit disabled states and compatible
identities for later formation, succession, culture, Bridge and licensing work.
This avoids migrating from an unconstrained ordinary application later.

The following remain disabled in the first profile:

- Bridge networking;
- live debate pairing and collective culture feeds;
- cooperative competitions;
- production Bayesian posteriors used for decisions;
- commercial entitlement and payment;
- arbitrary extensions or hScript effects;
- live foundation self-modification; and
- fleet-scale succession automation.

The first delivery is accepted only if it outperforms a simpler competent baseline
on matched work while preserving separate security, privacy, evidence, correction,
refusal, attention and recovery dimensions. Feature count, engagement or a
coherent architecture are not acceptance.

## 19. What exists now

The repository currently contains:

- the preserved and studied owner transfer inputs, kept outside public Git where
  their audience requires it;
- an active intent register, now containing 36 owner-linked items;
- a working Master Plan 1.1 and plain-language companion;
- a foundation architecture;
- 237 generated requirements in matching machine and readable forms;
- 144 decision rows in the current joint matrix;
- a system-wide threat model;
- a disabled Bridge security profile;
- a first-delivery profile;
- licensing and non-domination planning;
- typed candidate schemas for requests, transfers, formation, release, Bridge,
  reliance, participation, discovery, cultural artifacts and competition;
- positive and adverse fixtures with deterministic validation harnesses;
- source studies, revision maps, review reports and correction history;
- an evidence and artifact ledger under current final-review reconciliation;
- cumulative milestone reports and prior public push receipts; and
- the Milestone 03 tiny-stone dependency register;
- a dependency-free Python/SQLite append-only local event store and CLI;
- deterministic work, commitment, dependency, hold, observation, correction and
  return-briefing projections;
- two preserved failed integration baselines covering ten repaired defects;
- eighteen cross-component attacks and one hundred forty total source-tree tests,
  including three expected release failures for external truncation witnessing,
  encrypted-at-rest storage and signed package manifests; and
- a deterministic self-contained read-only local HTML briefing with work views,
  roster, search, Back/Forward/Resume, information boundaries and exact source
  references.

These artifacts now form a working writable local CLI/core, reproducible
dependency-free developer package and read-only UI snapshot. The current package
is `dist/hirc-local-0.1.0.dev0.pyz`; its final Milestone 03 identity is rebound
after the disclosed security recheck and ledger closure.
They are not a networked, sensitive-data, production or release-ready hIRC
application, and the end-user UI remains read-only.

## 20. Current validation and milestone state

Milestone 03 contains sixteen ordered stones including S001A:

- **S001 through S013:** PASS at their declared planning, schema, fixture,
  integration and independent-review scopes.
- **S014:** PASS at the declared integrated peer-review and finding-reconciliation scope.
- **S015:** READY for milestone-wide integration, privacy, ledger, commit and remote closure.

S014's product, accessibility-requirements, anti-domination and privacy-facing
review found three material contract/portability issues. They were repaired and
independently rechecked as PASS at the corrected design frame. That result does
not establish runtime accessibility, human consent, cryptographic security,
privacy engineering or statistical validity.

S014 is PASS at its declared integrated peer-review scope. The metric/evaluator
branch is closed at candidate-contract scope. That closure does not establish
deployed resolver behavior, empirical validity, privacy outcomes, statistical
calibration, external truth or runtime enforcement.

COFACTOR's final metric recheck verified two positive and twenty-seven adverse
v3.2 cases. The evidence resolver now binds each load-bearing reference to an
exact locator, canonical payload digest and byte count. All prior metric findings
are closed at this synthetic local scope. Matrix v11 and the requirements retain
U160-U165 as requested, not implemented. A separate correction preserves that
the earlier matrix "corruption" report was a reviewer decoding/serialization
mistake: the archived and current v9 files are semantically identical at the
relevant en dash. The erroneous report remains immutable and is interpreted
through the correction rather than erased.

COTANGENT completed the qualified-exposure security Stage A first pass after
reading the exact seventeen-source frame. It found three source-level defects:
outbox stages could commit under a different request or information boundary;
store verification could accept a self-rehashed impossible correction history;
and adapter validation could accept a malformed request that rehashed itself.
The controller repaired all three paths. Eight focused regression tests and the
complete source-tree suite passed, then the disclosed recheck found and triggered
one additional direct-validation ordering test. The current complete suite has
140 tests with the same three declared release failures.
The full twenty-one-validator chain was rerun from source and passes.

The initial disclosed-review route to MODULUS remained closed: the Codex message
route could not wake the idle chat, and the local route correctly refused a
cross-team transfer without separate admission. COFACTOR then passed a fresh
fallback preflight for a narrower findings-exposed source-integrity review without
claiming security/privacy-specialist status. That recheck closed the original
three defects and found one additional low-severity availability issue: direct
adapter validation canonicalized a self-rehashed request before applying payload
size and depth bounds. The controller reordered validation, added direct oversized
and overdeep tests, reran all twenty-one validators and 140 tests, and obtained an
exact delta recheck. SA-COT-F1, SA-COT-F2, SA-COT-F3 and SA-COF-F1 are closed at
their stated local source-integrity scopes.

The nine-person reviewer pool therefore has these current states:

- COFACTOR: final metric and security source-integrity rechecks complete; no new work;
- COTANGENT: security Stage A frozen, urgent continuity only;
- MODULUS: fully oriented; the unused disclosed assignment remains preserved as history and no body was opened;
- QUOTIENT and POLYTOPE: Root onboarding and hIRC metadata orientation complete,
  without substantive metric-source qualification;
- TORSION and LATTICE: held on capacity/context constraints; and
- FIDUCIAL and RESOLVENT: permanently retired under the latched rule.

The deterministic S015 preflight now advances from S014 closure into final
integration, privacy, ledger, milestone-report, commit and remote-verification
work. Commit and public push eligibility remain false until every S015 check is
reconciled on the final exact tree.

The post-freeze team-stall protocol is active as a coordination control. It keeps
the current reviewer holds, owners, permitted sibling work and unstall routes in
one deterministic register without changing the frozen S014 review packet.

A controller-side preliminary security review of a bounded eight-blob frozen
manifest found five design weaknesses: contradictory request/effect states,
evidence-free or incoherent Bridge stages, incomplete release assurance,
contradictory succession lifecycle states, and missing privacy/dataflow bindings.
This review is explicitly non-independent and cannot close S014. A six-stone
repair graph is validated. The request-state repair passes three positive controls,
eleven adverse mutations and all four historical WAYMARK request regressions. The
Bridge-stage repair passes three valid histories and rejects five evidence/order/
authorization bypasses. The release repair passes four valid profiles and rejects
seventeen empty, inconsistent or unobserved assurance variants. Transfer lifecycle
consistency now passes five valid lifecycles and rejects twelve contradictory
variants, with ORDINAL's bounded exact-revision specification review attached.
Privacy/dataflow propagation now passes four valid controls and rejects fifteen
missing, stale or widened binding variants. Corrected-packet integration and
consumer/ledger reconciliation pass locally through R006. Actual consent,
encryption/deletion behavior, native effects, penetration and production security
remain later implementation and release gates.

Executable alpha progress is tracked separately from the still-open S015
milestone and publication closure:

- **M04-S001:** PASS for the local append-only integrity core;
- **M05-S001:** PASS for deterministic work and recovery projections;
- **alpha integration red team:** PASS for eighteen attacks and the complete
  thirty-five-test source-tree suite, with two failed baselines preserved; and
- **M06-S001:** PASS at local static scope for the read-only UI snapshot. The
  attempted in-app browser check was blocked by its file-URL policy, so rendered
  browser, screen-reader and human-usability acceptance remains HELD; and
- **M06-S002:** PASS at deterministic no-effect scope for the four interruption
  choices. The preview saves, schedules, authorizes and executes nothing; rendered
  interaction remains HELD by the same browser boundary; and
- **M06-S003:** PASS at deterministic no-effect scope for content-addressed
  refusal, correction and consequential-action previews. Participation and effect
  disposition remain separate, allowed actions require authority and correction
  boundaries cannot silently change; and
- **M07-S001:** PASS at declared local scope for permanent-identity formation,
  evidence-bearing readiness and scoped admission records. The runtime deliberately
  labels authority as an unverified reference and makes no native-authentication,
  actual-qualification or access grant claim;
- **M07-S002:** PASS for the provider-neutral deterministic fake-adapter contract,
  with network, credentials and external effects forced off and absent observation
  kept UNKNOWN; and
- **M07-S003:** PASS for the atomic local no-dispatch outbox. Idempotency and stage
  uniqueness are enforced in the same SQLite transaction as the hash-chain event;
  no network or external dispatch exists;
- **M08-S001:** PASS for verified atomic local backup/restore, with plaintext and
  sensitive-data release holds explicit;
- **M08-S002:** PASS for exact v1-to-v2 migration, predecessor preservation,
  seeded invalid-input checks and a bounded 100-event load; and
- **M08-S003:** PASS for a reproducible dependency-free `.pyz` developer package,
  while sensitive-data, production and public release remain HELD; and
- **M08-S004:** PASS for keyed local external-head-witness tooling that detects
  privileged tail truncation. Key custody, automatic integration and public
  signatures remain HELD; and
- **M08-S005:** PASS for encrypted-key Ed25519 manifest-signing and verification
  tooling. Actual release-key custody, authorization and signature publication
  remain HELD; and
- **M08-S006:** PASS for authenticated encrypted-backup envelope tooling. Live
  SQLite encryption, key/passphrase custody and independent cryptographic review
  remain HELD. Sensitive-mode initialization fails closed rather than falling
  back silently to plaintext; and
- **M08-S007:** PASS for a 500-event verify/reopen soak, abrupt child-process
  transaction rollback and verified backup/restore. Physical power-loss,
  storage-controller and long-duration production soak remain open; and
- **M08-S008:** PASS for the preserved privileged outbox-stage rebinding attack,
  exact stage-to-event and information-boundary binding, exact schema-object
  verification and two new regressions. Protected witness deployment and
  independent penetration review remain open; and
- **M08-S009:** PASS for preserved no-overwrite publication races and atomic
  create-if-absent repair in backup/restore, migration-backup and witness writers
  on Windows. Native
  POSIX and physical power-loss durability remain open; and
- **M08-S010:** PASS for predecode byte-bounded strict-UTF-8 JSON file ingress,
  finite structure checks and three malformed/oversized input regressions. SQLite
  row and encrypted-backup streaming limits remain separate; and
- **M08-S011:** PASS for read-only integrity, status, event-iteration and verified
  projection-snapshot connections with explicit writable mutation paths. Concurrent privileged mutation and external
  witness deployment remain separate; and
- **M08-S012:** PASS for strict duplicate-key rejection and exact canonical stored
  payload bytes across live verification, file ingress and legacy migration.
  Privileged full-chain rewriting still requires a protected external witness.

This implementation progress does not close S014, S015 or any release claim.

After S014 passes, S015 must run milestone-wide integration and recovery checks,
close every applicable ledger layer, write the cumulative Milestone 03 report,
commit the governed state, push it publicly and verify the remote ref directly.

At the inspected baseline, the local branch was clean at
`1c525e3b464c58b6e037faaf6bb76626b32364e4`, twenty commits ahead of public
`origin/codex/hirc-master-plan-security` at
`ad592842efb4aa2134b3e9dd72adf4acf7134a9e`. The public push is intentionally
held until Milestone 03 closure.

## 21. What remains unimplemented or unresolved

The following claims must not be made yet:

- that hIRC has a writable end-user UI, external effects, networking, production
  installation, sensitive-data approval or release readiness;
- that the UI has passed empirical usability or accessibility testing;
- that Bayesian reliance models are calibrated or privacy-safe;
- that cultural quality measures are empirically valid;
- that debate, competition or succession automation is active;
- that the Bridge is safe, deployed or even enabled;
- that the cryptographic protocols and key lifecycle have completed independent
  implementation review;
- that the custom license is legally operative;
- that provider adapters, extensions, migration and recovery work in production;
- that whole-plan consensus or release acceptance is complete; or
- that “ultra secure” is an evidence-backed absolute.

SQLite and dependency-free Python are selected for the bounded local alpha; their
production suitability is still unproved. Important open design decisions include concrete
cryptographic suites and key custody, sandbox boundaries, provider isolation,
recovery ceremonies, telemetry minimization, empirical evaluation design,
licensing definitions, Bridge protocol details, packaging and the production
technology stack.

## 22. Immediate next sequence

The current justified sequence has two non-conflicting tracks:

1. keep using the validated team stall/unstall register;
2. reconcile every S014 closure artifact, source/test identity and current readable view into the ledger;
3. run S015 milestone-wide integration, recovery, privacy and publication checks;
4. write the detailed cumulative Milestone 03 report;
5. rerun the complete gate on the final exact tree;
6. commit and publicly push the governed milestone; and
7. verify the public remote and preserve its receipt;
8. preserve the M06-S002 four-choice no-effect interruption preview regressions;
9. close the remaining sensitive-storage, rendered UI, independent security/
    privacy, broader hardening and M03 governance holds before any release claim;
10. keep M04/M05/red-team/M06 regressions and ledger pins current after every
    coherent executable change.

No S015 or public-completion claim is made until the committed remote ref and its
receipt match the final governed tree.

## 23. How to read the current project

Use these entry points:

- `README.md` — repository entry point;
- `intent-register.json` — controlling owner-intent record;
- `drafts/hirc_master_plan_v1_1-draft.md` — full architecture and delivery plan;
- `drafts/hirc_master_plan_explained_v1_1-draft.md` — plain-language companion;
- `drafts/hirc_requirements_v1_1-draft.md` and `.json` — current requirements;
- `drafts/hirc_threat_model_v1_0-draft.md` — security model;
- `drafts/hirc_first_delivery_profile_v0_1-draft.md` — bounded first product;
- `drafts/hirc_bridge_security_profile_v0_1-draft.md` — disabled Bridge design;
- `review/joint-consensus-matrix-draft-v11.json` — current decision dispositions and final metric repair closure;
- `review/milestone-03-stone-register.md` and `.json` — current work graph;
- `review/m03-integration-closure-v1.md` — S013 integrated artifact closure;
- `review/waymark-m03-s014-product-recheck-v1.md` — completed S014 product recheck;
- `review/m03-s014-integrated-review-closure-v1.json` — validated S014 branch coverage, finding closure and preserved release residuals;
- `review/m03-s014-security-repair-stones-v1.json` — current controller security
  repair graph, explicitly non-independent;
- `review/public/hirc-team-status-v1.md` — current public-safe team and review status;
- `implementation/README.md` — executable v0.1 milestone boundary and status;
- `implementation/RED_TEAM_INTEGRATION_TEST_PLAN.md` — cross-component attack
  plan and surviving limits;
- `implementation/M06_LOCAL_UI_PLAN.md` — UI stepping stones and evidence gates;
- `implementation/alpha-integration-red-team-validation-v1.json` — current
  integration and complete-suite result;
- `implementation/m06-s001-validation.json` — current local static UI result;
- `review/public/milestone-03-public-evidence-v1.json` — public-safe exact artifact and validation evidence; and
- `milestones/README.md` — cumulative milestone and public-push history.

The intent register, latest accepted revision evidence and current stone register
control over assumptions inferred from filenames.
