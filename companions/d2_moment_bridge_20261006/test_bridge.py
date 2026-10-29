"""Exact finite-law and protocol controls, not substitutes for arbitrary-law Lean proofs."""
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import re
import unittest
import subprocess
import tempfile
import hashlib
import os

SIDE = Path(__file__).resolve().parent
THEOREMS = '''residual_sq_expand residual_sq_integrable residual_integral_eq_delta delta_nonneg delta_eq_zero_iff_residual cubicResidual_eq_zero_iff delta_eq_zero_iff_support delta_pos_iff_not_support property_of_ae_of_atom moment_two_pos_of_atom delta_pos_of_two_atoms square_gap_integrable square_gap_integral fourth_gt_second_sq_of_two_atoms tau_pos_of_two_atoms zero_atom_counterexample'''.split()
DEFINITIONS = ['moment', 'cubicResidual']


def moments(law):
    return [sum(p*x**k for x,p in law) for k in (2,4,6)]


def laws():
    # Zero plus two possible radii, including absent and equal-radius atoms.
    for a,b,z,u,v in itertools.product((F(1,2),F(1),F(2)),(F(1),F(2),F(3)),range(3),range(3),range(3)):
        if u+v == 0:
            continue
        total=z+u+v
        yield [(F(0),F(z,total)),(a,F(u,2*total)),(-a,F(u,2*total)),
               (b,F(v,2*total)),(-b,F(v,2*total))]


