import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); new=old.replace('ContinuousLinearMap.smul_apply,\n    ', '')
new=new.replace('simp [trigField, trigD, smul_eq_mul] <;> ring',
 'simp [trigField, trigD, smul_eq_mul]; ring')
assert old!=new
(BASE/'source-fixtures004.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='fixtures003-source',tofile='fixtures004-source')))
p.write_text(new)
print('Actual remaining fixture003 Werror lint only: remove deprecated unused simp alias and single-goal sequence focus.')
