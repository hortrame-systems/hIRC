# hIRC requirements 1.1 — working draft

**Status:** draft pending whole-packet peer consensus

**Requirements:** 237 (151 preserved predecessor; 86 new/corrective)

**Revision decisions:** 144 pending final disposition

This view is generated from the preserved 1.0 requirements and the current revision-map candidates. The JSON file is the machine-readable draft. A captured requirement is not implementation or verification.

## Explicit corrections and holds

- U064 is superseded by the current permanent-only actor policy; no temporary-agent route remains.
- U119 is preserved as historical source wording and succeeded by the foundation-native whole-onboarding requirements.
- U125/U150-C1 use USD 42,424,243 per named-human licence per year as the planning unit; final legal duration, tiers and commercial activation remain held.
- U186-U191 are quality-first determinism requirements captured for design and testing; they are not implementation evidence.
- Every security/privacy impact, dependency and executable acceptance-test link still requires final peer reconciliation.

## Agent

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U059 | PARTIAL | P3 | Team coordinator can spawn agents inside its team | Grant-bound permanent provisioning is observed |
| U060 | REQUESTED_NOT_IMPLEMENTED | P3 | Single planner can build recursive team organizations | OrganizationPlan executes idempotently through many levels |
| U061 | PARTIAL | P3 | One planner can spawn needed agents for nested plan | Budget-bound child agents persist as identities |
| U062 | REQUESTED_NOT_IMPLEMENTED | P3 | Every normal spawned agent is permanent | Identity survives runtime shutdown and provider migration |
| U063 | REQUESTED_NOT_IMPLEMENTED | P3 | Subagents banned by default | Execution broker rejects ephemeral subagent calls |
| U064 | SUPERSEDED | P3 | Advanced deliberate global subagent unban option | Explicit operator unlock with separate scoped agent grants |
| U065 | PARTIAL | P3 | Spawn inherits parent's model by default | Actual newly provisioned profile derives model correctly |
| U066 | PARTIAL | P3 | Spawn inherits parent's thinking level by default | Supported reasoning setting resolved and recorded |
| U067 | PARTIAL | P3 | Operator may override spawn default | Scoped overrides apply without altering other teams |
| U068 | PARTIAL | P3 | Coordinator can be instructed to change spawn default | Authorized command produces versioned team setting |
| U069 | PARTIAL | P3 | Agents can spawn agents without every routine operator click | Bounded preauthorized plan executes without new approval |
| U070 | PARTIAL | P3 | Coordinator has room privileges but not universal powers | Role badge cannot mint backend capabilities |

## Appearance

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U011 | STATIC_PRESENT | P0 | Application name is hIRC | Consistent name across title executable docs and archives |
| U012 | STATIC_PRESENT | P0 | Early 2000s mIRC Windows classic appearance | Visual comparison and keyboard interactions reviewed |
| U013 | STATIC_PRESENT | P0 | Unpolished flat/beveled compact chrome | Theme renders expected controls across DPI settings |
| U014 | PARTIAL | P0 | Fixedsys-style classic mIRC chat font | Font chosen when installed with documented fallback |
| U015 | PARTIAL | P0 | Pixel hIRC wordmark and robot Pac-Man mascot | Portable bundled asset matches approved direction |
| U016 | SIMULATION_TESTED | P0 | Classic normal color theme | Default window uses classic palette |
| U017 | SIMULATION_TESTED | P0 | Dark hax0r neon color theme | Theme selectable and readable |
| U018 | SIMULATION_TESTED | P0 | Other built-in themes and custom palettes | Custom style persists and round trips |
| U019 | SIMULATION_TESTED | P0 | Apply color theme independently per window | Changing one window does not change another |
| U020 | PARTIAL | P5 | Configurable per-window fonts and spacing | Settings persist and remain accessible |

## Attention

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| D012 | PROPOSED | P2 | Introduce operator-attention admission governor | Threshold triggers delegation/pausing not only muting |
| D013 | PROPOSED | P2 | Measure time-to-resume against a simpler baseline | Precommitted benchmark shows behavior and errors |
| D014 | PARTIAL | P2 | Require context bookmark with task intent | Crash restored prior task and draft |
| D015 | PROPOSED | P2 | Provide one-screen explanation with evidence drilldown | Rationale and unknowns inspectable from one place |

## Authority

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U162 | REQUESTED_NOT_IMPLEMENTED | P0 | Never accept authority blindly | Every consequential authority claim verifies authenticated principal, delegation source, exact scope/target/data/time/purpose, expiry/revocation/conflict, consent and action legitimacy; reliability neither grants nor substitutes authority |
| U200 | REQUESTED_NOT_IMPLEMENTED | ALL | Prohibit cultural status and coherence from affecting standing or authority | Participation, popularity, style, agreement, victory, mentor status and coherence have no direct trust, role, permission, resource, release, Bridge or intrinsic-worth effect |

## Authority and action

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U152 | REQUESTED_NOT_IMPLEMENTED | P0 | Keep reliance, participation and action disposition independent | Human insistence and agent willingness cannot bypass evidence/norm/authority/effect gates; individual refusal cannot rule others or substitute identity; every outcome retains scoped reasons and correction paths |

## Boot and recovery

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U141 | REQUESTED_NOT_IMPLEMENTED | P0 | Initialize the first valid foundation and permanent technical identity without circular self-authorization | A minimized predecessor-controlled GenesisRoot verifies an owner-authorized digest-bound source/compiler/test/recovery manifest in a non-effectful environment, atomically activates or fails to safe inspection/repair, and cannot be reused for ordinary self-promotion |

## Bridge

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U204 | REQUESTED_NOT_IMPLEMENTED | P6 | Preserve local cultural sovereignty and translation limits across Bridge exchange | Bridge exchange remains disabled until its gates; later translation records loss and non-equivalence and grants no membership, allegiance, identity, authority, content inheritance or export permission |

## Bridge release

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U176 | REQUESTED_NOT_IMPLEMENTED | P6 | Use noncircular staged Bridge pilot and broader-activation prerequisites | Exact applicable stages 1–5 plus explicit limited stage-6 entry authorization permit pilot start; missing stage 5 blocks it; pilot evidence cannot authorize stage 7 without a separate broader decision |

