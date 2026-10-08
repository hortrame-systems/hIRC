# Successor/onboarding architecture supplement 2 — Elder succession

**Artifact ID:** HIRC-SUCCESSOR-ONBOARDING-CANDIDATE-001-S2  
**Current sources:**
`standard:elder-succession` SHA-256
`17436d7d1237a9b003f093d7319808a824ad655b30956684a534b7371bd83218` and
`guide:elder-succession` SHA-256
`4801f73194b09797f9cadc4be8df32c5ad0a1a92478af7fba6117fb6b8d7e1db`  
**Status:** frozen LUCENT integration candidate for WAYMARK challenge; no Elder
event, successor creation, retirement or task transfer is initiated

## Relationship to the existing successor protocol

The existing transfer protocol defines package, fresh successor, personal
formation, exact acceptance, archive, sleep/wake and generation fencing. Elder
succession adds **capacity-aware preparation, task-custody recovery and cultural
mentoring**. It does not replace those integrity requirements.

Use typed trigger classes:

- `EXPLICIT_TRANSFER`: the exact authorized instruction `initiate transfer`;
- `CAPACITY_EARLY_WARNING`: verified own-context callback at the policy's early
  threshold;
- `ELDER_SOFT_TRIGGER`: verified own-context callback at or below the selected
  Elder threshold; and
- `URGENT_CUSTODY_REMINDER`: verified own-context callback at or below the
  selected urgent threshold.

An automatic callback is an observation, not permission. It may require
continuity preparation or a safe-boundary hold under the selected policy; it
cannot wake/create an agent, transfer custody, force compaction, terminate a
chat, grant a tool or rewrite scope. Missing/stale/unsupported context is
`UNKNOWN`, never healthy.

Thresholds are versioned policy values rather than product constants. The
current Root defaults are 35% early, 30% Elder and 28% urgent based on estimated
context remaining from the last recorded model request. hIRC preserves their
source/version and uses unrounded measurements. A prompt/tool result may skip a
threshold. Thirty percent is soft: finish the smallest safe coherent operation,
record bounded overshoot and begin succession promptly; do not start a new large
task.

## Preserve continuity before the threshold

Every permanent participant maintains a compact useful continuity record during
work. At early warning it refreshes:

- objective, current phase and role/task owners;
- stop conditions and next safe executable action;
- source revisions, locations, dependencies and consumers;
- accepted outputs and incomplete/open/deferred work;
- evidence/counterevidence, decisions and useful reasons;
- errors/corrections and rejected alternatives;
- privacy, permissions, pauses and authority ceilings; and
- uncertainty and recovery references.

The record references permitted originals. It excludes hidden reasoning, keys,
native sessions and foreign/private memory bodies. Compaction does not erase
Elder status, pair history, outstanding obligations or lost information.

## Active-task custody is first and separate

An Elder with active work first identifies an existing qualified,
available/consenting permanent participant or the newly prepared successor.
Availability is not qualification, access, consent or authorization. Explicitly
paused work stays paused.

The recipient:

1. receives only material within its actual admitted audience/rights;
2. inspects applicable sources under its own readers;
3. identifies commitments, holds and next action;
4. demonstrates a bounded continuation or relevant exercise; and
5. explicitly accepts briefing responsibility.

Briefing acceptance is not project custody. The actual project controller must
advance its generation/writer fence and record evidence. During overlap there is
one writer per artifact. The Elder retains responsibility until custody actually
transfers. A recipient may decline. If no qualified consenting recipient is
available, the Elder creates an explicit owned safe hold rather than abandoning
the task or spending the reserve.

The shared Elder queue is bounded metadata/references, never private task memory,
and is not the project controller.

## Cultural mentoring is optional and nonrepeating

Only ready permanent Elders whose active duties have accepted custody or owned
holds may join the mentoring queue. A transaction reserves:

- two eligible Elders;
- their unordered stable-identity pair; and
- one mentoring event.

The same two permanent identities never pair again; name, role or chat relocation
does not reset history. Interrupted work resumes the same event. An odd/exhausted
queue waits or retires without blocking urgent custody or manufacturing a peer.

