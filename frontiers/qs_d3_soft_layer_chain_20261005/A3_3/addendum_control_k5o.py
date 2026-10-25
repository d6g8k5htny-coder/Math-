#!/usr/bin/env python3
"""A3.3 control addendum for A33-S2-C1: the eigenvalue ordering of K5's cases, and an ordered negative-branch witness.

Usage:  python3 -B -S a33_k5o.py PATH/a33_exact.py            -> JSON on stdout, exit 0 iff every check passes
        python3 -B -S a33_k5o.py PATH/a33_exact.py --mutant Wk -> mutant W1 or W2; must exit 1
PATH/a33_exact.py is the frozen A3.3 executable (23,144 bytes, SHA-256 6d061461...7071); it is hashed, then imported
read-only. Standard library only; exact Fractions; no check depends on an assert; byte-identical output under -O.

  O1  Replays K5's sampling exactly (seed 20261004, after K1-K4) and classifies each grid case by the ordering
      lambda1 = r*lambda_tilde/k <= lambda2 of A3.3 §2. Also classifies K5's explicit negative example.
  O2  The ordered witness of OpenAI / GPT-6 Astra Pro (main#229 comment 5999623189), re-derived exactly:
      f = b - k r^3/2 + 2k x^3 - (3/2)k r^2 x + (1/2)(2r^2 - 12x^2) y^2 + (1/2)(r^2 - 8x^2) z^2.
      Pins exact; midpoint eigenframe with lambda1 = -2r^2 < lambda2 = -r^2 < 0; pin Hessians diag(-6kr,-r^2,-r^2)
      and diag(6kr,-r^2,-r^2); W_r/r^4 = 36 k^2 r^6 > 0; model weight 0; K5's test form with C0 = 2 holds.
Mutants: W1 flips the sign of the z^2 correction (pins untyped); W2 exchanges the transverse curvatures (unordered).
"""
import hashlib
import importlib.util
import json
import random
import sys
from fractions import Fraction as Fr

SHA = '6d061461e49a43277b9405466c437ca1d2c1246d74de8d5d23f73b94e4467071'
args = sys.argv[1:]
MUT = None
if len(args) == 3 and args[1] == '--mutant' and args[2] in ('W1', 'W2'):
    MUT = args[2]
elif len(args) != 1:
    sys.stderr.write('usage: a33_k5o.py PATH/a33_exact.py [--mutant W1|W2]\n')
    sys.exit(2)
FAIL = []


def fail(msg):
    FAIL.append(msg)


def load(path):
    try:
        data = open(path, 'rb').read()
    except OSError:
        sys.stderr.write('cannot read %s\n' % path)
        sys.exit(2)
    if hashlib.sha256(data).hexdigest() != SHA or len(data) != 23144:
        fail('a33_exact.py is not the frozen A3.3 executable')
        return None
    spec = importlib.util.spec_from_file_location('a33_exact_frozen', path)
    mod = importlib.util.module_from_spec(spec)
    saved = sys.argv
    sys.argv = [path]
    spec.loader.exec_module(mod)
    sys.argv = saved
    return mod


def o1(mod):
    random.seed(20261004)
    mod.k1()
    mod.k2()
    mod.k3()
    mod.k4()
    seen = []
    orig = mod.pinned_field

    def wrapped(r, k, b, lam1, lam2, free):
        seen.append((r, k, lam1, lam2))
        return orig(r, k, b, lam1, lam2, free)
    mod.pinned_field = wrapped
    res = mod.k5()
    mod.pinned_field = orig
    grid = seen[:-3]                      # the last three calls: the explicit example and the two (3.5) checks
    neg = seen[-3]
    out = {'grid_cases': len(grid), 'ordered': 0, 'unordered_lam2_le_0': 0, 'unordered_lam2_gt_0': 0,
           'ordered_lam2_le_0': 0}
    for (r, k, lam1, lam2) in grid:
        if lam1 <= lam2:
            out['ordered'] += 1
            if lam2 <= 0:
                out['ordered_lam2_le_0'] += 1
        elif lam2 <= 0:
            out['unordered_lam2_le_0'] += 1
        else:
            out['unordered_lam2_gt_0'] += 1
    r, k, lam1, lam2 = neg
    out['explicit_example'] = {'lambda1': str(lam1), 'lambda2': str(lam2), 'ordered': lam1 <= lam2}
    if len(grid) != 576 or res['cases'] != 576:
        fail('O1: K5 grid size')
    if out['unordered_lam2_le_0'] != res['grid_cases_lam2_le_0'] or out['ordered_lam2_le_0'] != 0:
        fail('O1: the lambda2 <= 0 cases are not all unordered')
    if neg[2] <= neg[3]:
        fail('O1: the explicit example is ordered')
    return out


