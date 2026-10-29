import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); new=old
new=new.replace('(coord 0).hasFDerivAt', '((coord 0).hasFDerivAt (x := X))')
new=new.replace('(coord 1).hasFDerivAt', '((coord 1).hasFDerivAt (x := X))')
new=new.replace('simpa [(point_coords 1 0).1] using this','simp [(point_coords 1 0).1] at this')
new=new.replace('simpa [(point_coords 0 1).2] using this','simp [(point_coords 0 1).2] at this')
new=new.replace('''    ext i
    fin_cases i <;> simp [fixturePoint, coord]''','''    have h0 : I4LifetimeField.coordinates 2 (fixturePoint 1 0) = (![1,0] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    have h1 : I4LifetimeField.coordinates 2 (fixturePoint 0 1) = (![0,1] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    rw [map_add, map_smul, map_smul, h0, h1]
    ext i
    fin_cases i <;> simp [coord]''')
new=new.replace('nlinarith [sq_pos_of_ne_zero ha, Real.pi_pos]',
 'nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]')
new=new.replace('simp [fixtureCenter, fixture_field]','norm_num [fixtureCenter, fixture_field]')
new=new.replace('isOpen_ball)', 'Metric.isOpen_ball)')
start=new.index('private theorem fixture_seam :')
end=new.index('\nprivate theorem fixture_consumer',start)
new=new[:start]+'''private theorem fixture_seam : fixtureCenter (-1) 0 = fixtureCenter 1 0 := by
  funext i
  fin_cases i
  · change ((-1 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ))
    simpa using (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm
  · rfl
''' +new[end:]
assert old!=new
(BASE/'source-fixtures002.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='fixtures001-source',tofile='fixtures002-source')))
p.write_text(new)
print('Actual fixture001 diagnostics fixed: explicit derivative basepoint, coordinate-complement expansion, scalar product positivity, arithmetic/open/seam public bindings.')
