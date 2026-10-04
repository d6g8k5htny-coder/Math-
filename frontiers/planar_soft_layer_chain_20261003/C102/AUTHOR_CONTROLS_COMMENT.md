# C102 public reproducibility companion — additive controls only

The unchanged full author proof is [comment5967305153](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967305153): 28,794 bytes, SHA256 `1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628`. Its entire native body was read back and matched the frozen proof exactly.

`PUBLIC_CONTROLS.py` is an additive successor to the frozen `exact_controls.py`. The only source changes are renaming `test_exact_source_copies_and_unchanged_claim` to `test_exact_public_source_copies` and removing the two-line assertion that reads the private `CLAIM_READBACK.json` hash. All public source checks, finite mathematical controls and five mutant branches are unchanged. The private claim check belongs to custody verification, and is not needed to run the public mathematical controls.

The original frozen checker remains 7,129 bytes, SHA256 `e16dca3319ef81d9d5ea040b62fd828bd6807cbc99e8c9a806a7fa6fb22cc9b9`; the original execution/failure record remains 3,237 bytes, SHA256 `10848c138d6ae1543bc4f485a3e2364919264c304491ad475fbb988d512a68f0`. These records and all proof/source/claim bytes were preserved. The new results below do not relabel or replace that original run.

Extraction and execution: each of the three payloads below has a unique BEGIN/END marker pair and one fenced block. Save exactly the text inside that block, excluding fence and marker lines, as the named UTF-8 file with LF line endings and its single final newline. The listed size and SHA256 apply to the extracted file, not this whole comment. Place `PUBLIC_CONTROLS.py` and `SOURCE_IDENTITIES.json` together. Retrieve the seven public source bodies from the manifest URLs, preserving their stated extraction, and save them at each `local_path`; the checker verifies their byte sizes and hashes. The manifest's `copied_from` paths record relative predecessor provenance and are not runtime dependencies. Issue comments are mutable; verify the recorded hashes. Repository sources use exact commit/blob identities.

Using a Python executable that reports version 3.11.16, run `python3.11 -B -S PUBLIC_CONTROLS.py` and `python3.11 -B -O -S PUBLIC_CONTROLS.py`. For each mode also run with `--mutant` followed by each listed mutant; those commands must exit 1 with assertion failures. All twelve invocations were actually executed for the record below.

This is author-side publication by OpenAI/Codex reader_surface_audit, acting for Dylan Roy — delegated AI work. Root's analytical coordination is author-side work. Fresh nonauthor review remains separate; human review NONE; organizational independence 0; personal reading PENDING; scientific effect NONE. No actual elder-event rate, lifetime theorem, k approaching zero, or Conjecture7 closure is asserted by these controls.

PUBLIC_CONTROLS.py: 6927 bytes; SHA256 `de8c39b08178369e38a03cb27c79aa0523516455feaf3d20e6f8bec87c5c4a4f`.

