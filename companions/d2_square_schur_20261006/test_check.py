import tempfile
#!/usr/bin/env python3
"""Finite diagnostics and exact evidence-parser controls, not Lean execution."""
from fractions import Fraction as F
import importlib.util
import itertools
from pathlib import Path
import unittest

SIDE = Path(__file__).resolve().parent

class Controls(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SIDE/'check.py').is_file(), 'missing evidence helper')
        spec = importlib.util.spec_from_file_location('d2_square_check', SIDE/'check.py')
        self.c = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.c)

    def test_strict_json(self):
        self.assertEqual(self.c.strict('{"ok":true,"n":1}'), {'ok':True,'n':1})
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1.0}', '{}{}'):
            with self.assertRaises(ValueError): self.c.strict(raw)

    def test_negative_controls_accept_exact_reason(self):
        for name in self.c.CONTROLS:
            msg = f'/tmp/{name}.lean:4:2: error: unsolved goals\n⊢ False\n'
            self.assertEqual(self.c.negative(msg,name,1), name)

    def test_negative_controls_reject_wrong_reason(self):
        name = self.c.CONTROLS[0]
        good = f'{name}.lean:4:2: error: unsolved goals\n⊢ False\n'
        bads = (good.replace('False','True'), good.replace(name,'Other'),
                good+'error: another problem\n', 'error: unknown identifier\n', '')
        for text in bads:
            with self.assertRaisesRegex(ValueError,'intended False'): self.c.negative(text,name,1)
        for code in (0,2,True):
            with self.assertRaisesRegex(ValueError,'exit'): self.c.negative(good,name,code)

    def test_type_inventory(self):
        names = self.c.TARGETS
        good = '\n'.join(n+' : True' for n in names)+'\n'
        self.assertEqual(self.c.types(good), list(names))
        for bad in (good+good, good.replace(names[0],'Other.first'),
                    'warning: unused\n'+good, good.replace(names[-1]+' : True\n','')):
            with self.assertRaises(ValueError): self.c.types(bad)

    def test_weighted_square(self):
        for u,v,a,b,c in itertools.product((F(1,3),F(2)),(F(1,4),F(3)),
                (F(-2),F(0),F(2)),(F(-1),F(3)),(F(-2),F(0),F(4))):
            lhs=u*(a-c)**2+v*(b-c)**2
            floor=u*v/(u+v)*(a-b)**2
            rhs=floor+(u+v)*(c-(u*a+v*b)/(u+v))**2
            self.assertEqual(lhs,rhs);self.assertLessEqual(floor,lhs)

    def test_schur_endpoints_and_input_floors(self):
        for s0,g0,sadd,gadd,q in itertools.product((F(1,3),F(1),F(3)),
                (F(1,4),F(2),F(5)),(F(0),F(2)),(F(0),F(3)),
                (F(0),F(1,16),F(1,4))):
            s,g=s0+sadd,g0+gadd;x=s*s
            a=x*(g+x);b=g*(g+4*x)/4;n=x*g*(g+2*x)
            d=(1-4*q)*a+4*q*b
            self.assertLessEqual(min(g,2*x),n/d)
            self.assertLessEqual(min(g0,2*s0*s0),n/d)

    def test_false_witnesses(self):
        # These are also executable Lean rejection contracts, not generalized facts.
        u,v,a,b,c=map(F,(-2,1,0,1,2))
        self.assertGreater(u*v/(u+v)*(a-b)**2,u*(a-c)**2+v*(b-c)**2)
        self.assertGreater(max(F(1),F(2)),F(3,2))
        self.assertGreater(min(F(1),F(2)),F(-3))

    def test_workflow_fetches_required_history(self):
        # The complete root suite resolves historical proof commits.
        text = (SIDE.parents[1]/'.github/workflows/d2-square-schur.yml').read_text()
        checkout = text.split('uses: actions/checkout@', 1)[1].split('\n      - ', 1)[0]
        settings = [line.strip() for line in checkout.splitlines()
                    if not line.lstrip().startswith('#')]
        self.assertIn('fetch-depth: 0', settings)
        self.assertIn('persist-credentials: false', settings)

    def test_identity_binds_every_byte(self):
        a=self.c.identity(b'abc\n');b=self.c.identity(b'abc')
        self.assertEqual(a['bytes'],4)
        self.assertNotEqual(a['sha256'],b['sha256'])
        self.assertNotEqual(a['git_blob'],b['git_blob'])


class FinalRuntimeTests(unittest.TestCase):
    """The companion's runtime is re-observed after its own last Lean run; earlier core evidence does not cover it."""
    RELEASE='Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'

    def setUp(self):
        spec=importlib.util.spec_from_file_location('final_runtime_check_d2_square',SIDE/'check.py')
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
        self.assertEqual(actual_tree, '522967e487401144a61f647d024431f726d8c78b')
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
                'manifest_sha256': '7303486433853c44c33b621cc995e8543b8760515c3c20ee6138ef3b187234f0',
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
