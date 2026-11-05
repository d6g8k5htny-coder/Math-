from pathlib import Path
p=Path('/workspace/scratch/framed-confluent-covariance-construct/Controls.lean');s=p.read_text()
s=s.replace('by ext i; fin_cases i <;> rfl','by\n  ext i\n  fin_cases i <;> simp [std,EuclideanSpace.basisFun_apply,EuclideanSpace.single,coordinates_apply,directionX,directionY]',2)
a=s.index('  rw [intervalIntegral.integral_sub',s.index('private theorem kernel_mass'));b=s.index('\nprivate theorem rows_zero',a)
s=s[:a]+'''  have hc : IntervalIntegrable (fun _ : ℝ => (1/4:ℝ)) volume (-1/2) (1/2) := intervalIntegrable_const
  have hp : IntervalIntegrable (fun t : ℝ => t^2) volume (-1/2) (1/2) :=
    (continuous_id.pow 2).intervalIntegrable _ _
  calc
    _ = (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4:ℝ)) - (∫ t in (-1/2:ℝ)..(1/2:ℝ),t^2) :=
      intervalIntegral.integral_sub hc hp
    _ = _ := by norm_num
''' +s[b:]
s=s.replace('''  · change 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f p ![e,e,e]) = _''','''  · change 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f p ![e,e,e]) =
      iteratedFDeriv ℝ 3 f p ![e,e,e]''')
s=s.replace('I4SourceConfluentLimits.weightedDerivativeIntegral','I4WeightedModeIntegrals.weightedDerivativeIntegral').replace('I4SourceConfluentLimits.modeF','I4ModeCurveChains.modeF').replace('I4SourceConfluentLimits.modeH','I4ModeCurveChains.modeH').replace('I4SourceConfluentLimits.axis_iteratedDeriv','I4ModeCurveChains.axis_iteratedDeriv')
a=s.index('  fin_cases i <;>',s.index('theorem standard_axis_coefficient_join'));b=s.index('\nprivate def frameOf',a)
s=s[:a]+'''  have hm : (0 : Fin 2 → ℝ)-(r/2) • directionX = ![-r/2,0] := by
    ext j; fin_cases j <;> simp [directionX] <;> ring
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
''' +s[b:]
s=s.replace('simp [reflectedFamily,R.inner_eq_one,R.inner_eq_zero','simp [reflectedFamily,R.inner_eq_zero')
s=s.replace('''  simpa [Fin.prod_univ_succ] using h
private theorem second_neg_both''','''  have he : (fun i : Fin 2 => ![(1:ℝ),-1] i • ![e,n] i) = ![e,-n] := by
    ext i; fin_cases i <;> simp
  rw [he] at h
  simpa [Fin.prod_univ_succ] using h
private theorem second_neg_both''')
s=s.replace('''  simpa [Fin.prod_univ_succ] using h

theorem reflected_coefficient_signs''','''  have he : (fun i : Fin 2 => (-1:ℝ) • ![n,n] i) = ![-n,-n] := by
    ext i; fin_cases i <;> simp
  rw [he] at h
  simpa [Fin.prod_univ_succ] using h

theorem reflected_coefficient_signs''')
s=s.replace('''  · simp only [rows,signs,map_neg]
    ring''','''  · change ((fderiv ℝ (modeCoefficient 2 L m) (coordinates 2 z-(r/2) • coordinates 2 (R 0))
      (-coordinates 2 (R 1))) + (fderiv ℝ (modeCoefficient 2 L m)
        (coordinates 2 z+(r/2) • coordinates 2 (R 0)) (-coordinates 2 (R 1))))/2 =
      (-1)*(((fderiv ℝ (modeCoefficient 2 L m) (coordinates 2 z-(r/2) • coordinates 2 (R 0))
        (coordinates 2 (R 1))) + (fderiv ℝ (modeCoefficient 2 L m)
          (coordinates 2 z+(r/2) • coordinates 2 (R 0)) (coordinates 2 (R 1))))/2)
    simp only [map_neg]
    ring''')
s=s.replace('''  · simpa only [rows,signs,one_mul] using
      second_neg_both''','''  · change iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z)
        ![-coordinates 2 (R 1),-coordinates 2 (R 1)] =
      1*iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (coordinates 2 z)
        ![coordinates 2 (R 1),coordinates 2 (R 1)]
    simpa only [one_mul] using second_neg_both''')
s=s.replace('((-1/3)/2)', '((-1/3:ℝ)/2)')
a=s.index('  simp [sineBase,',s.index('theorem sineBase_eval'));b=s.index('\ntheorem sineCube_eval',a)
s=s[:a]+'''  rw [sineBase,eval_scale]
  change Real.pi⁻¹ * Real.cos (phase 2 2 ![1,0] y-(Real.pi/2)) =
    Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi
  have hp : phase 2 2 ![1,0] y = Real.pi*y 0 := by
    simp [phase,I4SourceContact.sourceC,Fin.sum_univ_two]
  rw [hp,Real.cos_sub_pi_div_two]
  simp [div_eq_mul_inv,mul_comm]
''' +s[b:]
s=s.replace('''  simp only [localGerm,sub_zero,Pi.zero_apply]
  ring''','''  change (1/6:ℝ)*((Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi *
    (Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi))*(Real.sin (Real.pi*(y 0-(0:ℝ)))/Real.pi)) = _
  simp only [sub_zero]
  ring''',1)
s=s.replace('simpa only [mul_comm] using (((hasDerivAt_id t).const_mul c).sin).deriv','simpa only [id_eq,mul_one,mul_comm] using (((hasDerivAt_id t).const_mul c).sin).deriv')
s=s.replace('''    convert ((((hasDerivAt_id t).const_mul c).cos).const_mul c).deriv using 1 <;> ring''','''    have hh := ((((hasDerivAt_id t).const_mul c).cos).const_mul c).deriv
    simp only [id_eq,mul_one] at hh
    rw [hh]
    ring''')
s=s.replace('''    convert ((((hasDerivAt_id t).const_mul c).sin).const_mul (-(c^2))).deriv using 1 <;> ring''','''    have hh := ((((hasDerivAt_id t).const_mul c).sin).const_mul (-(c^2))).deriv
    simp only [id_eq,mul_one] at hh
    rw [hh]
    ring''')
s=s.replace('''    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionX) finiteDirection = _''','''    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionX) finiteDirection =
      fderiv ℝ (eval 2 sineCube) 0 directionX''')
s=s.replace('''    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionY) finiteDirection = _''','''    change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 2 m) 0 directionY) finiteDirection =
      fderiv ℝ (eval 2 sineCube) 0 directionY''')
s=s.replace('''    simpa only [map_zero,rows_zero] using (rfl :
      iteratedFDeriv ℝ 3 (modeCoefficient 2 2 m) 0 ![directionX,directionX,directionX] = _)''','''    rw [map_zero,rows_zero]
    rfl''')
p.write_text(s)
