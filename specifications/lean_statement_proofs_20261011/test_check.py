#!/usr/bin/env python3
"""Positive and negative controls for the proof-packet checker (standard library only).

Synthetic controls build a disposable repository holding a miniature statement packet (two
modules, a register) and a miniature proof packet, so that every refusal is exercised in
isolation. Real-tree controls read the committed packets' pins and scan the modules present.
Lean is required only by the `LeanHelpers` class, guarded by `skipUnless(lake)`; it builds two
dependency-free fixture packages (a statement package and a proof package depending on it by
path), never Mathlib. No test here is evidence about any mathematical claim; scientific effect
NONE.
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lean_proof_check', HERE / 'check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

LOCK = {'version': '1.2.0', 'packagesDir': '.lake/packages', 'packages': [
    {'name': 'batteries', 'url': 'https://github.com/leanprover-community/batteries', 'type': 'git', 'subDir': None,
     'scope': 'leanprover-community', 'rev': 'f2effa3d803fda822b1f97b806c47cf2adfbcbc2', 'manifestFile': 'lake-manifest.json',
     'inputRev': 'main', 'inherited': True, 'configFile': 'lakefile.toml'},
    {'name': 'mathlib', 'url': 'https://github.com/leanprover-community/mathlib4.git', 'type': 'git', 'subDir': None,
     'scope': '', 'rev': check.MATHLIB_REV, 'manifestFile': 'lake-manifest.json', 'inputRev': check.MATHLIB_REV,
     'inherited': False, 'configFile': 'lakefile.lean'}],
    'name': check.STATEMENT_LOCK_NAME, 'lakeDir': '.lake', 'fixedToolchain': True}
STATEMENT_LAKEFILE = ('name = "' + check.STATEMENT_LOCK_NAME + '"\nversion = "0.1.0"\ndefaultTargets = ["Specifications"]\n\n[[require]]\n'
                      'name = "mathlib"\ngit = "https://github.com/leanprover-community/mathlib4.git"\nrev = "' + check.MATHLIB_REV
                      + '"\n\n[[lean_lib]]\nname = "Specifications"\n' + check.LEAN_OPTIONS_LINE + '\n')
PROOF_LAKEFILE = check.LAKEFILE  # pinned byte-exactly by check_lock
DOC = 'Scientific effect: NONE. Alignment: PENDING_INDEPENDENT_REVIEW.\n'

STATEMENT_DEMO = '''import Mathlib

namespace UniversalLaw.Spec.Demo

/-- A. -/
def A : Prop := (2 : ℕ) + 2 = 4

/-- B. -/
def B (n : ℕ) : Prop := n + 0 = n

/-- C. -/
def C {X : Type} [Fintype X] (s : Finset X) : Prop := s ⊆ s

/-- An interface. -/
structure Iface (d : ℕ) where
  x : ℕ

end UniversalLaw.Spec.Demo
'''
STATEMENT_OTHER = '''import Mathlib

namespace UniversalLaw.Spec.Other

/-- D. -/
def D : Prop := True

/-- A, again (ambiguity control). -/
def A : Prop := True

end UniversalLaw.Spec.Other
'''
PROOF_DEMO = '''import Specifications.Demo
import Specifications.Other

/-! Demo proof module. A module docstring may mention sorry, axiom and native_decide. -/

namespace UniversalLaw.Proofs.Demo

open UniversalLaw.Spec.Demo

namespace Aux

/-- A helper (not inventory). -/
theorem helper : True := trivial

end Aux

private theorem hiddenHelper : True := trivial

/-- An auxiliary definition. -/
def twice (n : ℕ) : ℕ := 2 * n

/-- Proves: `UniversalLaw.Spec.Demo.A` (register row `demo-claim`).
Method: norm_num.
Does not establish: the informal claim, its review or acceptance. -/
theorem a : UniversalLaw.Spec.Demo.A := by
  norm_num [UniversalLaw.Spec.Demo.A]

/-- Proves: `B` (register row `demo-claim`).
Method: rfl.
Does not establish: anything beyond the Prop. -/
@[simp]
theorem b (n : ℕ) : B n := rfl

section Params

variable {X : Type} [Fintype X]

/-- Proves: `UniversalLaw.Spec.Demo.C` (register row `demo-node`).
Method: subset_rfl.
Does not establish: anything beyond the Prop. -/
theorem c (s : Finset X) :
    UniversalLaw.Spec.Demo.C s :=
  Finset.Subset.refl s

end Params

open UniversalLaw.Spec.Other in
/-- Proves: `D` (register row `demo-node`).
Method: trivial.
Does not establish: anything beyond the Prop. -/
theorem d : D := trivial

end UniversalLaw.Proofs.Demo
'''


def statement(module, declaration, kind='def_prop', package=check.STATEMENT_PACKAGE, progress='specified'):
    return {'package': package, 'module': module, 'declaration': declaration, 'kind': kind, 'formal_progress': progress,
            'anchor': 'two and two make four', 'does_not_claim': 'the source theorem; review; acceptance'}


def register():
    return {
        'schema_version': 1, 'object': check.REGISTER_OBJECT, 'scientific_effect': 'NONE', 'scientific_status_authority': False,
        'alignment_status': 'PENDING_INDEPENDENT_REVIEW', 'meaning': 'inventory of formal statements; labels only',
        'toolchain': {'lean': check.TOOLCHAIN, 'lean_commit': check.LEAN_COMMIT, 'mathlib': check.MATHLIB_REV},
        'vocabulary': {'formal_progress': ['none', 'specified', 'proved', 'kernel-checked']}, 'sources': [],
        'claims': [
            {'claim_id': 'demo-claim', 'kind': 'landing_claim', 'title': 'Demo claim', 'layer0': {'source_id': None, 'heading': None},
             'disposition_transcribed': None, 'formal_progress': 'specified',
             'statements': [statement('Specifications/Demo.lean', 'UniversalLaw.Spec.Demo.A'),
                            statement('Specifications/Demo.lean', 'UniversalLaw.Spec.Demo.B'),
                            statement('Specifications/Demo.lean', 'UniversalLaw.Spec.Demo.Iface', 'structure'),
                            statement('UniversalLaw/Demo.lean', 'UniversalLaw.Demo.two_add', 'theorem', 'formal', 'proved')],
             'kernel_evidence': [], 'not_established': 'the claim itself', 'next_step': 'independent alignment review'},
            {'claim_id': 'demo-node', 'kind': 'graph_node', 'title': 'Demo node', 'layer0': {'source_id': None, 'heading': None},
             'disposition_transcribed': None, 'formal_progress': 'specified',
             'statements': [statement('Specifications/Demo.lean', 'UniversalLaw.Spec.Demo.A'),
                            statement('Specifications/Demo.lean', 'UniversalLaw.Spec.Demo.C'),
                            statement('Specifications/Other.lean', 'UniversalLaw.Spec.Other.D'),
                            statement('Specifications/Other.lean', 'UniversalLaw.Spec.Other.A')],
             'kernel_evidence': [], 'not_established': 'everything beyond the statement', 'next_step': 'none planned'}]}


class Fixture:
    """A disposable repository with a miniature statement packet and a miniature proof packet
    that passes the source check."""

    def __init__(self):
        self.tmp = tempfile.mkdtemp()
        self.repo = Path(self.tmp) / 'repo'
        self.packet = self.repo / check.PACKAGE
        self.statements = self.repo / check.STATEMENT_PACKAGE
        (self.packet / 'SpecificationProofs').mkdir(parents=True)
        (self.statements / 'Specifications').mkdir(parents=True)
        self.write(check.WORKFLOW, 'name: placeholder\n', repo=True)
        # statement packet
        self.write('lakefile.toml', STATEMENT_LAKEFILE, stmt=True)
        self.write('lean-toolchain', check.TOOLCHAIN + '\n', stmt=True)
        self.write('lake-manifest.json', json.dumps(LOCK, indent=2) + '\n', stmt=True)
        self.write('Specifications.lean', 'import Specifications.Demo\nimport Specifications.Other\n', stmt=True)
        self.write('Specifications/Demo.lean', STATEMENT_DEMO, stmt=True)
        self.write('Specifications/Other.lean', STATEMENT_OTHER, stmt=True)
        self.write('REGISTER.json', json.dumps(register(), indent=2, ensure_ascii=False) + '\n', stmt=True)
        # proof packet
        self.write('.gitignore', '.lake/\n__pycache__/\n')
        for name in ('check.py', 'test_check.py', 'replay.sh'):
            self.write(name, '# bound copy\n')
        self.write('README.md', '# Demo\n\n' + DOC)
        self.write('SCOPE.md', '# Scope\n\n' + DOC)
        self.write('lakefile.toml', PROOF_LAKEFILE)
        self.write('lean-toolchain', check.TOOLCHAIN + '\n')
        lock = dict(LOCK, name=check.LOCK_NAME, packages=LOCK['packages'] + [dict(check.PATH_DEPENDENCY)])
        self.write('lake-manifest.json', json.dumps(lock, indent=2) + '\n')
        self.write('SpecificationProofs.lean', 'import SpecificationProofs.Demo\n')
        self.write('SpecificationProofs/Demo.lean', PROOF_DEMO)

    def path(self, rel, repo=False, stmt=False):
        return (self.repo if repo else self.statements if stmt else self.packet) / rel

    def write(self, rel, text, repo=False, stmt=False):
        p = self.path(rel, repo, stmt)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')

    def read(self, rel, repo=False, stmt=False):
        return self.path(rel, repo, stmt).read_text(encoding='utf-8')

    def mutate(self, rel, old, new, repo=False, stmt=False, count=1):
        text = self.read(rel, repo, stmt)
        if old not in text:
            raise AssertionError(f'{old!r} not in {rel}')
        self.write(rel, text.replace(old, new, count), repo, stmt)

    def inject(self, line, rel='SpecificationProofs/Demo.lean'):
        """Insert column-0 text before the closing `end` of the proof module."""
        text = self.read(rel)
        head, _, tail = text.rpartition('\nend ')
        self.write(rel, head + '\n' + line + '\n\nend ' + tail)

    def register(self):
        return json.loads(self.read('REGISTER.json', stmt=True))

    def save_register(self, reg):
        self.write('REGISTER.json', json.dumps(reg, indent=2, ensure_ascii=False) + '\n', stmt=True)

    def run(self, allow_dirty=True):
        return check.source_check(self.packet, self.repo, allow_dirty)

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


DOCSTRING = '/-- Proves: `{prop}`.\nMethod: control.\nDoes not establish: anything. -/\n'


def thm(name, prop='UniversalLaw.Spec.Demo.A', binders='', type_text=None, body='by norm_num [UniversalLaw.Spec.Demo.A]', doc=True):
    head = DOCSTRING.format(prop=prop) if doc else ''
    return f'{head}theorem {name}{(" " + binders) if binders else ""} : {type_text or prop} := {body}'


class Base(unittest.TestCase):
    def setUp(self):
        # Fixture packets are synthetic: their worktree is not a CI checkout, so the CI-only
        # requirements that check.py applies when GITHUB_ACTIONS is set (GITHUB_SHA == HEAD,
        # repository name) must not apply to them. Identity.test_clean_and_dirty_worktrees re-enables
        # CI mode explicitly inside its own patch to test exactly those refusals.
        patcher = mock.patch.dict(os.environ)
        patcher.start()
        self.addCleanup(patcher.stop)
        for key in ('GITHUB_ACTIONS', 'GITHUB_SHA', 'GITHUB_REPOSITORY', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT'):
            os.environ.pop(key, None)
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)

    def assertRefused(self, fragment, allow_dirty=True):
        with self.assertRaises(ValueError) as ctx:
            self.f.run(allow_dirty)
        self.assertIn(fragment, str(ctx.exception))
        return str(ctx.exception)


class Positive(Base):
    def test_fixture_passes(self):
        info = self.f.run()
        self.assertEqual(info['formalization_status'], 'proved')
        self.assertEqual(info['alignment_status'], 'PENDING_INDEPENDENT_REVIEW')
        self.assertEqual((info['checked_commit'], info['worktree']), (None, 'UNVERIFIED'))
        self.assertEqual(info['theorem_count'], 4)
        self.assertEqual(info['covered_props'], ['UniversalLaw.Spec.Demo.A', 'UniversalLaw.Spec.Demo.B', 'UniversalLaw.Spec.Demo.C',
                                                 'UniversalLaw.Spec.Other.D'])
        self.assertEqual(info['duplicate_proofs'], [])
        self.assertEqual((info['aux_theorems'], info['auxiliary_definitions'], info['registered_props']), (2, 1, 5))
        self.assertEqual(info['modules'], ['SpecificationProofs/Demo.lean'])
        self.assertEqual(info['dependency_revisions']['mathlib'], check.MATHLIB_REV)
        by_name = {t['name'].rsplit('.', 1)[1]: t for t in info['theorems']}
        self.assertEqual(by_name['a']['claim_ids'], ['demo-claim', 'demo-node'])
        self.assertEqual(by_name['c']['claim_ids'], ['demo-node'])
        self.assertEqual((by_name['c']['binder_count'], by_name['c']['explicit_parameters']), (1, 1))
        self.assertEqual(by_name['b']['proves'], 'UniversalLaw.Spec.Demo.B')
        self.assertEqual(by_name['d']['proves'], 'UniversalLaw.Spec.Other.D')
        self.assertEqual(by_name['a']['doc']['method'], 'norm_num.')
        self.assertIn('Specifications/Demo.lean', info['statement_module_sha256'])
        self.assertEqual(len(info['register_sha256']), 64)

    def test_cli(self):
        cmd = [sys.executable, '-B', '-S', str(HERE / 'check.py'), '--root', str(self.f.packet), '--repo', str(self.f.repo), '--allow-dirty']
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('SOURCE_CHECK_PASS', proc.stdout)
        self.assertIn('"formalization_status": "proved"', proc.stdout)
        self.assertIn('WORKTREE_UNVERIFIED', proc.stderr)
        proc = subprocess.run(cmd + ['source'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = subprocess.run(cmd + ['execute'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, 'only `source` is a positional mode')
        self.f.inject(thm('s', body='sorry'))
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn('LEAN_PROOF_CHECK_FAIL', proc.stderr)
        self.assertIn('refused token', proc.stderr)
        self.assertNotIn('SOURCE_CHECK_PASS', proc.stdout)

    def test_sibling_proof_module_import_is_accepted(self):
        self.f.write('SpecificationProofs/Second.lean', 'import Specifications.Demo\n\nnamespace UniversalLaw.Proofs.Second\n\n'
                     'namespace Aux\ntheorem helper : True := trivial\nend Aux\n\nend UniversalLaw.Proofs.Second\n')
        self.f.write('SpecificationProofs.lean', 'import SpecificationProofs.Second\nimport SpecificationProofs.Demo\n')
        self.f.mutate('SpecificationProofs/Demo.lean', 'import Specifications.Demo\n', 'import Specifications.Demo\nimport SpecificationProofs.Second\n')
        info = self.f.run()
        self.assertEqual(info['modules'], ['SpecificationProofs/Second.lean', 'SpecificationProofs/Demo.lean'])
        self.assertEqual(info['theorem_count'], 4)

    def test_duplicate_proofs_are_reported_not_refused(self):
        self.f.write('SpecificationProofs/Second.lean', 'import Specifications.Demo\n\nnamespace UniversalLaw.Proofs.Second\n\n'
                     + thm('aAgain') + '\n\nend UniversalLaw.Proofs.Second\n')
        self.f.write('SpecificationProofs.lean', 'import SpecificationProofs.Second\nimport SpecificationProofs.Demo\n')
        info = self.f.run()
        self.assertEqual(info['modules'], ['SpecificationProofs/Second.lean', 'SpecificationProofs/Demo.lean'])
        self.assertEqual(info['theorem_count'], 5)
        self.assertEqual(info['duplicate_proofs'], ['UniversalLaw.Spec.Demo.A'])

    def test_comments_may_mention_refused_words(self):
        self.f.inject('-- theorem sorry axiom native_decide set_option maxHeartbeats 999999999 unsafe opaque')
        self.f.mutate('SpecificationProofs/Demo.lean', 'Method: rfl.', 'Method: rfl (the source says theorem; no sorry anywhere).')
        self.f.run()

    def test_relative_and_opened_resolution(self):
        self.f.inject(thm('aRel', type_text='Spec.Demo.A'))
        self.f.inject(thm('aShort', type_text='A', prop='UniversalLaw.Spec.Demo.A'))
        info = self.f.run()
        self.assertEqual(info['theorem_count'], 6)
        self.assertEqual(info['duplicate_proofs'], ['UniversalLaw.Spec.Demo.A'])

    def test_ambiguous_short_name_is_refused(self):
        self.f.mutate('SpecificationProofs/Demo.lean', 'open UniversalLaw.Spec.Demo\n', 'open UniversalLaw.Spec.Demo UniversalLaw.Spec.Other\n')
        self.f.inject(thm('aShort', type_text='A'))
        self.assertRefused('resolves to several registered Props')

    def test_aux_and_private_theorems_may_have_any_type(self):
        self.f.inject('theorem Aux.dotted (n : ℕ) : n = n := rfl\nprivate theorem priv2 : 1 = 1 := rfl\n'
                      'namespace Aux\nnamespace Inner\ntheorem deep : True := trivial\nend Inner\nend Aux\nprotected theorem Aux.prot : True := trivial')
        info = self.f.run()
        self.assertEqual(info['aux_theorems'], 6)
        self.assertEqual(info['theorem_count'], 4)

    def test_protected_theorem_is_inventory(self):
        self.f.inject(DOCSTRING.format(prop='UniversalLaw.Spec.Demo.A') + 'protected theorem prot : UniversalLaw.Spec.Demo.A := by norm_num [UniversalLaw.Spec.Demo.A]')
        self.assertEqual(self.f.run()['theorem_count'], 5)
        self.f.inject('protected theorem protBad : True := trivial')
        self.assertRefused('not a registered')

    def test_continuation_lines_and_attributes(self):
        self.f.inject('def f : ℕ → ℕ\n| 0 => 0\n| n + 1 => f n\ntermination_by n => n\n\n@[simp, norm_cast]\n' + thm('attr'))
        info = self.f.run()
        self.assertEqual((info['theorem_count'], info['auxiliary_definitions']), (5, 2))

    def test_set_option_justified(self):
        for text in ('set_option maxHeartbeats 800000 in -- heavy norm_num\n' + thm('h1'),
                     '-- heavy norm_num\nset_option maxHeartbeats 800000 in\n' + thm('h2'),
                     '/- heavy\nnorm_num -/\nset_option maxHeartbeats 800000 in\n' + thm('h3'),
                     'set_option maxHeartbeats 400000 in\n' + thm('h4'),
                     'set_option linter.unusedVariables false in\n' + thm('h5')):
            with self.subTest(text=text[:40]):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(text)
                info = f.run()
                self.assertEqual(info['theorem_count'], 5)
                self.assertEqual(len(info['set_options']['SpecificationProofs/Demo.lean']), 1)


class Identity(Base):
    def test_requires_git_without_allow_dirty(self):
        self.assertRefused('not a git repository', allow_dirty=False)

    @unittest.skipUnless(shutil.which('git'), 'git not available')
    def test_clean_and_dirty_worktrees(self):
        def g(*args):
            return subprocess.run(['git', '-C', str(self.f.repo), '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false',
                                   *args], capture_output=True, text=True, check=True).stdout
        g('init', '-q')
        g('add', '-A')
        g('commit', '-q', '-m', 'fixture')
        info = self.f.run(allow_dirty=False)
        self.assertEqual(info['worktree'], 'CLEAN')
        self.assertRegex(info['checked_commit'], '^[0-9a-f]{40}$')
        self.f.mutate('SpecificationProofs/Demo.lean', 'Method: rfl.', 'Method: rfl!')
        self.assertRefused('uncommitted or untracked', allow_dirty=False)
        g('checkout', '--', '.')
        self.f.mutate('Specifications/Demo.lean', '/-- A. -/', '/-- A! -/', stmt=True)
        self.assertRefused('uncommitted or untracked', allow_dirty=False)
        g('checkout', '--', '.')
        self.f.write('SpecificationProofs/Extra.lean', 'untracked\n')
        self.assertRefused('uncommitted or untracked', allow_dirty=False)
        self.f.path('SpecificationProofs/Extra.lean').unlink()
        self.f.run(allow_dirty=False)
        os.environ['GITHUB_ACTIONS'] = 'true'
        os.environ['GITHUB_SHA'] = '0' * 40
        os.environ['GITHUB_REPOSITORY'] = check.REPOSITORY
        self.assertRefused('GITHUB_SHA', allow_dirty=False)
        os.environ['GITHUB_SHA'] = info['checked_commit']
        os.environ['GITHUB_REPOSITORY'] = 'someone/fork'
        self.assertRefused('GITHUB_REPOSITORY', allow_dirty=False)
        os.environ['GITHUB_REPOSITORY'] = check.REPOSITORY
        self.f.run(allow_dirty=False)


class Lexical(Base):
    def test_refused_tokens(self):
        cases = {'sorry': thm('t', body='sorry'), 'admit': thm('t', body='by admit'), 'axiom': 'axiom hidden : False',
                 'native_decide': thm('t', body='by native_decide'), 'ofReduceBool': thm('t', body='Lean.ofReduceBool _ _ rfl'),
                 'unsafe': 'unsafe def u : ℕ := 0', 'opaque': 'opaque o : ℕ', 'partial': 'partial def p (n : ℕ) : ℕ := p n',
                 'implemented_by': '@[implemented_by twice] def i (n : ℕ) : ℕ := n', 'extern': '@[extern "x"] def e : ℕ := 0',
                 'skipKernelTC': 'set_option debug.skipKernelTC true in\n' + thm('t'), 'byAsSorry': 'set_option debug.byAsSorry true in\n' + thm('t'),
                 'macro': 'macro "tt" : term => `(True)', 'notation': 'notation "⊤⊤" => True', 'syntax': 'syntax "tt" : term',
                 'elab': 'elab "tt" : term => pure (mkConst ``True)', 'run_cmd': 'run_cmd pure ()', 'initialize': 'initialize x : ℕ ← pure 0',
                 'export': 'export Nat (succ)', 'alias': 'alias succ := Nat.succ', 'irreducible_def': 'irreducible_def x : ℕ := 0',
                 'include': 'variable (h : False)\ninclude h\n' + thm('t', body='h.elim'), '_root_': 'theorem _root_.Escaped : True := trivial',
                 'trustCompiler': thm('t', body='Lean.trustCompiler'), 'sorryAx': thm('t', body='sorryAx _ false'),
                 'native': thm('t', body='by decide +native'), 'native (config)': thm('t', body='by decide (config := { native := true })')}
        for token, line in cases.items():
            with self.subTest(token=token):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(line)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn('refused token', str(ctx.exception))
                self.assertIn(token.split()[0], str(ctx.exception))

    def test_refused_token_detection_unit(self):
        self.assertEqual(check.refused_tokens('theorem t : False := by sorry\n'), ['sorry'])
        self.assertEqual(check.refused_tokens('exact sorryAx _ false\n'), ['sorryAx'])
        self.assertEqual(check.refused_tokens('by decide +native\n'), ['native'])
        self.assertEqual(check.refused_tokens('by decide +kernel\n'), [])
        self.assertEqual(check.refused_tokens('def partialSups : ℕ := 0\n'), [])
        self.assertEqual(check.refused_tokens('def x := Foo.sorry\n'), ['sorry'])
        self.assertEqual(check.refused_tokens('exact Classical.axiomOfChoice\n'), [])

    def test_hash_commands(self):
        for line in ('#check Nat', '#eval 1', '#exit', '  #print axioms Nat'):
            with self.subTest(line=line):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(line)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn('`#` commands', str(ctx.exception))
        self.f.inject('def arr : Array ℕ := #[1, 2]')
        self.f.run()

    def test_keywords_off_column_0(self):
        for line in ('  theorem hidden : True := trivial', 'open Classical in theorem hidden : True := trivial',
                     'set_option maxHeartbeats 1000 in theorem hidden : True := trivial', thm('two') + ' theorem hidden : True := trivial',
                     ' def hidden : ℕ := 0', ' namespace Hidden\n end Hidden', ' private theorem hidden : True := trivial',
                     ' section\n end', ' example : True := trivial', '  variable (h : False)', ' abbrev x : ℕ := 0',
                     ' instance : Inhabited ℕ := ⟨0⟩', ' structure S where\n   n : ℕ', ' inductive I | a'):
            with self.subTest(line=line):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(line)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn('off column 0', str(ctx.exception))

    def test_tactic_block_open_and_set_option_are_fine(self):
        self.f.inject(thm('t', body='by\n  open Classical in\n  set_option maxHeartbeats 1000 in\n  norm_num [UniversalLaw.Spec.Demo.A]'))
        self.assertEqual(self.f.run()['theorem_count'], 5)

    def test_instance_attribute_in_brackets_is_fine(self):
        self.f.inject('attribute [local instance] Classical.propDecidable')
        self.f.run()

    def test_column0_commands_not_allowed(self):
        for line, fragment in (('mutual\nend', 'column-0 command'), ('local notation "x" => True', 'refused token'),
                               ('scoped instance : Inhabited ℕ := ⟨0⟩', 'off column 0'), ('class K where\n  n : ℕ', 'column-0 command'),
                               ('| 0 => 0', None), ('universe u', None)):
            with self.subTest(line=line):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(line)
                if fragment is None:
                    f.run()
                else:
                    with self.assertRaises(ValueError) as ctx:
                        f.run()
                    self.assertIn(fragment, str(ctx.exception))

    def test_set_option_refusals(self):
        for line, fragment in (('set_option maxHeartbeats 800000 in\n' + thm('h'), 'justifying comment'),
                               ('set_option maxHeartbeats 400001 in\n' + thm('h'), 'justifying comment'),
                               ('set_option maxHeartbeats 0 in\n' + thm('h'), 'justifying comment'),
                               ('set_option maxHeartbeats 800000\n' + thm('h'), 'justifying comment'),
                               (thm('h', body='by\n  set_option maxHeartbeats 800000 in\n  norm_num [UniversalLaw.Spec.Demo.A]'), 'justifying comment'),
                               ('set_option autoImplicit true in\n' + thm('h'), 'refused option'),
                               ('set_option relaxedAutoImplicit true in\n' + thm('h'), 'refused option'),
                               ('set_option debug.terminalTacticsAsSorry true in\n' + thm('h'), 'refused option'),
                               ('set_option bootstrap.genMatcherCode false in\n' + thm('h'), 'refused option'),
                               ('set_option compiler.extract_closed false in\n' + thm('h'), 'refused option'),
                               ('set_option maxHeartbeats n in\n' + thm('h'), 'literal number')):
            with self.subTest(line=line[:60]):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(line)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn(fragment, str(ctx.exception))

    def test_open_in_must_end_its_line(self):
        self.f.inject('open Classical in def x : ℕ := 0')
        self.assertRefused('off column 0')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject('set_option maxHeartbeats 1000 in def x : ℕ := 0')
        self.assertRefused('off column 0')

    def test_variable_in_refused(self):
        self.f.inject('variable (n : ℕ) in\n' + thm('v'))
        self.assertRefused('`variable … in`')

    def test_string_literals_do_not_hide_tokens(self):
        self.f.inject('def opener : String := "/-"\ntheorem smuggled : True := sorry\ndef closer : String := "-/"')
        msg = self.assertRefused('refused token')
        self.assertIn('sorry', msg)

    def test_unterminated_comment(self):
        self.f.inject('/- never closed')
        self.assertRefused('unterminated block comment')


class Shape(Base):
    """Every way a non-aux theorem can fail the theorem-shape rule at source."""

    def test_unregistered_and_structure_types(self):
        for type_text in ('True', 'UniversalLaw.Spec.Demo.Iface 3', '(2 : ℕ) + 2 = 4', 'UniversalLaw.Spec.Demo.Ghost'):
            with self.subTest(type_text=type_text):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(thm('t', type_text=type_text, body='trivial'))
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertRegex(str(ctx.exception), 'not a registered|must be a registered Prop constant|bare parameter names')

    def test_quantifiers_implications_and_expressions(self):
        for type_text, fragment in (('UniversalLaw.Spec.Demo.A → UniversalLaw.Spec.Demo.A', 'must be a registered Prop constant applied'),
                                    ('∀ n : ℕ, UniversalLaw.Spec.Demo.B n', 'must be a registered Prop constant applied'),
                                    ('UniversalLaw.Spec.Demo.B (n + 1)', 'bare parameter names'),
                                    ('UniversalLaw.Spec.Demo.A ∧ UniversalLaw.Spec.Demo.A', 'must be a registered Prop constant applied'),
                                    ('¬ UniversalLaw.Spec.Demo.A', 'must be a registered Prop constant applied'),
                                    ('@UniversalLaw.Spec.Demo.B n', 'must be a registered Prop constant applied'),
                                    ('(UniversalLaw.Spec.Demo.A)', 'bare parameter names')):
            with self.subTest(type_text=type_text):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(thm('t', binders='(n : ℕ)', type_text=type_text, body='by trivial'))
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn(fragment, str(ctx.exception))

    def test_smuggled_explicit_hypothesis(self):
        self.f.inject(thm('t', binders='(h : False)', body='h.elim'))
        self.assertIn("'h'", self.assertRefused('not passed to'))
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject(thm('t', binders='(n : ℕ) (m : ℕ)', prop='UniversalLaw.Spec.Demo.B', type_text='UniversalLaw.Spec.Demo.B n', body='rfl'))
        self.assertIn("'m'", self.assertRefused('not passed to'))

    def test_implicit_hypothesis_passes_source_and_is_left_to_lean(self):
        """An implicit extra binder is invisible to the lexical rule (implicit binders may be
        passed implicitly); the environment audit refuses it (LeanHelpers)."""
        self.f.inject(thm('t', binders='{h : False}', body='h.elim'))
        self.assertEqual(self.f.run()['theorem_count'], 5)

    def test_argument_not_a_parameter(self):
        self.f.inject(thm('t', binders='(n : ℕ)', prop='UniversalLaw.Spec.Demo.B', type_text='UniversalLaw.Spec.Demo.B m', body='rfl'))
        self.assertRefused('is not a parameter of the theorem')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject(thm('t', binders='(n : ℕ)', prop='UniversalLaw.Spec.Demo.B', type_text='UniversalLaw.Spec.Demo.B n n', body='rfl'))
        self.assertRefused('repeated argument')

    def test_section_variables_are_parameters(self):
        self.f.inject('section S\nvariable (k : ℕ)\n' + thm('t', prop='UniversalLaw.Spec.Demo.B', type_text='UniversalLaw.Spec.Demo.B k', body='rfl') + '\nend S')
        self.assertEqual(self.f.run()['theorem_count'], 5)

    def test_missing_type_and_docstring(self):
        self.f.inject('/-- Proves: `A`.\nMethod: x.\nDoes not establish: y. -/\ntheorem t := trivial')
        self.assertRefused('without an explicit result type')
        for text, fragment in ((thm('t', doc=False), 'no docstring'),
                               ('/-- No labels. -/\n' + thm('t', doc=False), 'docstring must carry exactly one `Proves:`'),
                               ('/-- Proves: `A`.\nMethod: x. -/\n' + thm('t', doc=False), '`Does not establish:`'),
                               ('/-- Proves: `A`.\nProves: `A`.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'exactly one `Proves:`'),
                               ('/-- Proves: `B`.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'must name the registered Prop'),
                               ('/-- Proves: `AA`.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'as a whole token'),
                               ('/-- Proves: `A.eq_1`.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'as a whole token'),
                               ('/-- Proves: `xA`.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'as a whole token'),
                               ("/-- Proves: `A'`.\nMethod: x.\nDoes not establish: y. -/\n" + thm('t', doc=False), 'as a whole token'),
                               ('/-- Proves: `Spec.Demo.A` (row x).\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), None),
                               ('/-- Proves: the Prop A of the register.\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), None),
                               ('/-- Proves:\nMethod: x.\nDoes not establish: y. -/\n' + thm('t', doc=False), 'empty `Proves:`'),
                               ('/-- Proves: `A`.\nMethod: x.\nDoes not establish: y. -/\n\n-- a comment between\n' + thm('t', doc=False), None),
                               ('/-- Proves: `A`.\nMethod: x.\nDoes not establish: y. -/\n@[simp]\n' + thm('t', doc=False), None)):
            with self.subTest(text=text[:50]):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(text)
                if fragment is None:
                    f.run()
                else:
                    with self.assertRaises(ValueError) as ctx:
                        f.run()
                    self.assertIn(fragment, str(ctx.exception))

    def test_underscore_name_component(self):
        self.f.inject(thm('_hidden'))
        self.assertRefused('may not start with `_`')

    def test_module_local_declaration_shadowing_a_registered_prop(self):
        """Lean resolves a name of the current namespace before an opened one: with a module-local
        `def A : Prop`, `theorem t : A` is about the local definition, so the source scan refuses
        the collision (declared before or after the theorem, as def, abbrev, structure, private or
        under an opened local namespace); an unrelated local name is fine."""
        for text in ('def A : Prop := True\n' + thm('tA', type_text='A'),
                     thm('tA', type_text='A') + '\ndef A : Prop := True',
                     'abbrev A : Prop := True\n' + thm('tA', type_text='A'),
                     'structure A where\n  n : ℕ\n' + thm('tA', type_text='A'),
                     'private def A : Prop := True\n' + thm('tA', type_text='A'),
                     'noncomputable def A : Prop := True\n' + thm('tA', type_text='A'),
                     'def Spec.Demo.A : Prop := True\n' + thm('tA', type_text='Spec.Demo.A'),
                     'def UniversalLaw.Spec.Demo.A : Prop := True\n' + thm('tA'),
                     'namespace Local\ndef A : Prop := True\nend Local\nopen Local in\n' + thm('tA', type_text='A'),
                     'theorem Aux.A : True := trivial\nopen Aux in\n' + thm('tA', type_text='A')):
            with self.subTest(text=text[:60]):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.inject(text)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn('shadowed by the module-local declaration', str(ctx.exception))
                # the fixture's own `theorem a : UniversalLaw.Spec.Demo.A` is refused first when the local name shadows the qualified one
                self.assertRegex(str(ctx.exception), r'theorem UniversalLaw\.Proofs\.Demo\.(tA|a): ')
        self.f.inject('def a2 : Prop := True\ndef Spec.A : Prop := True\n' + thm('tA', type_text='A'))
        self.assertEqual(self.f.run()['theorem_count'], 5)

    def test_bound_variable_head(self):
        """A theorem whose result type is one of its own parameters or a section variable named
        like a registered Prop is not about the registered Prop."""
        self.f.inject(thm('t', binders='(A : Prop) (hA : A)', type_text='A', body='hA'))
        self.assertRefused('is a parameter or section variable of the theorem')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject('section S\nvariable (A : Prop)\n' + thm('t', type_text='A', body='trivial') + '\nend S')
        self.assertRefused('is a parameter or section variable of the theorem')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject(thm('t', binders='{A : Prop}', type_text='A', body='trivial'))
        self.assertRefused('is a parameter or section variable of the theorem')


class Structure(Base):
    def test_declaration_outside_namespace(self):
        self.f.mutate('SpecificationProofs/Demo.lean', 'namespace UniversalLaw.Proofs.Demo\n', 'theorem early : True := trivial\n\nnamespace UniversalLaw.Proofs.Demo\n')
        self.assertRefused('declaration outside namespace')

    def test_wrong_or_foreign_namespace(self):
        self.f.mutate('SpecificationProofs/Demo.lean', 'namespace UniversalLaw.Proofs.Demo\n', 'namespace UniversalLaw.Proofs.Other\n')
        self.f.mutate('SpecificationProofs/Demo.lean', 'end UniversalLaw.Proofs.Demo\n', 'end UniversalLaw.Proofs.Other\n')
        self.assertRefused('outside the module namespace')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.write('SpecificationProofs/Demo.lean', self.f.read('SpecificationProofs/Demo.lean')
                     + '\nnamespace UniversalLaw.Spec.Demo\ntheorem leak : True := trivial\nend UniversalLaw.Spec.Demo\n')
        self.assertRefused('outside the module namespace')

    def test_unbalanced_scoping(self):
        self.f.inject('section S')
        self.assertRefused('does not close')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.mutate('SpecificationProofs/Demo.lean', '\nend UniversalLaw.Proofs.Demo\n', '\n')
        self.assertRefused('unclosed')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject('end Nope')
        self.assertRefused('does not close')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        self.f.inject('end')
        self.assertRefused('does not close')

    def test_noncomputable_section(self):
        self.f.inject('noncomputable section\nnoncomputable def r : ℝ := 1\nend')
        self.assertEqual(self.f.run()['auxiliary_definitions'], 2)

    def test_imports(self):
        for imports, fragment in (('import Mathlib\n', 'no statement module is imported'),
                                  ('import Specifications.Demo\nimport SpecificationProofs.Other\n', 'not a proof module of this packet'),
                                  ('import Specifications.Demo\nimport SpecificationProofs.Demo\n', 'nothing else'),
                                  ('import Specifications.Demo\nimport SpecificationProofs.Other.Deep\n', 'nothing else'),
                                  ('import Specifications.Demo\nimport Specifications.Other.Deep\n', 'nothing else'),
                                  ('import Specifications.Demo\nimport Other.Demo\n', 'nothing else'),
                                  ('import Specifications.Demo\nimport Specifications.Ghost\n', 'not a module of the statement packet'),
                                  ('import Specifications.Demo\nimport Mathlib.Data.Real.Basic\n', None)):
            with self.subTest(imports=imports):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.mutate('SpecificationProofs/Demo.lean', 'import Specifications.Demo\nimport Specifications.Other\n', imports)
                if fragment is None:
                    f.mutate('SpecificationProofs/Demo.lean', 'open UniversalLaw.Spec.Other in\n', '')
                    f.mutate('SpecificationProofs/Demo.lean', 'theorem d : D := trivial', 'theorem d : UniversalLaw.Spec.Demo.A := by norm_num [UniversalLaw.Spec.Demo.A]')
                    f.mutate('SpecificationProofs/Demo.lean', 'Proves: `D` (register row `demo-node`).', 'Proves: `A` (register row `demo-node`).')
                    f.run()
                else:
                    with self.assertRaises(ValueError) as ctx:
                        f.run()
                    self.assertIn(fragment, str(ctx.exception))


class Packet(Base):
    def test_root_imports(self):
        self.f.write('SpecificationProofs.lean', '')
        self.assertRefused('root module must import exactly')
        self.f.write('SpecificationProofs.lean', 'import SpecificationProofs.Demo\nimport SpecificationProofs.Ghost\n')
        self.assertRefused('root module must import exactly')
        self.f.write('SpecificationProofs.lean', 'import SpecificationProofs.Demo\nimport Mathlib\n')
        self.assertRefused('root module lines must read')
        self.f.write('SpecificationProofs.lean', 'import SpecificationProofs.Demo\nimport SpecificationProofs.Demo\n')
        self.assertRefused('twice')

    def test_tree(self):
        self.f.write('SpecificationProofs/notes.txt', 'x\n')
        self.assertRefused('packet tree differs')
        self.f.path('SpecificationProofs/notes.txt').unlink()
        self.f.write('SpecificationProofs/lower.lean', 'x\n')
        self.assertRefused('packet tree differs')
        self.f.path('SpecificationProofs/lower.lean').unlink()
        self.f.path('README.md').unlink()
        self.assertRefused('packet tree differs')
        self.f.write('README.md', '# Demo\n\n' + DOC)
        self.f.write('.gitignore', '__pycache__/\n')
        self.assertRefused('.gitignore must ignore')
        self.f.write('.gitignore', '.lake/\n__pycache__/\n')
        self.f.path('SpecificationProofs/Demo.lean').unlink()
        self.assertRefused('no proof module')

    def test_lock_and_toolchain(self):
        self.f.write('lean-toolchain', 'leanprover/lean4:v4.34.0\n')
        self.assertRefused('lean-toolchain must read exactly')
        self.f.write('lean-toolchain', check.TOOLCHAIN + '\n')
        self.f.mutate('lakefile.toml', 'rev = "' + check.MATHLIB_REV + '"', 'rev = "' + '0' * 40 + '"')
        self.assertIn('line 8', self.assertRefused('lakefile.toml must be byte-exactly'))
        self.f.mutate('lakefile.toml', 'rev = "' + '0' * 40 + '"', 'rev = "' + check.MATHLIB_REV + '"')
        self.f.mutate('lakefile.toml', check.LEAN_OPTIONS_LINE, 'leanOptions = { autoImplicit = true }')
        self.assertRefused('lakefile.toml must be byte-exactly')
        self.f.mutate('lakefile.toml', 'leanOptions = { autoImplicit = true }', check.LEAN_OPTIONS_LINE)
        self.f.run()
        self.f.mutate('lakefile.toml', '[[lean_lib]]', '[[require]]\nname = "extra"\ngit = "https://x"\nrev = "' + '1' * 40 + '"\n\n[[lean_lib]]')
        self.assertRefused('lakefile.toml must be byte-exactly')
        self.f = Fixture()
        self.addCleanup(self.f.cleanup)
        lock = json.loads(self.f.read('lake-manifest.json'))
        lock['packages'][1]['rev'] = '0' * 40
        self.f.write('lake-manifest.json', json.dumps(lock) + '\n')
        self.assertRefused('git dependencies differ from the statement packet lock')
        lock = json.loads(self.f.read('lake-manifest.json'))
        lock['packages'][1]['rev'] = check.MATHLIB_REV
        lock['packages'][2]['dir'] = '../elsewhere'
        self.f.write('lake-manifest.json', json.dumps(lock) + '\n')
        self.assertRefused('path dependency')
        lock['packages'][2]['dir'] = check.STATEMENT_DIR
        lock['name'] = 'other'
        self.f.write('lake-manifest.json', json.dumps(lock) + '\n')
        self.assertRefused('lake-manifest.json name must be')
        lock['name'] = check.LOCK_NAME
        lock['version'] = '1.2.1'
        self.f.write('lake-manifest.json', json.dumps(lock) + '\n')
        self.assertRefused('beyond name and packages')

    def test_lakefile_extra_lines_refused(self):
        """Lake accepts options that weaken checking (`moreLeanArgs = ["-Ddebug.skipKernelTC=true"]`
        at library or package level) and extra targets; a byte-exact pin refuses every extra line."""
        for old, new in (('leanOptions = { autoImplicit = false }\n', 'leanOptions = { autoImplicit = false }\nmoreLeanArgs = ["-Ddebug.skipKernelTC=true"]\n'),
                         ('version = "0.1.0"\n', 'version = "0.1.0"\nmoreLeanArgs = ["-Ddebug.skipKernelTC=true"]\n'),
                         ('version = "0.1.0"\n', 'version = "0.1.0"\nmoreServerArgs = ["-Ddebug.byAsSorry=true"]\n'),
                         ('leanOptions = { autoImplicit = false }\n', 'leanOptions = { autoImplicit = false }\n\n[[lean_exe]]\nname = "x"\nroot = "X"\n'),
                         ('leanOptions = { autoImplicit = false }\n', 'leanOptions = { autoImplicit = false, debug.skipKernelTC = true }\n'),
                         ('defaultTargets = ["SpecificationProofs"]\n', 'defaultTargets = ["SpecificationProofs"]\nleanOptions = { debug.skipKernelTC = true }\n'),
                         ('name = "mathlib"\n', 'name = "mathlib"\nsubDir = "x"\n'),
                         ('leanOptions = { autoImplicit = false }\n', 'leanOptions = { autoImplicit = false }\n\n'),
                         ('\n[[lean_lib]]', '\n# a comment\n[[lean_lib]]')):
            with self.subTest(new=new):
                f = Fixture()
                self.addCleanup(f.cleanup)
                f.mutate('lakefile.toml', old, new)
                with self.assertRaises(ValueError) as ctx:
                    f.run()
                self.assertIn('lakefile.toml must be byte-exactly', str(ctx.exception))
        self.assertEqual(check.LAKEFILE.count('[[require]]'), 2)
        self.assertEqual(check.LAKEFILE.count('[[lean_lib]]'), 1)
        self.assertNotIn('moreLeanArgs', check.LAKEFILE)
        self.assertIn('rev = "' + check.MATHLIB_REV + '"\n', check.LAKEFILE)
        self.assertIn('path = "' + check.STATEMENT_DIR + '"\n', check.LAKEFILE)

    def test_register(self):
        reg = register()
        reg['object'] = 'OTHER'
        self.f.save_register(reg)
        self.assertRefused('object must be')
        reg = register()
        reg['claims'][0]['statements'][0]['formal_progress'] = 'proved'
        self.f.save_register(reg)
        self.assertRefused('never relabels the register')
        reg = register()
        reg['toolchain']['mathlib'] = '0' * 40
        self.f.save_register(reg)
        self.assertRefused('toolchain pins differ')
        reg = register()
        for row in reg['claims']:
            row['statements'] = [st for st in row['statements'] if st['kind'] != 'def_prop']
        self.f.save_register(reg)
        self.assertRefused('names no `def')
        reg = register()
        reg['claims'][1]['statements'][0]['module'] = 'Specifications/Other.lean'
        self.f.save_register(reg)
        self.assertRefused('registered in two modules')
        reg = register()
        reg['alignment_status'] = 'ALIGNED'
        self.f.save_register(reg)
        self.assertRefused('scope fields')
        reg = register()
        reg['claims'][1]['statements'][2]['module'] = 'Specifications/Ghost.lean'
        self.f.save_register(reg)
        self.assertRefused('missing or escaping file')

    def test_statement_packet_must_be_the_path_dependency(self):
        shutil.rmtree(self.f.statements)
        self.assertRefused('must be the statement packet')

    def test_docs(self):
        self.f.write('README.md', '# Demo\n\n<<TABLE>>\n' + DOC)
        self.assertRefused('placeholder')
        self.f.write('README.md', '# Demo\n\nScientific effect: NONE.\n')
        self.assertIn("missing 'PENDING_INDEPENDENT_REVIEW'", self.assertRefused('must state the scientific effect'))
        self.f.write('README.md', '# Demo\n\nEffect: NONE. Alignment: PENDING_INDEPENDENT_REVIEW.\n')
        self.assertIn("missing 'Scientific effect'", self.assertRefused('must state the scientific effect'))
        self.f.write('README.md', '# Demo\n\nScientific effect: none. Alignment: PENDING_INDEPENDENT_REVIEW.\n')
        self.assertIn("missing 'NONE'", self.assertRefused('must state the scientific effect'))
        self.f.write('README.md', '# Demo\n\n' + DOC)
        self.f.write('SCOPE.md', '# Scope\n\nScientific effect: NONE.\n')
        self.assertIn('SCOPE.md', self.assertRefused('must state the scientific effect'))


class Units(unittest.TestCase):
    def test_result_head(self):
        self.assertEqual(check.result_head(' UniversalLaw.Spec.P15.Foo F  '), ('UniversalLaw.Spec.P15.Foo', ['F']))
        self.assertEqual(check.result_head('Foo\n    x y'), ('Foo', ['x', 'y']))
        self.assertEqual(check.result_head("Foo x' y₁"), ('Foo', ["x'", 'y₁']))
        for bad in ('Foo (x)', 'Foo → Foo', '∀ x, Foo x', 'Foo ∧ Bar', '¬ Foo', '', '@Foo x', 'Foo _root_.x'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    check.result_head(bad)

    def test_parse_binders(self):
        out = check.parse_binders(' {X : Type} [Fintype X] [inst : DecidableEq X] (F G : RealizedData X) ⦃k : ℕ⦄ (n : ℕ := 3) (z) m ')
        self.assertEqual([(b['kind'], b['names']) for b in out],
                         [('implicit', ['X']), ('instance', []), ('instance', ['inst']), ('explicit', ['F', 'G']), ('strict', ['k']),
                          ('explicit', ['n']), ('explicit', ['z']), ('explicit', ['m'])])
        self.assertEqual(check.parse_binders(''), [])
        self.assertEqual(check.parse_binders('(h : ∀ x : ℕ, x = x)'), [{'kind': 'explicit', 'names': ['h']}])
        with self.assertRaises(ValueError):
            check.parse_binders('(x : ℕ')
        with self.assertRaises(ValueError):
            check.parse_binders('⟨a, b⟩')

    def test_first_colon(self):
        self.assertEqual(check.first_colon('(x : ℕ) : P x'), 8)
        self.assertEqual(check.first_colon(' := rfl'), None)
        self.assertEqual(check.first_colon('(h : a :: l = m) : Q'), 17)

    def test_legal_head(self):
        for head, ok in (('', True), ('private ', True), ('protected noncomputable ', True), ('@[simp] ', True), ('@[simp, norm_cast] private ', True),
                         ('open Classical in ', False), ('  ', False), (' private ', False), ('set_option x y in ', False), ('exact ', False), ('@[simp', False)):
            with self.subTest(head=head):
                self.assertEqual(check.legal_head(head), ok)

    def test_open_targets(self):
        self.assertEqual(check.open_targets('open Finset Real'), ['Finset', 'Real'])
        self.assertEqual(check.open_targets('open scoped BigOperators'), ['BigOperators'])
        self.assertEqual(check.open_targets('open Finset (sum prod)'), ['Finset'])
        self.assertEqual(check.open_targets('open Finset hiding card'), ['Finset'])
        self.assertEqual(check.open_targets('open Classical in'), ['Classical'])

    def test_resolve_head(self):
        reg = {'UniversalLaw.Spec.Demo.A': {}, 'UniversalLaw.Spec.Other.A': {}}
        ns = ['UniversalLaw.Proofs.Demo']
        self.assertEqual(check.resolve_head('UniversalLaw.Spec.Demo.A', [], ns, reg), 'UniversalLaw.Spec.Demo.A')
        self.assertEqual(check.resolve_head('Spec.Demo.A', [], ns, reg), 'UniversalLaw.Spec.Demo.A')
        self.assertEqual(check.resolve_head('A', ['UniversalLaw.Spec.Demo'], ns, reg), 'UniversalLaw.Spec.Demo.A')
        self.assertEqual(check.resolve_head('A', ['Spec.Demo'], ns, reg), 'UniversalLaw.Spec.Demo.A')
        with self.assertRaises(ValueError):
            check.resolve_head('A', ['UniversalLaw.Spec.Demo', 'UniversalLaw.Spec.Other'], ns, reg)
        with self.assertRaises(ValueError):
            check.resolve_head('A', [], ns, reg)
        local = {'UniversalLaw.Proofs.Demo.A', 'UniversalLaw.Proofs.Demo.twice'}
        with self.assertRaises(ValueError) as ctx:
            check.resolve_head('A', ['UniversalLaw.Spec.Demo'], ns, reg, local)
        self.assertIn('shadowed by the module-local declaration', str(ctx.exception))
        self.assertEqual(check.resolve_head('UniversalLaw.Spec.Demo.A', [], ns, reg, local), 'UniversalLaw.Spec.Demo.A')
        self.assertEqual(check.resolve_head('Spec.Demo.A', [], ns, reg, local), 'UniversalLaw.Spec.Demo.A')
        self.assertEqual(check.head_candidates('A', ['Spec.Demo'], ns),
                         {'A', 'UniversalLaw.A', 'UniversalLaw.Proofs.A', 'UniversalLaw.Proofs.Demo.A', 'Spec.Demo.A', 'UniversalLaw.Spec.Demo.A',
                          'UniversalLaw.Proofs.Spec.Demo.A', 'UniversalLaw.Proofs.Demo.Spec.Demo.A'})

    def test_names_prop(self):
        head = 'UniversalLaw.Spec.Demo.A'
        for text, ok in (('`UniversalLaw.Spec.Demo.A` (row x)', True), ('`A`.', True), ('`Spec.Demo.A`', True), ('the Prop A of', True),
                         ('`AA`', False), ('`xA`', False), ("`A'`", False), ('`A.eq_1`', False), ('`A_1`', False), ('`UniversalLaw.Spec.Demo.AA`', False),
                         ('A.', True), ('(A)', True), ('', False), ('`B`', False)):
            with self.subTest(text=text):
                self.assertEqual(check.names_prop(text, head), ok)

    def test_leanchecker_mode(self):
        with mock.patch.dict(os.environ):
            os.environ.pop(check.SKIP_LEANCHECKER_ENV, None)
            os.environ.pop('GITHUB_ACTIONS', None)
            self.assertEqual((check.leanchecker_mode(False), check.leanchecker_mode(True)), ('RUN', 'RUN'))
            os.environ[check.SKIP_LEANCHECKER_ENV] = '0'
            self.assertEqual((check.leanchecker_mode(False), check.leanchecker_mode(True)), ('RUN', 'RUN'))
            os.environ[check.SKIP_LEANCHECKER_ENV] = '1'
            self.assertEqual(check.leanchecker_mode(True), 'SKIPPED_LOCAL_ONLY')
            with self.assertRaises(ValueError) as ctx:
                check.leanchecker_mode(False)
            self.assertIn('only together with --allow-dirty', str(ctx.exception))
            os.environ['GITHUB_ACTIONS'] = 'true'
            with self.assertRaises(ValueError) as ctx:
                check.leanchecker_mode(True)
            self.assertIn('refused in CI', str(ctx.exception))

    def test_parse_audit(self):
        log = ('x.lean:1:0: info: AUDIT theorem UniversalLaw.Proofs.D.a UniversalLaw.Spec.D.A\nAUDIT aux_theorem UniversalLaw.Proofs.D.Aux.h\n'
               'AUDIT auxiliary UniversalLaw.Proofs.D.f\nAUDIT generated UniversalLaw.Proofs.D.S.injEq\nAUDIT END 4 0 1\n')
        classes, heads = check.parse_audit(log)
        self.assertEqual(heads, {'UniversalLaw.Proofs.D.a': 'UniversalLaw.Spec.D.A'})
        self.assertEqual(set(classes), check.AUDIT_CLASSES)
        with self.assertRaises(ValueError):
            check.parse_audit(log.replace('AUDIT END 4 0 1', 'AUDIT END 5 0 1'))
        with self.assertRaises(ValueError):
            check.parse_audit(log.replace('AUDIT END 4 0 1', 'AUDIT END 4 1 1'))
        with self.assertRaises(ValueError):
            check.parse_audit(log.replace('AUDIT END 4 0 1', 'AUDIT END 4 0 2'))
        with self.assertRaises(ValueError):
            check.parse_audit(log.replace('UniversalLaw.Proofs.D.a UniversalLaw.Spec.D.A', 'UniversalLaw.Proofs.D.a'))
        with self.assertRaises(ValueError):
            check.parse_audit(log + 'AUDIT END 4 0 1\n')
        refused = log.replace('AUDIT auxiliary UniversalLaw.Proofs.D.f', 'AUDIT REFUSED:premise:UniversalLaw.Spec.D.A UniversalLaw.Proofs.D.f').replace('END 4 0 1', 'END 4 1 1')
        classes, _ = check.parse_audit(refused)
        self.assertIn('REFUSED:premise:UniversalLaw.Spec.D.A', classes)

    def test_audit_axioms(self):
        text = "'A.a' depends on axioms: [propext, Classical.choice, Quot.sound]\n'A.b' does not depend on any axioms\n"
        self.assertEqual(check.audit_axioms(text, ['A.a', 'A.b']), {'A.a': ['Classical.choice', 'Quot.sound', 'propext'], 'A.b': []})
        with self.assertRaises(ValueError) as ctx:
            check.audit_axioms(text.replace('Quot.sound', 'sorryAx'), ['A.a', 'A.b'])
        self.assertIn('forbidden transitive axiom', str(ctx.exception))
        with self.assertRaises(ValueError):
            check.audit_axioms(text, ['A.a'])
        with self.assertRaises(ValueError):
            check.audit_axioms(text, ['A.a', 'A.b', 'A.c'])
        with self.assertRaises(ValueError):
            check.audit_axioms(text + 'stray line\n', ['A.a', 'A.b'])

    def test_signatures_and_version(self):
        log = 'A.a : UniversalLaw.Spec.D.A\nA.b (n : ℕ) :\n  UniversalLaw.Spec.D.B n\n'
        self.assertEqual(check.signatures(log, ['A.a', 'A.b'])['A.b'], 'A.b (n : ℕ) :\n  UniversalLaw.Spec.D.B n')
        with self.assertRaises(ValueError):
            check.signatures(log, ['A.c'])
        good = f'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit {check.LEAN_COMMIT}, Release)'
        self.assertEqual(check.check_lean_version('info: x\n' + good + '\n'), good)
        with self.assertRaises(ValueError):
            check.check_lean_version(good.replace('4.34.1', '4.34.0'))
        with self.assertRaises(ValueError):
            check.check_lean_version(good.replace(check.LEAN_COMMIT, '0' * 40))

    def test_audit_source_and_controls_text(self):
        src = check.audit_source('SpecificationProofs', ['SpecificationProofs.Demo'], ['UniversalLaw.Spec.Demo.A'])
        self.assertIn('def registeredProps : Array Name := #[`UniversalLaw.Spec.Demo.A]', src)
        self.assertIn('def auditModules : Array Name := #[`SpecificationProofs.Demo]', src)
        self.assertIn('REFUSED:premise', src)
        self.assertIn('run_cmd', src)
        hidden = check.HIDDEN_CONTROL.format(ns=check.CONTROL_NS, prop='P')
        for word in ('sorry', 'axiom hidden', 'theorem smuggled (h : False) : P', 'theorem implication : P → P', 'opaque', 'unsafe def'):
            self.assertIn(word, hidden)


class Controls(Base):
    def test_source_controls(self):
        info = self.f.run()
        ctrl = Path(self.f.tmp) / 'controls'
        ctrl.mkdir()
        outcomes = check.source_controls(info, ctrl)
        self.assertEqual({k: v for k, v in outcomes.items() if k != 'maxHeartbeats_justified'},
                         {k: 'REFUSED_BY_SOURCE_CHECK' for k in ('sorry', 'axiom', 'native_decide', 'maxHeartbeats_unjustified', 'unregistered_type',
                                                                 'smuggled_hypothesis', 'implication', 'missing_docstring_labels')})
        self.assertTrue(outcomes['maxHeartbeats_justified'].startswith('ACCEPTED'))
        self.assertEqual(len(list(ctrl.glob('Source_*.lean.txt'))), 8)

    def test_parameterless_prop(self):
        info = self.f.run()
        self.assertEqual(check.parameterless_prop(self.f.statements, info['registered']), 'UniversalLaw.Spec.Demo.A')
        self.f.mutate('Specifications/Demo.lean', 'def A : Prop :=', 'def A (u : Unit) : Prop :=', stmt=True)
        self.f.mutate('Specifications/Other.lean', 'def D : Prop :=', 'def D (u : Unit) : Prop :=', stmt=True)
        self.f.mutate('Specifications/Other.lean', 'def A : Prop :=', 'def A (u : Unit) : Prop :=', stmt=True)
        with self.assertRaises(ValueError):
            check.parameterless_prop(self.f.statements, info['registered'])

    def test_expect_refusal(self):
        def ok():
            return 1

        def bad():
            raise ValueError('wrong reason')
        with self.assertRaises(ValueError) as ctx:
            check.expect_refusal(ok, 'x', 'escaped')
        self.assertIn('escaped the source check', str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            check.expect_refusal(bad, 'other', 'label')
        self.assertIn('wrong reason', str(ctx.exception))


# ----------------------------------------------------------------------------- final runtime observation (no Lean)

GOOD_VERSION = f'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit {check.LEAN_COMMIT}, Release)'
LAST_CONTROL = 'control_environment_honest'  # the last Lean run of negative_controls()


def git_fixture(path, *args):
    return subprocess.run(['git', '-C', str(path), '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false', *args],
                          capture_output=True, text=True, check=True).stdout


def dependency_checkouts(packet, names):
    """Real disposable git checkouts under <packet>/.lake/packages, one commit each; {name: HEAD}."""
    heads = {}
    for name in names:
        pkg = packet / '.lake' / 'packages' / name
        pkg.mkdir(parents=True)
        git_fixture(pkg, 'init', '-q')
        (pkg / 'lakefile.toml').write_text('name = "' + name + '"\n')
        git_fixture(pkg, 'add', '-A')
        git_fixture(pkg, 'commit', '-q', '-m', 'pin')
        heads[name] = git_fixture(pkg, 'rev-parse', 'HEAD').strip()
    return heads


def audit_log(lines, refused, theorems):
    return (''.join(f'Environment.lean:1:0: info: AUDIT {line}\n' for line in lines)
            + f'Environment.lean:1:0: info: AUDIT END {len(lines)} {refused} {theorems}\n')


class FakeLean:
    """Stands in for check.run, through which every Lean execution of execute() passes: answers
    each label with output of the shape check.py parses, writes the log as run() does, records
    the label sequence, and calls `hook(label)` first so that a test can change the runtime during
    a chosen run. Never starts Lean; nothing it prints is evidence about anything."""

    def __init__(self, info=None, final_version=GOOD_VERSION, hook=None):
        self.info, self.hook, self.labels = info, hook, []
        self.versions = {'version': GOOD_VERSION, 'version-final': final_version}

    def __call__(self, command, label, out, cwd, env, expect_success=True, timeout=3600):
        self.labels.append(label)
        if self.hook:
            self.hook(label)
        text = self.answer(command, label)
        (out / (label + '.log')).write_text(text, encoding='utf-8')
        return text

    def answer(self, command, label):
        c = check.CONTROL_NS + '.'
        if label in self.versions:
            return 'info: toolchain already up to date\n' + self.versions[label] + '\n'
        if label in ('axioms', 'types', 'control_environment_hidden', 'control_environment_honest'):
            text = Path(command[-1]).read_text(encoding='utf-8')
        if label == 'axioms':
            return ''.join(f"'{n}' depends on axioms: [propext]\n" for n in re.findall(r'^#print axioms (\S+)$', text, re.M))
        if label == 'types':
            proves = {t['name']: t['proves'] for t in self.info['theorems']}
            return ''.join(f'{n} : {proves[n]}\n' for n in re.findall(r'^#check (\S+)$', text, re.M))
        if label == 'environment':
            return audit_log([f'theorem {t["name"]} {t["proves"]}' for t in self.info['theorems']], 0, len(self.info['theorems']))
        if label == 'control_sorry_axioms':
            return f"ControlSorry.lean:3:8: warning: declaration uses 'sorry'\n'{c}sorried' depends on axioms: [sorryAx]\n"
        if label == 'control_false_arithmetic':
            return ''.join(f'ControlFalseArithmetic.lean:{k}:0: error: unsolved goals\n⊢ False\n' for k in (4, 5))
        if label == 'control_missing_declaration':
            return f'ControlMissing.lean:2:7: error(lean.unknownIdentifier): Unknown identifier `{c}DoesNotExist`\n'
        if label == 'control_environment_hidden':
            prop = re.search(r'^theorem smuggled \(h : False\) : (\S+) :=', text, re.M).group(1)
            return audit_log([f'REFUSED:axioms:sorryAx {c}sorried', f'REFUSED:axiom {c}hidden', f'REFUSED:axioms:{c}hidden {c}usesAxiom',
                              f'REFUSED:type:True {c}unregistered', f'REFUSED:premise:{prop} {c}smuggled', f'REFUSED:premise:{prop} {c}implication',
                              f'REFUSED:proof_as_def {c}proofAsDef', f'REFUSED:opaque {c}opq', f'REFUSED:unsafe {c}unsafeDef'], 9, 0) + \
                'Environment.lean:1:0: error: AUDIT REFUSED 9 constant(s); see the AUDIT lines\n'
        if label == 'control_environment_honest':
            honest = re.search(r'^theorem honest : (\S+) :=', text, re.M)
            lines = ([f'theorem {c}honest {honest.group(1)}'] if honest else []) + [
                f'aux_theorem {c}Aux.helper', f'aux_theorem _private.SpecificationProofs.0.{c}privateHelper', f'auxiliary {c}helper',
                f'auxiliary {c}controlInst']
            return audit_log(lines, 0, 1 if honest else 0)
        return ''  # build, leanchecker: a clean log


@unittest.skipUnless(shutil.which('git'), 'git not available')
class FinalObservation(Base):
    """G4 placement: after its last Lean run execute() re-observes the exact Lean release and the
    dependency checkouts and requires both to equal the preflight observation. Lean is never run
    (check.run is a FakeLean); the dependency checkouts are real disposable git repositories, so the
    real dependency_state() and git decide. Each refusal test fails against a checker that observes
    the runtime only before the build."""

    def setUp(self):
        super().setUp()
        os.environ.pop(check.SKIP_LEANCHECKER_ENV, None)
        self.heads = dependency_checkouts(self.f.packet, ('batteries', 'mathlib'))
        self.out = Path(self.f.tmp) / 'evidence'
        self.out.mkdir()

    def observe(self, final_version=GOOD_VERSION):
        fake = FakeLean(final_version=final_version)
        with mock.patch.object(check, 'run', fake):
            return check.final_observation('/nonexistent/lake', self.f.packet, {}, self.out, GOOD_VERSION, dict(self.heads)), fake

    def execute(self, **fake_args):
        info = dict(self.f.run(), dependency_revisions=dict(self.heads))  # the fixture lock's revisions name no real checkout
        fake = FakeLean(info, **fake_args)
        with mock.patch.object(check, 'run', fake), mock.patch.object(check, 'lake_binary', return_value='/nonexistent/lake'):
            return check.execute(self.f.packet, self.f.repo, info, True), fake

    def move_head(self, label, name='mathlib'):
        if label == LAST_CONTROL:
            git_fixture(self.f.packet / '.lake' / 'packages' / name, 'commit', '-q', '--allow-empty', '-m', 'moved during the last Lean run')

    def make_dirty(self, label, name='batteries'):
        if label == LAST_CONTROL:
            (self.f.packet / '.lake' / 'packages' / name / 'lakefile.toml').write_text('name = "edited during the last Lean run"\n')

    def assertExecuteRefused(self, fragment, **fake_args):
        with self.assertRaises(ValueError) as ctx:
            self.execute(**fake_args)
        self.assertIn(fragment, str(ctx.exception))
        self.assertFalse((self.f.packet / '.lake' / 'evidence' / 'receipt.json').exists(), 'a refused execution writes no receipt')

    def test_unchanged_runtime_is_observed_equal(self):
        obs, fake = self.observe()
        self.assertEqual(obs, {'lean_version': GOOD_VERSION, 'dependency_revisions': self.heads, 'dependency_worktrees': 'CLEAN'})
        self.assertEqual(fake.labels, ['version-final'])
        self.assertTrue((self.out / 'version-final.log').is_file())

    def test_final_lean_version_differs(self):
        for bad, fragment in ((GOOD_VERSION.replace(check.LEAN_COMMIT, 'f' * 40), 'not the pinned release'),
                              (GOOD_VERSION.replace('Release', 'Debug'), 'not the pinned release'),
                              (GOOD_VERSION.replace('4.34.1', '4.34.2'), 'not the pinned release'),
                              # the pinned release on another platform passes check_lean_version; only the preflight equality refuses it
                              (GOOD_VERSION.replace('x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu'), 'changed during execution')):
            with self.subTest(final=bad):
                with self.assertRaises(ValueError) as ctx:
                    self.observe(bad)
                self.assertIn(fragment, str(ctx.exception))

    def test_dependency_head_moves(self):
        self.move_head(LAST_CONTROL)
        with self.assertRaises(ValueError) as ctx:
            self.observe()
        self.assertIn('dependency revisions', str(ctx.exception))

    def test_dependency_worktree_becomes_dirty(self):
        self.make_dirty(LAST_CONTROL)
        with self.assertRaises(ValueError) as ctx:
            self.observe()
        self.assertIn('dependency worktree is not clean: batteries', str(ctx.exception))
        git_fixture(self.f.packet / '.lake' / 'packages' / 'batteries', 'checkout', '--', '.')
        self.observe()
        (self.f.packet / '.lake' / 'packages' / 'mathlib' / 'untracked.lean').write_text('-- untracked\n')
        with self.assertRaises(ValueError) as ctx:
            self.observe()
        self.assertIn('dependency worktree is not clean: mathlib', str(ctx.exception))

    def test_execute_receipt_records_equal_observations_after_the_last_lean_run(self):
        receipt, fake = self.execute()
        preflight = {'lean_version': GOOD_VERSION, 'dependency_revisions': self.heads, 'dependency_worktrees': 'CLEAN'}
        self.assertEqual(receipt['observations'], {'preflight': preflight, 'final': preflight})
        self.assertEqual((receipt['lean_version'], receipt['dependency_revisions'], receipt['dependency_worktrees']),
                         (GOOD_VERSION, self.heads, 'CLEAN'), 'the existing receipt keys are kept as they were')
        self.assertEqual(receipt['leanchecker'], 'PASS')
        self.assertEqual(fake.labels[0], 'version')
        self.assertEqual(fake.labels[-1], 'version-final', 'the final observation follows every other Lean run')
        self.assertEqual(fake.labels.count('version-final'), 1)
        self.assertIn(LAST_CONTROL, fake.labels)
        self.assertIn('version-final.log', receipt['logs'])
        written = json.loads((self.f.packet / '.lake' / 'evidence' / 'receipt.json').read_text(encoding='utf-8'))
        self.assertEqual(written['observations']['final'], written['observations']['preflight'])

    def test_execute_refuses_a_lean_version_change(self):
        self.assertExecuteRefused('not the pinned release', final_version=GOOD_VERSION.replace(check.LEAN_COMMIT, '0' * 40))
        self.assertExecuteRefused('not the pinned release', final_version=GOOD_VERSION.replace('Release', 'Debug'))
        self.assertExecuteRefused('changed during execution', final_version=GOOD_VERSION.replace('x86_64-unknown-linux-gnu', 'aarch64-apple-darwin'))

    def test_execute_refuses_a_dependency_head_moved_during_the_last_lean_run(self):
        self.assertExecuteRefused('dependency revisions', hook=self.move_head)

    def test_execute_refuses_a_dependency_worktree_dirtied_during_the_last_lean_run(self):
        self.assertExecuteRefused('dependency worktree is not clean: batteries', hook=self.make_dirty)


# ----------------------------------------------------------------------------- Lean-driving tests

LAKE = check.lake_binary()
FIXTURE_STATEMENT = '''namespace UniversalLaw.Spec.Demo

/-- A. -/
def A : Prop := 1 + 1 = 2

/-- B. -/
def B (n : Nat) : Prop := n + 0 = n

/-- C. -/
def C {X : Type} [Inhabited X] (x : X) : Prop := x = x

/-- Iface. -/
structure Iface where
  x : Nat

end UniversalLaw.Spec.Demo
'''
FIXTURE_PROOFS = '''import Specifications.Demo

namespace UniversalLaw.Proofs.Demo

open UniversalLaw.Spec.Demo

namespace Aux
theorem helper : True := trivial
end Aux

private theorem hiddenHelper : True := trivial

def twice (n : Nat) : Nat := 2 * n

instance demoInst : Inhabited Nat := ⟨0⟩

structure Pair where
  a : Nat
  b : Nat

/-- Proves: `A`.
Method: rfl.
Does not establish: anything. -/
theorem a : UniversalLaw.Spec.Demo.A := rfl

/-- Proves: `B`.
Method: rfl.
Does not establish: anything. -/
theorem b (n : Nat) : B n := by
  simp [UniversalLaw.Spec.Demo.B]

section Params

variable {X : Type} [Inhabited X]

/-- Proves: `C`.
Method: rfl.
Does not establish: anything. -/
theorem c (x : X) : UniversalLaw.Spec.Demo.C x := rfl

end Params

end UniversalLaw.Proofs.Demo
'''
FIXTURE_PROOFS2 = '''import Specifications.Demo

namespace UniversalLaw.Proofs.Demo2

/-- Proves: `B`.
Method: simp (generates the equation lemma of `B` in this module too).
Does not establish: anything. -/
theorem bAgain (n : Nat) : UniversalLaw.Spec.Demo.B n := by
  simp [UniversalLaw.Spec.Demo.B]

end UniversalLaw.Proofs.Demo2
'''
FIXTURE_REGISTERED = ['UniversalLaw.Spec.Demo.A', 'UniversalLaw.Spec.Demo.B', 'UniversalLaw.Spec.Demo.C']
FIXTURE_EXPECTED = {'UniversalLaw.Proofs.Demo.a': 'UniversalLaw.Spec.Demo.A', 'UniversalLaw.Proofs.Demo.b': 'UniversalLaw.Spec.Demo.B',
                    'UniversalLaw.Proofs.Demo.c': 'UniversalLaw.Spec.Demo.C', 'UniversalLaw.Proofs.Demo2.bAgain': 'UniversalLaw.Spec.Demo.B'}


@unittest.skipUnless(LAKE, 'lake not available')
class LeanHelpers(unittest.TestCase):
    """Two dependency-free fixture packages (a statement package and a proof package depending on
    it by path): real `lake build`, `leanchecker`, `#check`, `#print axioms`, the environment
    audit, its controls, and module copies carrying each escape family that the environment audit
    must refuse. No Mathlib; nothing here is about the real modules."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        stmt, self.proofs = self.tmp / 'stmt', self.tmp / 'proofs'
        (stmt / 'Specifications').mkdir(parents=True)
        (self.proofs / 'SpecificationProofs').mkdir(parents=True)
        (stmt / 'lakefile.toml').write_text('name = "spec_fixture_statements"\ndefaultTargets = ["Specifications"]\n\n[[lean_lib]]\n'
                                            'name = "Specifications"\n' + check.LEAN_OPTIONS_LINE + '\n')
        (stmt / 'lean-toolchain').write_text(check.TOOLCHAIN + '\n')
        (stmt / 'lake-manifest.json').write_text(json.dumps({'version': '1.2.0', 'packagesDir': '.lake/packages', 'packages': [],
                                                           'name': 'spec_fixture_statements', 'lakeDir': '.lake'}) + '\n')
        (stmt / 'Specifications.lean').write_text('import Specifications.Demo\n')
        (stmt / 'Specifications/Demo.lean').write_text(FIXTURE_STATEMENT)
        (self.proofs / 'lakefile.toml').write_text('name = "spec_fixture_proofs"\ndefaultTargets = ["SpecificationProofs"]\n\n[[require]]\n'
                                                   'name = "spec_fixture_statements"\npath = "../stmt"\n\n[[lean_lib]]\n'
                                                   'name = "SpecificationProofs"\n' + check.LEAN_OPTIONS_LINE + '\n')
        (self.proofs / 'lean-toolchain').write_text(check.TOOLCHAIN + '\n')
        (self.proofs / 'lake-manifest.json').write_text(json.dumps({'version': '1.2.0', 'packagesDir': '.lake/packages', 'packages': [
            {'type': 'path', 'name': 'spec_fixture_statements', 'dir': '../stmt', 'manifestFile': 'lake-manifest.json', 'inherited': False,
             'configFile': 'lakefile.toml'}], 'name': 'spec_fixture_proofs', 'lakeDir': '.lake'}) + '\n')
        (self.proofs / 'SpecificationProofs.lean').write_text('import SpecificationProofs.Demo\nimport SpecificationProofs.Demo2\n')
        (self.proofs / 'SpecificationProofs/Demo.lean').write_text(FIXTURE_PROOFS)
        (self.proofs / 'SpecificationProofs/Demo2.lean').write_text(FIXTURE_PROOFS2)
        self.out = self.proofs / '.lake' / 'evidence'
        (self.out / 'controls').mkdir(parents=True)
        self.env = check.lean_env(LAKE)

    def build(self, module_text=None, expect_success=True):
        if module_text is not None:
            (self.proofs / 'SpecificationProofs/Demo.lean').write_text(module_text)
        if (self.proofs / '.lake' / 'build').exists():
            shutil.rmtree(self.proofs / '.lake' / 'build')
        return check.run([LAKE, 'build'], 'build', self.out, self.proofs, self.env, expect_success=expect_success)

    def audit(self, expected=FIXTURE_EXPECTED, registered=FIXTURE_REGISTERED):
        return check.environment_audit(LAKE, self.proofs, self.env, self.out, ['SpecificationProofs.Demo', 'SpecificationProofs.Demo2'], registered, expected)

    def test_fixture_packages(self):
        names = list(FIXTURE_EXPECTED)
        with contextlib.redirect_stdout(io.StringIO()):
            check.check_lean_version(check.run([LAKE, 'env', 'lean', '--version'], 'version', self.out, self.proofs, self.env))
            log = self.build()
            self.assertNotIn('is a proposition; use', log)
            self.assertIsNone(check.MODULE_WARNING.search(log))
            check.run([LAKE, 'env', 'leanchecker', 'SpecificationProofs'], 'leanchecker', self.out, self.proofs, self.env)
            axioms, sigs = check.kernel_audit(LAKE, self.proofs, self.env, self.out, names)
            self.assertEqual(set(axioms), set(names))
            self.assertTrue(all(set(v) <= check.ALLOWED_AXIOMS for v in axioms.values()), axioms)
            self.assertEqual((axioms['UniversalLaw.Proofs.Demo.a'], axioms['UniversalLaw.Proofs.Demo.c']), ([], []))
            self.assertEqual(sigs['UniversalLaw.Proofs.Demo.a'], 'UniversalLaw.Proofs.Demo.a : UniversalLaw.Spec.Demo.A')
            self.assertEqual(sigs['UniversalLaw.Proofs.Demo.b'], 'UniversalLaw.Proofs.Demo.b (n : Nat) : UniversalLaw.Spec.Demo.B n')
            counts = self.audit()
            self.assertEqual((counts['theorem'], counts['aux_theorem']), (4, 2))
            env_log = (self.out / 'environment.log').read_text()
            eqns = re.findall(r'AUDIT generated (UniversalLaw\.Spec\.Demo\.B\.eq_\w+)', env_log)
            self.assertTrue(eqns, 'the equation lemma of B, generated in both modules, is audited as generated: ' + env_log)
            self.assertEqual(len(eqns), len(set(eqns)), 'each equation lemma is audited once although two modules generate it')
            self.assertGreaterEqual(counts['auxiliary'], 4, 'twice, demoInst, Pair and its constructor/recursor/projections')
            env_log = (self.out / 'environment.log').read_text()
            self.assertIn('AUDIT aux_theorem UniversalLaw.Proofs.Demo.Aux.helper', env_log)
            self.assertRegex(env_log, r'AUDIT aux_theorem _private\.\S*hiddenHelper')
            self.assertIn('AUDIT auxiliary UniversalLaw.Proofs.Demo.twice', env_log)
            self.assertIn('AUDIT auxiliary UniversalLaw.Proofs.Demo.demoInst', env_log)
            self.assertIn('AUDIT theorem UniversalLaw.Proofs.Demo.c UniversalLaw.Spec.Demo.C', env_log)
            self.assertNotIn('REFUSED', env_log)
            with self.assertRaises(ValueError) as ctx:
                self.audit({**FIXTURE_EXPECTED, 'UniversalLaw.Proofs.Demo.ghost': 'UniversalLaw.Spec.Demo.A'})
            self.assertIn('missing', str(ctx.exception))
            with self.assertRaises(ValueError) as ctx:
                self.audit({k: v for k, v in FIXTURE_EXPECTED.items() if not k.endswith('.a')})
            self.assertIn('unexpected', str(ctx.exception))
            with self.assertRaises(ValueError) as ctx:
                self.audit({**FIXTURE_EXPECTED, 'UniversalLaw.Proofs.Demo.a': 'UniversalLaw.Spec.Demo.B'})
            self.assertIn('head differs', str(ctx.exception))
            with self.assertRaises(ValueError):
                check.environment_audit(LAKE, self.proofs, self.env, self.out, ['SpecificationProofs.Missing'], FIXTURE_REGISTERED, FIXTURE_EXPECTED)
            # a registered set that lacks A: Lean refuses `a` as REFUSED:type even though it compiles
            with self.assertRaises(ValueError) as ctx:
                self.audit(registered=FIXTURE_REGISTERED[1:])
            self.assertIn('REFUSED:type:UniversalLaw.Spec.Demo.A', str(ctx.exception) + (self.out / 'environment.log').read_text())
            self.assertEqual(check.lean_control_missing(LAKE, self.proofs, self.env, self.out, 'UniversalLaw.Proofs.Demo.Missing'), 'REJECTED_BY_LEAN')
            with self.assertRaises(ValueError):
                check.kernel_audit(LAKE, self.proofs, self.env, self.out, names + ['UniversalLaw.Proofs.Demo.Missing'])
            self.assertTrue(check.lean_control_sorry_axioms(LAKE, self.proofs, self.env, self.out, 'UniversalLaw.Spec.Demo.A').startswith('REFUSED_BY_AXIOM_AUDIT'))
            verdict = check.lean_control_environment(LAKE, self.proofs, self.env, self.out, FIXTURE_REGISTERED, 'UniversalLaw.Spec.Demo.A',
                                                     'UniversalLaw.Proofs.Demo.a')
            self.assertIn('REFUSED_BY_ENVIRONMENT_AUDIT', verdict)
            self.assertNotIn('no parameterless', verdict)
            hidden_log = (self.out / 'control_environment_hidden.log').read_text()
            c = check.CONTROL_NS + '.'
            for verdict_line in ('REFUSED:axioms:sorryAx ' + c + 'sorried', 'REFUSED:axiom ' + c + 'hidden',
                                 'REFUSED:axioms:' + c + 'hidden ' + c + 'usesAxiom', 'REFUSED:type:True ' + c + 'unregistered',
                                 'REFUSED:premise:UniversalLaw.Spec.Demo.A ' + c + 'smuggled', 'REFUSED:premise:UniversalLaw.Spec.Demo.A ' + c + 'implication',
                                 'REFUSED:proof_as_def ' + c + 'proofAsDef', 'REFUSED:opaque ' + c + 'opq', 'REFUSED:unsafe ' + c + 'unsafeDef'):
                self.assertIn('AUDIT ' + verdict_line, hidden_log)
            honest_log = (self.out / 'control_environment_honest.log').read_text()
            self.assertIn('AUDIT theorem ' + c + 'honest UniversalLaw.Spec.Demo.A', honest_log)
            verdict = check.lean_control_environment(LAKE, self.proofs, self.env, self.out, FIXTURE_REGISTERED, 'UniversalLaw.Spec.Demo.A', None)
            self.assertIn('no parameterless', verdict)
            self.assertNotIn('AUDIT theorem', (self.out / 'control_environment_honest.log').read_text())

    def test_environment_audit_refuses_escapes_lean_accepts(self):
        """Module copies Lean builds without error must be refused by the environment audit, each
        for its own reason: the shape rules the source scan cannot see (an implicit extra binder,
        a narrowed argument after `open`, a theorem in a non-Aux sub-namespace), and the escapes
        the scan does see but that must also fail at the Lean side."""
        tail = 'end UniversalLaw.Proofs.Demo'
        cases = {
            'implicit smuggled hypothesis': ('theorem t {h : False} : UniversalLaw.Spec.Demo.A := h.elim', 'REFUSED:premise:UniversalLaw.Spec.Demo.A'),
            'explicit smuggled hypothesis': ('theorem t (h : False) : UniversalLaw.Spec.Demo.A := h.elim', 'REFUSED:premise:UniversalLaw.Spec.Demo.A'),
            'narrowed argument': ('theorem t (k : Nat) : B (k + 1) := rfl', 'REFUSED:premise:UniversalLaw.Spec.Demo.B'),
            'fixed instance argument': ('theorem t : UniversalLaw.Spec.Demo.C (0 : Nat) := rfl', 'REFUSED:premise:UniversalLaw.Spec.Demo.C'),
            'implication P → P': ('theorem t : UniversalLaw.Spec.Demo.A → UniversalLaw.Spec.Demo.A := fun h => h', 'REFUSED:premise:UniversalLaw.Spec.Demo.A'),
            'unregistered type': ('theorem t : True := trivial', 'REFUSED:type:True'),
            'structure type is not a Prop': ('theorem t : (2 : Nat) + 2 = 4 := rfl', 'REFUSED:type:Eq'),
            'non-Aux sub-namespace': ('namespace Helpers\ntheorem t : True := trivial\nend Helpers', 'REFUSED:type:True'),
            'indented hidden theorem': (' theorem t : True := trivial', 'REFUSED:type:True'),
            'theorem between string literals': ('def opener : String := "/-"\ntheorem t : True := trivial\ndef closer : String := "-/"', 'REFUSED:type:True'),
            'axiom': ('axiom hidden : False', 'REFUSED:axiom'),
            'axiom used by a registered-type theorem': ('axiom hidden : False\ntheorem t : UniversalLaw.Spec.Demo.A := hidden.elim',
                                                        'REFUSED:axioms:UniversalLaw.Proofs.Demo.hidden'),
            'opaque': ('opaque opq : Nat', 'REFUSED:opaque'),
            'unsafe': ('unsafe def u : Nat := 0', 'REFUSED:unsafe'),
            'bound-variable type': ('theorem t (p : Prop) (hp : p) : p := hp', 'REFUSED:type:nonconstant'),
            'module-local def shadowing the registered Prop': ('def A : Prop := True\ntheorem tA : A := trivial', 'REFUSED:type:UniversalLaw.Proofs.Demo.A'),
            'decide +native (per-use native axiom)': ('theorem t : (1 : Nat) + 1 = 2 := by decide +native', 'REFUSED:axiom'),
        }
        with contextlib.redirect_stdout(io.StringIO()):
            for label, (text, fragment) in cases.items():
                with self.subTest(label=label):
                    self.build(FIXTURE_PROOFS.replace(tail, text + '\n' + tail))
                    with self.assertRaises(ValueError) as ctx:
                        self.audit()
                    self.assertIn(fragment, str(ctx.exception) + (self.out / 'environment.log').read_text())
            log = self.build(FIXTURE_PROOFS.replace(tail, 'def proofAsDef : (2 : Nat) + 2 = 4 := rfl\nabbrev proofAsAbbrev : True := trivial\n' + tail))
            self.assertIn('is a proposition; use', log, 'the build-log check of execute() refuses the defProp linter warning')
            with self.assertRaises(ValueError):
                self.audit()
            env_log = (self.out / 'environment.log').read_text()
            self.assertIn('AUDIT REFUSED:proof_as_def UniversalLaw.Proofs.Demo.proofAsDef', env_log)
            self.assertIn('AUDIT REFUSED:proof_as_def UniversalLaw.Proofs.Demo.proofAsAbbrev', env_log)
            log = self.build(FIXTURE_PROOFS.replace(tail, 'theorem t : UniversalLaw.Spec.Demo.A := sorry\n' + tail))
            self.assertIn('declaration uses', log)
            with self.assertRaises(ValueError):
                self.audit()
            self.assertIn('AUDIT REFUSED:axioms:sorryAx UniversalLaw.Proofs.Demo.t', (self.out / 'environment.log').read_text())
            # a registered-type theorem under Aux is an aux theorem, never inventory; one more inventory theorem is `unexpected`
            self.build(FIXTURE_PROOFS.replace(tail, 'theorem Aux.a2 : UniversalLaw.Spec.Demo.A := rfl\ntheorem a3 : UniversalLaw.Spec.Demo.A := rfl\n' + tail))
            with self.assertRaises(ValueError) as ctx:
                self.audit()
            self.assertIn('unexpected', str(ctx.exception))
            self.assertIn("['UniversalLaw.Proofs.Demo.a3']", str(ctx.exception))
            self.assertIn('AUDIT aux_theorem UniversalLaw.Proofs.Demo.Aux.a2', (self.out / 'environment.log').read_text())

    def test_auto_implicit_is_off(self):
        """With `autoImplicit = false` an unbound name in a header is an error instead of a silent
        implicit parameter."""
        with contextlib.redirect_stdout(io.StringIO()):
            log = self.build(FIXTURE_PROOFS.replace('theorem b (n : Nat) : B n := by', 'theorem b : B n := by'), expect_success=False)
        self.assertIn('Unknown identifier `n`', log)


