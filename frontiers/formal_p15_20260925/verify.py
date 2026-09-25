#!/usr/bin/env python3
"""Exact-real P15 sublemma checks via Z3's C API; Python standard library only.

This writes NEW evidence, never scientific statuses. libz3 is an explicit native
runtime requirement. SMT proof exports are not independently kernel-rechecked.
"""
from __future__ import annotations

import argparse
import ctypes as C
import ctypes.util
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OPS = {'+', '-', '*', '/', '=', '<', '<=', '>', '>=', 'and', 'or', 'not'}
NAME = re.compile(r'[A-Za-z][A-Za-z0-9_]*\Z')
NUMBER = re.compile(r'[0-9]+\Z')

class VerificationError(ValueError):
    pass


def parse_expr(text: str, variables: set[str]) -> Any:
    """Accept one formula only; no SMT commands, extra assertions, or includes."""
    if not isinstance(text, str) or len(text) > 20000:
        raise VerificationError('invalid expression')
    tokens = re.findall(r'\(|\)|[^\s()]+', text)
    pos = 0

    def take(depth: int = 0) -> Any:
        nonlocal pos
        if depth > 80 or pos >= len(tokens):
            raise VerificationError('truncated/deep expression')
        token = tokens[pos]
        pos += 1
        if token == '(':
            if pos >= len(tokens) or tokens[pos] not in OPS:
                raise VerificationError('unsupported operator')
            op = tokens[pos]
            pos += 1
            args = []
            while pos < len(tokens) and tokens[pos] != ')':
                args.append(take(depth + 1))
            if pos == len(tokens):
                raise VerificationError('unclosed expression')
            pos += 1
            n = len(args)
            good = ((op == 'not' and n == 1) or
                    (op in {'=', '<', '<=', '>', '>=', '/'} and n == 2) or
                    (op == '-' and n in {1, 2}) or
                    (op in {'+', '*', 'and', 'or'} and n >= 2))
            if not good:
                raise VerificationError('operator arity mismatch')
            return (op, args)
        if token in variables or NUMBER.fullmatch(token):
            return token
        raise VerificationError(f'unsupported atom: {token}')

    tree = take()
    if pos != len(tokens):
        raise VerificationError('more than one expression')
    return tree


def exact_eval(tree: Any, values: dict[str, Fraction]) -> Fraction | bool:
    """Independent rational evaluation of explicit witnesses, not universality."""
    if isinstance(tree, str):
        return values[tree] if tree in values else Fraction(tree)
    op, args = tree
    xs = [exact_eval(a, values) for a in args]
    if op in {'and', 'or', 'not'}:
        if any(type(v) is not bool for v in xs):
            raise VerificationError('non-Boolean logical operand')
        return all(xs) if op == 'and' else any(xs) if op == 'or' else not xs[0]
    if any(type(v) is not Fraction for v in xs):
        raise VerificationError('non-rational arithmetic operand')
    if op == '+':
        return sum(xs, Fraction(0))
    if op == '*':
        out = Fraction(1)
        for x in xs:
            out *= x
        return out
    if op == '-':
        return -xs[0] if len(xs) == 1 else xs[0] - xs[1]
    if op == '/':
        if xs[1] == 0:
            raise VerificationError('zero denominator in exact witness')
        return xs[0] / xs[1]
    if op == '=':
        return xs[0] == xs[1]
    if op == '<':
        return xs[0] < xs[1]
    if op == '<=':
        return xs[0] <= xs[1]
    if op == '>':
        return xs[0] > xs[1]
    if op == '>=':
        return xs[0] >= xs[1]
    raise VerificationError('unsupported evaluation')


def validate_case(case: dict[str, Any]) -> None:
    if (not isinstance(case, dict) or type(case.get('id')) is not str
        or not NAME.fullmatch(case['id'])):
        raise VerificationError('invalid case id')
    variables = case.get('variables')
    if (not isinstance(variables, list) or
        any(not isinstance(v, str) or not NAME.fullmatch(v) for v in variables) or
        len(set(variables)) != len(variables)):
        raise VerificationError('invalid variables')
    if case.get('role') not in {'theorem', 'mutant'}:
        raise VerificationError('invalid role')
    if not isinstance(case.get('hypotheses'), list):
        raise VerificationError('hypotheses must be a list')
    witness = case.get('witness')
    if not isinstance(witness, dict) or set(witness) != set(variables):
        raise VerificationError('witness must bind every variable exactly once')
    if any(type(v) is not str for v in witness.values()):
        raise VerificationError('witness values must be exact rational strings')
    try:
        values = {k: Fraction(v) for k, v in witness.items()}
        for formula in case['hypotheses']:
            if exact_eval(parse_expr(formula, set(variables)), values) is not True:
                raise VerificationError('witness fails a premise')
        result = exact_eval(parse_expr(case['conclusion'], set(variables)), values)
        expected = case['role'] == 'theorem'
        if type(result) is not bool or result != expected:
            raise VerificationError('witness does not demonstrate the intended case')
    except (ZeroDivisionError, KeyError, TypeError) as exc:
        raise VerificationError(str(exc)) from exc


