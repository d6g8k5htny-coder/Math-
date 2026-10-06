# Cap I4: explicit symmetric matrix and positive-cone identification

Dylan Roy — delegated AI work. Author OpenAI / GPT-6 Astra Pro,
`cap-i4-matrix-cone-20261006`, pickup main#229/6008101149. Scientific effect NONE.
This additive child uses frozen polar head035e14017267fe15276fdccf1758618ca7f96b45;
it does not change the parent or join the active integration queue.

## Exact contract

The entry association is `(a,(b,d))` for the actual real matrix `[[a,b],[b,d]]`.
One definition and eleven theorem contracts connect the parent scalar formulas
to Matrix.IsHermitian, trace, determinant, quadratic form, Matrix.PosDef, the
measurable positive-cone event, and the real algebra spectrum. The characteristic
determinant is the product of the two explicit roots; repeated roots are retained
as a singleton spectrum, not excluded by a gap hypothesis. The squared-root sum
is exactly `a^2+2*b^2+d^2`, not the unweighted three-entry Euclidean norm.

The positive-cone equivalence uses the strict criterion `a>0` and `ad-b^2>0`.
Its quadratic completion multiplies by the positive pivot; it does not assume
an inverse-eigenvalue moment or replace the determinant-weighted tail argument
with Cauchy–Schwarz. The cone boundary and negative-definite positive-determinant
counterexamples are exercised as separately rejected false propositions.

## Source and execution

Consumed parent Lean blob9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4. P source
`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
blobdfed3b8d318a3ab1950957f393307733a4bef3f2, §§3,6–7 supplies application context,
not an automatically proved Gaussian law. Its existing full-normalizer erratum
still applies. Exact mathlibd13f23b723b8a846827a245b89c10fc7d3f11612:
Matrix/PosDef.lean blobd85277376a28a5c2265aad6e21472b1fec73185a and
Matrix/Charpoly/Eigs.lean bloba0b9d7c3b01c9bf11742663f4df670a03cce7eda.
Pinned Lean4.34.1 is unchanged.

Run `bash companions/cap_i4_matrix_20261006/replay.sh` in the hosted workflow.
It checks source/parent/dependencies, warning-as-error compilation, every exact
contract and axiom/type inventory, explicit command statuses, fresh leanchecker,
two exact False-goal rejections, seven finite/source tests in both Python modes,
and unchanged before/after source records. Inventory parsing is not a general
Lean parser or independent source alignment. Source code/tests and a green
workflow are distinct from mathematical/model review. The initial contract is
published without the module to obtain actual missing-module RED evidence;
later runs retain their real outcomes.

## Boundaries

This is the deterministic 2x2 cone interface for transverse dimension2 only.
No Lebesgue Jacobian, Weyl/angular formula, Gaussian density, residual independence,
moment bound, typed-weight estimate, full normalizer, geometric elder event,
uniform radius, coefficient, primary63-target replay or parent-theorem closure
is awarded. The separately owned linear-volume and angular work stays separate.
The exact-head execution and nonauthor disposition must be read before reuse.
