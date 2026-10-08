# Quantitative squared-radius masses to actual D2 moment floors

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`d2-atom-integral-r12-20261006-1255`, pickup main#229/6016691076.
Scientific effect NONE. Author-exposed D2 lineage; organizational independence0.

This is a separate six-target Lean companion. Initial publication contains an
empty imported module so the unchanged exact-type Contract can genuinely fail
before any proof body is supplied. Configuration or old-core success is not
proof of these new targets; actual runs and amendments are recorded on the PR.

## Source correspondence and preserved sources

The quantitative inequalities are the existing #326 two-squared-radius result,
not a new moment discovery. #328's individual signed atoms are a sufficient
specialization, not the premise silently used here. #343 supplies the conservative
upper-moment-free Schur inequality. #371's sharper optional Part B is not included.

This companion consumes `D2MomentBridge.lean`, blob
b3184107e290189b91e3e18fd2aa1cb631bb9bde (landed #317), and
`D2SquareSchur.lean`, blob4855c92d55254969e1de7f8cf8dec2bdc027cf69
(landed #343, merge11f9127f00ce922e5d39b0da42af76134eb78a21).
The exact primary formal tree d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14,
its63-target manifest, gate and all old proof bytes are unchanged. The driver
checks both additional consumed module blobs against Git HEAD and working bytes,
compiles them under the pinned toolchain and audits transitive axioms of every
new target. It does not reuse an upstream receipt as new execution.

## Six exact targets

1. `two_event_integral_lower`: for disjoint measurable events S,T in a probability
   space, integrable nonnegative f, and constants a,b bounding f below on their
   respective events, `mu.real S*a + mu.real T*b <= integral f`. The constants
   need not be positive; disjointness and nonnegativity outside the union suffice.
2. `two_radius_integral_lower`: specialize to S={X^2=s}, T={X^2=t}, with s!=t,
   supplied real event-mass lower bounds p,q and nonnegative constant values a,b
   of f on those events. Its result is p*a+q*b<=integral f.
3. `second_moment_floor`: m2>=p*s+q*t, requiring integrable X^2 and positive s,t.
4. `fourth_gap_floor`: m4-m2^2>=p*q/(p+q)*(s-t)^2 for p,q>0, distinct s,t and
   integrable powers2/4. This statement need not require positive s,t separately.
5. `residual_moment_floor`: Delta>=((p*s)*(q*t)/(p*s+q*t))*(s-t)^2, with
   positive s,t,p,q, distinct radii, and integrable powers2/4/6. Delta is the
   original d2Delta at actual moments. Positivity of m2 follows from target3;
   no division-by-zero convention is used to manufacture the inequality.
6. `schur_floor_of_radius_masses`: under the same positive radius/mass premises
   and powers2/4, for every u in closed[0,1/4], the original d2Schur is at least
   `min(p*q/(p+q)*(s-t)^2, 2*(p*s+q*t)^2)`.

All six use an actual Measure and Bochner integrals through the inherited
`moment` definition. Event measurability is an explicit hypothesis; no global
measurability of X, independence, symmetry, Gaussianity or signed-atom premise
is silently inserted. Probability normalization stays explicit. No upper
moment input is needed for the Schur conclusion. Supplied positive masses imply
their compatibility with probability; p+q<=1 need not be an extra premise.

## Proof route and boundary cases

Integrate the sum of two constant indicators. Each is integrable because the
measure is finite; disjointness makes the sum pointwise <=f. Integral monotonicity
and the constant-indicator formula give target1. Target2 multiplies actual
mass bounds by nonnegative event values. Target3 uses f=X^2. Target4 uses
f=(X^2-m2)^2 and the already-proved probability gap identity, followed by #343's
weighted-square inequality at weights p,q. Target5 uses the already-proved
residual-square identity and weights p*s,q*t. Target6 supplies the two positive
floors to #343's lower-input theorem, retaining its denominator and closed-angle
hypotheses. This is the quantitative integral edge absent from the earlier
qualitative strictness companion.

Overlapping identical events cannot be added twice. The finite measure
delta_1+delta_2 has m4-m2^2=-8, so normalization cannot be removed. Mass at zero
and one nonzero radius can have positive fourth gap but Delta=0. Mass at both
signs of a radius counts together; neither sign alone need carry p. The finite
Python models and exact Lean false-proposition controls retain these distinctions.
The controls are explicit scalar consequences of the described finite laws,
not another general measure construction or a test of every possible omitted
hypothesis. The unchanged Contract fixes the actual theorem types.

## Reproduction and assurance

From repository root after the existing pinned Lean setup:
`bash companions/d2_atom_integral_20261006/replay.sh`.
Python-only controls: `python -B -S companions/d2_atom_integral_20261006/test_check.py`
and the same with -O. The eight-method helper suite first failed eight explicit
missing-helper assertions before implementation. Finite tests supplement the
proofs; they do not prove the arbitrary-measure statements.

The adapted #343 workflow retains full-history checkout, complete root/formal
Python suites in both modes, unchanged63-target core kernel replay, new source
build and exact Contract with warnings-as-errors, six ordered axiom/type reports,
fresh leanchecker and three precise False-goal failures. Original logs/statuses
and source/run/attempt bindings are preserved even on failure. The manifest is
an identity inventory, not an external trust root. The fixed inventory/type-name
parser is not a general Lean syntax or definitional-equality verifier; compiled
Contract and scoped source review provide different assurance.

Six new theorems, zero new definitions; no primary manifest expansion. Formal
sharpness, an actual periodic spectral measure and its summability, numerical
values/radii, uniform-L/family floors, Gaussian/Palm conditioning, the coefficient
integral, persistence matching and scientific acceptance are not supplied.
All older results/reviews retain their scopes. This author's proof and replay
need an actual separate nonauthor read before eligible integration; no self-merge.
