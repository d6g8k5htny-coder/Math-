import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

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

if __name__ == '__main__': unittest.main()

class BlueprintTests(unittest.TestCase):
    def test_valid_link(self):
        self.assertEqual(gate.check_blueprint(r'\lean{X.a}', ['X.a']), ['X.a'])
    def test_wrong_link(self):
        with self.assertRaises(ValueError): gate.check_blueprint(r'\lean{X.b}', ['X.a'])
    def test_empty_link(self):
        with self.assertRaises(ValueError): gate.check_blueprint('', ['X.a'])
    def test_unsupported_leanok(self):
        with self.assertRaises(ValueError): gate.check_blueprint(r'\lean{X.a}\leanok', ['X.a'])
