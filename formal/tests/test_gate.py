import copy
import hashlib
import importlib.util
import json
import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gate', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(spec) if spec else None
if spec and spec.loader and (ROOT / 'gate.py').exists():
    spec.loader.exec_module(gate)

class GateTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(hasattr(gate, 'audit_axioms'), 'formal evidence gate not implemented')

    def test_standard_axioms(self):
        self.assertEqual(gate.audit_axioms("'X.a' depends on axioms: [propext, Classical.choice, Quot.sound]", ['X.a'])['X.a'], ['Classical.choice', 'Quot.sound', 'propext'])
    def test_axiom_free(self):
        self.assertEqual(gate.audit_axioms("'X.a' does not depend on any axioms", ['X.a']), {'X.a': []})
    def test_sorry(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.a' depends on axioms: [sorryAx]", ['X.a'])
    def test_custom(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.a' depends on axioms: [Other.hidden]", ['X.a'])
    def test_native(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.a' depends on axioms: [X.a._nativeDecide_1]", ['X.a'])
    def test_missing_target(self):
        with self.assertRaises(ValueError): gate.audit_axioms('', ['X.a'])
    def test_duplicate_target_output(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.a' does not depend on any axioms\n'X.a' does not depend on any axioms", ['X.a'])
    def test_duplicate_target_request(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.a' does not depend on any axioms", ['X.a','X.a'])
    def test_unexpected_target(self):
        with self.assertRaises(ValueError): gate.audit_axioms("'X.b' does not depend on any axioms", ['X.a'])
    def test_multiline(self):
        self.assertIn('X.a', gate.audit_axioms("'X.a' depends on axioms: [propext,\n Classical.choice]", ['X.a']))
    def test_noise_denied(self):
        with self.assertRaises(ValueError): gate.audit_axioms("error: bad\n'X.a' does not depend on any axioms", ['X.a'])
    def test_manifest_content(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'x').write_bytes(b'abc')
            self.assertEqual(gate.check_files(p, {'x':hashlib.sha256(b'abc').hexdigest()}), None)
    def test_manifest_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'x').write_bytes(b'bad')
            with self.assertRaises(ValueError): gate.check_files(p, {'x':hashlib.sha256(b'abc').hexdigest()})
    def test_manifest_missing(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): gate.check_files(Path(d), {'missing':'0'*64})
    def test_manifest_escape(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): gate.check_files(Path(d), {'../x':'0'*64})
    def test_manifest_absolute(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): gate.check_files(Path(d), {'/x':'0'*64})
    def test_manifest_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'x').write_bytes(b'a'); (p/'y').symlink_to(p/'x')
            with self.assertRaises(ValueError): gate.check_files(p, {'y':hashlib.sha256(b'a').hexdigest()})
    def test_manifest_empty(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): gate.check_files(Path(d), {})
    def review(self):
        return dict(disposition='ACCEPTED',manifest_sha256='a'*64,targets=['X.a'],scope_sha256='b'*64,
                    author={'provider':'OpenAI','family':'GPT','agent':'A'},reviewer={'provider':'Other','family':'Different','agent':'B'},
                    evidence={'repository':'o/r','commit':'c'*40,'path':'review.md','sha256':'d'*64})
    def test_review_valid(self):
        gate.check_alignment(self.review(), 'a'*64, ['X.a'], 'b'*64)
    def test_review_stale(self):
        with self.assertRaises(ValueError): gate.check_alignment(self.review(), 'e'*64, ['X.a'], 'b'*64)
    def test_review_self(self):
        r=self.review(); r['reviewer']=r['author'].copy()
        with self.assertRaises(ValueError): gate.check_alignment(r, 'a'*64, ['X.a'], 'b'*64)
    def test_review_same_provider(self):
        r=self.review(); r['reviewer']['provider']='OpenAI'
        with self.assertRaises(ValueError): gate.check_alignment(r, 'a'*64, ['X.a'], 'b'*64)
    def test_review_partial(self):
        with self.assertRaises(ValueError): gate.check_alignment(self.review(), 'a'*64, ['X.a','X.b'], 'b'*64)
    def test_review_bad_disposition(self):
        r=self.review(); r['disposition']='AMEND_REQUIRED'
        with self.assertRaises(ValueError): gate.check_alignment(r, 'a'*64, ['X.a'], 'b'*64)
    def test_review_bad_evidence(self):
        r=self.review(); r['evidence']['commit']='main'
        with self.assertRaises(ValueError): gate.check_alignment(r, 'a'*64, ['X.a'], 'b'*64)
    def test_review_changed_scope(self):
        with self.assertRaises(ValueError): gate.check_alignment(self.review(), 'a'*64, ['X.a'], 'c'*64)

class BlueprintTests(unittest.TestCase):
    def test_valid_link(self):
        self.assertEqual(gate.check_blueprint(r'\lean{X.a}', ['X.a']), ['X.a'])
    def test_wrong_link(self):
        with self.assertRaises(ValueError): gate.check_blueprint(r'\lean{X.b}', ['X.a'])
    def test_empty_link(self):
        with self.assertRaises(ValueError): gate.check_blueprint('', ['X.a'])
    def test_unsupported_leanok(self):
        with self.assertRaises(ValueError): gate.check_blueprint(r'\lean{X.a}\leanok', ['X.a'])

class SourceContractTests(unittest.TestCase):
    def fixture(self):
        import shutil
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = Path(self.tmp.name) / 'formal'
        shutil.copytree(ROOT, p, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
        self.previous = gate.ROOT; gate.ROOT = p
        self.addCleanup(lambda: setattr(gate, 'ROOT', self.previous))
        self.m = json.loads((p/'manifest.json').read_text())
        self.m['files'] = {q.relative_to(p).as_posix(): hashlib.sha256(q.read_bytes()).hexdigest() for q in p.rglob('*') if q.is_file() and q.name != 'manifest.json'}
        self.p = p
        return p
    def save(self):
        (self.p/'manifest.json').write_text(json.dumps(self.m))
    def test_source_baseline(self):
        self.fixture(); self.save(); gate.source_check()
    def test_unbound_gate_refused(self):
        self.fixture(); del self.m['files']['gate.py']; self.save()
        with self.assertRaises(ValueError): gate.source_check()
    def test_manifest_cannot_claim_kernel_status(self):
        self.fixture(); self.m['formalization_status']='kernel-checked'; self.save()
        with self.assertRaises(ValueError): gate.source_check()
    def test_root_declaration_cannot_evade_audit(self):
        p=self.fixture(); root=p/'ResearchFormalCoreR1.lean'
        root.write_text(root.read_text()+'theorem hidden : False := by sorry\n')
        self.m['files']['ResearchFormalCoreR1.lean']=hashlib.sha256(root.read_bytes()).hexdigest(); self.save()
        with self.assertRaises(ValueError): gate.source_check()
    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError): gate.load_json('{"a":1,"a":2}')
    def test_json_object(self):
        self.assertEqual(gate.load_json('{"a":1}'), {'a':1})

class RuntimeVersionTests(unittest.TestCase):
    # These are orchestration tests with synthetic external process results;
    # source validation, log writes, build deletion and receipts are real.
    RELEASE = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit ' + 'a' * 40 + ', Release)'

    def fixture(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / 'formal'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
        previous = gate.ROOT
        gate.ROOT = self.root
        self.addCleanup(lambda: setattr(gate, 'ROOT', previous))
        manifest_path = self.root / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files'] = {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in self.root.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        manifest_path.write_text(json.dumps(manifest))
        self.manifest, self.digest = gate.source_check()
        self.sentinel = self.root / '.lake/build/preserve-before-preflight'
        self.sentinel.parent.mkdir(parents=True)
        self.sentinel.write_text('old build')
        self.calls = []
        self.version_index = 0

    def execute_synthetic(self, versions, version_exit=0, mutate_source=False, wrong_dependency=False):
        def external_run(command, **kwargs):
            self.calls.append(command)
            if command == ['lake', 'env', 'lean', '--version']:
                text = versions[min(self.version_index, len(versions) - 1)] + '\n'
                self.version_index += 1
                return subprocess.CompletedProcess(command, version_exit, text)
            if command == ['lake', 'build'] and mutate_source:
                path = self.root / 'lake-manifest.json'
                path.write_bytes(path.read_bytes() + b'\n')
            label = Path(command[-1]).stem
            if label == 'Audit':
                text = '\n'.join("'" + n + "' does not depend on any axioms" for n in self.manifest['targets'])
            elif label in ('false_fold', 'false_power'):
                return subprocess.CompletedProcess(command, 1, 'unsolved goals\n')
            elif label in ('sorry', 'custom_imported', 'native'):
                forbidden = {'sorry': 'sorryAx', 'custom_imported': 'hiddenPremise', 'native': 'injected._nativeDecide_1'}[label]
                text = "'injected' depends on axioms: [" + forbidden + ']'
            else:
                text = ''
            return subprocess.CompletedProcess(command, 0, text)

        def external_git(command, **kwargs):
            if command == ['git', 'rev-parse', 'HEAD']:
                return 'b' * 40 + '\n'
            name = Path(command[2]).name
            revision = self.manifest['dependency_revisions'][name]
            return ('c' * 40 if wrong_dependency else revision) + '\n'

        with patch.object(gate.subprocess, 'run', side_effect=external_run), \
             patch.object(gate.subprocess, 'check_output', side_effect=external_git), \
             contextlib.redirect_stdout(io.StringIO()):
            return gate.execute(self.manifest, self.digest)

    def assert_no_receipt(self):
        self.assertFalse((self.root / '.lake/formal-evidence/receipt.json').exists())

    def test_complete_pinned_release_record(self):
        self.assertTrue(callable(getattr(gate, 'check_lean_version', None)), 'complete release validator missing')
        self.assertEqual(gate.check_lean_version(self.RELEASE + '\n'), self.RELEASE)

    def test_other_versions_and_incomplete_or_extra_records_refused(self):
        self.assertTrue(callable(getattr(gate, 'check_lean_version', None)), 'complete release validator missing')
        invalid = ['', 'unrelated version 4.34.1 text',
                   self.RELEASE.replace('4.34.1', '4.34.10'), self.RELEASE.replace('4.34.1', '4.34.100'),
                   self.RELEASE.replace('4.34.1', '4.34.1-rc1'), self.RELEASE.replace('4.34.1', '4.34.1-nightly'),
                   'Lean (version 4.34.1,', self.RELEASE.replace(', Release)', ', Debug)'),
                   'noise\n' + self.RELEASE, self.RELEASE + '\nnoise', self.RELEASE + '\n' + self.RELEASE]
        for text in invalid:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'unexpected running Lean version'):
                gate.check_lean_version(text)

    def test_invalid_preflight_preserves_build_and_runs_no_build(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, 'unexpected running Lean version'):
            self.execute_synthetic([self.RELEASE.replace('4.34.1', '4.34.10')])
        self.assertTrue(self.sentinel.exists(), 'preflight refusal deleted the old build')
        self.assertEqual(self.calls, [['lake', 'env', 'lean', '--version']])
        self.assert_no_receipt()

    def test_preflight_process_failure_preserves_build(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, 'unexpected process outcome'):
            self.execute_synthetic([self.RELEASE], version_exit=1)
        self.assertTrue(self.sentinel.exists(), 'failed preflight deleted the old build')
        self.assertEqual(self.calls, [['lake', 'env', 'lean', '--version']])
        self.assert_no_receipt()

    def test_success_checks_before_build_and_after_controls_and_binds_both_logs(self):
        self.fixture()
        receipt = self.execute_synthetic([self.RELEASE, self.RELEASE])
        self.assertEqual(self.calls[0], ['lake', 'env', 'lean', '--version'])
        self.assertEqual(self.calls[1], ['lake', 'build'])
        self.assertEqual(self.calls[-1], ['lake', 'env', 'lean', '--version'])
        self.assertEqual(self.version_index, 2)
        self.assertFalse(self.sentinel.exists())
        self.assertEqual(receipt['lean_version'], self.RELEASE)
        self.assertEqual(receipt['manifest_sha256'], self.digest)
        self.assertEqual(receipt['checked_commit'], 'b' * 40)  # synthetic Git result
        self.assertEqual(set(receipt['negative_controls']), {'false_fold', 'false_power', 'sorry', 'custom_imported', 'native'})
        out = self.root / '.lake/formal-evidence'
        self.assertEqual(set(receipt['logs']), {p.name for p in out.glob('*.log')})
        for name in ('version-preflight.log', 'version.log'):
            self.assertEqual(receipt['logs'][name], hashlib.sha256((out / name).read_bytes()).hexdigest())

    def test_version_change_after_execution_refuses_receipt(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, 'unexpected running Lean version'):
            self.execute_synthetic([self.RELEASE, self.RELEASE.replace('4.34.1', '4.34.10')])
        self.assertEqual(self.version_index, 2)
        self.assert_no_receipt()

    def test_source_change_during_build_still_refuses_receipt(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, 'source hash mismatch: lake-manifest.json'):
            self.execute_synthetic([self.RELEASE], mutate_source=True)
        self.assert_no_receipt()

    def test_installed_dependency_change_still_refuses_receipt(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, 'installed dependency HEAD differs from lock'):
            self.execute_synthetic([self.RELEASE], wrong_dependency=True)
        self.assert_no_receipt()

class SuccessorTests(unittest.TestCase):
    def test_only_documented_algebra_repairs(self):
        original=(ROOT/'originals/Algebra.lean.txt').read_text()
        expected=original.replace('def foldPotential', 'noncomputable def foldPotential').replace('  field_simp [hr]\n  ring\n', '  field_simp [hr]\n')
        self.assertEqual((ROOT/'ResearchFormalCoreR1/AlgebraV2.lean').read_text(), expected)
    def test_only_documented_probability_repair(self):
        original=(ROOT/'originals/ProbabilityCompanions.lean.txt').read_text()
        expected=original.replace('  field_simp [hr, hcZ]\n  ring\n', '  field_simp [hr, hcZ]\n')
        self.assertEqual((ROOT/'ResearchFormalCoreR1/ProbabilityCompanionsV2.lean').read_text(), expected)

if __name__ == '__main__': unittest.main()
