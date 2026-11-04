from pathlib import Path
p=Path('/workspace/scratch/framed-confluent-covariance-construct/Controls.lean');s=p.read_text()
s=s.replace('coordinates_apply,directionX,directionY]', 'coordinates_apply,directionX]',1)
i=s.index('private theorem std1');s=s[:i]+s[i:].replace('coordinates_apply,directionX,directionY]','coordinates_apply,directionY]',1)
s=s.replace('toLp 2 ![(-4/5:ℝ),3/5]]','toLp 2 ![(-4/5:ℝ),3/5] ]')
s=s.replace('''  fin_cases i <;> fin_cases j <;>
    norm_num [ratFamily,EuclideanSpace.inner_eq_star_dotProduct,dotProduct,Fin.sum_univ_two]''','''  simp only [EuclideanSpace.inner_eq_star_dotProduct,star_trivial,dotProduct,Fin.sum_univ_two]
  fin_cases i <;> fin_cases j <;> norm_num [ratFamily]''')
s=s.replace('I4SourceConfluentLimits.peanoCubic,hm,hp,ht,one_mul]\n','I4SourceConfluentLimits.peanoCubic,hm,hp,ht,one_mul]\n  all_goals simp only [derivativeCoefficient,iteratedFDeriv_one_apply]\n  all_goals rfl\n',1)
s=s.replace('''  rw [sineBase,eval_scale]
  change''','''  rw [sineBase,eval_scale]
  simp only [eval,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,add_zero,termEval,one_mul]
  change''')
s=s.replace('I4SourceContact.sourceC','sourceC')
s=s.replace('simpa only [jet2,iteratedFDeriv_one_apply] using toSource_derivative','simpa only [finiteDirection,iteratedFDeriv_one_apply] using toSource_derivative')
# Add explicit actual same-sample fixed-axis join and contact order.
i=s.index('\nprivate def frameOf')
s=s[:i]+'''
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
''' +s[i:]
a=s.index('theorem signed_nonaxis_actual');b=s.index('\ntheorem reflected_nonaxis_law',a)
new=s[a:b].replace('theorem signed_nonaxis_actual','theorem reflected_nonaxis_actual').replace('midpoint ratFrame','midpoint (reflected ratFrame)').replace('ratFrame 0','(reflected ratFrame) 0').replace('ratFrame 1','(reflected ratFrame) 1')
s=s[:b]+'\n'+new+s[b:]
p.write_text(s)
