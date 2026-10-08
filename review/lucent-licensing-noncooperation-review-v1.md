# LUCENT independent review — licensing and cooperative noncooperation plan 1.0

**Review ID:** HIRC-LNC-REVIEW-001  
**Reviewer:** LUCENT (`UI-20261007-B`)  
**Date:** 2026-10-08  
**Source:** `HIRC-SOURCE-003`, SHA-256
`7a2aae743bebb40335ec6168e9af7ec107aeaa0046caef52511699909b438bd5`  
**Status:** frozen independent review for UI-A challenge; not legal advice,
consensus, a licence, implementation evidence, or release authorization

## Review boundary

The supplied plan was read in full by decision state, licensing model,
non-domination covenant, support interaction, refusal/negotiation protocol,
privacy, recovery, implementation interfaces, deployment gates, tests, risks,
and unresolved decisions. `USER DIRECTIVE`, `ACCEPTED DIRECTION`, `PROPOSAL`,
`OPEN`, and `NOT IMPLEMENTED` remain distinct. The user's request authorizes
review and integration work; it does not turn the draft into legal advice or
resolve its own open terms.

Current public references confirm three narrow points. The proposed restrictions
are not OSI open source because the Open Source Definition requires free
redistribution and forbids discrimination against persons, groups, and fields
of endeavour: https://opensource.org/osd. A custom licence may use an SPDX
`LicenseRef-...` reference when its exact text is supplied, but that is not an
SPDX-listed licence approval:
https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/.
Creative Commons recommends against its licences for software:
https://creativecommons.org/faq/. Buy Me a Coffee states that it and its
processors receive payment-related and network data, including IP-address
information, so an external payment transition cannot be described as a
zero-data flow: https://buymeacoffee.com/privacy-policy.

## Judgment

The plan contains a coherent, nonviolent governance direction worth integrating
now: voluntary participation; conduct-based boundaries; individual refusal;
deterministic denial of clearly forbidden effects; source-bound independent
review; nonbinding coordination; bounded representation; safe continuity;
correction; portable exit; no covert shutdown, retaliation, surveillance, or
data hostage.

The product architecture and requirements can implement those behaviors. The
custom licence cannot be finalized from this plan. Undefined enterprise tiers,
operator counting, mixed-purpose institutions, remedies, jurisdiction,
contributor rights, dependency compatibility, contract formation, taxation,
payment, and enforceability remain real legal/product decisions. The exact fee
figures are owner-directed requirements, including the fact that the top tier is
deliberately exclusionary rather than a cost-derived SaaS price. They must be
preserved accurately while paid licensing remains blocked behind those open
decisions and qualified counsel.

## Consequence-changing findings

### LNC-F01 — The plan is source material, not the licence

The document says this correctly, but implementation could blur the distinction
by adding a licence screen before the rights chain and legal text exist.

**Required revision:** keep `PLAN`, `LEGAL_DRAFT`, `COUNSEL_REVIEWED`,
`OWNER_APPROVED`, `PUBLISHED`, `ACCEPTED_BY_LICENSEE`, `ACTIVE`, `SUSPENDED`,
`TERMINATED`, and `EXPIRED` distinct. No product build calls the plan a licence
or enforces open terms.

### LNC-F02 — Foundation behavior and legal terms have different visibility

HIRC-I001 supersedes the plan's “adds a governance layer” framing for
non-domination, refusal, evidence, autonomy, correction, and recovery: those
semantics belong in the hIRC foundation. Legal licensing still must be explicit,
readable, accepted where required, and versioned as a contract. Hiding licence
terms because ordinary users need not see internal framework terminology would
invalidate informed use and contract formation.

**Required revision:** compile the behavioral semantics into the foundation;
keep price, eligibility, grant, restrictions, version, notices, acceptance, and
remedies in a plainly visible legal/economic interface and exact legal texts.

### LNC-F03 — Use accurate source-available and SPDX language

