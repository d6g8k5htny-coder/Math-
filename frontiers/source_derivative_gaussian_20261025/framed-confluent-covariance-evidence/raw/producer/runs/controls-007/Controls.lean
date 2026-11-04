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
private theorem std0 : coordinates 2 (std 0) = directionX := by
  ext i
  fin_cases i <;> simp [std,EuclideanSpace.basisFun_apply,EuclideanSpace.single,coordinates_apply,directionX]
private theorem std1 : coordinates 2 (std 1) = directionY := by
  ext i
  fin_cases i <;> simp [std,EuclideanSpace.basisFun_apply,EuclideanSpace.single,coordinates_apply,directionY]

private theorem kernel_mass : (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)) = (1/6:ℝ) := by
  have hc : IntervalIntegrable (fun _ : ℝ => (1/4:ℝ)) volume (-1/2) (1/2) := intervalIntegrable_const
  have hp : IntervalIntegrable (fun t : ℝ => t^2) volume (-1/2) (1/2) :=
    (continuous_id.pow 2).intervalIntegrable _ _
  calc
    _ = (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4:ℝ)) - (∫ t in (-1/2:ℝ)..(1/2:ℝ),t^2) :=
      intervalIntegral.integral_sub hc hp
    _ = _ := by norm_num

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
  · change 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f p ![e,e,e]) =
      iteratedFDeriv ℝ 3 f p ![e,e,e]
    rw [intervalIntegral.integral_mul_const,kernel_mass]; ring
  · rfl

-- This checks only the new fixed-axis specialization join; the old pin proof is reused.
theorem standard_axis_coefficient_join (L r : ℝ) (i : Fin 6) (m : SourceMode 2) :
    framedConfluentCoefficient L 0 std r (Fin.castAdd 1 i) m =
      I4SourceConfluentLimits.regularizedPinCoefficient L r i m := by
  rw [coefficient_rows,std0,std1]
  simp only [map_zero]
  have hm : (0 : Fin 2 → ℝ)-(r/2) • directionX = ![-r/2,0] := by
    ext j
    fin_cases j
    · simp [directionX,neg_div]
    · simp [directionX]
  have hp : (0 : Fin 2 → ℝ)+(r/2) • directionX = ![r/2,0] := by
    ext j; fin_cases j <;> simp [directionX]
  have ht (t : ℝ) : (0 : Fin 2 → ℝ)+(r*t) • directionX = ![r*t,0] := by
    ext j; fin_cases j <;> simp [directionX]
  fin_cases i <;>
    dsimp only [rows,I4SourceConfluentLimits.regularizedPinCoefficient,Fin.castAdd,
      Matrix.cons_val_zero,Matrix.cons_val_succ]
  all_goals simp only [I4ModeCurveChains.modeF_deriv,I4ModeCurveChains.modeF,
    I4ModeCurveChains.modeH,I4WeightedModeIntegrals.weightedDerivativeIntegral,
    I4SourceConfluentLimits.peanoCubic,hm,hp,ht,one_mul]
  all_goals simp only [derivativeCoefficient,iteratedFDeriv_one_apply]
  all_goals rfl

theorem standard_axis_same_sample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) :
    (fun i : Fin 6 => framedConfluentVector L 0 std r ω (Fin.castAdd 1 i)) =
      I4SourceEndpointRegression.sourceConfluentPinsAt L r ω := by
  rw [I4SourceConfluentLimits.sourceConfluentPinsAt_series hL]
  funext i
  change scalarSeries (framedConfluentCoefficient L 0 std r (Fin.castAdd 1 i))
    (sampleInclusion 2 L ω) = _
  congr 1
  funext m
  rw [standard_axis_coefficient_join,I4SourceConfluentLimits.pinCoefficient_eq_regularized L r hr]

theorem standard_contact_order {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    framedConfluentVector L 0 std 0 ω =
      ![actualField 2 L ω 0,fderiv ℝ (actualField 2 L ω) 0 (std 0),
        fderiv ℝ (actualField 2 L ω) 0 (std 1),
        iteratedFDeriv ℝ 2 (actualField 2 L ω) 0 ![std 0,std 0],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) 0 ![std 0,std 1],
        iteratedFDeriv ℝ 3 (actualField 2 L ω) 0 ![std 0,std 0,std 0],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) 0 ![std 1,std 1] ] :=
  (framedConfluentVector_actual hL 0 std 0).2.2.2.1 ω

