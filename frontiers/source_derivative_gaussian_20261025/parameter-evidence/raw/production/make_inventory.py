from pathlib import Path
import json,re
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/smooth-parameter-production');source=root/'SourceSmoothParameterSpace.lean'
stack=[];targets=[];private=[]
for number,line in enumerate(source.read_text().splitlines(),1):
    ns=re.match(r'^namespace (\w+)',line);end=re.match(r'^end (\w+)',line)
    if ns:stack.append(ns.group(1))
    if end and stack and end.group(1)==stack[-1]:stack.pop()
    decl=re.match(r'^(?:@\[[^\]]+\]\s*)?(?:(local|private)\s+)?(theorem|lemma|instance|def|abbrev)\s+(?:\(priority\s*:=\s*\d+\)\s*)?(\w+)',line)
    if decl:
        item={'kind':decl.group(2),'name':'.'.join(stack+[decl.group(3)]),'line':number,'local_attribute':decl.group(1)=='local'}
        (private if decl.group(1)=='private' else targets).append(item)
(out/'targets.json').write_text(json.dumps(targets,indent=2)+'\n')
(out/'private_targets.json').write_text(json.dumps(private,indent=2)+'\n')
(out/'AxiomAudit.lean').write_text('import SourceSmoothParameterSpace\n\n'+'\n'.join('#print axioms '+t['name'] for t in targets)+'\n')
print(f'{len(targets)} public declarations including named local instances; {len(private)} private declarations')
