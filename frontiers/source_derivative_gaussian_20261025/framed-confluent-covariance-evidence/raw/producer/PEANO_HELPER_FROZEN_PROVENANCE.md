# Shifted directional curves and exact first-six Peano identity

Frozen 26 October 2026 at approximately 20:31 UTC, **before one producer integration**. This is **UNCOMPILED TEXT ONLY**, supplied by `/root/endpoint_gaussian_ac_text` to `/root/remote_jet_gaussian_construct` for actual authorized58 module `SourceFramedConfluentCovariance`, namespace `I4SourceFramedConfluentCovariance`.

Root's `ROOT_GO.json`, the published concrete control contract, and the corrected shared-context text were read before drafting. Native pickup `6426117613` was created20:06:26 UTC, board `6426118341`, precode `f01e0c7e94b5e1f929bfe18fe6bb01e3c44060b1`, actual GO20:07:35.879688 UTC. Checkpoint21:30 UTC and terminal23:45 UTC/end are unchanged. The control contract was frozen before source/helper text. These process facts are carried without an external lookup or repeated identity check.

The producer-supplied corrected context is `/workspace/scratch/framed-confluent-covariance-construct/HELPER_SHARED_CONTEXT.corrected.lean.txt`, recorded5635 bytes, SHA-256 `1b1f87de27699b4fe56d59d7057316b88ec50279663d72a344af8095cfb01e6d`. That identity is transcribed from the supplied custody message, not recomputed.

The entire needed section is `SECTION.lean.txt`; exact narrow imports are listed in `IMPORTS.txt`. Insert the section once inside the target namespace and its existing noncomputable section, after the actual private `peanoRows` definition from the corrected context. No `peanoRows`, `De`, contact-row, coefficient, covariance, physical-coordinate or source-sample definition is redeclared.

## Exact target and assumptions

The sole main target is the producer-requested private theorem `peanoRows_confluent`:

For any `f : (Fin 2 → ℝ) → ℝ`, its supplied genuine smoothness `hf : ContDiff ℝ (⊤ : ℕ∞) f`, arbitrary vectors `p e n : Fin 2 → ℝ`, real r and `hr : r ≠ 0`, the actual first-six row function `fun i : Fin 6 => peanoRows f p e n r (Fin.castAdd 1 i)` equals the public `I4SourceConfluentPins.confluentTransform r` applied to the literal vector

`[f(M), f(S), D_e f(M), D_e f(S), D_n f(M), D_n f(S)]`,

where `M=p−(r/2)•e`, `S=p+(r/2)•e`, and each directional derivative is the actual `fderiv ℝ f` evaluation.

There is **no unit, orthogonality, nonzero-direction, frame-rank, period, covariance or desired-integral-identity premise**. The only nonzero hypothesis is r≠0 for the existing quotient formula. The zero-radius Peano extension is deliberately left to the producer's separate `peanoRows_zero` adapter; no quotient value is assigned at0 by this section.

The context's actual private Peano ledger must remain the corrected one: rows3/4 are the fixed-interval D_ee/D_en integrals at `p+(r*t)•e`; row5 is **6** times the integral of `(1/4−t²) D_eee`; row6 is the midpoint D_nn. The main theorem selects exactly indices0..5 by `Fin.castAdd 1`. The distinct lower-jet selector including row6 is not used here.

## Complete directional-curve proof

For the scalar curve `F(s)=f(p+s•e)`, first translate f by p, then compose with the public CLM `s↦s•e`. Public `ContinuousLinearMap.iteratedFDeriv_comp_right` and `iteratedFDeriv_comp_add_left` give its actual iterated scalar derivatives, with no invertibility or isometry assumption on that CLM. Evaluating on all scalar unit directions gives F's first/second/third derivatives as the literal e, [e,e], [e,e,e] directional derivatives.

For `H(s)=fderiv ℝ f (p+s•e) n`, genuine smoothness of `fderiv f` and constant CLM evaluation supplies smoothness. Public `iteratedFDeriv_clm_apply_const_apply` and the right-currying successor formula give H's first derivative as the literal mixed array **[e,n]**. No Hessian symmetry or swapping of e/n is needed to obtain the defined row.