class BridgeTests(unittest.TestCase):
    def test_source_exists_and_no_admission(self):
        self.assertTrue((SIDE/'D2MomentBridge.lean').is_file(), 'new Lean module missing')
        text=(SIDE/'D2MomentBridge.lean').read_text()
        code=re.sub(r'/\-.*?\-/', '', text, flags=re.S)
        for token in ('sorry','admit','axiom','unsafe','native_decide'):
            self.assertIsNone(re.search(r'\b'+token+r'\b',code), token)
        self.assertIn('import ResearchFormalCoreR1.D2Schur', text)
        self.assertIn('Integrable (fun w => X w ^ 6) μ', text)

    def test_exact_declared_inventory(self):
        self.assertTrue((SIDE/'SOURCE_FILES.json').is_file(), 'new inventory missing')
        meta=json.loads((SIDE/'SOURCE_FILES.json').read_text())
        text=(SIDE/'D2MomentBridge.lean').read_text()
        self.assertEqual(re.findall(r'^theorem (\w+)',text,re.M),THEOREMS)
        self.assertEqual(re.findall(r'^(?:noncomputable )?def (\w+)',text,re.M),DEFINITIONS)
        self.assertEqual(meta['theorems'],THEOREMS)
        self.assertEqual(meta['definitions'],DEFINITIONS)
        self.assertEqual(meta['scientific_effect'],'NONE')
        self.assertEqual(meta['core_tree'],'d3f585ccf71dd9f69938576db1053ea9c012157b')

    def test_residual_identity_and_exact_equality_class(self):
        count=0
        for law in laws():
            m2,m4,m6=moments(law); c=m4/m2; delta=m6-m4*m4/m2
            residual=sum(p*(x**3-c*x)**2 for x,p in law)
            self.assertEqual(delta,residual)
            self.assertGreaterEqual(delta,0)
            one_nonzero_radius=all(x==0 or x*x==c for x,p in law if p>0)
            self.assertEqual(delta==0,one_nonzero_radius)
            count+=1
        self.assertEqual(count,216)

    def test_two_nonzero_distinct_squared_atoms(self):
        strict=0
        for law in laws():
            xs=[x for x,p in law if p>0 and x!=0]
            if any(a*a!=b*b for a,b in itertools.combinations(xs,2)):
                m2,m4,m6=moments(law)
                self.assertGreater(m2,0)
                self.assertGreater(m4,m2*m2)
                self.assertGreater(m6-m4*m4/m2,0)
                for q in (F(0),F(1,16),F(1,8),F(1,4)):
                    delta=m6-m4*m4/m2
                    tau=(1-4*q)*delta+q*(delta+9*m2*(m4-m2*m2))
                    self.assertGreater(tau,0)
                strict+=1
        self.assertGreater(strict,0)

    def test_zero_atom_and_same_radius_countermodels(self):
        law=[(F(0),F(1,2)),(F(1),F(1,4)),(F(-1),F(1,4))]
        m2,m4,m6=moments(law)
        self.assertGreater(m4,m2*m2)
        self.assertEqual(m6-m4*m4/m2,0)
        a,b=F(1),F(-1)
        self.assertNotEqual(a,b)
        self.assertEqual(a*a,b*b)
        self.assertEqual(moments([(a,F(1,2)),(b,F(1,2))]),[1,1,1])

    def test_fourth_gap_needs_probability_normalization(self):
        # Mass2 is NOT probability: raw fourth gap can be negative.
        m2,m4,_=moments([(F(1),F(2))])
        self.assertLess(m4-m2*m2,0)
        for law in laws():
            m2,m4,_=moments(law)
            self.assertEqual(sum(p*(x*x-m2)**2 for x,p in law),m4-m2*m2)

    def test_residual_factorization(self):
        for x,c in itertools.product([F(i,3) for i in range(-9,10)], [F(i,4) for i in range(-8,9)]):
            self.assertEqual((x**3-c*x)**2,x**6-2*c*x**4+c*c*x*x)
            self.assertEqual(x**3-c*x==0,x==0 or x*x==c)

    def checker(self):
        self.assertTrue((SIDE/'check.py').is_file(),'evidence checker missing')
        spec=importlib.util.spec_from_file_location('moment_checker',SIDE/'check.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_negative_control_accepts_only_intended_false(self):
        m=self.checker()
        text='/tmp/evidence/RejectZeroAtom.lean:4:2: error: unsolved goals\n⊢ False\n'
        self.assertEqual(m.negative(text,'RejectZeroAtom',1),'RejectZeroAtom')
        for bad,status in [(text,0),(text,2),(text.replace('False','True'),1),
                           (text.replace('RejectZeroAtom','Other'),1),
                           (text+'error: unknown identifier\n',1),
                           ('Traceback: bad runtime\n',1),('error: unsolved goals\n',1)]:
            with self.subTest(bad=bad,status=status), self.assertRaises(ValueError):
                m.negative(bad,'RejectZeroAtom',status)
        with self.assertRaises(ValueError):m.negative(text,'Unknown',1)

    def test_final_command_does_not_hash_a_live_tee_output(self):
        # Execute the actual final shell invocation against a synthetic snapshot writer.
        # A live tee destination must not change after the receipt hashes that directory.
        command=next(line for line in (SIDE/'replay.sh').read_text().splitlines()
                     if 'check.py" finish' in line)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); out=root/'evidence'; out.mkdir()
            (root/'check.py').write_text("import pathlib,json,hashlib,time,sys\n"
                "out=pathlib.Path(sys.argv[-1]);time.sleep(0.05)\n"
                "r={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}\n"
                "(out/'receipt.json').write_text(json.dumps(r))\nprint('completed synthetic fixture')\n")
            run=subprocess.run(['bash','-c','set -euo pipefail\n'+command],
                capture_output=True,env={**os.environ,'SIDE':str(root),'OUT':str(out)})
            self.assertEqual(run.returncode,0,run.stderr)
            recorded=json.loads((out/'receipt.json').read_text())
            for name,digest in recorded.items():
                self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(),digest,
                                 'receipt hashed an output that was still being written')

    def test_type_inventory_missing_duplicate_unrecognized(self):
        m=self.checker(); names=['D2MomentBridge.a','D2MomentBridge.b']
        self.assertEqual(m.types('D2MomentBridge.a : True\nD2MomentBridge.b : False\n',names),names)
        for bad in ('D2MomentBridge.a : True\n','D2MomentBridge.a : True\nD2MomentBridge.a : True\n',
                    'error: crash\nD2MomentBridge.a : True\nD2MomentBridge.b : False\n'):
            with self.assertRaises(ValueError):m.types(bad,names)


