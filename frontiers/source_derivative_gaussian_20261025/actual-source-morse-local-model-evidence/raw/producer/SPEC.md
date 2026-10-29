# DRAFT — actual-source C¹ quadratic local model

Prospective module `SourceActualMorseLocalModel`, namespace
`I4SourceActualMorseLocalModel`. 26October2026. Design only; not adopted
PRECODE, a native claim, GO, implementation or qualification. Scientific
effect NONE; same-family/provider-distinct credit0. Root owns adoption and
the exact later lexical/source/control freeze. No timers are set here.

The accepted design source is
`/workspace/scratch/actual-source-morse-local-model-preflight/REPORT.md`,
which stays unchanged. Accepted conventional local-Morse mathematics and
completed applicable old API verification are reused under
`/workspace/AGENTS.md`.

## Sole public endpoint

Exactly **one public proposition and no public data** is proposed:
`I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel`.
All auxiliary functional/matrix definitions and lemmas are private.

Its complete mathematical contract is as follows. For each real `L>0`,
actual `omega : SmoothSample 2 L`, `X : Lifetime.E 2`, and natural `j`, let
`g` mean the literal `I4LifetimeField.actualField 2 L omega`. Inputs are

- `IsCriticalPoint 2 g X`;
- `HessianHasInertia 2 g X j`.

Derive `j<=2` and an actual
`phi : OpenPartialHomeomorph (Lifetime.E 2) (Fin 2 → ℝ)` satisfying the
following conjunction:

1. `X∈phi.source`, `phi X=0`, and `0∈phi.target`.
2. `ContDiffOn ℝ 1 phi phi.source` and
   `ContDiffOn ℝ 1 phi.symm phi.target`.
3. For every `x∈phi.source`, the exact identity

       g x = g X + sum i:Fin 2, sign_j(i) * (phi x i)^2,
       sign_j(i) = if i.val < j then -1 else 1.

4. For every ambient open `O` containing `X`, there exists ambient open `V`
   with `X∈V`, `V⊆O∩phi.source`, and

       IsPathConnected (V ∩ {x | g X <= g x}).

This bundles a coherent critical-level neighborhood consequence of the same
local model; it introduces no second public theorem. `j=0,1,2` respectively
give minimum, saddle and maximum. The saddle includes a genuine nonsingular
Hessian with zero ordinary-coordinate diagonal.

The literal inertia/criticality inputs are legitimate point hypotheses,
later derived from `Lifetime.IsMorseDistinct`. Actual source C∞ supplies the
needed derivatives through order3 internally. No supplied desired chart,
normal-form equation, nonzero coordinate pivot, component transition,
regular-slab flow, desired probability or Morse certificate replaces that
derivation. No finite critical set or global genericity premise is needed.

## Private construction contract

Write `Point2=Fin 2 → ℝ` privately. The following are implementation
obligations, with private names/inventory finalized only by a later freeze:

- Derive Hessian symmetry/nondegeneracy from actual smoothness and literal
  complementary-sign inertia. Normalize the quadratic form `D²g(X)/2`
  through a constant genuine continuous linear equivalence
  `P:Point2≃L[ℝ]E2`, with `Pᵀ D²g(X) P=2J` and
  `J=diag(sign_j)`. Prove the index/sign ordering, including `j<=2`.
- For `h(y)=g(X+P y)-g X`, define the actual matrix
  `M_ij(y)=∫₀¹(1-t)D²h(t*y)[basis_i,basis_j]dt`.
  Derive symmetry, C¹ regularity, `M(0)=J`, and `h(y)=yᵀM(y)y`.
  Public order1 integral Taylor and dominated first differentiation plus
  continuity use only compact/source-order3 bounds. The factor `1/2` in
  `∫₀¹(1-t)` is indispensable.
- On an actual neighborhood of `J`, derive the positive square-root
  arguments and the C¹ branch
  `R(M)=(J*M+sqrt(det(J*M))*I)/sqrt(trace(J*M)+2sqrt(det(J*M)))`.
  Derive `R(J)=I` and `R(M)ᵀ J R(M)=M` from the exact finite2 algebra,
  including J-self-adjointness; ordinary symmetry of `J*M` is not assumed.
- For `e(y)=R(M(y))*y`, derive derivative identity at0. Apply the public
  order1 inverse-function theorem to the actual physical coordinate map.
  Restrict to the normal-form validity neighborhood and to the finite-order
  C¹ source/target loci. All inverse and centering facts are proved outputs.
- Derive star convexity about0 of the signed homogeneous quadratic cone
  intersected with a sufficiently small centered ball. Transfer its path
  connectivity through the actual local inverse to obtain item4.

No measurable/random normalizer or chart selection, uniform sample-dependent
radius, eigenvalue floor or global O(2) source-law invariance is asserted.
These are deterministic coordinates for the same field. The result is C¹;
no unconsumed C∞ coordinate/inverse or smooth-integral library is proposed.

## Scope and dependencies

Consume only old accepted public source/Mathlib APIs. This module need not
import proposed/current59, use59 private declarations, or depend on58's new
implementation. A future59-before60 registration order is root's separate
process decision, not a mathematical dependency or a lease created here.

The exact local quotient-chart transfer to the product AddCircle torus,
regular/submersion boundary coordinates, regular-slab transport, component
events, elder induction, exhaustive counts and probability/Rice joins remain
separate. Item4 concerns the real-cover critical superlevel at `g X`; it does
not by itself assert global path connectivity or arbitrary closed-set
connectedness implies path connectivity.

No implementation, helper proof text, Lean/name probe, harness, build, check,
kernel, hash, Git/cache/shared-metadata or external action accompanies these
drafts. Delivery does not mean root adoption, successor reading or acceptance.