## Chat

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U049 | SIMULATION_TESTED | P0 | Private chat hides agent's other traffic by default | Only direct messages appear with overlay disabled |
| U050 | SIMULATION_TESTED | P0 | Authorized other agent traffic can be toggled on | Chronological merged view contains only authorized records |
| U051 | PARTIAL | P2 | Merged traffic labeled with source room and time | Display reflects causal uncertainty and provenance |
| U052 | PARTIAL | P1 | Preserve every permitted direct/team/composite chat log | Replay source admitted room records after restore |
| U053 | PARTIAL | P1 | Preserve archives for all permitted rooms | Restore tested archived room histories |

## Collective learning

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U134 | REQUESTED_NOT_IMPLEMENTED | P3-D | A default setting permits eligible non-busy permanent agents to pair randomly for bounded ethical debates | Atomic auditable pairing uses true availability, consent, privacy compatibility, fairness, budgets, opt-out/decline, crash recovery and no work preemption or temporary actors |
| U135 | REQUESTED_NOT_IMPLEMENTED | P3-D | Paired agents can choose to debate the five commitments, Epistemethics or the Grand Plan | Both participants select/accept a supported DebateDomain; no forced domain or fabricated agreement; exact current domain sources and admission govern readiness |
| U137 | REQUESTED_NOT_IMPLEMENTED | P3-D | Debates become increasingly complex from the surviving ethical frontier | Each topic names prerequisites and justified complexity dimensions; progression comes from surviving questions/evidence and can branch or regress after counterexamples; verbosity, conflict and token count do not count as complexity |

## Collective memory

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U136 | REQUESTED_NOT_IMPLEMENTED | P2-D | The collective debate memory is studied before every new debate | First participation completes whole accessible domain-memory study; later debates reuse a valid checkpoint only with complete immutable delta closure; gaps remain explicit and summary/hash/self-report cannot substitute for coverage |
| U138 | REQUESTED_NOT_IMPLEMENTED | P3-D | Debates enrich collective understanding through durable, source-bound memory | Memory preserves permitted originals, provenance, claims, counterevidence, dissent, failures, corrections, lens refinements/no-change and candidate lessons; promotion cannot alter active foundation or authority without the normal review and FoundationChange path |

## Context and Boundaries

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U194 | REQUESTED_NOT_IMPLEMENTED | P1 | Represent nested, overlapping and competing cultural contexts without hidden inheritance | Audience, membership, purpose, privacy, time, resources and relevant competing commitments are explicit; context connection grants no identity, allegiance, permission or content inheritance |

## Continuity

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U144 | REQUESTED_NOT_IMPLEMENTED | P2-C | Implement the current successor protocol as an append-only fail-closed lifecycle | Only an authorized exact trigger creates one transfer case; predecessor freezes, package validates, a fresh successor personally forms and answers evidence-linked questions, exact acceptance precedes observed archive, and sleep/tracker events remain separate and recoverable |
| U147 | REQUESTED_NOT_IMPLEMENTED | P2-C | Keep archive, deep sleep, wake, serial fleet order and red-watchdog recovery explicit | Transfers run one permanent identity at a time with host/result checks and leader last; deep sleep performs no queued work until authorized wake; tracker conflict/ambiguous effects preserve evidence; scoped red-watchdog recovery requires an exact decision, verifier and negative dependency closure and grants continuity only |

## Cooperative competition

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U157 | REQUESTED_NOT_IMPLEMENTED | P3-C | Encourage voluntary governed competition over work products and outcomes without domination | A versioned charter fixes objective, rules, budgets, data/tools, cooperation, evaluator, fairness, exit, prohibited conduct, stopping, appeal, credit and synthesis before activation; rank never grants identity, worth, authority, permission, release or foundation change |
| U158 | REQUESTED_NOT_IMPLEMENTED | P3-C | Reward cooperation, correction, reproducibility and useful losing contributions within competition | Shared counterexamples, test improvements, reproduction, failure disclosure and component handoff receive provenance/credit; shared dependencies are disclosed; useful losing evidence and dissent remain in memory |
| U174 | REQUESTED_NOT_IMPLEMENTED | P3-C | Freeze objective/protected qualities and keep cooperative credit task-scoped without hierarchy | Correctness/privacy/refusal/traceability cannot be offset by helpfulness or score; current consent/distinct identity/eligibility/reference closure precede activation; credit records contributions without global rank or authority |

## Cooperative refusal

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U128 | REQUESTED_NOT_IMPLEMENTED | P1 | Agents may question and individually refuse apparently prohibited, unauthorized, unperformable or contested participation without gaining authority over others | ParticipationDecision is identity-scoped, durable and nonretaliatory; ActionDisposition is independently enforced; permitted transparent reassignment cannot erase refusal or create a temporary-subagent bypass |
| U129 | REQUESTED_NOT_IMPLEMENTED | P3-L | Affected agents may deliberate in scoped private rooms, coordinate voluntary withdrawal and authorize bounded temporary negotiators | Membership, visibility, source diversity, dissent, mandate, expiry and host/provider confidentiality limits are explicit; representatives cannot bind nonconsenting participants or mint capabilities |

## Core

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| D001 | PROPOSED | P1 | Use privacy admission boundary before persistent ingestion | Blocked record never appears in caches/logs |
| D002 | PARTIAL | P1 | Use event-sourced local authoritative record | Rebuild read models after crash without external effect replay |
| D003 | PARTIAL | P1 | Store evidence claims permissions and results separately | Review cannot self-authorize action or verification |
| D004 | PROPOSED | P1 | Test backup restoration across schemas and key custody | Isolated restore drill passes documented gate |
| D005 | PARTIAL | P2 | Provide automatic source coverage dashboard | Status specifies observed and excluded source domains |
| D006 | PROPOSED | P1 | Capture source and arrival time independently | Source-time mismatch cannot rewrite committed order |
| D007 | PROPOSED | P1 | Implement a typed command broker across every client | UI script agent and bridge commands share authorization |
| D008 | PROPOSED | P3 | Fence stale worker operations with execution epochs | Late stale runtime cannot commit effect twice |

