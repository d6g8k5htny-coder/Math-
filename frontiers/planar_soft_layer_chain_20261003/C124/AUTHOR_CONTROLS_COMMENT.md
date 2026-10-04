## C124 exact controls and execution record

Dylan Roy — delegated AI work. Actual author: OpenAI/Codex next_math_triage; root publishes the exact frozen files. These are author-side arithmetic controls, not an independent analytic review.

For the proof [5974162498](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974162498). Each file is the literal text inside its five-backtick fence, including the final LF. controls.py is 12,062 bytes SHA256 3cc864185ba8e9cee780544ea1559c5591bda45110745f73f0cd9b4277745bcb. CONTROLS.md is 10,113 bytes SHA256 400a043d664f2ad894bbc669c38203d9809a14743522c031cc86bdbef923e399. The full normal/optimized baseline and ten adverse variants are recorded below. These finite checks do not prove the analytic imports.

### controls.py
`````python
#!/usr/bin/env python3
"""C124 finite exact arithmetic controls; no analytic or formal-proof claim.

No arguments: baseline (exit 0 on success). --mutant NAME: deliberately
incorrect candidate (exit 1 if rejected). Invalid arguments exit 2.
Only the Python standard library is used; no files or network are accessed.
"""

from fractions import Fraction as F
from math import comb, factorial, prod
import json
import sys


MUTANTS = (
    "WINDOW_H_OMITTED",
    "BAND_P_ONE",
    "DROP_BAND_FLOOR",
    "UNWEIGHTED_PROMOTION",
    "INDEPENDENT_COEFFICIENTS",
    "EXP_SCALE_TOO_LARGE",
    "DROP_SOFT_FACTOR",
    "DOUBLE_NORMALIZER",
    "DROP_SCALED_FAR",
    "GAUSSIAN_LAMBDA_SQUARED",
)


class Checks:
    def __init__(self):
        self.groups = {}
        self.failures = []

    def check(self, group, label, condition):
        counts = self.groups.setdefault(group, {"checks": 0, "failures": 0})
        counts["checks"] += 1
        if not condition:
            counts["failures"] += 1
            if len(self.failures) < 16:
                self.failures.append({"group": group, "label": label})

    def equal(self, group, label, got, want):
        self.check(group, label, got == want)

    def result(self, mutant):
        checks = sum(v["checks"] for v in self.groups.values())
        failures = sum(v["failures"] for v in self.groups.values())
        return {
            "object": "C124-EXACT-CONTROLS-v1",
            "candidate": mutant or "BASELINE",
            "passed": failures == 0,
            "checks": checks,
            "failure_count": failures,
            "failures_first_16": self.failures,
            "groups": self.groups,
            "scope": "finite rational controls; not analytic proof or source verification",
        }


def ledger(c, mutant):
    g = "G1_schedule_and_admissibility"
    # w=(r H^4)^(-1/12), retaining both exact powers.
    schedule = (F(-1, 12), F(-1, 3))
    if mutant == "WINDOW_H_OMITTED":
        schedule = (F(-1, 12), F(0))

    def substitute(r, h, w):
        return (F(r) + F(w) * schedule[0], F(h) + F(w) * schedule[1])

    # Input monomials (r,H,w) and independently hand-derived expected pairs.
    cases = (
        ("radius", (0, 0, -8), (F(2, 3), F(8, 3))),
        ("radius_actual", (1, 3, -4), (F(4, 3), F(13, 3))),
        ("selected_edge", (1, 4, 4), (F(2, 3), F(8, 3))),
        ("selected_edge_actual", (F(3, 2), 5, 2), (F(4, 3), F(13, 3))),
        ("endpoint", (1, 3, 2), (F(5, 6), F(7, 3))),
        ("endpoint_actual", (F(3, 2), 4, 1), (F(17, 12), F(11, 3))),
        ("joint_band", (1, 0, 4), (F(2, 3), F(-4, 3))),
        ("actual_band_floor", (1, 4, 0), (F(1), F(4))),
        ("large_N", (2, 3, 8), (F(4, 3), F(1, 3))),
        ("hessian_first", (2, 5, 4), (F(5, 3), F(11, 3))),
        ("hessian_second", (2, 7, 2), (F(11, 6), F(19, 3))),
        ("far_derivative", (1, 0, 0), (F(1), F(0))),
    )
    target = (F(2, 3), F(8, 3))
    values = {}
    for label, powers, want in cases:
        got = substitute(*powers)
        values[label] = got
        c.equal(g, label + ":exact_pair", got, want)
        c.check(g, label + ":log_dominance",
                got[0] > target[0] or
                (got[0] == target[0] and got[1] <= target[1]))
    c.equal(g, "balanced_leading_terms", values["radius"], values["selected_edge"])
    c.equal(g, "leading_target", values["radius"], target)
    for label, powers, want in (
        ("rH", (1, 1, 0), (F(1), F(1))),
        ("rw", (1, 0, 1), (F(11, 12), F(-1, 3))),
        ("e", (1, 0, 4), (F(2, 3), F(-4, 3))),
        ("H2e", (1, 2, 4), (F(2, 3), F(2, 3))),
        ("eta", (1, 0, 2), (F(5, 6), F(-2, 3))),
    ):
        got = substitute(*powers)
        c.equal(g, label + ":exact_admissibility", got, want)
        c.check(g, label + ":vanishes", got[0] > 0)
    c.check(g, "window_grows", schedule[0] < 0)
    # Fixed-Lambda schedule w=r^-1/12: H powers become constants.
    for label, powers, _ in cases:
        r, _, w = powers
        c.check(g, label + ":fixed_layer_at_least_two_thirds",
                F(r) - F(w, 12) >= F(2, 3))


def dyadic(c, mutant):
    g = "G2_joint_band_dyadic_sums"
    p = 1 if mutant == "BAND_P_ONE" else 2
    for m in range(2, 33):
        for scale in (F(1), F(3, 4), F(5, 7)):
            a = scale / 2**m
            b = F(3, 17)
            endpoint = 2 * a
            last = 0
            while 2 * endpoint <= F(1, 2):
                last += 1
                endpoint *= 2
            c.check(g, f"m{m}:{scale}:stopping_interval",
                    F(1, 4) < endpoint <= F(1, 2))
            shell_a = sum((2 * a * F(2) ** ((1 - p) * j)
                           for j in range(last + 1)), F(0))
            shell_b = sum((b * F(2) ** (-p * j)
                           for j in range(last + 1)), F(0))
            c.equal(g, f"m{m}:{scale}:linear_geometric_sum", shell_a,
                    4 * a * (1 - F(1, 2) ** (last + 1)))
            c.equal(g, f"m{m}:{scale}:floor_geometric_sum", shell_b,
                    F(4, 3) * b * (1 - F(1, 4) ** (last + 1)))
            c.check(g, f"m{m}:{scale}:uniform_shell_bound",
                    shell_a + shell_b <= 4 * a + F(4, 3) * b)
            c.check(g, f"m{m}:{scale}:large_N_threshold",
                    endpoint / a > 1 / (4 * a))
            c.check(g, f"m{m}:{scale}:tail_markov_coefficient",
                    (a / endpoint)**2 < 16 * a**2)
            c.check(g, f"m{m}:{scale}:combined_low_and_shells",
                    a + b + shell_a + shell_b <= 5 * a + F(7, 3) * b)
    # Abstract continuous band fixture: measure of total mass B, N=1,
    # uniform in mu on (0,delta]. It obeys mass{|mu|<=s} <= s+B for
    # every s>0, with no atom at the neutral level. It is not asserted
    # to be a realizable pinned Gaussian field. The bound alone cannot
    # discard B; choosing delta=B/2^m defeats a delta-only unit bound.
    for m in range(1, 33):
        b = F(1, 64)
        delta = b / 2**m
        offered = delta if mutant == "DROP_BAND_FLOOR" else delta + b
        c.check(g, f"continuous:m{m}:retain_band_error_floor", b <= offered)


def counterexample(c, mutant):
    g = "G3_unweighted_band_counterexample"
    # The geometric-distribution recurrence is compared with literal moments.
    moments = [1]
    for p in range(1, 9):
        moments.append(2 + sum(comb(p, j) * moments[j] for j in range(1, p)))
    c.equal(g, "geometric_moments_zero_through_eight", moments,
            [1, 2, 6, 26, 150, 1082, 9366, 94586, 1091670])
    for p in range(9):
        partial = sum((F(n**p, 2**n) for n in range(1, 129)), F(0))
        c.check(g, f"p{p}:partial_moment_below_exact", partial <= moments[p])
    for m in range(2, 65):
        delta = F(1, 2**m)
        e = delta / m
        c.equal(g, f"m{m}:event_lower_bound_over_e", delta / e, F(m))
        c.check(g, f"m{m}:event_containment_at_right_endpoint", delta <= e * m)
        # Exact partition into U-intervals with N=m+j, including the tail.
        finite = sum((F((m + j)**2, 2**(m + j)) for j in range(1, 17)), F(0))
        tail = F((m + 16)**2 + 4 * (m + 16) + 6, 2**(m + 16))
        joint = delta * (m*m + 4*m + 6)
        c.equal(g, f"m{m}:joint_second_moment", finite + tail, joint)
        c.equal(g, f"m{m}:joint_band_ratio", joint / delta, F(m*m + 4*m + 6))
        proposed_bound = 8 * e if mutant == "UNWEIGHTED_PROMOTION" else delta
        c.check(g, f"m{m}:unweighted_Oe_claim_not_inferred", delta <= proposed_bound)


def gaussian(c, mutant):
    g = "G4_correlated_gaussian_and_exp_square"
    for index, weights in enumerate(((F(1), F(1)), (F(1, 3), F(2, 3)),
                                     (F(2), F(3), F(5)),
                                     (F(1, 2), F(1, 3), F(1, 7)))):
        s = sum(weights)
        variance = sum(a*a for a in weights) if mutant == "INDEPENDENT_COEFFICIENTS" else s*s
        c.equal(g, f"fixture{index}:fully_correlated_variance", variance, s*s)
        c.check(g, f"fixture{index}:quadrature_is_too_small", sum(a*a for a in weights) < s*s)
        for m in range(1, 17):
            normal_moment = prod(range(1, 2*m, 2))
            candidate_moment = variance**m * normal_moment
            c.equal(g, f"fixture{index}:m{m}:actual_even_moment",
                    candidate_moment, s**(2*m) * normal_moment)
            c.check(g, f"fixture{index}:m{m}:Minkowski_majorant",
                    s**(2*m) * normal_moment <= s**(2*m) * (2*m)**m)
    # Rational coefficient check: if ||J||_p <= C sqrt(p), use
    # epsilon=1/(12 C^2), m! >= (m/3)^m, and sum 2^-m=2.
    # The assumed moment inequality and infinite-series step are analytic.
    for const in (F(1), F(3, 2), F(4), F(17, 3)):
        epsilon = 1 / (const*const * (1 if mutant == "EXP_SCALE_TOO_LARGE" else 12))
        for m in range(1, 49):
            c.check(g, f"C{const}:m{m}:factorial_majorant", m**m <= 3**m * factorial(m))
            coefficient = epsilon**m * const**(2*m) * (2*m)**m / factorial(m)
            c.check(g, f"C{const}:m{m}:geometric_exp_coefficient", coefficient <= F(1, 2**m))
    for m in range(1, 25):
        c.equal(g, f"exp_partial{m}", sum((F(1, 2**j) for j in range(m + 1)), F(0)),
                2 - F(1, 2**m))


def rare_scalar(c, mutant):
    g = "G5_rare_scalar_and_full_normalization"
    for r in (F(1, 2), F(1, 7), F(1, 64), F(3, 100)):
        for j in (F(1), F(3, 2), F(4)):
            for d, s in ((F(1), F(1)), (F(2), F(3, 4)), (F(1, 3), F(5))):
                top = d * r * j*j
                integral = top*top / 2 if mutant == "DROP_SOFT_FACTOR" else top**3/3 + s*r*j*j*top*top/2
                numerator = r*r*j**4 * integral
                coefficient = d**3/3 + s*d*d/2
                want = r**5*j**10*coefficient
                label = f"r{r}:J{j}:D{d}:C{s}"
                c.equal(g, label + ":scalar_integral", numerator, want)
                z = F(5, 3) * r*r
                normalized = numerator / (z*z if mutant == "DOUBLE_NORMALIZER" else z)
                c.equal(g, label + ":probability_scaling", normalized,
                        r**3*j**10*coefficient/F(5, 3))
                c.equal(g, label + ":scaled_measure", normalized/r**3,
                        j**10*coefficient/F(5, 3))
    # The documented input is E[(W/r^2) 1_exception] <= C r^4.
    c.equal(g, "near_radius_exponents", 5 - 2 - 3, 0)
    c.equal(g, "far_numerator_radius_exponent", 2 + 4, 6)
    far = F(0) if mutant == "DROP_SCALED_FAR" else F(1, 8)
    c.check(g, "retain_permitted_far_mass", F(1, 8) <= far)
    c.equal(g, "far_scaled_radius_exponent", 2 + 4 - 2 - 3, 1)


def exponential_tail(c, mutant):
    g = "G6_exponential_tail_threshold"
    for lam in (F(1), F(4), F(9), F(25), F(64), F(100)):
        for const in (F(1), F(4), F(9)):
            threshold_squared = lam*lam/const if mutant == "GAUSSIAN_LAMBDA_SQUARED" else lam/const
            c.equal(g, f"Lambda{lam}:C{const}:threshold_square", threshold_squared, lam/const)
    c.equal(g, "square_of_square_root_degree", F(1, 2)*2, 1)
    for decay in (F(1, 10), F(1, 3), F(1), F(7, 2)):
        D = F(2, 3)/decay
        c.equal(g, f"c{decay}:minimum_log_cutoff", decay*D, F(2, 3))
        c.check(g, f"c{decay}:larger_log_cutoff", decay*(D + 1) > F(2, 3))


def main(argv):
    if argv == ["--list-mutants"]:
        print(json.dumps(list(MUTANTS), separators=(",", ":")))
        return 0
    mutant = None
    if argv:
        if len(argv) != 2 or argv[0] != "--mutant" or argv[1] not in MUTANTS:
            print(json.dumps({"error": "expected no arguments, --list-mutants, or --mutant NAME",
                              "passed": False}, sort_keys=True, separators=(",", ":")))
            return 2
        mutant = argv[1]
    checks = Checks()
    for group in (ledger, dyadic, counterexample, gaussian, rare_scalar, exponential_tail):
        group(checks, mutant)
    result = checks.result(mutant)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
`````

