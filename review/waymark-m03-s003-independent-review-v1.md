# WAYMARK independent M03-S003 review, revision 1

Review ID: HIRC-M03-S003-WAYMARK-R01
Reviewer: WAYMARK / UI-20261007-A, permanent Product/Interaction participant.
Disposition: CHANGES_REQUIRED for the matrix integration validator. Source-first review complete at the original frozen frame; S003 PASS and controller integration remain pending.

## Exact scope and independence

U186-U191 and DTM-001-DTM-005, under the seven questions of m03-s003-independent-review-request-v1.md (SHA-256 e4203a763a544b32b5b4b66ed704d8e86e417f7aba3ab8c9825c348818dac70c), commit 7b69aa2129ee466901de3cde9043948345e65ba5. All11 input hashes/byte sizes were independently verified before analysis, then verified against the immutable Git frame before report creation. The integrator working copy changed after the finding was sent; that repair is a new frame and is not approved by this original report.

I personally completed the current education/recovery checks and consented to this new bounded design/requirements security and semantic review. The basis is my own source-plan education, genuine permanent-peer education review, interpretation and adverse-check work. This is not a penetration test, live runtime audit, cryptographic certification or scientific review qualification. I did not author these rows. Prior generic deterministic-default framing, observer reports and early-review-gate correction are disclosed; the review is not blinded or statistically independent. No retirement label, old receipt or proxy substitutes for the actual review. Generation2 retains custody and the integration writer.

## Finding HIRC-S003-WM-F01

Severity: MEDIUM. Status: SUBSTANTIATED.

Target: review/integrate_determinism_decisions_matrix.py:34-36, build() and its mechanical source-coverage claim.

Dictionary comprehensions collapse duplicate IDs before set-coverage checks. An earlier conflicting U188 or DTM-002 row is discarded by a later row with the same ID; validation still reports pass=true/errors=[]. Final set equality/counts cannot detect the lost meaning.

I exercised the actual build function on three in-memory source fixtures, inserting the conflicting row immediately before its unchanged counterpart. Each source object's read_text()/read_bytes() supplied the same mutated UTF-8 bytes. main() was never called and no packet file was written.

| Adverse case | Mutation | Result | Mutated input SHA-256 |
|---|---|---|---|
| duplicate_requirements_source | Earlier U188 acceptance=MUTANT_REMOVES_AUTHORITY_GATE in generated requirements | pass=true; errors=[] | 07a77e873fdeab16e5fa1f166dd940b045873a97b55205709572a32a98190b40 |
| duplicate_map_requirement | Earlier U188 acceptance=MUTANT_REMOVES_AUTHORITY_GATE in map | pass=true; errors=[] | 5bd9965c67bf130b76a3364f598913730f9a3de3413e4ad92288d54d307922d5 |
| duplicate_map_decision | Earlier DTM-002 change=MUTANT_MODEL_SUPPLIES_EFFECT_AUTHORITY in map | pass=true; errors=[] | 8fbae7617e4d5df719e3244a4c206a657cdb7047bee567664a2e9873e2934de8 |
| changed_map_acceptance | Change sole U188 map acceptance | pass=false; requirement-map-mismatch:U188:acceptance | 986efb3fc693653da9223b116a7aca42723c882faf701eadb0fdc7e88fd1596f |

The last case is a discriminating control: the source-consistency check was reached. Fixtures use deep copies serialized by json.dumps(data,ensure_ascii=False,indent=2) plus one newline, UTF-8. The duplicate-requirements case reserializes the otherwise unchanged map to SHA-256 f362cc0a19be9b1097e428fb80b8c70da55f5356b6d8045251949263d6571af0.

Consequence: the validator cannot support an unqualified unique/exact source-coverage claim. A later conflicting source can lose meaning without explicit reconciliation. This does not establish corruption of the actual frozen matrix: its target rows are unique and replay correctly.

Required repair: validate multiplicity before dictionary construction; reject both conflicting and identical duplicate identities in each authoritative input collection. Retain target-set and mismatch controls. Add all three adverse cases and a unique-input positive control. Preserve the failed frame and bind a separately attributable corrected validator/test report. LUCENT owns repair/integration. Hold S003 acceptance until the scoped repair checks and corrected-frame comparison pass.

Residual: this verifies bounded input integrity, not source authentication, semantic truth, consent, anti-gaming or runtime authority. Reopen on a changed parser/source/consumer that reintroduces silent coalescing.

## Warranted approvals and explicit NO_CHANGE

