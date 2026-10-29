import SpecificationProofs.P15Elementary
import Closure.DownsetMass

namespace UniversalLaw.P15Closure

open UniversalLaw.Spec.P15

/-- The positive affine exponential denominator of a coordinate section. -/
theorem affine_exp_pos {A B : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hAB : 0 < A + B) (x : ℝ) : 0 < A + B * Real.exp (-x) := by
  rcases lt_or_eq_of_le hA with hA | hA
  · exact add_pos_of_pos_of_nonneg hA (mul_nonneg hB (Real.exp_pos _).le)
  · have hB' : 0 < B := by linarith
    exact add_pos_of_nonneg_of_pos hA.le (mul_pos hB' (Real.exp_pos _))

/-- The first derivative in the coordinate-hazard argument. -/
theorem hasDerivAt_neg_log_affine_exp {A B : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hAB : 0 < A + B) (x : ℝ) :
    HasDerivAt (fun s : ℝ => -Real.log (A + B * Real.exp (-s)))
      (B / (A * Real.exp x + B)) x := by
  have hp := affine_exp_pos hA hB hAB x
  have hx : Real.exp x ≠ 0 := (Real.exp_pos x).ne'
  have hd := (((hasDerivAt_const x A).add
    (((hasDerivAt_id x).neg.exp).const_mul B)).log hp.ne').neg
  change HasDerivAt (fun s : ℝ => -Real.log (A + B * Real.exp (-s)))
    (-((0 + B * (Real.exp (-x) * -1)) / (A + B * Real.exp (-x)))) x at hd
  convert hd using 1
  rw [Real.exp_neg]
  field_simp
  ring

/-- Negative log of a nonnegative affine exponential is concave. -/
theorem concaveOn_neg_log_affine_exp {A B : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hAB : 0 < A + B) :
    ConcaveOn ℝ Set.univ (fun s : ℝ => -Real.log (A + B * Real.exp (-s))) := by
  have hd := hasDerivAt_neg_log_affine_exp hA hB hAB
  have hpos : ∀ x : ℝ, 0 < A * Real.exp x + B := by
    intro x
    rcases lt_or_eq_of_le hB with hb | hb
    · exact add_pos_of_nonneg_of_pos (mul_nonneg hA (Real.exp_pos _).le) hb
    · have ha : 0 < A := by linarith
      exact add_pos_of_pos_of_nonneg (mul_pos ha (Real.exp_pos x)) hB
  apply AntitoneOn.concaveOn_of_deriv convex_univ
    (fun x _ => (hd x).continuousAt.continuousWithinAt)
    (fun x _ => (hd x).differentiableAt.differentiableWithinAt)
  intro x _ y _ hxy
  rw [(hd x).deriv, (hd y).deriv]
  exact div_le_div_of_nonneg_left hB (hpos x) (by
    nlinarith [mul_nonneg hA (sub_nonneg.mpr (Real.exp_le_exp.mpr hxy))])

/-- One nonnegative concave coordinate gives its endpoint chord bound. -/
theorem coordinate_chord {f : ℝ → ℝ}
    (hc : ConcaveOn ℝ (Set.Icc (0 : ℝ) 1) f) (h0 : 0 ≤ f 0)
    {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : t * f 1 ≤ f t := by
  have h := hc.2 (show (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 by constructor <;> norm_num)
    (show (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 by constructor <;> norm_num)
    (show 0 ≤ 1 - t by linarith) ht0 (show 1 - t + t = 1 by ring)
  simp only [smul_eq_mul, mul_zero, mul_one, zero_add] at h
  have hn : 0 ≤ (1 - t) * f 0 := mul_nonneg (by linarith) h0
  linarith

/-- Iteration of separate coordinate chord inequalities on any finite cube. -/
theorem product_chord_of_coordinate_chord {Y : Type} [Fintype Y] [DecidableEq Y]
    (f : (Y → ℝ) → ℝ)
    (hc : ∀ t : Y → ℝ, (∀ i, 0 ≤ t i ∧ t i ≤ 1) → ∀ i,
      t i * f (Function.update t i 1) ≤ f t)
    (t : Y → ℝ) (ht : ∀ i, 0 ≤ t i ∧ t i ≤ 1) :
    (∏ i, t i) * f (fun _ => 1) ≤ f t := by
  have main : ∀ s : Finset Y,
      (∏ i ∈ s, t i) * f (fun i => if i ∈ s then 1 else t i) ≤ f t := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp
    | @insert a s ha ih =>
      let u : Y → ℝ := fun i => if i ∈ s then 1 else t i
      have hu : ∀ i, 0 ≤ u i ∧ u i ≤ 1 := by
        intro i
        dsimp [u]
        split_ifs <;> simp_all
      have hua : u a = t a := by simp [u, ha]
      have heq : Function.update u a 1 = fun i => if i ∈ insert a s then 1 else t i := by
        funext i
        by_cases hi : i = a
        · subst i; simp
        · simp [u, hi]
      have h := hc u hu a
      rw [hua, heq] at h
      have hp : 0 ≤ ∏ i ∈ s, t i := Finset.prod_nonneg (fun i _ => (ht i).1)
      have hmul := mul_le_mul_of_nonneg_left h hp
      rw [Finset.prod_insert ha]
      nlinarith [hmul]
  simpa using main Finset.univ

/-- Separate concavity and nonnegativity suffice for the product endpoint bound. -/
theorem product_chord_of_separate_concavity {Y : Type} [Fintype Y] [DecidableEq Y]
    (f : (Y → ℝ) → ℝ)
    (hn : ∀ t : Y → ℝ, (∀ i, 0 ≤ t i ∧ t i ≤ 1) → 0 ≤ f t)
    (hc : ∀ t : Y → ℝ, (∀ i, 0 ≤ t i ∧ t i ≤ 1) → ∀ i,
      ConcaveOn ℝ (Set.Icc (0 : ℝ) 1) (fun s => f (Function.update t i s)))
    (t : Y → ℝ) (ht : ∀ i, 0 ≤ t i ∧ t i ≤ 1) :
    (∏ i, t i) * f (fun _ => 1) ≤ f t := by
  apply product_chord_of_coordinate_chord f _ t ht
  intro u hu i
  have hzero : 0 ≤ f (Function.update u i 0) := by
    apply hn
    intro j
    by_cases hj : j = i
    · subst j; simp
    · simpa [Function.update_of_ne hj] using hu j
  have h := coordinate_chord (hc u hu i) hzero (hu i).1 (hu i).2
  simpa using h

/-- The exponential probability parameter lies in the probability cube. -/
theorem hazard_probability_bounds {t : ℝ} (ht : 0 ≤ t) :
    0 ≤ 1 - Real.exp (-t) ∧ 1 - Real.exp (-t) < 1 := by
  have he : Real.exp (-t) ≤ 1 := by rw [Real.exp_le_one_iff]; linarith
  have hp := Real.exp_pos (-t)
  constructor <;> linarith

/-- Both endpoint bounds for the transformed price ceiling. -/
theorem phi_bounds {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    0 ≤ phi p ∧ phi p ≤ 1 := by
  unfold phi
  split_ifs with h
  · have hl : Real.log (1 - p) ≤ 0 := Real.log_nonpos (by linarith) (by linarith)
    constructor
    · exact le_min (by norm_num) (by linarith)
    · exact min_le_left _ _
  · constructor <;> norm_num

/-- Truncating the hazard can only lower an original probability, including `p = 1`. -/
theorem transformed_probability_le {p : ℝ} (_hp0 : 0 ≤ p) (_hp1 : p ≤ 1) :
    1 - Real.exp (-phi p) ≤ p := by
  by_cases h : p < 1
  · have hp : 0 < 1 - p := by linarith
    have ht : phi p ≤ -Real.log (1 - p) := by simp only [phi, ite_eq_left h]; exact min_le_right _ _
    have he : 1 - p ≤ Real.exp (-phi p) := by
      calc
        1 - p = Real.exp (Real.log (1 - p)) := (Real.exp_log hp).symm
        _ ≤ Real.exp (-phi p) := Real.exp_le_exp.mpr (by linarith)
    linarith
  · have he := Real.exp_pos (-phi p)
    linarith

/-- Coordinate hazards are negative logarithms of nonnegative affine exponentials. -/
theorem hazard_coordinate_sections {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y)) (hA : IsProperDownset A)
    (t : Y → ℝ) (ht : ∀ j, 0 ≤ t j ∧ t j ≤ 1) (i : Y) :
    ∃ A0 B0 : ℝ, 0 ≤ A0 ∧ 0 ≤ B0 ∧ 0 < A0 + B0 ∧
      ∀ s : ℝ, muOf A (fun j => 1 - Real.exp (-Function.update t i s j)) =
        A0 + B0 * Real.exp (-s) := by
  let p : Y → ℝ := fun j => 1 - Real.exp (-t j)
  have hp : ∀ j, 0 ≤ p j ∧ p j ≤ 1 := fun j =>
    ⟨(hazard_probability_bounds (ht j).1).1, (hazard_probability_bounds (ht j).1).2.le⟩
  let m0 := muOf A (Function.update p i 0)
  let m1 := muOf A (Function.update p i 1)
  have hm1 : 0 ≤ m1 := by
    apply muOf_nonneg
    intro j
    by_cases hj : j = i
    · subst j; simp
    · simpa [Function.update_of_ne hj] using hp j
  have hm10 : m1 ≤ m0 := muOf_update_one_le_zero A hA.2.2 p hp i
  have hm0 : 0 < m0 := by
    apply muOf_pos_of_empty_mem A _ hA.1
    · intro j
      by_cases hj : j = i
      · subst j; simp
      · simpa [Function.update_of_ne hj] using (hp j).1
    · intro j
      by_cases hj : j = i
      · subst j; simp
      · simpa [Function.update_of_ne hj, p] using (hazard_probability_bounds (ht j).1).2
  refine ⟨m1, m0 - m1, hm1, sub_nonneg.mpr hm10, by linarith, ?_⟩
  intro s
  have heq : (fun j => 1 - Real.exp (-Function.update t i s j)) =
      Function.update p i (1 - Real.exp (-s)) := by
    funext j
    by_cases hj : j = i <;> simp [hj, p]
  rw [heq, muOf_update_endpoints]
  change (1 - (1 - Real.exp (-s))) * m0 + (1 - Real.exp (-s)) * m1 = _
  ring

/-- Exact registered coordinatewise concavity proposition. -/
theorem coordinatewiseConcavity : CoordinatewiseConcavity := by
  intro n A _ hA i t ht
  obtain ⟨A0, B0, hA0, hB0, hsum, heq⟩ := hazard_coordinate_sections A hA t ht i
  have hf : (fun s : ℝ => hazardCoord A (Function.update t i s)) =
      (fun s : ℝ => -Real.log (A0 + B0 * Real.exp (-s))) := by
    funext s
    exact congrArg (fun z => -Real.log z) (heq s)
  rw [hf]
  exact (concaveOn_neg_log_affine_exp hA0 hB0 hsum).subset
    (fun _ _ => Set.mem_univ _) (convex_Icc _ _)

/-- Every probability-cube hazard is nonnegative. -/
theorem hazardCoord_nonneg {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y)) (t : Y → ℝ) (ht : ∀ j, 0 ≤ t j ∧ t j ≤ 1) :
    0 ≤ hazardCoord A t := by
  let p : Y → ℝ := fun j => 1 - Real.exp (-t j)
  have hp : ∀ j, 0 ≤ p j ∧ p j ≤ 1 := fun j =>
    ⟨(hazard_probability_bounds (ht j).1).1, (hazard_probability_bounds (ht j).1).2.le⟩
  exact neg_nonneg.mpr (Real.log_nonpos (muOf_nonneg A p hp) (muOf_le_one A p hp))

/-- The all-one hazard vector is the reference hazard in the specification. -/
theorem hazardCoord_ones {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y)) : hazardCoord A (fun _ => 1) = hazardStar A := by
  simp only [hazardCoord, hazardStar, pStar]

/-- Exact registered product hazard bound (F6). -/
theorem hazardProductBound : HazardProductBound := by
  intro n A hn hA t ht
  have h := product_chord_of_separate_concavity (hazardCoord A)
    (hazardCoord_nonneg A)
    (fun u hu i => coordinatewiseConcavity n A hn hA i u hu) t ht
  simpa only [hazardCoord_ones] using h

/-- Exact registered transformed-probability hazard bound (F7), with every endpoint. -/
theorem hazardPhiBound : HazardPhiBound := by
  intro n A hn hA p hp hmu
  let t : Fin n → ℝ := fun i => phi (p i)
  let q : Fin n → ℝ := fun i => 1 - Real.exp (-t i)
  have ht : ∀ i, 0 ≤ t i ∧ t i ≤ 1 := fun i => phi_bounds (hp i).1 (hp i).2
  have hq : ∀ i, 0 ≤ q i ∧ q i ≤ 1 := fun i =>
    ⟨(hazard_probability_bounds (ht i).1).1, (hazard_probability_bounds (ht i).1).2.le⟩
  have hqp : ∀ i, q i ≤ p i := fun i => transformed_probability_le (hp i).1 (hp i).2
  have hmass : muOf A p ≤ muOf A q := muOf_antitone A hA.2.2 q p hq hp hqp
  have hlog := Real.log_le_log hmu hmass
  have hprod := hazardProductBound n A hn hA t ht
  change (∏ i, phi (p i)) * hazardStar A ≤ -Real.log (muOf A q) at hprod
  calc
    hazardStar A * ∏ i, phi (p i) = (∏ i, phi (p i)) * hazardStar A := mul_comm _ _
    _ ≤ -Real.log (muOf A q) := hprod
    _ ≤ -Real.log (muOf A p) := neg_le_neg hlog

/-- Exact registered full-ground generator price bound (F8). -/
theorem fullGroundPriceBound : FullGroundPriceBound := by
  intro n A hn hA p c hp hc
  have hc1 : ∀ i, c i ≤ 1 := fun i => (hc i).2.trans (phi_bounds (hp i).1 (hp i).2).2
  have hprice1 : (∏ i, c i) ≤ 1 :=
    Finset.prod_le_one₀ (fun i _ => (hc i).1) (fun i _ => hc1 i)
  by_cases hmu : 0 < muOf A p
  · have hphi := hazardPhiBound n A hn hA p hp hmu
    have hH := UniversalLaw.Proofs.P15Elementary.hazardStarPositive n A hn hA
    have hpricephi : (∏ i, c i) ≤ ∏ i, phi (p i) :=
      Finset.prod_le_prod₀ (fun i _ => (hc i).1) (fun i _ => (hc i).2)
    have hpricehaz : (∏ i, c i) ≤ (1 / hazardStar A) * (-Real.log (muOf A p)) := by
      have hmul : (∏ i, c i) * hazardStar A ≤ -Real.log (muOf A p) := by
        nlinarith [mul_le_mul_of_nonneg_left hpricephi hH.le]
      have hdiv := (le_div_iff₀ hH).mpr hmul
      simpa only [div_eq_mul_inv, one_mul, mul_comm] using hdiv
    simp only [cappedHazard, ite_eq_left hmu]
    exact le_min hprice1 hpricehaz
  · simpa only [cappedHazard, ite_eq_right hmu] using hprice1

/-- Exact registered reference-hazard criterion for the full-ground budget. -/
theorem fullGroundBudgetIff : FullGroundBudgetIff := by
  intro n A hn hA
  constructor
  · intro hbudget
    have hp0 := UniversalLaw.Proofs.P15Elementary.Aux.pStar_pos
    have hp1 := UniversalLaw.Proofs.P15Elementary.Aux.pStar_lt_one
    have hphi := UniversalLaw.Proofs.P15Elementary.phiAtPStar
    have hmu : 0 < muOf A (fun _ => pStar) :=
      muOf_pos_of_empty_mem A _ hA.1 (fun _ => hp0.le) (fun _ => hp1)
    have h := hbudget (fun _ => pStar) (fun _ => 1)
      (fun _ => ⟨hp0.le, hp1.le⟩) (fun _ => ⟨by norm_num, by rw [hphi]⟩)
    have hh : 1 ≤ min 1 (-Real.log (muOf A (fun _ => pStar))) := by
      simpa only [Finset.prod_const_one, cappedHazard, ite_eq_left hmu, one_mul] using h
    exact hh.trans (min_le_right _ _)
  · intro hH p c hp hc
    have hc1 : ∀ i, c i ≤ 1 := fun i => (hc i).2.trans (phi_bounds (hp i).1 (hp i).2).2
    have hprice1 : (∏ i, c i) ≤ 1 := Finset.prod_le_one₀ (fun i _ => (hc i).1) (fun i _ => hc1 i)
    by_cases hmu : 0 < muOf A p
    · have hphi := hazardPhiBound n A hn hA p hp hmu
      have hphinn : 0 ≤ ∏ i, phi (p i) := Finset.prod_nonneg
        (fun i _ => (phi_bounds (hp i).1 (hp i).2).1)
      have hpricephi : (∏ i, c i) ≤ ∏ i, phi (p i) :=
        Finset.prod_le_prod₀ (fun i _ => (hc i).1) (fun i _ => (hc i).2)
      have hpricehaz : (∏ i, c i) ≤ -Real.log (muOf A p) := by
        calc
          (∏ i, c i) ≤ ∏ i, phi (p i) := hpricephi
          _ ≤ hazardStar A * ∏ i, phi (p i) := by nlinarith
          _ ≤ -Real.log (muOf A p) := hphi
      simp only [cappedHazard, ite_eq_left hmu, one_mul]
      exact le_min hprice1 hpricehaz
    · simpa only [cappedHazard, ite_eq_right hmu] using hprice1

#check coordinatewiseConcavity
#check hazardProductBound
#check hazardPhiBound
#check fullGroundPriceBound
#check fullGroundBudgetIff
#print axioms coordinatewiseConcavity
#print axioms hazardProductBound
#print axioms hazardPhiBound
#print axioms fullGroundPriceBound
#print axioms fullGroundBudgetIff

#print axioms affine_exp_pos
#print axioms hasDerivAt_neg_log_affine_exp
#print axioms concaveOn_neg_log_affine_exp
#print axioms coordinate_chord
#print axioms product_chord_of_coordinate_chord

end UniversalLaw.P15Closure
