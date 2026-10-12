#!/usr/bin/env python3
"""Protocol tests and negative controls for the torus-filtration companion driver (stdlib only).

Nothing here executes Lean. The fixture tests exercise check.py's `source` and `finish`
commands against a temporary Git repository whose Lean modules are inventory placeholders,
so every weakening of a check is caught now, before the hosted replay runs the real modules.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SIDE = Path(__file__).resolve().parent
ROOT = SIDE.parents[1]
INVENTORY = {
    'TorusTopology': {
        'theorem': '''torus_field_latticeVec_formula torus_basis_sum_eq_latticeVec torus_lattice_mem_iff
            torus_proj_surjective torus_proj_continuous torus_proj_eq_iff torus_control_lattice_translate
            torus_proj_isCoveringMap torus_compact torus_pathConnectedSpace torus_field_periodic_formula
            torus_periodic_respects torus_descend_proj torus_descend_continuous torus_path_lift_from
            torus_control_constant_path_endpoint torus_control_no_arbitrary_endpoint torus_higher_path_iff
            torus_strict_higher_path_iff torus_closed_higher_path_iff torus_global_max_iff'''.split(),
        'abbrev': ['torus_E', 'torus_quotient'],
        'def': ['torus_latticeVec', 'torus_periodBasis', 'torus_periodLattice', 'torus_proj', 'torus_isPeriodic',
                'torus_descend'],
        'instance': ['torus_lattice_discrete', 'torus_lattice_addSubgroup_discrete', 'torus_lattice_isZLattice']},
    'ClosedSuperlevel': {
        'theorem': '''superlevel_control_closed_endpoint superlevel_control_strict_endpoint
            superlevel_control_parameter_sign superlevel_control_inclusion_direction superlevel_control_essential
            superlevel_mono superlevel_isClosed superlevel_inclusion_id superlevel_inclusion_comp
            superlevel_mem_at_own_height superlevel_neg_height superlevel_control_strict_thresholds
            superlevel_componentMap_mk superlevel_componentMap_id superlevel_componentMap_comp
            superlevel_componentInclusion_id superlevel_componentInclusion_comp superlevel_component_eq_iff_joinedIn
            superlevel_h0Filtration_map_id superlevel_h0Filtration_map_comp'''.split(),
        'abbrev': [],
        'def': ['superlevel_set', 'superlevel_inclusion', 'superlevel_componentMap', 'superlevel_componentInclusion',
                'superlevel_filtration', 'superlevel_h0Filtration'],
        'instance': []},
    # C263 successor (346eea94…), as scan_module reports it
    'SuperlevelBar': {
        'theorem': '''superlevelBar_essential_iff superlevelBar_mem_lt_start superlevelBar_clearance_bddAbove
            superlevelBar_clearance_empty_of_essential superlevelBar_death_eq_zero_of_empty
            superlevelBar_death_eq_zero_of_essential superlevelBar_death_eq_sSup_of_nonempty superlevelBar_path_minimum
            superlevelBar_clearance_nonempty superlevelBar_clearance_nonempty_iff superlevelBar_clearance_downward
            superlevelBar_clearance_improve superlevelBar_strict_cut superlevelBar_death_le_start_of_nonempty
            superlevelBar_death_le_start superlevelBar_clearance_eq_Iio superlevelBar_death_not_mem_clearance
            superlevelBar_cut_unique superlevelBar_death_const superlevelBar_control_negative_essential'''.split(),
        'abbrev': ['superlevelBar_E'],
        'def': ['superlevelBar_isEssential', 'superlevelBar_clearanceSet', 'superlevelBar_deathHeight'],
        'instance': []},
    # C264 successor (3d6b0d6b…), as scan_module reports it: the two filtration declarations precede the homology ones
    'OrdinaryH0': {
        'theorem': '''ordinaryH0_componentCoproductMap_iota ordinaryH0_componentFiltration_map_iota
            ordinaryH0_simplicialPointClass_iso ordinaryH0_simplicialPointClass_map ordinaryH0_toSSet_pointMap
            ordinaryH0_pointClass_map ordinaryH0_pointClass_iso ordinaryH0_componentIota_isoInv ordinaryH0_hom_ext
            ordinaryH0_iso_naturality ordinaryH0_pointClass_augmentation ordinaryH0_pointClass_ne_zero
            ordinaryH0_pointClass_eq_of_component_eq ordinaryH0_sameComponent_difference_zero
            ordinaryH0_pointClass_ne_of_component_ne ordinaryH0_pointClass_eq_iff ordinaryH0_difference_map
            ordinaryH0_difference_map_eq_zero_iff ordinaryH0_filtration_naturality
            ordinaryH0_filtration_difference_zero_iff_joinedIn'''.split(),
        'abbrev': [],
        'def': ['ordinaryH0_componentFunctor', 'ordinaryH0_componentCoproductFunctor', 'ordinaryH0_componentFiltration',
                'ordinaryH0_simplicialPointClass', 'ordinaryH0_pointClass', 'ordinaryH0_naturalIso', 'ordinaryH0_filtrationIso'],
        'instance': []},
    # owner-authored C264 item-4 controls (df9d3645…), as scan_module reports it; every name carries ordinaryH0Control_
    'OrdinaryH0Controls': {
        'theorem': '''ordinaryH0Control_intCoeff_id_ne_zero ordinaryH0Control_mod2Coeff_id_ne_zero
            ordinaryH0Control_mod2Coeff_id_add_self ordinaryH0Control_zeroCoeff_isZero ordinaryH0Control_zeroCoeff_id_eq_zero
            ordinaryH0Control_empty_components ordinaryH0Control_empty_componentCoproduct_isZero ordinaryH0Control_empty_h0_isZero
            ordinaryH0Control_zeroCoeff_componentCoproduct_isZero ordinaryH0Control_zeroCoeff_h0_isZero
            ordinaryH0Control_point_augmentation ordinaryH0Control_point_ne_zero ordinaryH0Control_point_h0_not_isZero
            ordinaryH0Control_line_component_eq ordinaryH0Control_line_difference_zero_int
            ordinaryH0Control_line_difference_zero_zeroCoeff ordinaryH0Control_line_classes_ne_zero
            ordinaryH0Control_discrete_component_ne ordinaryH0Control_bool_component_ne ordinaryH0Control_bool_pointClass_ne
            ordinaryH0Control_bool_pointClass_ne_mod2 ordinaryH0Control_collapse_difference_zero
            ordinaryH0Control_collapse_image_ne_zero ordinaryH0Control_collapse_difference_dies_classes_survive
            ordinaryH0Control_square_differences_ne_zero ordinaryH0Control_fst_difference_zero
            ordinaryH0Control_fst_difference_ne_zero ordinaryH0Control_bool_zeroCoeff_eq ordinaryH0Control_point_zeroCoeff_eq_zero
            ordinaryH0Control_separation_needs_nonzero ordinaryH0Control_nonvanishing_needs_nonzero ordinaryH0Control_parabola_le
            ordinaryH0Control_parabola_strict_growth ordinaryH0Control_parabola_not_joined_quarter ordinaryH0Control_parabola_joined
            ordinaryH0Control_parabola_difference_zero ordinaryH0Control_parabola_strict_difference_ne_zero'''.split(),
        'abbrev': ['ordinaryH0Control_intCoeff', 'ordinaryH0Control_zeroCoeff', 'ordinaryH0Control_mod2Coeff'],
        'def': ['ordinaryH0Control_collapse', 'ordinaryH0Control_fst', 'ordinaryH0Control_parabolaLeft',
                'ordinaryH0Control_parabolaRight'],
        'instance': []}}
HANDOFF_COMMENTS = ('6111056103', '6111059166', '6111059498', '6111059848', '6111255007', '6111093545', '6111139060')
# Math- #428 (and the #419 allocation) comments the C26x successor record cites, per module.
SUCCESSOR_COMMENTS = {'SuperlevelBar.lean': {'6112439759', '6113033545', '6113229784'},
                      'OrdinaryH0.lean': {'6113276830', '6113277173', '6113277485', '6113300903', '6113372506', '6113438262'}}
SUCCESSOR_IDENTITY = {'SuperlevelBar.lean': ('346eea948e18d5904422904006827930e27d3141ccbc19ee8ac2c24bcf65a4a9', 15309,
                                             'd74dc8b2c25eff5b90ce7133e51a0888c7885cae24ca6d5e648bc514089637a8', 14904),
                      'OrdinaryH0.lean': ('3d6b0d6b53413c484b1d010bccf0d53ae7f75becb2d747868f22dbd673fe0a88', 19803,
                                          '261dd0526d42890d8a4ac1225fcf47228eb3c9799af4106cb643a528bcbf968e', 18469)}
# The owner-authored controls module (no handoff bytes): its identity and the Math- #428 comments its record cites
# (6113277485: C264 owner task, item 4; 6113277173: the corrected CONTROL_OBLIGATIONS it instantiates).
OWNER_IDENTITY = {'OrdinaryH0Controls.lean': ('df9d3645282ca526b67eca3d5db691b622092a14b5fddee9be21013e39666184', 29590)}
OWNER_COMMENTS = {'OrdinaryH0Controls.lean': {'6113277485', '6113277173'}}
LEAN_VERSION_LINE = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)\n'
FALSE_LOG = '/tmp/evidence/{0}.lean:4:2: error: unsolved goals\n⊢ False\n'
# The item-4 controls as Lean 4.34.1 printed them at the Mathlib d13f23b7 pin (this lane's pre-commit run on the
# registered bytes, 2026-10-12; only the directory before the file name is shortened): each leaves exactly `⊢ False`.
CONTROL_LOGS = {
    'RejectMergerKillsPointClass': '/tmp/evidence/RejectMergerKillsPointClass.lean:3:255: error: unsolved goals\n⊢ False\n',
    'RejectSeparationWithoutNonzeroCoeff': '/tmp/evidence/RejectSeparationWithoutNonzeroCoeff.lean:3:160: error: unsolved goals\n⊢ False\n',
    'RejectNonmergerKillsDifference': '/tmp/evidence/RejectNonmergerKillsDifference.lean:3:391: error: unsolved goals\n⊢ False\n',
}
# Discriminators: the same tactic on each control's TRUE sibling statement (the difference under the collapse; the
# ℤ-coefficient separation of Bool; the (true, false)/(true, true) difference under the projection), emitted in the same
# format under the same file name and printed by Lean in the same run. Each is a different diagnostic, which `negative`
# must refuse: the controls' `⊢ False` comes from the falsehood of their statements, not from a tactic that turns any
# goal into False.
DISCRIMINATOR_LOGS = {
    'RejectMergerKillsPointClass': '/tmp/evidence/RejectMergerKillsPointClass.lean:4:2: error: `simp` made no progress\n',
    'RejectSeparationWithoutNonzeroCoeff': '/tmp/evidence/RejectSeparationWithoutNonzeroCoeff.lean:3:158: error: unsolved goals\n⊢ ¬ordinaryH0_pointClass (↧Bool) ordinaryH0Control_intCoeff true =\n      ordinaryH0_pointClass (↧Bool) ordinaryH0Control_intCoeff false\n/tmp/evidence/RejectSeparationWithoutNonzeroCoeff.lean:4:8: error: This simp argument is unused:\n  ordinaryH0Control_bool_zeroCoeff_eq\n\nHint: Omit it from the simp argument list.\n  [apply] simp\n\nNote: This linter can be disabled with `set_option linter.unusedSimpArgs false`\n',
    'RejectNonmergerKillsDifference': '/tmp/evidence/RejectNonmergerKillsDifference.lean:4:2: error: `simp` made no progress\n',
}
SORRY_WARNING = "/tmp/evidence/RejectSorry.lean:2:8: warning: declaration uses `sorry`\n"
INJECTED = "'injected' depends on axioms: [{0}]\n"
LEANCHECKER_MODULES = 'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0 OrdinaryH0Controls TorusFiltration'
LEANCHECKER_MODULES_BEFORE_CONTROLS = 'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0 TorusFiltration'
LEANCHECKER_MODULES_BEFORE_C26X = 'leanchecker TorusTopology ClosedSuperlevel TorusFiltration'
LEANCHECKER_FRESH = 'leanchecker --fresh TorusFiltration'
EMITTED = ('Audit.lean', 'Types.lean', 'Positive.lean', 'Census.lean', 'RejectSuperlevelSignFlip.lean',
           'RejectSuperlevelBelowThreshold.lean', 'RejectConstantNotPeriodic.lean', 'RejectEssentialDeathBound.lean',
           'RejectReducedPointClass.lean', 'RejectMergerKillsPointClass.lean', 'RejectSeparationWithoutNonzeroCoeff.lean',
           'RejectNonmergerKillsDifference.lean', 'RejectSorry.lean', 'RejectCustomAxiom.lean', 'RejectNativeDecide.lean')
PYTHON_LINE = 'TORUS_FILTRATION_PYTHON: optimize=%d' % sys.flags.optimize
# Compiler-generated internal constants as the real census lists them (abstracted proofs, equation lemmas); the fixture
# census carries a few so the parser's `internal generated` branch is exercised. Rows four to fifteen are exactly the
# `internal generated` rows of the C263 and C264 range-aware censuses at the pin (1 + 11), and the last four those of
# OrdinaryH0Controls (`_proof_1` and `eq_1` of its two subtype-point definitions); the fifth,
# `CategoryTheory.Limits.sigmaConst.eq_1`, is the equation lemma Lean generated for a Mathlib definition that
# OrdinaryH0.lean unfolds, attributed to the companion module, so the census parser must tolerate internal generated
# constants outside the companion namespace.
INTERNAL_GENERATED = ('TorusFiltration.superlevel_set.eq_1', 'TorusFiltration.torus_periodBasis._proof_1',
                      'TorusFiltration.torus_proj_eq_iff._abel_1_1',
                      'TorusFiltration.superlevelBar_deathHeight.eq_1',
                      'CategoryTheory.Limits.sigmaConst.eq_1', 'TorusFiltration.ordinaryH0_componentCoproductFunctor.eq_1',
                      'TorusFiltration.ordinaryH0_componentFunctor._proof_1', 'TorusFiltration.ordinaryH0_componentFunctor._proof_2',
                      'TorusFiltration.ordinaryH0_componentFunctor.eq_1', 'TorusFiltration.ordinaryH0_hom_ext._simp_1_1',
                      'TorusFiltration.ordinaryH0_simplicialPointClass._proof_1',
                      'TorusFiltration.ordinaryH0_simplicialPointClass._proof_2',
                      'TorusFiltration.ordinaryH0_simplicialPointClass._proof_3',
                      'TorusFiltration.ordinaryH0_simplicialPointClass._proof_4',
                      'TorusFiltration.ordinaryH0_simplicialPointClass.eq_1',
                      'TorusFiltration.ordinaryH0Control_parabolaLeft._proof_1', 'TorusFiltration.ordinaryH0Control_parabolaLeft.eq_1',
                      'TorusFiltration.ordinaryH0Control_parabolaRight._proof_1', 'TorusFiltration.ordinaryH0Control_parabolaRight.eq_1')
# The outer interpreter mode goes into the test transcript (tests.log / tests-optimized.log), so the hosted
# evidence records which mode each suite ran in (C262 G1).
print('TORUS_FILTRATION_TESTS: outer optimize=%d' % sys.flags.optimize, file=sys.stderr)


def checker():
    spec = importlib.util.spec_from_file_location('torus_filtration_checker', SIDE / 'check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def child_python():
    """Interpreter prefix for every check.py child: `-B -S` plus the OUTER interpreter's optimization level.

    A child spawned through sys.executable does not inherit the parent's -O; until C262 (Math- #428 comment
    6112740935, finding G1) the -O test run therefore exercised check.py's CLI paths unoptimized."""
    flags = ['-B', '-S']
    if sys.flags.optimize:
        flags.append('-' + 'O' * sys.flags.optimize)
    return [sys.executable, *flags]