def smt_rational(text: str) -> str:
    value = Fraction(text)
    n = str(abs(value.numerator))
    if value.numerator < 0:
        n = f'(- {n})'
    return n if value.denominator == 1 else f'(/ {n} {value.denominator})'


def build_query(case: dict[str, Any], *, witness_only: bool = False) -> tuple[str, str]:
    validate_case(case)
    expected = 'sat' if witness_only or case['role'] == 'mutant' else 'unsat'
    lines = ['(set-option :produce-models true)',
             '(set-option :timeout 10000)', '(set-logic QF_NRA)']
    lines += [f'(declare-const {v} Real)' for v in case['variables']]
    lines += [f'(assert {h})' for h in case['hypotheses']]
    if witness_only:
        lines += [f'(assert (= {v} {smt_rational(q)}))' for v, q in case['witness'].items()]
    else:
        lines += [f'(assert (not {case["conclusion"]}))']
    lines += ['(check-sat)', '(get-proof)' if expected == 'unsat' else '(get-model)']
    return '\n'.join(lines) + '\n', expected


def check_response(output: str, expected: str) -> None:
    if expected not in {'sat', 'unsat'}:
        raise VerificationError('invalid expected result')
    lines = output.strip().splitlines()
    if not lines or lines[0].strip() != expected or '(error' in output:
        raise VerificationError(f'solver did not establish {expected}: {output[:400]}')
    if expected == 'unsat' and '(proof' not in output:
        raise VerificationError('missing proof export')


class Z3:
    """Small C-API adapter. Errors fail closed; no Z3 Python package required."""
    def __init__(self, library: str | None = None) -> None:
        name = library or ctypes.util.find_library('z3')
        if not name:
            raise VerificationError('libz3 not found; install it or pass --library')
        self.lib = C.CDLL(name)
        bindings = [
            ('Z3_mk_config', [], C.c_void_p),
            ('Z3_set_param_value', [C.c_void_p, C.c_char_p, C.c_char_p], None),
            ('Z3_mk_context', [C.c_void_p], C.c_void_p),
            ('Z3_del_config', [C.c_void_p], None),
            ('Z3_del_context', [C.c_void_p], None),
            ('Z3_eval_smtlib2_string', [C.c_void_p, C.c_char_p], C.c_char_p),
            ('Z3_get_error_code', [C.c_void_p], C.c_uint),
            ('Z3_get_error_msg', [C.c_void_p, C.c_uint], C.c_char_p),
            ('Z3_get_full_version', [], C.c_char_p),
        ]
        for fname, args, result in bindings:
            fn = getattr(self.lib, fname)
            fn.argtypes, fn.restype = args, result
        self.callback_type = C.CFUNCTYPE(None, C.c_void_p, C.c_uint)
        self.lib.Z3_set_error_handler.argtypes = [C.c_void_p, self.callback_type]
        self.lib.Z3_set_error_handler.restype = None
        self.version = self.lib.Z3_get_full_version().decode('utf-8')
        self.loaded_path = str(Path(name).resolve()) if Path(name).is_file() else None
        maps = Path('/proc/self/maps')
        if self.loaded_path is None and maps.is_file():
            for line in maps.read_text().splitlines():
                fields = line.split()
                if fields and '/libz3.' in fields[-1] and Path(fields[-1]).is_file():
                    self.loaded_path = str(Path(fields[-1]).resolve())
                    break
        self.library_sha256 = (hashlib.sha256(Path(self.loaded_path).read_bytes()).hexdigest()
                               if self.loaded_path else None)

    def run(self, query: str, expected: str) -> str:
        cfg = self.lib.Z3_mk_config()
        if not cfg:
            raise VerificationError('could not allocate Z3 config')
        self.lib.Z3_set_param_value(cfg, b'proof', b'true')
        ctx = self.lib.Z3_mk_context(cfg)
        self.lib.Z3_del_config(cfg)
        if not ctx:
            raise VerificationError('could not allocate Z3 context')
        errors: list[int] = []
        handler = self.callback_type(lambda _ctx, code: errors.append(int(code)))
        self.lib.Z3_set_error_handler(ctx, handler)
        try:
            raw = self.lib.Z3_eval_smtlib2_string(ctx, query.encode('utf-8'))
            output = raw.decode('utf-8') if raw else ''
            code = self.lib.Z3_get_error_code(ctx)
            if errors or code:
                message = self.lib.Z3_get_error_msg(ctx, code or errors[-1]).decode('utf-8')
                raise VerificationError(f'Z3 error: {message}; {output[:400]}')
            check_response(output, expected)
            return output
        finally:
            self.lib.Z3_del_context(ctx)


