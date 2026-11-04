import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=BASE/'SaddleUppercutsControls.lean'; old=p.read_text(); new=old
new=new.replace('fin_cases i <;> simp [minusPoint] <;> ring','fin_cases i <;> simp <;> ring')
new=new.replace('congr 1 <;> ext i <;> fin_cases i <;> simp [boundaryTargetPoint] <;> ring',
 'congr 1 <;> ext i <;> fin_cases i <;> simp <;> ring')
new=new.replace('  simp only [Fin.isValue, Matrix.cons_val_one]\n  ring',
 '  change (chosenRho/2)*(-chosenRho/2) = -chosenRho^2/4\n  ring')
assert old!=new
(BASE/'controls002.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='Controls.INITIAL.lean',tofile='Controls002.lean')))
p.write_text(new)
print('Actual ordinary001 diagnostic fixes only: unused simp arguments and explicit finite-vector endpoint reduction before scalar ring arithmetic.')