def child_env(extra=None):
    """Child environment: no GITHUB_* (host identity is set explicitly where a test needs it) and no PYTHONOPTIMIZE,
    ambient or injected, so the child's mode is exactly the one child_python() selects."""
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GITHUB_')}
    environment.update(extra or {})
    environment.pop('PYTHONOPTIMIZE', None)
    return environment


OPTIMIZE_PROBE = 'import sys; print(sys.flags.optimize)'


def placeholder_module(module):
    """Inventory-exact Lean text that is never compiled; only the whitelist scan reads it."""
    lines = ['import Mathlib', '', '/-! fixture module; not the companion source -/', '', 'namespace TorusFiltration', '']
    lines += ['theorem %s : True := trivial' % n for n in INVENTORY[module]['theorem']]
    lines += ['abbrev %s : Type := Nat' % n for n in INVENTORY[module]['abbrev']]
    lines += ['noncomputable def %s : Nat := 0' % n for n in INVENTORY[module]['def']]
    lines += ['instance %s : Inhabited Nat := ⟨0⟩' % n for n in INVENTORY[module]['instance']]
    lines += ['', 'end TorusFiltration', '']
    return '\n'.join(lines)


def good_injection_log(c, control):
    _, forbidden, _ = c.INJECTIONS[control]
    return (SORRY_WARNING if control == 'RejectSorry' else '') + INJECTED.format(forbidden)


