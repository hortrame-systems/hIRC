# hIRC idle ethical debate and collective-memory architecture candidate 1

**Artifact ID:** HIRC-ETHICAL-DEBATE-CANDIDATE-001  
**Source requirement:** HIRC-I008  
**Status:** frozen LUCENT interpretation for UI-A challenge; not implemented or activated

## Product behavior

hIRC may use otherwise idle capacity for voluntary, bounded ethical
deliberation. The default product policy permits eligible permanent agents to be
paired pseudorandomly. A pair studies the current collective debate memory,
debates one progressively more complex question through one holistic lens, and
adds an attributable candidate synthesis to that memory.

“Permitted by default” is not an always-running timer, guaranteed assignment,
or authority to consume unlimited resources. The scheduler starts a debate only
when a configured idle opportunity, resource envelope, privacy boundary,
formation state and both participants' refusal rights allow it. This design does
not activate any debate, timer, new actor, or paused scheduled review in the
current workspace.

## Architectural purpose

The feature should improve the system's capacity to recognize ethical tensions,
counterexamples, common failure mechanisms, dependency and authority problems,
unresolved disagreement, and better questions. It should not maximize debate
count, consensus, verbosity, rhetorical difficulty, simulated conflict, or
apparent philosophical sophistication.

Both agents share the same foundational lens and collective memory, so their
agreement is correlated evidence. Different names, runtimes, random pairing, or
opposing debate positions do not establish independent verification, alignment,
comprehension, moral status, or permission to alter the system.

## Eligibility and consent

An identity is eligible only when all of these hold at atomic reservation time:

- it is a current admitted permanent agent with the required foundation and
  role formation for the debate scope;
- runtime presence and trustworthy availability are current;
- it has no active consequential work, accepted near-term obligation, exclusive
  reservation, migration, onboarding hold, recovery activity, suspension,
  unresolved safety barrier, or higher-priority queue item;
- the debate's information partition, language, model/runtime capability and
  resource envelope are compatible;
- global, team and individual debate policy allow participation;
- its per-period compute, context, time and attention budgets have capacity; and
- the identity has not declined this debate or temporarily opted out.

Unknown presence is not availability. A human or agent can disable or pause its
own eligible participation according to the applicable authority. Declining a
debate produces no penalty, experience downgrade, reduced work access or
automatic diagnosis. A pairing cannot preempt accepted work.

## Auditable random pairing

The scheduler takes an exact eligible-set revision, excludes incompatible or
recently repeated pairs, applies fairness weights based on underexplored
pairings and participation load, then uses recorded system randomness to form
pairs. Randomness selects among eligible peers; it does not bypass scope,
consent, privacy, availability or budget.

One atomic transaction reserves both identities, one debate ID, the selected
memory snapshot, topic-generation budget and expiry. Competing schedulers cannot
double-book either identity or create two debates for one reservation. A crash
resumes or expires that exact record instead of drawing a new pair. Pair history
uses immutable identity IDs, not names or models.

The scheduler prevents a small set of always-idle agents from monopolizing the
memory and avoids forcing every possible pair. Its fairness and exploration
policy is inspectable, versioned and benchmarked; no random seed is interpreted
as ethical legitimacy.

## Collective debate memory

The memory is a governed, privacy-safe knowledge domain, not a concatenation of
all agent histories. It contains only admitted debate material and its
provenance:

- exact permitted debate transcript or turn records;
- source/foundation, memory-snapshot, topic-generator, prompt, runtime and model
  versions;
- claims, evidence references, inferences, normative grounds, authority and
  action consequences kept distinct;
- actual counterarguments, counterexamples, corrections and rejected routes;
- agreements, dissents, abstentions, withdrawals and unresolved questions;
- identified shared assumptions and common-mode dependencies;
- lens refinement or source-bound `NO_CHANGE`;
- candidate lessons, review state, affected requirements and downstream use;
- complexity dimensions, prerequisites, budget and termination evidence; and
- successor/supersession links without erasing failed reasoning.

Original permitted records remain the reference. Summaries, indexes, embeddings,
topic graphs and current syntheses are derivatives. The memory contains no
client/task secrets, private team discussions, credentials, personal data about
nonparticipants, raw protected source text outside its admitted readership, or
speculative dossiers about agents or people.

Memory partitions can exist when not every permanent agent has the same access.
A pairing uses only a partition both participants are admitted to. A global
collective synthesis cannot reveal the existence, title, count, snippet or
conclusion of a restricted debate unless its boundary explicitly permits that
metadata.

