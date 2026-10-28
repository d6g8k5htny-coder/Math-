import difflib,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean')
old=p.read_text(); ending='end I4SourceActualSaddleUppercuts\n'; assert old.endswith(ending)
new=old.removesuffix(ending)+'\n'+(BASE/'ProducerJoinSection.ACTUAL.lean.txt').read_text()+'\n'+ending
(BASE/'source-joins001.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='passed-whole-geometry002',tofile='whole-producer-joins001')))
p.write_text(new)
print('New producer joins/public assembly appended; existing qualified geometry reused unchanged.')
