# D2 actual-law moment bridge

Author: OpenAI / GPT-6 Astra Pro, `d2-moment-law-bridge-20261006`.
Dylan Roy — delegated AI work. Scientific effect **NONE**; organizational
independence credit **0**. This is an author-side candidate until actual execution
and review records establish their distinct scopes. No author self-merge.

## Bound sources and purpose

Base: `2f8b6f372be383d752e9dd30d38234faa977243c`, the actual #309 landing.
The complete unchanged primary `formal/` tree is
`d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14`; primary manifest SHA256
`5d7ccdb0885af7bf4a2aa6ec4dce5f5c41435bb10a0a7a426a8af286d4f035e4`.
`ResearchFormalCoreR1.D2Schur` is the consumed scalar companion, blob
`b95460c0d263a32ea274b347079cca6aaab3d2e9`.
The source note is #302 `reviews/side24_d2_certified_small_L_claude_20261005/NOTE.md`,
blob `852f7403a8a06a1ef061e363df9502ae16f7a341`. Its section4 and C7 record
certified positive minima and the existing Gram floors at the listed periods.
This packet neither replaces those results nor supplies another numerical bound.

Motivation: review correction AUD-309-REVIEW-STRICTNESS-01 (#309/6006934456;
reviewer correction in6006807347). Strict Jensen for X^2 does not imply strict
Cauchy--Schwarz for X and X^3: P(0)=1/2, P(+-1)=1/4 has m4-m2^2=1/4 but Delta=0.
The old Lean statement already assumes Delta>0 separately and remains unchanged.

## What the new actual-law statements say

`moment mu X n` is the **actual Bochner integral** of X^n, not an arbitrary
real named a moment. `cubicResidual c x = x^3-c*x`. Integrability of X^2,X^4,X^6
is explicit where used. No independence, symmetry or Gaussian assumption is
required. No measurability assumption is silently substituted for integrability.

For any measure, with these three integrability premises and m2!=0:

    integral (X^3-(m4/m2)X)^2 = Delta = m6-m4^2/m2 >= 0.
    Delta=0 iff almost everywhere [X=0 or X^2=m4/m2].

The zero atom is deliberately permitted. This is an a.e. value-set description,
not a statement about topological support or a necessary two-atom condition.
Any positive-mass atom inherits an a.e. value property. Hence two positive-mass
nonzero atoms a,b with a^2!=b^2 suffice for m2>0 and Delta>0. The distinction is
**squared radii**, not just a!=b; a and -a do not suffice.

For a **probability** measure, the actual square-gap identity additionally gives
m4-m2^2 = integral (X^2-m2)^2. Two positive-mass atoms of different squared radii
make this gap strict. The final theorem supplies all three strict moment premises
to the unchanged `d2_tau_pos` on the closed q interval [0,1/4]. Probability mass
one is essential for this unscaled gap identity; it is not needed for the cubic
residual identity or its equality classification.

## Declaration map: 16 theorems, 2 definitions

| Theorem | Explicit scope |
|---|---|
| residual_sq_expand | Polynomial identity for arbitrary real c,x. |
| residual_sq_integrable | Powers2/4/6 integrable imply residual square integrable. |
| residual_integral_eq_delta | Actual integral identity, m2!=0. |
| delta_nonneg | Nonnegative actual residual variance, same hypotheses. |
| delta_eq_zero_iff_residual | Exact a.e. residual-zero characterization. |
| cubicResidual_eq_zero_iff | Pointwise zero or squared-radius factorization. |
| delta_eq_zero_iff_support | Exact a.e. zero-plus-one-radius characterization. |
| delta_pos_iff_not_support | Strictness iff that a.e. condition fails. |
| property_of_ae_of_atom | Atom mass nonzero transfers any a.e. value property. |
| moment_two_pos_of_atom | Integrable second power and a nonzero positive-mass atom. |
| delta_pos_of_two_atoms | Three integrabilities; two nonzero, distinct squared radii. |
| square_gap_integrable | Probability normalization; powers2/4 integrable. |
| square_gap_integral | Exact unscaled fourth-minus-second-square identity. |
| fourth_gt_second_sq_of_two_atoms | Probability law, two distinct squared radii. |
| tau_pos_of_two_atoms | Actual moment premises feed the existing scalar theorem. |
| zero_atom_counterexample | Exact scalar moments of the tested three-point law. |

The last theorem is a scalar control, not a Lean construction of that finite
measure. The Python tests instantiate the finite law separately. There are 18
explicit axiom/type targets, not18 new theorems and not a new combined primary
manifest. No existing theorem or gate is edited.

## Execution and review contract

Run from a complete checkout with the pinned primary toolchain installed:

    bash companions/d2_moment_bridge_20261006/replay.sh

The new read-only workflow uses the existing Lean/action pins. It executes both
Python test modes, the unchanged63-target primary gate, fresh compilation of this
module with warnings-as-errors, positive examples, all18 transitive axiom reports,
all18 elaborated types, a fresh leanchecker call, and two intended False-goal
negative controls. `check.py` imports the **hash-authenticated existing** primary
axiom parser; it does not replace RF-GATE-01/PR312 work. Exact names and bytes of
this small companion must still receive a real source review. A target inventory
or lexical test is not a general Lean parser or a proof of semantic equivalence.

The source check binds the whole primary tree and every companion/workflow byte
to actual Git HEAD, including its own manifest. Before/after records must agree.
A changed primary tree is a new integration/review scope, not automatically
accepted because the same theorem names remain. Original run/attempt, output,
exit codes, source identities and primary receipt are retained. Two negative
controls must fail specifically with an unsolved False goal at their expected
source file and exit1; crashes, extra errors and exit2 do not qualify. Normal
replay failures remain failures. The evidence directory must be new.

The local test suite checks finite exact laws, omitted-hypothesis countermodels,
source inventory and diagnostic handling. Local Python is not a Lean run. Hosted
build/axiom/recheck evidence, nonauthor mathematical review, full independent
alignment and scientific acceptance are separate predicates. No uniform spectral
floor, concrete periodic probability law, moment summability for that law,
trigonometric q map, Gaussian/Palm identification, interval quadrature, numerical
coefficient or persistence/cap theorem is proved by this packet.

## Initial failure and author repair

The original dedicated run37399665489 failed in the new Lean module at two
integral-linearity rewrites: implicit scalar metavariables were not inferred
through the pointwise function operations. Its unchanged63-target core replay
passed. The successor names the two exact integrable summands and explicit
scalar multipliers; no theorem statement, hypothesis or warning policy changes.
Separately, a new real-shell regression exposed that piping the final receipt
producer through tee into its own hashed directory would record a still-changing
output. The successor removes that tee. The failing original artifact and
separate red/green shell test are retained; the hosted failure did not reach the
final receipt step. Ten local test methods now cover this additional regression.
A successor kernel pass is not claimed by this historical explanation.

The next hosted run37400492648 reached one remaining probability-normalization
lemma-name error. The pinned mathlib Probability.lean exposes `probReal_univ`;
that name replaces the unavailable shorthand without changing the proof target.
The correction reference above points to the actual updated review6006807347;
the initial auxiliary acknowledgment identifier was not retrievable.