def witness(r, k, b):
    """Coefficients c_al of f = sum c_al z^al / al! for the ordered witness."""
    c = {}
    c[(0, 0, 0)] = b - k * r ** 3 / 2
    c[(3, 0, 0)] = 12 * k                 # 2k x^3
    c[(1, 0, 0)] = -Fr(3, 2) * k * r * r
    sy, sz = (Fr(2), Fr(1)) if MUT != 'W2' else (Fr(1), Fr(2))
    tz = Fr(-8) if MUT != 'W1' else Fr(8)
    c[(0, 2, 0)] = sy * r * r             # (1/2)(2 r^2) y^2
    c[(2, 2, 0)] = Fr(-24)                # (1/2)(-12 x^2) y^2 = -6 x^2 y^2 = c x^2 y^2/(2!2!)
    c[(0, 0, 2)] = sz * r * r             # (1/2)(r^2) z^2
    c[(2, 0, 2)] = 2 * 2 * tz / 2         # (1/2)(tz x^2) z^2
    return c


def o2(mod):
    worst = Fr(0)
    wmin = None
    n = 0
    for r in (Fr(1, 100), Fr(1, 1000), Fr(1, 10000)):
        for k in (Fr(1, 2), Fr(1), Fr(3, 2), Fr(2)):
            for b in (Fr(0), Fr(3, 2)):
                c = witness(r, k, b)
                cc = {al: c.get(al, Fr(0)) for al in mod.MULTI}
                vM, gM, HM = mod.eval_derivs(cc, (-r / 2, Fr(0), Fr(0)))
                vS, gS, HS = mod.eval_derivs(cc, (r / 2, Fr(0), Fr(0)))
                if vM != b or vS != b - k * r ** 3 or any(gM) or any(gS):
                    fail('O2: pins not exact')
                _, _, H0 = mod.eval_derivs(cc, (Fr(0), Fr(0), Fr(0)))
                A = [[H0[1][1], H0[1][2]], [H0[2][1], H0[2][2]]]
                if A[0][1] != 0:
                    fail('O2: not the eigenframe')
                lam1, lam2 = -A[0][0], -A[1][1]          # soft e1 = y, hard e2 = z
                if not (lam1 < lam2 < 0):
                    fail('O2: not ordered with lambda2 < 0 (r=%s k=%s)' % (r, k))
                if HM != [[-6 * k * r, 0, 0], [0, -r * r, 0], [0, 0, -r * r]] or \
                        HS != [[6 * k * r, 0, 0], [0, -r * r, 0], [0, 0, -r * r]]:
                    fail('O2: pin Hessians')
                W = mod.Fj(HM, 3) * mod.Fj(HS, 2) / r ** 4
                if W != 36 * k * k * r ** 6 or not W > 0:
                    fail('O2: W_r/r^4')
                lt = k * lam1 / r
                gam, B = cc[(2, 1, 0)], cc[(1, 2, 0)]
                Y = 3 * k * B - gam * gam / 4
                w = max(6 * lt + Y, Fr(0)) * max(6 * lt - Y, Fr(0))
                model = max(lam2, Fr(0)) ** 2 * w
                if model != 0:
                    fail('O2: model weight')
                Nf = 1 + max(abs(v) for al, v in cc.items() if sum(al) >= 3 and al != (3, 0, 0))
                Pi = 1 + abs(lt) + gam * gam + abs(B) + Nf
                ratio = abs(W - model) / (r * Nf * (abs(lam2) + r * Nf) * Pi ** 2)
                if ratio > 2:
                    fail('O2: K5 test form')
                worst = max(worst, ratio)
                wmin = W if wmin is None else min(wmin, W)
                n += 1
    return {'cases': n, 'Nf': str(Nf), 'max_ratio_C0_form': str(worst.limit_denominator(10 ** 30)),
            'min_W_over_r4': str(wmin)}


def main():
    mod = load(args[0])
    out = {'object': 'A3.3 control addendum for A33-S2-C1', 'scientific_effect': 'NONE'}
    if mod is not None:
        out['O1'] = o1(mod)
        out['O2'] = o2(mod)
    out['passed'] = not FAIL
    if FAIL:
        sys.stderr.write('FAILED:\n' + '\n'.join(FAIL[:20]) + '\n')
        sys.stdout.write(json.dumps(out, sort_keys=True) + '\n')
        sys.exit(1)
    sys.stdout.write(json.dumps(out, sort_keys=True) + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
