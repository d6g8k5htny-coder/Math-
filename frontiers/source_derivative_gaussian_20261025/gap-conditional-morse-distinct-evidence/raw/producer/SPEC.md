# Prospective global59 — source-gap conditional Morse distinctness

26 October2026. **DESIGN ONLY, before any proper global59 PRECODE/native claim
or implementation GO.** This new scope follows root's reading of CORE-AUDIT
native6427244462, created21:02:20UTC, and the original global research objective.
The prior `/workspace/scratch/raw-pin-local-morse-construct/` documents and
remote-consumer preflight remain unchanged, reusable private design material.
They are not separately packaged public endpoints in this scope.

Future module `SourceGapConditionalMorseDistinct.lean`, namespace
`I4SourceGapConditionalMorseDistinct`. Exactly **one authored public
proposition**, no authored public data/definitions/structures or extra public
generic/local library. Proper PRECODE/control freeze/native pickup/GO and every
timer/source cut are PENDING ROOT. Source58 must register before59; that process
ordering does not authorize reading58 source/helpers. No implementation,
harness/helper proof text, Lean/probe/build/check/kernel/audit/hash, Git/cache/
shared-metadata or external action is authorized by this draft.

Scientific effect NONE; same-family/provider-distinct credit0. Completed
applicable verification is reusable under `/workspace/AGENTS.md`; pending
process/different-family requirements do not erase it or warrant old replay.

## Exact single public endpoint

The following is a signature specification, not implementation text:

```text
sourceGapLaw_ae_isMorseDistinct
  {L : ℝ} (hL : 0 < L) :
  ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ δ ≤ L / 2 ∧
    ∀ r : ℝ, 0 < r → r < δ →
      ∀ b k : ℝ, 0 < k →
        ∀ᵐ ω ∂I4SourceCompactTargetMoments.sourceGapLaw hL.ne' r b k,
          UniversalLaw.Spec.Lifetime.IsMorseDistinct 2 L
            (I4LifetimeField.actualField 2 L ω)
```

The interval is derived from L **before r,b,k**. There is no compact mark bound,
k-lower-bound parameter, supplied frame/rank/law/Morse assumption, desired
section-nullity certificate or final kernel-equality premise. Each r,b,k is
outside its own a.e. quantifier. No common event over uncountably many marks or
radii is claimed. The positive-gap restrictions are essential: the final
theorem is not unrestricted in the full raw target or in k.

These are the actual accepted types and definitions. `actualField` is the
original `smoothSourceField 2 L ω` composed with
`I4LifetimeField.coordinates 2 : Lifetime.E 2 ≃L[ℝ] (Fin 2 → ℝ)`.
`Lifetime.IsMorseDistinct` means (i) every literal Lifetime critical point has
some **genuine complementary-subspace Hessian inertia**, and (ii) critical
points with **positive literal torusDist** have different values. Smoothness
and L-periodicity are already automatic through accepted
`actualField_smooth`/`actualField_periodic`; they are not public premises or new
conclusions bundled into this leaf.

## Accepted exact sampler identity: reuse, do not hypothesize

The critical fixed-null-target composition already has a public exact API:

`I4SourceCompactTargetMoments.sourceGapLaw_eq_rawPinKernel`
(`SourceCompactTargetMoments.lean:174–178`) states, for every r,b,k and hr:r≠0,

`sourceGapLaw hL r b k = rawPinKernel hL r ![b,b-k*r^3,0,0,0,0]`.

It uses `rawPinKernel_eq_confluent` and the exact
`sourceGapPins_eq_confluent` target identity. The underlying
`rawPosteriorSample_eq_posteriorSample` is an **every-sample coefficient-sampler
equality**, not an a.e.-target conditional-law uniqueness assertion. Reuse this
existing exact result at the prescribed target; do not redevelop regression,
replace the sampler, assume the desired equality, or invoke HasCondDistrib
uniqueness at a null conditioning point.

