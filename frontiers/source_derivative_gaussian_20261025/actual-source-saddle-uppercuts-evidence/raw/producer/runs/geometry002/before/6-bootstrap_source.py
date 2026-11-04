import json,pathlib,re
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
PROJECT=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
context=(BASE/'CONTEXT.md').read_text(); blocks=re.findall(r'```lean\n(.*?)```',context,re.S)
header=blocks[0]; common=blocks[1]
source=header+'\n'+common+'\nend I4SourceActualSaddleUppercuts\n'
path=PROJECT/'SourceActualSaddleUppercuts.lean'; path.write_text(source)
(BASE/'INITIAL_SOURCE_COMMON.lean.txt').write_text(source)
print(json.dumps({'created':str(path),'scope':'header and complete common private definitions only; no Lean check until COMPLETE helper geometry integrated'}))
