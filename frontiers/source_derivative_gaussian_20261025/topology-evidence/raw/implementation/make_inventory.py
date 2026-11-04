from pathlib import Path
import json,re
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-smooth-topology');source=root/'SourceSmoothTopology.lean'
stack=[];targets=[]
for number,line in enumerate(source.read_text().splitlines(),1):
    ns=re.match(r'^namespace (\w+)',line);end=re.match(r'^end (\w+)',line)
    if ns:stack.append(ns.group(1))
    if end and stack and end.group(1)==stack[-1]:stack.pop()
    decl=re.match(r'^(?:@\[[^\]]+\]\s*)?(?:local\s+)?(theorem|lemma|instance|def|abbrev)\s+(?:\(priority\s*:=\s*\d+\)\s*)?(\w+)',line)
    if decl:targets.append({'kind':decl.group(1),'name':'.'.join(stack+[decl.group(2)]),'line':number})
(out/'targets.json').write_text(json.dumps(targets,indent=2)+'\n')
(out/'AxiomAudit.lean').write_text('import SourceSmoothTopology\n\n'+
 '\n'.join('#print axioms '+t['name'] for t in targets)+'\n')
print(f'{len(targets)} direct declaration targets, including local instances')
