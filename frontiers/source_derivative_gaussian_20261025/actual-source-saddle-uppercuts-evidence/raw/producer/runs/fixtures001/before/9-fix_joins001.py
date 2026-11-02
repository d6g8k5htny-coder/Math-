import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); new=old
new=new.replace('· simpa only [hinv] using hus','· change sign (phi (phi.symm u) 1)\n      rw [hinv]\n      exact hus')
new=new.replace('phi.symm.continuousOn.mono fun u hu => by\n      rw [h.target_eq]',
 'phi.symm.continuousOn.mono fun u hu => by\n      change u ∈ phi.target\n      rw [h.target_eq]')
new=new.replace('exact Set.disjoint_left.mpr fun z hz hp => (not_lt_of_gt hz.2) hp.2',
 'exact Set.disjoint_left.mpr fun z hz hp => lt_asymm (show 0 < phi z 1 from hz.2) (show phi z 1 < 0 from hp.2)')
new=new.replace('hball _ (by rw [abs_neg, abs_of_pos (by positivity)]; linarith)',
 'hball _ (by rw [abs_of_neg (show -rho/4 < 0 by linarith)]; linarith)')
new=new.replace('''  intro O hO hqO
  exact actualUniformSaddleCuts''','''  dsimp only
  intro O hO hqO
  exact actualUniformSaddleCuts''')
assert old!=new
(BASE/'source-joins002.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='joins001-source',tofile='joins002-source')))
p.write_text(new)
print('Actual joins001 diagnostic fixes only: explicit set-membership/source target, abs sign and public let reduction.')