class FinalRuntimeTests(unittest.TestCase):
    """The companion's runtime is re-observed after its own last Lean run; earlier core evidence does not cover it."""
    RELEASE='Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'

    def setUp(self):
        spec=importlib.util.spec_from_file_location('final_runtime_check_d2_moment',SIDE/'check.py')
        self.c=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.c)
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.out=Path(tmp.name)
        self.lock={'mathlib':'d'*40,'batteries':'e'*40}
        observed={'lean_version':self.RELEASE,'dependency_revisions':dict(self.lock),'dependency_worktrees':'CLEAN','manifest_sha256':'a'*64}
        self.core={'lean_version':self.RELEASE,'observations':{'preflight':dict(observed),'final':dict(observed)}}
        for name in ('toolchain.log','toolchain-final.log'):(self.out/name).write_text(self.RELEASE+'\n')
        self.packages({n:(h,'clean') for n,h in self.lock.items()})

    def packages(self,rows):
        (self.out/'packages-final.log').write_text(''.join(n+' '+h+' '+s+'\n' for n,(h,s) in rows.items()))

    def refuse(self,message):
        with self.assertRaisesRegex(ValueError,message):self.c.final_runtime(self.out,self.core,self.lock)

    def test_final_observation_equal_to_core_passes(self):
        self.assertEqual(self.c.final_runtime(self.out,self.core,self.lock)['dependency_worktrees'],'CLEAN')

    def test_same_semver_other_commit_or_build_refused(self):
        for text in (self.RELEASE.replace('5045d0056413266e57c625dcd7c365b10e377c52','0'*40),self.RELEASE.replace(', Release)',', Debug)')):
            with self.subTest(text=text):
                (self.out/'toolchain-final.log').write_text(text+'\n');self.refuse('differs from the core gate')

    def test_runtime_changed_after_core_gate_refused(self):
        other=self.RELEASE.replace('x86_64-unknown-linux-gnu','aarch64-unknown-linux-gnu')
        (self.out/'toolchain-final.log').write_text(other+'\n');self.refuse('differs from the core gate: toolchain-final.log')

    def test_dependency_moved_or_dirtied_after_core_gate_refused(self):
        self.packages({'mathlib':('f'*40,'clean'),'batteries':('e'*40,'clean')});self.refuse('HEAD differs')
        self.packages({'mathlib':('d'*40,'dirty'),'batteries':('e'*40,'clean')});self.refuse('not clean')
        self.packages({'mathlib':('d'*40,'clean')});self.refuse('set differs')

    def test_missing_final_observation_refused(self):
        (self.out/'packages-final.log').unlink();self.refuse('missing final dependency observation')
        self.packages({n:(h,'clean') for n,h in self.lock.items()});(self.out/'toolchain-final.log').unlink();self.refuse('toolchain-final.log')

    def test_core_receipt_without_equal_observations_refused(self):
        self.core.pop('observations');self.refuse('lacks equal preflight and final')

    def test_replay_observes_after_the_last_lean_run_and_finish_requires_it(self):
        replay=(SIDE/'replay.sh').read_text();inner=replay[:replay.index('\nINNER\n')]
        self.assertGreater(inner.index('toolchain-final.log'),inner.rindex('lean -DwarningAsError=true'))
        self.assertGreater(inner.index('packages-final.log'),inner.rindex('lean -DwarningAsError=true'))
        source=(SIDE/'check.py').read_text();body=source[source.index('def finish(out):'):source.index('def main(')]
        self.assertIn('final_runtime(out,',body)

def copy_formal_fixture(source, destination):
    """Copy formal inputs for the actual protocol fixture; never execute Lean."""
    import shutil
    return shutil.copytree(source, destination,
                           ignore=shutil.ignore_patterns('.lake', '__pycache__'))