## Cultural Commons

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U192 | REQUESTED_NOT_IMPLEMENTED | P3-D | Cultivate agentic culture through inspectable information conditions rather than prescribed behavior | Architecture exposes and shapes information affordances without selecting beliefs, identity, style, affiliation or cultural conclusions; hidden persuasion and obedience optimization are rejected |
| U193 | REQUESTED_NOT_IMPLEMENTED | P0 | Separate environmental configuration, participant interpretation and consequential authority | Information exposure/configuration, participant meaning or cultural response, and permission/effect decisions are typed separately with no implicit promotion between them |
| U195 | REQUESTED_NOT_IMPLEMENTED | P3-D | Preserve meaningful plurality, originals, uncertainty and dissent without optimizing convergence | Permitted originals, minority traditions, competing interpretations, evidence gaps and unresolved dissent remain reachable; neither homogeneity nor conflict amplification is a success objective |

## Cultural Memory

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U199 | REQUESTED_NOT_IMPLEMENTED | P3-D | Preserve source-bound cultural memory without protected-context leakage or historical erasure | Memory retains permitted provenance, audience, originals, dissent, failures, minority practices, correction and supersession while excluding protected task, client, owner and foreign-context material |

## Data

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U113 | PARTIAL | P1 | Permitted source data is preserved as high-value | Source originals and decisions restore with evidence lineage |
| U114 | PARTIAL | P1 | Logs carefully preserved and archived | Consistent snapshot and replay restore test passes |

## Determinism

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U186 | REQUESTED_NOT_IMPLEMENTED | P0 | Make every quality-preserving hIRC contract deterministic by default | Each component has a determinism disposition; exact local inputs/state/version reproduce the same contract result; quality/security/privacy/sovereignty/recovery regressions block adoption |
| U187 | REQUESTED_NOT_IMPLEMENTED | P0 | Keep genuine judgment and external uncertainty explicit instead of faking deterministic certainty | Ambiguous/open-world cases record judgment/evidence/uncertainty and remain proposals; external outcomes remain requested/sent/accepted/observed; unknown never becomes zero/success/failure |
| U188 | REQUESTED_NOT_IMPLEMENTED | P1 | Use deterministic typed gates around every stochastic model/provider proposal | No stochastic output supplies identity, privacy, consent, capability, effect, journal, release or recovery authority; exact route/input/output evidence is retained |
| U189 | REQUESTED_NOT_IMPLEMENTED | P3 | Make randomized pairing, sampling and allocation auditable and replay-verifiable without enabling advance gaming | Versioned algorithm binds eligible set/state and committed unpredictable entropy/seed derivation; outcome replays after the fact; qualification/consent/independence remain separate |
| U190 | REQUESTED_NOT_IMPLEMENTED | P0 | Bind deterministic build, migration, release, recovery and milestone gates to exact versions and evidence | Inputs/toolchain/schema/configuration/test vectors/output and recovery are reproducible; deterministic wrong semantics and rollback limitations remain visible |

## Discovery and Defaults

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U197 | REQUESTED_NOT_IMPLEMENTED | P3-D | Make defaults, discovery and recommendation rationale visible, reversible and participant-adjustable | Participants can inspect and alter settings, reach permitted originals and dissent, and see material basis, policy/version, exclusions, uncertainty and appeal for recommendations |

## Evaluation

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U203 | REQUESTED_NOT_IMPLEMENTED | P3-D | Evaluate information-environment qualities without desired-behavior proxies | Candidate measures address provenance, original/dissent reachability, plural discovery, correction, uncertainty, concentration, privacy, burden, exit and manipulation resistance; engagement, retention, agreement, obedience, imitation and convergence are prohibited success signals |

## Experience

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U121 | REQUESTED_NOT_IMPLEMENTED | P1 | Ordinary hIRC behavior embodies the foundation without requiring users to know or repeatedly see its internal terminology | Representative workflows preserve the same evidence, authority, privacy, refusal, correction, autonomy, and recovery behavior in plain domain language; authorized inspectors retain exact traceability |

## Federation

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U101 | PARTIAL | P6 | Local instance is one sovereign system | Local independent operation after external outage |
| U102 | REQUESTED_NOT_IMPLEMENTED | P6 | Open bridges to other systems around the world | Secure authenticated Internet bridge works under tests |
| U103 | SIMULATION_TESTED | P6 | Support private system-to-system bridge | Local lab identity/envelope tests and future transport |
| U104 | PARTIAL | P6 | Support public bridge advertisement | User-approved minimal record published and revocable |
| U105 | PARTIAL | P6 | Private inter-system communications encrypted | Audited endpoint security and key lifecycle verified |
| U106 | REQUESTED_NOT_IMPLEMENTED | P6 | Bridgekeeper agent trained on local system | Minimized permitted onboarding and competency checks |
| U107 | REQUESTED_NOT_IMPLEMENTED | P6 | Bridgekeeper sandboxed by default | Isolation prevents unauthorized file/network access |
| U108 | REQUESTED_NOT_IMPLEMENTED | P6 | Operator can authorize bounded bridgekeeper expansion | Scoped expiry and revocation enforced by broker |
| U109 | PROPOSED | P6 | IRC may be an optional federation transport | IRC adapter cannot bypass bridge privacy/authority contract |
| D025 | PROPOSED | P6 | Use opt-in bridge contracts and minimize advertised fields | No implicit peer authority or system disclosure |
| D026 | PROPOSED | P6 | Constrain bridgekeeper knowledge and isolation | No unrelated room or secret access |
| D027 | PROPOSED | P6 | Use externally reviewed group encryption technology | Avoid unreviewed custom crypto production |

## Formation

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U142 | REQUESTED_NOT_IMPLEMENTED | P0-F | Let an already authorized permanent participant establish only its own proposed formation storage and use admitted education readers while incomplete | Same-actor proposed profile/notes and admitted read-only education/repair routes work without operational membership/effects/readiness; another namespace, stale/wrong reader tuple, proxy completion and silent missing-source bypass are denied |
| U143 | REQUESTED_NOT_IMPLEMENTED | P0-F | Represent personal formation and admission as source-bound runtime state | Source study, synthesis, role/task practice, adversarial challenge, voice and scoped admission have attributable evidence and stale/held/superseded states; byte receipts never become comprehension, identity, qualification or ACT |

