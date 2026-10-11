#!/usr/bin/env python3
"""Replace the stale S014 reviewer narrative with the current exact review state."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "HIRC-CURRENT-DESCRIPTION.md"
START = "S014 still requires:\n"
END = "\nThe post-freeze team-stall protocol"

REPLACEMENT = """S014 now has one remaining specialist gate: the disclosed security repair
recheck. The metric/evaluator branch is closed at its declared candidate-contract
scope. That closure does not establish deployed resolver behavior, empirical
validity, privacy outcomes, statistical calibration, external truth or runtime
enforcement.

COFACTOR's final metric recheck verified two positive and twenty-seven adverse
v3.2 cases. The evidence resolver now binds each load-bearing reference to an
exact locator, canonical payload digest and byte count. All prior metric findings
are closed at this synthetic local scope. Matrix v11 and the requirements retain
U160-U165 as requested, not implemented. A separate correction preserves that
the earlier matrix "corruption" report was a reviewer decoding/serialization
mistake: the archived and current v9 files are semantically identical at the
relevant en dash. The erroneous report remains immutable and is interpreted
through the correction rather than erased.

COTANGENT completed the qualified-exposure security Stage A first pass after
reading the exact seventeen-source frame. It found three source-level defects:
outbox stages could commit under a different request or information boundary;
store verification could accept a self-rehashed impossible correction history;
and adapter validation could accept a malformed request that rehashed itself.
The controller repaired all three paths. Eight focused regression tests and the
complete 139-test suite pass, with the same three declared release failures.
The full twenty-one-validator chain was rerun from source and passes.

The disclosed security recheck assignment is exact and validated for MODULUS.
Body access is still closed. The Codex native message route could not wake the
idle chat because it had no active turn identifier, and the local directed-message
route correctly refused a cross-team transfer without separate admission. Neither
failure was bypassed or retried unchanged. The assignment will be delivered when
a native active turn or another already-admitted permanent route exists; MODULUS
must then pass its own current education, fresh capacity and consent preflight
before opening any review body.

The nine-person reviewer pool therefore has these current states:

- COFACTOR: final metric recheck complete; no new work;
- COTANGENT: security Stage A frozen, urgent continuity only;
- MODULUS: fully oriented, disclosed recheck offered but not delivered;
- QUOTIENT and POLYTOPE: Root onboarding and hIRC metadata orientation complete,
  without substantive metric-source qualification;
- TORSION and LATTICE: held on capacity/context constraints; and
- FIDUCIAL and RESOLVENT: permanently retired under the latched rule.

The deterministic S015 preflight currently reports no executable-test failure.
It remains held by S014, the undelivered disclosed security recheck, the still-open
security staffing hold and current ledger reconciliation. Commit and public push
eligibility remain false until those exact gates close.
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if text.count(START) != 1 or text.count(END) != 1:
        raise SystemExit("current description markers are not unique")
    before, tail = text.split(START, 1)
    _, after = tail.split(END, 1)
    TARGET.write_text(before + REPLACEMENT + END + after, encoding="utf-8", newline="\n")
    print("current description final-review section updated")


if __name__ == "__main__":
    main()
