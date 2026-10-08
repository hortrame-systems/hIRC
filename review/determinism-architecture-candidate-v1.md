# hIRC determinism architecture candidate 1

**Artifact ID:** HIRC-DETERMINISM-CANDIDATE-001

**Source:** HIRC-I021

**Status:** frozen LUCENT candidate for successor/peer challenge; not implementation

## Rule

Prefer deterministic behavior whenever exact inputs, state and a quality-
preserving contract make it legitimate. Quality, truth, semantic fidelity,
privacy, security, sovereignty, accessibility and recovery outrank determinism,
latency, cost and token reduction.

## Deterministic core

Require deterministic/versioned behavior for:

- source selection manifests, hashes, coverage and semantic diffs;
- canonical parsing/serialization and signed intent envelopes;
- identity/session/generation/epoch and capability checks;
- privacy classification rules that are actually rule-complete, field egress and
  derived-data inheritance;
- lifecycle state machines, idempotency, retry/reconciliation and writer fences;
- policy prohibitions, effect admission, trusted preview digest and journal/outbox;
- work/dependency transitions whose evidence contract is complete;
- resource ceilings, queue invariants and eligibility constraints;
- build inputs, schema/compiler/tool versions, SBOM, release/update selection;
- migrations, backup/restore verification and clean-room reconstruction; and
- tests, fixtures, seeds, expected observations and milestone gates.

The same input/state/version must produce the same local contract result. A
deterministic result is still only as good as its rule and evidence.

## Judgment and stochastic boundary

Ambiguous human intent, ethical consequence, ontology mapping, novel design,
source interpretation, open-world evidence and creative synthesis may require
model/human judgment. Record `JUDGMENT_REQUIRED`, evidence, uncertainty,
alternatives, affected parties and review. The result is a proposal until it
passes deterministic privacy, authority, consent, capability, effect, audit,
release and recovery gates.

LLM/provider output is never called deterministic merely because temperature or
seed controls are requested. Bind exact route/model/version/configuration/input,
record what was sent/accepted/observed and preserve the actual output. Unsupported
controls stay unsupported.

## Auditable randomness

Random pairing, sampling and contest allocation must be fair and resistant to
gaming while allowing later audit. Use a versioned selection algorithm with a
committed/unpredictable entropy event or approved deterministic seed derivation,
bind the eligible set and state, and record the outcome. Replay verifies the
selection without letting participants predict/manipulate it in advance. Random
does not mean independent, qualified, consenting or authorized.

## Quality guard

Do not replace a better contextual decision with a simpler deterministic rule
unless evidence shows the rule preserves required quality. Test:

- false precision and unknown-to-zero conversion;
- biased or incomplete rules and common-mode propagation;
- brittle edge cases and liveness/deadlock;
- security/privacy loss through predictable identifiers or schedules;
- metric gaming/Goodhart effects;
- degraded accessibility/usability or operator burden; and
- deterministic reproduction of a wrong semantic interpretation.

Determinism failures create a held/corrected contract, not an invitation to hide
the rule in model prose.

## Boundary inventory

Every component publishes a `DeterminismDisposition`:

- `DETERMINISTIC` — exact reproducible local rule;
- `DETERMINISTIC_WITH_COMMITTED_ENTROPY` — replayable randomized selection;
- `JUDGMENT_ASSISTED` — contextual proposal plus deterministic effect gate;
- `EXTERNAL_OBSERVED` — outside system outcome reconciled from evidence;
- `NONDETERMINISTIC_BOUNDED` — declared permitted variation and capture; or
- `HELD` — no quality-preserving contract yet.

Each names inputs, state, algorithm/model/provider version, environment,
permitted variation, output evidence, tests and recovery.