private def frameOf (u : Fin 2 → E 2) (hu : Orthonormal ℝ u) :
    OrthonormalBasis (Fin 2) ℝ (E 2) :=
  OrthonormalBasis.mk hu ((hu.linearIndependent.span_eq_top_of_card_eq_finrank' (by simp [E])).ge)
private theorem frameOf_apply (u : Fin 2 → E 2) (hu : Orthonormal ℝ u) (i : Fin 2) :
    frameOf u hu i = u i := by simp [frameOf]

private def ratFamily : Fin 2 → E 2 :=
  ![toLp 2 ![(3/5:ℝ),4/5],toLp 2 ![(-4/5:ℝ),3/5] ]
private theorem rat_orthonormal : Orthonormal ℝ ratFamily := by
  rw [orthonormal_iff_ite]
  intro i j
  simp only [EuclideanSpace.inner_eq_star_dotProduct,star_trivial,dotProduct,Fin.sum_univ_two]
  fin_cases i <;> fin_cases j <;> norm_num [ratFamily]
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
    simp [reflectedFamily,R.inner_eq_zero (show (0:Fin 2) ≠ 1 by decide),
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
  have he : (fun i : Fin 2 => ![(1:ℝ),-1] i • ![e,n] i) = ![e,-n] := by
    ext i; fin_cases i <;> simp
  rw [he] at h
  simpa [Fin.prod_univ_succ] using h
private theorem second_neg_both (T : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => Fin 2 → ℝ) ℝ)
    (n : Fin 2 → ℝ) : T ![-n,-n] = T ![n,n] := by
  have h := T.toMultilinearMap.map_smul_univ (fun _ => (-1:ℝ)) ![n,n]
  have he : (fun i : Fin 2 => (-1:ℝ) • ![n,n] i) = ![-n,-n] := by
    ext i; fin_cases i <;> simp
  rw [he] at h
  simpa [Fin.prod_univ_succ] using h

theorem reflected_coefficient_signs (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i : Fin 7) (m : SourceMode 2) :
    framedConfluentCoefficient L z (reflected R) r i m =
      signs i * framedConfluentCoefficient L z R r i m := by
  rw [coefficient_rows,coefficient_rows,reflected0,reflected1,map_neg]
  fin_cases i
  · simp [rows,signs]
  · simp [rows,signs]
  · change ((fderiv ℝ (modeCoefficient 2 L m) (coordinates 2 z-(r/2) • coordinates 2 (R 0))
      (-coordinates 2 (R 1))) + (fderiv ℝ (modeCoefficient 2 L m)
        (coordinates 2 z+(r/2) • coordinates 2 (R 0)) (-coordinates 2 (R 1))))/2 =
      (-1)*(((fderiv ℝ (modeCoefficient 2 L m) (coordinates 2 z-(r/2) • coordinates 2 (R 0))
        (coordinates 2 (R 1))) + (fderiv ℝ (modeCoefficient 2 L m)
          (coordinates 2 z+(r/2) • coordinates 2 (R 0)) (coordinates 2 (R 1))))/2)
    simp only [map_neg]
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
  · change iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z)
        ![-coordinates 2 (R 1),-coordinates 2 (R 1)] =
      1*iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z)
        ![coordinates 2 (R 1),coordinates 2 (R 1)]
    simpa only [one_mul] using second_neg_both (iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z))
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
        ![actualField 2 (-2) ω (midpoint-((-1/3:ℝ)/2) • ratFrame 0),
          actualField 2 (-2) ω (midpoint+((-1/3:ℝ)/2) • ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3:ℝ)/2) • ratFrame 0) (ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3:ℝ)/2) • ratFrame 0) (ratFrame 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3:ℝ)/2) • ratFrame 0) (ratFrame 1),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3:ℝ)/2) • ratFrame 0) (ratFrame 1)] := by
  have h := framedConfluentVector_actual (L := (-2)) (by norm_num) midpoint ratFrame (-1/3)
  exact ⟨h.1,h.2.1,h.2.2.2.2 (by norm_num) ω⟩