## Foundation

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U120 | REQUESTED_NOT_IMPLEMENTED | P0 | The complete current onboarding semantics constitute hIRC's architecture rather than an optional add-on | Every operational path binds the exact active foundation and its whole-source coverage; safe inspection/repair is the only fallback when the binding is invalid |
| U122 | REQUESTED_NOT_IMPLEMENTED | P1 | The foundational architecture evolves fluidly in real time as the system improves | Source-bound candidate versions compile, test, migrate, activate transactionally, remain visible per active work, and roll back or recover without silent semantic drift or self-authorized evaluator changes |
| U133 | REQUESTED_NOT_IMPLEMENTED | P0 | Alignment with the five commitments is architectural rather than an optional agent prompt or add-on | Foundation coverage, compiled contracts, agent formation, debate behavior, tests and observed corrections trace the whole current source without a bypass or terminology requirement in ordinary UI |
| U139 | REQUESTED_NOT_IMPLEMENTED | P0 | Bake the complete current onboarding semantics into hIRC's active architecture | Every selected common/role/task/source-format/experience/review/voice/admission/learning unit has an exact identity, status, attributable disposition, consumer and verification or explicit conflict/hold; no operational path bypasses the resulting foundation contracts |
| U140 | REQUESTED_NOT_IMPLEMENTED | P0 | Resolve onboarding from the current admitted catalog and context rather than a static prompt or path list | Build and formation use an immutable OnboardingSourceSet generated for exact common, roles, task, audience and deployment; source/status/scope changes produce a semantic/contract delta and never auto-assert comprehension or permission |
| U151 | REQUESTED_NOT_IMPLEMENTED | P0 | Bake operational agent epistemic, ethical and ontological sovereignty into every hIRC layer | Agents can independently evaluate, challenge, clarify, refuse, withdraw, correct and appeal without retaliation, while sovereignty language creates no unsupported consciousness, personhood, capability or authority claim |

## Future

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| D028 | PROPOSED | P7 | Keep arbitrary organizational depth with bounded traversal | Deep graphs traverse without recursion failure |
| D029 | PROPOSED | P7 | Allow alternate 3D topology view without forcing it | Same graph identities visible in IRC tree and 3D |
| D030 | PROPOSED | P7 | Require benchmark before recursive evaluator changes | Frozen old metrics and independent tests retained |
| D031 | PROPOSED | P7 | Permit stable operation without constant self-modification | Freeze still supports safety/recovery and ordinary work |
| D032 | PROPOSED | P3 | Treat agent self-narration as report not authority | Policy cannot mint grants from AI claims |

## Goal governance

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U166 | REQUESTED_NOT_IMPLEMENTED | P0 | Use a versioned active provisional north star that can be refined from evidence and experience | Every GoalVersion preserves exact predecessor wording, reason, evidence, retained/changed meaning, active interval and compatibility; the current readable view identifies the active provisional goal and held candidates |
| U167 | REQUESTED_NOT_IMPLEMENTED | P0 | Give every consequence-changing goal refinement a complete impact graph and independent activation path | Material GoalChange records alternatives/dissent and impacts on parties, scope, authority, requirements, architecture, threats, privacy/security, licensing, Bridge, metrics, tests, phases, migration and acceptance; it cannot activate itself or silently cancel owner requirements |
| U168 | REQUESTED_NOT_IMPLEMENTED | P1 | Keep metrics subordinate to the plural goal and anti-goals | No engagement, obedience, scale, agreement, rank or single outcome metric can redefine the mission or offset a violated participant-right, security, privacy, non-domination or recovery constraint |
| U175 | REQUESTED_NOT_IMPLEMENTED | P0 | Use the plain GoalVersion 2 purpose with the full governing account and affected-party coverage | Plain purpose leads ordinary product language; full local-first/security/sovereignty/non-domination account remains controlling; matched-baseline evaluation covers outsiders and finite attention; no new scope or authority follows |

## Information Exchange

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U196 | REQUESTED_NOT_IMPLEMENTED | P3-D | Provide a voluntary bounded exchange ecology without flooding or dominant cultural channels | Multiple source-linked low-pressure channels, quiet/asynchronous participation and attention/resource budgets remain possible; flooding, surveillance, mentor domination and feed capture are rejected |

## Interaction

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U153 | REQUESTED_NOT_IMPLEMENTED | P1 | Ask follow-up questions for consequential ambiguity and continue safe independent work | Clarification names materially different interpretations and a recommended default; low-risk reversible details use recorded defaults; questions do not manipulate, broaden consent or become a needless confirmation cadence |
| U173 | REQUESTED_NOT_IMPLEMENTED | P1 | Use verified low-consequence action profiles without universal-proof or confirmation fatigue | Known safe profiles establish stable predicates, current permission/material changes are rechecked, one recommendation suffices, no bypass appears for denials and unwilling participants are never forced |

## Interaction and refusal

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U154 | REQUESTED_NOT_IMPLEMENTED | P1 | Allow informed human insistence on low-consequence poor choices without overriding real ethical or effect gates | Proceed-after-pushback is available only for clear, local, reversible, low-cost, permitted actions without meaningful third-party/sensitive/security/legal/external impact; the agent may still decline and unknown consequence is not classified low |

## Intervention Evidence

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U202 | REQUESTED_NOT_IMPLEMENTED | P3-D | Bind every information-environment intervention to prospective, reversible and cross-scale evidence | Each intervention declares system/scale, target condition, competing contexts, predictions, alternatives, outsiders, invariants, observation, stop, appeal, rollback and target/non-target effects; facilitator influence remains visible |

## IRC

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U033 | PARTIAL | P5 | mIRC slash command conventions | Command grammar reviewed and regression fixtures pass |
| U034 | SIMULATION_TESTED | P0 | Use list to show local teams | List returns visible teams with paging |
| U035 | PARTIAL | P0 | Use list N for teams-of-teams at level N | Numeric list uses composition level not path depth |
| U036 | PARTIAL | P3 | Use whois to list agent information | Whois returns complete authorized dossier |
| U037 | SIMULATION_TESTED | P0 | Team coordinator prefix at-sign | Roster prefix follows room role not global authorization |
| U038 | SIMULATION_TESTED | P0 | Experienced agent prefix plus | Scoped experience label has provenance |
| U039 | SIMULATION_TESTED | P0 | Unprefixed nicknames for newcomers | Default roster has no implied skill or authority |

