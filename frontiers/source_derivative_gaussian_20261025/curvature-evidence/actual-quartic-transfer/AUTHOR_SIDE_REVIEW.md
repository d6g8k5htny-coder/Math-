# Author-side mathematical review: actual quartic transfer

26 October 2026. Reviewer/author: OpenAI/Codex
`/root/normalizer_palm_research`. This is same-family author-side critique,
not independent scientific review, Lean qualification, theorem promotion, or
closure of capture, Palm identification, or the lifetime/counting parent.

Reviewed snapshot: `PROOF_CANDIDATE.md`, SHA256
`0c02f1973e7e4bf519bed5e3ca54e343b1d450d24c31bcc94805d3f7d9a622a9`.
The owner is amending its support/norm wording after this review; the arithmetic
assessed here is the unchanged arithmetic of that snapshot.

Source alignment used:

- `/workspace/Math-curvature-20261026/imports/hardening_ebedb780/P02-LM-001/proof.md.export.txt`,
  LCR-CAP-009-v1.0, exact frozen polynomial, eight-coordinate U, threshold,
  geometry, selected increasing-xi branch, and conditional degree-four scope.
- `/workspace/scratch/LM004-frozen.md`, LCR-DER-016-v1.1, frozen-body SHA256
  `d43179f3abfd7e93f988725f3b89a5826cc71e0fa04840f65c7f93f3359d0f87`.
  Its C1 norm is the maximum of value-Euclidean and derivative-operator suprema;
  its robustness tolerance is RW/4. Its own scientific-review status remains open.
- Read-only source inspection of `SourceConditionalMajorant.lean`,
  `SourcePinCurvatureBounds.lean`, and `SourceSmoothPalm.lean` in the new curvature
  worktree, solely to identify the actual norms, majorants and pin-support premises.

No existing Lean proof, build, test, gate, or baseline verification was rerun.
Completed source mathematics is reused. The activity below is the newly requested
paper-level critique and source/interface comparison.

## Verdict and one application-scope repair

The deterministic pin-preserving comparison and the global-cutoff-to-adaptive-
tolerance argument are mathematically consistent with the stated hypotheses.
I found no error in the requested coefficients, powers of r, constants, polynomial
transcription, or branch/time scaling. The argument avoids the earlier invalid
identification of the actual endpoint Hessians with a frozen raw midpoint jet:
it compares the actual field to a separately defined pin-preserving polynomial
with a proved remainder, rather than asserting exact endpoint equality.

The reviewed introduction overstates the actual-law support unless its radius is
qualified. `sourceSmoothLaw hL r b` has the asserted exact raw pin support under
the current covariance-invertibility hypothesis. `hL : L != 0` supplies that
hypothesis for all sufficiently small positive r through the completed parameter-
limit theorem, not as an unrestricted assertion for every 0<r<=1. For example,
at L=r=1 the periodic field has equal values at (-1/2,0) and (1/2,0), whereas
the requested height difference is -1/6; those pins cannot both hold.

Repair: retain the deterministic theorem for every sample satisfying its displayed
pins, and state the probabilistic application for current invertible G, or restrict
to the already derived small-radius interval. In the eventual application take the
minimum of that radius, the normalizer/curvature radii, and 1. This changes no
Taylor or tolerance calculation and adds no new probabilistic premise to a final
hL-only eventual theorem. Root explicitly accepted this repair during review.

Two norm/interface clarifications are also essential, although neither invalidates
the mathematical inequalities:

1. The existing Lean domain `Fin 2 -> Real` has the Pi/sup norm. To read its
   scalar multilinear derivative bound in Euclidean coordinates, state the bridge
   ||v||_infinity <= ||v||_2. Euclidean unit directions are therefore sup-norm
   bounded by one, so the source Gamma bounds dominate the needed Euclidean
   directional derivatives. The subsequent component-gradient and Hessian
   conversions already include their factor-two losses. Root accepted making
   this bridge explicit.
