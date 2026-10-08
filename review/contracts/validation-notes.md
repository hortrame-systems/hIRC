# Candidate contract validation notes

The first validation-runner attempt stopped before adverse schema evaluation
because its PowerShell object mutation tried to assign an absent
`low_consequence` property directly. This was a runner-fixture setup error, not a
schema pass or failure. The runner was corrected to add the property explicitly
and the complete suite was rerun.

The completed run passed:

- five positive fixtures: onboarding source set, transfer case, request case,
  Bayesian reliance and cooperative-competition charter;
- request `PROCEED_AFTER_PUSHBACK` with a failed low-consequence boundary was
  rejected;
- Bayesian posterior with a direct authority/permission effect was rejected;
  and
- competition charter permitting rank-to-permission conversion was rejected.

Validator: PowerShell `Test-Json` 7.0.0.0. This establishes only structural JSON
Schema behavior for the declared fixtures. It does not establish semantic
correctness, source completeness, statistical validity, privacy, security,
usability, implementation conformance or peer consensus.

