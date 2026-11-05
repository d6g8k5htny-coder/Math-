from pathlib import Path
packet=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
p=packet/'SourceGapWeightedNumerator.lean'
s=p.read_text().replace('\nend I4SourceGapWeightedNumerator\n','\n')
s+='''
/-- Existing all-height moments specialized uniformly to a compact height set.
The radius is chosen before the moment order and every displayed mark. -/
theorem sourceGapLaw_compact_moments {L : ℝ} (hL : L ≠ 0)
    (B K : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceGammaRadius L ω^n) (sourceGapLaw hL r b k) ∧
        (∫ ω, sourceGammaRadius L ω^n ∂sourceGapLaw hL r b k) ≤ C := by
  obtain ⟨δ,hδ,hδ1,hmom⟩ := sourceGapLaw_height_moments hL K hK
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hbound⟩ := hmom n
  refine ⟨C*(1+B)^n,by positivity,?_⟩
  intro r hr hrδ b k hb hk
  obtain ⟨hint,hbound⟩ := hbound r hr hrδ b k hk
  exact ⟨hint,hbound.trans (mul_le_mul_of_nonneg_left
    (pow_le_pow_left₀ (by positivity) (by linarith : 1+|b| ≤ 1+B) n) hC)⟩

/-- Sixth-power Markov for the literal varying-gap law. This is the retained
thirtieth-moment calculation with its actual measure changed to the gap law. -/
theorem sourceGapLaw_regularity_base_bound {L : ℝ} (hL : L ≠ 0)
    (r b k eps M : ℝ) (hr : 0 < r) (heps : 0 < eps)
    (hR : Integrable (fun ω => sourceGammaRadius L ω^30) (sourceGapLaw hL r b k))
    (hbound : (∫ ω, sourceGammaRadius L ω^30 ∂sourceGapLaw hL r b k) ≤ M) :
    (sourceGapLaw hL r b k).real (sourceRegularityBad L r eps) ≤ (M/eps^6)*r^6 := by
  let Q := sourceGapLaw hL r b k
  have hint : Integrable (fun ω => (r*sourceGammaRadius L ω^5)^6) Q := by
    simpa only [mul_pow, ← pow_mul] using hR.const_mul (r^6)
  have hnon : 0 ≤ᵐ[Q] (fun ω => (r*sourceGammaRadius L ω^5)^6) :=
    Eventually.of_forall (fun ω => by positivity)
  have hMarkov := mul_meas_ge_le_integral_of_nonneg hnon hint (eps^6)
  have hsub : sourceRegularityBad L r eps ⊆
      {ω | eps^6 ≤ (r*sourceGammaRadius L ω^5)^6} := by
    intro ω hω
    exact pow_le_pow_left₀ heps.le hω.le 6
  have hp : eps^6*Q.real (sourceRegularityBad L r eps) ≤ r^6*M := by
    calc
      _ ≤ eps^6*Q.real {ω | eps^6 ≤ (r*sourceGammaRadius L ω^5)^6} :=
        mul_le_mul_of_nonneg_left (measureReal_mono hsub) (pow_nonneg heps.le 6)
      _ ≤ ∫ ω, (r*sourceGammaRadius L ω^5)^6 ∂Q := hMarkov
      _ = r^6*∫ ω, sourceGammaRadius L ω^30 ∂Q := by
        simp only [mul_pow, ← pow_mul]
        rw [integral_const_mul]
      _ ≤ r^6*M := mul_le_mul_of_nonneg_left hbound (pow_nonneg hr.le 6)
  calc
    _ ≤ (r^6*M)/(eps^6) := (le_div_iff₀ (pow_pos heps 6)).2 (by simpa [mul_comm] using hp)
    _ = _ := by ring

/-- The physical square bound and sixth-power base tail give an r^5
unnormalized irregular-layer numerator by the existing event Cauchy-Schwarz. -/
theorem sourceGapLaw_regularity_numerator {L : ℝ} (hL : L ≠ 0)
    (B K eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) ∧
        (∫ ω in sourceRegularityBad L r eps, sourceSmoothWeight L r ω
          ∂sourceGapLaw hL r b k) ≤ N*r^5 := by
  obtain ⟨δR,hδR,hδR1,hmom⟩ := sourceGapLaw_compact_moments hL B K hB hK
  obtain ⟨M8,hM8,h8⟩ := hmom 8
  obtain ⟨M30,hM30,h30⟩ := hmom 30
  obtain ⟨δW,hδW,_hδW1,hW⟩ := sourceGapLaw_curvature_bounds hL
  let C := 100*M8
  let T := M30/eps^6
  have hC : 0 ≤ C := by dsimp [C]; positivity
  have hT : 0 ≤ T := div_nonneg hM30 (pow_nonneg heps.le 6)
  refine ⟨Real.sqrt C*Real.sqrt T,min δR δW,by positivity,
    lt_min hδR hδW,(min_le_left _ _).trans hδR1,?_⟩
  intro r hr hrδ b k hb hk
  have hrR : r < δR := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrW : r < δW := lt_of_lt_of_le hrδ (min_le_right _ _)
  obtain ⟨h8int,h8bound⟩ := h8 r hr hrR b k hb hk
  obtain ⟨h30int,h30bound⟩ := h30 r hr hrR b k hb hk
  have hsq : ∀ᵐ ω ∂sourceGapLaw hL r b k,
      sourceSmoothWeight L r ω^2 ≤ 100*r^4*sourceGammaRadius L ω^8 := by
    filter_upwards [hW r hr hrW b k] with ω hω
    have hh := pow_le_pow_left₀ (sourceSmoothWeight_nonneg L r ω) hω.2.2.1 2
    convert hh using 1 <;> ring
  have hmajor : Integrable (fun ω => 100*r^4*sourceGammaRadius L ω^8)
      (sourceGapLaw hL r b k) := h8int.const_mul _
  have hsqint : Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) := by
    apply hmajor.mono' ((sourceSmoothWeight_measurable hL r hr.ne').pow_const 2).aestronglyMeasurable
    filter_upwards [hsq] with ω hω
    simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)] using hω
  have hsqbound : (∫ ω, sourceSmoothWeight L r ω^2 ∂sourceGapLaw hL r b k) ≤ C*r^4 := by
    calc
      _ ≤ ∫ ω, 100*r^4*sourceGammaRadius L ω^8 ∂sourceGapLaw hL r b k :=
        integral_mono_ae hsqint hmajor hsq
      _ = 100*r^4*(∫ ω, sourceGammaRadius L ω^8 ∂sourceGapLaw hL r b k) := integral_const_mul _ _
      _ ≤ 100*r^4*M8 := mul_le_mul_of_nonneg_left h8bound (by positivity)
      _ = _ := by dsimp [C]; ring
  have hbase := sourceGapLaw_regularity_base_bound hL r b k eps M30 hr heps h30int h30bound
  have hsqrt : Real.sqrt ((sourceGapLaw hL r b k).real (sourceRegularityBad L r eps)) ≤
      Real.sqrt T*r^3 := by
    calc
      _ ≤ Real.sqrt (T*r^6) := Real.sqrt_le_sqrt hbase
      _ = _ := by
        rw [Real.sqrt_mul hT,show r^6 = (r^3)^2 by ring,Real.sqrt_sq (pow_nonneg hr.le 3)]
  have hLp : MemLp (sourceSmoothWeight L r) 2 (sourceGapLaw hL r b k) :=
    (memLp_two_iff_integrable_sq (sourceSmoothWeight_measurable hL r hr.ne').aestronglyMeasurable).mpr hsqint
  have hevent := p02_lm008_event_numerator (sourceGapLaw hL r b k) (sourceSmoothWeight L r)
    (sourceRegularityBad L r eps) hLp
    (Eventually.of_forall (sourceSmoothWeight_nonneg L r))
    (sourceRegularityBad_measurable L r eps) r C hC hsqbound
  refine ⟨hsqint,hevent.trans ?_⟩
  calc
    _ ≤ Real.sqrt C*r^2*(Real.sqrt T*r^3) :=
      mul_le_mul_of_nonneg_left hsqrt (by positivity)
    _ = _ := by ring
'''
# Adapt the retained generic-product pullback to literal gap targets; the
# scalar integration proof remains an invocation of the old generic theorem.
old=(packet/'SourceWeightedCurvatureBound.lean').read_text()
start=old.index('theorem sourceRegularCurvatureSlab_numerator_of_product')
end=old.index('/-- Composition with an r⁵ regular numerator.',start)
x=old[start:end]
x=x.replace('sourceRegularCurvatureSlab_numerator_of_product','sourceGapLaw_regular_numerator_of_product')
x=x.replace('(r b K eps A D T : ℝ) (hr : 0 < r) (hr1 : r ≤ 1)', '(r b k K eps A D T : ℝ) (hr : 0 < r)')
x=x.replace('sourceSmoothLaw hL r b','sourceGapLaw hL r b k')
x=x.replace('sourceConfluentPinsAt L r ω 4 = 0 ∧ sourceConfluentPinsAt L r ω 5 = 2','sourceConfluentPinsAt L r ω 4 = 0')
x=x.replace('''    · exact (measurableSet_eq_fun ((measurable_pi_apply 4).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const).inter
        (measurableSet_eq_fun ((measurable_pi_apply 5).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const)''','''    · exact measurableSet_eq_fun ((measurable_pi_apply 4).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const''')
x=x.replace('''    have hh := source_prescribed_pin_constraints_ae hL r b hG''','''    have hh : ∀ᵐ ω ∂sourceGapLaw hL r b k, pin ω := by
      have hs := I4SourceGapPinCurvature.sourceSmoothKernel_curvature_bounds_ae hL r hr
        (sourceGapPins r b k) hG (by simp [sourceGapPins]) (by simp [sourceGapPins])
      filter_upwards [hs] with ω hω
      exact ⟨by simpa [sourceGapPins] using congrFun hω.1 3,
        by simpa [sourceGapPins] using congrFun hω.1 4⟩''')
x=x.replace('''sourceSmoothWeight_curvature_bound hL r hr hr1 (Ψ p)
        hp.2.1.1 hp.2.1.2.1 hp.2.1.2.2''','''I4SourceGapPinCurvature.sourceSmoothWeight_curvature_bound hL r hr (Ψ p)
        hp.2.1.1 hp.2.1.2''')
s+='\n/-- Exact pullback at a literal gap target, with only the two zero-gradient pins. -/\n'+x
s+='\nend I4SourceGapWeightedNumerator\n'
p.write_text(s)