<!-- BEGIN C102 PUBLIC_CONTROLS.py -->
```python
#!/usr/bin/env python3
"""Finite rational controls for C102; these do not prove its analytic claims."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import unittest

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--mutant', choices=['amplitude-law', 'jacobian-r', 'extra-k4',
                                       'soft-normalizer', 'sqrt-congruence'])
ARGS, REST = PARSER.parse_known_args()
MUTANT = ARGS.mutant
ROOT = Path(__file__).resolve().parent


def det(matrix):
    a = [list(map(F, row)) for row in matrix]
    ans = F(1)
    for col in range(len(a)):
        pivot = next((j for j in range(col, len(a)) if a[j][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            ans = -ans
        d = a[col][col]
        ans *= d
        for row in range(col+1, len(a)):
            factor = a[row][col] / d
            for j in range(col+1, len(a)):
                a[row][j] -= factor * a[col][j]
    return ans


def filtered(matrix, index):
    d = det(matrix)
    if index == 1:
        return max(-d, F(0))
    return max(d, F(0)) if matrix[0][0] < 0 else F(0)


def physical_jet_jacobian(r, k):
    if MUTANT == 'jacobian-r':
        return r
    return abs(det([[r/k, 0, 0, 0], [0, 1, 0, 0],
                    [0, 0, 1/k, 0], [0, 0, 0, 1/k**2]]))


def physical_hessian(raw, r, k):
    return [[r*k*raw[0][0], r*raw[0][1]],
            [r*raw[1][0], r*raw[1][1]/k]]


def weighted_product(raw_max, raw_saddle, r, k):
    value = (filtered(physical_hessian(raw_max, r, k), 2)
             * filtered(physical_hessian(raw_saddle, r, k), 1))
    return value * k**4 if MUTANT == 'extra-k4' else value


def original_conditional_covariance(k):
    # X,Y,Z independent unit Gaussians; condition on U=X+Y at target k.
    # Cov(F,U)=(1,1,0), Var(U)=2. The target belongs in the mean only.
    cross = [F(1), F(1), F(0)]
    covariance = [[F(i == j) - cross[i]*cross[j]/2 for j in range(3)]
                  for i in range(3)]
    if MUTANT == 'amplitude-law':
        covariance = [[k*k*x for x in row] for row in covariance]
    return covariance


def tilted_soft_mass(r, model_mass, full_z):
    numerator = r**5 * model_mass
    normalizer = r**2 * full_z
    if MUTANT == 'soft-normalizer':
        normalizer = numerator
    return numerator / normalizer


def normalizer_congruence_at_quarter(matrix):
    # r=1/4; E1 requires r^-1/2=2, not sqrt(r)=1/2.
    d = F(1, 2) if MUTANT == 'sqrt-congruence' else F(2)
    return [[d*d*matrix[0][0], d*matrix[0][1]],
            [d*matrix[1][0], matrix[1][1]]]


class ExactControls(unittest.TestCase):
    def test_original_covariance_is_not_multiplied_with_gap_target(self):
        self.assertEqual(original_conditional_covariance(F(2)),
                         [[F(1, 2), F(-1, 2), 0],
                          [F(-1, 2), F(1, 2), 0], [0, 0, 1]])

    def test_physical_four_jet_volume_keeps_all_three_gap_factors(self):
        self.assertEqual(physical_jet_jacobian(F(1, 10), F(2)), F(1, 160))
        self.assertEqual(physical_jet_jacobian(F(2, 9), F(3, 2)), F(32, 729))

    def test_anisotropic_congruence_cancels_extra_gap_weight(self):
        # lambda=1, gamma=2, B=1: h_M=8, h_S=4, product=32.
        maximum = [[F(-6), F(-1)], [F(-1), F(-3, 2)]]
        saddle = [[F(6), F(1)], [F(1), F(-1, 2)]]
        self.assertEqual(weighted_product(maximum, saddle, F(1, 10), F(2)),
                         F(2, 625))
        self.assertEqual(physical_hessian(maximum, F(1, 10), F(2)),
                         [[F(-6, 5), F(-1, 10)], [F(-1, 10), F(-3, 40)]])

    def test_rare_density_and_full_normalizer_ledger(self):
        # Physical jet density one at this target: mu density=32/16=2;
        # eta density=2/5 when the independent FULL z equals five.
        r, k = F(1, 10), F(2)
        maximum = [[F(-6), F(-1)], [F(-1), F(-3, 2)]]
        saddle = [[F(6), F(1)], [F(1), F(-1, 2)]]
        g = r**-5 * physical_jet_jacobian(r, k) * weighted_product(maximum, saddle, r, k)
        self.assertEqual(g, F(2))
        self.assertEqual(g / 5, F(2, 5))
        self.assertEqual(r**-3 * tilted_soft_mass(r, F(7), F(5)), F(7, 5))

    def test_inverse_square_root_congruence_preserves_normalizer_scale(self):
        h = [[F(-3), F(1, 2)], [F(1, 2), F(-2)]]
        self.assertEqual(normalizer_congruence_at_quarter(h),
                         [[F(-12), F(1)], [F(1), F(-2)]])
        self.assertEqual(det(normalizer_congruence_at_quarter(h)), F(23))

    def test_centered_six_pin_target_and_factor_twelve(self):
        r, k, b = F(1, 10), F(2), F(3)
        matrix = [[F(1, 2), 0, F(1, 2), 0, 0, 0],
                  [-1/r, 0, 1/r, 0, 0, 0],
                  [0, -1/r, 0, 1/r, 0, 0],
                  [12/r**3, 6/r**2, -12/r**3, 6/r**2, 0, 0],
                  [0, 0, 0, 0, F(1, 2), F(1, 2)],
                  [0, 0, 0, 0, -1/r, 1/r]]
        target = [b, 0, b-k*r**3, 0, 0, 0]
        self.assertEqual([sum(a*x for a, x in zip(row, target)) for row in matrix],
                         [F(2999, 1000), F(-1, 50), 0, 24, 0, 0])
        self.assertEqual(abs(det(matrix)), F(1200000))
        # r^-5 pins, r spatial, r^3 heights, r^2 full determinant.
        self.assertEqual(F(-5)+1+3+2, F(1))

    def test_filtered_off_diagonal_bound_includes_type_crossings(self):
        cases = [(F(a), F(b), F(c, 2)) for a in [-2, 0, 3]
                 for b in [-2, 0, 1] for c in [-3, 0, 2]]
        for a, b, c in cases:
            for index in [1, 2]:
                with self.subTest(a=a, b=b, c=c, index=index):
                    delta = abs(filtered([[a, c], [c, b]], index)
                                - filtered([[a, 0], [0, b]], index))
                    self.assertLessEqual(delta, c*c)
        # Exact crossing from a negative-definite matrix to an indefinite one.
        self.assertEqual(filtered([[-1, 2], [2, -1]], 2), 0)
        self.assertEqual(filtered([[-1, 2], [2, -1]], 1), 3)

    def test_typing_edge_weight_has_quadratic_integrated_vanishing(self):
        # gamma=0,B=2,lambda>1: w=36(lambda^2-1).
        # a_S<=1/2 means 1<lambda<=49/48.
        lower, upper = F(1), F(49, 48)
        primitive = lambda x: 12*x**3-36*x
        self.assertEqual(upper-lower, F(1, 48))
        self.assertEqual(primitive(upper)-primitive(lower), F(145, 9216))

    def test_exact_public_source_copies(self):
        rows = json.loads((ROOT/'SOURCE_IDENTITIES.json').read_text())
        self.assertEqual({x['key'] for x in rows}, {'C91', 'C92', 'P', 'E1', 'E2', 'REC', 'CUB'})
        for row in rows:
            raw = (ROOT/row['local_path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])


if __name__ == '__main__':
    unittest.main(argv=['exact_controls.py'] + REST, verbosity=2)
```
<!-- END C102 PUBLIC_CONTROLS.py -->