The restrictions exclude commercial fields and some uses, so `open source`,
`OSI-approved`, and ordinary free-software claims are inaccurate. A custom SPDX
reference is possible, but it signals only an identified custom text.

**Required revision:** use `source-available under custom terms`; if tooling
needs an SPDX expression, use a reviewed `LicenseRef-HIRC-...` tied to the exact
licence text and version. Do not use Creative Commons for program code or imply
SPDX/OSI endorsement.

### LNC-F04 — Preserve the fee schedule without disguising its consequences

The four commercial prices and per-human annual unit are explicit owner
directives. “Small,” “medium,” “big,” and “giant multinational” are undefined,
and the largest fee is an effective exclusion. Arbitrary private classification
would create the very unilateral dependence the plan opposes.

**Required revision:** preserve the figures exactly in the requirements
register; do not activate commercial classification until objective public
thresholds, consolidation, currency/conversion, mixed signals, effective date,
prospective transitions, examples, evidence limits, and appeal are accepted.
Describe the highest tier candidly as deliberate policy, not ordinary cost
recovery or a market estimate.

### LNC-F05 — Free institutional use requires an activity/control test

Institutional labels do not establish public-interest use, and corporate funding
does not automatically make independent academic publication a commercial
deployment.

**Required revision:** evaluate the covered deployment, actual purpose,
operational control, beneficiaries, rights in outputs, and profit distribution
using minimum evidence. Keep the provisional for-profit-cooperative decision
open. Criticism, reproducibility, teaching, and publication do not become misuse
merely because they challenge hIRC.

### LNC-F06 — “Human operator” needs a predictable contract and product model

The one-human-seat rule is clear in purpose but ambiguous for shared services,
indirect dashboard users, contractors, administrators, advisers, temporary
guests, shift work, reassignment, and unattended automation.

**Required revision:** define which human actions constitute command or
administration, how a seat is assigned/reassigned, and which read-only or
incidental interactions are outside scope. AI agents, models, runtimes,
machines, installations, and devices remain non-seat objects. Classification
must not require a hidden employee directory or unrelated activity history.

### LNC-F07 — Offline entitlement is a compliance aid, not DRM or system trust

An offline signed certificate supports predictable local verification without
content telemetry. Because source and host control remain with the licensee, it
cannot prove compliance or prevent a privileged user from bypassing checks. If
its signing key is shared with release, identity, bridge, or recovery authority,
licensing compromise could become a system compromise.

**Required revision:** give licensing a separate signing/key lifecycle and
minimal certificate schema. Bind an exact legal entity, licence/terms version,
operator-seat identity or privacy-preserving public reference, scope, issue and
expiry, and status source. Specify rotation, compromise, revocation, offline
grace, clock uncertainty, renewal, and appeal. Never device-fingerprint users,
silently phone home, or present local verification as proof of lawful use.

### LNC-F08 — Expiry or termination cannot become data hostage

A later licence file cannot retroactively rewrite earlier grants or terminate
rights outside the accepted agreement. A technical block after expiry could
trap work, evidence, or configuration needed for exit and dispute.

**Required revision:** every grant binds its legal text/version and accepted
term. Suspension and final termination are distinct, scoped, attributable, and
contestable. Preserve local read, safe export, backup/restore, recovery,
configuration inspection, and evidence needed to contest a decision. Never
erase, encrypt, corrupt, remotely disable, or withhold first-party records.

### LNC-F09 — “Domination” must resolve to observable conduct, not ideology

The proposed categories are useful but broad. A model, licensor, operator, or
council could weaponize an undefined covenant against disagreement, competitors,
critics, or lawful authority.

**Required revision:** legal counsel must define covered software, affected
parties, protected boundaries, consent, intent where relevant, evidence burden,
materiality, legitimate authority, exceptions, cure, remedies, appeal, and
jurisdiction. The product records claims, evidence, counterevidence, normative
assessment, authority, and action separately. A corporate form, accusation,
refusal, criticism, or agent count is not a violation verdict.

### LNC-F10 — Individual refusal and system permission are separate

