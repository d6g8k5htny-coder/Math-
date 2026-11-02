import json
from pathlib import Path
import re

root=Path('/workspace/Math-wholefield-20261025/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-smooth-conditional')
source=root/'SourceSmoothConditionalKernel.lean'
pattern=re.compile(r'^(?:@\[[^\]]+\]\s*)?(theorem|lemma|instance)\s+([A-Za-z0-9_]+)',re.M)
targets=[{'kind':m.group(1),'name':'I4SourceSmoothConditional.'+m.group(2),
          'line':source.read_text()[:m.start()].count('\n')+1}
         for m in pattern.finditer(source.read_text())]
(out/'targets.json').write_text(json.dumps(targets,indent=2)+'\n')
(out/'AxiomAudit.lean').write_text('import SourceSmoothConditionalKernel\n\n'+
    '\n'.join('#print axioms '+t['name'] for t in targets)+'\n')
print(f'{len(targets)} public theorem/lemma/instance targets')