class Fixture:
    """A committed temporary repository carrying the companion layout and a matching manifest."""

    def __init__(self, c, tmp):
        self.c = c
        self.root = Path(tmp)
        self.side = self.root / c.PACKAGE
        self.side.mkdir(parents=True)
        (self.root / c.WORKFLOW).parent.mkdir(parents=True)
        (self.root / 'formal').mkdir()
        for module in c.MODULES:
            (self.side / (module + '.lean')).write_text(placeholder_module(module))
        (self.side / 'TorusFiltration.lean').write_text(c.ROOT_SOURCE)
        shutil.copy(SIDE / 'check.py', self.side / 'check.py')
        for name in ('replay.sh', 'test_torus_filtration.py', 'README.md', 'SCOPE.md'):
            (self.side / name).write_text('# fixture ' + name + '\n')
        (self.root / c.WORKFLOW).write_text('name: fixture\n')
        (self.root / 'formal/lean-toolchain').write_text('leanprover/lean4:v4.34.1\n')
        (self.root / 'formal/lakefile.toml').write_text('name = "fixture"\n')
        self.revisions = {'mathlib': 'd1' * 20, 'batteries': 'f2' * 20}
        self.write_manifest([{'name': k, 'rev': v} for k, v in self.revisions.items()])
        self.regenerate()
        self.git('init', '-q', '-b', 'main')
        self.commit()

    def git(self, *args):
        return subprocess.run(['git', '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                               '-c', 'commit.gpgsign=false', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'fixture', '--allow-empty')

    def write_manifest(self, packages):
        (self.root / 'formal/lake-manifest.json').write_text(json.dumps({'packages': packages}))

    def regenerate(self):
        meta = self.c.metadata()
        meta['files'] = {p: self.c.identity((self.root / p).read_bytes()) for p in self.c.REQUIRED_FILES
                         if (self.root / p).is_file()}
        (self.side / 'SOURCE_FILES.json').write_text(json.dumps(meta, indent=2, sort_keys=True) + '\n')

    def manifest(self, mutate):
        """Commit a SOURCE_FILES.json with one field rewritten (mutate edits the dict, or returns raw text)."""
        meta = json.loads((self.side / 'SOURCE_FILES.json').read_text())
        raw = mutate(meta)
        text = raw if isinstance(raw, str) else json.dumps(meta, indent=2, sort_keys=True) + '\n'
        (self.side / 'SOURCE_FILES.json').write_text(text)
        self.commit()

    def restore(self):
        self.regenerate()
        self.commit()

    def run(self, *args, env=None):
        result = subprocess.run([*child_python(), str(self.side / 'check.py'), *args], cwd=self.root,
                                capture_output=True, text=True, env=child_env(env))
        # Every child reports the mode it actually runs in (check.py main); it must be the outer mode, on every
        # call, accept or refuse. A fixture that stopped propagating -O would fail here, not pass silently (C262 G1).
        if result.stderr.count(PYTHON_LINE + '\n') != 1 or 'TORUS_FILTRATION_PYTHON: optimize=' in result.stderr.replace(PYTHON_LINE, ''):
            raise AssertionError('check.py child did not report the outer interpreter mode %d: %r' % (sys.flags.optimize, result.stderr[:300]))
        return result

    def evidence(self):
        out = self.root / 'evidence'
        out.mkdir()
        source = self.run('source')
        if source.returncode != 0:
            raise AssertionError(source.stderr)
        (out / 'source.json').write_text(source.stdout)
        emitted = self.run('emit', str(out))
        if emitted.returncode != 0:
            raise AssertionError(emitted.stderr)
        (out / 'toolchain.log').write_text(LEAN_VERSION_LINE)
        (out / 'packages.log').write_text(''.join('%s %s\n' % kv for kv in self.revisions.items()))
        (out / 'tests.log').write_text('TORUS_FILTRATION_TESTS: outer optimize=0\nRan 1 test\n\nOK\n')
        (out / 'tests-optimized.log').write_text('TORUS_FILTRATION_TESTS: outer optimize=1\nRan 1 test\n\nOK\n')
        for label in self.c.BUILDS:
            (out / (label + '.status')).write_text('0\n')
            (out / (label + '.log')).write_text('')
        (out / 'leanchecker.cmd').write_text(LEANCHECKER_MODULES + '\n')
        meta = self.c.metadata()
        targets = self.c.targets(meta)
        lines = ["'%s' depends on axioms: [propext, Classical.choice, Quot.sound]" % n for n in targets[:-1]]
        lines.append("'%s' does not depend on any axioms" % targets[-1])
        (out / 'axioms.log').write_text('\n'.join(lines) + '\n')
        (out / 'types.log').write_text(''.join('%s (d : ℕ) : True\n' % n for n in self.c.theorem_targets(meta)))
        for control in self.c.FALSE_CONTROLS:
            (out / (control + '.log')).write_text(FALSE_LOG.format(control))
            (out / (control + '.status')).write_text('1\n')
        for control in self.c.INJECTIONS:
            (out / (control + '.log')).write_text(good_injection_log(self.c, control))
            (out / (control + '.status')).write_text('0\n')
        rows = sorted([(n, 'user range') for n in targets] + [(n, 'user generated') for n in meta['census_auxiliary']]
                      + [(n, 'internal generated') for n in INTERNAL_GENERATED])
        (out / 'census.log').write_text(''.join('%s %s\n' % r for r in rows) + 'CENSUS_END %d\n' % len(rows))
        return out


class FixtureCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = checker()

    def assertFails(self, run, message):
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn('TORUS_FILTRATION_FAIL: ' + message, run.stderr)


class ChildInterpreterMode(unittest.TestCase):
    """C262 G1: the mode a check.py child actually runs in is observed, not inferred from an argument string."""

    def test_children_run_in_the_outer_optimization_mode(self):
        outer = sys.flags.optimize
        probe = subprocess.run([*child_python(), '-c', OPTIMIZE_PROBE], capture_output=True, text=True, env=child_env())
        self.assertEqual((probe.returncode, probe.stdout.strip()), (0, str(outer)), probe.stderr)
        # Ambient or injected PYTHONOPTIMIZE never reaches the child: the mode is the outer one in both cases.
        saved = os.environ.get('PYTHONOPTIMIZE')
        os.environ['PYTHONOPTIMIZE'] = '2'
        try:
            ambient = subprocess.run([*child_python(), '-c', OPTIMIZE_PROBE], capture_output=True, text=True, env=child_env())
            injected = subprocess.run([*child_python(), '-c', OPTIMIZE_PROBE], capture_output=True, text=True,
                                      env=child_env({'PYTHONOPTIMIZE': '1'}))
        finally:
            if saved is None:
                del os.environ['PYTHONOPTIMIZE']
            else:
                os.environ['PYTHONOPTIMIZE'] = saved
        self.assertEqual(ambient.stdout.strip(), str(outer))
        self.assertEqual(injected.stdout.strip(), str(outer))
        self.assertFalse('PYTHONOPTIMIZE' in child_env({'PYTHONOPTIMIZE': '1'}))   # assertFalse: never print an environment
        # The invocation the fixture used before C262 (no propagation) runs the child unoptimized whatever the outer
        # mode is; under `-O` that is exactly the G1 observation, under the normal mode the two agree at 0.
        plain = subprocess.run([sys.executable, '-B', '-S', '-c', OPTIMIZE_PROBE], capture_output=True, text=True, env=child_env())
        self.assertEqual(plain.stdout.strip(), '0')
        if outer:
            self.assertNotEqual(plain.stdout.strip(), str(outer))
        self.assertEqual(child_python()[1:], ['-B', '-S'] + (['-' + 'O' * outer] if outer else []))

    def test_every_check_py_child_reports_the_outer_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(checker(), tmp)
            accepted = f.run('source')                      # Fixture.run itself requires the diagnostic on every call
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(accepted.stderr.strip(), PYTHON_LINE)
            (f.side / 'README.md').write_text('# edited without a commit\n')
            refused = f.run('source')
            self.assertEqual(refused.returncode, 1)
            self.assertEqual(refused.stderr.splitlines()[0], PYTHON_LINE)
            self.assertIn('TORUS_FILTRATION_FAIL: dirty execution/source bytes', refused.stderr)
            f.git('checkout', '--', '.')
            # The invocation the fixture used before C262 runs the real check.py unoptimized under an outer -O, and
            # check.py now says so itself; under the normal outer mode both report 0.
            plain = subprocess.run([sys.executable, '-B', '-S', str(f.side / 'check.py'), 'source'], cwd=f.root,
                                   capture_output=True, text=True, env=child_env())
            self.assertEqual(plain.returncode, 0, plain.stderr)
            self.assertEqual(plain.stderr.strip(), 'TORUS_FILTRATION_PYTHON: optimize=0')
            if sys.flags.optimize:
                self.assertNotEqual(plain.stderr.strip(), PYTHON_LINE)
            # Negative control of the fixture's own guard: with the child prefix rebound to the OTHER mode, Fixture.run
            # itself must refuse (so a fixture that stopped propagating -O, or dropped the guard, is caught here).
            other = [sys.executable, '-B', '-S'] + ([] if sys.flags.optimize else ['-O'])
            saved = globals()['child_python']
            globals()['child_python'] = lambda: other
            try:
                with self.assertRaises(AssertionError):
                    f.run('source')
            finally:
                globals()['child_python'] = saved
            self.assertEqual(f.run('source').returncode, 0)


class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = checker()

    def test_inventory_constants(self):
        names = [n for m in INVENTORY.values() for kind in m.values() for n in kind]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(sum(len(m['theorem']) for m in INVENTORY.values()), 118)
        self.assertEqual([len(INVENTORY[m]['theorem']) for m in ('TorusTopology', 'ClosedSuperlevel', 'SuperlevelBar', 'OrdinaryH0',
                                                                  'OrdinaryH0Controls')],
                         [21, 20, 20, 20, 37])
        self.assertEqual(sum(len(m['def']) for m in INVENTORY.values()), 26)
        self.assertEqual([len(INVENTORY[m]['def']) for m in INVENTORY], [6, 6, 3, 7, 4])
        self.assertEqual(sum(len(m['abbrev']) for m in INVENTORY.values()), 6)
        self.assertEqual([len(INVENTORY[m]['abbrev']) for m in INVENTORY], [2, 0, 1, 0, 3])
        self.assertEqual(sum(len(m['instance']) for m in INVENTORY.values()), 3)
        self.assertEqual(sum(len(kind) for m in INVENTORY.values() for kind in m.values()), 153)
        self.assertEqual(sum(len(kind) for kind in INVENTORY['OrdinaryH0Controls'].values()), 44)
        # every declaration of the controls module carries its own prefix, and no other module uses it
        self.assertTrue(all(n.startswith('ordinaryH0Control_') for kind in INVENTORY['OrdinaryH0Controls'].values() for n in kind))
        self.assertFalse(any(n.startswith('ordinaryH0Control_') for m in self.c.MODULES[:-1] for kind in INVENTORY[m].values() for n in kind))
        self.assertEqual(len(INTERNAL_GENERATED), 19)
        self.assertTrue(all(re.fullmatch(self.c.IDENT, n) for n in names))
        self.assertEqual(tuple(INVENTORY), self.c.MODULES)

    def test_source_files_inventory_provenance_and_identities(self):
        meta = self.c.metadata()
        for module in self.c.MODULES:
            self.assertEqual(meta['theorems'][module], INVENTORY[module]['theorem'])
            for kind in ('abbrev', 'def', 'instance'):
                self.assertEqual(meta['definitions'][module][kind], INVENTORY[module][kind])
        self.assertEqual(len(self.c.targets(meta)), 153)
        self.assertEqual(self.c.theorem_targets(meta)[0], 'TorusFiltration.torus_field_latticeVec_formula')
        self.assertEqual(self.c.theorem_targets(meta)[-1], 'TorusFiltration.ordinaryH0Control_parabola_strict_difference_ne_zero')
        prov = meta['provenance']
        self.assertEqual(set(HANDOFF_COMMENTS), set(prov['handoff_comments'].values()))
        self.assertEqual(prov['handoff_pr'], 'd6g8k5htny-coder/Math-#419')
        self.assertIn('OpenAI/Codex', prov['source_author'])
        self.assertIn('Anthropic/Claude', prov['compile_fixes_and_companion'])
        # The C26x successor record: handoff and successor identities, cited comments, honesty labels; and the registered
        # module bytes in the tree ARE the recorded successors (the fixture cannot check this, its modules are placeholders).
        self.assertEqual(set(prov['successors']), set(SUCCESSOR_IDENTITY))
        self.assertEqual(prov['successors'], self.c.SUCCESSORS)
        self.assertEqual(prov['original_bytes'], self.c.ORIGINAL_BYTES)
        self.assertEqual(set(self.c.ORIGINAL_BYTES), set(self.c.ORIGINAL_SHA256))
        for name, (successor, successor_bytes, handoff, handoff_bytes) in SUCCESSOR_IDENTITY.items():
            record = prov['successors'][name]
            self.assertEqual((record['successor_sha256'], record['successor_bytes']), (successor, successor_bytes), name)
            self.assertEqual((record['handoff_sha256'], record['handoff_bytes']), (handoff, handoff_bytes), name)
            key = next(k for k in self.c.ORIGINAL_SHA256 if k.endswith('/' + name))
            self.assertEqual((self.c.ORIGINAL_SHA256[key], self.c.ORIGINAL_BYTES[key]), (handoff, handoff_bytes), name)
            self.assertEqual(set(record['comments'].values()), SUCCESSOR_COMMENTS[name], name)
            self.assertEqual(record['organizational_independence_credit'], 0)
            self.assertTrue(record['formal_status'].startswith('FORMAL_HOLD'), name)
            self.assertIn('OpenAI/Codex', record['source_author'])
            self.assertIn('Anthropic/Claude', record['successor_author'])
            self.assertIn('TorusFiltration', record['namespace'])
            tracked = ROOT / self.c.PACKAGE / name
            if tracked.is_file():
                actual = self.c.identity(tracked.read_bytes())
                self.assertEqual((actual['sha256'], actual['bytes']), (successor, successor_bytes), 'tracked module is not the recorded successor: ' + name)
                self.assertEqual(meta['files'][self.c.PACKAGE + '/' + name]['sha256'], successor, name)
        self.assertEqual(prov['successors']['SuperlevelBar.lean']['imports'], ['Mathlib'])
        self.assertEqual(prov['successors']['OrdinaryH0.lean']['imports'], ['Mathlib', 'ClosedSuperlevel'])
        self.assertIn('ite_eq_left', prov['successors']['SuperlevelBar.lean']['successor_changes'])
        self.assertIn('6113438262', prov['successors']['OrdinaryH0.lean']['successor_changes'])
        self.assertIn('25 constants = 24 user range + 0 user generated + 1 internal generated', prov['successors']['SuperlevelBar.lean']['census_at_pin'])
        self.assertIn('38 constants = 27 user range + 0 user generated + 11 internal generated', prov['successors']['OrdinaryH0.lean']['census_at_pin'])
        self.assertIn('authored directly in namespace TorusFiltration', prov['namespace_mapping'])
        self.assertIn('OrdinaryH0Controls', prov['namespace_mapping'])
        # The owner-authored record: compared whole, its identity is the tracked module's, it cites the item-4 task and the
        # CONTROL_OBLIGATIONS specification, it is not a handoff successor and not a review, and the FORMAL HOLD of
        # OrdinaryH0 is recorded as unchanged; credit 0.
        self.assertEqual(prov['owner_modules'], self.c.OWNER_MODULES)
        self.assertEqual(set(prov['owner_modules']), set(OWNER_IDENTITY))
        self.assertFalse(set(prov['owner_modules']) & set(prov['successors']))
        for name, (digest, size) in OWNER_IDENTITY.items():
            record = prov['owner_modules'][name]
            self.assertEqual((record['sha256'], record['bytes']), (digest, size), name)
            self.assertEqual(set(record['comments'].values()), OWNER_COMMENTS[name], name)
            self.assertEqual(record['organizational_independence_credit'], 0)
            self.assertIn('Anthropic/Claude', record['author'])
            self.assertIn('not a handoff successor', record['kind'])
            self.assertIn('not a review', record['kind'])
            self.assertIn('not a review of OrdinaryH0', record['review_status'])
            self.assertIn('FORMAL HOLD of OrdinaryH0', record['review_status'])
            self.assertIn('unchanged', record['review_status'])
            self.assertEqual(record['imports'], ['Mathlib', 'OrdinaryH0'])
            self.assertIn('48 constants = 44 user range + 0 user generated + 4 internal generated', record['census_at_pin'])
            self.assertEqual(record['declarations'], '37 theorems, 3 abbrevs, 4 defs, 0 instances')
            self.assertNotIn(name, {k.split('/')[-1] for k in self.c.ORIGINAL_SHA256})
            tracked = ROOT / self.c.PACKAGE / name
            if tracked.is_file():
                actual = self.c.identity(tracked.read_bytes())
                self.assertEqual((actual['sha256'], actual['bytes']), (digest, size), 'tracked module is not the recorded owner module: ' + name)
                self.assertEqual(meta['files'][self.c.PACKAGE + '/' + name]['sha256'], digest, name)
        modules = {self.c.PACKAGE + '/' + m + '.lean' for m in self.c.MODULES}
        for path in self.c.REQUIRED_FILES:
            target = ROOT / path
            if target.is_file() and (path in meta['files'] or path not in modules):
                self.assertIn(path, meta['files'], 'present companion file without identity: ' + path)
                self.assertEqual(meta['files'][path], self.c.identity(target.read_bytes()), 'stale identity: ' + path)
            elif not target.is_file():
                self.assertNotIn(path, meta['files'], 'identity listed for an absent file: ' + path)

    def test_lean_modules_match_inventory(self):
        self.assertEqual((SIDE / 'TorusFiltration.lean').read_text(), self.c.ROOT_SOURCE)
        for module in self.c.MODULES:
            path = SIDE / (module + '.lean')
            if not path.is_file():
                self.skipTest('module not yet placed by the integrator: ' + module)
            scan = self.c.scan_module(path.read_text(encoding='utf-8'), module)
            self.assertEqual(scan, INVENTORY[module], module)

    def test_no_admission_tokens_in_comment_stripped_code(self):
        self.assertEqual(self.c.strip_comments('a /- sorry\n axiom -/ b -- native_decide\nc').split(), ['a', 'b', 'c'])
        for path in sorted(SIDE.glob('*.lean')):
            code = self.c.strip_comments(path.read_text(encoding='utf-8'))
            for token in self.c.ADMISSION:
                self.assertIsNone(re.search(r'(?<![A-Za-z0-9_])' + token + r'(?![A-Za-z0-9_])', code), path.name + ': ' + token)

    def test_comment_lexer_follows_lean_comment_rules(self):
        c = self.c
        self.assertEqual(c.strip_comments('x /- a /- nested -/ still comment -/ y').split(), ['x', 'y'])
        self.assertEqual(c.strip_comments('/-- doc -- not a closer -/ x').split(), ['x'])
        self.assertEqual(c.strip_comments('a -- /- not an opener\nb').split(), ['a', 'b'])
        self.assertEqual(c.strip_comments('/-! module\n# heading\ntheorem phantom : False := sorry\n-/\nz').split(), ['z'])
        self.assertEqual(c.strip_comments('/-- one -/\ntheorem a : True := trivial').split(), ['theorem', 'a', ':', 'True', ':=', 'trivial'])
        self.assertEqual(len(c.code_lines('a\n/- b\nc -/\nd')), 4)
        with self.assertRaisesRegex(ValueError, 'comment closer outside a comment'):
            c.strip_comments('a -/ b')
        with self.assertRaisesRegex(ValueError, 'unterminated block comment'):
            c.strip_comments('a /- b')

    def test_module_scan_accepts_only_the_whitelisted_shapes(self):
        good = placeholder_module('ClosedSuperlevel')
        inventory = INVENTORY['ClosedSuperlevel']
        prelude = ('import Mathlib\nimport Mathlib.Topology.Basic\nimport TorusTopology\n\nnoncomputable section\n\n'
                   'open CategoryTheory Topology\nopen scoped Simplicial\n\n'
                   'universe w v u\n\nnamespace TorusFiltration\n/-- Control: a docstring\nwith a column-0 continuation line '
                   'mentioning theorem and sorry -/\nvariable {C : Type u} [Category.{v} C]\n    [Preadditive C] [CategoryWithHomology C]\n')
        for text in (good, good + '-- sorry in a comment is text\n',
                     good.replace('import Mathlib\n', 'import Mathlib\n/-! theorem phantom : False := by native_decide -/\n'),
                     good.replace('namespace TorusFiltration', prelude.split('\n\nnamespace TorusFiltration\n')[0] + '\n\nnamespace TorusFiltration\n'
                                  + prelude.split('\n\nnamespace TorusFiltration\n')[1]),
                     good.replace(':= trivial', ':= by\n  exact trivial\n', 1),
                     good.replace('noncomputable def superlevel_set : Nat := 0', 'def superlevel_set : Nat :=\n  0 -- indented body'),
                     good.replace('theorem superlevel_mono : True := trivial', 'theorem superlevel_mono\n    (h : True) : True := h')):
            with self.subTest(text=text[-80:]):
                self.assertEqual(self.c.scan_module(text, 'ClosedSuperlevel'), inventory)
        # Since the C263/C264 registration: a companion module may import the companion modules listed before it in
        # MODULES (OrdinaryH0.lean imports ClosedSuperlevel), and `open scoped <Namespaces>` is a prelude line
        # (OrdinaryH0.lean opens the scoped simplicial notation). Only those; see the refusals below.
        h0 = placeholder_module('OrdinaryH0')
        for text in (h0.replace('import Mathlib\n', 'import Mathlib\nimport ClosedSuperlevel\n', 1),
                     h0.replace('import Mathlib\n', 'import Mathlib\nimport TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\n', 1),
                     h0.replace('import Mathlib\n', 'import Mathlib\nopen scoped Simplicial\n', 1),
                     h0.replace('import Mathlib\n', 'import Mathlib\nopen scoped Simplicial CategoryTheory.Limits\n', 1)):
            self.assertEqual(self.c.scan_module(text, 'OrdinaryH0'), INVENTORY['OrdinaryH0'])
        # OrdinaryH0Controls.lean imports OrdinaryH0 (and may import any module before it)
        controls = placeholder_module('OrdinaryH0Controls')
        for text in (controls.replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0\n', 1),
                     controls.replace('import Mathlib\n', 'import Mathlib\nimport ClosedSuperlevel\nimport OrdinaryH0\n', 1)):
            self.assertEqual(self.c.scan_module(text, 'OrdinaryH0Controls'), INVENTORY['OrdinaryH0Controls'])
        self.assertEqual(self.c.MODULES, ('TorusTopology', 'ClosedSuperlevel', 'SuperlevelBar', 'OrdinaryH0', 'OrdinaryH0Controls'))

    def test_module_scan_refuses_admissions_and_unexpected_kinds(self):
        good = placeholder_module('ClosedSuperlevel')

        def inject(line):
            return good.replace('\nend TorusFiltration', '\n' + line + '\nend TorusFiltration')
        unexpected = 'unexpected column-0 line in ClosedSuperlevel:'
        command = 'command token outside a column-0 declaration in ClosedSuperlevel:'
        cases = [
            (good.replace(':= trivial', ':= by sorry', 1), 'admission token in ClosedSuperlevel: sorry'),
            (good.replace(':= trivial', ':= sorryAx _ false', 1), 'admission token in ClosedSuperlevel: sorryAx'),
            (good.replace(':= trivial', ':= by native_decide', 1), 'admission token in ClosedSuperlevel: native_decide'),
            (good.replace(':= trivial', ':= by\n  skipKernelTC', 1), 'admission token in ClosedSuperlevel: skipKernelTC'),
            (good.replace(':= trivial', ':= Lean.ofReduceBool _ _ rfl', 1), 'admission token in ClosedSuperlevel: ofReduceBool'),
            (inject('axiom hidden : False'), 'admission token in ClosedSuperlevel: axiom'),
            (inject('opaque hidden : Nat := 0'), 'admission token in ClosedSuperlevel: opaque'),
            (inject('unsafe def hidden : Nat := 0'), 'admission token in ClosedSuperlevel: unsafe'),
            (inject('partial def hidden : Nat := 0'), 'admission token in ClosedSuperlevel: partial'),
            (inject('set_option autoImplicit true'), 'admission token in ClosedSuperlevel: autoImplicit'),
            (inject('@[simp] theorem extra_hidden : True := trivial'), unexpected),
            (inject('private theorem hidden : True := trivial'), unexpected),
            (inject('protected def hidden : Nat := 0'), unexpected),
            (inject('noncomputable instance hidden : Inhabited Nat := ⟨0⟩'), unexpected),
            (inject('scoped macro_rules | `(tactic| foo) => `(tactic| trivial)'), unexpected),
            (inject('macro_rules | `(tactic| foo) => `(tactic| trivial)'), unexpected),
            (inject('local instance : Inhabited Nat := ⟨0⟩'), unexpected),
            (inject('attribute [simp] superlevel_set'), unexpected),
            (inject('set_option maxHeartbeats 0'), unexpected),
            (inject('set_option maxHeartbeats 0 in'), unexpected),
            (inject('section\n  theorem indented_hidden : True := trivial\nend'), unexpected),
            (inject('  theorem indented_hidden : True := trivial'), command),
            (good.replace('namespace TorusFiltration\n', 'namespace TorusFiltration\n  alias hidden := Nat.add_comm\n'), command),
            (inject('theorem a_hidden : True := trivial alias hidden := Nat.add_comm'), command),
            (inject('alias hidden := Nat.add_comm'), unexpected),
            (inject('  irreducible_def hidden : Nat := 0'), command),
            (inject('  simproc hidden (Nat.succ _) := fun _ => return .continue'), command),
            (inject('  notation3 hidden => Nat.zero'), command),
            (inject('  run_meta pure ()'), command),
            (inject('  mk_iff_of_inductive_prop Nat.le hidden'), command),
            (inject('  cbv_simproc hidden (Nat.succ _) := fun _ => return .continue'), command),
            (inject('  builtin_simproc_decl hidden (Nat.succ _) := fun _ => return .continue'), command),
            (inject('  add_aesop_rules safe hidden'), command),
            (inject('  register_label_attr hidden'), command),
            (inject('  grind_propagator hidden ↓Nat.le := fun _ => pure ()'), command),
            (inject('  declare_uint_theorems Nat'), command),
            (inject('  name_poly_vars X over Nat'), command),
            (inject('  with_weak_namespace Hidden theorem hidden : True := trivial'), command),
            (inject('  meta def hidden : Nat := 0'), command),
            (inject('  public theorem hidden : True := trivial'), command),
            (inject('  aux_def hidden : Nat := 0'), command),
            (inject('  lrat_proof hidden "p cnf 1 1 1 0" "1 0"'), 'string literal in code: ClosedSuperlevel:'),
            (inject('  lrat_proof hidden'), command),
            # lexical splices found by the verification of the G2 repair: a closed block comment is a token separator
            # (as in Lean), and a numeral ends at the first non-digit, so `0alias` is `0` then the keyword
            (inject('  theorem/- -/hidden : True := trivial'), command),
            (inject('  alias/- -/hidden := Nat.add_comm'), command),
            (inject('theorem a_hidden : True := trivial theorem/- -/b_hidden : True := trivial'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0alias hidden := Nat.add_comm'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0theorem hidden : True := trivial'), command),
            (good.replace(':= trivial', ':= by\n  exact/- -/sorry', 1), 'admission token in ClosedSuperlevel: sorry'),
            # Lean's non-decimal numerals end where Lean ends them (hex, binary, octal, exponent, `_` separators)
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0x1Ftheorem hidden : True := trivial'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 1e5theorem hidden : True := trivial'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 1_0theorem hidden : True := trivial'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0o7instance hidden : Inhabited Nat := ⟨0⟩'), command),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0b1axiom hidden : False'), 'admission token in ClosedSuperlevel: axiom'),
            (good.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0x1Fset_option maxHeartbeats 0'), command),
            (inject('  reprove superlevel_mono by trivial'), command),
            (inject('  declare_aesop_exception hidden'), command),
            (inject('  seal superlevel_set'), command),
            (inject('  unset_option maxHeartbeats'), command),
            (good.replace(':= trivial', ':= by/- -/native_decide', 1), 'admission token in ClosedSuperlevel: native_decide'),
            (inject('  unif_hint (x : Nat) where ⊢ x =?= x'), command),
            (inject('  recall superlevel_set : Nat := 0'), command),
            (inject('  add_decl_doc superlevel_set'), command),
            (inject('  nonrec def hidden : Nat := 0'), command),
            (inject('theorem a_hidden : True := trivial theorem b_hidden : True := trivial'), command),
            (inject('theorem a_hidden : True := by\n  open Classical in exact trivial'), command),
            (inject('variable (h : False) in theorem hidden : True := trivial'), command),
            (inject('universe z in'), command),
            (inject('open Classical in'), unexpected),
            (inject('macro foo : tactic => `(tactic| trivial)'), unexpected),
            (inject('elab foo : term => pure (mkConst ``True)'), unexpected),
            (inject('syntax foo : tactic'), unexpected),
            (inject('notation x ⊕ y => x'), unexpected),
            (inject('lemma extra : True := trivial'), unexpected),
            (inject('example : True := trivial'), unexpected),
            (inject('structure Hidden where\n  x : Nat'), unexpected),
            (inject('inductive Hidden | a'), unexpected),
            (inject('class Hidden (α : Type) where\n  k : α'), unexpected),
            (inject('instance : Inhabited Nat := ⟨0⟩'), unexpected),
            (inject('mutual\ntheorem a_hidden : True := trivial\nend'), unexpected),
            (inject('deriving instance Repr for Nat'), unexpected),
            (inject('#eval 1'), unexpected),
            (inject('#print axioms superlevel_set'), unexpected),
            (inject('export Nat (succ)'), unexpected),
            (inject('include h'), unexpected),
            (inject('run_cmd pure ()'), unexpected),
            (inject('initialize hidden : Nat ← pure 0'), unexpected),
            (inject('import Hidden'), unexpected),
            (inject('import Mathlib'), 'import inside the namespace: ClosedSuperlevel:'),
            (inject('import TorusTopology'), 'import inside the namespace: ClosedSuperlevel:'),
            # companion imports: only modules BEFORE this one in MODULES, never itself, a later module or the root
            (good.replace('import Mathlib\n', 'import Mathlib\nimport ClosedSuperlevel\n', 1), 'companion import out of dependency order in ClosedSuperlevel:2: ClosedSuperlevel'),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport SuperlevelBar\n', 1), 'companion import out of dependency order in ClosedSuperlevel:2: SuperlevelBar'),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0\n', 1), 'companion import out of dependency order in ClosedSuperlevel:2: OrdinaryH0'),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0Controls\n', 1), 'companion import out of dependency order in ClosedSuperlevel:2: OrdinaryH0Controls'),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport TorusFiltration\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport TorusTopology.Hidden\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nimport TorusTopology Hidden\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import TorusTopology\n', 1).replace('namespace TorusFiltration\n', 'namespace TorusFiltration\nimport Mathlib\n'), 'import inside the namespace: ClosedSuperlevel:'),
            # `open scoped`: capitalized namespaces only, nothing else on the line, column 0 only
            (good.replace('import Mathlib\n', 'import Mathlib\nopen scoped simplicial\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nopen scoped\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nopen scoped Simplicial in\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nopen scoped Simplicial theorem hidden : True := trivial\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\n  open scoped Simplicial\n', 1), command),
            (good.replace('import Mathlib\n', 'import Mathlib\nopen  scoped Simplicial\n', 1), unexpected),
            (good.replace('import Mathlib\n', 'import Mathlib\nopen scoped  Simplicial\n', 1), unexpected),
            (inject("theorem hidden' : True := trivial"), unexpected),
            (inject('theorem hidden.name : True := trivial'), unexpected),
            (inject('theorem'), unexpected),
            (inject('end'), unexpected),
            (inject('noncomputable section extra'), unexpected),
            (inject('variable'), unexpected),
            (inject('variable (h : True)\n  (h2 : True) in theorem hidden : True := trivial'), command),
            (inject('def s : String := "x"'), 'string literal in code: ClosedSuperlevel:'),
            (inject('def s : String := "/-"\ndef t : String := "-/"'), 'string literal in code: ClosedSuperlevel:'),
            (inject('theorem a_hidden : True := trivial -- fine\n  @[simp] theorem b_hidden : True := trivial'), command),
            (inject('theorem a_hidden : True := by\n  simp #[1]'), 'attribute or #-command in ClosedSuperlevel:'),
            (good.replace('namespace TorusFiltration', 'namespace ResearchFormalCoreR1'), 'handoff namespace left in place: ClosedSuperlevel'),
            (good.replace('namespace TorusFiltration', ''), 'declaration outside namespace TorusFiltration: ClosedSuperlevel:'),
            (good.replace('namespace TorusFiltration\n', 'namespace TorusFiltration\nnamespace TorusFiltration\n'), 'namespace declaration: ClosedSuperlevel:'),
            (good.replace('end TorusFiltration', ''), 'namespace TorusFiltration not opened and closed exactly once: ClosedSuperlevel'),
            (good + 'theorem after_end : True := trivial\n', 'code after end TorusFiltration: ClosedSuperlevel:'),
            (good + '-/\n', 'comment closer outside a comment'),
            (good + '/- open forever\n', 'unterminated block comment'),
            (good.replace('import Mathlib', 'theorem early : True := trivial\nimport Mathlib'), 'declaration outside namespace TorusFiltration'),
        ]
        self.assertEqual(self.c.scan_module(good, 'ClosedSuperlevel'), INVENTORY['ClosedSuperlevel'])
        for text, message in cases:
            with self.subTest(message=message, text=text[-70:]), self.assertRaisesRegex(ValueError, re.escape(message)):
                self.c.scan_module(text, 'ClosedSuperlevel')
        # The first module may import nothing but Mathlib; a module name outside MODULES is not scanned at all.
        with self.assertRaisesRegex(ValueError, 'companion import out of dependency order in TorusTopology:2: ClosedSuperlevel'):
            self.c.scan_module(placeholder_module('TorusTopology').replace('import Mathlib\n', 'import Mathlib\nimport ClosedSuperlevel\n', 1), 'TorusTopology')
        # The controls module comes last: OrdinaryH0 may not import it, nor may it import itself or the root.
        with self.assertRaisesRegex(ValueError, 'companion import out of dependency order in OrdinaryH0:2: OrdinaryH0Controls'):
            self.c.scan_module(placeholder_module('OrdinaryH0').replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0Controls\n', 1), 'OrdinaryH0')
        with self.assertRaisesRegex(ValueError, 'companion import out of dependency order in OrdinaryH0Controls:2: OrdinaryH0Controls'):
            self.c.scan_module(placeholder_module('OrdinaryH0Controls').replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0Controls\n', 1), 'OrdinaryH0Controls')
        with self.assertRaisesRegex(ValueError, 'unexpected column-0 line in OrdinaryH0Controls:2: import TorusFiltration'):
            self.c.scan_module(placeholder_module('OrdinaryH0Controls').replace('import Mathlib\n', 'import Mathlib\nimport TorusFiltration\n', 1), 'OrdinaryH0Controls')
        with self.assertRaisesRegex(ValueError, 'not a companion module: TorusFiltration'):
            self.c.scan_module(good, 'TorusFiltration')
        with self.assertRaisesRegex(ValueError, 'not a companion module: Other'):
            self.c.scan_module(good, 'Other')
        # Every command keyword the scanner knows is refused somewhere other than the start of a whitelisted line,
        # indented after the namespace opening included (the C262 G2 position).
        for keyword in self.c.COMMANDS:
            with self.subTest(keyword=keyword), self.assertRaises(ValueError):
                self.c.scan_module(inject('theorem k_hidden : True := trivial ' + keyword), 'ClosedSuperlevel')
            with self.subTest(keyword=keyword, position='indented after namespace'), self.assertRaises(ValueError):
                self.c.scan_module(good.replace('namespace TorusFiltration\n', 'namespace TorusFiltration\n  ' + keyword + ' hidden\n'), 'ClosedSuperlevel')
        # Identifiers that merely contain a keyword, or dotted components, are not keywords (no false refusal).
        for text in (good.replace(':= trivial', ':= (fun (_ : Foo.alias = 0) => trivial) rfl', 1),
                     good.replace(':= trivial', ':= (fun (foo2alias : True) => foo2alias) trivial', 1),
                     good.replace(':= trivial', ':= (fun (alias_like theorem_like : True) => theorem_like) trivial trivial', 1),
                     good.replace(':= trivial', ':= (Classical.byContradiction fun h => h trivial)', 1)):
            self.assertEqual(self.c.scan_module(text, 'ClosedSuperlevel'), INVENTORY['ClosedSuperlevel'])
        # A `where` clause adds a dotted auxiliary declaration that no keyword list refuses: the scanner accepts it
        # and the elaborated census (Census.lean, `finish`) is what refuses it. Recorded here so the boundary is explicit.
        where_clause = good.replace('theorem superlevel_mono : True := trivial', 'theorem superlevel_mono : True := trivial\n  where hidden : True := trivial')
        self.assertEqual(self.c.scan_module(where_clause, 'ClosedSuperlevel'), INVENTORY['ClosedSuperlevel'])


class ParserControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = checker()

    def test_negative_false_controls_accept_only_the_intended_diagnostic(self):
        for control in self.c.FALSE_CONTROLS:
            good = FALSE_LOG.format(control)
            self.assertEqual(self.c.negative(good, control, 1), 'REJECTED_BY_LEAN')
            for bad, status in [(good, 0), (good, 2), (good, True), (good, '1'), (good.replace('False', 'True'), 1),
                                (good.replace(control, 'Other'), 1), (good + 'error: unknown identifier\n', 1),
                                ('Traceback: bad runtime\n', 1), ('error: unsolved goals\n', 1), ('', 1),
                                ('warning: declaration uses `sorry`\n' + good, 1)]:
                with self.subTest(control=control, bad=bad, status=status), self.assertRaises(ValueError):
                    self.c.negative(bad, control, status)
        with self.assertRaises(ValueError):
            self.c.negative(FALSE_LOG.format('Unknown'), 'Unknown', 1)

    def test_item4_controls_accept_their_pinned_logs_and_refuse_their_true_siblings(self):
        # The C264 item-4 controls: the diagnostics Lean printed for each control are accepted, and the diagnostics of the
        # same tactic on each control's true sibling statement (same file name, same exit status 1) are refused, as are
        # each control's log under another control's name and under a non-1 status.
        self.assertEqual(set(CONTROL_LOGS), set(DISCRIMINATOR_LOGS))
        self.assertTrue(set(CONTROL_LOGS) <= set(self.c.FALSE_CONTROLS))
        for control, log in CONTROL_LOGS.items():
            self.assertEqual(self.c.negative(log, control, 1), 'REJECTED_BY_LEAN')
            for status in (0, 2):
                with self.subTest(control=control, status=status), self.assertRaisesRegex(ValueError, 'false-statement control must exit exactly one'):
                    self.c.negative(log, control, status)
            for other in CONTROL_LOGS:
                if other != control:
                    with self.subTest(control=control, other=other), self.assertRaisesRegex(ValueError, 'not the intended False-goal diagnostic: ' + other):
                        self.c.negative(log, other, 1)
        for control, log in DISCRIMINATOR_LOGS.items():
            self.assertNotIn('⊢ False', log)
            with self.subTest(discriminator=control), self.assertRaisesRegex(ValueError, 'not the intended False-goal diagnostic: ' + control):
                self.c.negative(log, control, 1)

    def test_negative_injection_controls_require_the_audit_to_refuse(self):
        for control, (_, forbidden, _) in self.c.INJECTIONS.items():
            good = good_injection_log(self.c, control)
            self.assertEqual(self.c.negative(good, control, 0), 'REJECTED_BY_AXIOM_AUDIT')
            escaped = good.replace(forbidden, 'propext')
            for bad, status in [(good, 1), (good, 2), (escaped, 0), (good.replace('injected', 'other'), 0),
                                (good + 'extra\n', 0), ('', 0), (good.replace('[' + forbidden + ']', '[]'), 0),
                                (good.replace("'injected' depends", "'injected' does not depend"), 0)]:
                with self.subTest(control=control, bad=bad, status=status), self.assertRaises(ValueError):
                    self.c.negative(bad, control, status)
        sorry_log = good_injection_log(self.c, 'RejectSorry')
        with self.assertRaises(ValueError):
            self.c.negative(sorry_log.replace('`sorry`', "'sorry'"), 'RejectSorry', 0)
        with self.assertRaises(ValueError):
            self.c.negative(INJECTED.format('sorryAx'), 'RejectSorry', 0)
        with self.assertRaises(ValueError):
            self.c.negative(SORRY_WARNING + INJECTED.format('hiddenPremise'), 'RejectCustomAxiom', 0)

    def test_negative_injection_second_refusal_follows_the_audit_rules(self):
        # Behind the regex pin, negative() also requires audit_axioms itself to refuse the injected line for the
        # intended reason; widening ALLOWED (resolved at call time) must turn the control into an escape.
        c = self.c
        saved = c.ALLOWED
        try:
            c.ALLOWED = frozenset(saved | {'sorryAx'})
            with self.assertRaisesRegex(ValueError, 'negative control escaped the axiom audit: RejectSorry'):
                c.negative(good_injection_log(c, 'RejectSorry'), 'RejectSorry', 0)
            self.assertEqual(c.negative(good_injection_log(c, 'RejectCustomAxiom'), 'RejectCustomAxiom', 0),
                             'REJECTED_BY_AXIOM_AUDIT')
        finally:
            c.ALLOWED = saved
        self.assertEqual(c.negative(good_injection_log(c, 'RejectSorry'), 'RejectSorry', 0), 'REJECTED_BY_AXIOM_AUDIT')

    def test_audit_axioms_rules(self):
        names = ['TorusFiltration.a', 'TorusFiltration.b', 'TorusFiltration.c']
        good = ("'TorusFiltration.a' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
                "'TorusFiltration.b' depends on axioms: [propext]\n'TorusFiltration.c' does not depend on any axioms\n")
        self.assertEqual(self.c.audit_axioms(good, names),
                         {'TorusFiltration.a': ['Classical.choice', 'Quot.sound', 'propext'],
                          'TorusFiltration.b': ['propext'], 'TorusFiltration.c': []})
        for bad, message in ((good.replace('[propext]', '[propext, sorryAx]'), 'forbidden transitive axiom'),
                             (good.replace('[propext]', '[Lean.ofReduceBool]'), 'forbidden transitive axiom'),
                             (good.replace('TorusFiltration.b', 'TorusFiltration.unknown'), 'unexpected or duplicate axiom target'),
                             (good.replace("'TorusFiltration.b' depends on axioms: [propext]\n", ''), 'missing target axiom report'),
                             (good + "'TorusFiltration.a' depends on axioms: [propext]\n", 'unexpected or duplicate axiom target'),
                             ('warning: something\n' + good, 'unrecognized audit output'),
                             (good.replace('[propext]', '[prop ext]'), 'malformed axiom name'),
                             (good.replace('[propext]', '[propext,]'), 'malformed axiom name'),
                             (good.replace('[propext]', '[hiddenPremise]'), 'forbidden transitive axiom')):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, message):
                self.c.audit_axioms(bad, names)
        for targets in ([], ['TorusFiltration.a', 'TorusFiltration.a'], 'TorusFiltration.a'):
            with self.subTest(targets=targets), self.assertRaisesRegex(ValueError, 'empty or duplicate target list'):
                self.c.audit_axioms(good, targets)
        duplicated = {'theorems': {m: ['a'] if m in self.c.MODULES[:2] else [] for m in self.c.MODULES},
                      'definitions': {m: {'abbrev': [], 'def': [], 'instance': []} for m in self.c.MODULES}}
        with self.assertRaisesRegex(ValueError, 'duplicate or empty target list'):
            self.c.targets(duplicated)
        duplicated['theorems'] = {m: [] for m in self.c.MODULES}
        with self.assertRaisesRegex(ValueError, 'duplicate or empty target list'):
            self.c.targets(duplicated)

    def test_types_rules(self):
        names = ['TorusFiltration.a', 'TorusFiltration.b']
        good = 'TorusFiltration.a : True\nTorusFiltration.b (d : ℕ) :\n  ∀ x, x = x\n'
        self.assertEqual(self.c.types(good, names), names)
        for bad, message in (('TorusFiltration.a : True\n', 'type inventory mismatch'),
                             (good + 'TorusFiltration.c : True\n', 'type inventory mismatch'),
                             ('TorusFiltration.a : True\nTorusFiltration.a : True\n', 'type inventory mismatch'),
                             ('TorusFiltration.b : True\nTorusFiltration.a : True\n', 'type inventory mismatch'),
                             ('error: crash\n' + good, 'type diagnostic'), (good + 'error: crash\n', 'type diagnostic'),
                             ('warning: lint\n' + good, 'type diagnostic'), (good + 'warning: lint\n', 'type diagnostic'),
                             ('preamble\n' + good, 'unrecognized type preamble')):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, message):
                self.c.types(bad, names)

    def test_lean_version_and_packages(self):
        self.assertEqual(self.c.lean_version(LEAN_VERSION_LINE), LEAN_VERSION_LINE.strip())
        for bad in (LEAN_VERSION_LINE.replace('4.34.1', '4.34.0'), LEAN_VERSION_LINE.replace('5045d0056', '5045d005'),
                    LEAN_VERSION_LINE.replace('Release', 'Debug'), LEAN_VERSION_LINE + 'extra\n', ''):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.c.lean_version(bad)
        expected = {'mathlib': 'd1' * 20, 'batteries': 'f2' * 20}
        good = 'batteries %s\nmathlib %s\n' % ('f2' * 20, 'd1' * 20)
        self.assertEqual(self.c.packages(good, expected), expected)
        for bad in ('mathlib %s\n' % ('d1' * 20), good + 'aesop %s\n' % ('a3' * 20), good.replace('d1' * 20, 'e1' * 20),
                    good + 'mathlib %s\n' % ('d1' * 20), good.replace('\nmathlib', '\n mathlib'), 'mathlib short\n'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.c.packages(bad, expected)

    def test_leanchecker_mode_accepts_exactly_the_two_recorded_invocations(self):
        self.assertEqual(self.c.leanchecker_mode(LEANCHECKER_MODULES + '\n'), 'modules')
        self.assertEqual(self.c.leanchecker_mode(LEANCHECKER_FRESH + '\n'), 'fresh')
        self.assertEqual(self.c.LEANCHECKER, {LEANCHECKER_MODULES: 'modules', LEANCHECKER_FRESH: 'fresh'})
        for bad in ('', 'leanchecker TorusFiltration', 'leanchecker --fresh TorusTopology', 'leanchecker TorusTopology ClosedSuperlevel',
                    LEANCHECKER_MODULES_BEFORE_C26X, 'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0',
                    LEANCHECKER_MODULES_BEFORE_CONTROLS, LEANCHECKER_MODULES_BEFORE_CONTROLS + ' OrdinaryH0Controls',
                    'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0 OrdinaryH0Controls',
                    'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0Controls OrdinaryH0 TorusFiltration',
                    'leanchecker OrdinaryH0Controls',
                    'leanchecker TorusTopology ClosedSuperlevel SuperlevelBar TorusFiltration',
                    'leanchecker TorusTopology ClosedSuperlevel OrdinaryH0 SuperlevelBar TorusFiltration',
                    LEANCHECKER_MODULES + ' Extra', 'leanchecker --verbose ' + LEANCHECKER_MODULES[12:],
                    'lean ' + LEANCHECKER_MODULES[12:], LEANCHECKER_MODULES + '\n' + LEANCHECKER_FRESH):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, 'unrecognized leanchecker invocation'):
                self.c.leanchecker_mode(bad)

    def test_emit_writes_exactly_the_audit_types_positive_and_controls(self):
        meta = self.c.metadata()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.c.emit(out)
            self.assertEqual({p.name for p in out.iterdir()}, set(EMITTED))
            self.assertEqual({p.name for p in out.iterdir()},
                             {'Audit.lean', 'Types.lean', 'Positive.lean', 'Census.lean'} | {n + '.lean' for n in self.c.CONTROLS})
            census = (out / 'Census.lean').read_text()
            self.assertTrue(census.startswith('import TorusFiltration\n'))
            for needed in ('isInternalDetail', 'findDeclarationRanges?', 'getModuleIdxFor?', '`TorusTopology', '`ClosedSuperlevel',
                           '`SuperlevelBar, `OrdinaryH0, `OrdinaryH0Controls, `TorusFiltration', 'CENSUS_END', '"internal" else "user"',
                           '"range" else "generated"'):
                self.assertIn(needed, census)
            self.assertIn('#[`TorusTopology, `ClosedSuperlevel, `SuperlevelBar, `OrdinaryH0, `OrdinaryH0Controls, `TorusFiltration]', census)
            audit = (out / 'Audit.lean').read_text().splitlines()
            self.assertEqual(audit[0], 'import TorusFiltration')
            self.assertEqual(audit[1:], ['#print axioms ' + n for n in self.c.targets(meta)])
            self.assertEqual(len(audit[1:]), 153)
            types = (out / 'Types.lean').read_text().splitlines()
            self.assertEqual(types[:2], ['import TorusFiltration', 'set_option pp.explicit true'])
            self.assertEqual(types[2:], ['#check ' + n for n in self.c.theorem_targets(meta)])
            positive = (out / 'Positive.lean').read_text()
            self.assertTrue(positive.startswith('import TorusFiltration\n'))
            self.assertTrue(3 <= len(re.findall(r'^example', positive, re.M)) <= 6)
            for token in ('sorry', 'admit', 'axiom', 'native_decide'):
                self.assertIsNone(re.search(r'\b' + token + r'\b', positive))
            for control in self.c.CONTROLS:
                text = (out / (control + '.lean')).read_text()
                self.assertTrue(text.startswith('import TorusFiltration\n'), control)
                self.assertEqual('sorry' in text, control == 'RejectSorry')
                self.assertEqual('axiom hiddenPremise' in text, control == 'RejectCustomAxiom')
                self.assertEqual('native_decide' in text, control == 'RejectNativeDecide')
                if control in self.c.FALSE_CONTROLS:
                    self.assertIn('example : ' + self.c.FALSE_CONTROLS[control][0] + ' := by', text)
                else:
                    self.assertIn('#print axioms injected', text)
        self.assertEqual(set(self.c.FALSE_CONTROLS) | set(self.c.INJECTIONS), set(self.c.CONTROLS))
        self.assertGreaterEqual(len(self.c.FALSE_CONTROLS), 1)
        # One false control per module at least, each naming one of that module's own definitions (the C26x controls
        # name superlevelBar_deathHeight and ordinaryH0_pointClass, the item-4 controls the fixtures of OrdinaryH0Controls);
        # none of them is proved by a hypothesis-free `rfl`.
        item4 = ('RejectMergerKillsPointClass', 'RejectSeparationWithoutNonzeroCoeff', 'RejectNonmergerKillsDifference')
        for prefix, names in (('superlevel_', ('RejectSuperlevelSignFlip', 'RejectSuperlevelBelowThreshold')),
                              ('torus_', ('RejectConstantNotPeriodic',)), ('superlevelBar_', ('RejectEssentialDeathBound',)),
                              ('ordinaryH0_', ('RejectReducedPointClass',) + item4), ('ordinaryH0Control_', item4)):
            for name in names:
                self.assertIn(prefix, self.c.FALSE_CONTROLS[name][0], name)
        # The item-4 controls, exactly: each tactic rewrites with the true fixture theorem the statement contradicts.
        self.assertEqual(self.c.FALSE_CONTROLS['RejectMergerKillsPointClass'], (
            'CategoryTheory.CategoryStruct.comp (ordinaryH0_pointClass (TopCat.of Bool) ordinaryH0Control_intCoeff true) '
            '(((AlgebraicTopology.singularHomologyFunctor (ModuleCat.{0} ℤ) 0).obj ordinaryH0Control_intCoeff).map ordinaryH0Control_collapse) = 0',
            'simp only [ordinaryH0Control_collapse_image_ne_zero]'))
        self.assertEqual(self.c.FALSE_CONTROLS['RejectSeparationWithoutNonzeroCoeff'], (
            'ordinaryH0_pointClass (TopCat.of Bool) ordinaryH0Control_zeroCoeff true ≠ ordinaryH0_pointClass (TopCat.of Bool) ordinaryH0Control_zeroCoeff false',
            'simp [ordinaryH0Control_bool_zeroCoeff_eq]'))
        self.assertEqual(self.c.FALSE_CONTROLS['RejectNonmergerKillsDifference'], (
            'CategoryTheory.CategoryStruct.comp (ordinaryH0_pointClass (TopCat.of (Bool × Bool)) ordinaryH0Control_intCoeff ((true, false) : Bool × Bool) '
            '- ordinaryH0_pointClass (TopCat.of (Bool × Bool)) ordinaryH0Control_intCoeff ((false, true) : Bool × Bool)) '
            '(((AlgebraicTopology.singularHomologyFunctor (ModuleCat.{0} ℤ) 0).obj ordinaryH0Control_intCoeff).map ordinaryH0Control_fst) = 0',
            'simp only [ordinaryH0Control_fst_difference_ne_zero]'))
        for name in item4:
            lemma = self.c.FALSE_CONTROLS[name][1].split('[')[1].rstrip(']')
            self.assertIn(lemma, INVENTORY['OrdinaryH0Controls']['theorem'], name)
        self.assertEqual(self.c.FALSE_CONTROLS['RejectEssentialDeathBound'],
                         ('superlevelBar_deathHeight (fun _ : superlevelBar_E 1 => (-1 : ℝ)) 0 ≤ (-1 : ℝ)', 'norm_num [superlevelBar_death_const]'))
        self.assertEqual(self.c.FALSE_CONTROLS['RejectReducedPointClass'][1], 'simp [ordinaryH0_pointClass_augmentation]')
        self.assertIn('ordinaryH0_pointClass (TopCat.of Unit) (ModuleCat.of ℤ ℤ) ()', self.c.FALSE_CONTROLS['RejectReducedPointClass'][0])
        self.assertIn('≠ CategoryTheory.CategoryStruct.id (ModuleCat.of ℤ ℤ)', self.c.FALSE_CONTROLS['RejectReducedPointClass'][0])
        self.assertEqual(list(self.c.CONTROLS), ['RejectSuperlevelSignFlip', 'RejectSuperlevelBelowThreshold', 'RejectConstantNotPeriodic',
                                                 'RejectEssentialDeathBound', 'RejectReducedPointClass', 'RejectMergerKillsPointClass',
                                                 'RejectSeparationWithoutNonzeroCoeff', 'RejectNonmergerKillsDifference', 'RejectSorry',
                                                 'RejectCustomAxiom', 'RejectNativeDecide'])
        self.assertEqual(len(self.c.EVIDENCE_FILES), 65)
        self.assertEqual(self.c.BUILDS, ('build-TorusTopology', 'build-ClosedSuperlevel', 'build-SuperlevelBar', 'build-OrdinaryH0',
                                         'build-OrdinaryH0Controls', 'build-TorusFiltration', 'positive', 'axioms', 'types', 'census',
                                         'leanchecker'))
        self.assertEqual(self.c.ROOT_SOURCE, 'import TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\nimport OrdinaryH0\n'
                                             'import OrdinaryH0Controls\n')
        self.assertEqual({v[1] for v in self.c.INJECTIONS.values()},
                         {'sorryAx', 'hiddenPremise', 'injected._native.native_decide.ax_1_1'})
        self.assertTrue(all(re.fullmatch(self.c.NAME, v[1]) and v[1] not in self.c.ALLOWED for v in self.c.INJECTIONS.values()))


class WorkflowAndReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = checker()
        cls.workflow = (ROOT / cls.c.WORKFLOW).read_text()
        cls.replay = (SIDE / 'replay.sh').read_text()
        cls.d2 = (ROOT / '.github/workflows/d2-moment-bridge.yml').read_text()

    def paths(self, event):
        marker = '  ' + event + ':\n'
        self.assertEqual(self.workflow.count(marker), 1, event)
        rest = self.workflow.split(marker, 1)[1]
        ends = [i for i in (rest.find('\n  push:\n'), rest.find('\n  workflow_dispatch:\n')) if i >= 0]
        block = rest[:min(ends)]
        self.assertEqual(block.count('    paths:\n'), 1, event)
        return re.findall(r"^      - '([^']+)'$", block, re.M)

    def test_path_triggers_exclude_the_core_tree(self):
        expected = ['companions/torus_filtration_20261011/**', '.github/workflows/torus-filtration.yml',
                    'formal/lakefile.toml', 'formal/lake-manifest.json', 'formal/lean-toolchain']
        self.assertEqual(self.paths('pull_request'), expected)
        self.assertEqual(self.paths('push'), expected)
        self.assertNotIn("'formal/**'", self.workflow)
        self.assertIn('    branches: [main]\n', self.workflow)
        self.assertIn('  workflow_dispatch:\n', self.workflow)
        self.assertIn('permissions:\n  contents: read\n', self.workflow)

    def test_action_pins_match_the_d2_companion_workflow(self):
        for action in ('actions/checkout@', 'leanprover/lean-action@', 'actions/upload-artifact@'):
            mine = re.findall(re.escape(action) + r'([0-9a-f]{40})', self.workflow)
            theirs = re.findall(re.escape(action) + r'([0-9a-f]{40})', self.d2)
            self.assertEqual(len(mine), 1, action)
            self.assertEqual(mine, theirs, action)
        for required in ('lake-package-directory: formal', "use-mathlib-cache: 'true'", "build: 'false'",
                         'persist-credentials: false', 'run: bash companions/torus_filtration_20261011/replay.sh',
                         'name: torus-filtration-${{ github.run_id }}-${{ github.run_attempt }}',
                         'path: .lake/torus-filtration-evidence/', 'retention-days: 30', 'if-no-files-found: error',
                         'if: always()', 'LEAN_NUM_THREADS: 2'):
            self.assertIn(required, self.workflow, required)
        self.assertRegex(self.workflow, r'\n    timeout-minutes: [0-9]+\n', 'job timeout must be explicit')
        self.assertNotIn('continue-on-error', self.workflow)
        self.assertNotIn('formal/.lake/formal-evidence', self.workflow)
        # The hosted job must run the modules-mode leanchecker: no --fresh and no fresh switch in the workflow.
        self.assertNotIn('--fresh', self.workflow)
        self.assertNotIn('TORUS_LEANCHECKER_FRESH', self.workflow)

    def test_replay_contract(self):
        for required in ('set -euo pipefail', 'test ! -e "$OUT"', 'OUT="$ROOT/.lake/torus-filtration-evidence"',
                         'python3 -B -S "$SIDE/check.py" source > "$OUT/source.json"',
                         'python3 -B -S "$SIDE/test_torus_filtration.py"', 'python3 -B -O -S "$SIDE/test_torus_filtration.py"',
                         'python3 -B -S "$SIDE/check.py" emit "$OUT"', 'lake env bash', 'lean --version > "$TORUS_OUT/toolchain.log"',
                         'rev-parse HEAD)" >> "$TORUS_OUT/packages.log"',
                         'printf \'%s\\n\' "$LEANCHECKER_COMMAND" > "$TORUS_OUT/leanchecker.cmd"',
                         'run_lean leanchecker $LEANCHECKER_COMMAND',
                         'run_lean positive lean -DwarningAsError=true', 'run_lean axioms lean -DwarningAsError=true',
                         'run_lean types lean -DwarningAsError=true',
                         'run_lean census lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/Census.lean"',
                         'set -euo pipefail\n# The outer Python mode is the one named on each command line below, never an ambient PYTHONOPTIMIZE (C262 G1).\nunset PYTHONOPTIMIZE\n'):
            self.assertIn(required, self.replay, required)
        positions = []
        for module in ('TorusTopology', 'ClosedSuperlevel', 'SuperlevelBar', 'OrdinaryH0', 'OrdinaryH0Controls', 'TorusFiltration'):
            line = ('run_lean build-%s lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/%s.olean" "$TORUS_SIDE/%s.lean"'
                    % (module, module, module))
            self.assertEqual(self.replay.count(line), 1, module)
            positions.append(self.replay.index(line))
        # dependency order: TorusTopology, ClosedSuperlevel, SuperlevelBar, OrdinaryH0 (imports ClosedSuperlevel),
        # OrdinaryH0Controls (imports OrdinaryH0), then the root
        self.assertEqual(positions, sorted(positions))
        self.assertLess(positions[-1], self.replay.index('run_lean positive'))
        self.assertEqual(len(re.findall(r'^run_lean build-', self.replay, re.M)), 6)
        commands = '\n'.join(line for line in self.replay.splitlines() if not line.lstrip().startswith('#'))
        for forbidden in ('gate.py', 'formal/tests', 'lake build', 'lake update', 'lake exe cache', 'formal-evidence',
                          'ResearchFormalCoreR1'):
            self.assertNotIn(forbidden, commands, forbidden)
        # leanchecker: the modules-mode command is the default; --fresh exists only behind the operator switch.
        switch = re.search(r'^if \[ "\$\{TORUS_LEANCHECKER_FRESH:-0\}" = 1 \]; then\n  LEANCHECKER_COMMAND=\'([^\']+)\'\nelse\n'
                           r'  LEANCHECKER_COMMAND=\'([^\']+)\'\nfi\n', commands, re.M)
        self.assertIsNotNone(switch, 'leanchecker mode switch')
        self.assertEqual(switch.group(1), LEANCHECKER_FRESH)
        self.assertEqual(switch.group(2), LEANCHECKER_MODULES)
        self.assertEqual(self.c.LEANCHECKER[switch.group(2)], 'modules')
        self.assertEqual(commands.count('--fresh'), 1)
        self.assertEqual(commands.count('leanchecker.cmd'), 1)
        loops = re.findall(r'^for control in ([^;]+); do\n  code=0\n  lean ([^\n]*)', self.replay, re.M)
        self.assertEqual(len(loops), 2)
        self.assertEqual(loops[0][0].split(), list(self.c.FALSE_CONTROLS))
        self.assertIn('-DwarningAsError=true', loops[0][1])
        self.assertEqual(loops[1][0].split(), list(self.c.INJECTIONS))
        self.assertNotIn('warningAsError', loops[1][1])
        finish = [line for line in self.replay.splitlines() if 'check.py" finish' in line]
        self.assertEqual(finish, ['python3 -B -S "$SIDE/check.py" finish "$OUT"'])
        self.assertTrue(self.replay.strip().splitlines()[-1].startswith("echo 'PASS:"))

    def test_documents_keep_the_status_vocabulary(self):
        for name in ('README.md', 'SCOPE.md'):
            text = (SIDE / name).read_text(encoding='utf-8')
            for required in ('Scientific effect', 'NONE', 'credit', 'PENDING_INDEPENDENT_REVIEW', 'OpenAI/Codex',
                             'Anthropic/Claude', '8a5c7a24-784b-4aaa-b951-cd9f37b0dc64', 'efa80d28', '1fed3eda',
                             'ResearchFormalCoreR1.<n>', 'TorusFiltration.<n>', 'PairLawInterface.p',
                             'critical-level attainment', 'once-counting', LEANCHECKER_MODULES,
                             # C263/C264 registration: handoff and successor identities, the fixes, the census, FORMAL HOLD
                             'd74dc8b2', '346eea94', '261dd052', '3d6b0d6b', 'ite_eq_left', '6113438262', '6113033545', '6113372506',
                             '25 = 24 + 0 + 1', '38 = 27 + 0 + 11', 'FORMAL HOLD', 'superlevelBar_', 'ordinaryH0_',
                             'nonauthor exact-source review',
                             # C264 item-4 controls: the owner module, its identity, census, task and specification, the
                             # three controls, and the time-scoped pointers to the review and the readback (no label moves)
                             'OrdinaryH0Controls', 'df9d3645', '48 = 44 + 0 + 4', 'ordinaryH0Control_', '6113277485',
                             '6113277173', 'RejectMergerKillsPointClass', 'RejectSeparationWithoutNonzeroCoeff',
                             'RejectNonmergerKillsDifference', '5485883117', '5485829137', '2026-10-12 01:32Z',
                             'C264 owner task item 4 controls (2026-10-12)', 'not a review',
                             # FORMAL HOLD rests on the handoffs' own listed conditions; the source-scoped review keeps
                             # Lean execution open and states no credit; the readback records credit 0
                             '6113277485 item 5', 'open condition', 'same project account', 'nonzero organizational-independence credit'):
                self.assertIn(required, text, name + ' lacks ' + required)
            flat = ' '.join(text.split())
            for stale in (
                    # the hold presented as tied to one review that now exists (fix round of the item-4 commit)
                    'The handoffs tied that hold', 'The handoffs tied it to', 'the handoffs tied to a nonauthor',
                    'since 2026-10-12 01:32Z one does', 'Until 2026-10-12 01:32Z no nonauthor review of the compiled',
                    'this README records none since', 'records none since', 'beyond the discrete cases',
                    'Each statement applies one of the C264', 'instantiates the C264 statements',
                    'concrete instances of those C264 statements',
                    'so that each statement is seen in use'):
                self.assertNotIn(stale, flat, name + ' keeps a corrected statement: ' + stale)
            self.assertNotIn(LEANCHECKER_MODULES_BEFORE_C26X + '`', text, name + ' still names the pre-registration leanchecker command as current')
            self.assertNotIn(LEANCHECKER_MODULES_BEFORE_CONTROLS + '`', text, name + ' still names the pre-controls leanchecker command as current')
            self.assertNotIn('`leanchecker --fresh` re-checked', text, name + ' describes the withdrawn --fresh step as run')
            self.assertNotIn('runs `leanchecker --fresh TorusFiltration`', text)
            prose = re.sub(r'`[^`\n]*`', '', text)
            for forbidden in ('verified', 'accepted', 'kernel-checked'):
                hits = [m.start() for m in re.finditer(r'(?i)\b' + forbidden + r'\b', prose)]
                if forbidden == 'kernel-checked':
                    # Allowed only when naming the receipt field it belongs to.
                    hits = [h for h in hits if 'receipt' not in prose[max(0, h - 160):h + 160]]
                self.assertEqual(hits, [], name + ' uses the status word ' + forbidden + ' outside code spans')
        readme = (SIDE / 'README.md').read_text(encoding='utf-8')
        self.assertIn('## Compile fixes at the pin', readme)
        self.assertNotIn('formal/**', readme.replace('`formal/`', ''))
        # The control table quotes each emitted false statement verbatim, and the .olean hazard is stated.
        for statement, _ in self.c.FALSE_CONTROLS.values():
            self.assertIn('`' + statement + '`', readme, 'control statement not quoted verbatim: ' + statement)
        for required in ('.olean', 'never be committed', 'NOT_RUN', 'TORUS_LEANCHECKER_FRESH', 'leanchecker.cmd',
                         'exactly the 65 evidence files', 'Registration is not review', 'OrdinaryH0Controls.olean',
                         '6116225936', 'C254 alone did not establish this', 'DISCRIMINATOR_LOGS',
                         # the relabel is a dated companion note, the hosted run of 940dffc9 is reported, not adopted
                         '(companion note, 2026-10-12, Math- #428 comment 6116225936, not\n  part of the copied exclusion',
                         '38187870416', 'does not adopt its receipt', '01:16Z'):
            self.assertIn(required, readme, 'README lacks ' + required)
        for stale in ('exactly the 44 evidence files', 'those 44 files', '41 theorems and 17 definitions', 'the 58 declarations',
                      'two-line root module', 'six negative', 'Both modules `import Mathlib`',
                      # counts and phrases the item-4 controls commit moved
                      'exactly the 54 evidence files', 'those 54 files', 'What the 81 theorems and 28 definitions',
                      'Every one of the 109', 'four-line root module', 'the twelve emitted Lean files',
                      'All four modules `import Mathlib`', '(none exists: this lane', 'no nonauthor review of the compiled successor\nbytes yet'):
            self.assertNotIn(stale, readme, 'README keeps a superseded count or statement: ' + stale)
        scope = (SIDE / 'SCOPE.md').read_text(encoding='utf-8')
        for stale in ('41 theorem statements and 17 audited definitions', 'these 58 declarations', 'exactly these 58',
                      '81 theorem statements and 28 audited definitions', 'these 109 declarations', 'exactly these 109'):
            self.assertNotIn(stale, scope, 'SCOPE keeps a superseded count: ' + stale)


