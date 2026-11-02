# Actual-source Lifetime pair-set finiteness

Scientific effect: **NONE**. This packet proves a narrow actual-source finiteness
application, with nine new public `Prop` theorems. Source integration commit:
`c039243e449fcab837127ff2bc0b12edb1dc05e9` (provided by root). The binding brief
was frozen at `8d64490df8620b749ba2f224da535eeb6016c2d0`, SHA256
`4c45c172ab8cf5beb11032cdd3169f102f9238bd1967efb2837b379f38588804`.

The new source is `SourceLifetimePairFiniteness.lean`, SHA256
`36bf363f88d450a61052086c5d7eb799d12dd58ce4b74c1c083a056991606081`.
Its field and law are exactly `I4LifetimeField.actualField 2 L` and
`I4SmoothCarrier.smoothLaw 2 L` on the existing `SmoothSample 2 L` carrier.
No field with an assumed Morse or finiteness property is substituted.

For `0 < L`, the literal Lifetime critical set

```
{x | x ∈ UniversalLaw.Spec.Lifetime.FundDomain 2 L ∧
     UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (actualField 2 L ω) x}
```

is almost surely finite. Criticality means the actual Fréchet derivative is
zero, exactly as in the original Lifetime input. The existing continuous linear
equivalence `I4LifetimeField.coordinates 2` transports criticality to the
Pi-coordinate gradient zero condition. The half-open domain `[0,L)^2` lies in
the completed closed source cube `[0,|L|]^2`.

The application then proves, on one common full-measure event, that for **every**
height set `A` and **every** pair predicate `Pair` whose members are actual
critical points at both endpoints,

```
UniversalLaw.Spec.Lifetime.pairSet 2 L Pair (actualField 2 L ω) A
```

is finite. The only population premise is endpoint criticality, not the desired
finiteness conclusion. No measurability or positivity restriction on `A` is
needed for this set-theoretic finiteness result. The set is contained in the
product of the finite actual critical sets.

The genuine existing Lifetime definitions yield candidate, window,
window-elder, unrestricted positive-gap, and finite-bar specializations by their
criticality clauses. Window parameters, elder interfaces, and height sets are
quantified inside the full-measure event. An elder interface only restricts the
population here; no elder-rule correctness premise or conclusion is used.

## Exact new public theorem inventory

All names have prefix `I4SourceLifetimePairFiniteness`.

| Source line | Theorem | Coverage |
|---|---|---|
| 26 | `actual_critical_coordinateGradient_zero` | Actual Fréchet criticality implies the existing Pi-coordinate gradient is zero. |
| 44 | `coordinates_fundDomain_mem_sourceMorseCube` | Literal half-open Lifetime domain embeds in the completed source cube. |
| 57 | `smoothLaw_ae_finite_criticalFundDomain` | Same-law actual Lifetime critical set is almost surely finite. |
| 69 | `smoothLaw_ae_finite_pairSet_of_critical` | One full-measure event covers every height set and population implying both endpoint criticalities. |
| 83 | `smoothLaw_ae_finite_candidatePairSet` | Genuine `IsCandidatePair` specialization. |
| 90 | `smoothLaw_ae_finite_windowPairSet` | Genuine `IsWindowPair` for all window parameters. |
| 100 | `smoothLaw_ae_finite_windowElderPairSet` | Genuine `IsWindowElderPair` for all parameters and supplied elder interfaces. |
| 110 | `smoothLaw_ae_finite_unrestrictedPairSet` | Genuine `IsUnrestrictedPair` specialization. |
| 117 | `smoothLaw_ae_finite_finiteBarPairSet` | Genuine `IsFiniteBar` specialization for every supplied elder interface. |

`PUBLIC_PROOF_NAMES_APPEND.json` contains exactly these nine fully qualified
names. The new module introduces zero definitions, zero data instances, and
zero private or generated declarations beyond these nine theorems.

## Reused mathematics and support provenance

The proof reuses the completed theorem
`I4ActualSourceMorse.smoothLaw_ae_finite_sourceCriticalCube` with `hL.ne'`.
Its source `SourceMorseIncidence.lean` has SHA256
`b93fe8f7856d4e632b3ff823788469720ae0814440bbec744fde099d4f29f127`;
its completed `.olean` identity is
`c59d6ec1e4f72ae2635255dcd81894c39c352eadf10b409a65ec7fa0464d37bb`.
All prior applicable source/cube verification remains reused. No Sard, inverse
function theorem, compact-zero argument, or C293 quotient/inertia theorem is
reproved or replayed here.

