import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=BASE/'FixtureSection.INITIAL.lean.txt'; old=p.read_text(); new=old
new=new.replace('I4Source.scalarSeries','I4Foundation.scalarSeries')
new=new.replace('I4SourceFiniteTrig.scalarSeries_finitePairing','fixture_scalarSeries_finitePairing')
new=new.replace('SourceActualFoldTorus.torusProjection2L_isOpenMap','SourceActualFoldTorus.torusProjection2L_open')
new=new.replace('private theorem fixture_source (u : Fin 2 → ℝ) :', '''private theorem fixture_scalarSeries_finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    I4Foundation.scalarSeries a v = I4SourceFinitePinKernel.finitePairing a v := by
  classical
  unfold I4Foundation.scalarSeries I4SourceFinitePinKernel.finitePairing
  exact tsum_eq_sum fun m hm => by
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]

private theorem fixture_source (u : Fin 2 → ℝ) :''')
assert new!=old
(BASE/'FixtureSection.DRAFT001.lean.txt').write_text(old)
(BASE/'FixtureSection.ACTUAL.lean.txt').write_text(new)
(BASE/'fixture-draft001.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=p.name,tofile='FixtureSection.ACTUAL.lean.txt')))
p=BASE/'ProducerJoinSection.INITIAL.lean.txt'; old=p.read_text()
new=old.replace('fin_cases i <;> simpa using (show |(0 : ℝ)| < rho by simpa using hrho) <;> assumption',
'''fin_cases i
    · simpa using hrho
    · simpa using hs''')
(BASE/'ProducerJoinSection.ACTUAL.lean.txt').write_text(new)
(BASE/'producer-draft001.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=p.name,tofile='ProducerJoinSection.ACTUAL.lean.txt')))
print('Fresh producer drafts corrected from specific public declarations; no Lean execution and no foreign-private API used.')