Choose the small interval from the target-independent invertibility fact
`(I4SourceEndpointEstimates.sourceEndpoint_parameter_limits hL.ne' 0).1`.
Shrink it so δ≤1 and δ≤L/2. For0<r<δ this yields the accepted
`IsUnit (sourcePinCovarianceAt L r)`, r≠0 and distinct pin quotient classes.
The existing `rawPinKernel_pin_fiber` then gives exact raw target pins on one
a.e. event. Its nonsingularity hypotheses are derived on the interval, not
supplied by the public theorem. The choice b=0 in the covariance-limit API is
only a target-independent way to extract its first component, not a restriction
on the later real b.

## Private finite source normalization, shared by dimensions2,3,5

Use accepted actual finite original-mode witnesses:

- `I4SourceRemoteJetWitness.actual_finite_remoteJet_witnesses`: raw-kernel and
  identity response for(value,dx,dy,dxx,dxy,dyy) at one quotient-remote point.
- `I4SourceTwoRemoteFirstJetWitness.actual_finite_twoRemoteFirstJet_witnesses`:
  raw-kernel and identity response for(fu,dxu,dyu,fv,dxv,dyv), when both points
  are remote from both pins and their quotient positions differ.

Select the needed actual Finsupp columns and derive linear independence by
their identity response. Put their finite support union in the existing finite
Euclidean coefficient space, not the random coefficient product space.
Use existing `gramSchmidtNormed_orthonormal`,
`gramSchmidtNormed_linearIndependent`, `span_gramSchmidtNormed_range` together
with `span_gramSchmidt`, then extend the finitely many coordinates back by zero.
This bounded private source adapter produces the public57
`RawPinFreeFrame L r n` for n=2,3,5. Its finite Gram normalization preserves the
span and an invertible change of basis, **not** the identity response matrix.
Raw zero pairings survive linear combinations. No random sampled sequence is
assumed l2. There is no new public Gram–Schmidt/general library or copied old
private scalar Gaussian chain.

For each selected frame, the actual constraint response matrix B(y) is a finite
sum of literal mode derivatives, hence smooth. Its center response is
invertible by the finite witness/change-of-basis identities. Derive a local
invertible chart and compact closed subcharts; no rank or uniform conditioning
floor near the pins/diagonal is assumed. Frames and charts are deterministic
and selected independently of residual samples and target values.

## Three private null-event consumers

All use literal finite shifts of the **same** smooth sample and the57 entire
coordinate-vector/whole residual law. The finite source field/derivative
identities are derived from accepted finite-change/derivative-series engines,
not supplied as an assumed perturbation model.

| Private event | Spatial variables | Constraint order | Selected old columns | Free dimension |
| --- | --- | --- | --- | --- |
| Degenerate remote critical point | y∈R² | dx,dy; singular actual Hessian | one-remote1,2 |2|
| Remote critical point at a fixed level α | y∈R² | f−α,dx,dy | one-remote0,1,2 |3|
| Two quotient-distinct remote critical points with equal values | (u,v)∈R⁴ | dxu,dyu,dxv,dyv,fu−fv | two-remote1,2,4,5,0 |5|

**Local Morse.** For a fixed actual base posterior sample, let g(y) be its
actual coordinate gradient and θ(y)=−B(y)⁻¹g(y). Prove the mandatory full normal
equation

`B(y)Dθ(y)v = −(Dg(y)v + (DB(y)v)θ(y)) = −Hshift(y,θ(y))v`.

Hshift is the actual spatial Hessian with the parameter held fixed at θ(y).
Dropping DB·θ is false and is the sole mutation target. Accepted source
gradient/discriminant/symmetry APIs and the accepted normal-equation singularity
engine show that a degenerate critical point lies in the singular-Dθ image.
Apply the existing equal-dimensional Sard/Haar-null-image theorem and public
two-dimensional Gaussian absolute continuity. This is private local design,
not an additional public theorem.