theorem reflected_nonaxis_actual (ω : SmoothSample 2 (-2)) :
    HasGaussianLaw (framedConfluentVector (-2) midpoint (reflected ratFrame) (-1/3)) (smoothLaw 2 (-2)) ∧
    (∀ i j : Fin 7, cov[fun η => framedConfluentVector (-2) midpoint (reflected ratFrame) (-1/3) η i,
      fun η => framedConfluentVector (-2) midpoint (reflected ratFrame) (-1/3) η j;smoothLaw 2 (-2)] =
      framedConfluentCovariance (-2) midpoint (reflected ratFrame) (-1/3) i j) ∧
    (fun i : Fin 6 => framedConfluentVector (-2) midpoint (reflected ratFrame) (-1/3) ω (Fin.castAdd 1 i)) =
      confluentTransform (-1/3)
        ![actualField 2 (-2) ω (midpoint-((-1/3:ℝ)/2) • (reflected ratFrame) 0),
          actualField 2 (-2) ω (midpoint+((-1/3:ℝ)/2) • (reflected ratFrame) 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3:ℝ)/2) • (reflected ratFrame) 0) ((reflected ratFrame) 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3:ℝ)/2) • (reflected ratFrame) 0) ((reflected ratFrame) 0),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint-((-1/3:ℝ)/2) • (reflected ratFrame) 0) ((reflected ratFrame) 1),
          fderiv ℝ (actualField 2 (-2) ω) (midpoint+((-1/3:ℝ)/2) • (reflected ratFrame) 0) ((reflected ratFrame) 1)] := by
  have h := framedConfluentVector_actual (L := (-2)) (by norm_num) midpoint (reflected ratFrame) (-1/3)
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

-- The sole mutation has a concrete finite original-source witness.
def sineBase : TrigPoly := scale Real.pi⁻¹ [⟨1,![1,0],-(Real.pi/2)⟩]
def sineCube : TrigPoly := scale (1/6) (mul (mul sineBase sineBase) sineBase)
def finiteDirection : SourceMode 2 →₀ ℝ := toSource 2 sineCube

theorem sineBase_eval (y : Fin 2 → ℝ) :
    eval 2 sineBase y = localGerm Real.pi 0 1 y := by
  rw [sineBase,eval_scale]
  simp only [eval,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,add_zero,termEval,one_mul]
  change Real.pi⁻¹ * Real.cos (phase 2 2 ![1,0] y-(Real.pi/2)) =
    Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi
  have hp : phase 2 2 ![1,0] y = Real.pi*y 0 := by
    simp [phase,sourceC,Fin.sum_univ_two]
  rw [hp,Real.cos_sub_pi_div_two]
  simp [div_eq_mul_inv,mul_comm]

theorem sineCube_eval (y : Fin 2 → ℝ) :
    eval 2 sineCube y = Real.sin (Real.pi*y 0)^3/(6*Real.pi^3) := by
  rw [sineCube,eval_scale,eval_mul,eval_mul,sineBase_eval]
  change (1/6:ℝ)*((Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi *
    (Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi))*(Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi)) = _
  simp only [sub_zero]
  ring

private theorem sineCube_smooth : ContDiff ℝ (⊤ : ℕ∞) (eval 2 sineCube) := by
  have he : eval 2 sineCube = fun y => Real.sin (Real.pi*y 0)^3/(6*Real.pi^3) := funext sineCube_eval
  rw [he]
  fun_prop

theorem sineCube_lower_jets : jet2 (eval 2 sineCube) 0 = 0 := by
  let q := localGerm Real.pi 0 (1:Fin 6)
  have hq : ContDiff ℝ (⊤ : ℕ∞) q := by
    change ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ => Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi)
    fun_prop
  have hJ : jet2 q 0 = fun j => if j=(1:Fin 6) then 1 else 0 := by
    ext j
    exact localGerm_jet2 Real.pi Real.pi_ne_zero 0 j 1
  have hcube : jet2 (fun y => (q y*q y)*q y) 0 = 0 := by
    rw [jet2_mul _ _ ((hq.mul hq).of_le (by norm_num)) (hq.of_le (by norm_num)),
      jet2_mul _ _ (hq.of_le (by norm_num)) (hq.of_le (by norm_num)),hJ]
    ext j
    fin_cases j <;> norm_num [mulJet2]
  have he : eval 2 sineCube = fun y => (1/6:ℝ)*((q y*q y)*q y) := by
    funext y
    simp only [sineCube,eval_scale,eval_mul,sineBase_eval,q]
  rw [he,jet2_mul _ _ (contDiff_const : ContDiff ℝ 2 (fun _ : Fin 2 → ℝ => (1/6:ℝ)))
    (((hq.mul hq).mul hq).of_le (by norm_num)),hcube]
  ext j
  fin_cases j <;> simp [mulJet2]

