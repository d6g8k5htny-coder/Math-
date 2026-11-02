import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); new=old.replace('ContinuousLinearMap.smul_apply, ','')
new=new.replace('  simp only [Fin.isValue, Fin.init_cons, Matrix.cons_val_zero, Matrix.cons_val_one]',
 '  change fderiv ℝ (fderiv ℝ trigField) X v w = _')
new=new.replace('    simpa using (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm',
'''    have h : (((-1 : ℝ)+2 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ)) :=
      congrArg (fun t : ℝ => (t : AddCircle (2 : ℝ))) (by norm_num)
    exact (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm.trans h''')
assert old!=new
(BASE/'source-fixtures003.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='fixtures002-source',tofile='fixtures003-source')))
p.write_text(new)
print('Actual fixtures002 fixes: remove deprecated simp alias, use definitional finite derivative-array reduction, explicit period arithmetic equality.')
