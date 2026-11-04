import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=BASE/'runner/record_run.py'; old=p.read_text()
new=old.replace("paths+=sorted(BASE.glob('*.lean'))", "paths+=sorted(BASE.glob('*.lean'))\npaths+=sorted(BASE.glob('*.lean.txt'))\npaths+=sorted(BASE.glob('*.patch'))")
assert old!=new
(BASE/'context/runner-001-to-002.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='INITIAL-record_run.py',tofile='record_run.002.py')))
p.write_text(new)
(BASE/'context/record_run.002.py').write_text(new)
print('Runner002 adds affected producer draft sections/full actual patches to automatic pre-run snapshots; initial runner immutable.')