# ----------------------------------------------------------------------------- real tree

REAL_REPO = HERE.parents[1]
REAL_STATEMENTS = (HERE / check.STATEMENT_DIR).resolve()


@unittest.skipUnless((REAL_STATEMENTS / 'REGISTER.json').is_file() and (HERE / 'lakefile.toml').is_file(), 'real tree not present')
class RealPacket(unittest.TestCase):
    """The committed packets' pins and the scans of the modules present, independent of git state."""

    def test_pins(self):
        revs = check.check_lock(HERE, REAL_STATEMENTS)
        self.assertEqual(revs['mathlib'], check.MATHLIB_REV)
        self.assertEqual(len(revs), 9)
        lock = json.loads((HERE / 'lake-manifest.json').read_text())
        self.assertEqual(lock['packages'][-1], check.PATH_DEPENDENCY)
        self.assertIn('.lake/', (HERE / '.gitignore').read_text().splitlines())
        self.assertIn(check.LEAN_OPTIONS_LINE, (HERE / 'lakefile.toml').read_text().splitlines())
        self.assertEqual((HERE / 'lakefile.toml').read_bytes(), check.LAKEFILE.encode(), 'lakefile.toml is pinned byte-exactly')
        self.assertEqual((HERE / 'lean-toolchain').read_text(), check.TOOLCHAIN + '\n')

    def test_register_inventory(self):
        registered, structures, digest = check.load_register(REAL_STATEMENTS)
        self.assertGreaterEqual(len(registered), 100)
        self.assertIn('UniversalLaw.Spec.P15.RhoStarBelowSixSevenths', registered)
        self.assertTrue(all(n.startswith(check.STATEMENT_NAMESPACE) for n in registered))
        self.assertEqual(len(digest), 64)
        self.assertIn(check.parameterless_prop(REAL_STATEMENTS, registered), registered)

    def test_modules_scan(self):
        registered, _, _ = check.load_register(REAL_STATEMENTS)
        modules = sorted((HERE / check.ROOT_MODULE).glob('*.lean'))
        self.assertTrue(modules, 'at least one proof module is present')
        for m in modules:
            with self.subTest(module=m.name):
                scan = check.scan_module(m.read_text(encoding='utf-8'), m.stem, registered)
                self.assertTrue(scan['theorems'], m.name + ' declares at least one inventory theorem')
                for t in scan['theorems']:
                    self.assertIn(t['proves'], registered)

    def test_root_imports_present_modules(self):
        modules = sorted(check.ROOT_MODULE + '/' + p.name for p in (HERE / check.ROOT_MODULE).glob('*.lean'))
        check.check_root(HERE, modules)

    def test_workflow(self):
        path = REAL_REPO / check.WORKFLOW
        if not path.is_file():
            self.skipTest('workflow not present in this tree')
        text = path.read_text(encoding='utf-8')
        for needle in ('lake-package-directory: ' + check.PACKAGE, "use-mathlib-cache: 'true'", "- '" + check.PACKAGE + "/**'",
                       "- '" + check.STATEMENT_PACKAGE + "/**'", 'check.py --execute', 'test_check.py LeanHelpers', '.lake/evidence/',
                       'python -B -O -S'):
            self.assertIn(needle, text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
