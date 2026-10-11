# M07 formation and adapter stepping stones

M07 adds permanent participant formation and provider-neutral local interfaces.
It does not create a model participant, authenticate a native caller, grant a
source audience, enable a provider, dispatch an effect or activate the Bridge.

## M07-S001 — permanent formation and scoped admission — PASS (declared local scope)

Project verified participant events into one deterministic formation state:

- only permanent logical identities are accepted;
- native binding, consent, task, requested roles and requested scopes are
  explicit and do not grant themselves;
- source study and demonstrated use are separate gates;
- every required gate carries attributable evidence and is either PASS or HELD;
- readiness is derived from the complete exact gate set rather than asserted;
- admission requires the latest READY assessment, an authority-bound observed
  action, the same task and subsets of requested roles/scopes; and
- information boundaries cannot change during formation.

Acceptance requires positive formation/admission, held-to-ready progression and
adverse cases for temporary identity, missing gates, premature/stale admission,
role/scope escalation, duplicate native binding and audience widening.

## M07-S002 — provider-neutral no-effect adapter — PASS (local fake-provider scope)

Define a local adapter contract and deterministic fake provider that separates
request creation, provider acceptance and observed result. No network/process
edge or credential is allowed.

## M07-S003 — local outbox and uncertain effects — PASS (local no-dispatch scope)

Add an atomic local outbox with idempotency, retry uncertainty, effect-state
separation and recovery. External dispatch remains disabled until later gates.