SOURCE_IDENTITIES.json: 3585 bytes; SHA256 `a2c5f89fdd516a92c1a7be11273b53f72e41abcf2168f7f52e0daba314ebf70d`.

<!-- BEGIN C102 SOURCE_IDENTITIES.json -->
```json
[
  {
    "key": "C91",
    "local_path": "sources/C91.md",
    "copied_from": "work/continuation98/sources/C91_PROOF.md",
    "bytes": 12433,
    "sha256": "74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa",
    "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963566666",
    "comment_id": 5963566666,
    "extraction": "Exact UTF-8 body"
  },
  {
    "key": "C92",
    "local_path": "sources/C92.md",
    "copied_from": "work/continuation98/sources/C92_PROOF.md",
    "bytes": 19567,
    "sha256": "6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a",
    "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963825788",
    "comment_id": 5963825788,
    "extraction": "Exact UTF-8 body"
  },
  {
    "blob": "dfed3b8d318a3ab1950957f393307733a4bef3f2",
    "bytes": 40261,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "P",
    "local_path": "sources/P.md",
    "path": "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
    "sha256": "9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
    "copied_from": "work/continuation99/sources/P.md"
  },
  {
    "blob": "213594d6ca6a86fb938110f4d166d9ce275a02d0",
    "bytes": 1782,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "E1",
    "local_path": "sources/E1.md",
    "path": "imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
    "sha256": "bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
    "copied_from": "work/continuation99/sources/E1.md"
  },
  {
    "blob": "fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a",
    "bytes": 9062,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "E2",
    "local_path": "sources/E2.md",
    "path": "reviews/d1_section9_borel_repair_20260925/REPAIR.md",
    "sha256": "845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_section9_borel_repair_20260925/REPAIR.md",
    "copied_from": "work/continuation99/sources/E2.md"
  },
  {
    "blob": "75da2597971510f843f8d90c743950cb8c177342",
    "bytes": 23312,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "REC",
    "local_path": "sources/REC.md",
    "path": "reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
    "sha256": "451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
    "copied_from": "work/continuation99/sources/REC.md"
  },
  {
    "blob": "bb446d08db8a944537a743ad550b88c1c2ad5758",
    "bytes": 19889,
    "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
    "key": "CUB",
    "local_path": "sources/CUB.md",
    "path": "frontiers/planar_cubic_cluster_20260929/PROOF.md",
    "sha256": "117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0",
    "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/frontiers/planar_cubic_cluster_20260929/PROOF.md",
    "copied_from": "work/continuation99/sources/CUB.md"
  }
]
```
<!-- END C102 SOURCE_IDENTITIES.json -->

