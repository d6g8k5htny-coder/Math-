#!/usr/bin/env python3
"""Exact finite controls and evidence-driver tests; not Lean proof execution."""
from fractions import Fraction as F
import importlib.util
import itertools
from pathlib import Path
import tempfile
import unittest

SIDE=Path(__file__).resolve().parent

class AtomIntegralTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SIDE/'check.py').is_file(), 'quantitative integral evidence helper absent')
        spec=importlib.util.spec_from_file_location('atom_check',SIDE/'check.py')
        self.c=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.c)

    def test_json_and_byte_identity(self):
        self.assertEqual(self.c.strict('{"n":1}'), {'n':1})
        for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":1.0}'):
            with self.assertRaises(ValueError): self.c.strict(raw)
        self.assertNotEqual(self.c.identity(b'x'),self.c.identity(b'x\n'))

    def test_negative_reason_not_generic_failure(self):
        for label in self.c.CONTROLS:
            good=f'/tmp/{label}.lean:4:2: error: unsolved goals\n⊢ False\n'
            self.assertEqual(self.c.negative(good,label,1),label)
            for bad in (good.replace('False','True'),good.replace(label,'Wrong'),good+'extra\n',''):
                with self.assertRaises(ValueError): self.c.negative(bad,label,1)
            for code in (0,2,True):
                with self.assertRaises(ValueError): self.c.negative(good,label,code)

    def test_exact_inventory_and_emitted_commands(self):
        self.assertEqual(len(self.c.TARGETS),6)
        good='\n'.join(n+' : True' for n in self.c.TARGETS)+'\n'
        self.assertEqual(self.c.types(good),list(self.c.TARGETS))
        for bad in (good+good,'warning: bad\n'+good,good.replace(self.c.TARGETS[0],'Other.first')):
            with self.assertRaises(ValueError):self.c.types(bad)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td);self.c.emit(out)
            self.assertEqual(set(p.name for p in out.iterdir()),
                             {'Audit.lean','Types.lean'}|{n+'.lean' for n in self.c.CONTROLS})
            self.assertEqual((out/'Audit.lean').read_text().count('#print axioms '),6)
            for name,statement in self.c.FALSE_STATEMENTS.items():
                self.assertIn('example : '+statement,(out/(name+'.lean')).read_text())

    def test_disjoint_event_integral_lower(self):
        weights=(F(1,6),F(1,3),F(1,2))
        for f in itertools.product((F(0),F(1),F(3)),repeat=3):
            for membership in itertools.product((0,1,2),repeat=3):
                S=[i for i in range(3) if membership[i]==1]
                T=[i for i in range(3) if membership[i]==2]
                a=min((f[i] for i in S),default=F(7))
                b=min((f[i] for i in T),default=F(9))
                lhs=sum(weights[i] for i in S)*a+sum(weights[i] for i in T)*b
                self.assertLessEqual(lhs,sum(weights[i]*f[i] for i in range(3)))

    def test_squared_radius_floors_and_schur(self):
        for a,b,p,q,extra in itertools.product((F(1),F(-1,2)),(F(2),F(-3)),
                (F(1,10),F(1,4)),(F(1,5),F(1,3)),(F(0),F(1,7),F(-4))):
            # Split every retained squared-radius mass equally over both signs.
            law=[(a,p/2),(-a,p/2),(b,q/2),(-b,q/2),(extra,1-p-q)]
            s,t=a*a,b*b
            m2,m4,m6=[sum(w*x**n for x,w in law) for n in (2,4,6)]
            s0=p*s+q*t;g0=p*q/(p+q)*(s-t)**2;d0=p*s*q*t/s0*(s-t)**2
            g=m4-m2*m2;delta=m6-m4*m4/m2
            self.assertGreaterEqual(m2,s0);self.assertGreaterEqual(g,g0);self.assertGreaterEqual(delta,d0)
            for u in (F(0),F(1,16),F(1,4)):
                x=m2*m2;D=(1-4*u)*x*m4+4*u*g*(m4+3*x)/4
                self.assertLessEqual(min(g0,2*s0*s0),x*g*(g+2*x)/D)
            if extra==0:self.assertEqual(delta,d0)

    def test_magnitude_mass_is_not_one_signed_atom(self):
        law=[(F(1),F(1,8)),(F(-1),F(1,8)),(F(2),F(1,8)),(F(-2),F(1,8)),(F(0),F(1,2))]
        self.assertEqual(sum(w for x,w in law if x*x==1),F(1,4))
        self.assertLess(sum(w for x,w in law if x==1),F(1,4))

    def test_necessary_boundaries_have_countermodels(self):
        # Coincident full events each mass1 cannot contribute twice to integral1.
        self.assertGreater(F(1)+F(1),F(1))
        # Non-probability measure delta_1+delta_2: unnormalised gap is negative.
        self.assertEqual(F(17)-F(5)**2,F(-8))
        # Half at0 and half on radius1: positive fourth gap, zero cubic residual.
        self.assertGreater(F(1,2)-F(1,2)**2,0)
        self.assertEqual(F(1,2)-F(1,2)**2/F(1,2),0)

    def test_workflow_preserves_history_and_execution(self):
        root=SIDE.parents[1]
        workflow=(root/self.c.WORKFLOW).read_text()
        self.assertIn('fetch-depth: 0',workflow)
        self.assertIn('persist-credentials: false',workflow)
        for path in self.c.CONSUMED:
            self.assertIn(path,workflow)
        shell=(SIDE/'replay.sh').read_text()
        for required in ('formal/gate.py --execute','-DwarningAsError=true','leanchecker --fresh D2AtomIntegral',
                         '-m unittest discover -s tests','-m unittest discover -s formal/tests','Contract.lean'):
            self.assertIn(required,shell)
        self.assertNotIn('continue-on-error',workflow)
        self.assertNotIn('linter.unnecessarySeqFocus false',shell)


class FinalRuntimeTests(unittest.TestCase):
    """The companion's runtime is re-observed after its own last Lean run; earlier core evidence does not cover it."""
    RELEASE='Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'

    def setUp(self):
        spec=importlib.util.spec_from_file_location('final_runtime_check_d2_atom_i',SIDE/'check.py')
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
        self.assertEqual(actual_tree, 'c506a5ff25864023a57369a5a9f0f55046283905')
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
                'manifest_sha256': '3cfc23e4b595a31a6a7e7e0bd964973c42e4c33c0f8008a38383f6cfb6210800',
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



if __name__=='__main__':unittest.main(verbosity=2)