def verify_parent(path: Path, binding: dict[str, Any]) -> dict[str, Any]:
    """Require the exact original proof, not a renamed or stale reading copy."""
    raw = path.read_bytes()
    actual = {'size_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
              'git_blob_sha1': hashlib.sha1(
                  b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
    if any(binding.get(key) != value for key, value in actual.items()):
        raise VerificationError('parent proof byte identity mismatch')
    return actual


def run_suite(output: Path, library: str | None = None,
              source_proof: Path | None = None) -> dict[str, Any]:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise VerificationError('output must be outside the source directory')
    output.mkdir(parents=True, exist_ok=False)
    spec = json.loads((ROOT / 'SPEC.json').read_text(encoding='utf-8'))
    if (type(spec.get('schema_version')) is not int or spec['schema_version'] != 1
        or spec.get('scientific_effect') != 'NONE'
        or spec.get('parent_acceptance') is not False
        or spec.get('proof_assistant_checked') is not False):
        raise VerificationError('unsafe specification metadata')
    source_proof = source_proof or ROOT.parent / 'full_price_20260924' / 'PROOF.md'
    parent_identity = verify_parent(source_proof, spec['source'])
    cases = spec.get('cases')
    if not isinstance(cases, list) or not cases:
        raise VerificationError('missing cases')
    ids = [case['id'] for case in cases]
    if len(set(ids)) != len(ids):
        raise VerificationError('duplicate case ids')
    solver = Z3(library)
    rows = []
    for case in cases:
        validate_case(case)
        records = {}
        for witness_only in (True, False):
            suffix = 'witness' if witness_only else 'negation'
            query, expected = build_query(case, witness_only=witness_only)
            stem = f'{case["id"]}.{suffix}'
            query_path, log_path = output / (stem + '.smt2'), output / (stem + '.txt')
            query_path.write_text(query, encoding='utf-8')
            transcript = solver.run(query, expected)
            log_path.write_text(transcript, encoding='utf-8')
            records[suffix] = {'result': expected,
                'query_sha256': hashlib.sha256(query.encode()).hexdigest(),
                'transcript_sha256': hashlib.sha256(transcript.encode()).hexdigest()}
        rows.append({'id': case['id'], 'role': case['role'],
                     'exact_rational_witness_checked': True, 'checks': records})
    report = {'object': spec['object'], 'passed': True,
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'platform': platform.platform(),
        'optimized': bool(sys.flags.optimize), 'z3_version': solver.version,
        'library_path': solver.loaded_path, 'library_sha256': solver.library_sha256,
        'source': spec['source'], 'parent_identity_verified': parent_identity,
        'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(ROOT.iterdir()) if p.is_file()},
        'theorems_checked': sum(c['role'] == 'theorem' for c in cases),
        'false_variants_rejected': sum(c['role'] == 'mutant' for c in cases),
        'solver_queries': 2 * len(cases), 'cases': rows,
        'scientific_effect': 'NONE', 'parent_acceptance': False,
        'proof_assistant_checked': False, 'independent_proof_recheck': False,
        'independent_translation_review': False,
        'trust_boundary': 'Z3 implementation and this translation/runner; exported Z3 proof is not independently checked. No Lean build is claimed.'}
    (output / 'REPORT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--library')
    parser.add_argument('--source-proof', type=Path,
                        help='exact parent proof; default is sibling full_price_20260924/PROOF.md')
    args = parser.parse_args()
    try:
        report = run_suite(args.output, args.library, args.source_proof)
    except (VerificationError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f'FAIL CLOSED: {exc}', file=sys.stderr)
        return 1
    print(json.dumps({k: report[k] for k in ('passed', 'theorems_checked',
          'false_variants_rejected', 'solver_queries', 'z3_version', 'scientific_effect')}, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
