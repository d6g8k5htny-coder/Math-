"""Exact finite probability controls; neither Lean nor continuum proof."""
from fractions import Fraction as F
import importlib.util, itertools, json
from pathlib import Path
import random, subprocess, sys, unittest
P=Path(__file__).with_name('tilt_check.py')
class TiltTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue(P.is_file(),'tilted-law implementation not supplied')
  s=importlib.util.spec_from_file_location('tilt',P); self.m=importlib.util.module_from_spec(s); s.loader.exec_module(self.m)
 def test_density_normalization(self):
  p=(F(1,4),F(1,4),F(1,2))
  for a in itertools.product((0,1,2),repeat=3):
   if not any(a): continue
   w=self.m.tilt(p,a)
   self.assertEqual(sum(w),1); self.assertTrue(all(v>=0 for v in w))
 def test_reference_tv_bound(self):
  p=(F(1,4),F(1,4),F(1,2))
  ws=[a for a in itertools.product((0,1,2),repeat=3) if any(a)]
  for a,b in itertools.product(ws,repeat=2):
   d=self.m.density_data(p,a,b)
   self.assertLessEqual(d['tv'],d['delta']/d['z0'])
 def test_all_latent_events(self):
  p=(F(1,3),F(2,3)); events=list(itertools.product((False,True),repeat=2))
  for a,b in itertools.product(((1,0),(0,1),(1,3),(2,2)),repeat=2):
   d=self.m.density_data(p,a,b)
   for event in events:
    gap=abs(sum(v for v,c in zip(d['alpha'],event) if c)-sum(v for v,c in zip(d['beta'],event) if c))
    self.assertLessEqual(gap,d['delta']/d['z0'])
 def test_clipped_lipschitz_observables(self):
  p=(F(1,4),F(1,4),F(1,2)); rng=random.Random(913)
  for _ in range(300):
   a=tuple(F(rng.randrange(1,5)) for _ in p); b=tuple(F(rng.randrange(1,5)) for _ in p)
   x=tuple(F(rng.randrange(-8,9),4) for _ in p); y=tuple(F(rng.randrange(-8,9),4) for _ in p)
   d=self.m.density_data(p,a,b)
   fun=lambda t:max(F(-1),min(F(1),t))
   gap=abs(sum(v*fun(t) for v,t in zip(d['alpha'],x))-sum(v*fun(t) for v,t in zip(d['beta'],y)))
   self.assertLessEqual(gap,self.m.bl_bound(p,a,b,x,y))
 def test_padded_event_both_directions(self):
  p=(F(1,4),F(3,4)); rng=random.Random(914)
  for _ in range(200):
   a=tuple(F(rng.randrange(1,4)) for _ in p); b=tuple(F(rng.randrange(1,4)) for _ in p)
   x=tuple(F(rng.randrange(-4,5),2) for _ in p); y=tuple(F(rng.randrange(-4,5),2) for _ in p)
   A={F(rng.randrange(-4,5),2)}; t=F(1,2)
   d=self.m.density_data(p,a,b); budget=self.m.padded_budget(p,a,b,x,y,t)
   for z,w,az,aw in ((x,y,d['alpha'],d['beta']),(y,x,d['beta'],d['alpha'])):
    lhs=sum(v for v,q in zip(az,z) if q in A)
    rhs=sum(v for v,q in zip(aw,w) if min(abs(q-u) for u in A)<=t)
    self.assertLessEqual(lhs,rhs+budget)
 def test_threshold_margin(self):
  p=(F(1,2),F(1,2)); rng=random.Random(915)
  for _ in range(150):
   a=(F(1),F(rng.randrange(1,4))); b=(F(rng.randrange(1,4)),F(1))
   x=tuple(F(rng.randrange(-8,9),4) for _ in p); y=tuple(F(rng.randrange(-8,9),4) for _ in p)
   d=self.m.density_data(p,a,b); t=F(1,2)
   gap=abs(sum(v for v,q in zip(d['alpha'],x) if q<=0)-sum(v for v,q in zip(d['beta'],y) if q<=0))
   margin=sum(v for v,q in zip(d['beta'],y) if abs(q)<=t)
   self.assertLessEqual(gap,margin+self.m.padded_budget(p,a,b,x,y,t))
 def test_movement_not_weight_error(self):
  p=(F(1),); a=b=(F(1),); x=(F(1,8),); y=(F(0),)
  d=self.m.density_data(p,a,b)
  self.assertEqual(d['delta'],0); self.assertEqual(self.m.bl_bound(p,a,b,x,y),F(1,8))
  self.assertEqual(self.m.discrete_tv(self.m.pushforward(p,a,x),self.m.pushforward(p,b,y)),1)
 def test_tilted_motion_not_original_probability(self):
  p=(F(1,16),F(15,16)); a=b=(F(16),F(0)); x=(F(1),F(0)); y=(F(0),F(0))
  self.assertEqual(self.m.padded_budget(p,a,b,x,y,F(1,2)),1)
 def test_gaussian_fourth_moment_bound(self):
  for mu in itertools.product((F(-1),F(0),F(2)),repeat=2):
   for lam in itertools.product((F(0),F(1,2),F(2)),repeat=2):
    m4,e2=self.m.gaussian_diagonal_fourth(mu,lam)
    self.assertLessEqual(m4,3*e2*e2)
  self.assertEqual(self.m.gaussian_diagonal_fourth((0,),(1,)),(F(3),F(1)))
 def test_zero_normalizers_and_invalid_inputs(self):
  for p,a in [((F(1),),(0,)),((F(1),),(-1,)),((F(1,2),),(1,)),((1,),(True,)),((1,),(1.0,))]:
   with self.assertRaises((ValueError,TypeError)): self.m.tilt(p,a)
  self.assertEqual(self.m.tilt((F(0),F(1)),(-2,1)),(F(0),F(1)))
 def test_cli_named_failures(self):
  expected={'M1':'NORMALIZED_MASS','M2':'ABSOLUTE_NOT_SIGNED_ERROR','M3':'MOVEMENT_TERM','M4':'TILTED_TAIL','M5':'BOUNDARY_MARGIN','M6':'GAUSSIAN_FOURTH','M7':'TV_NOT_BL'}
  for flags in (['-B','-S'],['-B','-O','-S']):
   r=subprocess.run([sys.executable,*flags,str(P)],capture_output=True,text=True,timeout=15)
   self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(r.stderr,''); self.assertGreater(json.loads(r.stdout)['controls'],0)
   for m,want in expected.items():
    r=subprocess.run([sys.executable,*flags,str(P),'--mutant',m],capture_output=True,text=True,timeout=15)
    self.assertEqual(r.returncode,1); self.assertEqual(r.stdout,''); self.assertEqual(r.stderr,'TILT_FAIL: '+want+'\n')
 def test_cli_invalid(self):
  for args in (['--mutant','M9'],['--invalid'],['--mutant']):
   r=subprocess.run([sys.executable,'-B','-S',str(P),*args],capture_output=True,text=True,timeout=15)
   self.assertEqual(r.returncode,2)
if __name__=='__main__': unittest.main()