class SourceFixture(FixtureCase):
    def test_clean_fixture_passes_and_records_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            run = f.run('source')
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(run.stdout)
            self.assertEqual(result['checked_commit'], f.git('rev-parse', 'HEAD').strip())
            self.assertEqual(set(result['sources']), set(self.c.REQUIRED_FILES) | {self.c.PACKAGE + '/SOURCE_FILES.json'})
            self.assertEqual(len(result['declarations']), 153)
            self.assertEqual(result['environment'], {'lean_toolchain': 'leanprover/lean4:v4.34.1',
                                                     'dependency_revisions': f.revisions})
            self.assertEqual(result['run_id'], 'local')
            self.assertEqual(len(result['theorems']), 118)
            hosted = {'GITHUB_ACTIONS': 'true', 'GITHUB_SHA': result['checked_commit'], 'GITHUB_REPOSITORY': self.c.REPO,
                      'GITHUB_RUN_ID': '77', 'GITHUB_RUN_ATTEMPT': '2'}
            run = f.run('source', env=hosted)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['run_id'], '77')
            self.assertFails(f.run('source', env={**hosted, 'GITHUB_SHA': '0' * 40}), 'host/source mismatch')
            self.assertFails(f.run('source', env={**hosted, 'GITHUB_REPOSITORY': 'someone-else/Math-'}), 'host/source mismatch')
            self.assertFails(f.run('source', env={**hosted, 'GITHUB_RUN_ID': ''}), 'run identity absent')
            self.assertFails(f.run('source', env={**hosted, 'GITHUB_RUN_ATTEMPT': ''}), 'run identity absent')
            (f.side / 'stray.olean').write_bytes(b'untracked build artefact')
            self.assertEqual(f.run('source').returncode, 0, 'untracked artefacts are not source')

    def test_membership_and_byte_mutations_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            (f.side / 'README.md').write_text('# edited without a commit\n')
            self.assertFails(f.run('source'), 'dirty execution/source bytes: ' + self.c.PACKAGE + '/README.md')
            f.git('checkout', '--', '.')
            (f.root / 'formal/lean-toolchain').write_text('leanprover/lean4:v4.34.0\n')
            self.assertFails(f.run('source'), 'uncommitted modification in bound paths')
            f.git('checkout', '--', '.')
            (f.side / 'EXTRA.md').write_text('tracked but not in the manifest\n')
            f.commit()
            self.assertFails(f.run('source'), 'tracked companion membership differs')
            f.git('rm', '-q', '--', str(f.side / 'EXTRA.md'))
            f.commit()
            self.assertEqual(f.run('source').returncode, 0)
            (f.side / 'TorusTopology.olean').write_bytes(b'committed build artefact')
            f.commit()
            self.assertFails(f.run('source'), "tracked companion membership differs: ['" + self.c.PACKAGE + "/TorusTopology.olean']")
            f.git('rm', '-q', '--', str(f.side / 'TorusTopology.olean'))
            f.commit()
            (f.side / 'SCOPE.md').write_text('# changed and committed, manifest stale\n')
            f.commit()
            self.assertFails(f.run('source'), 'manifest source mismatch: ' + self.c.PACKAGE + '/SCOPE.md')
            f.restore()
            self.assertEqual(f.run('source').returncode, 0)
            (f.side / 'README.md').unlink()
            os.symlink('SCOPE.md', f.side / 'README.md')
            f.restore()
            self.assertFails(f.run('source'), 'symlink source: ' + self.c.PACKAGE + '/README.md')

    def test_module_mutations_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            module = f.side / 'ClosedSuperlevel.lean'
            original = module.read_text()
            swapped = original.replace('theorem superlevel_mono : True := trivial\ntheorem superlevel_isClosed : True := trivial',
                                       'theorem superlevel_isClosed : True := trivial\ntheorem superlevel_mono : True := trivial')
            self.assertNotEqual(swapped, original)
            cases = [(original.replace('theorem superlevel_mono ', 'theorem superlevel_monotone '),
                      'theorem inventory differs from source: ClosedSuperlevel'),
                     (swapped, 'theorem inventory differs from source: ClosedSuperlevel'),
                     (original.replace('noncomputable def superlevel_set : Nat := 0\nnoncomputable def superlevel_inclusion : Nat := 0',
                                       'noncomputable def superlevel_inclusion : Nat := 0\nnoncomputable def superlevel_set : Nat := 0'),
                      'def inventory differs from source: ClosedSuperlevel'),
                     (original.replace('def superlevel_set ', 'def superlevel_family '),
                      'def inventory differs from source: ClosedSuperlevel'),
                     (original.replace(':= trivial', ':= by sorry', 1), 'admission token in ClosedSuperlevel: sorry'),
                     (original + 'lemma injected : True := trivial\n', 'code after end TorusFiltration: ClosedSuperlevel:'),
                     (original.replace('\nend TorusFiltration', '\nlemma injected : True := trivial\nend TorusFiltration'),
                      'unexpected column-0 line in ClosedSuperlevel:'),
                     (original.replace('\nend TorusFiltration', '\nnoncomputable instance hidden : Inhabited Nat := ⟨0⟩\nend TorusFiltration'),
                      'unexpected column-0 line in ClosedSuperlevel:'),
                     (original.replace('\nend TorusFiltration', '\n  theorem hidden : True := trivial\nend TorusFiltration'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     # C262 G2: an indented imported `alias` immediately after the namespace opening, refused by the source CLI
                     (original.replace('namespace TorusFiltration\n', 'namespace TorusFiltration\n  alias hidden := Nat.add_comm\n'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     (original.replace('theorem superlevel_mono : True := trivial',
                                       'theorem superlevel_mono : True := trivial alias hidden := Nat.add_comm'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     (original.replace('\nend TorusFiltration', '\nalias hidden := Nat.add_comm\nend TorusFiltration'),
                      'unexpected column-0 line in ClosedSuperlevel:'),
                     (original.replace('\nend TorusFiltration', '\n  theorem/- -/hidden : True := trivial\nend TorusFiltration'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     (original.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0alias hidden := Nat.add_comm'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     (original.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0x1Ftheorem hidden : True := trivial'),
                      'command token outside a column-0 declaration in ClosedSuperlevel:'),
                     (original.replace('noncomputable def superlevel_set : Nat := 0', 'noncomputable def superlevel_set : Nat := 0b1axiom hidden : False'),
                      'admission token in ClosedSuperlevel: axiom'),
                     (original.replace('namespace TorusFiltration', 'namespace ResearchFormalCoreR1'),
                      'handoff namespace left in place: ClosedSuperlevel')]
            for text, message in cases:
                with self.subTest(message=message):
                    module.write_text(text)
                    f.restore()
                    self.assertFails(f.run('source'), message)
            module.write_text(original + '-- sorry inside a comment is not an admission\n')
            f.restore()
            self.assertEqual(f.run('source').returncode, 0)
            (f.side / 'TorusFiltration.lean').write_text('import TorusTopology\n')
            f.restore()
            self.assertFails(f.run('source'), 'root module must import exactly the five modules')
            # the pre-registration root (two imports) and the pre-controls root (four imports) are refused too; so is a
            # reordered, duplicated or unterminated import list
            for root in ('import TorusTopology\nimport ClosedSuperlevel\n',
                         'import TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\nimport OrdinaryH0\n',
                         'import TorusTopology\nimport ClosedSuperlevel\nimport OrdinaryH0\nimport SuperlevelBar\nimport OrdinaryH0Controls\n',
                         'import TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\nimport OrdinaryH0Controls\nimport OrdinaryH0\n',
                         'import TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\nimport OrdinaryH0\nimport OrdinaryH0Controls\nimport OrdinaryH0Controls\n',
                         'import TorusTopology\nimport ClosedSuperlevel\nimport SuperlevelBar\nimport OrdinaryH0\nimport OrdinaryH0Controls'):
                (f.side / 'TorusFiltration.lean').write_text(root)
                f.restore()
                self.assertFails(f.run('source'), 'root module must import exactly the five modules')
            (f.side / 'TorusFiltration.lean').write_text(self.c.ROOT_SOURCE)
            # companion imports through the CLI: OrdinaryH0 may import ClosedSuperlevel (as the registered module does);
            # ClosedSuperlevel may not import SuperlevelBar, and no module may import the root
            h0 = f.side / 'OrdinaryH0.lean'
            h0_original = h0.read_text()
            h0.write_text(h0_original.replace('import Mathlib\n', 'import Mathlib\nimport ClosedSuperlevel\n', 1))
            f.restore()
            self.assertEqual(f.run('source').returncode, 0, 'a companion import in dependency order is source')
            h0.write_text(h0_original.replace('import Mathlib\n', 'import Mathlib\nimport TorusFiltration\n', 1))
            f.restore()
            self.assertFails(f.run('source'), 'unexpected column-0 line in OrdinaryH0:2: import TorusFiltration')
            h0.write_text(h0_original)
            # the controls module may import OrdinaryH0 (as the registered module does); OrdinaryH0 may not import it
            controls = f.side / 'OrdinaryH0Controls.lean'
            controls_original = controls.read_text()
            controls.write_text(controls_original.replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0\n', 1))
            f.restore()
            self.assertEqual(f.run('source').returncode, 0, 'the controls module importing OrdinaryH0 is source')
            controls.write_text(controls_original)
            h0.write_text(h0_original.replace('import Mathlib\n', 'import Mathlib\nimport OrdinaryH0Controls\n', 1))
            f.restore()
            self.assertFails(f.run('source'), 'companion import out of dependency order in OrdinaryH0:2: OrdinaryH0Controls')
            h0.write_text(h0_original)
            module.write_text(original.replace('import Mathlib\n', 'import Mathlib\nimport SuperlevelBar\n', 1))
            f.restore()
            self.assertFails(f.run('source'), 'companion import out of dependency order in ClosedSuperlevel:2: SuperlevelBar')
            module.write_text(original)
            f.regenerate()
            meta = json.loads((f.side / 'SOURCE_FILES.json').read_text())
            del meta['files'][self.c.PACKAGE + '/TorusTopology.lean']
            (f.side / 'SOURCE_FILES.json').write_text(json.dumps(meta, indent=2, sort_keys=True) + '\n')
            f.commit()
            self.assertFails(f.run('source'), 'files inventory must list every required companion file')

    def test_environment_pins_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            (f.root / 'formal/lean-toolchain').write_text('leanprover/lean4:v4.34.2\n')
            f.commit()
            self.assertFails(f.run('source'), "wrong Lean toolchain: 'leanprover/lean4:v4.34.2'")
            (f.root / 'formal/lean-toolchain').write_text('leanprover/lean4:v4.34.1\n')
            f.write_manifest([{'name': 'mathlib', 'rev': 'main'}, {'name': 'batteries', 'rev': 'f2' * 20}])
            f.commit()
            self.assertFails(f.run('source'), 'unpinned dependency')
            f.write_manifest([{'name': 'mathlib', 'rev': 'd1' * 20}, {'name': 'mathlib', 'rev': 'd1' * 20}])
            f.commit()
            self.assertFails(f.run('source'), 'duplicate or empty dependency list')
            f.write_manifest([])
            f.commit()
            self.assertFails(f.run('source'), 'duplicate or empty dependency list')
            f.write_manifest([{'name': k, 'rev': v} for k, v in f.revisions.items()])
            f.commit()
            self.assertEqual(f.run('source').returncode, 0)


class MetadataFixture(FixtureCase):
    """The honesty labels and schema rules of SOURCE_FILES.json are enforced through the CLI, one field at a time,
    except seven fields of the successor record (handoff byte count and status, lane, authors, namespace, imports,
    change summary), which are refused only through the whole-record comparison in check.py metadata(). The owner-module
    record of OrdinaryH0Controls is compared whole too; its identity, author, review status, census, credit, comment
    pointers and kind each have a single-field case below, and the record as a whole is required."""

    def test_each_label_and_schema_rule_withholds_source(self):
        c = self.c
        workflow = c.WORKFLOW
        original = c.ORIGINAL_SHA256

        def setter(path, value):
            def mutate(m):
                node = m
                for key in path[:-1]:
                    node = node[key]
                node[path[-1]] = value
            return mutate

        def deleter(path):
            def mutate(m):
                node = m
                for key in path[:-1]:
                    node = node[key]
                del node[path[-1]]
            return mutate
        cases = [
            (setter(('scientific_effect',), 'LOW'), 'scientific effect must be NONE'),
            (setter(('alignment_status',), 'ACCEPTED'), 'alignment status cannot self-award review'),
            (setter(('provenance', 'organizational_independence_credit'), 1), 'credit must stay zero'),
            (setter(('provenance', 'human_review'), 'self'), 'credit must stay zero'),
            (setter(('provenance', 'claim'), c.CLAIM[:-1] + '5'), 'provenance identity'),
            (setter(('provenance', 'original_sha256', next(iter(original))), '0' * 64), 'provenance identity'),
            (setter(('provenance', 'original_bytes', 'C263-handoff/SuperlevelBar.lean'), 14905), 'successor provenance identity'),
            (deleter(('provenance', 'original_bytes', 'C264-handoff/OrdinaryH0.lean')), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'SuperlevelBar.lean', 'successor_sha256'), '0' * 64), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'OrdinaryH0.lean', 'successor_bytes'), 19802), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'OrdinaryH0.lean', 'handoff_sha256'), '0' * 64), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'SuperlevelBar.lean', 'formal_status'), 'ACCEPTED'), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'OrdinaryH0.lean', 'formal_status'), 'FORMAL_HOLD lifted'), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'SuperlevelBar.lean', 'organizational_independence_credit'), 1), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'OrdinaryH0.lean', 'census_at_pin'), '27 constants'), 'successor provenance identity'),
            (deleter(('provenance', 'successors', 'OrdinaryH0.lean', 'comments', 'owner_repair_handoff_428')), 'successor provenance identity'),
            (deleter(('provenance', 'successors', 'OrdinaryH0.lean')), 'successor provenance identity'),
            (setter(('provenance', 'successors', 'Third.lean'), {}), 'successor provenance identity'),
            # the owner-authored controls record (OrdinaryH0Controls.lean), compared whole
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'sha256'), '0' * 64), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'bytes'), 28503), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'author'), 'OpenAI/Codex lane'), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'kind'), 'handoff successor'), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'review_status'), 'review of OrdinaryH0; FORMAL HOLD lifted'),
             'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'organizational_independence_credit'), 1), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'census_at_pin'), '44 constants'), 'owner module provenance identity'),
            (deleter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'comments', 'owner_task_item_4_428')), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean', 'formal_status'), 'ACCEPTED'), 'owner module provenance identity'),
            (deleter(('provenance', 'owner_modules', 'OrdinaryH0Controls.lean')), 'owner module provenance identity'),
            (setter(('provenance', 'owner_modules', 'Other.lean'), {}), 'owner module provenance identity'),
            (lambda m: m['provenance']['successors'].__setitem__('OrdinaryH0Controls.lean', m['provenance']['owner_modules']['OrdinaryH0Controls.lean']),
             'successor provenance identity'),
            (deleter(('provenance', 'owner_modules')), 'provenance key missing: owner_modules'),
            (deleter(('provenance', 'successors')), 'provenance key missing: successors'),
            (deleter(('provenance', 'original_bytes')), 'provenance key missing: original_bytes'),
            (setter(('provenance', 'original_sha256', 'C263-handoff/SuperlevelBar.lean'), '0' * 64), 'provenance identity'),
            (deleter(('provenance', 'original_sha256', 'C264-handoff/OrdinaryH0.lean')), 'provenance identity'),
            (setter(('provenance', 'original_status'), 'COMPILED'), 'provenance labels'),
            (setter(('provenance', 'namespace_mapping'), 'TorusFiltration.<n> -> TorusFiltration.<n>'), 'provenance labels'),
            (deleter(('provenance', 'human_review')), 'provenance key missing: human_review'),
            (setter(('provenance',), 'none'), 'provenance object'),
            (setter(('extra',), 1), 'SOURCE_FILES schema keys'),
            (deleter(('provenance',)), 'SOURCE_FILES schema keys'),
            (deleter(('census_auxiliary',)), 'SOURCE_FILES schema keys'),
            (setter(('census_auxiliary',), 'TorusFiltration.torus_periodBasis.congr_simp'), 'census_auxiliary must list dotted auxiliary names'),
            (setter(('census_auxiliary',), ['TorusFiltration.hidden']), 'census_auxiliary must list dotted auxiliary names'),
            (setter(('census_auxiliary',), ['Other.torus_periodBasis.congr_simp']), 'census_auxiliary must list dotted auxiliary names'),
            (setter(('census_auxiliary',), ['TorusFiltration.torus_periodBasis.congr_simp'] * 2), 'census_auxiliary must list dotted auxiliary names'),
            (setter(('schema',), 2), 'SOURCE_FILES schema version'),
            (setter(('schema',), '1'), 'SOURCE_FILES schema version'),
            (setter(('schema',), True), 'SOURCE_FILES schema version'),
            (lambda m: m['files'].__setitem__('formal/gate.py', m['files'][workflow]), 'files inventory outside the companion'),
            (setter(('files',), {}), 'files inventory outside the companion'),
            (setter(('theorems', 'Third'), ['x']), 'per-module inventory keys'),
            (deleter(('definitions', 'TorusTopology')), 'per-module inventory keys'),
            (lambda m: m['theorems']['ClosedSuperlevel'].append('torus_compact'), 'duplicate declaration name'),
            (lambda m: m['definitions']['ClosedSuperlevel']['def'].append('superlevel_set'), 'duplicate declaration name'),
            (setter(('namespace',), 'ResearchFormalCoreR1'), 'namespace or root module'),
            (setter(('root_module',), 'TorusTopology'), 'namespace or root module'),
            (setter(('modules',), ['ClosedSuperlevel', 'TorusTopology']), 'module list'),
            (setter(('modules',), ['TorusTopology', 'ClosedSuperlevel']), 'module list'),
            (setter(('modules',), ['TorusTopology', 'ClosedSuperlevel', 'OrdinaryH0', 'SuperlevelBar']), 'module list'),
            (setter(('modules',), ['TorusTopology', 'ClosedSuperlevel', 'SuperlevelBar', 'OrdinaryH0']), 'module list'),
            (setter(('modules',), ['TorusTopology', 'ClosedSuperlevel', 'SuperlevelBar', 'OrdinaryH0Controls', 'OrdinaryH0']), 'module list'),
            (deleter(('theorems', 'OrdinaryH0Controls')), 'per-module inventory keys'),
            (deleter(('definitions', 'OrdinaryH0Controls')), 'per-module inventory keys'),
            (lambda m: m['theorems']['OrdinaryH0Controls'].append('ordinaryH0_pointClass_eq_iff'), 'duplicate declaration name'),
            (setter(('theorems', 'OrdinaryH0Controls'), []), 'empty theorem list: OrdinaryH0Controls'),
            (deleter(('theorems', 'OrdinaryH0')), 'per-module inventory keys'),
            (deleter(('definitions', 'SuperlevelBar')), 'per-module inventory keys'),
            (lambda m: m['theorems']['OrdinaryH0'].append('superlevelBar_strict_cut'), 'duplicate declaration name'),
            (setter(('theorems', 'SuperlevelBar', 0), 'superlevelBar_essential_iff\u03b9'), 'invalid declaration name in SuperlevelBar'),
            (setter(('theorems', 'OrdinaryH0', 0), 'ordinaryH0_componentCoproductMap_ι'), 'invalid declaration name in OrdinaryH0'),
            (deleter(('definitions', 'TorusTopology', 'instance')), 'definition kinds: TorusTopology'),
            (setter(('theorems', 'TorusTopology', 0), 'bad-name'), 'invalid declaration name in TorusTopology'),
            (setter(('definitions', 'TorusTopology', 'def', 0), 7), 'invalid declaration name in TorusTopology'),
            (setter(('theorems', 'ClosedSuperlevel'), []), 'empty theorem list: ClosedSuperlevel'),
            (deleter(('files', workflow, 'bytes')), 'file entry keys: ' + workflow),
            (setter(('files', workflow, 'bytes'), -1), 'file bytes: ' + workflow),
            (setter(('files', workflow, 'bytes'), '1776'), 'file bytes: ' + workflow),
            (setter(('files', workflow, 'sha256'), 'zz' * 32), 'file sha256: ' + workflow),
            (setter(('files', workflow, 'git_blob'), 'ab' * 19), 'file git blob: ' + workflow),
            (lambda m: json.dumps(m, indent=2, sort_keys=True).replace('{\n  "alignment_status"', '{\n  "schema": 1,\n  "alignment_status"', 1) + '\n',
             'duplicate JSON key: schema'),
            (lambda m: json.dumps(m, indent=2, sort_keys=True).replace('"schema": 1', '"schema": 1.0', 1) + '\n',
             'nonfinite or noninteger JSON number'),
            (lambda m: json.dumps(m, indent=2, sort_keys=True).replace('"schema": 1', '"schema": NaN', 1) + '\n',
             'nonfinite or noninteger JSON number'),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(c, tmp)
            self.assertEqual(f.run('source').returncode, 0)
            for mutate, message in cases:
                with self.subTest(message=message):
                    f.manifest(mutate)
                    self.assertFails(f.run('source'), message)
                    f.restore()
            self.assertEqual(f.run('source').returncode, 0)


