# Weighted squares and upper-moment-free D2 Schur bound

Dylan Roy — delegated AI work. Author: OpenAI / GPT-6 Astra Pro,
`d2-square-schur-formal-20261006`, pickup main#229/6008966287.
Continuation: `d2-square-schur-resume-math-audit-20261006`, #343/6009354574.
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
hA<=gA<=N and hB<=2xB<=N. The exact nonnegative remainders are
N-gA=x^2*g and N-2xB=x*g^2/2. Hence h*max(A,B)<=N. The existing positive
endpoint-denominator theorem bounds N/max(A,B) below the actual d2Schur.
This never substitutes a lower determinant into a denominator and uses no
moment upper bound. Monotonicity of squares on positive inputs gives the last
target. The unchanged exact-type Contract preserves all hypotheses and the
original subtractive d2Schur definition, not a redefinition of the quotient.

## Verification and exclusions

Initial publication f9d478e was a test-first stub. Its dedicated run37411527600
failed historical Git reachability BEFORE Lean, not the missing-name contract.
Original artifact11389791199 (8911 bytes) has SHA256
430b82d3da185c92f17927d5e0e8b507a05791c80131b27c6cc65371b07172e6.
The successor3479b6e added fetch-depth0 and one regression while retaining every
root test and the stub. That regression failed on the old workflow before its
repair. Dedicated37414215874 then passed both189-method root suites, both133-method
core suites and the unchanged primary kernel replay; the stub compiled and
Contract.lean failed on EXACTLY the four absent target names, with exit1.
Original artifact11390508232 (37549 bytes) has SHA256
a03f164e08d4c34ea778eb3131c6f2e404af638ca340b03dc3d2a4b82cb973dc.

The four bodies are supplied only after that observed contract failure. Source
supply, successful hosted execution and a distinct source-alignment review are
separate states recorded in the PR. No configured workflow, empty stub, finite
Python model or successful OLD core build proves these new declarations.

The adapted #317 driver runs the complete root and primary formal Python suites
in normal and optimized modes, the pinned primary kernel check, then this
module's warnings-as-errors build, exact-type Contract, all four axiom/type
reports and fresh leanchecker. Three concrete false propositions must fail with
exact source-bound False-goal diagnostics: signed negative weights, replacing
the lower minimum by an endpoint maximum, and leaving the q interval.
Original raw logs/statuses and source/run identity are retained on failure.
The core audit function is reused by exact hash; this small explicit inventory
is not the independently owned general RF-GATE-01 declaration scanner.

These are FOUR scalar theorem targets, ZERO new definitions; the primary63-target
manifest and all older proof bytes are unchanged. No atom-measure integral
lower bound, moment realizability, periodic spectral law, trigonometric
parameterization, Gaussian/Palm covariance identification, quadrature or
persistence theorem is supplied. No full independent alignment or scientific
acceptance is claimed. #317's actual-law review is not transferred here.

From repository root: `bash companions/d2_square_schur_20261006/replay.sh`
after setting up the existing pinned formal toolchain. Python-only tests:
`python -B -S companions/d2_square_schur_20261006/test_check.py` and the same
command with -O. Python finite controls supplement, never replace, Lean.
