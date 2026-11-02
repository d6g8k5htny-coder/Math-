import SourceTwoRemoteFirstJetGaussian
import Lean.Elab.Tactic.Omega

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Source I4SmoothCarrier I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceRemoteJetWitness I4SourceRemoteJetGaussian I4SourceTwoRemoteFirstJetGaussian
open I4SourceDerivativeGaussian I4SourceSmoothTopology
open MeasureTheory ProbabilityTheory WithLp
namespace TwoRemoteFirstJetGaussianControls

private theorem unit_circle_ne (L : ℝ) (hL : L=2 ∨ L= -2) :
    ((1:ℝ):AddCircle L) ≠ 0 := by
  intro h
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=L)).mp h
  have hex : ∃ k : ℤ, (k:ℝ)*2=1 := by
    rcases hL with rfl|rfl
    · exact ⟨n,by simpa only [zsmul_eq_mul] using hn⟩
    · refine ⟨-n,?_⟩
      have hh : (n:ℝ)*(-2)=1 := by simpa only [zsmul_eq_mul] using hn
      push_cast
      linarith
  obtain ⟨k,hk⟩ := hex
  have hkZ : k*(2:ℤ)=1 := by exact_mod_cast hk
  omega

private theorem half_circle_ne : ((1/2:ℝ):AddCircle (2:ℝ)) ≠ 0 := by
  intro h
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=(2:ℝ))).mp h
  have hh : (n:ℝ)*2=1/2 := by simpa only [zsmul_eq_mul] using hn
  have h4 : (n:ℝ)*4=1 := by linarith
  have h4Z : n*(4:ℤ)=1 := by exact_mod_cast h4
  omega

private theorem ne_from_coordinate (L : ℝ) (x y : Fin 2 → ℝ) (j : Fin 2)
    (h : (((x j-y j):ℝ):AddCircle L) ≠ 0) :
    I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L y := by
  intro hxy
  apply h
  rw [AddCircle.coe_sub,sub_eq_zero]
  exact congrFun hxy j

private theorem repeated_separations (L : ℝ) (hL : L=2 ∨ L= -2) :
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L (endpointM 0) ∧
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L (endpointS 0) ∧
    I4Torus.torusProjection 2 L ![0,1] ≠ I4Torus.torusProjection 2 L (endpointM 0) ∧
    I4Torus.torusProjection 2 L ![0,1] ≠ I4Torus.torusProjection 2 L (endpointS 0) ∧
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L ![0,1] := by
  refine ⟨?_,?_,?_,?_,?_⟩
  · apply ne_from_coordinate L _ _ 0
    simpa [endpointM] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 0
    simpa [endpointS] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 1
    simpa [endpointM] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 1
    simpa [endpointS] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 0
    simpa using unit_circle_ne L hL

