import difflib,json,pathlib,re
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
context=(BASE/'CONTEXT.md').read_text(); blocks=re.findall(r'```lean\n(.*?)```',context,re.S)
header='import SourceActualSaddleUppercuts\n'+blocks[0].replace('namespace I4SourceActualSaddleUppercuts','namespace ActualSaddleUppercutsControls')
common=blocks[1]
# Reuse the producer's FRESH65 fixture derivation template, not any64 private body,
# production source concatenation, foreign private API, or old Controls binary.
fixture=(BASE/'FixtureSection.ACTUAL.lean.txt').read_text()
fixture=fixture.replace('(coord 0).hasFDerivAt', '((coord 0).hasFDerivAt (x := X))')
fixture=fixture.replace('(coord 1).hasFDerivAt', '((coord 1).hasFDerivAt (x := X))')
fixture=fixture.replace('simpa [(point_coords 1 0).1] using this','simp [(point_coords 1 0).1] at this')
fixture=fixture.replace('simpa [(point_coords 0 1).2] using this','simp [(point_coords 0 1).2] at this')
fixture=fixture.replace('''    ext i
    fin_cases i <;> simp [fixturePoint, coord]''','''    have h0 : I4LifetimeField.coordinates 2 (fixturePoint 1 0) = (![1,0] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    have h1 : I4LifetimeField.coordinates 2 (fixturePoint 0 1) = (![0,1] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    rw [map_add, map_smul, map_smul, h0, h1]
    ext i
    fin_cases i <;> simp [coord]''')
fixture=fixture.replace('nlinarith [sq_pos_of_ne_zero ha, Real.pi_pos]',
 'nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]')
fixture=fixture.replace('simp [fixtureCenter, fixture_field]','norm_num [fixtureCenter, fixture_field]')
fixture=fixture.replace('isOpen_ball)', 'Metric.isOpen_ball)')
fixture=fixture.replace('ContinuousLinearMap.smul_apply, ','').replace('ContinuousLinearMap.smul_apply,\n    ','')
fixture=fixture.replace('simp [trigField, trigD, smul_eq_mul] <;> ring','simp [trigField, trigD, smul_eq_mul]; ring')
fixture=fixture.replace('  simp only [Fin.isValue, Fin.init_cons, Matrix.cons_val_zero, Matrix.cons_val_one]',
 '  change fderiv ℝ (fderiv ℝ trigField) X v w = _')
start=fixture.index('private theorem fixture_seam :'); end=fixture.index('\nprivate theorem fixture_consumer',start)
fixture=fixture[:start]+'''private theorem fixture_seam : fixtureCenter (-1) 0 = fixtureCenter 1 0 := by
  funext i
  fin_cases i
  · change ((-1 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ))
    have h : (((-1 : ℝ)+2 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ)) :=
      congrArg (fun t : ℝ => (t : AddCircle (2 : ℝ))) (by norm_num)
    exact (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm.trans h
  · rfl
''' +fixture[end:]
fixture=fixture.replace('actualSource_quotient_saddle_uniform_closed_uppercuts',
 'I4SourceActualSaddleUppercuts.actualSource_quotient_saddle_uniform_closed_uppercuts')
for name in ['positive_consumer','negative_consumer','seam_consumer']:
    fixture=fixture.replace('fixture_'+name,'ordinary_'+name)
joins=(BASE/'ProducerJoinSection.ACTUAL.lean.txt').read_text()
cutoff=joins[joins.index('private theorem cutoffEquality'):joins.index('\ntheorem actualSource_quotient_saddle_uniform_closed_uppercuts')]
cutoff=cutoff.replace('hball _ (by rw [abs_neg, abs_of_pos (by positivity)]; linarith)',
 'hball _ (by rw [abs_of_neg (show -rho/4 < 0 by linarith)]; linarith)')
boundary=(BASE/'OrdinaryBoundarySection.INITIAL.lean.txt').read_text()
boundary=boundary.replace('''  obtain ⟨rho, hrho, phi, hu, _⟩ := ordinary_positive_consumer
  exact ⟨rho, hrho, phi, hu⟩''','''  let rho := Classical.choose ordinary_positive_consumer
  have h := Classical.choose_spec ordinary_positive_consumer
  exact ⟨rho, h.1, Classical.choose h.2, (Classical.choose_spec h.2).1⟩''')
(BASE/'OrdinaryFixtureTemplate.FROZEN.lean.txt').write_text(fixture)
(BASE/'OrdinaryCutoffTemplate.FROZEN.lean.txt').write_text(cutoff)
output=header+'\n'+common+'\n'+cutoff+'\n'+fixture+'\n'+boundary+'\nend ActualSaddleUppercutsControls\n'
p=BASE/'SaddleUppercutsControls.lean'; p.write_text(output)
(BASE/'frozen/Controls.INITIAL.lean').write_text(output)
(BASE/'ORDINARY_ASSEMBLY_PROVENANCE.json').write_text(json.dumps({
 'author':'/root/actual_fold_chart_construct','no_ordinary_helper':True,
 'fresh65_templates':['FixtureSection.ACTUAL.lean.txt','ProducerJoinSection.ACTUAL.lean.txt','OrdinaryBoundarySection.INITIAL.lean.txt'],
 'method':'Separate ordinary source authored from own fresh65 templates plus actual diagnostic corrections, common literal frozen context, and independent structural zero path; no production source concatenation/private foreign API/old64 proof or Controls body/binary',
 'ordinary_scope':'All common/fixture/zero-path proofs are own ordinary declarations; qualify via new strict and separate ALLmoduleinventory/std3 before soleFalse; no ordinary named kernel',
 'source_dependency':'Only new public65 theorem and old PUBLIC finite-source/physical/Mathlib APIs'},indent=2)+'\n')
print(json.dumps({'ordinary_source':str(p),'lines':len(output.splitlines()),'status':'complete uncompiled ordinary source frozen before first ordinary execution'}))
