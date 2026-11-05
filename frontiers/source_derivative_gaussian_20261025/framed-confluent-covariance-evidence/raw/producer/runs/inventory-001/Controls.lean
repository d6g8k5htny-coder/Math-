import SourceFramedConfluentCovariance

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology Interval
open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier I4SourceGaussian
open I4SourceCovariance I4SourceDerivativeGaussian I4SourceDerivativeContinuity
open I4SourceFiniteTrig I4SourceFinitePinKernel I4SourceRemoteJetWitness I4SourceConfluentPins
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SourceFramedConfluentCovariance
open MeasureTheory ProbabilityTheory WithLp Set
namespace FramedConfluentControls

private def rows (f : (Fin 2 → ℝ) → ℝ) (p e n : Fin 2 → ℝ) (r : ℝ) : Fin 7 → ℝ :=
  ![(f (p-(r/2) • e)+f (p+(r/2) • e))/2,
    (fderiv ℝ f (p-(r/2) • e) e+fderiv ℝ f (p+(r/2) • e) e)/2,
    (fderiv ℝ f (p-(r/2) • e) n+fderiv ℝ f (p+(r/2) • e) n)/2,
    ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f (p+(r*t) • e) ![e,e],
    ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f (p+(r*t) • e) ![e,n],
    6*∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f (p+(r*t) • e) ![e,e,e],
    iteratedFDeriv ℝ 2 f p ![n,n] ]

private theorem coefficient_rows (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i : Fin 7) (m : SourceMode 2) :
    framedConfluentCoefficient L z R r i m =
      rows (modeCoefficient 2 L m) (coordinates 2 z) (coordinates 2 (R 0))
        (coordinates 2 (R 1)) r i := rfl

private def std : OrthonormalBasis (Fin 2) ℝ (E 2) := EuclideanSpace.basisFun (Fin 2) ℝ
private theorem std0 : coordinates 2 (std 0) = directionX := by ext i; fin_cases i <;> rfl
private theorem std1 : coordinates 2 (std 1) = directionY := by ext i; fin_cases i <;> rfl

private theorem kernel_mass : (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)) = (1/6:ℝ) := by
  rw [intervalIntegral.integral_sub intervalIntegrable_const
    ((continuous_id.pow 2).intervalIntegrable _ _)]
  norm_num

private theorem rows_zero (f : (Fin 2 → ℝ) → ℝ) (p e n : Fin 2 → ℝ) :
    rows f p e n 0 = ![f p,fderiv ℝ f p e,fderiv ℝ f p n,
      iteratedFDeriv ℝ 2 f p ![e,e],iteratedFDeriv ℝ 2 f p ![e,n],
      iteratedFDeriv ℝ 3 f p ![e,e,e],iteratedFDeriv ℝ 2 f p ![n,n] ] := by
  unfold rows
  simp only [zero_div,zero_mul,zero_smul,sub_zero,add_zero]
  ext i
  fin_cases i
  · change (f p+f p)/2=f p; ring
  · change (fderiv ℝ f p e+fderiv ℝ f p e)/2=fderiv ℝ f p e; ring
  · change (fderiv ℝ f p n+fderiv ℝ f p n)/2=fderiv ℝ f p n; ring
  · change (∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f p ![e,e]) = _; norm_num
  · change (∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f p ![e,n]) = _; norm_num
  · change 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f p ![e,e,e]) = _
    rw [intervalIntegral.integral_mul_const,kernel_mass]; ring
  · rfl

-- This checks only the new fixed-axis specialization join; the old pin proof is reused.
theorem standard_axis_coefficient_join (L r : ℝ) (i : Fin 6) (m : SourceMode 2) :
    framedConfluentCoefficient L 0 std r (Fin.castAdd 1 i) m =
      I4SourceConfluentLimits.regularizedPinCoefficient L r i m := by
  rw [coefficient_rows,std0,std1]
  simp only [map_zero]
  fin_cases i <;>
    simp only [rows,I4SourceConfluentLimits.regularizedPinCoefficient,
      I4SourceConfluentLimits.weightedDerivativeIntegral,
      I4SourceConfluentLimits.modeF,I4SourceConfluentLimits.modeH,
      I4SourceConfluentLimits.modeF_deriv,I4SourceConfluentLimits.peanoCubic]
  all_goals congr 2 <;> try (ext a; fin_cases a <;> simp [directionX,directionY])

