# WAYMARK M03-S014 bounded product repair recheck, revision 1

Review ID: HIRC-M03-S014-WAYMARK-RECHECK01
Reviewer: WAYMARK / UI-20261007-A.
Disposition: PASS for F01-F03 at this exact corrected product frame. Full S014 remains open for independent security, privacy-engineering/dataflow and metric/evaluator specialist coverage; no broader assurance follows.

## Frozen frame and preserved history

Revision2 request SHA-256 b298168e18d77424c9d02c4ed6a7b04eecaa9ccde37750ab85c406d476edb04b, commit7c421b70ece04805d4d8fdc3acb65d37aa67d964. Its internal2b8d195 locator identifies the preceding corrected packet. All28 declared input/evidence hashes and sizes independently equal both current files and actual committed Git blob bytes. No representation adapter is needed for revision2.

Original report b80f9923609adc146288658d5a4ab2e7285a262795870257fb66c875c0995f92 and coverage manifest9edd3c9780a13317b0b215b5b0f979724f275ac146c2288351eeccf5202d0646 remain unchanged. Their original failed dispositions and CRLF identity remain history. Controller response0d282502537a899ee9b0e0c4f259441f1afc8f055a490acebfdc5c36844cfe53 was personally read. This is a new repair recheck, not a rewrite or expanded qualification.

## F01 and F02 — PASS

Read the complete repair diff and both current harnesses. Independently tested the actual latest schema via Test-Json and AST-extracted Test-S/Test-Semantics functions only. Main/report-writing bodies were not run. Six source pins were stable before/after.

| Case | Expected | Actual |
|---|---|---|
| Current explicit subscription | accept | schema and semantics accept |
| Declined active subscription | reject | schema and semantics reject |
| Withdrawn active subscription | reject | schema and semantics reject |
| Stale accepted active subscription | reject | schema and semantics reject |
| Legitimate dissent/exit | accept | schema and semantics accept |
| Withdrawn dissent with inactive subscription | accept | schema and semantics accept |
| Current quiet state with inactive subscription | accept | schema and semantics accept |
| Plural presented discovery | accept | schema and semantics accept |
| One permitted source, HELD with reason and no ranking | accept | schema and semantics accept |
| Zero permitted sources, HELD with reason and no ranking | accept | schema and semantics accept |
| HELD without reason | reject | schema and semantics reject |
| HELD with active ranking | reject | semantics rejects held-ranking-active |
| Presented captured one-authority feed | reject | semantics rejects one-authority-feed |
| Direct-source escape removed | reject | schema and semantics reject |

Seven positive and seven adverse controls passed their declared checks. Current-consent errors are active-state-without-current-consent and active-subscription-without-current-consent. The repaired contract keeps valid exit, inactive dissent and quiet operation; honest sparse holds cannot activate a feed. This closes the original synthetic-state findings at the scoped frame, not real consent/accessibility/privacy/runtime behavior.

| Checked source | SHA-256 |
|---|---|
| participation schema | 20429d3d738f42eff025350bf8b74a272168b5fdd1f0e3d39261d18128fe7436 |
| participation cases | 4108f78d4c7e49a4afb83f5c905557d05a50c9f8f6a737fdeee148fecdd21ae1 |
| participation harness | 36990f54aa050d512bc9877600e1776b9b84fcf9e49bfc6cedd0e743ee44751d |
| discovery schema | 425838b632503e10ca2dda83ee6d22eb4bee0f04ccde7a3036975b68f5aa0362 |
| discovery cases | a9377e544c292b8167773abeaffa882641797f468f8ad5cc5dc8df62583b9e6d |
| discovery harness | 77687e0b789ba4080d36cf9fd8c83f8b0b7b6d9842df97a90a15c77cac622bb1 |

The LF-only result-writer change occurred after an earlier recheck; I read it and repeated the14 controls at the final harness pins above. No earlier pin was silently promoted.

## F03 — PASS at corrected scope

Canonical intent JSON is24555 LF bytes, SHA-256 f3c08b9058f96abccec869130d854cae05c598ecbb8e2a2d5965f85fa0c4ef92; Markdown is4156bytes, SHA-256 b9b439d1dfab20af013b8595f713a4dcb07640209dadcb5133c4b6051967a557. Both directly match the committed blobs. Current14-artifact closure hashes/byte sizes are valid; all26 intent rows remain present with no reported unmapped/missing path. The actual project ledger directly binds both intent views and both repaired schemas at their current hashes/sizes. The corrected request binds them without the old CRLF projection.

The original request/coverage remains immutable historical evidence, not relabelled as canonical LF. This check inspected committed blob bytes and declared LF checkout attributes, not a physical fresh clone. Other older ledger-bound working/Git differences remain separately owned publication debt; repository-wide portability and S015 public closure are not claimed.

## Retained coverage and residuals

No new material product/accessibility-requirements/anti-domination/privacy-facing regression was found in this bounded repair. The original broader NO_CHANGE approvals survive at their actual design scope. The role/independence/common-mode limits in the original coverage manifest remain unchanged. No live UI, human consent/accessibility study, cryptographic/privacy/statistical assurance or runtime activation is certified.

LUCENT owns exact registration, response, final source/readable views and specialist coverage. This PASS permits reconciliation of these three findings; it cannot close the remaining S014/M03/full hIRC gates. Reopen on a consequential schema/semantic/source/consumer change or new evidence of an affected regression.