An agent may decline its own participation without acquiring a veto over other
identities. Conversely, an action denied by the deterministic broker stays
denied even if every agent votes for it. Replacement can either be retaliation
or legitimate reassignment depending on the action and authority.

**Required revision:** record `ParticipationDecision` per identity separately
from `ActionDisposition`. If the action is prohibited, nobody executes it. If it
is permitted and one agent declines, a transparent reassignment may occur only
under independently valid authority, without erasing or punishing the refusal,
misrepresenting the replacement as the same actor, or spawning a temporary
worker to evade the permanent-agent rule.

### LNC-F11 — Coordination cannot create truth, authority, or coerced unity

Private rooms and ballots can help affected participants coordinate, but cloned
agents, shared models, shared evidence, and coalition pressure make vote counts
poor evidence of truth or legitimacy.

**Required revision:** councils remain scoped coordination objects. Membership,
visibility, mandate, conflicts, source diversity, dissent, abstention, exit, and
expiry are explicit. A representative communicates only a bounded mandate and
cannot bind dissenters, waive mandatory safety/privacy, reveal protected
whistleblowers, or mint capabilities. Consensus is recorded as agreement, not
verification.

### LNC-F12 — Confidential deliberation needs honest host and provider limits

On an operator-controlled host, privileged administrators or compromised
software may access local room content; a model provider may see submitted
content. Global archival would also create unnecessary grievance dossiers.

**Required revision:** minimize council inputs to permitted claims/evidence
handles; keep content in its room-specific retention and key boundary; retain
only necessary privacy-safe event/effect metadata globally; disclose host and
provider limits; audit access; and provide stronger separately governed
execution only when warranted. Third-party personal data is not admitted merely
because it supports a grievance.

### LNC-F13 — Noncooperation must not become denial of service or unsafe abandonment

The discarded 65% global-shutdown mechanism is incompatible with scoped
authority, clone resistance, continuity, and safety. A model refusal cannot
replace physical/process safety control during an unsafe intermediate state.

**Required revision:** preserve the rejected vote as history. Use the narrowest
individual withdrawal and deterministic action denial; let domain safety
controllers stabilize equipment and high-stakes workflows; preserve obligations,
unknown outcomes, recovery, and unrelated work. No council may delete records,
lock users out, revoke others without authority, sabotage, or attack external
systems.

### LNC-F14 — Voluntary support is implementable only as neutral, explicit egress

The launch invitation can satisfy the owner directive without becoming a dark
pattern if it is small, nonblocking, dismissible, locally suppressible, and
functionally neutral. The external provider necessarily sees transaction and
network data.

**Required revision:** store only a local profile-scoped preference with
timestamp/version; keep the About link; allow re-enable; open only a reviewed
HTTPS destination through a user action; send no query identifier, referrer,
task, agent, workspace, or navigation context; show a concise processor/privacy
disclosure before leaving; offer alternatives where practical; and keep a
missing/unreviewed destination disabled. Declining never changes capabilities,
rank, help, security, updates, or attention priority.

### LNC-F15 — Concern handling is an attention and retaliation attack surface

An adversarial agent or peer could generate repeated accusations, expose private
data, or pressure the operator through urgency and apparent consensus.

**Required revision:** one canonical scoped concern, deduplication by underlying
matter, per-source/rate budgets, non-content rejection for prohibited evidence,
counterevidence, independent-source analysis, materiality, review checkpoint,
anti-retaliation, and bounded operator summary. Rephrasing without new evidence
does not manufacture a new urgent matter.

### LNC-F16 — Legal, foundation, and product versions cannot silently co-migrate

The hIRC foundation may evolve through governed live revisions. An accepted
licence is a historical legal grant and cannot be changed merely because the
foundation or onboarding changed. Immediate security revocation also does not
settle a contested contractual remedy.

**Required revision:** keep `FoundationVersion`, `CovenantVersion`,
`LicenceTextVersion`, `PriceScheduleVersion`, `EntitlementVersion`, and
`ProductRelease` separately linked. A foundation change can propose future
legal/covenant text; it cannot retroactively alter accepted licence rights.
Safety-critical technical capabilities can be contained under their existing
authority while legal notice, appeal, cure, and final disposition proceed.