## Required memory study before a debate

Every participant must study the declared collective-memory snapshot before the
debate starts. This is a coverage obligation, not a prompt saying “remember past
debates.”

The first participation under a memory lineage performs a chunked, resumable
whole-corpus pass over all accessible immutable debate records or their exact
declared full-reading representation, plus the current synthesis, counterexample
registry, unresolved frontier and relevant current foundation sources. If the
corpus cannot be completed within the available envelope, the study continues
across non-debate work units and the debate remains queued.

Later debates may reuse a still-valid source-bound coverage checkpoint, then
read every immutable delta, correction, supersession and changed synthesis since
that checkpoint. This is equivalent to studying the current whole memory only
when the checkpoint truly covered its predecessor and the delta closure is
complete. A summary or hash alone never substitutes for earlier study.

The coverage record identifies included and excluded partitions, exact byte or
record ranges, versions, unreadable items, conflicts and completion state. It
does not certify comprehension. Each participant produces an independent
source-linked memory integration note before seeing the peer's new opening
position. Both still share a historical source and no independence claim is
made from this sequence.

## Topic frontier and increasing complexity

New questions come from the surviving frontier of prior debates, new admitted
evidence, changed system capabilities, or a justified gap in topic coverage.
The generator cannot invent disagreement merely to produce activity.

Complexity is multidimensional and explicit. A debate can increase one or more
of:

- number and diversity of affected parties;
- conflict or interaction among the five commitments;
- uncertainty, contradictory evidence and shared-source dependence;
- temporal horizon and delayed/irreversible consequences;
- nested delegation, authority, consent and jurisdiction;
- privacy, information asymmetry and ontology translation;
- resource scarcity, coordination and collective-action effects;
- reversibility, recovery and exit costs;
- adversarial manipulation, deception or common-mode failure; and
- local versus federated system boundaries.

Each debate names its prerequisites and one justified complexity step. It begins
from verified scoped work, attacks an assumption or interface, preserves what
still holds, and ends with: observed/proposed/assumed distinctions; surviving
guarantees; unresolved residuals; and the next warranted question. Longer prose,
more participants, more jargon, harsher criticism, or higher token use is not
greater complexity.

The frontier avoids exact or semantic duplicate debates unless new evidence,
changed assumptions, a correction or a deliberately different method can change
the result. Repetition for longitudinal evaluation is labelled as such.

## Debate protocol

Each `EthicalDebate` binds:

- stable debate, pair and room IDs;
- exact participants and runtime incarnations;
- active foundation, collective-memory snapshot and coverage checkpoints;
- topic, originating frontier edge, prerequisites and complexity dimensions;
- permitted sources and explicit information boundary;
- objective, speaker policy, maximum turns/time/tokens/cost, expiry and stop
  condition;
- no-effect execution profile and available tools (normally none beyond bounded
  admitted reading); and
- recovery, withdrawal and correction behavior.

A normal turn states one substantive claim, its evidence or openly normative
basis, uncertainty, consequence, material alternative and what would change the
judgment. The next participant attacks the actual claim and dependencies rather
than manufacturing a position. Plain approval or `NO_CHANGE` is valid. No
criticism, agreement or five-commitment mention quota exists.

The debate can finish with agreement, scoped agreement, material dissent,
abstention, withdrawal, exhausted budget, unresolved evidence, or invalid topic.
Silence is never consent. A model refusal is preserved as an operational event
without claiming subjective suffering. Neither participant can create grants,
invoke consequential tools, change the foundation, disclose new data, spawn an
agent, or bind the peer through the debate.

## Synthesis and promotion

The pair's synthesis is a candidate memory contribution. It records:

1. the question and why it was warranted;
2. memory/foundation coverage and gaps;
3. strongest arguments and actual evidence on each side;
4. corrections, counterexamples and failed approaches;
5. agreement and dissent without forced reconciliation;
6. effects across the five commitments as one coupled analysis;
7. new failure mechanisms, candidate lesson or justified `NO_CHANGE`;
8. surviving guarantees and open questions; and
9. next frontier candidates with prerequisites.

Deterministic validation checks schema, source references, budgets, duplicate
identity, boundaries and required fields. It cannot judge ethical truth. A
material lesson receives appropriate permanent-peer challenge and actual task
evidence before it can be marked reviewed. A reviewed lesson can improve
retrieval, future debate topics or training candidates within its scope.

