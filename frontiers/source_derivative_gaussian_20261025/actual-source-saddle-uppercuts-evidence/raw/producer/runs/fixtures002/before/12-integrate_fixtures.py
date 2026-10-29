import difflib,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); ending='end I4SourceActualSaddleUppercuts\n'; assert old.endswith(ending)
frozen=BASE/'frozen'; frozen.mkdir()
dst=frozen/'CORE.lean'; shutil.copyfile(p,dst)
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text()); known=cache[str(p)]; st=dst.stat()
cache[str(dst)]={**known,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact passed joins002 source identity reused','copied_from':str(p)}
(frozen/'CORE_BINDING.json').write_text(json.dumps({'source':cache[str(dst)],
 'qualification':str(BASE/'runs/joins002/receipt.json'),'scope':'complete generic geometry/transport/publicassembly/cutoffEquality; actual fixture tail not yet included'},indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
new=old.removesuffix(ending)+'\n'+(BASE/'FixtureSection.ACTUAL.lean.txt').read_text()+'\n'+ending
(BASE/'source-fixtures001.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='passed-complete-core',tofile='full-actual-fixtures001')))
p.write_text(new)
print('Passed complete CORE frozen via reused identity; fresh actual fixture tail added, uncovered new scope.')