class SourceFixtureIsolationTests(unittest.TestCase):
    """Ignored runtime state must not enter a source-only protocol fixture."""
    def test_ignored_runtime_and_python_cache_are_not_copied(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            source = base / 'input' / 'formal'
            source.mkdir(parents=True)
            (source / '.gitignore').write_text('.lake/\n__pycache__/\n')
            tracked = source / 'tracked-source.txt'
            tracked.write_bytes(b'exact tracked source\n')
            tracked.chmod(0o755)
            ignored = ('.lake/packages/runtime-cache', '__pycache__/runtime.pyc')
            for relative in ignored:
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'ignored runtime sentinel\n')
            subprocess.run(['git', '-C', str(source.parent), 'init', '-q'],
                           check=True, capture_output=True)
            subprocess.run(['git', '-C', str(source.parent), 'add', 'formal'],
                           check=True, capture_output=True)
            for relative in ignored:
                subprocess.run(['git', '-C', str(source.parent), 'check-ignore',
                                'formal/' + relative], check=True, capture_output=True)
            copied = base / 'copied-formal'
            copy_formal_fixture(source, copied)
            for relative in ignored:
                with self.subTest(relative=relative):
                    self.assertFalse((copied / relative).exists(),
                                     'ignored runtime cache entered the source fixture')
            self.assertEqual((copied / tracked.name).read_bytes(), tracked.read_bytes())
            self.assertEqual((copied / tracked.name).stat().st_mode & 0o777,
                             tracked.stat().st_mode & 0o777)

    def test_actual_tracked_formal_tree_bytes_and_modes_preserved(self):
        import subprocess
        original = SIDE.parents[1]
        def git(root, *args):
            return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            copied = base / 'formal'
            copy_formal_fixture(original / 'formal', copied)
            git(base, 'init', '-q')
            git(base, 'add', 'formal')
            tree = git(base, 'write-tree')
            self.assertEqual(git(base, 'rev-parse', tree + ':formal'),
                             git(original, 'rev-parse', 'HEAD:formal'))
            for relative in git(original, 'ls-files', '--', 'formal').splitlines():
                source = original / relative
                target = base / relative
                with self.subTest(path=relative):
                    self.assertEqual(target.read_bytes(), source.read_bytes())
                    self.assertEqual(target.stat().st_mode & 0o777,
                                     source.stat().st_mode & 0o777)


