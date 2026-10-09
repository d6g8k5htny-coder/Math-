#!/usr/bin/env python3
"""Finer outward rectangle enclosure using the frozen Math-#362 primitives.

This separate driver does not change its parent's grid limit or saved result.
All certified arithmetic is integer/Fraction. No finite-radius bound or Lean.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from math import isqrt
import os
from pathlib import Path
import stat
import sys
import types

PARENT_COMMIT = '1f64b8f8ee450262e0f56e6bdf9dfb37931f48c6'
PARENT_SHA256 = '157e02ee22699b4fa2efdde1894824b92b962900dbb8da9bd65acee41ae91e88'
PARENT_BYTES = 7215
MAX_GRID = 8192
DEFAULT_GRID = 4096
R, T = 12, 4


def load_source(path):
    """Hash the exact regular-file bytes before compiling those same bytes."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size != PARENT_BYTES:
            raise ValueError('parent source identity mismatch')
        raw = stream.read(PARENT_BYTES + 1)
    if len(raw) != PARENT_BYTES or hashlib.sha256(raw).hexdigest() != PARENT_SHA256:
        raise ValueError('parent source identity mismatch')
    module = types.ModuleType('frozen_lm006_enclosure')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


@lru_cache(maxsize=1)
def parent():
    path = Path(__file__).resolve().parent.parent / 'lm006_wrong_sign_20261006_r20' / 'enclose.py'
    return load_source(path)


def validate_grid(n):
    if type(n) is not int:
        raise TypeError('integer grid required')
    if not 2 <= n <= MAX_GRID:
        raise ValueError('grid must lie in [2,8192]')
    return n


def row_stop(i, n):
    """First zero-upper cell: 32*k^2 >= 24*(i+1)*n, including equality."""
    validate_grid(n)
    if type(i) is not int or not 0 <= i < n:
        raise ValueError('row index outside grid')
    d1 = 2*R*(i+1)*n
    return min(n, isqrt((d1-1)//(2*T*T)) + 1)


def refinement(n=DEFAULT_GRID):
    n = validate_grid(n)
    p = parent()
    parameters = p.parameters()
    v = parameters['variance_D']
    d_pdf = [p.density(F(R*i, n), v) for i in range(n+1)]
    b_pdf = [p.density(F(T*i, n), (v[0]/4, v[1]/4)) for i in range(n+1)]
    dl = [p.fixed(t[0])[0] for t in d_pdf]
    du = [p.fixed(t[1])[1] for t in d_pdf]
    bl = [p.fixed(t[0])[0] for t in b_pdf]
    bu = [p.fixed(t[1])[1] for t in b_pdf]
    u = [2*T*T*k*k for k in range(n+1)]
    q = 2*n*n
    lower = upper = evaluated = 0
    jnum = p._jnum
    for i in range(n):
        d0 = 2*R*i*n
        d1 = d0 + 2*R*n
        stop = row_stop(i, n)
        evaluated += stop
        # Every omitted cell has u0>=d1 and hence identically zero J.
        for k in range(stop):
            u0, u1 = u[k], u[k+1]
            jlo = min(jnum(d0, u0), jnum(d0, u1))
            jhi = jnum(d1, min(max(d1//2, u0), u1))
            lower += jlo*dl[i+1]*bl[k+1]
            upper += jhi*du[i]*bu[k]
    factor = F(2*R*T, n*n*6*q**3*p.SCALE*p.SCALE)
    low, high = lower*factor, upper*factor
    # Same union-bound tails as the source, added only to the upper endpoint.
    tail_d = (v[1]*R*R + 2*v[1]**2)*d_pdf[-1][1]/24
    mean_d3 = 2*v[1]**2*d_pdf[0][1]
    tail_b = mean_d3/24*(v[1]/(2*T))*b_pdf[-1][1]
    tail = tail_d + tail_b
    gamma = (low, high + tail)
    coefficient = (gamma[0]*parameters['p0'][0]/parameters['z0'][1],
                   gamma[1]*parameters['p0'][1]/parameters['z0'][0])
    return {'grid': n, 'gamma': gamma, 'coefficient': coefficient,
            'tail': tail, 'parameters': parameters,
            'evaluated_cells': evaluated, 'zero_cells': n*n-evaluated}


def output(n):
    result = refinement(n)
    p = parent()
    def pair(a):
        return [p.decimal_bound(a[0]), p.decimal_bound(a[1], upper=True)]
    return {'scientific_effect': 'NONE', 'independently_reviewed': False,
            'meaning': 'separate finer-grid outward execution of the #362 rectangle formula',
            'source_commit': PARENT_COMMIT, 'source_sha256': PARENT_SHA256,
            'grid': n, 'evaluated_cells': result['evaluated_cells'],
            'zero_cells': result['zero_cells'],
            'coefficient': pair(result['coefficient']), 'gamma': pair(result['gamma']),
            'tail_gamma_upper': p.decimal_bound(result['tail'], places=18, upper=True),
            'z0': pair(result['parameters']['z0']), 'p0': pair(result['parameters']['p0']),
            'arithmetic': 'integer/Fraction; unchanged outward fixed-point scale 10^36',
            'scope': 'd2, L24, b6/5, original axes, six pins and gap r^3/6; no finite-r error bound'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grid', type=int, default=DEFAULT_GRID)
    args = parser.parse_args()
    try:
        result = output(args.grid)
    except (ValueError, TypeError, ArithmeticError, OSError) as exc:
        print('REFINEMENT_FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
