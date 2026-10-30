import Lifetime
import TorusTopology

/-!
# Finite literal critical set on the actual period-lattice quotient

C293: deterministic formal composition of the finite-critical-set step of C292.
The inputs below are the literal Lifetime predicates and C263 torus projection.
No finite event list, inverse certificate, Morse normal form or closed-level path
is supplied as a hypothesis.
-/

noncomputable section

open Set Topology
open UniversalLaw.Spec.Lifetime
open TorusFiltration

namespace TorusMorseFinite

theorem literal_hessian_eq_fderiv {d : ℕ} (g : E d → ℝ)
    (x v w : E d) :
    hessian d g x v w = fderiv ℝ (fderiv ℝ g) x v w := by
  simp [hessian, iteratedFDeriv_two_apply]

theorem literal_hessian_symmetric {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g) (x v w : E d) :
    hessian d g x v w = hessian d g x w v := by
  rw [literal_hessian_eq_fderiv, literal_hessian_eq_fderiv]
  exact ((hsmooth 2).contDiffAt.isSymmSndFDerivAt (by simp)).eq v w

theorem inertia_fderiv_injective {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g) {x : E d} {j : ℕ}
    (hinertia : HessianHasInertia d g x j) :
    Function.Injective (fderiv ℝ (fderiv ℝ g) x) := by
  let B := fderiv ℝ (fderiv ℝ g) x
  have hz : ∀ z : E d, B z = 0 → z = 0 := by
    intro z hzero
    obtain ⟨V, W, hcompl, _, _, hneg, hpos⟩ := hinertia
    obtain ⟨v, w, hv, hw, hvw⟩ :=
      Submodule.codisjoint_iff_exists_add_eq.mp hcompl.codisjoint z
    have hBv : B v v + B w v = 0 := by
      have h := congrArg (fun A : E d →L[ℝ] ℝ => A v) hzero
      simpa only [← hvw, map_add, add_apply, zero_apply] using h
    have hBw : B v w + B w w = 0 := by
      have h := congrArg (fun A : E d →L[ℝ] ℝ => A w) hzero
      simpa only [← hvw, map_add, add_apply, zero_apply] using h
    have hsym : B w v = B v w := by
      simpa only [B, ← literal_hessian_eq_fderiv] using
        literal_hessian_symmetric hsmooth x w v
    have heq : hessian d g x v v = hessian d g x w w := by
      simp only [literal_hessian_eq_fderiv]
      change B v v = B w w
      linarith
    have hv0 : v = 0 := by
      by_contra hv0
      have hn := hneg v hv hv0
      by_cases hw0 : w = 0
      · have hww : hessian d g x w w = 0 := by
          simp [hw0, literal_hessian_eq_fderiv]
        linarith
      · have hp := hpos w hw hw0
        linarith
    have hw0 : w = 0 := by
      by_contra hw0
      have hp := hpos w hw hw0
      have hvv : hessian d g x v v = 0 := by
        simp [hv0, literal_hessian_eq_fderiv]
      linarith
    simpa [hv0, hw0] using hvw.symm
  intro u v huv
  have hzero : B (u - v) = 0 := by simp [map_sub, huv, B]
  exact sub_eq_zero.mp (hz (u - v) hzero)

theorem inertia_fderiv_equiv {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g) {x : E d} {j : ℕ}
    (hinertia : HessianHasInertia d g x j) :
    ∃ e : E d ≃L[ℝ] (E d →L[ℝ] ℝ),
      (e : E d →L[ℝ] (E d →L[ℝ] ℝ)) = fderiv ℝ (fderiv ℝ g) x := by
  let J : E d ≃L[ℝ] (E d →L[ℝ] ℝ) :=
    (InnerProductSpace.toDual ℝ (E d)).toContinuousLinearEquiv
  let B := fderiv ℝ (fderiv ℝ g) x
  let A : E d →L[ℝ] E d := J.symm.toContinuousLinearMap.comp B
  have hA : Function.Injective A :=
    J.symm.injective.comp (inertia_fderiv_injective hsmooth hinertia)
  let eA : E d ≃L[ℝ] E d :=
    (LinearEquiv.ofInjectiveEndo A.toLinearMap hA).toContinuousLinearEquiv
  refine ⟨eA.trans J, ?_⟩
  apply ContinuousLinearMap.ext
  intro v
  change J (J.symm (B v)) = B v
  exact J.apply_symm_apply (B v)

theorem literal_critical_isolated {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g) {x : E d}
    (hcritical : IsCriticalPoint d g x) {j : ℕ}
    (hinertia : HessianHasInertia d g x j) :
    ∃ U : Set (E d), IsOpen U ∧ x ∈ U ∧
      ∀ y ∈ U, IsCriticalPoint d g y → y = x := by
  obtain ⟨e, he⟩ := inertia_fderiv_equiv hsmooth hinertia
  have hD : ContDiff ℝ 1 (fderiv ℝ g) :=
    (contDiff_succ_iff_fderiv.mp (hsmooth 2)).2.2
  have hderiv : HasFDerivAt (fderiv ℝ g)
      (e : E d →L[ℝ] (E d →L[ℝ] ℝ)) x := by
    rw [he]
    exact (hD.differentiable (by norm_num) x).hasFDerivAt
  let p := hD.contDiffAt.toOpenPartialHomeomorph (fderiv ℝ g) hderiv (by norm_num)
  have hxp : x ∈ p.source :=
    hD.contDiffAt.mem_toOpenPartialHomeomorph_source hderiv (by norm_num)
  refine ⟨p.source, p.open_source, hxp, ?_⟩
  intro y hy hcy
  apply p.injOn hy hxp
  change fderiv ℝ g y = fderiv ℝ g x
  exact hcy.trans hcritical.symm