private theorem sin_third_zero (c : ℝ) :
    iteratedDeriv 3 (fun t : ℝ => Real.sin (c*t)) 0 = -c^3 := by
  have h1 : deriv (fun t : ℝ => Real.sin (c*t)) = fun t => c*Real.cos (c*t) := by
    funext t
    simpa only [id_eq,mul_one,mul_comm] using (((hasDerivAt_id t).const_mul c).sin).deriv
  have h2 : deriv (fun t : ℝ => c*Real.cos (c*t)) = fun t => -(c^2)*Real.sin (c*t) := by
    funext t
    have hh := ((((hasDerivAt_id t).const_mul c).cos).const_mul c).deriv
    simp only [id_eq,mul_one] at hh
    rw [hh]
    ring
  have h3 : deriv (fun t : ℝ => -(c^2)*Real.sin (c*t)) = fun t => -(c^3)*Real.cos (c*t) := by
    funext t
    have hh := ((((hasDerivAt_id t).const_mul c).sin).const_mul (-(c^2))).deriv
    simp only [id_eq,mul_one] at hh
    rw [hh]
    ring
  simp only [iteratedDeriv_succ,iteratedDeriv_zero,h1,h2,h3,mul_zero,Real.cos_zero,mul_one]

theorem sineCube_third :
    iteratedFDeriv ℝ 3 (eval 2 sineCube) 0 ![directionX,directionX,directionX] = 1 := by
  have he : (fun t : ℝ => eval 2 sineCube ![t,0]) =
      fun t => (24*Real.pi^3)⁻¹*(3*Real.sin (Real.pi*t)-Real.sin ((3*Real.pi)*t)) := by
    funext t
    rw [sineCube_eval]
    change Real.sin (Real.pi*t)^3/(6*Real.pi^3) = _
    rw [show (3*Real.pi)*t=3*(Real.pi*t) by ring,Real.sin_three_mul]
    field_simp [Real.pi_ne_zero]
    ring
  have hscalar : iteratedDeriv 3 (fun t : ℝ => eval 2 sineCube ![t,0]) 0 = 1 := by
    rw [he,iteratedDeriv_const_mul_field]
    rw [iteratedDeriv_fun_sub (by fun_prop) (by fun_prop),iteratedDeriv_const_mul_field,
      sin_third_zero,sin_third_zero]
    field_simp [Real.pi_ne_zero]
    ring
  have ha := (I4ModeCurveChains.axis_iteratedDeriv (eval 2 sineCube) sineCube_smooth 3 0).symm.trans hscalar
  have hp : (![0,0] : Fin 2 → ℝ) = 0 := by ext j; fin_cases j <;> rfl
  have hd : (fun _ : Fin 3 => directionX) = ![directionX,directionX,directionX] := by
    ext j; fin_cases j <;> rfl
  simpa only [hp,hd] using ha

-- Concrete physical-coordinate pullback for the very same finite witness.
theorem physical_sineCube_third :
    iteratedFDeriv ℝ 3 (fun z : E 2 => eval 2 sineCube (coordinates 2 z)) 0
      ![std 0,std 0,std 0] = 1 := by
  have h := congrArg (fun T => T ![std 0,std 0,std 0])
    ((coordinates 2).toContinuousLinearMap.iteratedFDeriv_comp_right sineCube_smooth (0 : E 2) (i := 3) (by simp))
  refine h.trans ?_
  rw [ContinuousMultilinearMap.compContinuousLinearMap_apply]
  have hd : (fun i : Fin 3 => coordinates 2 (![std 0,std 0,std 0] i)) =
      ![directionX,directionX,directionX] := by
    ext i
    fin_cases i <;> simpa only using std0
  simpa only [map_zero,hd] using sineCube_third

