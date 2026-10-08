# hIRC 1.0 → 1.1 predecessor crosswalk — working draft

**Status:** deterministic heading/requirement inventory with authored candidate mappings; semantic audit pending

| 1.0 | Source section | 1.1 target | Status | Review note |
|---|---|---|---|---|
| 00 | Document contract and reading map | 00 Document contract | PRESERVED_AND_REVISED | Claim grades, source bindings and correction discipline are explicit. |
| 01 | Product definition | 01 Product definition | PRESERVED_AND_REVISED | Local-first operational-memory purpose and acceptance objective retained. |
| 02 | Non-negotiable invariants | 02 Non-negotiable invariants | PRESERVED_AND_EXTENDED | Original invariants retained through requirements; foundation/security/sovereignty invariants added. |
| 03 | What the current application actually has | 00 Document contract | DETAIL_RESTORED_PENDING_PEER_AUDIT | Draft 00.1 restores corrected prototype/transfer evidence and the source-reported functionality/boundary table. |
| 04 | Requirement traceability and change discipline | 00 Document contract | PRESERVED_AND_EXTENDED | Canonical intent/requirements and supersession/evidence discipline retained. |
| 05 | Privacy before ingestion | 07 Privacy and data lifecycle | PRESERVED_AND_EXTENDED | Pre-ingress and egress privacy plus field lifecycle and derived-data inheritance. |
| 06 | Architecture: a small trusted core with replaceable components | 08 Small trusted core and effect path | PRESERVED_AND_EXTENDED | Small trusted core now includes foundation/security/effect path. |
| 07 | Domain model and recursive composition | 10 Work, evidence and automatic reconstruction, 12 Permanent agents, teams, scheduling and resources | PRESERVED_AND_REVISED | Recursive domain/work/organization concepts split across work and permanent-team sections. |
| 08 | Identity, roles, permanence, and refusal | 05 Sovereignty, fallibility and principled refusal, 09 Identity, authentication, secrets and recovery roots, 12 Permanent agents, teams, scheduling and resources | PRESERVED_AND_EXTENDED | Identity/permanence/refusal now include sovereignty, secrets and permanent-only policy. |
| 09 | Operator attention and context continuity | 10 Work, evidence and automatic reconstruction, 11 Attention, navigation and trusted experience | PRESERVED_AND_EXTENDED | Context recovery and operator attention retained with trusted/security visibility. |
| 10 | Visual identity, windows, and accessibility | 11 Attention, navigation and trusted experience | PRESERVED_AND_REVISED | Classic visual/accessibility direction retained; asset-level detail remains in predecessor requirements. |
| 11 | Conversations and communication routing | 06 Requests, clarification, trust and authority, 10 Work, evidence and automatic reconstruction, 11 Attention, navigation and trusted experience | PRESERVED_AND_EXTENDED | Routing and message truth states are represented across request, work and UI contracts. |
| 12 | Shared-agent scheduling and reservations | 12 Permanent agents, teams, scheduling and resources | PRESERVED_AND_EXTENDED | Reservations/queues gain execution epochs, budgets and debate/competition eligibility. |
| 13 | Recursive team planning and permanent spawning | 12 Permanent agents, teams, scheduling and resources | PRESERVED_WITH_SUPERSESSION | Permanent recursive organization retained; temporary-agent unban is superseded. |
| 14 | Automatic operational memory and project management | 10 Work, evidence and automatic reconstruction | PRESERVED_AND_EXTENDED | Operational memory, dependencies, evidence and correction are core. |
| 15 | Provider-independent model configuration | 15 Provider-independent model and tool adapters | PRESERVED_AND_EXTENDED | Provider configuration becomes exact route/version/privacy/probe contract. |
| 16 | Durable memory and model migration | 16 Durable memory and secure migration | PRESERVED_AND_REVISED | Whole authorized migration and minimum active target context are separated. |
| 17 | Custom preprompts and effective instruction stacks | 03 Foundation source graph and compilation, 04 Genesis, formation and admission, 23 Safe recursive improvement | PRESERVED_AND_REVISED | Prompts are compiled model inputs under foundation/formation/change rather than authority. |
| 18 | Onboarding and specialist-update rollouts | 03 Foundation source graph and compilation, 04 Genesis, formation and admission, 23 Safe recursive improvement | PRESERVED_AND_EXTENDED | Onboarding becomes source graph, personal formation and governed rollout. |
| 19 | hScript, commands, plugins, and self-extension | 19 hScript, commands and extensions | PRESERVED_AND_EXTENDED | hScript/extensions gain no-ambient-authority sandbox/supply-chain controls. |
| 20 | Federated systems, bridges, bridles, and bridgekeepers | 20 Bridge architecture and protocol | PRESERVED_AND_REVISED | Federation becomes four-part Bridge with staged disabled gates. |
| 21 | Universal timestamps, causal order, and temporal reconstruction | 21 Time, journal, archives and recovery | PRESERVED_AND_EXTENDED | Time/causality gain trusted-time, nonce, epoch and replay constraints. |
| 22 | Data preservation, search, archives, and recovery | 21 Time, journal, archives and recovery | PRESERVED_AND_EXTENDED | Archives/restore gain audit anchors, key separation, disposition and clean-room recovery. |
| 23 | Security architecture and threat boundaries | 24 Threat model and security ownership | PRESERVED_AND_EXTENDED | Security becomes whole-system threat model, not only a section outline. |
| 24 | The attention governor: preventing cognitive overload as complexity grows | 11 Attention, navigation and trusted experience | PRESERVED_AND_EXTENDED | Attention governor now protects security classes and avoids coercive suppression. |
| 25 | Visual system, window mechanics, and adaptation | 11 Attention, navigation and trusted experience | PRESERVED_AND_REVISED | Visual/window adaptation retained in compact integrated section and predecessor requirements. |
| 26 | Source connectors, automation, and coverage contracts | 07 Privacy and data lifecycle, 10 Work, evidence and automatic reconstruction, 15 Provider-independent model and tool adapters | PRESERVED_AND_EXTENDED | Source connectors, reconstruction and dependency triggers split across data/work/provider contracts. |
| 27 | Capability discovery and computation economics | 12 Permanent agents, teams, scheduling and resources, 15 Provider-independent model and tool adapters | PRESERVED_AND_EXTENDED | Capability discovery and economics covered by provider probes and resource envelopes. |
| 28 | Safe recursive improvement and self-modification | 23 Safe recursive improvement | PRESERVED_AND_EXTENDED | Recursive improvement becomes source-bound FoundationChange with predecessor evaluation. |
| 29 | Scenario traces: concrete behavior to design against | 25 Executable acceptance and adversarial verification | DETAIL_RESTORED_PENDING_PEER_AUDIT | Draft 25.1 restores the nine predecessor scenarios and adds succession, refusal, Bayesian-reliance and competition cases. |
| 30 | Singularity-oriented stress scenarios and adaptation constraints | 24 Threat model and security ownership, 25 Executable acceptance and adversarial verification, 26 Delivery sequence and gates, 28 Explicit nonclaims | DETAIL_RESTORED_PENDING_PEER_AUDIT | Draft 25.2 restores scale/modality/coalition stress classes and adds foundation/evaluator compromise. |
| 31 | Architecture decisions and defaults to freeze | 27 Open decisions | DETAIL_RESTORED_PENDING_PEER_AUDIT | Draft 27.1 restores ADR-001–020 and adds ADR-021–035 for the revised architecture. |
| 32 | Executable acceptance and adversarial test specification | 25 Executable acceptance and adversarial verification | PRESERVED_AND_EXTENDED | Acceptance/adversarial families expanded across new architecture. |
| 33 | Implementation sequence and go/no-go release gates | 26 Delivery sequence and gates | PRESERVED_AND_EXTENDED | Implementation sequence gains foundation, legal, trust, continuity, debate and competition subphases. |
| 34 | Scope boundaries and unanswered design decisions | 27 Open decisions | PRESERVED_AND_EXTENDED | Scope boundaries and consequential decisions remain explicit. |
| 35 | What hIRC deliberately will not claim | 28 Explicit nonclaims | PRESERVED_AND_EXTENDED | Nonclaims expanded for trust, metrics, sovereignty, licensing and Bridge. |
| 36 | Traceability, source register, and framework crosswalk | 00 Document contract, 03 Foundation source graph and compilation, 29 Traceability and product language | PRESERVED_AND_REVISED | Traceability is internal/source-bound and ordinary product language stays plain. |
| 37 | Glossary and final product acceptance condition | 30 Acceptance objects | DETAIL_RESTORED_PENDING_PEER_AUDIT | Draft 30.1/30.2 restore and extend the glossary and final acceptance statement. |

## Requirement identity check

- 1.0 requirements: 151
- 1.1 draft requirements: 218
- missing predecessor IDs: none
- predecessor status changes: U064, U119
- new IDs: 67

ID presence does not prove preserved meaning. The first-pass detail debt for sections 03, 29, 30, 31 and 37 was restored in the working draft and remains pending peer semantic audit before 1.1 can replace 1.0.