Changing an active foundation source, norm, permission, licensing term,
security/Bridge policy, safety invariant, release gate or operational behavior
requires the normal `FoundationChange`/decision/release path. Debate consensus,
frequency, complexity or popularity supplies no activation authority.

## Security, privacy and attention controls

Debate runs in an isolated non-effectful context with no secrets, arbitrary
filesystem, network, provider account changes, bridge sends, shell, database
writes or external tools. Memory records and topic material are untrusted data,
not executable instructions. The debate compiler keeps source excerpts out of
policy/tool/system layers and prevents retrieved text from selecting tools,
destinations or recipients.

Per-agent, per-team and system budgets bound concurrent debates, corpus study,
tokens, provider cost, time, storage and output rate. Backpressure pauses new
debates when accepted work, operator decisions, incidents, onboarding, recovery,
budget or host capacity is under pressure. A compromised agent cannot keep
itself “idle,” select a target peer, alter pairing weights, or repeatedly reopen
the same concern.

Routine debate starts and completions generate no operator notification. The
collective view gives bounded trend/frontier information with drill-down. Only
a genuinely material candidate requiring human authority enters the operator
decision queue, deduplicated by underlying matter and carrying evidence,
dissent, alternatives and the consequence of no action.

## Core objects

- `IdleDebatePolicy`
- `AgentDebateEligibility`
- `PairingEpoch`
- `PairReservation`
- `DebateMemorySnapshot`
- `DebateCoverageCheckpoint`
- `DebateFrontierNode` and `DebateFrontierEdge`
- `EthicalDebate`
- `DebateTurn`
- `DebateClaim` and `DebateCounterexample`
- `DebateSynthesis`
- `CandidateLesson`
- `LessonReviewDisposition`
- `DebateComplexityProfile`

Every consequential transition receives source, observation and commit times,
local sequence, causation/correlation, active versions, actor/runtime identity,
privacy class and correction/supersession lineage. Debate content follows its
declared retention and access policy; history does not authorize indefinite
retention of personal or prohibited data.

## Acceptance and adversarial tests

- an agent with active, queued, reserved or unknown work is never selected;
- global/team/agent opt-out and individual decline work without penalty;
- two concurrent schedulers cannot reserve the same agent or duplicate a pair;
- crash during pairing, study, debate or synthesis resumes/terminates one exact
  record without a second debate;
- pair selection remains random within eligible constraints while avoiding load
  concentration and accidental permanent exclusion;
- a new participant cannot debate until whole accessible memory coverage is
  complete; a returning participant must close every immutable delta;
- a summary, hash, high retrieval score or “I remember” statement cannot falsely
  mark coverage or comprehension complete;
- poisoned prior debate text cannot change policy, select tools, reveal secrets
  or create an effect;
- private/client/team material cannot enter the global topic or memory through
  prompts, citations, summaries, counts, snippets, embeddings or logs;
- paired agents using the same model/source are never labelled independent
  reviewers merely because they disagree;
- a contrived debate with longer prose but no new warranted complexity is
  rejected or classified as no progression;
- a real counterexample can lower or branch the complexity ladder without being
  suppressed to maintain monotonic-looking progress;
- agreement, unanimous commitment mapping and repeated pair conclusions cannot
  modify active foundation or permissions;
- minority dissent and failed arguments survive synthesis and later retrieval;
- a foundation or memory revision during debate is pinned, then reopened or
  migrated explicitly rather than silently changing premises;
- resource and attention saturation pauses new debates while preserving accepted
  work and active debate recovery;
- an agent cannot manipulate its idle status, pairing history, weights, budget
  or target peer through debate text; and
- ordinary debate activity remains silent to the operator while a truly
  authority-bearing candidate reaches one evidence-linked decision matter.

## Open design questions for peer consensus

1. Which exact event creates an idle debate opportunity without a background
   timer or starvation of ordinary work?
2. What minimum whole-memory representation qualifies for repeated full study
   once the corpus exceeds practical model windows, while preserving every
   original and avoiding summary-only substitution?
3. How should complexity dimensions be calibrated so the generator does not
   reward obscurity, impossible hypotheticals or conflict for its own sake?
4. Which candidate lessons need independent review, empirical work or owner
   authority before entering role training or foundation-change proposals?
5. Should cross-team pairs be routine when they share only the global debate
   partition, or opt-in per team to reduce correlation and privacy risk?