**Prescribed level.** For each fixed α and full target t, solve the actual three
constraints by θ(y)∈R³ on a derived rank chart. Extend to a3→3 map by ignoring
one dummy input coordinate. A private explicit finite-coordinate flattening
uses(y0,y1,s), and the map ignores s. Its derivative kills the nonzero dummy
basis vector everywhere, so Sard gives a null image. There is no Hessian
condition in this consumer. α precedes a.e.; never assert absence of critical
points at every real level on one event.

**Remote pair tie.** Solve the listed five constraints by θ(u,v)∈R⁵. Use the
explicit finite-coordinate grouping(u0,u1,v0,v1,s) and ignore s to get a5→5 map
with a nonzero derivative-kernel dummy vector. The exact fifth row is
fu−fv; using old column0 after columns1,2,4,5 makes the center response identity
before normalization. No new twelve-jet witness, joint Hessian density or
expected-pair counting formula is needed.

For dimensions3 and5, derive private iid standard-Gaussian pi absolute
continuity from **public** `gaussianReal_absolutelyContinuous`,
`Measure.AbsolutelyContinuous.prod`, and the public finite grouping transports
`measurePreserving_piFinSuccAbove`/`volume_preserving_piFinSuccAbove` (or their
fixed-dimensional compositions). Do not call/copy52's private
`finiteGaussian3_absolutelyContinuous` or invent a public replacement library.
Only dimensions needed by this leaf are used. The57 law already handles every n
and supplies the full joint vector law, not merely scalar marginals.

For each compact chart, the bad sample event is Borel from the accepted compact
positivity theorem and evaluation measurability/continuous paths. For level/tie
events use nonnegative sums of squares of their actual constraints. The57
residual-first product map, all-target reconstruction, accepted
`rawPinKernel_apply` and product-null/Fubini transfer every proved finite
parameter null section to the **actual** defined raw sampling law. The
section-nullity is discharged by the source/incidence argument, never assumed
as the desired conclusion in another notation.

## Countable spatial composition and pins

For fixed L,r, the real-cover remote locus is open, as is the pair locus where
both projections avoid both pins and the two projections differ. Use
second-countability/Lindelöf or a rational compact-ball exhaustion subordinate
to the derived rank charts. Retain a **countable collection of compact
subcharts covering every point** of each locus. Frames can be chosen once for
these deterministic charts; no random/measurable frame selector is required.
No rank lower bound is required uniformly into pins or the pair diagonal.

Intersect the resulting countably many probability-one compact events, for
each fixed target. This yields remote Morse nondegeneracy; remote critical
values avoid each fixed α; and no quotient-distinct remote critical pair ties.
It is enough to build a measurable probability-one subset and infer the final
predicate pointwise; no global critical-point selector or separate Borel
IsMorseDistinct theorem is a premise.

At the two pin quotient classes reuse completed52
`rawPinKernel_ae_endpointHessian_det_ne_zero` and periodic jet transport of the
same sample. Exact raw-fiber pins give endpoint criticality and heights t0,t1.
For the gap target, t0=b and t1=b−kr³ are different since k>0,r>0. Apply the
prescribed-level consumer twice, at α=t0 and α=t1, to exclude remote/pin ties.
The remaining cases are remote/remote (five constraints) and pin/pin (positive
gap). The two pin classes are distinct on r<L/2.

Keep quotient-aware positions throughout. For literal Lifetime points X,Y,
positive `torusDist 2 L X Y` implies unequal projections of their accepted
coordinate images. The needed implication can be derived directly: equal
projections give an integer lattice shift making one term in the literal
distance infimum0. A full new metric identification theorem is unnecessary.
Different real lifts of the same quotient point must not be counted as a
distinct-position tie. Existing source periodicity gives values; its actual
first/second jets transport through the accepted translation/coordinate
calculus, without reconstructing Fourier periodicity or endpoint Hessian laws.

## Literal Lifetime bridge: genuine new assembly, reused Hessian mathematics

