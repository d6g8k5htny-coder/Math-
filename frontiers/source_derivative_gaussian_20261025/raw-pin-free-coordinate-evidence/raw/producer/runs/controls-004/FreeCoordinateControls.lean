import SourceRawPinFreeCoordinates
import Lean.Elab.Tactic.Omega

-- Concatenate these imports with SECTION.lean.txt to form the one qualified
-- scratch FreeCoordinateControls.lean integration. No new production import.
-- All names in namespace FreeCoordinateControls are ordinary exported scratch
-- controls. The negative imports the qualified Controls object and its exact
-- named-mode q/2q facts; it does not copy this section or production source.

/- Complete uncompiled TEXT-ONLY57 controls, for ONE integration into
FreeCoordinateControls.lean. These are ordinary exported scratch-control
facts, not additional production API. Positive Controls qualification covers
this text and any actual local amendments; the production kernel does not. -/

noncomputable section
set_option autoImplicit false
open I4Foundation I4Weights I4Source I4SmoothCarrier I4SourceGaussian
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceRawPinConditioning I4SourceSmoothConditional
open I4SourceFinitePinKernel I4SourceCurvatureDecomposition
open I4SourceRawPinFreeCoordinates MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Topology

namespace FreeCoordinateControls

def control57_frequency : Fin 4 → Fin 2 → ℤ :=
  ![![1,0], ![2,0], ![0,1], ![0,2]]

theorem control57_frequency_half (s : Fin 4) : control57_frequency s ∈ halfLattice 2 := by
  fin_cases s
  · refine ⟨0, by norm_num [control57_frequency], ?_⟩
    intro j hj
    fin_cases j <;> norm_num at hj
  · refine ⟨0, by norm_num [control57_frequency], ?_⟩
    intro j hj
    fin_cases j <;> norm_num at hj
  · refine ⟨1, by norm_num [control57_frequency], ?_⟩
    intro j hj
    fin_cases j <;> norm_num [control57_frequency] at *
  · refine ⟨1, by norm_num [control57_frequency], ?_⟩
    intro j hj
    fin_cases j <;> norm_num [control57_frequency] at *

def control57_mode (s : Fin 4) : SourceMode 2 :=
  some (⟨control57_frequency s, control57_frequency_half s⟩, false)

theorem control57_mode_injective : Function.Injective control57_mode := by
  intro s t h
  fin_cases s <;> fin_cases t <;>
    simp_all [control57_mode, control57_frequency, funext_iff, Fin.forall_fin_succ]

@[simp] theorem control57_mode_eq_iff (s t : Fin 4) :
    control57_mode s = control57_mode t ↔ s=t := control57_mode_injective.eq_iff

def control57_mA : SourceMode 2 := control57_mode 0
def control57_mB : SourceMode 2 := control57_mode 1
def control57_mC : SourceMode 2 := control57_mode 2
def control57_mD : SourceMode 2 := control57_mode 3

def control57_amplitude (s : Fin 4) : ℝ := modeCoefficient 2 2 (control57_mode s) 0
def control57_AA : ℝ := control57_amplitude 0
def control57_AB : ℝ := control57_amplitude 1
def control57_AC : ℝ := control57_amplitude 2
def control57_AD : ℝ := control57_amplitude 3
def control57_DAB : ℝ := Real.sqrt (control57_AA^2 + control57_AB^2)
def control57_DCD : ℝ := Real.sqrt (control57_AC^2 + control57_AD^2)

theorem control57_amplitude_pos (s : Fin 4) : 0 < control57_amplitude s := by
  have he : control57_amplitude s =
      Real.sqrt (2 * sourceWeight 2 2 (control57_frequency s) / sourceZ 2 2) := by
    simp [control57_amplitude,control57_mode,modeCoefficient,phase]
  rw [he]
  apply Real.sqrt_pos.mpr
  apply div_pos _ (sourceZ_pos 2 (by norm_num))
  apply mul_pos (by norm_num)
  rw [sourceWeight_eq_physical]
  exact Real.exp_pos _