PUBLIC_EXECUTION.txt: 1461 bytes; SHA256 `4ba09e022d6a4f7a508e1e63f3c0d2bfe0251207e9012403a37b20045f82bc48`.

<!-- BEGIN C102 PUBLIC_EXECUTION.txt -->
```text
C102 public-control execution record
Runtime: Python 3.11.16
Checker: PUBLIC_CONTROLS.py; 6927 bytes; SHA256 de8c39b08178369e38a03cb27c79aa0523516455feaf3d20e6f8bec87c5c4a4f
Normal flags: -B -S
Optimized flags: -B -O -S
Each invocation ran all 9 controls, including exact verification of the 7 public source copies.

normal: base; exit=0; tests=9; assertion_failures=0
normal: amplitude-law; exit=1; tests=9; assertion_failures=1
normal: jacobian-r; exit=1; tests=9; assertion_failures=2
normal: extra-k4; exit=1; tests=9; assertion_failures=2
normal: soft-normalizer; exit=1; tests=9; assertion_failures=1
normal: sqrt-congruence; exit=1; tests=9; assertion_failures=1
optimized: base; exit=0; tests=9; assertion_failures=0
optimized: amplitude-law; exit=1; tests=9; assertion_failures=1
optimized: jacobian-r; exit=1; tests=9; assertion_failures=2
optimized: extra-k4; exit=1; tests=9; assertion_failures=2
optimized: soft-normalizer; exit=1; tests=9; assertion_failures=1
optimized: sqrt-congruence; exit=1; tests=9; assertion_failures=1

Base runs: 9 passed in each mode. Each of 5 intentional invalid-scaling mutants failed with assertion errors in each mode (10 expected negative runs).
These are newly executed Python 3.11.16 results. Original frozen controls and their Python 3.9.6 output/failure evidence remain unchanged.
Finite algebra/source-integrity checks only; no analytic theorem proof, independent review, hosted CI or acceptance is inferred.
```
<!-- END C102 PUBLIC_EXECUTION.txt -->