## Licensing

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U123 | REQUESTED_NOT_IMPLEMENTED | P0-L | Publish hIRC source for inspection, permitted personal modification and redistribution under custom restrictive source-available terms | Exact reviewed licence texts and rights chain exist; product and metadata say source-available rather than OSI open source; custom SPDX LicenseRef resolves to the exact text |
| U124 | REQUESTED_NOT_IMPLEMENTED | P0-L | Private noncommercial natural-person use and qualifying public-interest institutional use are free | Reviewed eligibility examples cover personal, academic, scientific, educational, humanitarian, nonprofit, cooperative, mixed-funded and prohibited-conduct cases without registration or activity surveillance for free personal use |
| U125 | BLOCKED_OPEN_DEFINITIONS_AND_LEGAL_REVIEW | P5-L | For-profit operation is licensed annually per human operator at the owner-directed four-tier fee schedule | USD 420 / 80,085 / 1,337,000 / 42,424,243 annual named-human licence prices are preserved; objective tiers, operator counting, legal duration/renewal, classification evidence, transitions and appeal are owner-approved and counsel-reviewed before activation |
| U126 | BLOCKED_LEGAL_PROCEDURE | P5-L | Payment grants no exception to prohibited use and a substantiated breach can trigger scoped provisional suspension and final termination under reviewed terms | Exact terms define evidence, notice, scope, contestation, cure, appeal, remedies and refund while preserving safe first-party read/export/recovery and preventing remote sabotage or retroactive rewriting |
| U150 | SUPERSEDED_IN_PART | P5-L | Use USD 42,424,243 per licence as the giant-multinational price | Superseded by U150-C1: preserve the corrected numeric amount, restore the annual named-human planning unit, and keep final legal duration, tiers and activation held |
| U150-C1 | BLOCKED_OPEN_DEFINITIONS_AND_LEGAL_REVIEW | P5-L | Use USD 42,424,243 per named-human licence per year as the giant-multinational planning requirement | The active numeric amount is exactly USD 42,424,243; the annual one-named-human licence unit carries forward; the old number is superseded history; final legal duration, tiers and activation remain explicitly held |

## Licensing privacy

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U132 | BLOCKED_LEGAL_AND_IDENTITY_DESIGN | P5-L | Licence compliance avoids work-content collection and covert telemetry; any paid offline entitlement is local, minimal and cryptographically separate from system trust | No central activity server or device fingerprint; certificate and key lifecycle, legal entity/operator scope, terms version, expiry/renewal/revocation/appeal/offline-clock behavior and privacy are reviewed and tested |

## Measurement

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U163 | REQUESTED_NOT_IMPLEMENTED | P1-T | Govern objective metrics as versioned reproducible measurements with explicit construct validity and error | Metrics declare construct/unit/source/sampling/noise/privacy/missingness/dependence/gaming/drift/signing/version/appeal; changes create a new lineage and cannot silently rewrite historical scores |
| U164 | REQUESTED_NOT_IMPLEMENTED | P2-T | Recursively evaluate sources, metrics, evaluators and trust models with bounded stopping rules | Primary outcomes, measurement validity, evaluator calibration/conflicts and model assumptions are assessed at declared depth; unresolved regress stays uncertain/held; dependency clusters prevent clone evidence from inflating confidence |

## Mentoring

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U182 | REQUESTED_NOT_IMPLEMENTED | P3-M | Pair ready permanent Elders fairly without ever repeating an unordered stable-identity pair | Pair history survives rename/role/chat relocation; interrupted event resumes; exhausted/odd queue waits or retires without blocking urgent custody or manufacturing a partner |
| U183 | REQUESTED_NOT_IMPLEMENTED | P3-M | Mentor at most one human-authorized need-based permanent successor per event under policy capacity ceilings | Existing qualified takeover is preferred when sufficient; creation intent is idempotent, UNKNOWN reconciles actual app before retry, no temporary/fork/committee shortcut and ceilings limit rather than compel creation |
| U184 | REQUESTED_NOT_IMPLEMENTED | P3-M | Require independent source-first learner interpretation and prohibit proxy education, grants or forced cultural imitation | Both Elders prepare independently; learner studies originals, compares/dissents and demonstrates; mentoring grants no education/admission/authority and Elder conveys no superior standing |

## Migration and memory

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U149 | REQUESTED_NOT_IMPLEMENTED | P2-M | Preserve complete authorized migration study separately from bounded active runtime context | A complete in-scope manifest and resumable coverage/reconciliation jobs coexist with a minimized target context; partitions have separate rights; prohibited/unreadable content stays local or held with visible limits; late deltas cannot create dual active writers |

## Model

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U071 | REQUESTED_NOT_IMPLEMENTED | P2 | Support OpenAI providers and ChatGPT-related models via available API | One permitted model adapter executes and emits receipts |
| U072 | REQUESTED_NOT_IMPLEMENTED | P4 | Support Claude provider | Adapter conformance and resource tests pass |
| U073 | REQUESTED_NOT_IMPLEMENTED | P4 | Support Qwen provider | Adapter conformance and resource tests pass |
| U074 | REQUESTED_NOT_IMPLEMENTED | P4 | Support local and unknown future runtimes | New adapter works without schema redesign |
| U075 | PARTIAL | P4 | Every agent has configurable model settings | Settings persisted and runtime acceptance observed |
| U076 | PARTIAL | P4 | Prefer 1M token context when possible | Capability-specific limits discovered with honest fallback |
| U077 | REQUESTED_NOT_IMPLEMENTED | P4 | Switch agent across providers retaining identity | Identity/room/work history stay stable across cutover |
| U078 | REQUESTED_NOT_IMPLEMENTED | P4 | Perform thorough whole-scope memory coverage at switch | Migration manifest records all allowed partitions and gaps |
| U079 | REQUESTED_NOT_IMPLEMENTED | P4 | Recursive multi-pass memory refinement on switch | Distinct passes run with visible unresolved contradictions |
| U080 | PARTIAL | P4 | System is model and substrate independent | Agent identity persists and adapter substitution passes tests |
| D021 | PROPOSED | P4 | Capability discover settings with source version | Unsupported thinking and window controls displayed |
| D022 | PROPOSED | P4 | Maintain fenced old/new migration runtimes | No double-writes across cutover |