theorem control57_DAB_pos : 0 < control57_DAB := by
  have hA := control57_amplitude_pos 0
  have hB := control57_amplitude_pos 1
  unfold control57_DAB control57_AA control57_AB
  positivity

theorem control57_DCD_pos : 0 < control57_DCD := by
  have hC := control57_amplitude_pos 2
  have hD := control57_amplitude_pos 3
  unfold control57_DCD control57_AC control57_AD
  positivity

theorem control57_DAB_sq : control57_DAB^2 = control57_AA^2 + control57_AB^2 :=
  Real.sq_sqrt (add_nonneg (sq_nonneg _) (sq_nonneg _))

theorem control57_DCD_sq : control57_DCD^2 = control57_AC^2 + control57_AD^2 :=
  Real.sq_sqrt (add_nonneg (sq_nonneg _) (sq_nonneg _))

theorem control57_cosine_fderiv_zero (k : ↥(halfLattice 2)) :
    fderiv ℝ (modeCoefficient 2 2 (some (k,false))) 0 = 0 := by
  have heq : (fun x : Fin 2 → ℝ => phase 2 2 k x) =
      (I4C4.phaseCLM 2 2 k : (Fin 2 → ℝ) → ℝ) := by
    funext x
    exact (I4C4.phaseCLM_apply 2 2 k x).symm
  have hp : HasFDerivAt (fun x : Fin 2 → ℝ => phase 2 2 k x)
      (I4C4.phaseCLM 2 2 k) 0 := by
    rw [heq]
    exact (I4C4.phaseCLM 2 2 k).hasFDerivAt
  have h := (hp.cos.const_mul (Real.sqrt (2 * sourceWeight 2 2 k / sourceZ 2 2))).fderiv
  change fderiv ℝ (fun x => Real.sqrt (2 * sourceWeight 2 2 k / sourceZ 2 2) *
    Real.cos (phase 2 2 k x)) 0 = 0
  simpa [phase] using h

theorem control57_actual_raw_column (s : Fin 4) (i : Fin 6) :
    rawPinCoefficient 2 0 i (control57_mode s) =
      ![control57_amplitude s, control57_amplitude s, 0,0,0,0] i := by
  have hd : fderiv ℝ (modeCoefficient 2 2 (control57_mode s)) 0 = 0 :=
    control57_cosine_fderiv_zero _
  have hz (v : Fin 1 → (Fin 2 → ℝ)) :
      iteratedFDeriv ℝ 1 (modeCoefficient 2 2 (control57_mode s)) 0 v = 0 := by
    rw [_root_.iteratedFDeriv_one_apply,hd]
    rfl
  have hM : endpointM (0 : ℝ) = 0 := by ext j; fin_cases j <;> norm_num [endpointM]
  have hS : endpointS (0 : ℝ) = 0 := by ext j; fin_cases j <;> norm_num [endpointS]
  fin_cases i
  · change modeCoefficient 2 2 (control57_mode s) (endpointM 0) = control57_amplitude s
    rw [hM]
    rfl
  · change modeCoefficient 2 2 (control57_mode s) (endpointS 0) = control57_amplitude s
    rw [hS]
    rfl
  · change iteratedFDeriv ℝ 1 (modeCoefficient 2 2 (control57_mode s)) (endpointM 0)
      (rawDerivativeDirections 2) = 0
    rw [hM]
    exact hz _
  · change iteratedFDeriv ℝ 1 (modeCoefficient 2 2 (control57_mode s)) (endpointS 0)
      (rawDerivativeDirections 3) = 0
    rw [hS]
    exact hz _
  · change iteratedFDeriv ℝ 1 (modeCoefficient 2 2 (control57_mode s)) (endpointM 0)
      (rawDerivativeDirections 4) = 0
    rw [hM]
    exact hz _
  · change iteratedFDeriv ℝ 1 (modeCoefficient 2 2 (control57_mode s)) (endpointS 0)
      (rawDerivativeDirections 5) = 0
    rw [hS]
    exact hz _

theorem control57_pairing_single (a : SourceMode 2 → ℝ) (m : SourceMode 2) (c : ℝ) :
    finitePairing a (Finsupp.single m c) = a m*c := by
  classical
  simp [finitePairing, Finsupp.sum_single_index]

