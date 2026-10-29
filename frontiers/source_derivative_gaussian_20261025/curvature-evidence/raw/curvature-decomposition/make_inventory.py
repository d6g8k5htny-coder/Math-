import json,re
from pathlib import Path
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-curvature-implementation')
source=root/'SourceCurvatureDecomposition.lean'
stack=[];targets=[]
for number,line in enumerate(source.read_text().splitlines(),1):
    namespace=re.match(r'^namespace (\w+)',line)
    end=re.match(r'^end (\w+)',line)
    if namespace:
        stack.append(namespace.group(1))
    if end and stack and end.group(1)==stack[-1]:
        stack.pop()
    declaration=re.match(r'^(?:@\[[^\]]+\]\s*)?(theorem|lemma|instance|def)\s+(\w+)',line)
    if declaration:
        targets.append({'kind':declaration.group(1),'name':'.'.join(stack+[declaration.group(2)]),'line':number})
(out/'targets.json').write_text(json.dumps(targets,indent=2)+'\n')
(out/'AxiomAudit.lean').write_text('import SourceCurvatureDecomposition\n\n'+
    '\n'.join('#print axioms '+target['name'] for target in targets)+'\n')
print(f'{len(targets)} public declaration targets')