No compatible `Lifetime.olean` or `SourceLifetimeGeometry.olean` was found under
`/workspace`, so two new support inputs were necessary for this package ABI:

- `inputs/Lifetime.lean`: original C291
  `frontiers/source_lifetime_realization_20261017/inputs/Lifetime.lean`, SHA256
  `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`.
  Only the first `import Mathlib` line was replaced by eight narrow Mathlib
  imports; every following byte, mathematical definition body, and qualified
  name is preserved. Adapted SHA256:
  `371365f9bb17fbe1491c38bb00359300ea76641d3b5693d8feb11bb2c3fad51e`.
  The exact delta is `LIFETIME_IMPORT_ONLY.patch`.
- `inputs/SourceLifetimeGeometry.lean`: exact byte copy of original C291
  `frontiers/source_lifetime_realization_20261017/SourceLifetimeGeometry.lean`,
  SHA256 `8ec4b18959055f20d849337e44a70d0c5b39b7959b54cb4d7b6c2a473ee0612d`.
  The two definitions and eleven original theorem bodies are unchanged.

The Lifetime input contains 38 explicit named definitions/structures/abbreviation
and no source theorem. It is a statement/interface module, not 38 proved parent
results. The exhaustive axiom inventory also covers its generated declarations.
The copied geometry's preexisting theorems are not new proof-registry append
names. Definitions and generated data are classified separately in the catalog.
Original C291 source and existing proof records remain untouched.

## Completed, scoped qualification

Lean is pinned to `leanprover/lean4:v4.34.1`, Mathlib to
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The following execution evidence is
completed and reusable:

- Both necessary support inputs compiled with `-DwarningAsError=true` on their
  first attempts. The new application compiled with the same flag on attempt 03.
- One named `lake env leanchecker SourceLifetimePairFiniteness` replay exited 0.
- A direct `Lean.Util.CollectAxioms` audit of every declaration originating in
  the three named modules exited 0: Lifetime 103, geometry 16, new application 9,
  total 128. Allowed axioms are exactly `propext`, `Classical.choice`, and
  `Quot.sound`. The audit also prints all nine final public theorem statements.
- Completed controls prove the fundamental domain is infinite, an arbitrary
  population `Pair=True` gives infinitely many actual-source pairs on `univ`,
  the carrier's actual zero sample has identically zero field and infinitely
  many critical fundamental-domain points, and a concrete actual candidate
  window at `L=1` has an almost-sure finite pair set without a supplied Morse or
  finiteness premise.
- Two deliberately false mutations were rejected, each exit 1: removing both
  endpoint-criticality requirements; replacing almost sure finiteness by
  finiteness at every actual sample. The proved counterexamples explain why
  those mutations are false.

All failed production/control attempts, their exact source snapshots, raw logs,
observed exits, lineage, frozen sources, and successful recorder outputs are in
`raw-production/`. Initial compilation predates the structured recorder; its
source/command/exit associations are honestly identified as producer tool-history
transcriptions in `initial-command-history.json`, not invented machine receipts.
The later kernel, audit, controls, and rejections have actual structured records
with before/after source and artifact identities.

Packaging reuses those completed records and identities. It executes no Lean,
kernel replay, or mathematical control. Existing source/object hashes are read
from saved qualification records rather than recomputed. The
`/workspace/AGENTS.md` owner clarification of 25 October 2026 requires this reuse;
a new agent, session, or handoff alone does not warrant unchanged checks.

## Boundaries and remaining process requirements

This is one actual finiteness conjunct toward `IsLifetimeDensityVersion`. It
proves neither count integrability, count measurability, existence of a lifetime
density, a theta/field interface, elder correctness, distinct critical values,
parent asymptotics, nor any full parent theorem. There are no custom axioms,
`sorry`, `admit`, or `native_decide` additions. No scientific register or status is
changed. A provider-distinct alignment review is not claimed; it remains a
separate process requirement and does not erase completed mathematical evidence.

Producer: OpenAI / Codex, agent `/root/lifetime_pair_finiteness`; no subagents.
Root owns package registration, aggregate metadata, commits, publication, and
integration. Occupied PR482/485 were not taken over.

Standing owner sources carried for onboarding:
[owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
and
[standing delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md).