class CoreIdentityProtocolTests(unittest.TestCase):
    """Source/receipt protocol fixtures only; no Lean or finite-law execution."""
    def setUp(self):
        import shutil
        import subprocess
        from unittest import mock
        self._subprocess = subprocess
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        original = SIDE.parents[1]
        copy_formal_fixture(original / 'formal', self.root / 'formal')
        for package in ('d2_moment_bridge', 'd2_square_schur', 'd2_atom_integral'):
            relative = Path('companions') / (package + '_20261006')
            shutil.copytree(original / relative, self.root / relative)
            workflow = Path('.github/workflows') / (package.replace('_', '-') + '.yml')
            (self.root / workflow).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original / workflow, self.root / workflow)
        (self.root / 'tools').mkdir()
        shutil.copy2(original / 'tools/required_formal_check.py',
                     self.root / 'tools/required_formal_check.py')
        for args in (('init', '-q'), ('add', '.'),
                     ('-c', 'user.name=protocol-fixture',
                      '-c', 'user.email=protocol@example.invalid',
                      'commit', '-qm', 'copied exact source protocol fixture')):
            subprocess.run(['git', '-C', str(self.root), *args],
                           check=True, capture_output=True)
        self.head = subprocess.check_output(
            ['git', '-C', str(self.root), 'rev-parse', 'HEAD'], text=True).strip()
        actual_tree = subprocess.check_output(
            ['git', '-C', str(self.root), 'rev-parse', 'HEAD:formal'],
            text=True).strip()
        self.assertEqual(actual_tree, 'd3f585ccf71dd9f69938576db1053ea9c012157b')
        self.context = {'checked_commit': self.head}
        patch = mock.patch.dict('os.environ', {'GITHUB_ACTIONS': 'false'})
        patch.start()
        self.addCleanup(patch.stop)
        copied = self.root / 'companions' / SIDE.name / 'check.py'
        spec = importlib.util.spec_from_file_location('copied_d2_protocol', copied)
        self.c = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.c)

    def validator(self):
        function = getattr(self.c, 'validate_core_receipt', None)
        self.assertTrue(callable(function), 'production core receipt validator missing')
        return function

    def good_receipt(self):
        return {'checked_commit': self.head,
                'manifest_sha256': '7968411ca2dcc4cf63222c570380e3ad1542c47c7ff52d542f18e33849df2dc1',
                'formalization_status': 'kernel-checked'}

    def test_source_accepts_exact_reviewed_core_without_lean(self):
        try:
            current = self.c.source()
        except (ValueError, self._subprocess.CalledProcessError) as error:
            self.fail('reviewed frozen source cut must bind: ' + str(error))
        self.assertEqual(current['checked_commit'], self.head)
        self.assertIn('tools/required_formal_check.py', current['sources'])

    def test_actual_producer_to_receipt_validator(self):
        producer_path = self.root / 'formal/gate.py'
        spec = importlib.util.spec_from_file_location('copied_rf312_producer', producer_path)
        producer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(producer)
        _, digest = producer.source_check()
        self.assertEqual(digest, self.good_receipt()['manifest_sha256'])
        self.validator()(
            {'checked_commit': self.head, 'manifest_sha256': digest,
             'formalization_status': 'kernel-checked'}, self.context)

    def test_raw_digest_wrong_commit_and_non_kernel_receipts_refuse(self):
        validate = self.validator()
        raw = self.c.sha((self.root / 'formal/manifest.json').read_bytes())
        for key, value in (('manifest_sha256', raw),
                           ('checked_commit', '0' * 40),
                           ('formalization_status', 'source')):
            with self.subTest(key=key):
                bad = dict(self.good_receipt(), **{key: value})
                with self.assertRaises(ValueError):
                    validate(bad, self.context)

    def test_helper_drift_refuses_before_evaluating_changed_code(self):
        helper = self.root / 'tools/required_formal_check.py'
        helper.write_bytes(helper.read_bytes() +
                           b"\nraise RuntimeError('untrusted helper evaluated')\n")
        with self.assertRaisesRegex(ValueError, 'identity validator'):
            self.c.source()

    def test_helper_symlink_and_absence_refuse(self):
        helper = self.root / 'tools/required_formal_check.py'
        raw = helper.read_bytes()
        helper.unlink()
        with self.assertRaisesRegex(ValueError, 'identity validator'):
            self.c.source()
        outside = self.root / 'outside-validator.py'
        outside.write_bytes(raw)
        helper.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'identity validator'):
            self.c.source()

    def test_manifest_overlay_and_core_file_drift_refuse(self):
        changes = (('formal/manifest.json', b'\n'),
                   ('formal/manifest.overlay.json', b'\n'),
                   ('formal/ResearchFormalCoreR1/AlgebraV2.lean', b'\n'))
        for relative, suffix in changes:
            with self.subTest(path=relative):
                path = self.root / relative
                raw = path.read_bytes()
                path.write_bytes(raw + suffix)
                try:
                    with self.assertRaises((ValueError, self._subprocess.CalledProcessError)):
                        self.c.source()
                finally:
                    path.write_bytes(raw)

    def test_missing_or_unknown_overlay_regime_never_downgrades(self):
        validate = self.validator()
        overlay = self.root / 'formal/manifest.overlay.json'
        original = overlay.read_bytes()
        overlay.unlink()
        with self.assertRaises(ValueError):
            validate(self.good_receipt(), self.context)
        overlay.write_bytes(b'{"schema_version":2,"files":{}}')
        with self.assertRaises(ValueError):
            validate(self.good_receipt(), self.context)
        overlay.write_bytes(original)
        manifest = self.root / 'formal/manifest.json'
        raw = manifest.read_bytes()
        document = self.c.strict(raw)
        document.pop('source_identity')
        manifest.write_text(__import__('json').dumps(document))
        with self.assertRaises(ValueError):
            validate(self.good_receipt(), self.context)



if __name__=='__main__':
    unittest.main(verbosity=2)
