# Validation record — author-side, not analytic acceptance

Scientific effect NONE. Runtime: Python3.13.5 and Git2.47.3. Shipped code is
standard-library only and uses Python3.11-compatible syntax. The hosted workflow
requests Python3.11.16 and real historical project source objects.

## Test-first mathematical work

The initial ten-test scaffold produced ten expected assertion failures before
implementation. One proposed companion fixture was first recalculated from an
independent line/conic intersection and corrected BEFORE the implementation:
for u=-1,v=6 the correct companion is(-13/23,294/529,-7/23).

After implementation, all ten tests passed. Subsequent mathematical tests bring
the suite to35 tests:893 rational shape/companion/classifier/anchor checks;
independent exact line/conic elimination;32 exact automatic-differentiation
checks of Q(T)|det DT|=Q|t_c|^11; direct polynomial-strip integrals; dense Lagrange
interpolation checks of the rationalized Laurent integrand at four rational
y-values and four height-moment orders; strict endpoint, degree-drop and tie
cases; outward rational log(2) intervals and normalized ratios.

An exploratory generic symbolic integration timed out. The delivered integral
certificate instead uses the explicit rationalizing substitution and a finite
Laurent polynomial, integrated termwise by Fraction arithmetic. Exploratory CAS
scripts are not runtime dependencies or shipped proof evidence.

## Test-first custody work

A no-op verifier scaffold ran31 real-Git/inventory test methods and produced45
expected assertion failures (including separate subtests). The completed verifier
passed all31. Hostile fixtures cover changed historical identities, source files
whose worktree contents differ, missing/duplicate/unexpected identities, path
traversal, duplicate JSON, ancestor and leaf symlinks, tree/blob/annotated-tag
objects offered as commits, and Git replacement refs that can forge or invalidate
ordinary git-show results. All Git reads disable replacements, and the nested
packet path test exercises --full-tree. No project source tampering is asserted.

The hosted environment also sets GIT_NO_REPLACE_OBJECTS=1. Replaying the hostile
fixture under that environment first produced two expected failures because its
ordinary git-show precondition inherited the protection. The fixture now removes
that variable ONLY for its deliberately ordinary Git calls; the real verifier
always disables replacements. Replaying the same environment passes both controls.
This fixes the test harness, not the source-authentication policy.

## Fresh complete local replay

66 tests PASS under python -B -S and66 under python -B -O -S. Normal/optimized
baseline stdout is byte-identical to RESULTS.json with no stderr. The eight
semantic mutants reject with return code1 in EACH mode on the intended assertions:

| Mutation | Intended rejected statement |
|---|---|
| drop-companion-sign | signed companion |
| point-is-cluster | one maximum anchor, not point counting |
| close-window | height endpoint must be open |
| drop-log2 | inner integral |
| double-count-inner | inner integral |
| lose-height-jacobian | point integral and height convention |
| wrong-tail-power | cusp exponent ledger |
| uniform-cluster-from-point | cluster law must be unbiassed |

Unknown mutant labels return2. The complete packet inventory is authenticated
before and after replay. No temporary files or __pycache__ are added to it.

The decimal enclosures use60 rational terms of the convergent log(2) series,
a rigorous rational remainder upper bound, signed interval arithmetic, positive
divisions and outward decimal rounding. No Gaussian coefficient is numerically
computed and no quadrature is used to certify a decimal.

## Limitations and corrections

The local environment could not resolve raw.githubusercontent.com; no full
upstream checkout was obtained. Therefore local-only replay explicitly reports
source_pins_checked=false. Real-Git fixtures test the verifier but do not replace
actual source authentication. The hosted target must fetch and verify all four
SOURCES.json identities, separately from the existing full downstream/formal gates.
No hosted pass is asserted by this author-time file; actual head/run/job readbacks
will be posted on the PR, with revalidation if head or base changes.

During manuscript self-review, a loose sentence equating a uniformly chosen root
of a uniformly chosen cluster with point intensity was corrected before the
first publication. Point intensity sums over roots and biases cluster sampling;
uniformly choosing a root within a uniformly chosen cluster is a third convention.
The corrected PROOF Section8 explicitly distinguishes them.

Finite exact tests support algebra and implementation. They do not independently
prove the source Gaussian assumptions, changes of variables with multiplicity,
physical-anchor domination or weak convergence. Those new arguments require
source-bound nonauthor analytic review. Existing Lean package success is not a
Lean formalization of this manuscript. No self-merge or scientific-register fold.
