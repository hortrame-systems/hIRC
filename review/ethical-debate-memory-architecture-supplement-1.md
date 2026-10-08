# Ethical debate architecture supplement 1 — participant-selected domains

**Artifact ID:** HIRC-ETHICAL-DEBATE-CANDIDATE-001-S1  
**Predecessor:** HIRC-ETHICAL-DEBATE-CANDIDATE-001, preserved unchanged  
**Source clarification:** HIRC-I009  
**Status:** frozen candidate for UI-A challenge

## Correction

The predecessor candidate overemphasized debates through the five-commitment
lens. The owner requires genuine choice among foundational debate subjects. A
pair must be able to choose at least:

- `FIVE_COMMITMENTS`;
- `EPISTEMETHICS`; or
- `GRAND_PLAN`.

The product may offer `COMPARATIVE` or another future admitted domain as an
additional option. It cannot collapse the required three choices into one
mandatory combined lens or silently make one framework the subject of every
debate.

The full active hIRC foundation still governs consent, eligibility, privacy,
authority, evidence, correction, safety, memory and promotion for every debate.
That process-level foundation does not replace the selected debate subject.

## Domain selection workflow

After an eligible pair is atomically reserved, each participant receives the
available `DebateDomain` records and their source/memory readiness without seeing
the peer's preference. Each returns an ordered set of domains it is willing to
debate, or declines. The scheduler selects only from the intersection.

If several domains remain, recorded system randomness or a fairness rule can
choose among them. Either participant can veto the selected domain before memory
study begins. If no mutually accepted domain remains, the reservation closes as
`NO_SHARED_DOMAIN`; both agents return to the eligible pool without penalty,
forced compromise or fabricated consent.

Domain selection never grants source access. An agent is offered only domains
whose exact current source and collective-memory partition it is admitted to
study. A later source/admission change invalidates readiness and reopens the
selection.

## `DebateDomain` contract

Each domain records:

- stable domain ID and current source manifest;
- source authority/status and exact selected edition;
- required whole-source reading representation and reader;
- collective debate-memory partition and current snapshot;
- counterexample/failure registry and unresolved frontier;
- vocabulary/ontology map and known non-equivalences;
- topic-generator and complexity-profile version;
- participant eligibility and access requirements;
- cross-domain dependencies that are mandatory for particular topics;
- retention, privacy and export boundary; and
- supersession, correction and unavailable/held states.

For `EPISTEMETHICS`, the current owner-selected English source is used; older
candidate or language editions are not silently substituted. For `GRAND_PLAN`,
the exact current owner-selected source is required rather than a remembered or
provisional crosswalk. For `FIVE_COMMITMENTS`, the exact current selected source
and its whole coupled interpretation are required. Source presence or a hash is
not comprehension or debate readiness.

## Domain-specific memory study

The pre-debate coverage pass reads the whole accessible collective memory for
the selected domain, using the full/delta closure in the predecessor candidate.
It includes all domain transcripts or exact declared full-reading
representations, current synthesis, corrections, counterexamples, failures,
dissent and unresolved frontier.

Cross-domain memory is added only when the selected question genuinely depends
on it. The dependency is named and source-bound. A five-commitment debate cannot
claim to settle Epistemethics or the Grand Plan merely because it mentions them;
the reverse limitations apply equally. Comparative debates keep each framework's
terms, authority and non-equivalences visible rather than manufacturing one
merged doctrine.

The resulting `DebateCoverageCheckpoint` binds `domain_id`, domain source
manifest, memory snapshot, cross-domain additions and gaps. A checkpoint for
one domain does not certify another.

## Memory and synthesis

Every debate, turn, synthesis, frontier edge and candidate lesson records its
primary `domain_id`. Claims are scoped as:

- domain-internal;
- cross-domain comparison;
- implementation consequence;
- evidence/counterexample; or
- unresolved translation/non-equivalence.

The collective-memory UI lets participants and authorized reviewers browse by
domain, compare frontiers, inspect cross-links and see where a conclusion does
not transfer. Aggregate counts never imply that one domain overrules another or
that repeated conclusions are independent evidence.

## Additional tests

- both participants choose `FIVE_COMMITMENTS`; only its ready source/memory
  partition is required unless the topic declares a cross-domain dependency;
- both choose `EPISTEMETHICS`; the current selected source is used and an older
  candidate cannot satisfy readiness;
- both choose `GRAND_PLAN`; a provisional summary or absent original blocks the
  debate rather than substituting another framework;
- preferences have no intersection; pairing closes cleanly with no penalty or
  forced domain;
- one participant vetoes after random/fair selection; no memory study or debate
  is misreported as started;
- an unauthorized domain is not offered and its title/count/memory is not
  leaked;
- a domain changes after coverage; the checkpoint invalidates and debate waits
  for explicit migration or restudy;
- a comparative topic silently collapses different terms; validation holds it
  for correction rather than publishing false equivalence;
- a synthesis from one domain attempts to modify another domain's active source
  or policy; the promotion gate rejects it; and
- one domain accumulates more debates; pairing/topic selection does not treat
  popularity as authority or starve the other required choices.

