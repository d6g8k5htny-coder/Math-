"""Exact tests for a finer execution of the existing rectangle enclosure.

Finite cross-checks support the stated interval proof; they are not Lean.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
PROGRAM = HERE / 'refine.py'


class RefinementTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PROGRAM.is_file(), 'refinement implementation is not supplied')
        spec = importlib.util.spec_from_file_location('refinement', PROGRAM)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_original_source_authenticated_before_execution(self):
        original = HERE.parent / 'lm006_wrong_sign_20261006_r20' / 'enclose.py'
        raw = original.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.m.PARENT_SHA256)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'changed.py'
            marker = Path(tmp) / 'executed'
            p.write_text("from pathlib import Path\nPath(%r).touch()\n" % str(marker))
            with self.assertRaisesRegex(ValueError, 'source identity'):
                self.m.load_source(p)
            self.assertFalse(marker.exists())
            p.write_bytes(raw + b'\n')
            with self.assertRaisesRegex(ValueError, 'source identity'):
                self.m.load_source(p)
            link = Path(tmp) / 'link.py'
            link.symlink_to(original)
            with self.assertRaises(OSError):
                self.m.load_source(link)

    def test_parent_exact_shared_grids(self):
        p = self.m.parent()
        for n in (2, 3, 5, 8, 16, 32):
            with self.subTest(n=n):
                old, new = p.enclosure(n), self.m.refinement(n)
                for key in ('gamma', 'coefficient', 'tail', 'parameters'):
                    self.assertEqual(new[key], old[key], key)
                self.assertEqual(new['evaluated_cells'] + new['zero_cells'], n*n)

    def test_pruning_excludes_exactly_zero_upper_cells(self):
        p = self.m.parent()
        for n in (2, 3, 5, 16, 31):
            for i in range(n):
                d1 = 24*(i+1)*n
                stop = self.m.row_stop(i,n)
                self.assertTrue(1 <= stop <= n)
                for k in range(n):
                    u0,u1 = 32*k*k,32*(k+1)*(k+1)
                    upper = p._jnum(d1,min(max(d1//2,u0),u1))
                    self.assertEqual(upper > 0, k < stop, (i,k,n))
        # Exact equality u0=d1 belongs to the omitted zero side.
        self.assertEqual(self.m.row_stop(2,4),3)

    def test_independent_unpruned_fraction_sum(self):
        p = self.m.parent(); n=8; v=p.parameters()['variance_D']
        area = F(96,n*n); lower=upper=F(0)
        for i in range(n):
            d0,d1 = F(12*i,n),F(12*(i+1),n)
            for k in range(n):
                b0,b1=F(4*k,n),F(4*(k+1),n)
                lo,hi=p.cell_bounds(d0,d1,b0*b0,b1*b1)
                lower += area*lo*p.density(d1,v)[0]*p.density(b1,(v[0]/4,v[1]/4))[0]
                upper += area*hi*p.density(d0,v)[1]*p.density(b0,(v[0]/4,v[1]/4))[1]
        r=self.m.refinement(n)
        self.assertEqual(r['gamma'], (lower,upper+r['tail']))

    def test_interior_maximum_is_retained(self):
        p=self.m.parent()
        self.assertEqual(p.cell_bounds(2,4,0,4)[1],F(8,3))
        self.assertEqual(p.j(4,0),0);self.assertEqual(p.j(4,4),0)
        n=32; seen=0
        for i in range(n):
            d1=24*(i+1)*n
            for k in range(self.m.row_stop(i,n)):
                u0,u1=32*k*k,32*(k+1)*(k+1)
                if u0<d1//2<u1:
                    peak=p._jnum(d1,d1//2)
                    self.assertGreater(peak,p._jnum(d1,u0))
                    self.assertGreater(peak,p._jnum(d1,u1));seen+=1
        self.assertGreater(seen,0)

    def test_tail_and_opposite_denominator_preserved(self):
        r=self.m.refinement(8);p=self.m.parent();v=r['parameters']['variance_D']
        tail=(v[1]*144+2*v[1]**2)*p.density(12,v)[1]/24
        tail+=2*v[1]**2*p.density(0,v)[1]/24*(v[1]/8)*p.density(4,(v[0]/4,v[1]/4))[1]
        self.assertGreater(tail,0);self.assertEqual(r['tail'],tail)
        par=r['parameters']
        self.assertEqual(r['coefficient'],(r['gamma'][0]*par['p0'][0]/par['z0'][1],r['gamma'][1]*par['p0'][1]/par['z0'][0]))
        self.assertGreater(r['coefficient'][1],r['gamma'][1]*par['p0'][1]/par['z0'][1])

    def test_strict_grid_and_row_inputs(self):
        for n in (True,2.0,F(2),1,8193,-1):
            with self.assertRaises((ValueError,TypeError)):
                self.m.refinement(n)
        self.assertEqual(self.m.validate_grid(8192),8192)
        for i,n in ((-1,8),(8,8),(True,8),(0,1)):
            with self.assertRaises((ValueError,TypeError)):
                self.m.row_stop(i,n)
        with self.assertRaises(ValueError):
            self.m.parent().enclosure(2049)  # Original cap was not edited.

    def test_frozen_source_and_result_unchanged(self):
        original = HERE.parent / 'lm006_wrong_sign_20261006_r20'
        expected={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in original.iterdir() if p.is_file()}
        self.m.refinement(16)
        self.assertEqual(expected,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in original.iterdir() if p.is_file()})
        old=json.loads((original/'RESULTS.json').read_text())
        self.assertEqual(old['grid'],2048)
        self.assertEqual(old['coefficient'],['0.001305365507','0.001338803452'])

    def test_cli_protocol_and_cross_mode_identity(self):
        results=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            done=subprocess.run([sys.executable,*flags,str(PROGRAM),'--grid','32'],capture_output=True,timeout=30)
            self.assertEqual(done.returncode,0,done.stderr)
            self.assertEqual(done.stderr,b'')
            data=json.loads(done.stdout)
            self.assertEqual(data['grid'],32)
            self.assertEqual(data['source_sha256'],self.m.PARENT_SHA256)
            self.assertEqual(data['evaluated_cells']+data['zero_cells'],32**2)
            self.assertFalse(data['independently_reviewed'])
            results.append(done.stdout)
            for args,code in ((['--grid','1'],1),(['--grid','8193'],1),(['--grid','bad'],2),(['--bogus'],2)):
                failed=subprocess.run([sys.executable,*flags,str(PROGRAM),*args],capture_output=True,timeout=30)
                self.assertEqual(failed.returncode,code,(args,failed.stderr))
                self.assertEqual(failed.stdout,b'')
                if code==1:self.assertTrue(failed.stderr.startswith(b'REFINEMENT_FAIL:'))
        self.assertEqual(*results)


if __name__=='__main__':
    unittest.main(verbosity=2)
