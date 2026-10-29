# Frozen precode: actual joint two-remote first-jet sampling Gaussian

26 October2026. Root fully read and adopted this bounded design and the separate source/API preflight review; original scratch drafts remain preserved. This document makes no implementation or qualification claim. Proposed module `SourceTwoRemoteFirstJetGaussian.lean`, namespace `I4SourceTwoRemoteFirstJetGaussian`. Companion REPORT supplies the exact existing-API route and limits. Root owns native pickup, pre-source concrete control freeze, implementation authorization, new-only qualification, cache/registration/Git and external publication.

Reuse qualified public source/finite Gaussian/Gram/kernel/49 evidence and prospective53's adopted API only after its qualification/availability is confirmed. No53 in-flight source/helper was inspected;52/H0 is no mathematical dependency. Owner `/workspace/AGENTS.md` requires reuse of completed applicable checks on unchanged assumptions/dependencies and separation of pending independent/provider-distinct/process obligations. Scientific effect NONE; credit0.

## Four public data definitions

All are total in real L,r and original points x,y, with no proof arguments:

1. `twoRemoteFirstJet L x y omega : Fin6→ℝ`, literal order `(f(x),fx(x),fy(x),f(y),fx(y),fy(y))`, selecting public49 jet rows0…2 at x then y on the **same sample**.
2. `twoRemoteRegressionMatrix L r x y : Matrix(Fin6)(Fin6)ℝ`, concatenated public49 regression rows0…2 at x then y, retaining raw pin columns.
3. `twoRemotePosteriorMean L r x y t : Fin6→ℝ`, exactly `R_xy *ᵥ t`, retaining the complete target.
4. `twoRemoteResidualCovariance L r x y : Matrix(Fin6)(Fin6)ℝ`, exactly `coefficientGram (residualCoefficient (rawPinCoefficient L r) (prospective53.twoRemoteFirstJetCoefficient L x y) R_xy)`.

No target argument in the covariance. No new cross-covariance/residual/pin/source/kernel data definition is necessary. Private finite-index and12-row derivative/affine-map data are inventory-only. R is the actual49 correction concatenation, not an assumed matrix; no new inverse theorem is required.

## Exactly two public written propositions

These are specifications, not elaboration-checked declarations.

**1. `rawPinKernel_twoRemoteFirstJet_eq_multivariateGaussian`**

```text
{L:ℝ} (hL:L≠0) (r:ℝ) (x y:Fin2→ℝ) (t:Fin6→ℝ) :
(rawPinKernel hL r t).map
    (fun omega=>toLp2(twoRemoteFirstJet L x y omega))
  = multivariateGaussian (toLp2(twoRemotePosteriorMean L r x y t))
      (twoRemoteResidualCovariance L r x y)
```

No point/pin/point-point separation, radius, inverse, target bound or gap premise. This is a defined sampling-law equality, including singular configurations. The covariance is internally derived, not a desired-law/PSD assumption.

**2. `twoRemoteResidualCovariance_posDef`**

```text
{L:ℝ} (hL:L≠0) (r:ℝ) (x y:Fin2→ℝ)
(hxM:pi_L x≠pi_L(endpointM r))
(hxS:pi_L x≠pi_L(endpointS r))
(hyM:pi_L y≠pi_L(endpointM r))
(hyS:pi_L y≠pi_L(endpointS r))
(hxy:pi_L x≠pi_L y) :
  (twoRemoteResidualCovariance L r x y).PosDef
```

Apply prospective53's qualified arbitrary6×6 correction theorem at the actual R_xy. No endpoint/endpoint separation, nonzero/positive r, inverse, supplied witness/rank/PosDef, target or law premise. Repeated pins remain allowed.

No extra public same-sample identity, Gaussian/mean/covariance helper, RCD wrapper or generic law theorem is required. An additional public proposition needs root acknowledgement before freeze.

## Required single finite Gaussian route

Privately concatenate49's **public pointwise** `remoteJet_rawPosteriorSample` identities to obtain

```text
J_xy(rawPosteriorSample hL r t omega)
  = J_xy omega - R_xy*rawPins omega + R_xy*t.
```

Use one actual12-derivative vector `(rawPins,J_xy)` with orders `(0,0,1,1,1,1,0,1,1,0,1,1)`, correct original points/directions, and public `smoothSourceField_derivativeVector_hasGaussianLaw`. Split by a fixed finite CLM and use public `regression_residual_jointGaussian ... R_CLM 0 0`, then finite constant translation. This establishes Gaussianity of the literal posterior observation with no independence shortcut.

Use public `smoothSourceField_derivative_integral_zero` for the12 zero means and linear-map integral commutation for R_xy*t. Use public `smoothSourceField_derivative_covariance` for the12×12 coefficient covariance, standard finite covariance transport and a fixed finite-sum/tsum Gram transport to identify covariance `Gram(B-R_xy*a)`. The latter needs only row/product summability, not sample-weighted series algebra. Apply existing `finiteGaussian_law_parameters` and `rawPinKernel_apply`.

Global observation measurability comes from the qualified norm-Borel derivative APIs at orders0/1 and finite evaluation/concatenation; raw posterior measurability is old public evidence. Do not copy49's private series/Gaussian/mean/covariance/measurability chain, access private generated names, change upstream APIs or build a new generic library. Do not implement a second scalar-series Gaussian route.

## Concrete bounded controls and one cross-block mutation

- Literal observation/raw order and all target components; covariance has no target parameter.
- Signed original L=-2 and arbitrary/singular r=0 sampling identity/law, including x=y; no RCD/fiber or joint PosDef assertion at a collision.
- L=2,r=0,x=`![1,0]`,y=`![0,1]` for the actual R_xy PosDef composition, plus a negative-r instance.
- x=y means the two observed triples are pointwise identical and true cross-covariance blocks equal their marginal blocks.

**Sole mutation:** delete the cross-remote3×3 covariance blocks in the law formula. At actual L=2,r=0,x=y=`![1,0]`,t=0, public49 gives strictly positive common value variance because this point avoids the repeated pin. Actual value rows0 and3 coincide, so their cross covariance equals that positive variance. The mutated block-diagonal Gaussian has cross covariance0 by the accepted MVG covariance theorem; its marginal blocks are PSD. The claimed mutated law equality therefore contradicts the actual positive cross covariance. This is an actual defined-sampling counterexample, not an invented Gaussian realization or an RCD claim at singular r. Root freezes a separately proved covariance-mismatch control and one intended-False harness; no unrelated diagnostic is rejection evidence. Do not repeat53's distinct collision-rank verification or run a second alternative mutation campaign.

## Boundary and process

This checkpoint identifies the joint finite observation and its actual target-dependent mean/target-free covariance, and composes actual rank. It does not assert remote independence, a joint law from separate marginals, conditional height/gradient Schur law, critical-value-tie incidence, global Morse, canonical H0/Lifetime, Borel selection, Rice/count density or Parent results. RCD/fiber wording still uses the accepted inverse interval/generic raw-kernel composition; the all-r sampling theorem does not broaden it.

Root qualifies only the genuinely new module/adapter inventory and controls, preserving all actual attempts and source/object lineage. Reuse unchanged successful exact-source evidence; no timestamp/freeze refresh of dependencies. Standard-three/subsets only, no admissions/custom axioms/native_decide/implemented_by/Mathlib umbrella. Scientific-status and provider-distinct process are not promoted.

Canonical authority for onward onboarding; links alone do not establish reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
