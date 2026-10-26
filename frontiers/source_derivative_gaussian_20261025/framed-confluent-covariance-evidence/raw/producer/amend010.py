from pathlib import Path
p=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceFramedConfluentCovariance.lean');s=p.read_text()
s=s.replace('.continuous_iteratedFDeriv\n    (by simp)','.continuous_iteratedFDeriv (m := k)\n    (by simp)')
s=s.replace("intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'\n    (f :=", "intervalIntegral.continuous_parametric_intervalIntegral_of_continuous' (μ := volume)\n    (f :=")
s=s.replace('Set.setOf_forall','Set.ofPred_forall')
a=s.index('  exact (compact_peano_continuous L m i).comp',s.index('private theorem compact_coefficient_continuous'))
b=s.index('\nprivate theorem compact_gram_continuous',a)
s=s[:a]+'''  have hz : Continuous (fun p : (E 2 × CompactFrame) × ℝ => coordinates 2 p.1.1) :=
    (coordinates 2).continuous.comp (continuous_fst.comp continuous_fst)
  have hu : Continuous (fun p : (E 2 × CompactFrame) × ℝ => p.1.2.val) :=
    continuous_subtype_val.comp (continuous_snd.comp continuous_fst)
  have he := (coordinates 2).continuous.comp ((continuous_apply (0 : Fin 2)).comp hu)
  have hn := (coordinates 2).continuous.comp ((continuous_apply (1 : Fin 2)).comp hu)
  exact (compact_peano_continuous L m i).comp
    ((hz.prodMk (he.prodMk hn)).prodMk continuous_snd)
''' +s[b:]
a=s.index('  have hu :=',s.index('private theorem compact_uniform_contact'))
b=s.index('  refine ⟨min (d / 2)',a)
s=s[:a]+'''  let f : ((E 2 × CompactFrame) × ℝ) → (Fin 7 × Fin 7 → ℝ) :=
    fun p ij => compact_gram L p ij.1 ij.2
  have hf : Continuous f := by
    apply continuous_pi
    intro ij
    exact (continuous_apply ij.2).comp ((continuous_apply ij.1).comp
      (compact_gram_continuous hL))
  have hu := (compact_parameters_isCompact L).uniformContinuousOn_of_continuous hf.continuousOn
  obtain ⟨d, hd, hdist⟩ := Metric.uniformContinuousOn_iff.mp hu eps heps
''' +s[b:]
a=s.index('  have hij :',s.index('private theorem compact_uniform_contact'))
b=s.index('\nprivate def compact_square',a)
s=s[:a]+'''  have hij : dist (f ((z,u),r) (i,j)) (f ((z,u),0) (i,j)) < eps :=
    lt_of_le_of_lt (dist_le_pi_dist (f ((z,u),r)) (f ((z,u),0)) (i,j)) he
  change |compact_gram L ((z,u),r) i j - compact_gram L ((z,u),0) i j| < eps
  simpa only [Real.dist_eq, f] using hij
''' +s[b:]
s=s.replace('''  have hg := (continuous_apply j).comp ((continuous_apply i).comp
    ((compact_gram_continuous hL).comp continuous_fst))
  exact (((continuous_apply i).comp continuous_snd).mul hg).mul
    ((continuous_apply j).comp continuous_snd)''','''  have hg : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) =>
      compact_gram L p.1 i j) :=
    (continuous_apply j).comp ((continuous_apply i).comp
      ((compact_gram_continuous hL).comp continuous_fst))
  have hvi : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) => p.2 i) :=
    (continuous_apply i).comp continuous_snd
  have hvj : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) => p.2 j) :=
    (continuous_apply j).comp continuous_snd
  exact (hvi.mul hg).mul hvj''')
s=s.replace('← Finset.sum_div, ← Finset.mul_sum, ← Finset.sum_mul, compact_square','← Finset.sum_div, ← Finset.mul_sum, compact_square')
s=s.replace('''    rw [Fin.sum_univ_castSucc]
    simpa only [Matrix.mulVec, dotProduct,
      w, Fin.snoc_castSucc, Fin.snoc_last, mul_one, A, b, hcast, Fin.last] using hi''','''    rw [Fin.sum_univ_castSucc]
    change (∑ j : Fin 6, G i.castSucc j.castSucc * x j) + G i.castSucc (Fin.last 6) * 1 = 0
    simpa only [Matrix.mulVec, dotProduct, mul_one, A, b, hcast] using hi''')
s=s.replace('''    have hupp : compact_quad G w ≤ M :=
      hM (mem_image_of_mem QT (show (p, w) ∈ KT from ⟨hp, hw⟩))''','''    have hupp : compact_quad G w ≤ M := by
      change QT (p,w) ≤ M
      exact hM (a := QT (p,w)) ⟨(p,w),⟨hp,hw⟩,rfl⟩''')
p.write_text(s)
