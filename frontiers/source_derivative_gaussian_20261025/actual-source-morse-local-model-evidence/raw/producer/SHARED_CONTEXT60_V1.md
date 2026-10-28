# Frozen shared lexical context60 V1

ROOT_GO issued14:42:03.059235UTC28October2026, actual fresh pickup6471999400;
PRECODE4e41aaec1d6a63d2425112141372a2d23d7c7409. New checkpoint15:20 and
terminal16:30UTC28October2026 or invocation end are unchanged. Controls were
adopted before all60 source/harness/helper proof text. Original26October
bounds are historical and unreset. Scientific effect NONE/same-family0.

Each helper must read and ACK this exact complete context/signature boundary
BEFORE writing proof text. If an import/signature change is necessary, agree
the explicit supplement first. Each complete original SECTION/imports/
provenance freezes before ONE production integration, ZERO standalone Lean,
name-probe/build/check/kernel/control/audit/hash/object execution. Producer
owns all actual amendment patches and final-module qualification. No59
source/private helper inspection or dependency; root owns shared metadata,
cache, Git and external activity.

## Imports and outer context

```text
import SourceActualFoldCandidate
import SourceFiniteTrig
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.LinearAlgebra.QuadraticForm.Signature
import Mathlib.Analysis.Calculus.TaylorIntegral
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Analysis.Calculus.ContDiff.FiniteDimension
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Topology.OpenPartialHomeomorph.IsImage

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open Set MeasureTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
  I4SourceDerivativeGaussian I4SourceSmoothConditional I4SourceFinitePinKernel
  I4SourceFiniteTrig I4LifetimeField UniversalLaw.Spec.Lifetime
namespace I4SourceActualMorseLocalModel
```

All signatures below are PRIVATE. No helper adds a public declaration.
The producer supplies these definitions before helper integration:

```text
private abbrev Point2 := Fin 2 → ℝ
private abbrev E2 := UniversalLaw.Spec.Lifetime.E 2
private abbrev Mat2 := Matrix (Fin 2) (Fin 2) ℝ
private def basis2 (i : Fin 2) : Point2 := Pi.single i 1
private def sign2 (j : ℕ) (i : Fin 2) : ℝ := if i.val < j then -1 else 1
private def jMatrix (j : ℕ) : Mat2 := Matrix.diagonal (sign2 j)
private def normalizedField (g : E2 → ℝ) (X : E2)
    (P : Point2 ≃L[ℝ] E2) (y : Point2) : ℝ := g (X + P y) - g X
private def taylorMatrix (h : Point2 → ℝ) (y : Point2) : Mat2 :=
  fun i k => ∫ t : ℝ in (0:ℝ)..1,
    (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]
private def orderedNormalization (g : E2 → ℝ) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2) : Prop :=
  ∀ u v : Point2, iteratedFDeriv ℝ 2 g X ![P u,P v] =
    2 * ∑ i : Fin 2, sign2 j i * u i * v i
private def criticalConeBasis (g : E2 → ℝ) (X : E2)
    (phi : OpenPartialHomeomorph E2 Point2) : Prop :=
  ∀ O : Set E2, IsOpen O → X ∈ O →
    ∃ V : Set E2, IsOpen V ∧ X ∈ V ∧ V ⊆ O ∩ phi.source ∧
      IsPathConnected (V ∩ {x | g X ≤ g x})
private def localModel (g : E2 → ℝ) (X : E2) (j : ℕ)
    (phi : OpenPartialHomeomorph E2 Point2) : Prop :=
  X ∈ phi.source ∧ phi X = 0 ∧ (0 : Point2) ∈ phi.target ∧
    ContDiffOn ℝ 1 phi phi.source ∧ ContDiffOn ℝ 1 phi.symm phi.target ∧
    (∀ x ∈ phi.source, g x = g X + ∑ i : Fin 2, sign2 j i * (phi x i)^2) ∧
    criticalConeBasis g X phi
```

The aliases/propositions are private convenience only. The sole final public
statement uses the existing literal carrier names and transparent sign
expression, not a leaked private relation or alias.

## Helper A — finite2 J branch

Owner `/root/remote_jet_gaussian_construct`, scratch
`/workspace/scratch/morse-local-model-finite2-branch-text`.
Supply the following exact private definitions and complete lemmas:

```text
private def jBranchDomain (j : ℕ) : Set Mat2 :=
  {M | 0 < (jMatrix j * M).det ∧
    0 < (jMatrix j * M).trace + 2 * Real.sqrt ((jMatrix j * M).det)}
private def jBranch (j : ℕ) (M : Mat2) : Mat2 :=
  (Real.sqrt ((jMatrix j * M).trace +
      2 * Real.sqrt ((jMatrix j * M).det)))⁻¹ •
    (jMatrix j * M + Real.sqrt ((jMatrix j * M).det) • (1 : Mat2))
private theorem jBranchDomain_isOpen (j : ℕ) : IsOpen (jBranchDomain j)
private theorem jMatrix_mem_jBranchDomain (j : ℕ) : jMatrix j ∈ jBranchDomain j
private theorem jBranch_center (j : ℕ) : jBranch j (jMatrix j) = 1
private theorem jBranch_contDiffOn (j : ℕ) :
  ContDiffOn ℝ 1 (jBranch j) (jBranchDomain j)
private theorem jBranch_congruence (j : ℕ) (M : Mat2)
    (hM : M ∈ jBranchDomain j) (hs : M.transpose = M) :
  (jBranch j M).transpose * jMatrix j * jBranch j M = M
```