2. The final constant 3 is for the exact **maximum** C1 norm in LM004. A sum of
   the two displayed suprema would instead be bounded by 3989/960>4. There is
   no mismatch when the source norm is used, but a generic differently normalized
   C1 norm must not be substituted silently.

## Axial pin5 estimate

For K(v)=1/4-v^2 on [-1/2,1/2], K is nonnegative and even. The exact moments are

    integral K = 1/6,
    integral K*v = 0,
    integral K*v^2 = (1/4)(1/12)-1/80 = 1/120.

Consequently 6 integral K*v^2=1/20. The actual pins imply pin5=2: the mean
endpoint axial derivative is zero and the divided height difference is -r^2/6.
The already available Peano representation thus has the correct sign and
normalization, 2=6 integral K(v) u'''(rv) dv.

The Taylor remainder for u''' is at most G r^2 v^2/2 because its second
derivative is the axial fifth derivative. The linear term r v c40 cancels
against the odd kernel moment. The resulting bound is exactly

    |t-2| <= 6*(G r^2/2)*(1/120) = G r^2/40.

This step needs C5 regularity on the axial segment and a fifth-derivative bound
there. The actual smooth carrier and global Gamma5 supply both. A Gamma4
Lipschitz estimate alone would not supply this second-order cancellation bound.

## Low Taylor coefficients and the exact LM001 polynomial

Writing h=r/2, each endpoint remainder for a degree-three expansion of f_x or
f_y is bounded by G h^4/24=G r^4/384. Taking the average and then the divided
difference of the two zero endpoint gradients gives exactly

    |f_x(0)+t r^2/8| <= G r^4/384,
    |f_xx(0)+c40 r^2/24| <= G r^3/192,
    |f_y(0)+a r^2/8| <= G r^4/384,
    |f_xy(0)+c31 r^2/24| <= G r^3/192.

The axial t correction contributes (r^2/8)*(G r^2/40), hence

    1/384 + 1/320 = 11/1920

in the corrected constant x coefficient. The constant y coefficient is bounded
by 1/384=5/1920. After dividing the gradient by r^2, their Euclidean norm is
bounded by their absolute sum, (11+5)/1920=1/120 times G r^2.

The scaled Hessian correction has only entries xx and xy=yx, each bounded by
G r^2/192; its yy correction is zero because q/r is retained exactly. The sum
of the absolute entries bounds its Euclidean operator norm and gives
3/192=1/64. The remaining quadratic discrepancy is precisely
((t-2)X^2/2,0), with value bound G r^2 d^2/80 and derivative bound
G r^2 d/40.

The polynomial in the candidate matches the capsule coefficient by coefficient.
In particular the linear corrections are -r c40 X/24 and -r c31 Y/24 in
P_X, and -r c31 X/24 in P_Y. Mixed differentiation gives
partial_Y P_X=partial_X P_Y. The use of literal a=f_xxy and c31=f_xxxy,
and the exclusion of q from U, are correct. No rescaling of a,w,z or the
fourth-order coordinates is missing: the r^-2 gradient scaling leaves the
third derivatives at order one and multiplies the fourth derivatives by r.

## C1 comparison and constants

For an evaluation point of Euclidean norm d, the degree-three gradient Taylor
remainder is bounded componentwise by G r^2 d^4/24 after scaling. Passing to
the Euclidean vector norm with sqrt(2)<=2 gives G r^2 d^4/12. The Hessian
Taylor remainder is bounded entrywise by G r^2 d^3/6; the 2-by-2 operator
norm bound by twice the maximum entry gives G r^2 d^3/3. These losses are
safe, and differentiate the same scaled Taylor polynomial.

The two coefficient sums at d=2 are exactly

    1/120 + 2/64 + 4/80 + 16/12 = 683/480 < 3,
    1/64  + 2/40 + 8/3          = 2623/960 < 3.

Thus the stated maximum C1 error on the closed ball of radius two is at most
3 r^2 Gamma5. A physical neighborhood of the compared ball suffices for all
Taylor arguments; the actual field is globally smooth, so this is available.
The Euclidean gradient identity is also correct:

    r^-2 grad f(rZ) = grad_Z (r^-3 f(rZ)).

