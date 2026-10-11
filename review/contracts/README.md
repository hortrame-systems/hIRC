# Candidate foundation and continuity contracts

These schemas make two load-bearing Master Plan 1.1 proposals reviewable:

- `hirc-onboarding-source-set.candidate.schema.json` describes the exact,
  context-qualified source graph and unit-level dispositions used to compile
  foundation, formation, interface, test and governance contracts.
- `hirc-transfer-case.candidate.schema.json` describes generation-fenced
  successor state, evidence and observed lifecycle effects.
- `hirc-request-case.candidate.schema.json` separates interpreted intent,
  reliance, participation, authority and action disposition, including the
  narrow proceed-after-pushback path.
- `hirc-bayesian-reliance.candidate.schema.json` records scoped posterior
  lineage, evidence dependence, metric/evaluator governance and the prohibition
  on direct permission effects.
- `hirc-cooperative-competition-charter.candidate.schema.json` fixes consent,
  rules, budgets, evaluation, fairness, prohibited conduct, appeal, credit and
  learning boundaries before a contest can run.
- `hirc-release-profile.candidate.schema.json` distinguishes the exact enabled
  software profile from the plan edition and full target, including genuine
  disabled capability evidence.
- `hirc-bridge-gate.candidate.schema.json` encodes noncircular stage-6 pilot and
  stage-7 broader-activation prerequisites.
- `hirc-cultural-artifact.candidate.schema.json` represents source/audience/
  privacy-bound cultural artifact references, append-only provenance, preserved
  dissent, non-destructive correction/supersession, zero cultural authority
  effects and recoverability without embedding protected real bodies.
- `hirc-discovery-decision.candidate.schema.json` represents plural candidate
  routes, disclosed policy/version and rationale, exclusions and uncertainty,
  bounded variation, original/dissent reachability and direct source-bound
  retrieval without engagement, agreement or authority effects.

They are candidate design contracts. Schema validity does not establish correct
source interpretation, personal education, permission, security, privacy,
consent, statistical/metric validity, successful external effects or peer consensus. Protected source bodies,
credentials and hidden reasoning are intentionally outside these records.

`../fixtures/cultural-artifact-contract-validation-v1.json` records two accepted
synthetic controls and rejects protected-source leakage, provenance stripping,
dissent erasure, destructive correction and authority coupling. The semantic
harness supplements structural JSON Schema checks; neither establishes real
privacy enforcement, consent, cultural benefit or runtime behavior.

`../fixtures/discovery-decision-contract-validation-v1.json` accepts plural
deterministic and replayable bounded-random controls and rejects a one-authority
feed, opaque ranking, engagement optimization, suppressed minority access,
randomness-as-independence and removal of direct-source escape.

`hirc-cultural-participation.candidate.schema.json` and its synthetic validation
cover visible reversible defaults/subscriptions, voluntary dissent and exit,
preserved standing/resource floors and valid transition history. Dark defaults,
hidden subscriptions, exit penalties, conformity access, retaliation and invalid
transitions are rejected.

The integrated M03-S014 product review exposed and repaired two state-model gaps.
Active subscription and joined/subscribed/quiet states now require current explicit
consent; declined, withdrawn or stale consent cannot remain actively subscribed.
Discovery now represents zero/single-permitted-source scarcity as an honest `HELD`
state with a reason and no active ranking, while successful/non-held discovery
still requires plural candidates and a result. Synthetic controls preserve current
subscription, dissent/exit, plural discovery and sparse holds while rejecting the
reviewed failure cases. These checks do not prove real consent, accessibility,
privacy enforcement, recommendation quality or runtime revocation latency.

`validation-result.json` records five positive and three adverse fixture checks
using PowerShell `Test-Json` 7.0.0.0. See `validation-notes.md` for scope and the
repaired runner-setup failure. This is structural schema behavior only.

The original request/reliance/competition schemas are frozen v1 counterexamples.
WAYMARK's seven adverse variants all passed their structural schemas. Current v2
candidates add cross-record activation constraints and explicit governance:

- `hirc-request-case.candidate.schema.v2.json`;
- `hirc-bayesian-reliance.candidate.schema.v2.json`; and
- `hirc-cooperative-competition-charter.candidate.schema.v2.json`.