private def frameOf (u : Fin 2 → E 2) (hu : Orthonormal ℝ u) :
    OrthonormalBasis (Fin 2) ℝ (E 2) :=
  OrthonormalBasis.mk hu ((hu.linearIndependent.span_eq_top_of_card_eq_finrank' (by simp [E])).ge)
private theorem frameOf_apply (u : Fin 2 → E 2) (hu : Orthonormal ℝ u) (i : Fin 2) :
    frameOf u hu i = u i := by simp [frameOf]

private def ratFamily : Fin 2 → E 2 :=
  ![toLp 2 ![(3/5:ℝ),4/5],toLp 2 ![(-4/5:ℝ),3/5]]
private theorem rat_orthonormal : Orthonormal ℝ ratFamily := by
  rw [orthonormal_iff_ite]
  intro i j
  fin_cases i <;> fin_cases j <;>
    norm_num [ratFamily,EuclideanSpace.inner_eq_star_dotProduct,dotProduct,Fin.sum_univ_two]
private def ratFrame := frameOf ratFamily rat_orthonormal
private def midpoint : E 2 := toLp 2 ![(1/3:ℝ),-1/5]
private theorem midpoint_domain : ∀ a : Fin 2, |coordinates 2 midpoint a| ≤ |(-2:ℝ)|/2 := by
  intro a; fin_cases a <;> norm_num [midpoint,coordinates_apply]

private def reflectedFamily (R : OrthonormalBasis (Fin 2) ℝ (E 2)) : Fin 2 → E 2 := ![R 0,-R 1]
private theorem reflected_orthonormal (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :
    Orthonormal ℝ (reflectedFamily R) := by
  rw [orthonormal_iff_ite]
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [reflectedFamily,R.inner_eq_one,R.inner_eq_zero (show (0:Fin 2) ≠ 1 by decide),
      R.inner_eq_zero (show (1:Fin 2) ≠ 0 by decide)]
private def reflected (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :=
  frameOf (reflectedFamily R) (reflected_orthonormal R)
private theorem reflected0 (R : OrthonormalBasis (Fin 2) ℝ (E 2)) : reflected R 0 = R 0 := by
  simp [reflected,frameOf_apply,reflectedFamily]
private theorem reflected1 (R : OrthonormalBasis (Fin 2) ℝ (E 2)) : reflected R 1 = -R 1 := by
  simp [reflected,frameOf_apply,reflectedFamily]
private def signs : Fin 7 → ℝ := ![1,1,-1,1,-1,1,1]

private theorem second_neg (T : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => Fin 2 → ℝ) ℝ)
    (e n : Fin 2 → ℝ) : T ![e,-n] = -T ![e,n] := by
  have h := T.toMultilinearMap.map_smul_univ ![(1:ℝ),-1] ![e,n]
  simpa [Fin.prod_univ_succ] using h
private theorem second_neg_both (T : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => Fin 2 → ℝ) ℝ)
    (n : Fin 2 → ℝ) : T ![-n,-n] = T ![n,n] := by
  have h := T.toMultilinearMap.map_smul_univ (fun _ => (-1:ℝ)) ![n,n]
  simpa [Fin.prod_univ_succ] using h

theorem reflected_coefficient_signs (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i : Fin 7) (m : SourceMode 2) :
    framedConfluentCoefficient L z (reflected R) r i m =
      signs i * framedConfluentCoefficient L z R r i m := by
  rw [coefficient_rows,coefficient_rows,reflected0,reflected1,map_neg]
  fin_cases i
  · simp [rows,signs]
  · simp [rows,signs]
  · simp only [rows,signs,map_neg]
    ring
  · simp [rows,signs]
  · change (∫ t in (-1/2:ℝ)..(1/2:ℝ),
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z+(r*t) • coordinates 2 (R 0))
        ![coordinates 2 (R 0),-coordinates 2 (R 1)]) =
        (-1)*(∫ t in (-1/2:ℝ)..(1/2:ℝ),
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z+(r*t) • coordinates 2 (R 0))
        ![coordinates 2 (R 0),coordinates 2 (R 1)])
    simp_rw [second_neg]
    rw [intervalIntegral.integral_neg]
    ring
  · simp [rows,signs]
  · simpa only [rows,signs,one_mul] using
      second_neg_both (iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z))
        (coordinates 2 (R 1))

theorem reflected_gram_signs (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i j : Fin 7) :
    framedConfluentCovariance L z (reflected R) r i j =
      signs i * signs j * framedConfluentCovariance L z R r i j := by
  change (∑' m, framedConfluentCoefficient L z (reflected R) r i m *
    framedConfluentCoefficient L z (reflected R) r j m) = _
  simp_rw [reflected_coefficient_signs]
  calc
    _ = ∑' m, (signs i * signs j) *
        (framedConfluentCoefficient L z R r i m * framedConfluentCoefficient L z R r j m) := by
          apply tsum_congr; intro m; ring
    _ = _ := tsum_mul_left

