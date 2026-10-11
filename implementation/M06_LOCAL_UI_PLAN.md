# M06 local UI stepping stones

M06 turns only verified local projections into a compact human-readable surface.
It does not add a listener, provider, model, external effect or Bridge path.

## M06-S001 — verified read-only snapshot

Generate one self-contained HTML file from one atomic verified store snapshot.
The file exposes:

- Back, Forward and deterministic Resume controls;
- a keyboard-labelled search field;
- work, status, next action, dependencies, holds and source-event references;
- information-boundary labels on every work item;
- a roster derived from explicit owners; and
- a visible statement that the surface is read-only and local.

All untrusted text is HTML-escaped. JavaScript uses text and attributes already
rendered by the trusted generator; it never uses `innerHTML`, `eval`, remote
resources, inline event handlers or a network API. A restrictive hash-bound CSP
permits only the exact embedded style and navigation/search script. Output is
written atomically.

Acceptance requires deterministic output, hostile markup remaining inert,
accessible controls/landmarks, a CLI end-to-end fixture, the complete regression
suite, and reconciled ledger pins.

## M06-S002 — interruption preview — PASS (deterministic no-effect scope)

Add the four interruption choices as an explicit local preview state with safe-
boundary explanation and deterministic queue semantics. This stone will not
execute, schedule or persist the new task until the local event contract and
recovery tests exist.

## M06-S003 — refusal, correction and trusted preview — PASS (deterministic no-effect scope)

Add inspectable refusal/correction flows and a trusted consequential preview that
binds exact intent without enabling an external effect. Accessibility and hostile
UI-state tests remain acceptance gates.

The local preview object is content-addressed and semantically revalidated. It
separates participation from effect disposition, requires authority for an
allowed action, preserves correction boundaries, rejects unknown fields and
self-consistent semantic forgeries, and keeps approval/persistence/effect flags
false. Browser-engine interaction remains held at the existing local-file policy
boundary; M07 may proceed independently while that empirical M06 gate stays open.

## Deferred M06 evidence

Browser-engine behavior, screen-reader traversal, zoom/reflow, forced colors,
pointer targets and human usability require rendered empirical checks. Static
source checks do not pass those gates.
