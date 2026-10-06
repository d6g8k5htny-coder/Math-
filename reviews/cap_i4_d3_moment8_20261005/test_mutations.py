"""Reject seven named wrong formulas through the actual finite-control subprocess."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
P=Path(__file__).resolve().parent
MUTATIONS={
 'low_constant':('return K + (1+K)*L','return (1+K)*L',{'test_low_hard_factor','test_low_integral_identity'}),
 'power_factor':('return 128*(J**8+L**8)','return 127*(J**8+L**8)',{'test_eighth_power_envelope'}),
 'tail_power':('return s**(8-q)*J**8','return s**(9-q)*J**8',{'test_tail_moment'}),
 'mixed_weight':('(5*K/2)*r**3*U**3*L**3','(0*K/2)*r**3*U**3*L**3',{'test_high_polynomial_weight'}),
 'radial_half':('F(comb(q,j),2)','F(comb(q,j),1)',{'test_gaussian_coefficients'}),
 'lower_factor':('return truncated_eighth(N)/12','return truncated_eighth(N)',{'test_countermodel_band_and_weight'}),
 'normalizer':('C*r**5/(cZ*r**2)','C*r**5/(cZ*r**5)',{'test_normalization_separate'})}
class MutationChecks(unittest.TestCase):
 def test_all_named_mutations(self):
  code=(P/'bounds.py').read_text(); tests=(P/'test_bounds.py').read_text()
  flags=['-B','-S']+(['-O'] if sys.flags.optimize else [])
  seen=[]
  for name,(old,new,wanted) in MUTATIONS.items():
   with self.subTest(mutant=name),tempfile.TemporaryDirectory() as d:
    self.assertEqual(code.count(old),1)
    p=Path(d);(p/'bounds.py').write_text(code.replace(old,new));(p/'test_bounds.py').write_text(tests)
    r=subprocess.run([sys.executable,*flags,'test_bounds.py'],cwd=p,capture_output=True,text=True,timeout=20)
    self.assertEqual(r.returncode,1,r.stderr)
    s=json.loads(r.stdout)
    self.assertEqual(s['tests'],12);self.assertIs(s['success'],False);self.assertEqual(s['errors'],[])
    self.assertEqual(set(s['failures']),wanted);self.assertEqual(len(s['failures']),len(wanted))
    self.assertIn('Ran 12 tests in ',r.stderr)
    seen.append({'mutant':name,'exit':r.returncode,'failures':sorted(wanted),'errors':[]})
  print(json.dumps({'scope':'finite altered-formula controls only','rejections':seen},sort_keys=True))
if __name__=='__main__':unittest.main(verbosity=2)