class FinishFixture(FixtureCase):
    def test_complete_evidence_yields_a_bounded_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            out = f.evidence()
            self.assertEqual({p.name for p in out.iterdir() if p.name.endswith('.lean')}, set(EMITTED))
            run = f.run('finish', str(out))
            self.assertEqual(run.returncode, 0, run.stderr)
            receipt = json.loads((out / 'receipt.json').read_text())
            self.assertEqual(receipt['schema'], 1)
            self.assertEqual(receipt['scientific_effect'], 'NONE')
            self.assertEqual(receipt['formalization_status'], 'kernel-checked')
            self.assertEqual(receipt['alignment_status'], 'PENDING_INDEPENDENT_REVIEW')
            self.assertIs(receipt['scientific_acceptance'], False)
            self.assertEqual(receipt['lean_version'], LEAN_VERSION_LINE.strip())
            self.assertEqual(receipt['dependency_revisions'], f.revisions)
            self.assertEqual(len(receipt['declarations']), 153)
            self.assertEqual(len(receipt['axioms']), 58 + 24 + 27 + 44)
            self.assertEqual(receipt['theorem_count'], 118)
            self.assertEqual(receipt['definition_count'], {'abbrev': 6, 'def': 26, 'instance': 3})
            self.assertEqual(receipt['provenance']['successors'], self.c.SUCCESSORS)
            self.assertEqual(receipt['provenance']['owner_modules'], self.c.OWNER_MODULES)
            self.assertEqual(receipt['provenance']['original_bytes'], self.c.ORIGINAL_BYTES)
            self.assertEqual(len(receipt['provenance']['original_sha256']), 4)
            self.assertEqual(receipt['negative_controls'],
                             {**{k: 'REJECTED_BY_LEAN' for k in self.c.FALSE_CONTROLS},
                              **{k: 'REJECTED_BY_AXIOM_AUDIT' for k in self.c.INJECTIONS}})
            self.assertEqual(receipt['provenance']['claim'], self.c.CLAIM)
            self.assertEqual(receipt['provenance']['original_sha256'], self.c.ORIGINAL_SHA256)
            self.assertEqual(receipt['leanchecker'], {'command': LEANCHECKER_MODULES, 'mode': 'modules'})
            self.assertIn('own declarations against the cached', receipt['scope_note'])
            self.assertNotIn('--fresh', receipt['scope_note'])
            for name, digest in receipt['log_sha256'].items():
                self.assertEqual(hashlib.sha256((out / name).read_bytes()).hexdigest(), digest, name)
            self.assertEqual(set(receipt['log_sha256']), {p.name for p in out.iterdir() if p.is_file()} - {'receipt.json'})
            self.assertEqual(set(receipt['log_sha256']), set(self.c.EVIDENCE_FILES))
            self.assertEqual(len(receipt['log_sha256']), 65)
            self.assertEqual(receipt['census'], {'constants': 153 + len(self.c.metadata()['census_auxiliary']) + len(INTERNAL_GENERATED),
                                                 'user_declarations': 153,
                                                 'generated_user': sorted(self.c.metadata()['census_auxiliary']),
                                                 'internal_generated': len(INTERNAL_GENERATED)})
            self.assertIn('census.log', receipt['log_sha256'])
            self.assertIn('axioms.log', receipt['log_sha256'])
            for name in ('build-SuperlevelBar', 'build-OrdinaryH0', 'build-OrdinaryH0Controls', 'RejectEssentialDeathBound',
                         'RejectReducedPointClass', 'RejectMergerKillsPointClass', 'RejectSeparationWithoutNonzeroCoeff',
                         'RejectNonmergerKillsDifference'):
                self.assertIn(name + '.log', receipt['log_sha256'])
                self.assertIn(name + '.status', receipt['log_sha256'])
            for name in ('RejectEssentialDeathBound', 'RejectReducedPointClass', 'RejectMergerKillsPointClass',
                         'RejectSeparationWithoutNonzeroCoeff', 'RejectNonmergerKillsDifference'):
                self.assertIn(name + '.lean', receipt['log_sha256'])
            self.assertIn('leanchecker.cmd', receipt['log_sha256'])
            self.assertIn('Positive.lean', receipt['log_sha256'])
            self.assertIn('tests-optimized.log', receipt['log_sha256'])
            # C262 G3: a receipt is never replaced. A second finish on the same directory is refused and leaves the
            # old bytes intact, with or without a newly failing input; no digest of the receipt itself appears.
            frozen = (out / 'receipt.json').read_bytes()
            self.assertFails(f.run('finish', str(out)), 'receipt.json already present')
            self.assertEqual((out / 'receipt.json').read_bytes(), frozen)
            (out / 'leanchecker.status').write_text('1\n')
            self.assertFails(f.run('finish', str(out)), 'receipt.json already present')
            self.assertEqual((out / 'receipt.json').read_bytes(), frozen)
            (out / 'leanchecker.status').write_text('0\n')
            self.assertNotIn('receipt.json', receipt['log_sha256'])
            # An operator's --fresh run is recorded as such, with leanchecker's own progress line tolerated.
            (out / 'receipt.json').unlink()
            (out / 'leanchecker.cmd').write_text(LEANCHECKER_FRESH + '\n')
            (out / 'leanchecker.log').write_text('replaying TorusFiltration with --fresh\n')
            run = f.run('finish', str(out))
            self.assertEqual(run.returncode, 0, run.stderr)
            receipt = json.loads((out / 'receipt.json').read_text())
            self.assertEqual(receipt['leanchecker'], {'command': LEANCHECKER_FRESH, 'mode': 'fresh'})
            self.assertIn('--fresh', receipt['scope_note'])

    def test_every_weakening_withholds_the_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(self.c, tmp)
            out = f.evidence()
            meta = self.c.metadata()
            first = self.c.targets(meta)[0]
            axioms = (out / 'axioms.log').read_text()
            types_log = (out / 'types.log').read_text()
            audit = (out / 'Audit.lean').read_text()
            def census_with(row):
                lines = (out / 'census.log').read_text().splitlines(True)
                body = sorted(lines[:-1] + ['%s %s\n' % row])
                return ''.join(body) + 'CENSUS_END %d\n' % len(body)

            def census_without(name):
                lines = (out / 'census.log').read_text().splitlines(True)
                body = [l for l in lines[:-1] if not l.startswith(name + ' ')]
                return ''.join(body) + 'CENSUS_END %d\n' % len(body)
            cases = [
                ('build-TorusTopology.status', '1\n', 'missing successful process: build-TorusTopology'),
                ('build-SuperlevelBar.status', '1\n', 'missing successful process: build-SuperlevelBar'),
                ('build-OrdinaryH0.status', '', 'missing successful process: build-OrdinaryH0'),
                ('build-OrdinaryH0Controls.status', '1\n', 'missing successful process: build-OrdinaryH0Controls'),
                ('leanchecker.cmd', LEANCHECKER_MODULES_BEFORE_C26X + '\n', "unrecognized leanchecker invocation: '" + LEANCHECKER_MODULES_BEFORE_C26X + "'"),
                ('leanchecker.cmd', LEANCHECKER_MODULES_BEFORE_CONTROLS + '\n', "unrecognized leanchecker invocation: '" + LEANCHECKER_MODULES_BEFORE_CONTROLS + "'"),
                ('leanchecker.status', '', 'missing successful process: leanchecker'),
                ('leanchecker.cmd', 'leanchecker TorusFiltration\n', "unrecognized leanchecker invocation: 'leanchecker TorusFiltration'"),
                ('leanchecker.cmd', 'leanchecker --fresh TorusTopology\n', 'unrecognized leanchecker invocation'),
                ('leanchecker.log', 'uncaught exception: failed to read module data\n', 'leanchecker reported diagnostics'),
                ('toolchain.log', LEAN_VERSION_LINE.replace('4.34.1', '4.34.0'), 'unexpected running Lean version'),
                ('packages.log', 'mathlib %s\n' % ('d1' * 20), 'installed dependency HEADs differ'),
                ('axioms.log', axioms.replace('[propext, Classical.choice, Quot.sound]', '[propext, sorryAx]', 1),
                 'forbidden transitive axiom'),
                ('axioms.log', axioms.replace("'%s' depends on axioms: [propext, Classical.choice, Quot.sound]\n" % first, ''),
                 'missing target axiom report'),
                ('axioms.log', 'warning: noise\n' + axioms, 'unrecognized audit output'),
                ('types.log', ''.join(types_log.splitlines(True)[1:]), 'type inventory mismatch'),
                ('types.log', types_log + 'error: crash\n', 'type diagnostic'),
                # C262 G2 closure: the elaborated census. N = the fixture's row count.
                ('census.log', census_with(('TorusFiltration.superlevel_mono.hidden', 'user range')), "user-written declarations outside the inventory: ['TorusFiltration.superlevel_mono.hidden']"),
                ('census.log', census_with(('TorusFiltration.superlevel_mono.proof_1', 'internal range')), "user-written declarations with internal-style names: ['TorusFiltration.superlevel_mono.proof_1']"),
                ('census.log', census_with(('TorusFiltration.superlevel_mono._hidden', 'internal range')), "user-written declarations with internal-style names: ['TorusFiltration.superlevel_mono._hidden']"),
                ('census.log', census_with(('TorusFiltration.superlevel_mono.other_simp', 'user generated')), "compiler-generated constants not listed in census_auxiliary: ['TorusFiltration.superlevel_mono.other_simp']"),
                ('census.log', census_without('TorusFiltration.superlevel_mono'), "inventory targets absent from the census: ['TorusFiltration.superlevel_mono']"),
                ('census.log', census_without('TorusFiltration.ordinaryH0Control_collapse'), "inventory targets absent from the census: ['TorusFiltration.ordinaryH0Control_collapse']"),
                ('census.log', census_with(('TorusFiltration.ordinaryH0Control_collapse.hidden', 'user range')),
                 "user-written declarations outside the inventory: ['TorusFiltration.ordinaryH0Control_collapse.hidden']"),
                ('census.log', census_without('TorusFiltration.torus_periodBasis.congr_simp'), "census_auxiliary entries absent or not compiler-generated: ['TorusFiltration.torus_periodBasis.congr_simp']"),
                ('census.log', (out / 'census.log').read_text().replace('TorusFiltration.torus_periodBasis.congr_simp user generated', 'TorusFiltration.torus_periodBasis.congr_simp user range'),
                 "user-written declarations outside the inventory: ['TorusFiltration.torus_periodBasis.congr_simp']"),
                ('census.log', (out / 'census.log').read_text().replace('CENSUS_END', 'TorusFiltration.superlevel_mono.hidden user range\nCENSUS_END'), 'census count mismatch'),
                ('census.log', ''.join((out / 'census.log').read_text().splitlines(True)[:-1]), 'census terminator absent'),
                ('census.log', 'warning: noise\n' + (out / 'census.log').read_text(), 'unrecognized census output'),
                ('census.log', (out / 'census.log').read_text().replace(' user range\n', '\n', 1), 'unrecognized census output'),
                ('census.status', '1\n', 'missing successful process: census'),
                ('RejectSuperlevelSignFlip.log', FALSE_LOG.format('RejectSuperlevelSignFlip').replace('False', 'True'),
                 'not the intended False-goal diagnostic'),
                ('RejectSuperlevelSignFlip.status', '0\n', 'false-statement control must exit exactly one'),
                ('RejectEssentialDeathBound.log', FALSE_LOG.format('RejectEssentialDeathBound').replace('⊢ False', '⊢ 1 ≤ 0'),
                 'not the intended False-goal diagnostic: RejectEssentialDeathBound'),
                ('RejectEssentialDeathBound.status', '0\n', 'false-statement control must exit exactly one'),
                ('RejectReducedPointClass.log', '', 'not the intended False-goal diagnostic: RejectReducedPointClass'),
                ('RejectReducedPointClass.log', FALSE_LOG.format('RejectReducedPointClass') + 'error: This simp argument is unused\n',
                 'not the intended False-goal diagnostic: RejectReducedPointClass'),
                ('RejectReducedPointClass.status', '2\n', 'false-statement control must exit exactly one'),
                # the item-4 controls: each true sibling's diagnostic (pinned from Lean, DISCRIMINATOR_LOGS) is refused
                ('RejectMergerKillsPointClass.log', DISCRIMINATOR_LOGS['RejectMergerKillsPointClass'],
                 'not the intended False-goal diagnostic: RejectMergerKillsPointClass'),
                ('RejectSeparationWithoutNonzeroCoeff.log', DISCRIMINATOR_LOGS['RejectSeparationWithoutNonzeroCoeff'],
                 'not the intended False-goal diagnostic: RejectSeparationWithoutNonzeroCoeff'),
                ('RejectNonmergerKillsDifference.log', DISCRIMINATOR_LOGS['RejectNonmergerKillsDifference'],
                 'not the intended False-goal diagnostic: RejectNonmergerKillsDifference'),
                ('RejectNonmergerKillsDifference.status', '0\n', 'false-statement control must exit exactly one'),
                ('RejectMergerKillsPointClass.lean', (out / 'RejectMergerKillsPointClass.lean').read_text().replace(' true)', ' true - '
                 'ordinaryH0_pointClass (TopCat.of Bool) ordinaryH0Control_intCoeff false)', 1),
                 'emitted Lean file changed across execution: RejectMergerKillsPointClass.lean'),
                ('RejectSeparationWithoutNonzeroCoeff.lean', (out / 'RejectSeparationWithoutNonzeroCoeff.lean').read_text().replace('zeroCoeff', 'intCoeff'),
                 'emitted Lean file changed across execution: RejectSeparationWithoutNonzeroCoeff.lean'),
                ('RejectSorry.status', '1\n', 'injection control must be accepted by Lean'),
                ('RejectSorry.log', SORRY_WARNING + INJECTED.format('propext'), 'not the intended injected axiom report'),
                ('RejectNativeDecide.log', INJECTED.format('sorryAx'), 'not the intended injected axiom report'),
                ('source.json', json.dumps({**json.loads((out / 'source.json').read_text()), 'run_id': '1'}),
                 'source changed across execution'),
                ('Positive.lean', 'import TorusFiltration\n', 'emitted Lean file changed across execution: Positive.lean'),
                ('Audit.lean', ''.join(audit.splitlines(True)[:-1]), 'emitted Lean file changed across execution: Audit.lean'),
                ('Types.lean', (out / 'Types.lean').read_text().replace('set_option pp.explicit true\n', ''),
                 'emitted Lean file changed across execution: Types.lean'),
                ('RejectSorry.lean', (out / 'RejectSorry.lean').read_text().replace('by sorry', 'trivial'),
                 'emitted Lean file changed across execution: RejectSorry.lean'),
                ('RejectConstantNotPeriodic.lean', 'import TorusFiltration\n',
                 'emitted Lean file changed across execution: RejectConstantNotPeriodic.lean'),
                ('RejectReducedPointClass.lean', (out / 'RejectReducedPointClass.lean').read_text().replace('≠', '='),
                 'emitted Lean file changed across execution: RejectReducedPointClass.lean'),
                ('Census.lean', (out / 'Census.lean').read_text().replace(', `OrdinaryH0,', ','),
                 'emitted Lean file changed across execution: Census.lean'),
                ('Census.lean', (out / 'Census.lean').read_text().replace(', `OrdinaryH0Controls', ''),
                 'emitted Lean file changed across execution: Census.lean')]
            for name, content, message in cases:
                with self.subTest(name=name, message=message):
                    saved = (out / name).read_text()
                    (out / name).write_text(content)
                    try:
                        self.assertFails(f.run('finish', str(out)), message)
                        self.assertFalse((out / 'receipt.json').exists(), 'receipt written despite refusal')
                    finally:
                        (out / name).write_text(saved)
            # C262 G3: every one of the 65 required evidence members is required; removing any one withholds the receipt.
            self.assertEqual({p.name for p in out.iterdir()}, set(self.c.EVIDENCE_FILES))
            for name in sorted(self.c.EVIDENCE_FILES):
                with self.subTest(removed=name):
                    saved = (out / name).read_bytes()
                    (out / name).unlink()
                    try:
                        self.assertFails(f.run('finish', str(out)), "evidence membership differs: missing ['%s'], unexpected []" % name)
                        self.assertFalse((out / 'receipt.json').exists(), 'receipt written despite refusal')
                    finally:
                        (out / name).write_bytes(saved)
            # An unexpected member, a symlinked member and a stray subdirectory are refused too.
            (out / 'extra.log').write_text('')
            self.assertFails(f.run('finish', str(out)), "evidence membership differs: missing [], unexpected ['extra.log']")
            (out / 'extra.log').unlink()
            (out / 'stray').mkdir()
            self.assertFails(f.run('finish', str(out)), "evidence membership differs: missing [], unexpected ['stray']")
            (out / 'stray').rmdir()
            # A required member that is a directory is not a regular file.
            saved = (out / 'tests.log').read_bytes()
            (out / 'tests.log').unlink()
            (out / 'tests.log').mkdir()
            self.assertFails(f.run('finish', str(out)), 'evidence member is not a regular file: tests.log')
            self.assertFalse((out / 'receipt.json').exists())
            (out / 'tests.log').rmdir()
            (out / 'tests.log').write_bytes(saved)
            saved = (out / 'tests.log').read_bytes()
            (out / 'tests.log').unlink()
            os.symlink('tests-optimized.log', out / 'tests.log')
            self.assertFails(f.run('finish', str(out)), 'evidence member is not a regular file: tests.log')
            self.assertFalse((out / 'receipt.json').exists())
            (out / 'tests.log').unlink()
            (out / 'tests.log').write_bytes(saved)
            # A symlinked evidence directory is refused before anything is read.
            os.symlink(out, Path(tmp) / 'evidence-link')
            self.assertFails(f.run('finish', str(Path(tmp) / 'evidence-link')), 'evidence directory absent, not a directory, or a symlink')
            (Path(tmp) / 'evidence-link').unlink()
            # The exclusive write itself (not only the pre-check) refuses an existing file and a planted symlink, intact.
            frozen = b'frozen receipt bytes\n'
            (out / 'planted.json').write_bytes(frozen)
            with self.assertRaises(FileExistsError):
                self.c.write_new_file(out / 'planted.json', 'new\n')
            self.assertEqual((out / 'planted.json').read_bytes(), frozen)
            (out / 'planted.json').unlink()
            os.symlink('absent-target', out / 'planted.json')
            with self.assertRaises(OSError):
                self.c.write_new_file(out / 'planted.json', 'new\n')
            self.assertFalse((out / 'absent-target').exists())
            (out / 'planted.json').unlink()
            # A pre-existing receipt (even a symlink to nothing) is never replaced.
            os.symlink('absent-target', out / 'receipt.json')
            self.assertFails(f.run('finish', str(out)), 'receipt.json already present')
            (out / 'receipt.json').unlink()
            self.assertEqual(f.run('finish', str(out)).returncode, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