## Radius, curvature threshold, and adaptive tolerance

All relevant coordinate directions are unit directions. Therefore

    R0 <= 1+3 Gamma3+5 Gamma4 <= 5R.

The q coordinate is correctly omitted. With K0=4096,

    Kcap = 2*K0*5^5+10 = 25600010,
    epsilonStar = epsilon0/5^5,

the global cutoff implies r R0^5<=epsilon0. Since R>=1,
2 K0 R0^5+2 R0 <=(2 K0 5^5+10) R^5, so the negative curvature hypothesis
implies exactly the capsule threshold q/r<=-(2 K0 R0^5+2 R0).

Fstar>=1 gives R0 W>=1/(K0 R0^4). The sufficient relative-error quantity is
12 K0 R0^4 r^2 Gamma5. Using R0<=5R, Gamma5<=R, and r R^5<=epsilonStar,

    12 K0 R0^4 r^2 Gamma5
      <=12 K0 5^4 r^2 R^5
      <=12 K0 5^4 r epsilonStar
      =3r/1280 <=3/1280 <1.

This proves 3 r^2 Gamma5 <R0 W/4 with room to spare. The claimed absence of
an additional fifth-derivative tail is justified: Gamma5 is already contained
in the very same global radius cutoff. The strict comparison also covers
equality in the regularity and negative-curvature hypotheses.

The geometry fits inside the compared ball. From R0 W<=1/2048 one obtains
rho<=1/256 and W<=1/2048. The endpoint centers have norm 1/2, the strip has
|X|<=1/2, and every cone piece used before handoff is contained in the saddle
ball. Sections and the transit rectangle are subsets of these bounded regions.
The assertion concerns these truncated certificate cone pieces, not the whole
unbounded cone. One may choose the fixed compact chart D to be the radius-two
closed ball and an open neighborhood O of it.

## Flow, logical inclusion, and remaining obligations

For the physical ascending gradient flow x'=grad f(x), x=rZ gives
Z'=r^-1 grad f(rZ)=r F_r(Z). Since r>0, this is a positive constant time
change. Spatial multiplication by r preserves e_u dot(M-S)>0, the selected
M-ward unstable branch, and convergence to M. It does not reverse the flow.
If the eventual event is formulated on the quotient torus rather than its real
cover, explicitly compose the projection/chart and the branch definition. A
further small-radius restriction r<|L|/4 is a simple way to make the physical
radius-two chart injective; fixed L!=0 permits this without a new tail event.

Conditional on a valid/applicable exact LM004 robustness implication, the
deterministic implication produces the proposed complement inclusion with
strict events

    {epsilonStar < r R^5} union {q > -Kcap r R^5}.

The curvature probability theorem's version with q>=-Kcap r R^5 is a valid
larger event. This logical enlargement introduces no lost equality case.
It becomes a probability statement only after the capture event/branch is
defined measurably and the pin-support/weighted-law joins are supplied.

The concrete next formal obligations are:

1. Define the literal Euclidean gradient, raw derivative table, and source
   sup-norm-to-Euclidean bridge; justify mixed derivative symmetry from smoothness.
2. Formalize the second-order Taylor remainder for u''', the three Peano moments,
   the endpoint low-coefficient inequalities, and the exact coefficient identity
   between the scaled Taylor polynomial and LM001's pin-preserving polynomial.
3. Formalize both vector/operator Taylor bounds and the maximum C1 estimate on
   the fixed ball, then the arithmetic cutoff-to-R0W/4 implication above.
4. Keep LM004's scientific validity and source-bound independent review distinct
   from these analytic calculations. Its frozen candidate header is not a proof
   qualification, and this review supplies no different-family credit.
5. Prove the exact measurable capture/selected-branch interface and flow/chart
   transport; apply raw prescribed-pin support on the derived small-radius
   interval and transfer the deterministic inclusion under the actual weighted law.

These steps still do not establish global elder pairing, a geometric point-process
Palm disintegration, or the lifetime/counting parent theorem. No such conclusion
is assumed or certified by this author-side review.
