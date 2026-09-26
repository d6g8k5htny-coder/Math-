#!/usr/bin/env python3
"""Fail-closed reader for the radius-scoped H5 rim envelope input."""
import ast
from decimal import Decimal, ROUND_DOWN, localcontext
import hashlib
import json
from pathlib import Path


ANGLES = (15, 45, 75, 105, 135, 150, 160, 165, 170, 175)


def strict_json(text):
    def pairs(items):
        row = {}
        for key, value in items:
            if key in row:
                raise ValueError('duplicate JSON object name: ' + key)
            row[key] = value
        return row

    def constant(value):
        raise ValueError('nonstandard JSON numeric constant: ' + value)

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def load_rim_constants(path, expected_radius):
    path = Path(path)
    radius = path.name.removeprefix('h5_results_r').split('_', 1)[0]
    if Decimal(radius) != expected_radius:
        raise ValueError('ledger filename radius does not match requested radius')

    block = {}
    block_failed = False
    values = None
    selected_failure = False
    for line in path.read_text().splitlines():
        row = strict_json(line)
        if row.get('part') == 'rimprobes_done':
            values = None if block_failed else block
            selected_failure = block_failed
            block = {}
            block_failed = False
        elif row.get('part') == 'rimprobe':
            if row['th'] in block:
                raise ValueError('duplicate rim angle in completed block')
            block[row['th']] = Decimal(row['rho_hi'])
        elif row.get('part') == 'rimprobe_fail':
            block_failed = True
    if block:
        raise ValueError('unterminated rimprobe block')
    if values is None:
        if selected_failure:
            raise ValueError('rimprobe failure row in selected completed block')
        raise ValueError('no completed rimprobe block')
    if len(values) != len(ANGLES) or set(values) != set(ANGLES):
        raise ValueError('completed-block rim coverage does not match required angles')
    if not all(value.is_finite() and value > 0 for value in values.values()):
        raise ValueError('completed-block rim bounds must be positive finite decimals')
    return {angle: values[angle] for angle in ANGLES}


def flat_envelope(values):
    result = {}
    for angle, value in values.items():
        with localcontext() as context:
            context.prec = len(value.as_tuple().digits) + 1
            result[angle] = Decimal(2) * value
    return result


def compare_historical_literal(hunt_path, values):
    tree = ast.parse(Path(hunt_path).read_bytes(), filename=str(hunt_path))
    assignment = next(
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'RHO_HI'
                for target in node.targets)
    )
    literal = ast.literal_eval(assignment.value)
    if tuple(literal) != ANGLES:
        raise ValueError('historical rim literal angles do not match contract')
    matching = []
    mismatching = []
    quantum = Decimal('1e-20')
    for angle in ANGLES:
        truncated = values[angle].quantize(quantum, rounding=ROUND_DOWN)
        if Decimal(literal[angle]) == truncated:
            matching.append(angle)
        else:
            mismatching.append(angle)
    with localcontext() as context:
        context.prec = 120
        factor = Decimal(literal[175]) / values[175]
    return {
        'matching_truncated_angles': matching,
        'mismatching_angles': mismatching,
        'angle_175_inflation_factor': factor,
    }


def reproduction_report(hunt_path, ledger_path):
    hunt_path = Path(hunt_path)
    ledger_path = Path(ledger_path)
    values = load_rim_constants(ledger_path, expected_radius=Decimal('0.05'))
    comparison = compare_historical_literal(hunt_path, values)
    envelope = flat_envelope(values)
    factor = comparison['angle_175_inflation_factor']
    if not Decimal('1e34') < factor < Decimal('1e35'):
        raise ValueError('angle-175 inflation factor left the documented bracket')
    return {
        'scientific_effect': 'NONE',
        'historical_hunt_sha256': hashlib.sha256(hunt_path.read_bytes()).hexdigest(),
        'ledger_sha256': hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        'matching_truncated_angles': comparison['matching_truncated_angles'],
        'mismatching_angles': comparison['mismatching_angles'],
        'angle_175_inflation_factor_bracket': ['1E+34', '1E+35'],
        'ledger_rho_hi_175': str(values[175]),
        'corrected_cflat_175': str(envelope[175]),
        'numerical_hunt_replayed': False,
        'bound_certified': False,
    }