`../fixtures/waymark-trust-contract-validation-v1.json` preserves the v1 gap;
`../fixtures/waymark-trust-contract-validation-v2.json` records four accepted
controls and seven rejected adverse variants after v2 adaptation. Runtime truth
and reference closure remain separate.

`../fixtures/waymark-trust-contract-validation-v2.1.json` repairs the target
trace with exact v2 paths/hashes, adapted-input hashes, retained harness identity,
PowerShell/runtime and validator-module identity. It is the current bounded
historical product-review fixture result for its pinned v2 revision.

The controller's M03-S014 preliminary security repair R001 strengthens the request
v2 candidate again. Effect records now bind target, capability, principal,
session, generation, execution epoch, idempotency key and trusted preview digest.
Schema conditions reject stale/failed authority with `PROCEED`, declined
participation with effectful dispositions, performed work without an effect,
contradictory requested/sent/accepted/observed states and more than one selected
interpretation. Request and performed-effect records also bind a canonical privacy
snapshot, so an in-record audience or purpose change without the matching snapshot
update is rejected. Resolving that snapshot against the trusted prior preview is
an external gate; co-editing both the record and its digest is not authorization.
`../fixtures/security-request-state-validation-v1.json` records three valid
controls, eleven rejected security/privacy mutations and the four historical
WAYMARK request cases at their expected valid/adverse dispositions. This is a
controller repair; runtime dispatch and qualified whole-packet review remain open.

Security repair R002 strengthens the Bridge staged-gate candidate. A stage marked
`PASS` now requires nonempty evidence; stage-6 authorization/in-progress/pass
requires explicit entry authority and stop conditions; stage-7 authorization/
in-progress/pass requires its decision. The paired deterministic validator also
enforces a monotonic passed prefix and rejects future-stage advancement hidden
behind an earlier current or held stage. Three valid histories pass and five
evidence/order/authorization bypasses fail. This remains design-state evidence,
not protocol implementation, hostile-lab evidence or Bridge activation.

Security repair R003 strengthens the release-profile candidate. It binds exact
build, environment, release authority and assurance profile identities; declares
the required control/test coverage; requires release evidence and an observed
release for `RELEASED`; and makes disabled listener, scheduler, credential and
grant absence true at release. The deterministic companion rejects empty or
all-N/A assurance, coverage mismatch, enabled/disabled overlap and unobserved
release. Per-capability evidence, exact assurance-set hashes, strict relative
timestamps, subject binding and nonempty disabled-capability absence evidence are
required. Four valid profiles pass, including enabled-only and disabled-only
profiles, and seventeen adverse variants fail. The single-sided controls close a
reviewer-found null-array execution defect. Deployment, external resolver truth,
runtime assurance and release authorization remain open; the corrected-frame peer
recheck is tracked separately.

Security repair R004 strengthens the transfer candidate after ORDINAL's exact
read-only specification review. Accepted states require accepted disposition,
valid packages and passed forbidden-content scans; confirmed archive/sleep require
provider acceptance plus observed confirmation and evidence; tracker closure
requires applied CAS while post-archive conflict preserves a valid accepted/
archived record. Trigger and wake records now bind scope, expiry, revocation epoch
and idempotency. Deterministic relations additionally reject generation/session/
epoch, recipient, manifest, archive/sleep target and time-order mismatches. Five
valid lifecycle controls pass and twelve adverse variants fail. Native platform
effects and actual custody remain outside this evidence.

Security repair R005 requires request and transfer records to carry explicit
data classes, audiences, purpose, consent snapshot/currentness, retention,
derived-data, egress and deletion-residual bindings. Effect records bind the exact
privacy snapshot; transfer packages additionally require recipient-bound encryption
profiles. Transfer packages bind both source and current canonical privacy
snapshots and a typed relation for audience, purpose, data class, consent,
retention, derived data, egress, encryption and deletion residuals. Four valid
controls pass, including legitimate audience attenuation, and fifteen widening or
loss variants fail. These checks establish local relation and binding behavior,
not trusted source-snapshot resolution, real consent, cryptographic protection,
deletion effectiveness or privacy certification. A co-edited source snapshot and
digest therefore remains invalid until the external resolver admits it. The
corrected-frame peer recheck remains open.