Additional private support is allowed. There is no `j≤2` premise: every
diagonal entry of jMatrix is ±1 for every natural j, so the stated finite2
branch identities hold. Z=jMatrix*M is J-self-adjoint; ordinary symmetry of
Z must not be assumed. All positive root arguments and scalar denominators
are derived from the exact domain. No matrix-square-root or desired
congruence premise may replace the new proof.

## Helper B — actual literal inertia to ordered constant normalization

Owner `/root/intrinsic_h0_packaging`, scratch
`/workspace/scratch/morse-local-model-inertia-normalizer-text`.
Supply the exact private endpoint (additional private support allowed):

```text
private theorem actual_ordered_normalizer {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hi : HessianHasInertia 2 (actualField 2 L omega) X j) :
  j ≤ 2 ∧ ∃ P : Point2 ≃L[ℝ] E2,
    orderedNormalization (actualField 2 L omega) X j P
```

The complete output is the full bilinear identity, not merely an equality
of diagonal evaluations/determinants. Negative columns come first. Derive
symmetry, zero radical, genuine finite-dimensional normalizer and literal
index agreement internally. A constant spectral/Sylvester/basis choice at
the fixed source point is permitted. Do not require an ordinary-coordinate
nonzero diagonal, a desired chart or a supplied desired normalization.

## Producer-owned interfaces available to fixture helper

Producer alone owns actual Taylor C¹/remainder/IFT/cone construction. The
following exact private interfaces are frozen so fixtures can directly
exercise their explicit P (definitions first, theorems before fixtures):

```text
private def normalizedResponse (g : E2 → ℝ) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2) (y : Point2) : Point2 :=
  jBranch j (taylorMatrix (normalizedField g X P) y) *ᵥ y

private theorem actual_taylorMatrix_zero {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
  taylorMatrix (normalizedField (actualField 2 L omega) X P) 0 = jMatrix j

private theorem normalizedResponse_hasFDerivAt {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
  HasFDerivAt (normalizedResponse (actualField 2 L omega) X j P)
    (ContinuousLinearMap.id ℝ Point2) 0

private theorem normalized_localModel {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ) (hj : j ≤ 2)
    (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
  ∃ phi : OpenPartialHomeomorph E2 Point2,
    localModel (actualField 2 L omega) X j phi
```

All localModel output components, including criticalConeBasis, are the same
chart. Additional private producer support handles actual order3 dominated
integrals, exact Taylor formula, matrix response derivative and cone
pullback. These internal normalization premises are discharged both by the
public actual normalizer and explicit actual finite-source fixture ledgers;
none becomes a desired premise in the public theorem.

## Helper C — actual four fixtures plus separate ordinary Controls

Owner `/root/actual_canonical_partner_preflight`, scratch
`/workspace/scratch/morse-local-model-actual-fixtures-text`.
Supply a complete PRIVATE production SECTION, imports/provenance and frozen
original IDs. The four actual L=2/X=0 samples are exactly
finiteShiftSample(toSource 2 p)(zeroSample 2 2) for fields:

- minimum `-cos(pi*x)-cos(pi*y)`, j0;
- maximum `cos(pi*x)+cos(pi*y)`, j2;
- diagonal saddle `cos(pi*x)-cos(pi*y)`, j1;
- zero-diagonal saddle `sin(pi*x)*sin(pi*y)`, j1.

Own private names under prefix fixture_ may be chosen in the section, but
the exact producer interfaces above are fixed. For first3 use explicit
P=sqrt(2)/pi*I; for zero-diagonal use P=pi^-1[[1,1],[-1,1]] (negative first).
Derive actual field/gradient/Hessian/complementary-subspace inertia/full
orderedNormalization, invertibility and P→2J. Directly call
actual_taylorMatrix_zero, jBranch_center at this actual center,
normalizedResponse_hasFDerivAt and normalized_localModel with these P.
Retain model/cone consequences on the actual source samples. Do not assert
equality of noncanonical chosen charts. No foreign-private representedSample
or copied private finite-pairing proof, no old57 scratch dependency.

Supply ONE separately frozen complete ordinary Controls SECTION importing
qualified SourceActualMorseLocalModel and old accepted public APIs only.
It uses namespace I4MorseLocalModelControls, reconstructs independently the
SAME actual minimum/P/h and weighted/unweighted scalar entries at0. Export
ordinary facts correctTaylorEntry_eq_one, omittedTaylorEntry_eq_two and
omittedTaylorEntry_ne_one; definitions are ordinary scratch names. Also
specialize the sole public endpoint to the actual minimum with genuine
criticality/inertia. Its code may not access production private names or
copy production private proofs. ZERO helper execution; only later ordinary
Controls compilation qualifies it, separately from the production kernel.

The sole future False imports ONLY the qualified ordinary Controls object
after its actual1vs2 counterproof PASS; falsely claims omittedTaylorEntry=1.
Only (1-t) is omitted; field/P/amplitude/point/directions/measure/interval
are unchanged. The mutant2I remains invertible. No negative execution or
kernel occurs prematurely. All actual producer amendments must be retained
against each original complete section (production and Controls separately).

## Shared reuse and qualification limits

Completed applicable old source/proof/check/hash evidence is reused. No
handoff, lease, new session or source cut justifies replay. Final public
contract remains exactly one authored Prop/no public data; helper private
data/generated declarations are classified honestly in the actual final
inventory. Final strict, exactly one own kernel and the one concrete
negative belong to the producer's final source/control campaign, not helper
objects. Root alone performs metadata/cache/Git/publication actions.