theorem control57_pairing_add_right (a : SourceMode 2 → ℝ)
    (v w : SourceMode 2 →₀ ℝ) :
    finitePairing a (v+w) = finitePairing a v + finitePairing a w := by
  classical
  exact Finsupp.sum_add_index' (fun _ => mul_zero _) (fun _ _ _ => mul_add _ _ _)

theorem control57_pairing_smul_right (a : SourceMode 2 → ℝ) (c : ℝ)
    (v : SourceMode 2 →₀ ℝ) : finitePairing a (c • v) = c*finitePairing a v := by
  classical
  unfold finitePairing
  rw [Finsupp.sum_smul_index' (fun _ => mul_zero _)]
  simp only [Finsupp.sum, smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro m _
  ring

theorem control57_pairing_neg_right (a : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) : finitePairing a (-v) = -finitePairing a v := by
  simpa using control57_pairing_smul_right a (-1) v

theorem control57_pairing_neg_left (a : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) : finitePairing (fun m => -a m) v = -finitePairing a v := by
  classical
  simp [finitePairing,Finsupp.sum,neg_mul,Finset.sum_neg_distrib]

theorem control57_pairing_add_left (a b : SourceMode 2 → ℝ) (v : SourceMode 2 →₀ ℝ) :
    finitePairing (fun m => a m+b m) v = finitePairing a v + finitePairing b v := by
  classical
  simp [finitePairing, Finsupp.sum, add_mul, Finset.sum_add_distrib]

theorem control57_pairing_mul_left (c : ℝ) (a : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) :
    finitePairing (fun m => c*a m) v = c*finitePairing a v := by
  classical
  simp [finitePairing, Finsupp.sum, Finset.mul_sum, mul_assoc]

theorem control57_pairing_hasSum (a : SourceMode 2 → ℝ) (v : SourceMode 2 →₀ ℝ) :
    HasSum (fun m => a m*v m) (finitePairing a v) := by
  classical
  apply hasSum_sum_of_ne_finset_zero
  intro m hm
  simp only [Finsupp.notMem_support_iff.mp hm, mul_zero]

def control57_chi0 : SourceMode 2 →₀ ℝ :=
  Finsupp.single control57_mA (control57_AB/control57_DAB) +
    Finsupp.single control57_mB (-control57_AA/control57_DAB)

def control57_chi1 : SourceMode 2 →₀ ℝ :=
  Finsupp.single control57_mC (control57_AD/control57_DCD) +
    Finsupp.single control57_mD (-control57_AC/control57_DCD)

def control57_chi : Fin 2 → (SourceMode 2 →₀ ℝ) := ![control57_chi0,control57_chi1]

theorem control57_chi_values (j : Fin 2) (s : Fin 4) :
    control57_chi j (control57_mode s) =
      ![![control57_AB/control57_DAB, -control57_AA/control57_DAB,0,0],
        ![0,0,control57_AD/control57_DCD,-control57_AC/control57_DCD]] j s := by
  classical
  fin_cases j <;> fin_cases s <;>
    simp [control57_chi, control57_chi0, control57_chi1,
      control57_mA, control57_mB, control57_mC, control57_mD]

theorem control57_chi_off_modes (j : Fin 2) (m : SourceMode 2)
    (hA : m ≠ control57_mA) (hB : m ≠ control57_mB)
    (hC : m ≠ control57_mC) (hD : m ≠ control57_mD) :
    control57_chi j m = 0 := by
  classical
  fin_cases j <;>
    simp [control57_chi,control57_chi0,control57_chi1,
      hA,hB,hC,hD]

theorem control57_chi_gram (j k : Fin 2) :
    finitePairing (fun m => control57_chi j m) (control57_chi k) =
      if j=k then 1 else 0 := by
  have hAB := control57_DAB_pos.ne'
  have hCD := control57_DCD_pos.ne'
  have hsAB := control57_DAB_sq
  have hsCD := control57_DCD_sq
  fin_cases j <;> fin_cases k <;>
    simp [control57_chi, control57_chi0, control57_chi1,
      control57_pairing_add_right, control57_pairing_single,
      control57_mA, control57_mB, control57_mC, control57_mD] <;>
    field_simp [hAB,hCD] <;> nlinarith [hsAB,hsCD]

theorem control57_chi_raw_kernel (i : Fin 6) (j : Fin 2) :
    finitePairing (rawPinCoefficient 2 0 i) (control57_chi j) = 0 := by
  fin_cases j <;> fin_cases i <;>
    simp [control57_chi, control57_chi0, control57_chi1,
      control57_pairing_add_right, control57_pairing_single,
      control57_mA, control57_mB, control57_mC, control57_mD,
      control57_actual_raw_column, control57_AA,control57_AB,control57_AC,control57_AD] <;> ring

def control57_frame : RawPinFreeFrame 2 0 2 where
  chi := control57_chi
  gram := control57_chi_gram
  raw_kernel := control57_chi_raw_kernel

theorem four_cosine_raw_frame :
    (∀ j k, finitePairing (fun m => control57_frame.chi j m) (control57_frame.chi k) =
      if j=k then 1 else 0) ∧
    (∀ i j, finitePairing (rawPinCoefficient 2 0 i) (control57_frame.chi j) = 0) :=
  ⟨control57_frame.gram,control57_frame.raw_kernel⟩

theorem control57_shift_val {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (freeShiftSample F z ω).val m = ω.val m + ∑ j, z j*F.chi j m := by
  change ω.val m + (∑ j : Fin n, z j • F.chi j) m = _
  simp

theorem control57_residual_val {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (freeResidualSample F ω).val m =
      ω.val m - ∑ j, F.chi j m*freeCoordinate F ω j := by
  change (freeShiftSample F (-freeCoordinate F ω) ω).val m = _
  rw [control57_shift_val]
  simp only [Pi.neg_apply,neg_mul,Finset.sum_neg_distrib,sub_eq_add_neg]
  congr 1
  apply congrArg Neg.neg
  apply Finset.sum_congr rfl
  intro j _
  exact mul_comm _ _

def control57_singleFrame : RawPinFreeFrame 2 0 1 where
  chi := fun _ => control57_chi0
  gram := by
    intro j k
    fin_cases j
    fin_cases k
    simpa [control57_chi] using control57_chi_gram 0 0
  raw_kernel := by
    intro i j
    fin_cases j
    simpa [control57_chi] using control57_chi_raw_kernel i 0

theorem control57_one_coordinate (ω : SmoothSample 2 2) :
    freeCoordinate control57_singleFrame ω 0 = unitDirection control57_chi0 ω := by
  change finitePairing ω.val control57_chi0 = ∑' m, control57_chi0 m*ω.val m
  simpa only [mul_comm] using (control57_pairing_hasSum ω.val control57_chi0).tsum_eq.symm

theorem single_direction_identification (ω : SmoothSample 2 2) :
    freeCoordinate control57_singleFrame ω 0 = unitDirection control57_chi0 ω ∧
    ∀ m, (freeResidualSample control57_singleFrame ω).val m =
      unitDirectionCoefficientResidual control57_chi0 ω m := by
  refine ⟨control57_one_coordinate ω,?_⟩
  intro m
  rw [control57_residual_val]
  rw [Fin.sum_univ_one,control57_one_coordinate]
  rfl

theorem control57_single_standard_law :
    HasLaw (unitDirection (L := 2) control57_chi0) (gaussianReal 0 1) (smoothLaw 2 2) := by
  have hs : Summable (fun m => control57_chi0 m) := by
    simpa only [one_mul] using
      (control57_pairing_hasSum (fun _ => 1) control57_chi0).summable
  have hn : (∑' m, control57_chi0 m^2) = 1 := by
    calc
      (∑' m, control57_chi0 m^2) =
          finitePairing (fun m => control57_chi0 m) control57_chi0 := by
        simpa only [pow_two] using
          (control57_pairing_hasSum (fun m => control57_chi0 m) control57_chi0).tsum_eq
      _ = 1 := by simpa [control57_chi] using control57_chi_gram 0 0
  exact unitDirection_hasLaw (by norm_num) control57_chi0 hs hn

def control57_emptyFrame : RawPinFreeFrame 2 0 0 where
  chi := Fin.elim0
  gram := by intro j; exact Fin.elim0 j
  raw_kernel := by intro i j; exact Fin.elim0 j

theorem control57_empty_coordinate (ω : SmoothSample 2 2) :
    freeCoordinate control57_emptyFrame ω = 0 := by
  funext j
  exact Fin.elim0 j

theorem control57_empty_shift (z : Fin 0 → ℝ) (ω : SmoothSample 2 2) :
    freeShiftSample control57_emptyFrame z ω = ω := by
  apply Subtype.ext
  funext m
  rw [control57_shift_val]
  simp

theorem control57_empty_residual (ω : SmoothSample 2 2) :
    freeResidualSample control57_emptyFrame ω = ω :=
  control57_empty_shift _ _

theorem control57_empty_pi :
    Measure.pi (fun _ : Fin 0 => gaussianReal 0 1) = Measure.dirac (0 : Fin 0 → ℝ) := by
  ext s hs
  by_cases h : (0 : Fin 0 → ℝ) ∈ s
  · have he : s = Set.univ := by
      ext x
      simp only [Set.mem_univ,iff_true]
      simpa only [Subsingleton.elim x 0] using h
    simp [he]
  · have he : s = ∅ := by
      ext x
      simp only [Set.mem_empty_iff_false,iff_false]
      simpa only [Subsingleton.elim x 0] using h
    simp [he]

theorem empty_frame_maps_and_joint_law :
    (∀ ω, freeCoordinate control57_emptyFrame ω = 0 ∧
      freeResidualSample control57_emptyFrame ω = ω) ∧
    (∀ z ω, freeShiftSample control57_emptyFrame z ω = ω) ∧
    (smoothLaw 2 2).map (fun ω =>
      (freeResidualSample control57_emptyFrame ω,freeCoordinate control57_emptyFrame ω)) =
      ((smoothLaw 2 2).map (freeResidualSample control57_emptyFrame)).prod
        (Measure.dirac (0 : Fin 0 → ℝ)) := by
  refine ⟨fun ω => ⟨control57_empty_coordinate ω,control57_empty_residual ω⟩,
    control57_empty_shift,?_⟩
  rw [← control57_empty_pi]
  exact freeResidual_freeCoordinate_joint_map (by norm_num) control57_emptyFrame

theorem control57_two_frame_joint_law :
    (smoothLaw 2 2).map (fun ω => (freeResidualSample control57_frame ω,freeCoordinate control57_frame ω)) =
      ((smoothLaw 2 2).map (freeResidualSample control57_frame)).prod
        (Measure.pi (fun _ : Fin 2 => gaussianReal 0 1)) :=
  freeResidual_freeCoordinate_joint_map (by norm_num) control57_frame

def control57_psi : Fin 2 → (SourceMode 2 →₀ ℝ) :=
  ![(3/5 : ℝ) • control57_chi0 + (4/5 : ℝ) • control57_chi1,
    (-4/5 : ℝ) • control57_chi0 + (3/5 : ℝ) • control57_chi1]

theorem control57_psi_gram (j k : Fin 2) :
    finitePairing (fun m => control57_psi j m) (control57_psi k) =
      if j=k then 1 else 0 := by
  have h00 : finitePairing (fun m => control57_chi0 m) control57_chi0 = 1 := by
    simpa [control57_chi] using control57_chi_gram 0 0
  have h01 : finitePairing (fun m => control57_chi0 m) control57_chi1 = 0 := by
    simpa [control57_chi] using control57_chi_gram 0 1
  have h10 : finitePairing (fun m => control57_chi1 m) control57_chi0 = 0 := by
    simpa [control57_chi] using control57_chi_gram 1 0
  have h11 : finitePairing (fun m => control57_chi1 m) control57_chi1 = 1 := by
    simpa [control57_chi] using control57_chi_gram 1 1
  fin_cases j <;> fin_cases k <;>
    norm_num [control57_psi,control57_pairing_add_right,control57_pairing_smul_right,
      Finsupp.add_apply,Finsupp.smul_apply,smul_eq_mul,
      control57_pairing_add_left,control57_pairing_mul_left,
      control57_pairing_neg_left,control57_pairing_neg_right,h00,h01,h10,h11]

theorem control57_psi_raw_kernel (i : Fin 6) (j : Fin 2) :
    finitePairing (rawPinCoefficient 2 0 i) (control57_psi j) = 0 := by
  have h0 : finitePairing (rawPinCoefficient 2 0 i) control57_chi0 = 0 := by
    simpa [control57_chi] using control57_chi_raw_kernel i 0
  have h1 : finitePairing (rawPinCoefficient 2 0 i) control57_chi1 = 0 := by
    simpa [control57_chi] using control57_chi_raw_kernel i 1
  fin_cases j <;>
    simp [control57_psi,control57_pairing_add_right,control57_pairing_smul_right,
      h0,h1]

def control57_rotatedFrame : RawPinFreeFrame 2 0 2 where
  chi := control57_psi
  gram := control57_psi_gram
  raw_kernel := control57_psi_raw_kernel

theorem control57_psi_named_nonzero (j : Fin 2) (s : Fin 4) :
    control57_psi j (control57_mode s) ≠ 0 := by
  have hA := (control57_amplitude_pos 0).ne'
  have hB := (control57_amplitude_pos 1).ne'
  have hC := (control57_amplitude_pos 2).ne'
  have hD := (control57_amplitude_pos 3).ne'
  have hAB := control57_DAB_pos.ne'
  have hCD := control57_DCD_pos.ne'
  fin_cases j <;> fin_cases s <;>
    simp [control57_psi,control57_chi0,control57_chi1,
      control57_mA,control57_mB,control57_mC,control57_mD,
      control57_AA,control57_AB,control57_AC,control57_AD,hA,hB,hC,hD,hAB,hCD]

theorem control57_psi_support (j : Fin 2) :
    (control57_psi j).support = {control57_mA,control57_mB,control57_mC,control57_mD} := by
  classical
  ext m
  by_cases hA : m=control57_mA
  · subst m
    simpa [Finsupp.mem_support_iff,control57_mA] using control57_psi_named_nonzero j 0
  by_cases hB : m=control57_mB
  · subst m
    simpa [Finsupp.mem_support_iff,control57_mB] using control57_psi_named_nonzero j 1
  by_cases hC : m=control57_mC
  · subst m
    simpa [Finsupp.mem_support_iff,control57_mC] using control57_psi_named_nonzero j 2
  by_cases hD : m=control57_mD
  · subst m
    simpa [Finsupp.mem_support_iff,control57_mD] using control57_psi_named_nonzero j 3
  fin_cases j <;>
    simp [Finsupp.mem_support_iff,control57_psi,control57_chi0,control57_chi1,
      hA,hB,hC,hD]

theorem control57_rotated_coordinates (ω : SmoothSample 2 2) :
    freeCoordinate control57_rotatedFrame ω =
      ![(3*freeCoordinate control57_frame ω 0+4*freeCoordinate control57_frame ω 1)/5,
        (-4*freeCoordinate control57_frame ω 0+3*freeCoordinate control57_frame ω 1)/5] := by
  ext j
  fin_cases j <;>
    simp [freeCoordinate,control57_rotatedFrame,control57_frame,control57_psi,control57_chi,
      control57_pairing_add_right,control57_pairing_smul_right] <;> ring

theorem control57_full_projection (ω : SmoothSample 2 2) (m : SourceMode 2) :
    (∑ j : Fin 2, control57_rotatedFrame.chi j m*freeCoordinate control57_rotatedFrame ω j) =
      ∑ j : Fin 2, control57_frame.chi j m*freeCoordinate control57_frame ω j := by
  rw [control57_rotated_coordinates]
  simp [control57_rotatedFrame,control57_frame,control57_psi,control57_chi,
    Fin.sum_univ_succ,Finsupp.add_apply,Finsupp.smul_apply,smul_eq_mul]
  ring

theorem control57_rotated_residual (ω : SmoothSample 2 2) :
    freeResidualSample control57_rotatedFrame ω = freeResidualSample control57_frame ω := by
  apply Subtype.ext
  funext m
  rw [control57_residual_val,control57_residual_val,control57_full_projection]

theorem rotated_frame_coordinates_and_projection (ω : SmoothSample 2 2) :
    freeCoordinate control57_rotatedFrame ω =
      ![(3*freeCoordinate control57_frame ω 0+4*freeCoordinate control57_frame ω 1)/5,
        (-4*freeCoordinate control57_frame ω 0+3*freeCoordinate control57_frame ω 1)/5] ∧
    freeResidualSample control57_rotatedFrame ω = freeResidualSample control57_frame ω ∧
    ∀ m, (∑ j : Fin 2, control57_rotatedFrame.chi j m*freeCoordinate control57_rotatedFrame ω j) =
      ∑ j : Fin 2, control57_frame.chi j m*freeCoordinate control57_frame ω j :=
  ⟨control57_rotated_coordinates ω,control57_rotated_residual ω,control57_full_projection ω⟩

def control57_omegaA : SmoothSample 2 2 :=
  finiteShiftSample (Finsupp.single control57_mA 1) (zeroSample 2 2)

def control57_eraseFourSample (ω : SmoothSample 2 2) : SmoothSample 2 2 :=
  finiteShiftSample (-(Finsupp.single control57_mA (ω.val control57_mA) +
    Finsupp.single control57_mB (ω.val control57_mB) +
    Finsupp.single control57_mC (ω.val control57_mC) +
    Finsupp.single control57_mD (ω.val control57_mD))) ω

theorem control57_omegaA_coordinates :
    freeCoordinate control57_frame control57_omegaA = ![control57_AB/control57_DAB,0] := by
  ext j
  fin_cases j <;>
    simp [freeCoordinate,control57_frame,control57_chi,control57_chi0,control57_chi1,
      control57_pairing_add_right,control57_pairing_single,
      control57_omegaA,finiteShiftSample_val,zeroSample,
      control57_mA,control57_mB,control57_mC,control57_mD]

theorem control57_omegaA_residual_A :
    (freeResidualSample control57_frame control57_omegaA).val control57_mA =
      control57_AA^2/control57_DAB^2 := by
  rw [control57_residual_val,control57_omegaA_coordinates]
  simp [control57_frame,control57_chi,control57_chi0,control57_chi1,
    control57_omegaA,finiteShiftSample_val,zeroSample,Fin.sum_univ_succ,
    control57_mA,control57_mB,control57_mC,control57_mD]
  field_simp [control57_DAB_pos.ne']
  nlinarith [control57_DAB_sq]

theorem projection_keeps_complement :
    (freeResidualSample control57_frame control57_omegaA).val control57_mA =
      control57_AA^2/control57_DAB^2 ∧
    (freeResidualSample control57_rotatedFrame control57_omegaA).val control57_mA =
      control57_AA^2/control57_DAB^2 ∧
    0 < control57_AA^2/control57_DAB^2 ∧
    (control57_eraseFourSample control57_omegaA).val control57_mA = 0 := by
  refine ⟨control57_omegaA_residual_A,?_,?_,?_⟩
  · rw [control57_rotated_residual]
    exact control57_omegaA_residual_A
  · exact div_pos (sq_pos_of_pos (control57_amplitude_pos 0))
      (sq_pos_of_pos control57_DAB_pos)
  · simp [control57_eraseFourSample,finiteShiftSample_val,
      control57_mA,control57_mB,control57_mC,control57_mD]

theorem singular_posterior_reconstruction (t : Fin 6 → ℝ) (ω : SmoothSample 2 2) :
    rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 t ω =
      freeShiftSample control57_frame (freeCoordinate control57_frame ω)
        (rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 t
          (freeResidualSample control57_frame ω)) :=
  rawPosteriorSample_free_reconstruction (by norm_num) control57_frame t ω

def control57_omega1 : SmoothSample 2 2 := finiteShiftSample control57_chi1 (zeroSample 2 2)
def control57_q : ℝ := control57_AD/control57_DCD

theorem control57_q_pos : 0 < control57_q :=
  div_pos (control57_amplitude_pos 3) control57_DCD_pos

theorem control57_omega1_coordinates : freeCoordinate control57_frame control57_omega1 = ![0,1] := by
  ext j
  change finitePairing (fun m => 0+control57_chi1 m) (control57_chi j) = _
  simp only [zero_add]
  have h := control57_chi_gram 1 j
  fin_cases j <;> simpa [control57_chi] using h

theorem control57_omega1_residual :
    freeResidualSample control57_frame control57_omega1 = zeroSample 2 2 := by
  apply Subtype.ext
  funext m
  rw [control57_residual_val,control57_omega1_coordinates]
  simp [control57_omega1,finiteShiftSample_val,zeroSample,control57_frame,control57_chi,
    Fin.sum_univ_succ]

theorem control57_zero_rawPins : rawPins 2 0 (zeroSample 2 2) = 0 := by
  rw [rawPins_series (by norm_num)]
  ext i
  simp [scalarSeries,sampleInclusion,zeroSample]

theorem control57_omega1_rawPins : rawPins 2 0 control57_omega1 = 0 := by
  rw [control57_omega1,rawPins_finiteShiftSample (by norm_num),control57_zero_rawPins]
  ext i
  simpa [control57_chi] using control57_chi_raw_kernel i 1

theorem control57_zero_posterior :
    rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 (zeroSample 2 2) = zeroSample 2 2 := by
  apply Subtype.ext
  funext m
  rw [rawPosteriorSample_val,control57_zero_rawPins]
  simp [zeroSample,rawPinLift]

theorem control57_omega1_posterior :
    rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control57_omega1 = control57_omega1 := by
  rw [control57_omega1,rawPosteriorSample_finiteShiftSample (by norm_num) 0 0 control57_chi1
    (fun i => by simpa [control57_chi] using control57_chi_raw_kernel i 1),
    control57_zero_posterior]

def control57_mutantResidual (ω : SmoothSample 2 2) : SmoothSample 2 2 :=
  finiteShiftSample ((-freeCoordinate control57_frame ω 0) • control57_chi0) ω

theorem control57_mutantResidual_omega1 : control57_mutantResidual control57_omega1 = control57_omega1 := by
  apply Subtype.ext
  funext m
  simp [control57_mutantResidual,control57_omega1_coordinates,finiteShiftSample_val]

def control57_mutantReconstruction : SmoothSample 2 2 :=
  freeShiftSample control57_frame (freeCoordinate control57_frame control57_omega1)
    (rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0
      (control57_mutantResidual control57_omega1))

theorem control57_original_named_coefficient :
    (rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control57_omega1).val control57_mC = control57_q := by
  rw [control57_omega1_posterior]
  simp [control57_omega1,finiteShiftSample_val,zeroSample,control57_chi1,control57_q,
    control57_mC,control57_mD]

theorem control57_mutant_named_coefficient :
    control57_mutantReconstruction.val control57_mC = 2*control57_q := by
  unfold control57_mutantReconstruction
  rw [control57_mutantResidual_omega1,control57_omega1_posterior,control57_shift_val,
    control57_omega1_coordinates]
  simp [control57_omega1,finiteShiftSample_val,zeroSample,control57_frame,control57_chi,
    control57_chi1,control57_q,Fin.sum_univ_succ,
    control57_mC,control57_mD]
  ring

theorem second_projection_omission_counterexample :
    (rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control57_omega1).val control57_mC ≠
      control57_mutantReconstruction.val control57_mC := by
  rw [control57_original_named_coefficient,control57_mutant_named_coefficient]
  nlinarith [control57_q_pos]

theorem control57_mutant_equality_iff_false :
    ((rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control57_omega1).val control57_mC =
      control57_mutantReconstruction.val control57_mC) ↔ False := by
  exact iff_false_intro second_projection_omission_counterexample

end FreeCoordinateControls
end
