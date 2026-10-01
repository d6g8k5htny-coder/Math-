"""Tests and implementation mutants for C52-ALL-D.

    python3 -B -S test_check.py -v          # unit tests
    python3 -B -S test_check.py --mutants   # each mutant of check.py must make the tests fail, in -B -S and -B -O -S"""
from fractions import Fraction as Fr
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as C          # noqa: E402
import verify_sources as V  # noqa: E402


class Sources(unittest.TestCase):
    def test_seven_sources(self):
        n, cited = V.verify()
        self.assertEqual(n, 7)
        self.assertEqual(set(cited), {'C52-FOLD', 'C52-PROOF'})

    def test_historical_rejections(self):
        import json
        man = json.loads((V.HERE / 'SOURCES.json').read_text())
        good = dict(man['current_required'][0])
        V.historical(good)
        other = man['current_required'][1]
        for bad in (dict(good, blob=other['blob']),                      # wrong blob at that commit/path
                    dict(good, path=other['path']),                      # another path at that commit
                    dict(good, commit='0' * 40),                         # absent commit
                    dict(good, sha256='0' * 64),                         # wrong recorded digest
                    dict(good, bytes=good['bytes'] + 1),                 # wrong recorded size
                    dict(good, path='../' + good['path'])):              # noncanonical path
            with self.assertRaises(ValueError):
                V.historical(bad)


class PinTransform(unittest.TestCase):
    def test_det_and_target(self):
        for d in range(2, 8):
            for r in (Fr(1, 2), Fr(3, 11)):
                self.assertEqual(abs(C.det(C.pin_transform(d, r))), 12 * r ** -(d + 3))
                self.assertEqual(C.pin_target(d, r, 2, Fr(1, 3)), C.expected_target(d, r, 2, Fr(1, 3)))

    def test_target_shape(self):
        v = C.expected_target(3, Fr(1, 2), 1, 2)
        self.assertEqual(v[:4], [1 - Fr(2, 16), -Fr(1, 2), 0, 24])
        self.assertEqual(len(v), 2 * 3 + 2)


class Ridge(unittest.TestCase):
    def test_identities(self):
        rng = random.Random(7)
        for m in (1, 2, 3):
            for _ in range(2):
                F, _ = C.random_ridge_poly(m, rng)
                J = C.ridge_jets(F, m)
                self.assertEqual(J['g1'], J['Fx'])
                self.assertEqual(J['g2'], J['schur'])
                self.assertEqual(J['g2'], J['D2vv'])
                self.assertEqual(J['g3'], J['D3vvv'])
                self.assertEqual(J['psi1'], J['psi1_formula'])

    def test_contact(self):
        rng = random.Random(11)
        for m in (1, 2, 3):
            F, k = C.random_ridge_poly(m, rng, contact=True)
            J = C.ridge_jets(F, m)
            self.assertEqual((J['g1'], J['g2'], J['g3']), (0, 0, 12 * k))

    def test_known_ridge(self):
        # F = x^3 + x y - y^2 (m = 1): psi = x/2, g = x^3 + x^2/4; g'' = 1/2, g''' = 6
        F = {(3, 0): Fr(1), (1, 1): Fr(1), (0, 2): Fr(-1)}
        J = C.ridge_jets(F, 1)
        self.assertEqual(J['psi1'], [Fr(1, 2)])
        self.assertEqual((J['g1'], J['g2'], J['g3']), (0, Fr(1, 2), 6))
        self.assertEqual(J['Fxxx'], 6)
        # F = x y^2/2 ... with a curved ridge: F = x y - y^2 + x^2 y: psi = (x + x^2)/2, g = (x + x^2)^2/4
        F = {(1, 1): Fr(1), (0, 2): Fr(-1), (2, 1): Fr(1)}
        J = C.ridge_jets(F, 1)
        self.assertEqual((J['g2'], J['g3']), (Fr(1, 2), 3))
        self.assertNotEqual(J['g3'], J['Fxxx'])


class Inertia(unittest.TestCase):
    def test_signatures(self):
        self.assertEqual(C.inertia([[1, 0], [0, -1]]), (1, 0, 1))
        self.assertEqual(C.inertia([[0, 1], [1, 0]]), (1, 0, 1))
        self.assertEqual(C.inertia([[-1, 0, 0], [0, -2, 0], [0, 0, 0]]), (2, 1, 0))
        self.assertEqual(C.inertia([[2, 1], [1, -3]]), (1, 0, 1))