theorem signed_nonaxis_actual (ω : SmoothSample 2 (-2)) :
    HasGaussianLaw (framedConfluentVector (-2) midpoint ratFrame (-1/3)) (smoothLaw 2 (-2)) ∧
    (∀ i j : Fin 7, cov[fun η => framedConfluentVector (-2) midpoint ratFrame (-1/3) η i,
      fun η => framedConfluentVector (-2) midpoint ratFrame (-1/3) η j;smoothLaw 2 (-2)] =
      framedConfluentCovariance (-2) midpoint ratFrame (-1/3) i j) ∧
    (fun i : Fin 6 => framedConfluentVector (-2) midpoint ratFrame (-1/3) ω (Fin.castAdd 1 i)) =
      confluentTransform (-1/3)
        ![actualField 2 (-2) ω (midpoint-((-1/3)/2) • ratFrame 0),
          actualField 2 (-2) ω (midpoint+((-1/3)/2) • ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3)/2) • ratFrame 0) (ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3)/2) • ratFrame 0) (ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3)/2) • ratFrame 0) (ratFrame 1),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3)/2) • ratFrame 0) (ratFrame 1)] := by
  have h := framedConfluentVector_actual (L := (-2)) (by norm_num) midpoint ratFrame (-1/3)
  exact ⟨h.1,h.2.1,h.2.2.2.2 (by norm_num) ω⟩

theorem reflected_nonaxis_law :
    HasGaussianLaw (framedConfluentVector (-2) midpoint (reflected ratFrame) (-1/3)) (smoothLaw 2 (-2)) :=
  (framedConfluentVector_actual (L := (-2)) (by norm_num) midpoint (reflected ratFrame) (-1/3)).1

theorem explicit_envelope_above_three :
    (∀ m, 0 ≤ 8*∑ j : Fin 4, orderModeBound (j:ℕ) 2 (-2) m) ∧
    Summable (fun m => orderModeBound 7 2 (-2) m*(8*∑ j : Fin 4, orderModeBound (j:ℕ) 2 (-2) m)) ∧
    (∀ z : E 2, ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ, ∀ i m,
      |framedConfluentCoefficient (-2) z R r i m| ≤ 8*∑ j : Fin 4, orderModeBound (j:ℕ) 2 (-2) m) := by
  have h := framedConfluent_family_bounds (L := (-2)) (by norm_num)
  exact ⟨h.1,h.2.1 7,h.2.2.1⟩

theorem same_constants_two_orientations :
    ∃ gamma Lambda delta : ℝ, 0 < gamma ∧ 0 < Lambda ∧ 0 < delta ∧ delta ≤ 1 ∧ delta ≤ |(-2:ℝ)|/8 ∧
      ∀ R ∈ ({ratFrame,reflected ratFrame} : Set (OrthonormalBasis (Fin 2) ℝ (E 2))),
      ∀ r ∈ ({0,delta/2} : Set ℝ),
        let G := framedConfluentCovariance (-2) midpoint R r
        let A : Matrix (Fin 6) (Fin 6) ℝ := fun i j => G (Fin.castAdd 1 i) (Fin.castAdd 1 j)
        (∀ v : Fin 7 → ℝ, gamma*(∑ i, (v i)^2) ≤ v ⬝ᵥ (G *ᵥ v) ∧
          v ⬝ᵥ (G *ᵥ v) ≤ Lambda*(∑ i, (v i)^2)) ∧ G.PosDef ∧ A.PosDef ∧ IsUnit A ∧
        gamma ≤ G 6 6-∑ i : Fin 6, ∑ j : Fin 6,
          G 6 (Fin.castAdd 1 i)*(A⁻¹) i j*G (Fin.castAdd 1 j) 6 := by
  obtain ⟨g,B,d,hg,hB,hd,hd1,hdL,h⟩ :=
    framedConfluent_covariance_uniform_floor (L := (-2)) (by norm_num)
  refine ⟨g,B,d,hg,hB,hd,hd1,hdL,?_⟩
  intro R _ r hr
  have hr' : r = 0 ∨ r = d/2 := by simpa using hr
  rcases hr' with rfl|rfl
  · exact h midpoint midpoint_domain R 0 le_rfl hd.le
  · exact h midpoint midpoint_domain R (d/2) (half_pos hd).le (half_le_self hd.le)
