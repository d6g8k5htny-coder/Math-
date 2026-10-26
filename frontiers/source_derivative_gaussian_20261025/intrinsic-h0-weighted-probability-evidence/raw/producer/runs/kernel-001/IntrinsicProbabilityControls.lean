import SourceIntrinsicH0WeightedProbability

noncomputable section
open CategoryTheory Limits Set MeasureTheory BoundedContinuousFunction
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceH0OlderClearance I4SourceIntrinsicH0Interface
open I4SourceActualFoldCandidate I4SourceIntrinsicH0WeightedProbability
open I4SourceConfluentPins TorusFiltration SourceCompactFoldWeightedProbability ResearchFormalCoreR1
set_option autoImplicit false
namespace IntrinsicProbabilityControls

def zeroBCF : E 2 →ᵇ ℝ := 0

theorem zero_bcf_clearance_empty :
    superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0 = ∅ := by
  ext h
  constructor
  · rintro ⟨P,hP,_⟩
    exact (lt_irrefl (0 : ℝ) hP).elim
  · exact False.elim

theorem zero_bcf_death : superlevelBar_deathHeight (zeroBCF : E 2 → ℝ) 0 = 0 :=
  superlevelBar_death_eq_zero_of_empty _ _ zero_bcf_clearance_empty

/-- Correct new guarded upper-cut formula at both sides of the empty default. -/
theorem zero_bcf_guarded_preimages :
    ((-1 : ℝ) < superlevelBar_deathHeight (zeroBCF : E 2 → ℝ) 0 ↔
      (-1 : ℝ) ∈ superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0 ∨
        ((-1 : ℝ) < 0 ∧ ¬ (superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0).Nonempty)) ∧
    ((1 : ℝ) < superlevelBar_deathHeight (zeroBCF : E 2 → ℝ) 0 ↔
      (1 : ℝ) ∈ superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0 ∨
        ((1 : ℝ) < 0 ∧ ¬ (superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0).Nonempty)) := by
  rw [zero_bcf_death,zero_bcf_clearance_empty]
  norm_num

theorem zero_bcf_no_threshold_pair (S : E 2) :
    ¬ h0ThresholdPair (zeroBCF : E 2 → ℝ) 0 S := by
  rintro ⟨_hM,_hS,hcut⟩
  have hc : superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0 = Iio (zeroBCF S) :=
    (h0Interface_cut_death_eq_C263 2 _ zeroBCF.continuous 0).1.symm.trans hcut
  have hi : (-1 : ℝ) ∈ Iio (zeroBCF S) := by norm_num [zeroBCF]
  rw [← hc,zero_bcf_clearance_empty] at hi
  exact hi

/-- Independent concrete witness before the sole empty-branch mutation. -/
theorem zero_bcf_mutation_counterexample :
    (-1 : ℝ) < superlevelBar_deathHeight (zeroBCF : E 2 → ℝ) 0 ∧
      (-1 : ℝ) ∉ superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0 := by
  rw [zero_bcf_death,zero_bcf_clearance_empty]
  norm_num

def ordinaryQ (a b c : ℝ) (v : Fin 2 → ℝ) : ℝ :=
  a*(v 0)^2 + 2*b*(v 0)*(v 1) + c*(v 1)^2

/-- Concrete scalar/matrix cases for the private exact-form inertia controls.
Those private controls conclude genuine Lifetime inertia under exact hessian
identities; these are ordinary forms, not fabricated Gaussian realizations. -/
theorem planar_matrix_controls :
    dm2Negative !![(-1 : ℝ),0;0,-1] ∧
    (!![(-1 : ℝ),0;0,-1]).det = 1 ∧
    (!![(1 : ℝ),0;0,-1]).det = -1 ∧
    (!![(0 : ℝ),1;1,0]).det = -1 ∧
    ordinaryQ 0 1 0 ![-1,1] < 0 ∧ 0 < ordinaryQ 0 1 0 ![1,1] ∧
    (!![(1 : ℝ),2;2,3]).det = -1 := by
  refine ⟨(dm2_negative_iff (-1) 0 (-1)).2 (by norm_num),?_⟩
  norm_num [Matrix.det_fin_two,ordinaryQ]

/-- Literal event test at singular pins, without any normalized-law claim. -/
theorem zero_radius_event_empty : sourceIntrinsicFiniteBarEvent 2 0 = ∅ := by
  ext ω
  constructor
  · rintro ⟨_hcan,hgap,_hpair⟩
    have heq : endpointLiftM 0 = endpointLiftS 0 := by
      norm_num [endpointLiftM,endpointLiftS,endpointM,endpointS]
    change 0 < actualField 2 2 ω (endpointLiftM 0) - actualField 2 2 ω (endpointLiftS 0) at hgap
    rw [heq,sub_self] at hgap
    exact (lt_irrefl (0 : ℝ) hgap).elim
  · exact False.elim

theorem positivePeriod : (0 : ℝ) < 2 := by norm_num

/-- Actual compact-mark event/mass specialization, with constants before marks. -/
theorem actual_compact_probability :
    ∃ C rStar : ℝ, 0 ≤ C ∧ 0 < rStar ∧ rStar ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r ≤ rStar → ∀ b k : ℝ, |b| ≤ 3 → 1 ≤ k → k ≤ 2 →
        let QW := sourceCompactFoldWeightedLaw positivePeriod.ne' r b k
        let E := sourceIntrinsicFiniteBarEvent 2 r
        let p := sourceIntrinsicFiniteBarProbability positivePeriod r b k
        IsProbabilityMeasure QW ∧ QW.real Eᶜ = 1-p ∧
          0 ≤ p ∧ p ≤ 1 ∧ 0 ≤ 1-p ∧ 1-p ≤ C*r^3 := by
  obtain ⟨C,rStar,hC,hr,hr1,_hrL,h⟩ := sourceIntrinsicFiniteBarProbability_uniform
    positivePeriod 3 1 2 (by norm_num) (by norm_num) (by norm_num)
  exact ⟨C,rStar,hC,hr,hr1,h⟩

end IntrinsicProbabilityControls