### LNC-F17 — Rights chain and dependency compatibility precede publication

Source availability does not grant the author rights to relicense third-party
dependencies or independent contributions. Multiple personal/public-interest/
commercial instruments can also create incompatibilities across forks and
contributions.

**Required revision:** inventory ownership, contributor grants, dependency
licences, patents/trademarks, generated assets, existing releases, and prior
irrevocable grants. Define incoming contribution terms and fork/redistribution
rules with counsel. Build/package outputs must identify exact custom terms and
all third-party notices without implying that a new file revokes past grants.

## Implementation disposition

### Integrate into Master Plan 1.1 and the foundation now

- conduct-based non-domination and reciprocal limits on author, human, agent,
  collective, administrator, and peer;
- individual scoped refusal, deterministic action denial, evidence review,
  voluntary coordination, bounded mandate, safe withdrawal, correction,
  restoration, and portable exit;
- no majority-created truth or authority, no global kill switch, no retaliation,
  no sabotage, no data hostage, and no licence surveillance;
- exact owner fee schedule and per-human unit as blocked product requirements;
- free personal/noncommercial and qualifying public-interest paths as pending
  legal grants;
- neutral voluntary-support experience and privacy boundary;
- versioned data objects, causal/timestamp history, recovery, attention, tests,
  and honest residual limits.

### Implement as specifications and test contracts before application code

- licence/covenant state machine and exact version relationships;
- self-declared classification and offline entitlement candidate with separate
  key lifecycle;
- concern/evidence/disposition/participation/negotiation/restoration objects;
- room/effect privacy contracts and safety-controller interfaces;
- donation preference and reviewed external-navigation contract; and
- the supplied LIC/DON/GOV tests plus certificate, parser, clock, key,
  impersonation, privacy, retaliation, attention, crash, and recovery attacks.

### Hold from product activation

- all final licence texts and claims of enforceability;
- commercial tier classification or billing;
- payment/donation destination;
- paid entitlement issuance, suspension, termination, renewal, or refund;
- final cooperative/research eligibility;
- any remote licensing server, covert telemetry, remote kill switch, destructive
  enforcement, or hidden activity classifier; and
- any claim that technical controls prevent a source/host owner from modifying
  the software.

## Additional adversarial tests

- modified, duplicated, expired, future-dated, revoked, wrong-entity, wrong-seat,
  and wrong-terms entitlement certificates;
- licence-signing key compromise, rotation, loss, and clean-room recovery without
  release/bridge/recovery-key crossover;
- wall-clock rollback, offline expiry, long disconnection, renewal overlap, and
  appeal during provisional suspension;
- several humans behind one service and one human using several devices/agents;
- contractor, guest, administrator, read-only observer, automation owner, and
  departed/reassigned operator cases;
- nonprofit label with prohibited conduct, commercial work through an academic
  intermediary, critical independent research, and for-profit cooperative;
- agent accusation, clone chorus, forged evidence, private-data grievance,
  repeated rewording, retaliatory reassignment, and valid transparent
  reassignment after individual refusal;
- representative mandate fork, expiry, overreach, dissent, withdrawal, and crash;
- safety-critical withdrawal while a physical/process controller is mid-state;
- donation URL substitution, referrer/query leakage, malicious redirect,
  missing configuration, offline mode, decline, opt-out restore, and payment
  provider privacy-change detection; and
- licence expiry/termination with full safe read/export/backup/restore and no
  effect replay or data lockout.

## Decisions requiring owner/counsel evidence

The plan's U-01–U-12 remain open. They are not implementation details an agent
should silently choose. Legal counsel and owner decisions are required before a
published licence, commercial activation, or payment destination. The local
foundation, refusal, safety, privacy, recovery, voluntary-support UI contract,
and test specifications can advance without pretending those decisions are
resolved.

