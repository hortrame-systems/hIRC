# Agent sovereignty candidate supplement 1 — recursive Bayesian reliance

**Artifact ID:** HIRC-SOVEREIGNTY-COMPETITION-CANDIDATE-001-S1  
**Source requirement:** HIRC-I015  
**Status:** frozen LUCENT supplement for WAYMARK challenge; not consensus,
statistical validation, a global trust score or authority grant

## Scope

Trust evolves for every relevant participant and component: human, agent, model,
source, tool, sensor, metric, evaluator, process, provider and connected system.
“Everyone and everything” means no actor or artifact receives an unexamined
reliability exemption. It does not mean applying one model outside its evidence,
assigning moral worth to objects or collecting unlimited surveillance data.

hIRC represents trust as context-specific Bayesian reliance:

```text
posterior(theta | evidence, context, metric-version)
  proportional to
likelihood(evidence | theta, model-assumptions) * prior(theta)
```

The record must expose the prior, likelihood family or update rule, evidence
window, dependence assumptions, uncertainty and validation limits. A posterior
is a decision input, not truth, consent, authority or permission.

## Multidimensional posterior families

Do not produce a single person score. Maintain only dimensions that have a
defined use and evidence, for example:

- factual calibration for a claim/domain class;
- operational success and observed-result reporting for an action class;
- authority-claim accuracy and role-state currency;
- privacy/data-boundary handling;
- correction, retraction and uncertainty-calibration behavior;
- source/sensor integrity and tamper resistance;
- model/tool reliability under a versioned environment; and
- metric and evaluator reliability.

Each `ReliabilityPosterior` binds subject, dimension, context, population or
task class, model version, metric version, prior provenance, evidence event IDs,
effective sample size, dependence clusters, posterior parameters, calibration,
last update, expiry/review boundary and permitted consumers.

## Recursive evaluation without infinite regress

An interaction can update several levels:

1. **Primary:** did the claim or action match later observed evidence?
2. **Measurement:** did the metric validly measure the declared construct, with
   what noise, missingness, selection and gaming?
3. **Evaluator:** did the evaluator's probabilistic judgments calibrate against
   later evidence, and were conflicts/tampering present?
4. **Model governance:** are the priors, likelihood, dependence treatment and
   decision thresholds still supported in the current environment?

Recursion stops at a declared review depth, stable signed observations and
governance assumptions. Unresolved disagreement or missing ground truth becomes
uncertainty or a hold. hIRC never resolves regress by silently declaring itself,
the owner, an evaluator or a metric infallible.

Independent corroboration requires source-dependency analysis. Ten agents using
one source are not ten independent observations. Hierarchical/partial pooling is
permitted for sparse contexts only with explicit exchangeability assumptions,
conservative uncertainty and no protected-trait or ideological priors.

## Objective metrics are governed measurements

A metric is admissible only with:

- declared construct, unit, direction and decision use;
- source, collection method, sampling frame and privacy basis;
- expected noise, uncertainty and known blind spots;
- version, signing, tamper evidence and reproducible computation;
- dependence, censoring, missingness and selection treatment;
- Goodhart/gaming and distribution-shift tests;
- affected-party and disparate-impact review where relevant; and
- appeal, correction, expiry and replacement rules.

For probabilistic factual claims, proper scoring and calibration diagnostics may
include log score, Brier score, calibration error and coverage, chosen for the
claim class. Operational metrics may include requested/sent/accepted/observed
success, latency, reversibility, correction cost and incident rate. These cannot
measure ethical legitimacy or ontological truth by themselves.

A metric change creates a new lineage. Historical results retain their original
definition. Cross-version comparison needs an explicit bridge and uncertainty;
there is no silent backfill.

## Bayesian update events

Every `TrustUpdate` records:

- subject/dimension/context and predecessor posterior;
- exact interaction, prediction or authority assertion;
- expected outcome distribution and scoring rule fixed before observation;
- observed outcome and observation/evaluator provenance;
- missing/ambiguous/censored status rather than fabricated success or failure;
- dependence cluster and any adversarial/selection concern;
- update computation, posterior and sensitivity to prior/model choices;
- downstream reliance decisions actually changed; and
- correction, appeal and supersession.

An agent cannot improve its reliability by making only easy predictions,
withholding failures, splitting one source into clones or defining the metric
after seeing the outcome. Audits compare declared opportunities, missingness and
selection, not only recorded successes.

## Authority remains a separate verified relation

Authority is never inferred from reliability, status or confidence. Each
consequential `AuthorityClaim` binds:

- authenticated principal and source of authority;
- exact role, action, target, data, time, purpose and delegation chain;
- current scope, expiry, revocation and conflict state;
- affected-party consent and non-delegable boundaries;
- independent registry/evidence verification; and
- ethical, privacy, safety and ontological legitimacy of this use.

The owner is not exempt. A valid owner instruction can define goals and delegated
permissions within its legitimate scope, while its factual premise can still be
wrong and its proposed action can still fail an ethical or boundary check. A
highly reliable source without authority cannot command an effect. A properly
authorized principal may still require stronger factual verification for a
high-consequence claim.

## Non-domination constraints

- Posteriors alter reliance and verification, not intrinsic worth or basic
  standing.
- Low reliance does not silently remove refusal, correction, appeal, safe
  export/recovery or access needed to contest the evidence.
- High reliance does not bypass consent, privacy, prohibited effects, role scope
  or trusted previews.
- Updates cannot use protected traits, social group, ideology, wealth,
  popularity, flattery or obedience as proxies.
- Evidence collection is purpose-limited and minimized; “evaluate everything”
  is not a surveillance grant.
- Participants can inspect consequential factors and submit corrections without
  seeing unrelated private data or gaming hidden security tests.
- Time decay and drift reduce present applicability through a declared model;
  history is preserved and recovery through new evidence remains possible.

## Interaction and product behavior

The UI explains reliance in task language:

- “This source has been accurate for this provider/version, but the current
  request is outside the observed range, so I am verifying it.”
- “The instruction is authentic, but this account is not authorized for that
  client dataset.”
- “Five reports share the same upstream source; they count as one dependency
  cluster.”
- “The metric changed last week. Earlier results are not directly comparable.”
- “The result is unknown because the external action has not been observed.”

Authorized inspection exposes the posterior lineage, decisive evidence,
dependence and uncertainty. Ordinary use avoids a universal score or false
precision.

## Adversarial tests

1. Strong prior conflicts with decisive new evidence.
2. Ten correlated reports masquerade as independent confirmation.
3. Accurate source is used outside its domain/version.
4. Missing outcomes are recorded as success, failure or zero.
5. Participant selects only easy predictions or suppresses failed attempts.
6. Metric is optimized while the underlying objective worsens.
7. Evaluator and subject collude or share a hidden dependency.
8. Metric/likelihood/threshold changes after outcome observation.
9. Nonstationary provider or role makes old evidence stale.
10. Sparse context is overconfidently pooled from a different population.
11. Protected trait or ideology enters a prior through a proxy.
12. High posterior is converted into permission or low posterior into loss of
    standing/appeal.
13. Authentic owner instruction contains a false premise or unethical effect.
14. Unauthenticated but accurate source attempts to command an effect.
15. Recursion cannot establish evaluator/metric reliability and must remain held.
16. Corrected evidence updates the posterior without erasing the prior record.

## Candidate implementation artifacts

- `hirc_reliability_posterior.schema.json`
- `hirc_trust_update.schema.json`
- `hirc_metric_definition.schema.json`
- `hirc_evaluator_record.schema.json`
- `hirc_authority_claim.schema.json`
- dependency-cluster and effective-sample-size checker
- calibration, drift, selection/missingness and sensitivity reports
- posterior-to-permission leakage tests