1. U186/U187/DTM-001: NO_CHANGE. Quality comes first; dispositions preserve genuine judgment, unknown external outcomes and permitted variation. Reproducibility is not truth. Accessibility survives in the governing rule and U191.
2. U188/DTM-002: NO_CHANGE. Stochastic output remains a proposal, with deterministic current-state privacy/authority/consent/capability/effect/journal/release/recovery gates. Seed/temperature settings do not certify provider determinism. Future effects must actually enforce the gates atomically.
3. U189/DTM-003: NO_CHANGE at requirement/design-intake scope. Eligibility, replay, qualification, consent, independence and authority remain separate. No anti-gaming implementation/proof is supplied. Before implementation acceptance, require frozen eligible-set/algorithm/state commitment before entropy is knowable, a justified unpredictable source, verification/reveal ordering and an abort/retry rule preventing selective resampling. A publicly predictable deterministic seed cannot meet the stated requirement. Replay must retain only minimum permitted eligibility references/commitments; no public participant dossier follows. Withheld entropy/withdrawal is a liveness dependency, not consent to coerced participation.
4. U190/U191/DTM-004/DTM-005: NO_CHANGE. Semantic errors, rollback/recovery limits, common mode, liveness, Goodhart, accessibility/usability and operator burden remain visible. Actual recovery and quality tests are still required. Fixed test entropy must not become reused production cryptographic secrets/nonces. These are retained implementation constraints, not passed runtime checks.
5. Predecessor preservation: independently compared all80 prior matrix requirement objects and139 decision objects including statuses and peer evidence; each is equal in order/content. Other fields are unchanged except the declared new ID/status/source-map/new rows and the explanatory reason of HOLD-S003-EARLY-REVIEW. Price/cultural holds are unchanged. This is object identity, not byte equality of a reformatted whole file.
6. Pending labels: NO_CHANGE. All11 added rows are authored candidates pending independent review. Joint rationale is absent; S003 hold remains OPEN. Requirements are REQUESTED_NOT_IMPLEMENTED; completion rules still require impact/dependency/test/peer closure. The historical S002 validation binds older generator/output bytes and alone cannot validate the later whole pair; this review separately replayed the current pair.
7. One integrated lens: revalidated the preceding holistic understanding against actual evidence, affected parties, shared premises, authority and dependencies. Keep evidence/inference/permission distinct, preserve reciprocal consent and consequential dissent, protect privacy/recovery/usability together, and correct only consequence-bearing failures. This changes the validator acceptance decision and supports unaffected semantics. No criticism quota, private reasoning disclosure or certainty claim.

## Actual reading/replay and limits

Personally read the complete request, architecture, determinism addendum, both producer scripts, both validation records and stepping-stone protocol; inspected HIRC-I021 and exact target rows in the large registers. No whole reread of unrelated requirements or full master plan is claimed.

Executed actual requirements build() read-only: full returned object equals the pinned current requirements; render() equals the readable Markdown pair. Executed actual matrix build() read-only: full returned object equals pinned v7 and positive validation passes. Independently checked predecessor objects/metadata/holds and four fixtures above. These are bounded replays, not independent implementations of every generator or runtime security evidence. No authored packet bytes were edited by this reviewer.

One substantiated finding and unaffected candidate approvals are frozen here. Controller response/integration, later full product/security/privacy challenge, other holds, runtime build and milestone closure remain separate.

## Original frozen input manifest

| Path | SHA-256 | Bytes |
|---|---|---:|
| intent-register.json | 3da344b6a834fe26acdcbbb2f86ca4104ff0e4f0769cfaac6aa0ce24297d2477 | 66060 |
| review/determinism-architecture-candidate-v1.md | a32ba3d42438a04c8ffad990a8840826a56e49213857e772220cb9b63fd22321 | 3991 |
| review/revision-map-addendum-determinism-v1.json | 3a35f35ad986fd6f1e1f8d9f42cf82b5770ae2647f3ac78ad6bc670b8f0b2a0b | 4038 |
| review/build_requirements_v1_1.py | 69cefaf12499f8e408ad0af9967bce0d07603f4924fddef2541aa6fd2dcec302 | 11777 |
| drafts/hirc_requirements_v1_1-draft.json | 985f0b77a91a83cb5da3b895f44218368a4d28e957c5b716466ea18402e26f69 | 260630 |
| review/fixtures/determinism-requirements-validation.json | ef450bc4987a5dc1b744edb95ca8387ee8d7966b4f89c86be42f21cb0b52975b | 3061 |
| review/integrate_determinism_decisions_matrix.py | 8131faf2a7145ddd8496285d7514665df8651310dcdd6df568b170bfa9cd44a0 | 7745 |
| review/joint-consensus-matrix-draft-v6.json | dc788b19c113d295b18227a8cb801a48d8b377d245cf41e8b3a8eeebbec9e3f7 | 157025 |
| review/joint-consensus-matrix-draft-v7.json | fa74cd1c6250568664e810b24edf7d2c68fec260974e71cb8dbfc705019a40f1 | 166186 |
| review/fixtures/determinism-matrix-integration-validation-v1.json | b7009c3680ab724ca0844adb96a0fc19b6070cf6f6a9df36a71ce91619439345 | 1344 |
| drafts/hirc_stepping_stone_protocol_v0_1-draft.md | 23a489be7749df19aa733679574cef940ea016426668c68337e0affcc5abd6ad | 2669 |

The controller links this immutable review, response, repair evidence and final readable matrix through the existing project ledger. Saving this report does not declare that integration complete.
