from pathlib import Path
import hashlib,json
base=Path('/workspace/scratch/actual-source-morse-join')
files=['lean-sard-route/TrigonometricMorseSard.lean','lean-sard-route/FiniteMorseTransfer.lean','lean-sard-route/GroupFourCoefficients.lean','measurable/ActualMorseEvent.lean','lean-sard-route/CoordinateMorse.lean','lean-sard-route/ActualFourModeShift.lean']
imports=[]; bodies=[]; lineage=[]
for f in files:
 p=base/f;t=p.read_text(); body=[]
 for l in t.splitlines():
  if l.startswith('import '):
   if l not in imports:imports.append(l)
  else:body.append(l)
 bodies.append('/-! Preserved author-side helper: '+f+' -/\n'+'\n'.join(body))
 lineage.append({'source':str(p),'sha256':hashlib.sha256(t.encode()).hexdigest()})
text='\n'.join(imports)+'\n\n/-! Actual source Morse incidence: the equal-dimensional Sard argument is joined\nto the literal four original Fourier coefficients and the unchanged smooth law.\nHelper lineage and all earlier verification remain attributed to their authors. -/\n\n'+'\n\n'.join(bodies)+'\n'
text=text.replace('    simp_all [fourMode_eq, fourFrequency10, fourFrequency01]','    simp_all [fourMode_eq, fourFrequency10, fourFrequency01]\n  all_goals have h := congrFun (congrArg Subtype.val hij) 0; norm_num at h')
Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceMorseIncidence.lean').write_text(text)
Path('/workspace/scratch/morse-incidence-production/helper-lineage.json').write_text(json.dumps(lineage,indent=2)+'\n')
