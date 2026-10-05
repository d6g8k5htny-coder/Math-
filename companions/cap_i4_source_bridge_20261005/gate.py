#!/usr/bin/env python3
"""Fail-closed companion custody/contract checks; not a mathematical alignment verdict."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

BASE = 'c08e83597f94f923b8411dc13cdf28be3f214b37'
SOURCE = 'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md'
SOURCE_BLOB = 'dfed3b8d318a3ab1950957f393307733a4bef3f2'
HERE = Path(__file__).resolve().parent
REL = 'companions/cap_i4_source_bridge_20261005'
ROOT = HERE.parent.parent
TARGETS = '''depthEvent fourthEvent goodCap cap_failure_eq_union cap_failure_subset
fourth_moment_tail E4_specialization double_soft_integral matrix_soft_integral
spectralEnvelope spectralKernel spectral_kernel_eq MatrixDepthTransport
depth_numerator_r5 weighted_depth_r3 scalar_near_or_far scalar_soft_integral
scalar_far_fourth_moment cap_union_mass cap_cubic_of_tails'''.split()
ALLOW_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
NEGATIVES = {'RejectDroppedSoft', 'RejectDroppedFar'}
FRAGMENTS = [
    'lam x ≤ (4 / (3 * k)) * r * M3 x ^ 2',
    '3 * k / 10 < r * M4 x',
    'x * (x + E * r * U)',
    'r ^ 3 * ((D ^ 3 / 3) * U ^ 6 + (E * D ^ 2 / 2) * U ^ 5)',
    'r ^ 2 * P * U ^ (2 * m)',
    'p02_lm009_markov_event', 'weightedLaw_event_real',
    'ht : MatrixDepthTransport',
    'hi : Integrable (fun z => spectralEnvelope',
    'hz : cZ * r ^ 2 ≤ ∫ x, W x ∂μ',
    'lam ≤ 4 * D * r * J ^ 2 ∨ 1 / (4 * D * r) < lam',
    'r ^ 5 * (64 * D ^ 3 / 3 + 8 * E * D ^ 2) * J ^ 10',
]

def no_comments(text: str) -> str:
    """Strip Lean nested block and line comments, rejecting unclosed block comments."""
    out: list[str] = []
    depth = 0
    i = 0
    while i < len(text):
        if text.startswith('/-', i):
            depth += 1; i += 2
        elif depth and text.startswith('-/', i):
            depth -= 1; i += 2
        elif depth:
            i += 1
        elif text.startswith('--', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        else:
            out.append(text[i]); i += 1
    if depth:
        raise ValueError('unclosed Lean comment')
    return ''.join(out)

def check_contract(text: str) -> None:
    code = no_comments(text)
    banned = r'\b(sorry|admit|axiom|unsafe|native_decide|run_tac|run_elab|elab|initialize|implemented_by|extern)\b'
    if re.search(banned, code):
        raise ValueError('trust escape token')
    if 'Real.sqrt' in code or re.search(r'p02_lm00[89]_.*transfer', code):
        raise ValueError('weak square-root transfer substituted')
    names = re.findall(r'^(?:noncomputable )?(?:def|theorem) (\w+)', code, re.M)
    if names != TARGETS:
        raise ValueError('declaration inventory changed')
    if not all(s in code for s in FRAGMENTS):
        raise ValueError('source equation/explicit premise contract changed')
    imports = re.findall(r'^import (.+)$', code, re.M)
    if imports != ['ResearchFormalCoreR1.MomentTail',
                   'Mathlib.Analysis.SpecialFunctions.Integrals.Basic', 'Mathlib.Tactic']:
        raise ValueError('import boundary changed')
    if re.findall(r'^set_option (.+)$', code, re.M) != ['autoImplicit false']:
        raise ValueError('options boundary changed')

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def source_check() -> None:
    check_contract((HERE/'CapI4.lean').read_text())
    if git('hash-object', SOURCE) != SOURCE_BLOB:
        raise ValueError('source blob mismatch')
    if git('diff', '--name-only', BASE, '--', 'formal', SOURCE):
        raise ValueError('sealed formal package/source changed')
    allowed = {f'{REL}/{name}' for name in ['CapI4.lean', 'gate.py', 'replay.sh', 'README.md']}
    allowed.add('.github/workflows/cap-i4-source-bridge.yml')
    if git('diff', '--name-only', 'HEAD', '--', *sorted(allowed)):
        raise ValueError('companion working bytes differ from HEAD')
    for row in git('diff', '--name-status', BASE, 'HEAD').splitlines():
        state, path = row.split('\t', 1)
        if state != 'A' or path not in allowed:
            raise ValueError(f'out-of-scope change: {row}')
    print(json.dumps({'source_gate': 'PASS', 'head': git('rev-parse', 'HEAD'),
        'base': BASE, 'source_path': SOURCE, 'source_blob': SOURCE_BLOB,
        'source_sha256': hashlib.sha256((ROOT/SOURCE).read_bytes()).hexdigest(),
        'companion_sha256': hashlib.sha256((HERE/'CapI4.lean').read_bytes()).hexdigest(),
        'packet_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(allowed)},
        'audited_declarations': len(TARGETS), 'scientific_effect': 'NONE'}))

def emit(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out/'Audit.lean').write_text('import CapI4\n' + '\n'.join(
        '#print axioms CapI4.' + n for n in TARGETS) + '\n')
    (out/'Types.lean').write_text('import CapI4\nset_option pp.universes true\n' + '\n'.join(
        '#check @CapI4.' + n for n in TARGETS) + '\n')
    (out/'Positive.lean').write_text('''import CapI4
open MeasureTheory
example : CapI4.depthEvent 1 1 (fun _ : Unit => 4/3) (fun _ => 1) = Set.univ := by
  ext x; norm_num [CapI4.depthEvent]
example : CapI4.fourthEvent 1 1 (fun _ : Unit => 3/10) = ∅ := by
  ext x; norm_num [CapI4.fourthEvent]
example : (∫ x in (0 : ℝ)..1, x * (x + 1)) = 5/6 := by
  rw [CapI4.double_soft_integral]; norm_num
example : (8 : ℝ) ≤ 4 * 1 * 1 * (1 : ℝ)^2 ∨ (1 : ℝ)/(4*1*1) < 8 :=
  CapI4.scalar_near_or_far 8 1 1 1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
example : ¬ ((8 : ℝ) ≤ 4 * 1 * 1 * (1 : ℝ)^2) := by norm_num
''')
    (out/'RejectDroppedSoft.lean').write_text('''import CapI4
open MeasureTheory
example : (∫ x in (0 : ℝ)..1, x * (x + 1)) = 1/3 := by
  rw [CapI4.double_soft_integral]; norm_num
''')
    (out/'RejectDroppedFar.lean').write_text('''import CapI4
-- Same admissible witness as Positive.lean, with the necessary far disjunct deleted.
example : (8 : ℝ) ≤ 4 * 1 * 1 * (1 : ℝ)^2 := by norm_num
''')

def check_audit(log: Path) -> None:
    text = log.read_text()
    found: dict[str, list[str]] = {}
    pat = r"'?CapI4\.(\w+)'?\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pat, text, flags=re.S):
        name = match.group(1)
        if name in found:
            raise ValueError(f'duplicate audit declaration: {name}')
        found[name] = [s.strip() for s in (match.group(2) or '').split(',') if s.strip()]
    if set(found) != set(TARGETS):
        raise ValueError(f'audit inventory mismatch: {sorted(set(TARGETS)-set(found))}')
    for name, axioms in found.items():
        if set(axioms) - ALLOW_AXIOMS:
            raise ValueError(f'forbidden axiom at {name}: {axioms}')
    print(json.dumps({'axiom_audit': 'PASS', 'declarations': len(found), 'reports': found}))

def check_negative_text(control: str, status: int, text: str) -> None:
    """Require the intended concrete False goal; reject crashes and unrelated failures."""
    if control not in NEGATIVES or status != 1:
        raise ValueError('wrong control or compiler exit status')
    pattern = (r'(?:[^\n]*[/\\])?' + re.escape(control) +
               r'\.lean:\d+:\d+: error: unsolved goals\s*\n\s*⊢ False\s*')
    if re.fullmatch(pattern, text) is None:
        raise ValueError('negative did not fail solely on the intended False goal')

def check_types(text: str) -> None:
    names = re.findall(r'^@?CapI4\.(\w+)(?:\.\{[^}]*\})?\s*:', text, re.M)
    if names != TARGETS:
        raise ValueError('elaborated type inventory mismatch')

class Controls(unittest.TestCase):
    def setUp(self) -> None:
        self.text = (HERE/'CapI4.lean').read_text()
    def test_contract(self) -> None:
        check_contract(self.text)
    def test_reject_trust_escape(self) -> None:
        for bad in ['axiom stolen : False', 'theorem bad : False := by sorry',
                    'example : True := by native_decide']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                check_contract(self.text+'\n'+bad)
    def test_reject_missing_target(self) -> None:
        with self.assertRaises(ValueError):
            check_contract(self.text.replace('theorem cap_cubic_of_tails', 'theorem renamed'))
    def test_reject_dropped_factor(self) -> None:
        with self.assertRaises(ValueError):
            check_contract(self.text.replace('x * (x + E * r * U)', '(x + E * r * U)'))
    def test_reject_wrong_radius(self) -> None:
        with self.assertRaises(ValueError):
            check_contract(self.text.replace('r ^ 2 * P * U ^ (2 * m)', 'r * P * U ^ (2 * m)'))
    def test_reject_threshold_change(self) -> None:
        with self.assertRaises(ValueError):
            check_contract(self.text.replace('3 * k / 10 < r * M4 x', '3 * k / 10 ≤ r * M4 x'))
    def test_reject_unclosed_comment(self) -> None:
        with self.assertRaises(ValueError):
            check_contract(self.text+'\n/-')
    def test_audit_missing_and_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'log'
            p.write_text('')
            with self.assertRaises(ValueError): check_audit(p)
            p.write_text('\n'.join(f"'CapI4.{n}' depends on axioms: [sorryAx]" for n in TARGETS))
            with self.assertRaises(ValueError): check_audit(p)

class EvidenceControls(unittest.TestCase):
    def test_intended_false_goals(self) -> None:
        for name in sorted(NEGATIVES):
            check_negative_text(name, 1, f'/tmp/{name}.lean:3:50: error: unsolved goals\n⊢ False\n')
    def test_import_failure(self) -> None:
        with self.assertRaises(ValueError):
            check_negative_text('RejectDroppedSoft', 1, 'RejectDroppedSoft.lean:1:0: error: unknown module CapI4\n')
    def test_type_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            check_negative_text('RejectDroppedFar', 1, 'RejectDroppedFar.lean:5:2: error: type mismatch\n')
    def test_crash_timeout_and_success(self) -> None:
        text = 'RejectDroppedSoft.lean:3:50: error: unsolved goals\n⊢ False\n'
        for status in [0, 2, 124, 137, 139, -11]:
            with self.subTest(status=status), self.assertRaises(ValueError):
                check_negative_text('RejectDroppedSoft', status, text)
    def test_combined_error_is_not_a_pass(self) -> None:
        text = 'RejectDroppedSoft.lean:3:50: error: unsolved goals\n⊢ False\n'
        with self.assertRaises(ValueError):
            check_negative_text('RejectDroppedSoft', 1, text+'error: unknown module\n')
    def test_wrong_file_or_nonfalse_goal(self) -> None:
        for text in ['Other.lean:3:50: error: unsolved goals\n⊢ False\n',
                     'RejectDroppedSoft.lean:3:50: error: unsolved goals\n⊢ True\n', '']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                check_negative_text('RejectDroppedSoft', 1, text)
    def test_line_wrapped_universe_headers(self) -> None:
        text = '\n'.join(f'@CapI4.{n}.{{u_1,\n    u_2}} : Prop' for n in TARGETS)
        check_types(text)
        with self.assertRaises(ValueError):
            check_types(text.replace('u_2} :', 'u_2 :', 1))
    def test_type_universes_and_missing_or_duplicate(self) -> None:
        text = '\n'.join(f'@CapI4.{n}.{{u_1, u_2}} : Prop' for n in TARGETS)
        check_types(text)
        for bad in [text.split('\n', 1)[1], text+'\n'+text.split('\n')[0], '']:
            with self.assertRaises(ValueError): check_types(bad)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['source', 'self-test', 'emit', 'audit', 'negative', 'types'])
    ap.add_argument('path', nargs='?', type=Path)
    ap.add_argument('--control', choices=sorted(NEGATIVES))
    ap.add_argument('--status', type=int)
    args = ap.parse_args()
    if args.mode == 'source': source_check()
    elif args.mode == 'self-test':
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                                   for c in [Controls, EvidenceControls])
        raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
    elif args.mode == 'emit':
        if args.path is None: ap.error('emit requires output directory')
        emit(args.path)
    elif args.mode == 'audit':
        if args.path is None: ap.error('audit requires log path')
        check_audit(args.path)
    elif args.mode == 'types':
        if args.path is None: ap.error('types requires log path')
        check_types(args.path.read_text())
        print(json.dumps({'elaborated_types': 'PASS', 'declarations': len(TARGETS)}))
    else:
        if args.path is None or args.control is None or args.status is None:
            ap.error('negative requires log path, --control and --status')
        check_negative_text(args.control, args.status, args.path.read_text())
        print(json.dumps({'control': args.control, 'status': args.status, 'reason': 'CONCRETE_FALSE_GOAL'}))