The main proof derives C3 regularity of F and C2 regularity of H from hf and the smooth affine curve. It invokes only the already accepted public `pin3_integral`, `pin4_integral`, `pin5_integral`. Endpoint conversion `p+(-r/2)•e=p−(r/2)•e` preserves signed r. Reordering the derivative endpoint average aligns the public scalar pin5 convention with the actual raw vector. The six final row comparisons are then definition/finite-index reductions.

In particular, the cubic factor6 is inherited literally from accepted `pin5_integral` and remains present on both the actual Peano row and its formula. The frozen future control/mutation distinguishing correct pairing1 from omitted-factor pairing1/6 is unchanged. This helper neither implements nor executes that control.

## Authored inventory and ownership

Exactly four authored **private** propositions are supplied:

1. `peanoCurve_iteratedDeriv`, a fixed-Pi2 shifted-curve conversion.
2. `peanoCurve_deriv`, its first-derivative spelling.
3. `peanoCurve_transverse_iteratedDeriv`, constant transverse evaluation conversion.
4. `peanoRows_confluent`, the exact requested first-six statement.

There is no authored data definition or public declaration. The local linear map and scalar curves are local proof terms. Generated auxiliaries remain for the final integrated owned-module inventory to classify. The production public inventory remains exactly three data definitions and three propositions.

The producer retains physical coordinate chain rules for actualField, signed-source smoothness instantiation, samplewise series–integral interchange, Gaussian/Gram identification and source envelopes. Other assigned helpers retain rank and compact-matrix work. This section contains none of those proofs and introduces no general public calculus library, source-law rotation claim or probabilistic certificate.

## Exact accepted API text read

All paths below are in the existing packet and its pinned `.lake/packages/mathlib/Mathlib`:

- `ConfluentIntegralIdentities.lean`: public `pin3`, `pin4`, `pin5` and `pin3_integral`, `pin4_integral`, `pin5_integral`. Their accepted scalar proofs are reused, not reimplemented or checked again.
- `SourceConfluentPins.lean:22`: the exact public `confluentTransform` row order and normalization.
- `Analysis/Calculus/ContDiff/Basic.lean:461`: `ContinuousLinearMap.iteratedFDeriv_comp_right`.
- `Analysis/Calculus/ContDiff/FTaylorSeries.lean:959`: `iteratedFDeriv_comp_add_left`.
- `Analysis/Calculus/ContDiff/FTaylorSeries.lean:919`: `iteratedFDeriv_succ_apply_right`, with `Fin.init_snoc`/`Fin.snoc_last` preserving mixed-direction order.
- `Analysis/Calculus/ContDiff/Comp.lean:563`: `iteratedFDeriv_clm_apply_const_apply`.
- `Topology/Algebra/Module/ContinuousLinearMap/Basic.lean:704,710`: fixed-vector `smulRight` and its evaluation.
- `Analysis/Calculus/IteratedDeriv/Defs.lean`: scalar iterated derivative/Fréchet evaluation and `iteratedDeriv_one`.
- Existing public directional-axis conversions in `SourceConfluentLimits.lean` illustrate the already accepted scalar/Fréchet and constant-evaluation route. The new work is its arbitrary shifted-direction application, and no foreign private generated name is imported.

Only accepted read-only API lookup, new text writing and the single requested first custody identity recording for these new text files occurred. No Lean/name probe/test/build/check/kernel/audit/control campaign/object creation, old payload hash, packet edit, Git/cache/shared metadata/configuration or external action occurred. All earlier directories remain unchanged. No57 source or other58 helper's source was inspected or consumed; only the producer's explicitly corrected shared context was read.

The complete needed text/import/provenance is frozen before one integration. Final producer qualification covers the actual integrated source and any necessary local amendments; this helper has no standalone qualification or credit. Completed applicable verification and accepted scalar/source mathematics remain reusable under `/workspace/AGENTS.md`. Pending different-family/process work remains separate from that evidence. Scientific effect **NONE**; same-family/provider-distinct credit **0**.

Canonical onward authority carried from the adopted58 controls, without claiming link reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
- https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md
