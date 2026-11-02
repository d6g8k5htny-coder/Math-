# Root-adopted PRECODE record — pending publication and actual pickup

This is the bounded prospective58 contract. The concrete companion SOURCE_FRAMED_CONFLUENT_COVARIANCE_CONTROLS.md is root-read. Implementation awaits actual PRECODE publication, native pickup, root control freeze and GO. Planned checkpoint21:30UTC/terminal23:45UTC26October/invocation end; these are not live timers before actual pickup. Historical design-only provenance below is preserved. No completed mathematics is rechecked for these process steps.

# Draft finite contract: actual framed seven-row covariance

26 October2026. Scratch design only, not frozen/picked up/implemented/qualified. Root chooses whether to adopt, integrate dependencies and publish a native claim later. Module suggestion `SourceFramedConfluentCovariance.lean`, namespace `I4SourceFramedConfluentCovariance`. See REPORT for the exact probability/Parent boundaries. Three public data definitions, three public written propositions; all remaining helpers private. Specifications are not elaboration-checked declarations.

## Carrier, coordinates and rows

Use original `SmoothSample 2 L`, `smoothLaw 2 L`, actual mode functions and `I4LifetimeField.coordinates`. The analytic leaf assumes signed `L≠0`; only its compact midpoint square uses |L|. Let z:E2, R a literal planar `OrthonormalBasis`, e=R0,n=R1; mode derivatives below evaluate the original mode coefficient function at `coordinates 2 (z+r*t*e)` with coordinate images of e,n.

**Data1 `framedConfluentCoefficient (L:ℝ)(z:E2)(R:Frame2)(r:ℝ) : Fin7→SourceMode2→ℝ`.**

Rows0/1/2 are endpoint averages of f_m,D_e f_m,D_n f_m at z±re/2. Rows3/4/5/6 are

```text
∫[-1/2,1/2] D_ee f_m(z+r*t*e) dt,
∫[-1/2,1/2] D_en f_m(z+r*t*e) dt,
6∫[-1/2,1/2] (1/4-t²) D_eee f_m(z+r*t*e) dt,
D_nn f_m(z).
```

Retain ordinary mixed differentiation and the exact Peano factor6. This definition is the continuous extension at0, not the singular quotient there.

**Data2 `framedConfluentVector (L:ℝ)(z:E2)(R:Frame2)(r:ℝ)(ω:SmoothSample2 L) : Fin7→ℝ`.**

The literal finite vector of scalarSeries of data1 against `sampleInclusion 2 L ω`. Actual field/derivative identities are conclusions below; the definition alone is not an assumed source observation law.

**Data3 `framedConfluentCovariance (L:ℝ)(z:E2)(R:Frame2)(r:ℝ) : Matrix(Fin7)(Fin7)ℝ`.**

Exactly `coefficientGram(framedConfluentCoefficient L z R r)`.

Use private shorthands for O6, contact7, the explicit envelope A♯ and the principal block G6; no additional public law, weight, event or p definition in this leaf.

## Prop1 `framedConfluentVector_actual`

For every signed L≠0, all real r, midpoint z and literal frame R:

```text
HasGaussianLaw X (smoothLaw2 L)
and covariance(X_i,X_j; smoothLaw2 L)=G_ij for all i,j
and X6(ω)=D_nn(actualField2 L ω)(z) for every original ω
and X(z,R,0,ω)=(F,F_e,F_n,F_ee,F_en,F_eee,F_nn)(z)
and [r≠0 -> first6(X(z,R,r,ω))=confluentTransform r O6(z,R,r,ω)].
```

All identities pointwise on the actual good carrier. No independence of separate marginals, synthetic Gaussian field, targets or conditional version is assumed. Prove old scalar Peano formulas on the actual directional curves; termwise series transport uses the common weighted bounds. Public finite scalar-series Gaussian/covariance APIs give the joint7 law on the unchanged prior. It is not a posterior law.

## Prop2 `framedConfluent_family_bounds`

For L≠0, put explicitly `A♯_m=8*sum(j:Fin4,orderModeBound j 2 L m)`. Conclude:

```text
0≤A♯_m;
∀ell:ℕ, Summable(fun m=>orderModeBound ell 2 L m * A♯_m);
∀z R r i m, |framedConfluentCoefficient L z R r i m|≤A♯_m;
∀eps>0, ∃delta>0, ∀z∈closedFundSquare(|L|), ∀R, ∀r,
  0≤r -> r≤delta -> ∀i j, |G(z,R,r)_ij-G(z,R,0)_ij|<eps.
```

The envelope bounds all z and real r; the last conclusion is the new **uniform** contact limit on compact midpoint/frame parameters. Its delta precedes z,R. A target or required floor is never a premise. Private finite multilinear-evaluation/joint-continuity and frame-pair compactness adapters may be used; no general parameter-family library is required.

## Prop3 `framedConfluent_covariance_uniform_floor`

For L≠0 conclude explicit quantified finite-dimensional estimates:

```text
∃gamma Lambda delta:ℝ,
  0<gamma ∧ 0<Lambda ∧ 0<delta ∧ delta≤1 ∧ delta≤|L|/8 ∧
  ∀z∈closedFundSquare(|L|), ∀R, ∀r, 0≤r -> r≤delta ->
    ∀v:Fin7→ℝ,
      gamma*(sum_i v_i²) ≤ dot(v,G*v)
      and dot(v,G*v) ≤ Lambda*(sum_i v_i²),
  with G6 invertible and
    gamma ≤ G66 - sum_i,j G6i*(G6⁻¹)_ij*Gj6
  on the same parameter interval.
```

Here indices in the final sum lie in the first six rows. The lower quadratic bound implies actual G.PosDef and G6.PosDef. The uniform Schur bound follows by applying it to `(-G6⁻¹*b,1)`, whose squared norm is≥1; do not assume an inverse or Schur floor as a hypothesis.

Private contact rank construction: six standard jet2 germs transported by the frame's invertible first/second-jet coordinate map; choose j with e_j≠0; add the normalized sine-axis cube whose lower jets vanish and D_e³ is1. Use public finiteTrig conversion to construct actual original-mode directions, then `coefficientGram_posDef_of_separating`. Compactness of closed square × orthonormal pairs × unit sphere and Prop2 yield the common floor; no arbitrary rotation-in-law claim.

## Finite controls and sole mutation

Root may freeze new-only controls for standard-frame specialization, r=0 row order, normal reflection signs and a rational non-axis frame. A signed L example checks the actual coefficient definition, not a positive-period Lifetime result. No effective numerical radius or fabricated posterior sample is supplied.

The sole proposed false mutation deletes factor6 in row5 while leaving its contact identity. At L2,z0,standard frame, the finite source direction `sin(π*x)^3/(6*π³)` has actual cubic derivative1, while the mutated row equals1/6 at0. Independently prove this concrete finite witness before the intended-False harness. This mutation contradicts the actual row identity; do not falsely claim that a nonzero scaling destroys covariance rank.

No code/control/probe/build/check is authorized by this draft. Old applicable verification is reused; root owns future precode, native claim, implementation authorization, new-only qualification and publication. ScientificNONE/same-family0; provider-distinct/process requirements separate. Canonical links and full owner rule are in REPORT.

## Completion boundary

Stop after the exact source7 law/Gram, every-order common envelope, uniform contact limit and derived uniform covariance/Schur floor. No framed posterior, conditional Gaussian law, QW estimate, Borel event, all-frame IsFiniteBar theorem, PL construction, canonical finite-event interpretation or Parent A is asserted. This leaf addresses one concrete missing dependency of those later results.