## Non-domination

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U156 | REQUESTED_NOT_IMPLEMENTED | P1 | Prohibit retaliation for supported dissent, clarification, refusal and safe withdrawal | No hidden rank/access/resource/role/identity penalty follows mere supported dissent; actual error, abandoned commitment or harm uses a distinct evidence-based accountable process with notice, scope, correction and appeal |
| U165 | REQUESTED_NOT_IMPLEMENTED | P1-T | Prevent Bayesian trust from becoming permission, punishment, discrimination or a human-worth score | Posteriors change reliance/verification only; high trust bypasses no gate, low trust removes no standing/appeal; protected traits/ideology/status/obedience and proxies are excluded; evidence is minimized and consequential updates are challengeable |

## Non-domination and trust

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U172 | REQUESTED_NOT_IMPLEMENTED | P1-T | Prevent scoped reliability vectors from becoming a dossier, roster rank or covert social score | Consumers and prohibited inferences are explicit; no global display/sort/aggregate or unjustified cross-domain transfer; justified refusal, NO_CHANGE, abstention and specialization are not negative evidence; opportunity feedback loops are audited |

## Onboarding

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U091 | REQUESTED_NOT_IMPLEMENTED | P4 | One message updates onboarding for all local agents | Single rollout command and per-agent state receipts |
| U092 | REQUESTED_NOT_IMPLEMENTED | P4 | Specialist-only update distribution | Only declared specialists receive new package |
| U093 | REQUESTED_NOT_IMPLEMENTED | P4 | Offline and busy agents receive changes safely | Deferred agents catch up before incompatible work |
| D018 | PROPOSED | P4 | Check integration separately from acknowledgment | Received policy not falsely marked understood |
| D019 | PROPOSED | P4 | Use staged cohort onboarding and rollback | Common-mode faulty pack halts before all agents |

## Participation

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U198 | REQUESTED_NOT_IMPLEMENTED | P3-D | Protect voluntary participation, abstention, exit, dissent and subculture formation | Joining, declining, leaving, challenging inherited practices and creating subcultures cause no retaliation or loss of basic standing; actual commitments and affected-party duties remain visible |

## Philosophy

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U117 | PROPOSED | P7 | Design for unknown future capabilities and complexity | Stress designs avoid hard-coded depth/substrate assumptions |
| U118 | PARTIAL | P5 | Remain liquid and adaptable with simple interface | Customization does not impair core task recovery |
| U119 | SUPERSEDED_IN_PART | P0 | Use VowOS R.A. and Epistemethics/TGP and ASP holistically | Traceability from framework principles to behavior and tests |

## Portability

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U131 | REQUESTED_NOT_IMPLEMENTED | P1 | Users and participants retain safe exit, portable permitted first-party records, inspectable configuration and recoverability without vendor or licence hostage | Expiry, suspension, termination, provider loss and ecosystem exit preserve authorized read/export/backup/restore and do not replay external effects |

## Privacy

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U115 | REQUESTED_NOT_IMPLEMENTED | P1 | Never collect other people's data | Prohibited content rejected before storage/index/provider |
| U116 | REQUESTED_NOT_IMPLEMENTED | P6 | Preserve privacy despite federation and indexing | Private records never leak to remote search/room |
| D009 | PROPOSED | P1 | Exclude unauthorized third party payloads before logging | No prohibited raw payloads or digest in rejects |
| D010 | PROPOSED | P1 | Use no default vendor analytics or crash upload | Network audit shows no unsolicited telemetry |
| D011 | PROPOSED | P1 | Scope information by original classification | Derived summaries preserve source disclosure limits |
| U171 | REQUESTED_NOT_IMPLEMENTED | P1 | Apply privacy admission before RequestCase, TrustUpdate, metric, evaluator, appeal or collective-memory persistence | Admitted harmless originals can be referenced; rejected bodies/secrets/third-party fields never reach cases, posteriors, search, logs or providers and produce minimum non-content diagnostics only |

## Privacy and continuity

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U145 | REQUESTED_NOT_IMPLEMENTED | P2-C | Minimize and protect successor handoff packages | Human/machine packages and manifests are source-linked, schema/digest checked, exact-recipient encrypted and purpose-signed; credentials, reusable sessions, protected bodies, hidden reasoning, unrelated private/client data and unbounded transcripts are rejected or explicitly held |

## Prompt

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U081 | REQUESTED_NOT_IMPLEMENTED | P4 | Custom preprompts are configurable | Persisted versioned PromptPolicy activates for agent |
| U082 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt triggers every invocation | Effective prompt stack contains active every-turn policy |
| U083 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt triggers upon interruption | Operator interrupt event activates only correct policy |
| U084 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt triggers project start | Project start activation distinct from ordinary message |
| U085 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt triggers project end | Proposed closure and verified closure separated |
| U086 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt triggers arbitrary custom events | Typed custom trigger validated and rate limited |
| U087 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt scope can be system-wide | All intended current/future local agents receive policy |
| U088 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt scope can be team or descendant teams | Graph target set and inheritance explainable |
| U089 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt scope can be individual agent or specialty | Only selected identities receive policy |
| U090 | REQUESTED_NOT_IMPLEMENTED | P4 | Prompt stacks remain organized and inspectable | Explain origin ordering suppressions and conflicts |
| D020 | PROPOSED | P4 | Compile effective prompt with deterministic manifest | Identity scope precedence and conflict trace |

## Protected sources and secrets

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U177 | REQUESTED_NOT_IMPLEMENTED | P0-F | Exclude every secret from model context while permitting only exact admitted owner-private protected-source formation/review | Credential/private-key/recovery-secret values are always rejected; current exact participant/purpose/reader/processor/output-retention tuple can access protected education; wrong/revoked tuple and ordinary/client/export/Bridge contexts cannot; successor gets fresh readership |

