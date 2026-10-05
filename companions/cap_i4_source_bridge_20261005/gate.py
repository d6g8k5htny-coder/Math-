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
    for row in git('diff', '--name-status', BASE, 'HEAD').splitlines():
        state, path = row.split('\t', 1)
        if state != 'A' or path not in allowed:
            raise ValueError(f'out-of-scope change: {row}')
    print(json.dumps({'source_gate': 'PASS', 'head': git('rev-parse', 'HEAD'),
        'base': BASE, 'source_path': SOURCE, 'source_blob': SOURCE_BLOB,
        'source_sha256': hashlib.sha256((ROOT/SOURCE).read_bytes()).hexdigest(),
        'companion_sha256': hashlib.sha256((HERE/'CapI4.lean').read_bytes()).hexdigest(),
        'audited_declarations': len(TARGETS), 'scientific_effect': 'NONE'}))

def emit(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out/'Audit.lean').write_text('import CapI4\n' + '\n'.join(
        '#print axioms CapI4.' + n for n in TARGETS) + '\n')
    (out/'Positive.lean').write_text('''import CapI4
open MeasureTheory
example : CapI4.depthEvent 1 1 (fun _ : Unit => 4/3) (fun _ => 1) = Set.univ := by
  ext x; norm_num [CapI4.depthEvent]
example : CapI4.fourthEvent 1 1 (fun _ : Unit => 3/10) = ∅ := by
  ext x; norm_num [CapI4.fourthEvent]
example : (∫ x in (0 : ℝ)..1, x * (x + 1)) = 5/6 := by
  rw [CapI4.double_soft_integral]; norm_num
example : (8 : ℝ) ≤ 4 ∨ 1/4 < 8 := by norm_num
''')
    (out/'RejectDroppedSoft.lean').write_text('''import CapI4
open MeasureTheory
example : (∫ x in (0 : ℝ)..1, x * (x + 1)) = 1/3 := by
  rw [CapI4.double_soft_integral]; norm_num
''')
    (out/'RejectDroppedFar.lean').write_text('''import CapI4
example : ∀ (l J D r : ℝ), 0 < D → 0 < r → 0 < l →
    l ≤ 2*D*r*J^2 + 2*D*r*l^2 → l ≤ 4*D*r*J^2 := by
  intro l J D r hD hr hl hd
  exact CapI4.scalar_near_or_far l J D r hD hr hl hd
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

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['source', 'self-test', 'emit', 'audit'])
    ap.add_argument('path', nargs='?', type=Path)
    args = ap.parse_args()
    if args.mode == 'source': source_check()
    elif args.mode == 'self-test':
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
    elif args.mode == 'emit':
        if args.path is None: ap.error('emit requires output directory')
        emit(args.path)
    else:
        if args.path is None: ap.error('audit requires log path')
        check_audit(args.path)
