from pathlib import Path
p=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceFramedConfluentCovariance.lean')
s=p.read_text().replace('by simpa only [coordinates_apply] using h01','by simpa only [coordinates_apply, mul_comm] using h01')
s=s.replace('(show (k : ℕ∞) ≤ ⊤ from le_top)','(by simp)').replace('(show (⊤ : ℕ∞) ≠ 0 by simp)','(by simp)')
s=s.replace('    apply h2.comp\n    fun_prop','    exact h2.comp (show Continuous (fun p :\n      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>\n      (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1, ![p.1.1.2.1, p.1.1.2.1])) by fun_prop)',1)
s=s.replace('    apply h2.comp\n    fun_prop','    exact h2.comp (show Continuous (fun p :\n      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>\n      (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1, ![p.1.1.2.1, p.1.1.2.2])) by fun_prop)',1)
s=s.replace('      apply h3.comp\n      fun_prop\n    exact (by fun_prop).mul hh','      exact h3.comp (show Continuous (fun p :\n        (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>\n        (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1,\n          ![p.1.1.2.1, p.1.1.2.1, p.1.1.2.1])) by fun_prop)\n    exact (show Continuous (fun p :\n      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>\n      (1 / 4 : ℝ) - p.2 ^ 2) by fun_prop).mul hh')
s=s.replace('''  have hi22 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    h22 (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi2n := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    h2n (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi33 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    h33 (-1 / 2 : ℝ) (1 / 2 : ℝ)''','''  have hi22 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.1]) h22 (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi2n := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.2]) h2n (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi33 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      (1/4-t^2)*iteratedFDeriv ℝ 3 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.1,p.1.2.1]) h33 (-1 / 2 : ℝ) (1 / 2 : ℝ)''')
s=s.replace('    simp only [orthonormal_iff_ite]\n    change IsClosed','    simp only [orthonormal_iff_ite, Set.setOf_forall]\n    change IsClosed')
s=s.replace('    simpa using (abs_le.mpr ⟨hx.1 a, hx.2 a⟩)','    change |coordinates 2 ((coordinates 2).symm x) a| ≤ |L|/2\n    rw [(coordinates 2).apply_symm_apply x]\n    exact abs_le.mpr ⟨hx.1 a, hx.2 a⟩')
s=s.replace('''  apply (compact_peano_continuous L m i).comp
  fun_prop''','''  change Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
    peanoRows (modeCoefficient 2 L m) (coordinates 2 p.1.1)
      (coordinates 2 (p.1.2.val 0)) (coordinates 2 (p.1.2.val 1)) p.2 i)
  exact (compact_peano_continuous L m i).comp
    (show Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
      ((coordinates 2 p.1.1, coordinates 2 (p.1.2.val 0),
        coordinates 2 (p.1.2.val 1)),p.2)) by fun_prop)''')
s=s.replace('    (compact_gram_continuous hL)\n  obtain','    (compact_gram_continuous hL).continuousOn\n  obtain')
s=s.replace('    exact pow_eq_zero this','    exact sq_eq_zero_iff.mp this').replace('continuous_finset_sum','continuous_finsetSum')
s=s.replace('''      simp [compact_square, mul_add, add_div, Finset.mul_sum,
        Finset.sum_add_distrib, Finset.sum_div, Finset.sum_mul] <;> ring''','''      simp only [mul_add, add_div, Finset.sum_add_distrib]
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      simp only [← Finset.sum_div, ← Finset.mul_sum, ← Finset.sum_mul, compact_square]
      ring''')
s=s.replace('''      intro i j h
      apply Fin.ext
      exact congrArg Fin.val h)
  letI : Invertible A := hA.isUnit.invertible''','''      intro i j h
      exact Fin.ext (congrArg (fun t : Fin 7 => t.val) h))
  let : Invertible A := hA.isUnit.invertible''')
s=s.replace('← Matrix.mulVec_mulVec, Matrix.mul_inv_of_invertible','Matrix.mulVec_mulVec, Matrix.mul_inv_of_invertible')
s=s.replace('w, Fin.snoc_castSucc, Fin.snoc_last, mul_one, A, b, hcast] using hi','w, Fin.snoc_castSucc, Fin.snoc_last, mul_one, A, b, hcast, Fin.last] using hi')
s=s.replace('''  have hQ0 : Continuous Q0 := by
    apply (compact_quad_continuous hL).comp
    fun_prop''','''  have hQ0 : Continuous Q0 := by
    exact (compact_quad_continuous hL).comp
      (show Continuous (fun p : (E 2 × CompactFrame) × (Fin 7 → ℝ) =>
        ((p.1,(0:ℝ)),p.2)) by fun_prop)''')
p.write_text(s)