theorem finite_lower_pairings (j : Fin 6) :
    finitePairing (fun m => jet2 (modeCoefficient 2 2 m) 0 j) finiteDirection = 0 := by
  have hj : jet2 (eval 2 sineCube) 0 j = 0 := congrFun sineCube_lower_jets j
  rw [← hj]
  fin_cases j
  · exact toSource_eval (by norm_num) sineCube 0
  · have he : derivativeCoefficient 2 2 1 0 (fun _ => directionX) =
        fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionX := by
      funext m; exact iteratedFDeriv_one_apply _
    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionX) finiteDirection =
      fderiv ℝ (eval 2 sineCube) 0 directionX
    rw [← he]
    simpa only [finiteDirection,iteratedFDeriv_one_apply] using toSource_derivative (by norm_num) sineCube 1 0 (fun _ => directionX)
  · have he : derivativeCoefficient 2 2 1 0 (fun _ => directionY) =
        fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionY := by
      funext m; exact iteratedFDeriv_one_apply _
    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionY) finiteDirection =
      fderiv ℝ (eval 2 sineCube) 0 directionY
    rw [← he]
    simpa only [finiteDirection,iteratedFDeriv_one_apply] using toSource_derivative (by norm_num) sineCube 1 0 (fun _ => directionY)
  · exact toSource_derivative (by norm_num) sineCube 2 0 ![directionX,directionX]
  · exact toSource_derivative (by norm_num) sineCube 2 0 ![directionX,directionY]
  · exact toSource_derivative (by norm_num) sineCube 2 0 ![directionY,directionY]

def omittedFactorRow (m : SourceMode 2) : ℝ :=
  ∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 (modeCoefficient 2 2 m) 0
    ![directionX,directionX,directionX]

theorem correct_pairing_one :
    finitePairing (framedConfluentCoefficient 2 0 std 0 5) finiteDirection = 1 := by
  have he : framedConfluentCoefficient 2 0 std 0 5 =
      derivativeCoefficient 2 2 3 0 ![directionX,directionX,directionX] := by
    funext m
    rw [coefficient_rows,std0,std1]
    rw [map_zero,rows_zero]
    rfl
  rw [he]
  exact (toSource_derivative (by norm_num) sineCube 3 0 ![directionX,directionX,directionX]).trans sineCube_third

theorem omitted_pairing_sixth : finitePairing omittedFactorRow finiteDirection = (1/6:ℝ) := by
  have he : omittedFactorRow = fun m => (1/6:ℝ)*derivativeCoefficient 2 2 3 0 ![directionX,directionX,directionX] m := by
    funext m
    unfold omittedFactorRow
    rw [intervalIntegral.integral_mul_const,kernel_mass]
    rfl
  rw [he]
  have hs : finitePairing (fun m => (1/6:ℝ)*derivativeCoefficient 2 2 3 0 ![directionX,directionX,directionX] m) finiteDirection =
      (1/6:ℝ)*finitePairing (derivativeCoefficient 2 2 3 0 ![directionX,directionX,directionX]) finiteDirection := by
    classical
    simp only [finitePairing,Finsupp.sum,mul_assoc,Finset.mul_sum]
  rw [hs]
  have hd := (toSource_derivative (by norm_num) sineCube 3 0 ![directionX,directionX,directionX]).trans sineCube_third
  rw [show finiteDirection = toSource 2 sineCube from rfl,hd]
  norm_num

theorem factor_six_actual_counterexample :
    (∀ j : Fin 6, finitePairing (fun m => jet2 (modeCoefficient 2 2 m) 0 j) finiteDirection = 0) ∧
    finitePairing (framedConfluentCoefficient 2 0 std 0 5) finiteDirection = 1 ∧
    finitePairing omittedFactorRow finiteDirection = (1/6:ℝ) ∧
    finitePairing omittedFactorRow finiteDirection ≠ 1 := by
  refine ⟨finite_lower_pairings,correct_pairing_one,omitted_pairing_sixth,?_⟩
  rw [omitted_pairing_sixth]
  norm_num

end FramedConfluentControls