Reuse `I4SourceLifetimePairFiniteness.actual_critical_coordinateGradient_zero`
for criticality transport, `I4SourceActualFoldCandidate.actual_hessian_coordinates`
for the full actual Hessian bilinear transport, accepted source C2 symmetry and
`I4LifetimeField.coordinates`. These are actual continuous-linear equivalences,
not an invented Pi/E2 isometry assertion.

The remaining private bridge must turn a nonzero symmetric actual Hessian
determinant into **∃j,HessianHasInertia** on Lifetime.E2. Reuse public Mathlib
finite-dimensional symmetric spectral theory, notably
`LinearMap.IsSymmetric.eigenvectorBasis`, its eigenvalue/eigenvector action and
orthonormal decomposition. The Hessian's associated self-adjoint operator has
no zero eigenvalues; spans of the negative and positive eigenbasis parts are
genuine complementary submodules with dimensions j and2−j and the required
strict quadratic signs. This is an actual coordinate/spectral/submodule
assembly, not an assumed inertia certificate. Do not redo spectral theory,
copy56's private planar inertia chain, or impose a nonzero first diagonal
pivot. The zero-diagonal saddle must remain covered. Existing public diagonal
inertia engines may be used where appropriate without adding public API.

Combining remote/pin nondegeneracy, the three value-comparison cases and the
exact gap-law sampler identity yields the displayed literal IsMorseDistinct
endpoint. Smoothness and periodicity remain automatic accepted facts.

## Evidence and nonclaims

`CONTROLS.md` fixes the actual DB·θ omission as the **one** future mutation,
nonorthogonal finite normalization,3/5 row and dummy-coordinate ledgers, an
actual global positive-gap specialization, and an equal-height forced-pin-tie
**positive limit control**. It introduces no second negative campaign.

The lexical route is **settled before proper PRECODE/control freeze**. All
production adapters remain private. Source-local **private positive
specializations** directly invoke the normalization/3–5 row/dummy/inertia
adapters on internally obtained actual48/53 finite families, the actual
solved-source θ maps, and four honestly labeled finite symmetric forms. These
specializations are inventoried and covered by the one production strict and
kernel qualification; they create no public API. Production imports no old57
scratch Controls object. The generic normal equation is used on actual source
families in the main proof. If an optional source-local cosine-formula
specialization is included, it must invoke the actual new private adapter;
symbolic source parameters may then be identified with actual a0,a1 by scratch
controls.

Separately, ordinary scratch `GapMorseDistinctControls` imports the qualified
new production module and the already qualified57 `FreeCoordinateControls`
object **only in scratch**. It reuses the old χ facts and proves the new actual
φ/B/g/θ/DB·θ mismatch, nonorthogonal arithmetic, public global specialization
and positive k=0 limit. It does not claim direct calls of production-private
adapters. The sole negative imports **only** the new Controls module's ordinary
`dropped_DBtheta_eq_iff_false`, after the counterexample passes. No
foreign/mangled private names, source concatenation, untracked copied source or
old57 campaign. Production and scratch-Controls coverage are reported
separately. Every complete future helper section/imports/provenance freezes
before one integration, with zero standalone helper execution.

Future qualification is new-module-only: retain every actual attempt/snapshot/
command/time/exit/full original stream and helper amendment/source-object
lineage; exact successful strict result reused after freeze/cut; full actual
owned inventory including private/data/generated/foreign constants; standard
`propext`, `Classical.choice`, `Quot.sound` only; meaningful controls; exactly one
sole counterexample-backed False and exactly one own-module kernel. No
sorry/admit/custom axiom/native_decide/implemented_by/umbrella import/private
foreign generated API or .ilean refresh. Root alone owns proper
PRECODE/pickup/timing/shared metadata/cache/config/Git/registration/external
publication. No old proof/kernel/audit/control/hash campaign is reopened.

This supplies a global **Morse/distinct-value** source-law join only. It does
not supply canonical intrinsic H0 labels/once-counting, a Borel elder selector,
marked Rice/counting identities, integrability/density versions, Parent A/B,
or a scientific-status promotion. The original research goal remains active.

Canonical authority carried without implying link reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
