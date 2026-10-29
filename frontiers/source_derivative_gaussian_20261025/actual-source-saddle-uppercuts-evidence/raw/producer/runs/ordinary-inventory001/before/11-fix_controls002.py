import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=BASE/'SaddleUppercutsControls.lean'; old=p.read_text(); new=old
new=new.replace('''    ext i
    fin_cases i <;> simp <;> ring

private theorem boundaryPath_formula''','''    ext i
    fin_cases i
    · rfl
    · change (1-2*(1 : ℝ))*chosenRho/2 = -chosenRho/2
      ring

private theorem boundaryPath_formula''')
new=new.replace('''    convert boundaryTargetPoint_mem (1 : unitInterval) using 1 <;>
      congr 1 <;> ext i <;> fin_cases i <;> simp <;> ring''','''    have h := boundaryTargetPoint_mem (1 : unitInterval)
    have he : boundaryTargetPoint (1 : unitInterval) = (![0,-chosenRho/2] : Point2) := by
      ext i
      fin_cases i
      · rfl
      · change (1-2*(1 : ℝ))*chosenRho/2 = -chosenRho/2
        ring
    rwa [he] at h''')
assert old!=new
(BASE/'controls003.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='Controls002.lean',tofile='Controls003.lean')))
p.write_text(new)
print('Actual controls002 remaining lint fixed by explicit two-coordinate endpoint equalities; zero-path/counterproof mathematics unchanged.')
