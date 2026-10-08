# LUCENT WST response supplement 1 — exact v2 validation trace

**Artifact ID:** HIRC-LUCENT-WST-RESPONSE-001-S1  
**Corrects evidence grade for:** `waymark-trust-contract-validation-v2.json`  
**Status:** bounded trace repair; no broader rerun or runtime assurance

The first v2 result reported the intended v2 execution but retained only the
fixture file's v1 schema-binding block. That was insufficient to verify the
actual target frame independently. The original result is preserved.

The exact same eleven WAYMARK cases were rerun once. Result
`waymark-trust-contract-validation-v2.1.json` records:

- fixture SHA-256
  `2f361a190ffe1ad2de435d9165d07b5d5cfd9842e2778e65ca3c98886d3311ae`;
- executed v2 request, reliance and competition paths and full hashes;
- exact adapted-input SHA-256 for every case;
- hash-bound adapter/harness SHA-256
  `000771021f331a019003da8172e2c6d2f072a826e1965d6ca2b7e4a43526509b`;
- PowerShell Core 7.6.5 on Win32NT / Windows 10.0.26200;
- `Test-Json` from `Microsoft.PowerShell.Utility` 7.0.0.0; and
- four controls structurally/semantically accepted, seven adverse cases
  structurally/semantically rejected, zero adverse structurally accepted.

An exact-byte retained harness copy is stored beside the result. This raises the
claim from producing-agent-reported target success to executed structural and
candidate-semantic fixture evidence at the declared target/runtime. It does not
establish runtime reference closure, cryptographic verification, privacy
admission, dispatch/activation enforcement, Bayesian validity, usability,
security assurance or whole-plan consensus.