private theorem negative_radius_separations :
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 (endpointM (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 (endpointS (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,1] ≠ I4Torus.torusProjection 2 2 (endpointM (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,1] ≠ I4Torus.torusProjection 2 2 (endpointS (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 ![0,1] := by
  refine ⟨?_,?_,?_,?_,?_⟩
  · apply Ne.symm
    apply ne_from_coordinate 2 _ _ 0
    simpa [endpointM] using half_circle_ne
  · apply ne_from_coordinate 2 _ _ 0
    change (((0:ℝ)-(-1)/2:ℝ):AddCircle (2:ℝ)) ≠ 0
    rw [show (0:ℝ)-(-1)/2=1/2 by ring]
    exact half_circle_ne
  · apply ne_from_coordinate 2 _ _ 1
    simpa [endpointM] using unit_circle_ne 2 (Or.inl rfl)
  · apply ne_from_coordinate 2 _ _ 1
    simpa [endpointS] using unit_circle_ne 2 (Or.inl rfl)
  · apply Ne.symm
    apply ne_from_coordinate 2 _ _ 1
    simpa using unit_circle_ne 2 (Or.inl rfl)


/- Uncompiled Controls-only text for ONE integration inside
TwoRemoteFirstJetGaussianControls. No production declaration or separate
helper proof/control campaign is introduced. -/

private def firstThreeBlockDiagonal (S : Matrix (Fin 6) (Fin 6) ℝ) :
    Matrix (Fin 6) (Fin 6) ℝ :=
  Fin.addCases
    (fun i : Fin 3 => Fin.addCases
      (fun j : Fin 3 => S (Fin.castAdd 3 i) (Fin.castAdd 3 j)) (fun _ : Fin 3 => 0))
    (fun i : Fin 3 => Fin.addCases
      (fun _ : Fin 3 => 0) (fun j : Fin 3 => S (Fin.castAdd 3 i) (Fin.castAdd 3 j)))

private theorem firstThreeBlockDiagonal_posSemidef
    (S : Matrix (Fin 6) (Fin 6) ℝ) (hS : S.PosDef) :
    (firstThreeBlockDiagonal S).PosSemidef := by
  let A : Matrix (Fin 3) (Fin 3) ℝ :=
    fun i j => S (Fin.castAdd 3 i) (Fin.castAdd 3 j)
  have hA : A.PosSemidef :=
    hS.posSemidef.submatrix (Fin.castAdd 3 : Fin 3 → Fin 6)
  let P₀ : Matrix (Fin 6) (Fin 3) ℝ :=
    Fin.addCases (fun i j : Fin 3 => if i=j then 1 else 0)
      (fun (_ : Fin 3) (_ : Fin 3) => 0)
  let P₁ : Matrix (Fin 6) (Fin 3) ℝ :=
    Fin.addCases (fun (_ : Fin 3) (_ : Fin 3) => 0)
      (fun i j : Fin 3 => if i=j then 1 else 0)
  have heq : firstThreeBlockDiagonal S = P₀ * A * P₀ᴴ + P₁ * A * P₁ᴴ := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [firstThreeBlockDiagonal, P₀, P₁, A, Matrix.mul_apply,
        Matrix.conjTranspose_apply, Fin.sum_univ_succ, Fin.addCases]
  rw [heq]
  exact (hA.mul_mul_conjTranspose_same P₀).add
    (hA.mul_mul_conjTranspose_same P₁)


/-- Literal value/dx/dy order uses the same sample at both points. -/
theorem observation_order (L : ℝ) (x y : Fin 2 → ℝ) (ω : SmoothSample 2 L) :
    twoRemoteFirstJet L x y ω =
      ![remoteJet L x ω 0,remoteJet L x ω 1,remoteJet L x ω 2,
        remoteJet L y ω 0,remoteJet L y ω 1,remoteJet L y ω 2] := rfl

/-- Raw columns remain intact in both actual regression blocks. -/
theorem regression_order (L r : ℝ) (x y : Fin 2 → ℝ) :
    twoRemoteRegressionMatrix L r x y =
      ![remoteRegressionMatrix L r x 0,remoteRegressionMatrix L r x 1,
        remoteRegressionMatrix L r x 2,remoteRegressionMatrix L r y 0,
        remoteRegressionMatrix L r y 1,remoteRegressionMatrix L r y 2] := rfl

/-- All six distinct target coordinates participate in the deterministic response. -/
theorem full_target_mean (L r : ℝ) (x y : Fin 2 → ℝ) (j : Fin 6) :
    twoRemotePosteriorMean L r x y ![1,2,3,4,5,6] j =
      twoRemoteRegressionMatrix L r x y j 0 +
      2*twoRemoteRegressionMatrix L r x y j 1 +
      3*twoRemoteRegressionMatrix L r x y j 2 +
      4*twoRemoteRegressionMatrix L r x y j 3 +
      5*twoRemoteRegressionMatrix L r x y j 4 +
      6*twoRemoteRegressionMatrix L r x y j 5 := by
  simp [twoRemotePosteriorMean,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]
  ring

/-- The mean identity is on the actual posterior sample, also at signed/singular inputs. -/
theorem signed_collision_actual_identity (ω : SmoothSample 2 (-2)) :
    twoRemoteFirstJet (-2) ![1,0] ![1,0]
      (rawPosteriorSample (by norm_num) 0 ![1,2,3,4,5,6] ω) =
    twoRemoteFirstJet (-2) ![1,0] ![1,0] ω -
      twoRemoteRegressionMatrix (-2) 0 ![1,0] ![1,0] *ᵥ rawPins (-2) 0 ω +
      twoRemotePosteriorMean (-2) 0 ![1,0] ![1,0] ![1,2,3,4,5,6] := by
  have h := remoteJet_rawPosteriorSample (L:=(-2)) (by norm_num) 0 ![1,0] ![1,2,3,4,5,6] ω
  ext i
  fin_cases i
  all_goals first | exact congrFun h 0 | exact congrFun h 1 | exact congrFun h 2

/-- Sampling law at a negative period, repeated pin, equal remote point and nonzero target. -/
theorem signed_collision_sampling_law :
    (rawPinKernel (L:=(-2)) (by norm_num) 0 ![1,2,3,4,5,6]).map
      (fun ω => toLp 2 (twoRemoteFirstJet (-2) ![1,0] ![1,0] ω)) =
    multivariateGaussian (toLp 2 (twoRemotePosteriorMean (-2) 0 ![1,0] ![1,0] ![1,2,3,4,5,6]))
      (twoRemoteResidualCovariance (-2) 0 ![1,0] ![1,0]) :=
  rawPinKernel_twoRemoteFirstJet_eq_multivariateGaussian (by norm_num) 0 _ _ _

/-- Actual correction positivity with coincident raw pins and separated remote points. -/
theorem repeated_pin_actualR_posDef :
    (twoRemoteResidualCovariance 2 0 ![1,0] ![0,1]).PosDef := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact twoRemoteResidualCovariance_posDef (by norm_num) 0 _ _
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

/-- Negative radius enters the identical theorem with its actual regression matrix. -/
theorem negative_radius_actualR_posDef :
    (twoRemoteResidualCovariance 2 (-1) ![0,0] ![0,1]).PosDef := by
  have h := negative_radius_separations
  exact twoRemoteResidualCovariance_posDef (by norm_num) (-1) _ _
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

/-- Equal points observe equal triples on every original sample. -/
theorem same_sample_triples (L : ℝ) (x : Fin 2 → ℝ) (ω : SmoothSample 2 L) (i : Fin 3) :
    twoRemoteFirstJet L x x ω (Fin.castAdd 3 i) =
      twoRemoteFirstJet L x x ω (Fin.natAdd 3 i) := by
  fin_cases i <;> rfl

/-- True equal-point cross blocks coincide with the marginal blocks, without independence. -/
theorem same_point_covariance_blocks (L r : ℝ) (x : Fin 2 → ℝ) (i j : Fin 3) :
    twoRemoteResidualCovariance L r x x (Fin.castAdd 3 i) (Fin.natAdd 3 j) =
      remoteResidualCovariance L r x (Fin.castAdd 3 i) (Fin.castAdd 3 j) := by
  fin_cases i <;> fin_cases j <;> rfl

private theorem control_derivative_measurable {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    Measurable (fun ω : SmoothSample 2 L =>
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u) := by
  borelize (DerivativeBCF 2 k)
  have he : Continuous (fun F : DerivativeBCF 2 k => F x u) := by fun_prop
  have hh := he.measurable.comp (sourceDerivativeBCF_borel 2 hL k)
  change Measurable (fun ω => sourceDerivativeBCF 2 hL k ω x u) at hh
  simp_rw [sourceDerivativeBCF_apply] at hh
  exact hh

private theorem marginal_measurable :
    Measurable (fun ω : SmoothSample 2 (2:ℝ) => toLp 2 (remoteJet 2 ![1,0] ω)) := by
  apply (by fun_prop : Measurable (fun v : Fin 6 → ℝ => toLp 2 v)).comp
  apply Measurable.of_eval
  intro i
  fin_cases i
  · change Measurable (fun ω : SmoothSample 2 (2:ℝ) => smoothSourceField 2 2 ω ![1,0])
    simpa only [iteratedFDeriv_zero_apply] using control_derivative_measurable (L:=2) (by norm_num) 0 ![1,0] (fun i => Fin.elim0 i)
  · change Measurable (fun ω : SmoothSample 2 (2:ℝ) => fderiv ℝ (smoothSourceField 2 2 ω) ![1,0] directionX)
    simpa only [iteratedFDeriv_one_apply] using control_derivative_measurable (L:=2) (by norm_num) 1 ![1,0] (fun _ => directionX)
  · change Measurable (fun ω : SmoothSample 2 (2:ℝ) => fderiv ℝ (smoothSourceField 2 2 ω) ![1,0] directionY)
    simpa only [iteratedFDeriv_one_apply] using control_derivative_measurable (L:=2) (by norm_num) 1 ![1,0] (fun _ => directionY)
  · exact control_derivative_measurable (L:=2) (by norm_num) 2 ![1,0] ![directionX,directionX]
  · exact control_derivative_measurable (L:=2) (by norm_num) 2 ![1,0] ![directionX,directionY]
  · exact control_derivative_measurable (L:=2) (by norm_num) 2 ![1,0] ![directionY,directionY]

private theorem marginal_posDef : (remoteResidualCovariance 2 0 ![1,0]).PosDef := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact remoteResidualCovariance_posDef (by norm_num) 0 _ h.1 h.2.1

/-- Public49's actual sampling law identifies a strictly positive common value variance. -/
theorem actual_common_value_variance_positive :
    0 < cov[fun ω => twoRemoteFirstJet 2 ![1,0] ![1,0] ω 0,
      fun ω => twoRemoteFirstJet 2 ![1,0] ![1,0] ω 3;
      rawPinKernel (L:=2) (by norm_num) 0 0] := by
  have hp := marginal_posDef
  have hc := covariance_eval_multivariateGaussian (μ:=toLp 2 (remotePosteriorMean 2 0 ![1,0] 0))
    hp.posSemidef (0:Fin 6) (0:Fin 6)
  rw [← rawPinKernel_remoteJet_eq_multivariateGaussian (L:=2) (by norm_num) 0 ![1,0] 0] at hc
  rw [covariance_map_fun (by fun_prop) (by fun_prop) marginal_measurable.aemeasurable] at hc
  change cov[fun ω => remoteJet 2 ![1,0] ω 0,fun ω => remoteJet 2 ![1,0] ω 0;
    rawPinKernel (L:=2) (by norm_num) 0 0] = remoteResidualCovariance 2 0 ![1,0] 0 0 at hc
  change 0 < cov[fun ω => remoteJet 2 ![1,0] ω 0,fun ω => remoteJet 2 ![1,0] ω 0;
    rawPinKernel (L:=2) (by norm_num) 0 0]
  rw [hc]
  exact hp.diag_pos 0

/-- The mutation retains the actual deterministic mean at the zero target. -/
theorem mutation_mean_is_actual :
    toLp 2 (twoRemotePosteriorMean 2 0 ![1,0] ![1,0] 0) = (0 : EuclideanSpace ℝ (Fin 6)) := by
  simp [twoRemotePosteriorMean]

/-- The sole candidate deletes exactly the two cross-remote blocks. -/
def zeroCrossCandidate : Matrix (Fin 6) (Fin 6) ℝ :=
  firstThreeBlockDiagonal (remoteResidualCovariance 2 0 ![1,0])

/-- Both candidate diagonal blocks retain the actual joint covariance entries. -/
theorem zeroCrossCandidate_actual_diagonal_blocks (i j : Fin 3) :
    zeroCrossCandidate (Fin.castAdd 3 i) (Fin.castAdd 3 j) =
      twoRemoteResidualCovariance 2 0 ![1,0] ![1,0] (Fin.castAdd 3 i) (Fin.castAdd 3 j) ∧
    zeroCrossCandidate (Fin.natAdd 3 i) (Fin.natAdd 3 j) =
      twoRemoteResidualCovariance 2 0 ![1,0] ![1,0] (Fin.natAdd 3 i) (Fin.natAdd 3 j) := by
  fin_cases i <;> fin_cases j <;> exact ⟨rfl,rfl⟩

/-- Candidate covariance validity is proved before its Gaussian covariance is used. -/
theorem zeroCrossCandidate_posSemidef : zeroCrossCandidate.PosSemidef :=
  firstThreeBlockDiagonal_posSemidef _ marginal_posDef

/-- Deleting cross blocks makes the candidate value cross covariance zero. -/
theorem zeroCrossCandidate_entry03 : zeroCrossCandidate 0 3 = 0 := rfl

private theorem joint_collision_measurable :
    Measurable (fun ω : SmoothSample 2 (2:ℝ) =>
      toLp 2 (twoRemoteFirstJet 2 ![1,0] ![1,0] ω)) := by
  exact (by fun_prop : Measurable (fun v : EuclideanSpace ℝ (Fin 6) =>
    toLp 2 (![v 0,v 1,v 2,v 0,v 1,v 2] : Fin 6 → ℝ))).comp marginal_measurable

/-- Actual common variance is positive, whereas the valid candidate has zero cross covariance. -/
theorem actual_zero_cross_mutation_false :
    ¬ (rawPinKernel (L:=2) (by norm_num) 0 0).map
      (fun ω => toLp 2 (twoRemoteFirstJet 2 ![1,0] ![1,0] ω)) =
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin 6)) zeroCrossCandidate := by
  intro hmut
  have hc : cov[fun v : EuclideanSpace ℝ (Fin 6) => v 0,fun v => v 3;
      (rawPinKernel (L:=2) (by norm_num) 0 0).map
        (fun ω => toLp 2 (twoRemoteFirstJet 2 ![1,0] ![1,0] ω))] = 0 := by
    rw [hmut,covariance_eval_multivariateGaussian zeroCrossCandidate_posSemidef]
    exact zeroCrossCandidate_entry03
  rw [covariance_map_fun (by fun_prop) (by fun_prop) joint_collision_measurable.aemeasurable] at hc
  exact (ne_of_gt actual_common_value_variance_positive) hc


end TwoRemoteFirstJetGaussianControls