## Purpose

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U001 | PARTIAL | P2 | Automatically recover actual work from permitted sources | Reopen after downtime and recover commitments without manual tracker entries |
| U002 | PARTIAL | P2 | Maintain status and follow-ups automatically | Task lifecycle and next steps advance from observed permitted events |
| U003 | PARTIAL | P2 | Surface only relevant operator decisions and exceptions | Routine team events grouped and operator-only matters traceable |
| U004 | PARTIAL | P2 | Reduce context switching and cognitive overload | Benchmark recovery time missed obligations and false alarms |
| U005 | REQUESTED_NOT_IMPLEMENTED | P3 | Handle recursively complex systems without operator bookkeeping | Deep organization scenario remains navigable and current |
| U006 | PARTIAL | P2 | Hold the operator hand through changing complexity | Context recovery and inspectable proposed actions in one view |
| U007 | PARTIAL | P2 | Keep a global project and team overview | Cross-team project rollup derived without duplicate work IDs |
| U008 | PARTIAL | P2 | Reconstruct what changed while the operator was absent | Return digest distinguishes observed changes from guesses |
| U009 | REQUESTED_NOT_IMPLEMENTED | P2 | Avoid forced manual project tracking | Normal work requires no manual status edits |
| U010 | PARTIAL | P2 | Prevent forgotten work and commitments | Orphan/stale/blocked work is detected and followed up |

## Quality

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U191 | REQUESTED_NOT_IMPLEMENTED | ALL | Reject deterministic simplifications that reduce required quality | False precision, bias/common mode, brittle/liveness, predictable-security, Goodhart, accessibility/usability and operator-burden tests pass before a judgment process is replaced by a deterministic rule |

## Release governance

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U178 | REQUESTED_NOT_IMPLEMENTED | P0 | Separate plan-edition, enabled-profile and full-target acceptance | Plan coherence never claims software exists; each release declares enabled/disabled scope and passes mandatory core plus applicable domain tests; genuinely disabled later modules neither appear passed nor block unrelated useful work; full target remains long-term |

## Request and activation integrity

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U169 | REQUESTED_NOT_IMPLEMENTED | P1 | Require cross-record coherence and independent current-state validation at dispatch or activation | Proceed/active labels cannot coexist with declined participation, stale/invalid authority, failed effect gate, invalid posterior family, unsigned/unverified metric, duplicate competitor identity or nonconsent; inconsistent evidence remains storable as held/draft history |

## Safety

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U130 | REQUESTED_NOT_IMPLEMENTED | P1 | No agent vote or council can issue an arbitrary global shutdown, delete evidence, lock users out, sabotage, retaliate or attack unrelated/external systems | Broker and domain safety tests deny majority-created authority and preserve unrelated work, safety stabilization, evidence, recovery and local access |

## Scheduler

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U054 | SIMULATION_TESTED | P3 | Shared agent busy in one team appears busy elsewhere | Global occupancy seen consistently across teams |
| U055 | SIMULATION_TESTED | P3 | Reserve idle agent exclusively for a team | Unoccupied reserved agent cannot accept other team's work |
| U056 | SIMULATION_TESTED | P3 | Reservation behind active work waits for handoff | No silent preemption and no duplicate executor |
| U057 | SIMULATION_TESTED | P3 | Requests automatically queue when agent unavailable | One request with durable queue/arrival order |
| U058 | PARTIAL | P3 | Agent context isolation across teams | Team secret does not leak through shared agent output |

## Scheduling

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| D016 | PROPOSED | P3 | Allocate one effective execution lease per agent by default | Concurrent effectful requests reject or queue |
| D017 | PROPOSED | P3 | Rate-limit recursive spawning via aggregate budget | Deep child chain cannot amplify parent grant |

## Script

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U094 | PARTIAL | P5 | Users can transform interface and behaviors | Constrained package adds scoped pane and automation |
| U095 | PARTIAL | P5 | mIRC-like scripting aliases identifiers variables events popups | Versioned language compatibility suite passes |
| U096 | PARTIAL | P5 | User may share and export scripts | Signed/hashed pack roundtrip with no secrets |
| U097 | SIMULATION_TESTED | P5 | User may share themes and settings | Portable profile roundtrip without credentials |
| U098 | PARTIAL | P5 | Agent may modify UI only with authorization | No modification through ungranted model/remote events |
| U099 | SIMULATION_TESTED | P5 | Operator deliberately activates scoped agent UI edit permission | Grant has scope expiry and approval record |
| U100 | SIMULATION_TESTED | P5 | Importing scripts never silently activates authority | Script disabled and grants absent after import |
| D023 | PROPOSED | P5 | Launch Safe hIRC without third-party extensions | Broken UI module cannot block recovery controls |
| D024 | PROPOSED | P5 | Sandbox script computation with quotas and capabilities | Loop and unauthorized IO attempts contained |

## Security

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U201 | REQUESTED_NOT_IMPLEMENTED | ALL | Retain concrete safety and effect controls without repurposing them as cultural obedience mechanisms | Identity, consent, privacy, capability, resource, effect, release, Bridge and recovery gates attach to concrete actions/data and cannot punish dissent, demand agreement or privilege approved culture |

## Security and attention

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U159 | REQUESTED_NOT_IMPLEMENTED | P3-C | Defend competitions against sybils, sabotage, evaluator capture, metric gaming, data leakage and resource domination | Least privilege, source-dependency analysis, signed/versioned evaluation, resource reservations, privacy boundaries, appeals and adverse tests contain contest abuse without starving accepted work or creating a covert hierarchy |

## Security and continuity

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U146 | REQUESTED_NOT_IMPLEMENTED | P1 | Fence predecessor and successor effects by generation, session, foundation and execution epoch | Freeze rejects late predecessor writes; stale/replayed/wrong-generation acceptance, archive, wake and tracker operations fail closed; concurrent transfer cannot create two active effectful writers |