theorem literal_fderiv_periodic {d : ℕ} {L : ℝ} {g : E d → ℝ}
    (hperiodic : IsLPeriodic d L g) (x : E d) (k : Fin d → ℤ) :
    fderiv ℝ g (x + torus_latticeVec d L k) = fderiv ℝ g x := by
  have heq : (fun y : E d => g (y + torus_latticeVec d L k)) = g := by
    funext y
    simpa only [torus_latticeVec, latticeVec] using hperiodic y k
  rw [← fderiv_comp_add_right, heq]

theorem literal_fderiv_respects {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g) (x y : E d)
    (hxy : QuotientAddGroup.leftRel (torus_periodLattice d L hL).toAddSubgroup x y) :
    fderiv ℝ g x = fderiv ℝ g y := by
  have hq : torus_proj d L hL x = torus_proj d L hL y := Quotient.sound hxy
  obtain ⟨k, rfl⟩ := (torus_proj_eq_iff d L hL x y).mp hq
  exact (literal_fderiv_periodic hperiodic x k).symm

def quotientDerivative (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) :
    torus_quotient d L hL → (E d →L[ℝ] ℝ) :=
  Quotient.lift (fderiv ℝ g) (literal_fderiv_respects hL hperiodic)

@[simp] theorem quotientDerivative_proj (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) (x : E d) :
    quotientDerivative d L hL g hperiodic (torus_proj d L hL x) =
      fderiv ℝ g x := rfl

theorem quotientDerivative_continuous {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g)
    (hsmooth : IsSmooth d g) :
    Continuous (quotientDerivative d L hL g hperiodic) :=
  ((hsmooth 1).continuous_fderiv (by norm_num)).quotient_lift
    (literal_fderiv_respects hL hperiodic)

/-- The full image of all literal critical points, on C263's actual quotient. -/
def quotientCriticalSet (d : ℕ) (L : ℝ) (hL : 0 < L) (g : E d → ℝ) :
    Set (torus_quotient d L hL) :=
  torus_proj d L hL '' {x : E d | IsCriticalPoint d g x}

theorem mem_quotientCriticalSet_iff {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g)
    (q : torus_quotient d L hL) :
    q ∈ quotientCriticalSet d L hL g ↔
      quotientDerivative d L hL g hperiodic q = 0 := by
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact hx
  · intro hq
    obtain ⟨x, rfl⟩ := torus_proj_surjective d L hL q
    exact ⟨x, hq, rfl⟩

theorem quotientCriticalSet_closed {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g)
    (hsmooth : IsSmooth d g) :
    IsClosed (quotientCriticalSet d L hL g) := by
  have heq : quotientCriticalSet d L hL g =
      {q | quotientDerivative d L hL g hperiodic q = 0} := by
    ext q
    exact mem_quotientCriticalSet_iff hL hperiodic q
  rw [heq]
  exact isClosed_eq (quotientDerivative_continuous hL hperiodic hsmooth) continuous_const

theorem quotientCriticalSet_discrete {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g)
    (hsmooth : IsSmooth d g)
    (hmorse : ∀ x : E d, IsCriticalPoint d g x →
      ∃ j : ℕ, HessianHasInertia d g x j) :
    IsDiscrete (quotientCriticalSet d L hL g) := by
  rw [isDiscrete_iff_forall_mem_exists_isOpen]
  rintro q ⟨x, hx, rfl⟩
  obtain ⟨j, hj⟩ := hmorse x hx
  obtain ⟨U, hU, hxU, hiso⟩ := literal_critical_isolated hsmooth hx hj
  refine ⟨torus_proj d L hL '' U,
    (torus_proj_isCoveringMap d L hL).isOpenMap U hU, ?_⟩
  ext q
  constructor
  · rintro ⟨⟨y, hy, rfl⟩, hcy⟩
    have hyc : IsCriticalPoint d g y :=
      (mem_quotientCriticalSet_iff hL hperiodic _).mp hcy
    have hyx := hiso y hy hyc
    simp [hyx]
  · intro hq
    have hqx := Set.mem_singleton_iff.mp hq
    subst q
    exact ⟨⟨x, hxU, rfl⟩, ⟨x, hx, rfl⟩⟩

/-- Core finiteness only needs nondegeneracy at critical points; distinct heights
are not used. No finiteness conclusion is supplied in the assumptions. -/
theorem quotientCriticalSet_finite_of_inertia {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hsmooth : IsSmooth d g)
    (hperiodic : IsLPeriodic d L g)
    (hmorse : ∀ x : E d, IsCriticalPoint d g x →
      ∃ j : ℕ, HessianHasInertia d g x j) :
    (quotientCriticalSet d L hL g).Finite := by
  have hc : IsCompact (quotientCriticalSet d L hL g) := by
    simpa only [Set.univ_inter] using
      (torus_compact d L hL).inter_right
        (quotientCriticalSet_closed hL hperiodic hsmooth)
  exact hc.finite (quotientCriticalSet_discrete hL hperiodic hsmooth hmorse)

/-- C292-facing theorem on the literal Morse-distinct locus. The result in fact
holds for every natural dimension; C292 may instantiate it at its `d ≥ 1`. -/
theorem quotientCriticalSet_finite (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g)
    (hperiodic : IsLPeriodic d L g) (hmorse : IsMorseDistinct d L g) :
    (quotientCriticalSet d L hL g).Finite :=
  quotientCriticalSet_finite_of_inertia hL hsmooth hperiodic hmorse.1

end TorusMorseFinite
