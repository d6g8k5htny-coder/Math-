import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); new=old
new=new.replace('abs_of_pos hu.2','abs_of_pos (show 0 < u 1 from hu.2)')
new=new.replace('abs_of_pos hv.2','abs_of_pos (show 0 < v 1 from hv.2)')
new=new.replace('''  · simpa [ug65_reflect] using
      (continuous_apply (1 : Fin 2) : Continuous (fun u : Point2 => u 1)).neg''','''  · change Continuous (fun u : Point2 => -u 1)
    exact (continuous_apply (1 : Fin 2)).neg''')
new=new.replace('linarith [hu.2]','linarith [show 0 < u 1 from hu.2]')
new=new.replace('linarith [hv.2]','linarith [show v 1 < 0 from hv.2]')
new=new.replace('exact lt_asymm hpos.2 hneg.2','exact lt_asymm (show 0 < u 1 from hpos.2) (show u 1 < 0 from hneg.2)')
assert new!=old
(BASE/'source-geometry002.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='geometry001-source',tofile='geometry002-source')))
p.write_text(new)
print('Actual geometry001 diagnostics fixed: explicit sign membership types and continuous reflection inference; whole helper original immutable.')
