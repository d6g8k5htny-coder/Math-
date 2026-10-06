# Weighted squares and upper-moment-free D2 Schur bound

Dylan Roy — delegated AI work. Author: OpenAI / GPT-6 Astra Pro,
`d2-square-schur-formal-20261006`, pickup main#229/6008966287.
Scientific effect NONE; author-exposed; organizational-independence credit 0.

## Four target statements

1. `weighted_square_identity`: weighted completion for real u,v,a,b,c with
   u+v nonzero. The signed-weight algebra is valid; no positivity is asserted.
2. `weighted_square_lower`: the first term is a lower bound when both weights
   are positive. These sufficient assumptions are intentionally retained.
3. `schur_no_upper`: for m2>0, m4>m2^2 and 0<=q<=1/4,
   `min (m4-m2^2) (2*m2^2) <= ResearchFormalCoreR1.d2Schur m2 m4 q`.
4. `schur_from_lower_inputs`: substitute actual positive lower inputs
   s0<=m2 and g0<=m4-m2^2 to obtain `min g0 (2*s0^2) <= d2Schur ...`.

The source is #328 NOTE sections 3 and 5 at 31f7a6b5a36045be7795a6461da067a8ada96343,
blob cedbb44a237d1a158111dca81c30983f7efd37f1. The shared two-mass calculation is
already in #326, not a second discovery. The stronger optional proposal in
#328 comment6008747995 Part B is NOT incorporated. This companion uses only
unchanged D2Schur.lean blob b95460c0d263a32ea274b347079cca6aaab3d2e9,
from the primary formal tree d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14.

## Proof route

Field simplification proves the weighted identity; nonnegative square gives
the lower bound. Write x=m2^2 and g=m4-x. The two determinant endpoints are
A=x(g+x) and B=g(g+4x)/4, and numerator N=xg(g+2x). With h=min(g,2x),
hA<=gA<=N and hB<=2xB<=N. Hence h*max(A,B)<=N. The existing positive
endpoint-denominator theorem bounds N/max(A,B) below the actual d2Schur.
This never substitutes a lower determinant into a denominator and uses no
moment upper bound. Monotonicity of squares on positive inputs gives the last
target. The exact-type Contract preserves all hypotheses and the original
subtractive d2Schur definition, not an unrelated redefinition of the quotient.

## Verification and exclusions

Initial publication is a test-first stub; Contract.lean must fail on the four
missing names. Source supply, successful hosted execution and a distinct
source-alignment review are separate states recorded in the PR. A configured
workflow or an empty stub module does not establish these theorems.

The adapted #317 driver runs the complete root and primary formal Python suites
in normal and optimized modes, the pinned primary kernel check, then this
module's warnings-as-errors build, exact-type Contract, all four axiom/type
reports and fresh leanchecker. Three concrete false propositions must fail with
exact source-bound False-goal diagnostics: signed negative weights, replacing
the lower minimum by an endpoint maximum, and leaving the q interval.
Original raw logs/statuses and source/run identity are retained on failure.
The core audit function is reused by exact hash; this small explicit inventory
is not the independently owned general RF-GATE-01 declaration scanner.

These are FOUR scalar theorems, ZERO new definitions; the primary 63-target
manifest and all older proof bytes are unchanged. No atom-measure integral
lower bound, moment realizability, periodic spectral law, trigonometric
parameterization, Gaussian/Palm covariance identification, quadrature or
persistence theorem is supplied. No full independent alignment or scientific
acceptance is claimed. #317's actual-law review is not transferred here.

From repository root: `bash companions/d2_square_schur_20261006/replay.sh`
after setting up the existing pinned formal toolchain. Python-only tests:
`python -B -S companions/d2_square_schur_20261006/test_check.py` and the same
command with -O. Python finite controls supplement, never replace, Lean.