class Counts(unittest.TestCase):
    def test_mesh(self):
        self.assertEqual(C.mesh_counts(2), {'Z_M': (3, 4), 'Z_V': (4, 5), 'Z_b': (2, 3)})
        self.assertEqual(C.mesh_counts(4), {'Z_M': (7, 8), 'Z_V': (8, 9), 'Z_b': (4, 5)})

    def test_hv(self):
        self.assertEqual(C.rank(C.hv_matrix([Fr(0), Fr(0), Fr(1)])), 3)
        self.assertEqual(C.rank(C.hv_matrix([Fr(0), Fr(0), Fr(0)])), 0)

    def test_ledger(self):
        for d in range(2, 12):
            self.assertEqual(C.ledger_exponent(d), 1)

    def test_jacobian(self):
        self.assertEqual(*C.lifetime_jacobian(Fr(1, 8), Fr(27, 64), Fr(1, 125)))


class Whole(unittest.TestCase):
    def test_run(self):
        self.assertEqual(C.run(verbose=False), 0)


MUTANTS = [
    ("T[0][0] = T[0][2] = Fr(1, 2)", "T[0][0] = T[0][2] = Fr(1, 3)"),
    ("s = 6 / r ** 2", "s = 5 / r ** 2"),
    ("T[3][0], T[3][2] = 2 * s / r, -2 * s / r", "T[3][0], T[3][2] = s / r, -2 * s / r"),
    ("T[ic][ia], T[ic][ic] = -1 / r, 1 / r", "T[ic][ia], T[ic][ic] = -1 / r, 2 / r"),
    ("return [b - k * r ** 3 / 2, -k * r ** 2, Fr(0), 12 * k]", "return [b - k * r ** 3 / 2, -k * r ** 2, Fr(0), 6 * k]"),
    ("def det_exponent(d):\n    return d + 3", "def det_exponent(d):\n    return d + 2"),
    ("g1, g2, g3 = g[1], 2 * g[2], 6 * g[3]", "g1, g2, g3 = g[1], 2 * g[2], 3 * g[3]"),
    ("schur = Fxx - sum(", "schur = Fxx + sum("),
    ("v = [Fr(1)] + [psi[j][1] for j in range(m)]", "v = [Fr(1)] + [Fr(0) for j in range(m)]"),
    ("'psi1_formula': [-t for t in w]", "'psi1_formula': [t for t in w]"),
    ("F[(3,) + (0,) * m] = 2 * k", "F[(3,) + (0,) * m] = k"),
    ("return {'Z_M': (d + (d - 1), 2 * d)", "return {'Z_M': (d + d, 2 * d)"),
    ("M[i][c] += v[j]\n        if i != j:", "M[i][c] += v[j]\n        if False:"),
    ("return (d - 1) + 3 - det_exponent(d) + 2", "return (d - 1) + 2 - det_exponent(d) + 2"),
    ("lhs = r * r / (3 * y)", "lhs = r * r / (2 * y)"),
    ("neg, pos = neg + (p < 0), pos + (p > 0)", "neg, pos = neg + (p > 0), pos + (p < 0)"),
    ("for _ in range(NS + 1):", "for _ in range(1):"),
]


def run_mutants():
    src = open(os.path.join(HERE, 'check.py')).read()
    survivors = 0
    for i, (a, b) in enumerate(MUTANTS):
        if src.count(a) != 1:
            print('mutant %d: anchor not unique/absent: %r' % (i, a))
            survivors += 1
            continue
        tmp = tempfile.mkdtemp()
        try:
            for f in ('test_check.py', 'verify_sources.py', 'SOURCES.json'):
                shutil.copy(os.path.join(HERE, f), tmp)
            open(os.path.join(tmp, 'check.py'), 'w').write(src.replace(a, b))
            killed = True
            for flags in (['-B', '-S'], ['-B', '-O', '-S']):
                env = dict(os.environ, C52D_SOURCE_ROOT=HERE)
                p = subprocess.run([sys.executable] + flags + [os.path.join(tmp, 'test_check.py'), '--mutant-run'],
                                   capture_output=True, text=True, env=env, timeout=300)
                killed = killed and p.returncode != 0
            print('mutant %2d %s' % (i, 'killed (both modes)' if killed else 'SURVIVED'))
            survivors += not killed
        finally:
            shutil.rmtree(tmp)
    print('mutants: %d of %d killed' % (len(MUTANTS) - survivors, len(MUTANTS)))
    return survivors


if __name__ == '__main__':
    if '--mutants' in sys.argv:
        sys.exit(1 if run_mutants() else 0)
    if '--mutant-run' in sys.argv:
        sys.argv.remove('--mutant-run')
        # sources are verified against the real tree; skip that test in the temporary copy
        del Sources
    unittest.main()