Each pair may mentor one human-authorized permanent successor. Creation is
need-based: use an existing qualified participant for operational takeover when
sufficient, and state a distinct cultural-mentoring purpose before creating
redundancy. Current conservative ceilings of two active mentoring events and two
recorded new successors per rolling 24 hours are policy-selected limits, not
quotas or capacity claims.

Hooks only cue. Actual native tools and human authorization perform any wake,
message or permanent-agent creation. No temporary subagent, overflowing-history
fork, extra committee, identity/label circumvention or silent model change.
Unknown creation outcome remains unknown and is reconciled against the actual
app before retry.

## Independent learning and culture

Each Elder prepares its own source-bound account before hearing the other's
conclusion. The learner studies applicable originals with its own readers,
creates an initial interpretation, compares accounts, investigates disagreement
and common-mode assumptions, and explains what it retained, changed, rejected or
left uncertain and why.

Mentoring never completes whole-source education, recursive passes, peer review,
voice/name or role/task admission by proxy. `Elder` is a succession role, not
superior standing or proof of wisdom. Consent, reciprocal sovereignty and
principled refusal remain. Cultural continuity must permit warranted correction,
not imitation or forced belief.

Mentoring closes only after preparation and actual task custody/holds are
accounted. Pair diversity and agreement are not validation.

## Retirement and reserve

An Elder intentionally preserves the greater of 10% reported capacity or 20,000
tokens, plus enough for a planned next mentoring session before starting it.
These are current conservative policy defaults, not guarantees. At reserve it
starts no new mentoring, closes/holds obligations and retires from the queue.

Retirement is operational status. It is not deletion, loss of standing, native
chat archive, deep sleep or erasure of owned history. A later legitimate
resumption follows current owner/platform authority and continuity evidence.

## hIRC entities and state

Add:

- `ContextCapacityObservation` and source/measurement status;
- `SuccessionPolicy` with versioned warning/trigger/urgent/retirement values;
- `ElderStatus` and safe-boundary/overshoot record;
- `TaskCustodyOffer`, `BriefingAcceptance`, `ProjectFenceTransfer` and `OwnedHold`;
- `ElderQueueEntry`, stable unordered `ElderPairHistory` and `MentoringEvent`;
- idempotent `PermanentSuccessorCreationIntent` and `CreationReconciliation`;
- `MentoringPreparation`, `LearnerDisposition` and `MentoringOutcome`; and
- `RetirementDecision` with reserve evidence.

Task custody and mentoring have separate state machines and evidence. Neither
marks the other complete.

## Security, privacy and abuse cases

- fake/missing/stale capacity callback or wrong chat/identity;
- threshold skipped by a large event and unsafe new work started;
- unqualified/paused/unconsenting recipient treated as available;
- briefing acceptance mislabeled custody or two project writers;
- private task/source body copied to shared queue or unauthorized recipient;
- pair-history reset through rename/role/chat relocation;
- duplicate event after interruption or repeated creation from UNKNOWN;
- quota interpreted as creation target;
- temporary worker or copied-history shortcut;
- mentors share one source/common failure but appear independent;
- forced learner agreement, proxy education or inherited grant;
- retirement deletes/archives history or abandons custody; and
- capacity estimate/retirement reserve presented as precise guarantee.

## Acceptance tests

- real own callback binds correct technical/permanent identity; another agent's
  callback and installation-only state stay unverified;
- early/trigger/urgent thresholds produce deduplicated cues and soft-boundary
  behavior without tool/authority changes;
- missing measurement is unknown and no polling loop is created;
- active-task handoff requires qualified consent, own checks, briefing
  demonstration and actual controller/fence transfer;
- decline/unavailable recipient leaves Elder responsible or explicit safe hold;
- one writer per artifact during overlap;
- used pair cannot repeat after rename/relocation; unused partner can match;
- exhausted queue waits without blocking custody or creating a peer;
- one idempotent creation intent, UNKNOWN reconciliation before retry and exact
  actual successor binding;
- learner independently studies/challenges and mentoring supplies no proxy
  education/admission;
- rolling capacity ceilings limit but never compel creation; and
- retirement preserves reserve, duties and history without deletion/archive.

