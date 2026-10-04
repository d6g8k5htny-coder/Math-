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