### CONTROLS.md
`````markdown
# C124 exact arithmetic controls — author-side design

Actual author: OpenAI/Codex delegated executor `/root/next_math_triage`, under
parent C124 claim `33e06044-3ffa-4d61-81d8-937ad54e3fb4` (WE733). This executor
supplied author-side proof analysis and is not an independent reviewer.
Organizational independence credit: 0. Human review: NONE.

The controls are finite exact arithmetic checks, not a proof of Gaussian
regression, the saddle-band integral, the actual global elder event, or the
continuum/asymptotic theorem. They import no independent reference field law.
Only `controls.py` and this document are authored by this executor.

## Frozen test intentions before implementation

1. Substitute `w = r^(-1/12) H^(-1/3)` into the complete new error ledger with
   exact `Fraction` exponents. Check every resulting pair and dominance by
   `(2/3, 8/3)` when `H = 1 + D log(1/r)`. The dominance test permits any fixed
   logarithmic power if its radius exponent is strictly greater than `2/3`;
   at equality its logarithmic exponent must be at most `8/3`. Check the
   remaining small-radius admissibility exponents separately. A schedule
   omitting the power of H must fail.
2. For `a = 2 K0 e <= 1/4` and `B = r H^4`, sum the actual mu-shell majorants
   `2 a 2^(-j) + B 4^(-j)` through the last endpoint at most `1/2`. Verify
   their exact geometric sums, the endpoint in `(1/4,1/2]`, and the residual
   large-N cost `16 a^2 mu_r(N^2)`. The low band contributes `a+B`, so the
   resulting constants are `5a + (7/3)B + 16H^3a^2`, before source constants.
   Using p=1 or deleting the actual-law floor B must fail.
3. Keep a counterexample to promoting an unweighted band plus all moments:
   `U ~ Uniform(0,1)`, `N = ceil(log2(1/U))`, and `e_m = 2^(-m)/m`.
   On `0<U<=2^(-m)`, `U<=e_m N`, so the event has mass at least `m e_m`.
   Moreover `P(N=n)=2^(-n)` for n>=1, every fixed moment is finite by the
   ratio test, and `E[N^2; U<=2^(-m)] = 2^(-m)(m^2+4m+6)`. The finite
   checks verify these geometric/moment identities; they do not prove an
   assertion for every real p by enumeration.
4. Use perfectly correlated Gaussian coefficients `eta_i=G`, not independent
   ones. The variance is `(sum a_i)^2`, and the even moments follow the exact
   double-factorial identity. Check that the sum-of-standard-deviations
   majorant works while the independent-coefficient variance fails. Verify
   finite coefficients of a conservative exponential-square majorant;
   convergence of its infinite series remains analytic reasoning.
5. Reconstruct, for rational positive parameters, the rare scalar integral
   `r^2 J^4 integral_0^(D r J^2) l(l+C r J^2) dl`
   `= r^5 J^10 (D^3/3+C D^2/2)`. Preserve both scalar factors. Check the
   single full normalizer `r^2`, subsequent `r^-3` scaling, and the retained
   scaled far/derivative contribution `O(r)`. Missing a soft factor or
   normalizing twice must fail.
6. Check the threshold-degree conversion `J > sqrt(Lambda/C)` followed by
   an exponential-square tail: its exponential order is Lambda, not
   Lambda squared. These algebra checks do not establish a tail estimate.

All rejection checks will use explicit conditions rather than Python
`assert`, so optimized Python cannot remove them. No network, random
sampling, third-party module, project test, or source mutation is involved.

## Executed results

Final script: **12062 bytes**, SHA-256
`3cc864185ba8e9cee780544ea1559c5591bda45110745f73f0cd9b4277745bcb`.

Executed with Python **3.11.16** at
`/Users/dylanroy/Documents/Codex/2026-09-19/connect-research-repository/work/venv/bin/python3.11`.
There were **24 final invocations**: baseline, ten named adverse candidates,
and one unknown label, each in normal and optimized mode. All had the
expected exit; all stderr streams were empty. Each corresponding pair of
stdout streams was byte-identical.

Baseline: **1,740 checks, zero failures**, in six groups:

| Group | Checks |
|---|---:|
| G1 — schedule and admissibility | 49 |
| G2 — joint-band dyadic sums | 683 |
| G3 — unweighted-band counterexample | 325 |
| G4 — correlated Gaussian and exponential-square arithmetic | 544 |
| G5 — rare scalar integral and normalization | 112 |
| G6 — exponential-tail threshold | 27 |

Counts enumerate arithmetic predicates and are not theorem counts or
independent proofs. A negative candidate runs the same predicates and
must exit 1. The unknown label exits 2 before checks. Output lists at most
the first sixteen failed labels but counts every failure.

| Candidate | Exit (both modes) | Failed predicates | Stdout bytes | Stdout SHA-256 (both modes) |
|---|---:|---:|---:|---|
| `BASELINE` | 0 | 0 | 591 | `14b587bd72fd8b16ce56791178c2fab4f57535534e5c0f4e1697daf9692cdcdd` |
| `WINDOW_H_OMITTED` | 1 | 17 | 1807 | `84cf603bbb2361ec185c3c86c177e5e1602021280b86c30c240cf7c579cf23f7` |
| `BAND_P_ONE` | 1 | 360 | 1801 | `8999f77b2e0fe300d4344505a444b0185aee2d08e4a5fac77eb8eb188d8b6830` |
| `DROP_BAND_FLOOR` | 1 | 32 | 1983 | `fff2a4497204b922b2e9d58e1a6536a67b8df9fefc4b3215fb97ffadc703abcb` |
| `UNWEIGHTED_PROMOTION` | 1 | 56 | 2092 | `7a121924fa4901d152b705a722feae2b93ae64bbaeda858a8b7ff7ee0dc4900f` |
| `INDEPENDENT_COEFFICIENTS` | 1 | 68 | 2075 | `55634f5b00ba1fcfc6d1c09639a9c1cd31e31f8ffda95be760c36b97e5ca39ad` |
| `EXP_SCALE_TOO_LARGE` | 1 | 192 | 2085 | `8c9b05ac6d858e9151fae55d0ff292972e5fc0800b1ef45f41573919f41db590` |
| `DROP_SOFT_FACTOR` | 1 | 105 | 2092 | `9ab1a8fda6ab2888d9299b48e212bee5032cc523cc2f5700163fca5ebb1f498e` |
| `DOUBLE_NORMALIZER` | 1 | 72 | 2098 | `b059ff988449f4d9f9bcd4615831ebad4628e9b166f75d4d0fb200e7f6bcaaad` |
| `DROP_SCALED_FAR` | 1 | 1 | 684 | `7f5c21d1e8719ec2564333fd6b4186cdcf02cacd742832b30e0f88401535bdd1` |
| `GAUSSIAN_LAMBDA_SQUARED` | 1 | 15 | 1820 | `8355c4cbde5561bdf2ddcebf4d1270dd79db61433a83c5947b734218fe543b91` |
| `UNKNOWN` | 2 | n/a | 83 | `5189cbc57e52c13b5608e65a6311f44598eaacec80d76a6544051e4c44d897ce` |

Empty stderr SHA-256 is
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The final baseline stdout, including its terminating newline, is:

```json
{"candidate":"BASELINE","checks":1740,"failure_count":0,"failures_first_16":[],"groups":{"G1_schedule_and_admissibility":{"checks":49,"failures":0},"G2_joint_band_dyadic_sums":{"checks":683,"failures":0},"G3_unweighted_band_counterexample":{"checks":325,"failures":0},"G4_correlated_gaussian_and_exp_square":{"checks":544,"failures":0},"G5_rare_scalar_and_full_normalization":{"checks":112,"failures":0},"G6_exponential_tail_threshold":{"checks":27,"failures":0}},"object":"C124-EXACT-CONTROLS-v1","passed":true,"scope":"finite rational controls; not analytic proof or source verification"}
```

## Replaying the finite controls

From this directory:

```sh
python3 -B controls.py
python3 -B -O controls.py
python3 -B controls.py --list-mutants
python3 -B controls.py --mutant DROP_SOFT_FACTOR
python3 -B -O controls.py --mutant DROP_SOFT_FACTOR
python3 -B controls.py --mutant UNKNOWN
```

The last three commands intentionally return 1, 1 and 2. All ten labels in
the table can be substituted for `DROP_SOFT_FACTOR`. No command downloads
sources, verifies a source digest, or replays the project master suite.
The complete analytic imports and proof must be assessed independently.

## Development and conceptual limits

The written test intentions above preceded implementation. The first
baseline used an unfinished constant-window placeholder
`schedule = (F(0), F(0))`: it exited 1 with **18 expected ledger failures**,
while the other five groups passed. That test-first source was
11856 bytes, SHA-256
`b37a96e544ec4f70ad6f0747c797bc457adb8ae71bb938dd755bc4c37cff9f52`; its 1792-byte stdout was
`bae8c10f566276eee0d9e348919511af574c7f27759ca68aa02dc5661f04c0fc`. Replacing the placeholder by the intended two
powers made the baseline pass. The initial red run was repeated once to
capture its identity. A later final-source tightening made the floor
fixture continuous instead of atomic; the complete final 24-invocation
matrix above was then rerun. No analytic conclusion rests on that
development history.

The `DROP_BAND_FLOOR` fixture is an **abstract continuous measure**, with
N=1 and total mass B distributed uniformly over `0<mu<=delta`.
For every s>0 it satisfies `mass(|mu|<=s)<=s+B`, and has no atom at mu=0.
It shows what the stated band inequality alone permits. It is not claimed
to arise from the pinned Gaussian field. In particular it does not
contradict actual neutral-level nullity. Removing B in the analytic proof
would require additional source information.

The U,N counterexample is also abstract. Its unweighted band is exactly
`P(U<=delta)=delta` for `0<=delta<=1`; all fixed moments of N exist.
Nevertheless the ratio `P(U<=e_m N)/e_m` is at least m and unbounded.
The adverse label uses a proposed constant 8, rejected for m>8. The
divergence for arbitrary constants follows from the written argument,
not from testing only m<=64. Its joint band has an unbounded quadratic
coefficient `m^2+4m+6`, which identifies precisely the extra hypothesis
used by the C124 proof.

The Gaussian fixtures take identical coefficients, eta_i=G. They show
that coefficient-wise variance bounds do not give independence or a
sum-of-variances bound. Minkowski uses a sum of standard deviations and
remains valid. The exponential-square coefficient check chooses the
conservative rational `epsilon=1/(12 C^2)` under the analytic premise
`||J||_p<=C sqrt(p)`, using `m!>=(m/3)^m` and the geometric sum.
Only finitely many coefficients are checked; the premise, factorial
inequality for all m, infinite series, conditional Fourier convergence
and tail transfer belong to the analytic proof.

No finite-r saddle matching, ordinary-global-elder equivalence, retained
cap theorem, compact-family uniformity, or full normalizer lower bound
is proved by this script. It neither extends the contribution beyond
physical k=1 nor establishes once-counted replacement bars, a transported
real-valued mark, k-to-zero behavior, higher dimensions, or unrestricted
lifetime asymptotics.
`````
