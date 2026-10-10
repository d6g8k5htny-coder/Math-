import PushedHeight
import Mathlib.Analysis.Calculus.BumpFunction.InnerProduct
import Mathlib.Topology.Algebra.Support

noncomputable section
#eval IO.eprintln "BOUNDARY imports"
set_option backward.isDefEq.respectTransparency false
open Filter Set SourceCoordinates SourceNormalForm SourcePushedHeight
open MorseCongruence
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius
namespace SourceCompactCutoff
attribute [local instance] I4TorusC4.actualChartedSpace
attribute [local instance] Classical.propDecidable

def cutoffBump {n : ℕ} (ρ : ℝ) (hρ : 0 < ρ) : ContDiffBump (0 : E n) :=
  ⟨ρ/4, ρ/2, by linarith, by linarith⟩


#eval IO.eprintln "BOUNDARY bump"
def beta {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ) (z : E k × E (n-k)) : ℝ :=
  cutoffBump (n := n) ρ hρ ((split hk).symm z)

def K {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) : Set (E k × E (n-k)) :=
  split hk '' Metric.closedBall 0 (ρ/2)

def M {n k : ℕ} (hk : k ≤ n) (ρ : ℝ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) : Set (X n) :=
  phi.symm '' K hk ρ

def extension {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n))
    (Q : (E k × E (n-k)) → X n) (x : X n) : X n :=
  if x ∈ U then beta hk ρ hρ (phi x) • Q (phi x) else 0

def V0 {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n)) : X n → X n :=
  extension hk ρ hρ phi U (Q0 phi.symm)

def V1 {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n)) : X n → X n :=
  extension hk ρ hρ phi U (Q1 phi.symm)


#eval IO.eprintln "BOUNDARY defs"
structure CompactGeometry {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (x0 : X n) : Prop where
  inner_one : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 → beta hk ρ hρ z = 1
  outer_zero : ∀ z, ρ/2 ≤ ‖(split hk).symm z‖ → beta hk ρ hρ z = 0
  beta_bounds : ∀ z, 0 ≤ beta hk ρ hρ z ∧ beta hk ρ hρ z ≤ 1
  compact_K : IsCompact (K hk ρ)
  compact_M : IsCompact (M hk ρ phi)
  K_target : K hk ρ ⊆ T
  M_physical : M hk ρ phi ⊆ U
  support0 : Function.support (V0 hk ρ hρ phi U) ⊆ M hk ρ phi
  support1 : Function.support (V1 hk ρ hρ phi U) ⊆ M hk ρ phi
  C1_0 : ContDiff ℝ 1 (V0 hk ρ hρ phi U)
  C1_1 : ContDiff ℝ 1 (V1 hk ρ hρ phi U)
  compact0 : HasCompactSupport (V0 hk ρ hρ phi U)
  compact1 : HasCompactSupport (V1 hk ρ hρ phi U)
  rate0 : ∀ x, fderiv ℝ F x (V0 hk ρ hρ phi U x) =
    if x ∈ U then beta hk ρ hρ (phi x) * (2 * ‖(phi x).2‖^2) else 0
  rate1 : ∀ x, fderiv ℝ F x (V1 hk ρ hρ phi U x) =
    if x ∈ U then beta hk ρ hρ (phi x) * (2 * (‖(phi x).1‖^2 + ‖(phi x).2‖^2)) else 0
  nonnegative0 : ∀ x, 0 ≤ fderiv ℝ F x (V0 hk ρ hρ phi U x)
  nonnegative1 : ∀ x, 0 ≤ fderiv ℝ F x (V1 hk ρ hρ phi U x)
  inner_rate0 : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 →
    fderiv ℝ F (phi.symm z) (V0 hk ρ hρ phi U (phi.symm z)) = 2 * ‖z.2‖^2
  inner_rate1 : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 →
    fderiv ℝ F (phi.symm z) (V1 hk ρ hρ phi U (phi.symm z)) =
      2 * (‖z.1‖^2 + ‖z.2‖^2)
  center0 : V0 hk ρ hρ phi U x0 = 0
  center1 : V1 hk ρ hρ phi U x0 = 0


#eval IO.eprintln "BOUNDARY structure"
theorem compact_cutoff_of_geometry {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (c : ℝ) (x0 : X n)
    (hgeo : LocalGeometry F phi T U c x0) (hsource : U ⊆ phi.source)
    (hrad : MorseCone.radiusBall ρ ⊆ T) : CompactGeometry hk ρ hρ F phi T U x0 := by


#eval IO.eprintln "BOUNDARY generic-target"
theorem actual_source_compact_cutoff {n : ℕ} {L : ℝ} [Fact (0 < L)]
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (PhysicalSpectral.hessian (L := L) omega x0).det ≠ 0)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) :
    ∃ (k : ℕ) (hk : k ≤ n) (P : E n ≃L[ℝ] X n) (s : Sym n → Sym n)
      (e : OpenPartialHomeomorph (E n) (E n))
      (D : MorseCone.NormalForm (I4Torus.SourceTorus n L) (E k) (E (n-k))),
      let J := PhysicalSpectral.signSym n k
      let M := TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap
      M 0 = J ∧ (∀ u, e u = theta J s M u) ∧
      e 0 = 0 ∧ e.symm 0 = 0 ∧ 0 ∈ e.source ∧ 0 ∈ e.target ∧
      HasFDerivAt e (ContinuousLinearMap.id ℝ (E n)) 0 ∧
      ContDiffOn ℝ 2 e e.source ∧ ContDiffOn ℝ 2 e.symm e.target ∧
      D.f = I4Torus.torusSourceField n L omega ∧
      D.p = I4Torus.torusProjection n L x0 ∧ D.c = I4Source.sourceField n L omega x0 ∧
      D.chart = (liftChart (L := L) x0).trans (physicalChart hk x0 P e) ∧
      (∀ q, D.chart q = split hk (e (P.symm (liftChart (L := L) x0 q - x0)))) ∧
      (∀ z, D.chart.symm z = I4Torus.torusProjection n L (x0 + P (e.symm ((split hk).symm z)))) ∧
      ContMDiffOn 𝓘(ℝ, X n) 𝓘(ℝ, E k × E (n-k)) 2 D.chart D.chart.source ∧
      ContMDiffOn 𝓘(ℝ, E k × E (n-k)) 𝓘(ℝ, X n) 2 D.chart.symm D.chart.target ∧
      LocalGeometry (I4Source.sourceField n L omega) (physicalChart hk x0 P e)
        D.chart.target ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target)
        D.c x0 ∧
      CompactGeometry hk D.ρ D.hρ (I4Source.sourceField n L omega)
        (physicalChart hk x0 P e) D.chart.target
        ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target) x0 := by


#eval IO.eprintln "BOUNDARY actual-target"
end SourceCompactCutoff