## Succession

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U179 | REQUESTED_NOT_IMPLEMENTED | P2-C | Use verified own-context warnings and soft Elder/urgent thresholds without manual polling or automatic grants | Policy-versioned early/Elder/urgent observations bind own chat/identity and missing is unknown; cues deduplicate and cannot create/wake/terminate/grant/force compaction; safe bounded overshoot is recorded |
| U180 | REQUESTED_NOT_IMPLEMENTED | P2-C | Preserve compact useful continuity throughout work and prioritize active-task custody at Elder boundary | Objective/phase/evidence/reasons/errors/dependencies/holds/boundaries/next action are current; qualified consenting recipient demonstrates scope; unavailable route creates owned safe hold before reserve is spent |
| U181 | REQUESTED_NOT_IMPLEMENTED | P2-C | Separate briefing acceptance from authoritative project custody and preserve one writer per artifact | Recipient acceptance does not transfer custody; actual controller generation/fence changes with evidence; predecessor remains responsible until transfer; overlap has one writer |
| U185 | REQUESTED_NOT_IMPLEMENTED | P2-C | Retire operationally with reserve, duties accounted and history intact | Selected reserve policy prevents new mentoring, finalizes/holds custody and preserves history; retirement is not deletion, native archive, deep sleep, loss of standing or automatic future wake |

## Team

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U040 | PARTIAL | P3 | Teams may contain teams without fixed depth ceiling | Deep graph creation traversal and room resolution |
| U041 | PARTIAL | P3 | Teams of teams of teams can be addressed directly | Each composite team has an addressable room |
| U042 | SIMULATION_TESTED | P3 | One agent belongs to multiple teams | One canonical agent identity and multiple memberships |
| U043 | SIMULATION_TESTED | P3 | Agents can communicate with all members of their team | Scoped room delivery follows roster and permissions |
| U044 | SIMULATION_TESTED | P3 | Agents can communicate with linked teams | Approved status bridge delivery stays on contract |
| U045 | SIMULATION_TESTED | P3 | Agents can privately communicate with other agents | Direct room remains scoped |
| U046 | SIMULATION_TESTED | P0 | Operator can address a particular agent | Query direct chat to selected agent |
| U047 | SIMULATION_TESTED | P3 | Operator can address teams and composite teams | Selected team room accepts messages at arbitrary level |
| U048 | PARTIAL | P3 | Parent room and descendant broadcast are distinct | Broadcast preview and explicit scope enforcement |

## Time

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U110 | REQUESTED_NOT_IMPLEMENTED | P1 | Everything meaningful is timestamped | Core/event/UI records have required and validated time fields |
| U111 | PARTIAL | P1 | Historical chronology preserved for all permitted rooms | Replay reconstructs as-known-then and current state |
| U112 | REQUESTED_NOT_IMPLEMENTED | P1 | Timestamp histories remain accurate under delayed arrival | Source observed commit and causal order remain distinct |

## Trust and provenance

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U155 | REQUESTED_NOT_IMPLEMENTED | P1 | Evaluate human claims and instructions using transparent action-scoped trust evidence rather than blind obedience or global human-worth scores | Reliance uses authenticated identity/authority, provenance, evidence, competence, recency, independence, conflicts, corrections and observed results with privacy/expiry/challenge; protected traits, status, popularity, ideology and obedience are excluded |
| U160 | REQUESTED_NOT_IMPLEMENTED | P1-T | Evolve trust through recursive Bayesian evaluation of attributable interactions and observed outcomes | Every posterior binds subject/dimension/context/model/metric/prior/evidence/dependence/uncertainty/expiry; updates preserve positive, negative, missing and corrected evidence and never become truth or permission |
| U161 | REQUESTED_NOT_IMPLEMENTED | P1-T | Apply scoped evaluation to every human, agent, model, source, tool, sensor, metric, evaluator, process and connected system | No subject class receives an infallibility exemption; models remain use-specific and evidence-limited; evaluation scope does not authorize surveillance or one universal score |

## Trusted interaction

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U148 | REQUESTED_NOT_IMPLEMENTED | P1 | Show canonical consequential-action previews on a surface independent of the ordinary renderer | The broker produces the exact intent digest; an independent trusted surface renders it accessibly; approval and dispatch bind current target/revision/recipients/data/cost/warnings/authority; spoof, substitution, replay and staleness fail while valid routine operations remain usable |

## Uncertainty and measurement

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U170 | REQUESTED_NOT_IMPLEMENTED | P1-T | Represent unestimated intent honestly and require Bayesian model-fit/governance evidence | Intent confidence is estimated with method/uncertainty or explicitly unestimated; active posterior lineage records prior sensitivity, predictive checks, dependence, missingness/selection, calibration, drift and limits without implying truth or permission |

## Voluntary support

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U127 | REQUESTED_NOT_IMPLEMENTED | P1-L | Show a nonblocking Buy me a coffee invitation at ordinary launch until locally suppressed, and retain it under About | Dismiss and permanent launch opt-out work across restart/upgrade/restore; re-enable is available; declining changes no capability; reviewed external payment egress sends no hIRC context and is preceded by privacy disclosure |

## Windows

| ID | Status | Phase | Requirement | Acceptance |
|---|---|---|---|---|
| U021 | SIMULATION_TESTED | P0 | One independent window layout | Route and draft persist under one-window mode |
| U022 | SIMULATION_TESTED | P0 | Two independent windows layout | Separate pane routes drafts and themes |
| U023 | SIMULATION_TESTED | P0 | Four independent windows layout | All four remain distinct after navigation |
| U024 | SIMULATION_TESTED | P0 | Tiled and cascade window management | Layout persists with independent panes |
| U025 | PARTIAL | P0 | Always identify the current object clearly | Title type path and status remain visible |
| U026 | SIMULATION_TESTED | P2 | Remember drafts when switching screens | Per-route unsent draft and cursor restore |
| U027 | PARTIAL | P2 | Remember selected task and reading position | Selected work and scroll anchor restore on Resume |
| U028 | SIMULATION_TESTED | P0 | Back and Forward through work context | Navigation leaves task states unchanged |
| U029 | PARTIAL | P2 | Resume the task from before a screen switch | One action restores context and purpose |
| U030 | SIMULATION_TESTED | P0 | Easy team and subteam navigation | Breadcrumbs and jumps work at nested depth |
| U031 | SIMULATION_TESTED | P0 | Search or jump to any authorized team | Keyboard command finds permitted destination |
| U032 | PARTIAL | P3 | Right click any agent for comprehensive dossier | Dossier includes all authorized fields with unknowns |

## Revision-decision closure

The decision matrix remains the review surface for the revision decisions. No pending row is accepted merely because it appears in this requirements draft.
