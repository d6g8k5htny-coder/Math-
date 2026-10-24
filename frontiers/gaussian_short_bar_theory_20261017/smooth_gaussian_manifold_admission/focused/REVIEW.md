# Focused nonauthor review: dense smooth support and literal-target Gaussian kernels

**Verdict: ACCEPT_SCOPED. No must-fix finding or required amendment in the reviewed focus.**

This is a fresh conventional mathematical review of the exact new author proof
`PROOF.md`, 40,231 UTF-8 bytes / 739 lines, SHA-256
`8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319`.
The author freeze is 2,203 bytes, SHA-256
`3f1338445bf20cf6d1300fbdf1ddbc687b4abb0ab318b777b7fb70bf77121c5e`.
The reviewed theorem concerns the actual independent Gaussian series specified
in that proof, with positive weights, dense smooth span and summability of every
weighted smooth norm. This review does not silently admit every smooth field,
every law having the same covariance, or every Gaussian law lacking these
hypotheses.

The reviewer is OpenAI/Codex
`/root/reverse_localization_nonauthor_review_20261017/dense_support_rice_nonauthor`.
The reviewer did not author this proof, the dense-support admission mechanism,
the previous ST/IG sources, or their cited reviews. The proof, exact consumed
sources and their reviews were exposed before this review. This is a distinct
source-exposed nonauthor mathematical review with organizational-independence
credit **0**. It is not blind, human or provider-distinct review.

## 1. Scope, actual reads and the accepted conclusion

The new 739-line proof was read in full. The verdict is restricted to §§2–4 and
§§6–7: nonemptiness and dense smooth support; finite original coefficient
minors; actual whole-field Gaussian regression; fixed-target all-Borel
finite-block Rice; and contact-conditioned off-contact Morse and critical-value
genericity. The other new sections were read for compatibility and context;
their geometry, coefficient, antipodal and complete theorem conclusions remain
the integrated reviewer's separate responsibility.

The exact copied ST source is 43,927 bytes, SHA-256
`3d952a906553d578876456539a8f0dcd64aedd45099e8394cbe9db99866ec531`.
I read its §§1–2, §4 and §8, including the literal COUNT contract and precise
contact-global genericity premise of the deterministic elder adapter. The exact
copied IG source is 34,629 bytes, SHA-256
`c8bd489ca3fbb3760f7b2d53e7385131ac5336c51ba983e00e4d540fe2f00aaa`.
I read its §§5–6 as the preceding finite-block/tail route. Both source-bound
review records, the new input manifest, the new author freeze and the new
author read-extent record were read in full. `INPUT_MANIFEST.json` records eight
actual retained input copies and the precise partial read extents. The copies
were byte-hash compared with the relevant author-freeze entries. I did not
read or execute the author's 137-control program or use its result as proof.

Within this focus, the proof establishes the following chain without a missing
probabilistic-genericity assumption:

1. A nonempty class of actual smooth Gaussian laws exists on each declared
   compact smooth manifold, with all positive smooth-norm moments and full
   support in the smooth Fréchet topology.
2. Dense span realizes every required independent finite jet observation through
   a finite subset of the **original weighted independent coefficients**.
3. Finite-observation regression specifies a jointly Borel whole-field kernel
   at each literal observation target, including target zero and the forced
   cubic-contact target.
4. Finite incidence plus weighted area gives all nonnegative Borel marks at the
   literal gradient target zero. Its conditional field kernel is the same
   canonical regression kernel; no almost-everywhere version is silently
   evaluated at an exceptional target.
5. Conditional on each specified contact target, the off-contact critical
   points are Morse, have pairwise distinct values different from the contact
   value, and form a finite set after contact isolation. These are exactly the
   genericity premises needed by the consumed deterministic elder adapter.

These conclusions are under the explicit smooth Sard, weighted area and other
classical imports retained by the proof. They do not themselves prove the entire
admission theorem, its leading coefficient, a Poisson limit or formal Lean
alignment. No production source, native board, claim, runtime or scientific
status was changed during this review.

## 2. Nonemptiness, smooth series and support

The localized Fourier construction in §2 is valid. Compactness permits a finite
coordinate-cube cover with a smooth partition subordinate to relatively compact
chart interiors, plus larger chart cutoffs. Each localized summand of a smooth
function extends by zero to a smooth periodic function. Its Fourier sums converge
in every prescribed derivative norm. Multiplication by the larger cutoff gives
globally smooth finite linear combinations of the declared list, converging to
that localized function. The finite sum of localized approximations converges
to the original function in the smooth topology. This requires the stated
partition/cutoff import; it does not require a spectral completeness theorem or
a globally trivial tangent bundle.

For a fixed smooth norm order q, the explicit positive weights in equation (4)
give a summable tail bounded termwise by 2^(-j), with only finitely many earlier
indices. Thus the class is nonempty and every required A_q is finite.
Allowing a list with redundant or zero functions causes no problem: positivity
is required of the weights, and the weighted span retains the dense unweighted
span. A later finite full-rank selection simply avoids redundant columns.

The random upper bound B_q has finite expectation by nonnegative Tonelli and
the finite first absolute Gaussian moment. Hence it is finite almost surely.
Taking the countable intersection over q gives absolute uniform convergence of
every derivative series on the same probability-one event. Smooth completeness
then identifies a smooth field. Minkowski applied first to finite partial sums
and then to their monotone upper bounds gives all L^p bounds for p>=1; smaller
positive moments follow from those. No infinite standard Gaussian coefficient
vector is required to belong to unweighted l2 or to have bounded norm.

The covariance derivative series are justified by the same deterministic
summability. For any two derivative orders, the sum of diagonal products of
the weighted derivative bounds is at most the product of their finite sums.
This provides uniform absolute convergence of the mixed covariance derivatives
and proves a smooth covariance kernel. Each finite vector of field observations
is Gaussian as the L^2 limit of its Gaussian partial sums. The almost-sure
smooth limit is a Borel random element in the smooth Fréchet space.

The support argument respects the two independent pieces of the original law.
For a prescribed smooth-neighborhood ball, choose a fixed finite approximant,
then enlarge its containing prefix with zero target coefficients until the
expected remaining norm is small. Markov gives positive probability of a small
tail. The finite Gaussian prefix has a positive density near the prescribed
coefficients, since each selected weight is strictly positive. Prefix and tail
are independent. Their positive-probability intersection lies in the requested
ball. This proves full smooth support, not merely dense possible deterministic
series values.

Full support is not by itself a probabilistic transversality theorem. For
example, mixing a full-support smooth law with a positive atom at the zero
function preserves full support but gives positive probability of a non-Morse
sample. The proof does not make that invalid inference; it subsequently uses
finite absolutely continuous Gaussian coordinates and Sard.

## 3. Dense span to finite minors and residual ranks

The finite-dimensional annihilator argument in §3 is complete. Given finitely
many linearly independent continuous functionals L_i, failure of their weighted
column span to be all of R^m gives a nonzero annihilating vector c. Positivity of
all weights and density of the smooth span would force the continuous functional
sum c_i L_i to vanish on every smooth function, contradicting independence.
Since the target is finite dimensional, finitely many columns already span it.
Their positive covariance sum is a lower bound for the full covariance. No
compactness statement about the entire infinite coefficient sequence is used.

The required functional independence follows from disjoint bump-polynomial jet
interpolation. At finitely many distinct sites, coordinate polynomials with
cutoffs realize arbitrary finite Taylor jets independently. The displayed
contact rows consist of the value, all gradient components, the independent
axial Hessian column and one pure axial cubic component. The additional
transverse symmetric Hessian entries are not duplicates of that column.
Lower-order connection terms are triangular changes of jet coordinates and do
not destroy these ranks. The proof's use of independence here means linear
independence of functionals, not statistical independence of arbitrary jet
coordinates; later Gaussian covariances and conditional means are allowed to
be correlated.

The important conditional implication is stronger than separate contact rank
and remote rank. Surjectivity of the combined map (L,J) implies that J maps
ker L onto the entire remote target: for each y, lift the pair (0,y). It follows
that J P J^T is positive definite for the contact orthogonal projection P.
Likewise, joint rank of the contact and transverse Hessian coordinates makes
the latter's Gaussian Schur complement positive definite. This establishes
the full conditional transverse density and off-contact residual first-jet
densities actually used later.

Continuity gives each selected finite minor a working neighborhood. A finite
cover of a compact separated tuple domain, followed by the union of the
selected original columns, gives one finite block for that domain. Adding
columns cannot reduce row rank. The resulting covariance matrices are
continuous and have positive compact eigenvalue floors. Local frame changes
are invertible, and the orthonormal frame bundle is compact. A global
perpendicular frame is unnecessary.

There is no single finite block claimed to work down to all collisions. The
countable domains separated from the fixed contact and the pair diagonal are
the correct scope for the later conditional genericity proof.

## 4. The whole-field regression kernel at literal targets

For a finite full-rank observation L F=U with covariance Sigma and covariance
field c, write

    R = F - c Sigma^(-1) U.

Every finite evaluation vector of R is jointly Gaussian with U and has zero
cross covariance with U. Therefore it is independent of U. Independence for a
countable collection of evaluations identifies independence of the smooth
random element itself. The map

    Q_v = law(R + c Sigma^(-1) v)

is consequently a regular conditional field law, explicitly defined at every
v. Applying L gives the exact target because Lc=Sigma. No positive-probability
pin event is asserted.

The countable-evaluation identification is appropriate for C-infinity(X).
Choose countably many rational coordinate points and difference-quotient
sequences in a finite atlas. Derivative evaluations are measurable limits of
value evaluations. Smooth seminorms are suprema on countable dense coordinate
subsets. Rational finite combinations of the dense system give a countable
dense subset of the Fréchet space, so these seminorm tests generate its Borel
sigma-field. Hence equality of every finite evaluation law gives equality of
whole smooth-field Borel laws, including arbitrary global Borel marks.

The finite-difference contact rows in (7) have the declared smooth limit and
uniform boundedness as functionals of C^3. Their difference from the contact
rows is O(r) on C^4. The fourth row is a third-derivative averaging functional;
bounding its apparent singular summands separately would be wrong, but is not
the method used. Compact parameter control and smooth covariance differentiation
then give the small-r covariance floor and convergence of covariance fields in
every required smooth norm.

The explicit same-field regression formula thus gives global C^4 convergence,
almost surely and in finite L^p, both at fixed parameters and along convergent
parameter sequences. Its smooth-norm upper bound keeps a single random term
with all finite moments and a deterministic term linear in |b|+k. It does not
apply finite-dimensional norm equivalence to an infinite coefficient vector.

The claimed support of the residual law is also correct: H=I-c Sigma^(-1)L is a
continuous projection of smooth functions onto ker L and is identity there.
The preimage of a nonempty relatively open subset of that kernel is nonempty
and open. Full support of F gives it positive probability. Translation gives
full support in the affine fiber. This is auxiliary support information; the
subsequent incidence arguments use actual finite residual Gaussian densities.

## 5. Finite-tail Bayes and the null-fiber issue

I reconstructed the literal-target calculation rather than relying on an
almost-everywhere conditional-law theorem. Let xi in R^n and eta in R^s be
independent standard Gaussian vectors. Use a full-row-rank finite block L,
tail observation matrix T, and a finite evaluation vector

    U = L xi + T eta,       Y = A xi + B eta.

Put S_B=LL^T, S=S_B+TT^T, and

    P=I-L^T S_B^(-1)L,
    C_t=I-T^T S^(-1)T.

The tail Bayes density is p_(L xi)(v-T eta)/p_U(v). Completing its finite
Gaussian square gives precision

    C_t^(-1)=I+T^T S_B^(-1)T

and mean T^T S^(-1)v. The determinant identity

    det S = det S_B det(I+T^T S_B^(-1)T)

gives the normalizing constant. These identities hold for every v, with no
excluded target set. Given eta, xi has mean L^T S_B^(-1)(v-T eta) and residual
covariance P.

Writing D=B-A L^T S_B^(-1)T, the integrated conditional evaluation law has mean

    A L^T S_B^(-1)v + D T^T S^(-1)v
      = (A L^T+B T^T)S^(-1)v

and covariance

    A P A^T + D C_t D^T
      = AA^T+BB^T
        -(A L^T+B T^T)S^(-1)(L A^T+T B^T).

These are exactly the full joint Gaussian conditional mean and covariance at
the same literal v. The finite conditional characteristic functions therefore
agree at every v. For the infinite tail in the proof, only its finite
observation/evaluation vector enters this calculation; it is jointly Gaussian.
Countable evaluations then identify the whole-field Borel kernel as above.

This establishes the specific issue required by COUNT: the finite area-formula
fiber law at gradient target zero equals the canonical regression law there,
even for a globally discontinuous Borel elder selector. It does not extend a
continuous-mark formula by guessing a value on a null fiber.

The finite block may come from an overcomplete or noninjective smooth series.
That causes no problem. The calculation conditions the augmented original
coefficient/block/tail probability space, then pushes its law to the field.
It does not require that a tail or an individual coefficient can be recovered
as a Borel function of the field.

Keeping the original tail law after pinning would generally be wrong. The
displayed Bayes reweighting is essential, as is an orthonormal basis of ker L
for independent standard residual coordinates. In an arbitrary kernel basis N,
the correct covariance is N(N^T N)^(-1)N^T; simply using N N^T changes the law.
Both failures are distinguished by the new exact controls below.

## 6. All-Borel Rice and unconditional genericity

For a smooth fixed tail and a locally invertible gradient coefficient minor,
the exact incidence solution is a(p,eta)=-B(p)^(-1)(grad T(p)+D(p)eta).
Its equal-dimensional coefficient projection is smooth. Differentiating the
zero-gradient equation gives selected spatial derivative -B^(-1)H in physical
orthonormal coordinates. Terms from differentiating a moving frame multiply
the vanishing gradient. Thus the incidence projection is singular precisely
when the Hessian is singular. The smooth Sard import makes the corresponding
coefficient values null. The finite Gaussian block has a Lebesgue density.
Countably many charts and minor neighborhoods cover the critical-point
possibilities; integration over the independent smooth tail proves Morse
genericity before Rice is used. This avoids a Morse-to-Rice circularity.

For pair incidence, the spatial derivative at two gradient zeros is the block
diagonal physical Hessian. Its projection Jacobian is the absolute product of
the two Hessian determinants divided by the chosen coefficient-minor
determinant. The weighted equal-dimensional area formula supplies multiplicity
and every nonnegative Borel field mark from the outset. The coefficient change
of variables restores the observation density and its exact fiber law. There
is exactly one Hessian determinant product, not a second hidden determinant
weight.

The proof correctly partitions overlapping spatial/minor charts into disjoint
Borel pieces and exhausts their unbounded coefficient coordinates by compact
subdomains. Only local Lipschitzness of each smooth finite-dimensional map is
needed. Nonnegative Tonelli and separated-domain exhaustion therefore justify
the extended formula without presuming finiteness or conditional genericity.
The fixed-target calculation in §5 above supplies the required canonical
kernel on its right side.

Positive first-jet covariance gives nondegenerate conditional height laws.
The critical-value tie mark has zero integral after height disintegration,
including its determinant weight. Compact separated domains supply the
required finite Gaussian determinant moments and covariance floors; countable
annulus exhaustion removes the separation restriction. The analogous
single-point calculation gives finite expected critical-point count, and
compactness plus the already proved Morse property gives finiteness almost
surely. The exact ST Borel selector and named Morse/H0 once-counting package
can therefore be consumed on the resulting Morse/distinct locus.

The everywhere Borel selector remains zero on its complement. No conclusion
about conditional Morse genericity at each finite-r observation target is
needed to define or integrate that selector. The topological once-counting
and complete final intensity derivation remain separate aspects of the parent
integrated review, rather than new conclusions established by this focus.

## 7. Contact-conditioned genericity and countable-domain joins

Fix x,u,b,k with k>0 and the precise contact target. The canonical law has a
forced degenerate critical point at x, so it is not a globally Morse law.
The proof treats that fact correctly.

For each compact domain away from x, choose a finite original block witnessing
the joint contact/remote ranks. Its contact covariance is positive. Under the
literal contact law, the original smooth tail is reweighted by equation (20).
This density is positive and has a finite upper bound for the fixed target,
so the conditional tail stays smooth and retains all required finite moments.
Given any smooth tail, the finite contact fiber has the deterministic mean
in (21) and covariance projection P_B. Choosing an orthonormal kernel basis
gives independent standard Gaussian free coordinates. The mean may depend on
the target and tail; the argument does not discard that mean.

Joint rank implies remote first-jet surjectivity on these free coordinates.
The finite Sard construction consequently proves that all critical points in
the chosen domain are Morse for almost every conditional coefficient vector.
The same finite incidence/area derivation applies to all Borel marks under
this conditional law. Residual first-jet rank gives a nondegenerate height
given the remote gradient; residual paired-first-jet rank gives nondegenerate
two heights given the two remote gradients. These kill the marks F(p)=b and
F(p)=F(q), respectively.

All covariance floors are asserted on domains with positive separation from
x and from the pair diagonal. The proof does not require a uniform floor
as a remote point approaches x, nor a finite block valid for all such points.
The compact domains can be covered by open minor neighborhoods; boundaries
of a chosen domain introduce no new application of Sard to a singular domain.

Different separated domains may use different finite blocks and residual
bases. This remains legitimate precisely because the literal-target Bayes
calculation identifies each resulting pushed-forward law with the same
whole-field Q_0. Their countably many probability-one conclusions can be
intersected under that one Q_0. The proof makes no simultaneous assertion
over uncountably many contact targets or frames.

Finally, the conditional transverse Hessian A_0 has a full Gaussian density,
so it is invertible almost surely (with the empty-block convention in d=1).
At the contact the axial Hessian column is zero. The implicit transverse
ridge consequently has derivative zero there; its reduced first and second
derivatives vanish and its reduced third derivative is 12k. The reduced
derivative is 6k s^2+o(s^2), positive for sufficiently small nonzero s.
Thus the forced contact is isolated without requiring A_0 negative definite.
The other critical set is closed inside a compact region away from that
contact. Its points are isolated Morse points, so it is finite. Its already
excluded equalities give finite positive gaps between other critical values
and from b. This is exactly the contact-global genericity hypothesis of the
consumed ST deterministic elder theorem.

## 8. Fresh controls, limitations and disposition

One new reviewer-authored rational-arithmetic program was run once. It uses
six explicitly weighted finite block/tail matrix families. It performs no
sampling, numerical integration, Lean execution, source runtime or author
control replay. All **168 exact identities passed**. The program retains
**18 negative-control instances in three families**, six of each:

* An unwhitened nonorthonormal kernel basis does not reproduce the Gaussian
  contact projection covariance.
* Leaving the tail unreweighted after the observation changes the conditional
  evaluation covariance.
* A remote map can have full unconditional rank while sharing a pinned contact
  row, and then loses conditional rank. Joint contact/remote rank is essential.

Positive checks cover projection symmetry/idempotence, exact pins, the
Gram-corrected kernel covariance, positive residual remote minors, Bayes
posterior precision and normalization determinant, equality of one-stage and
two-stage conditional evaluation means/covariances at four literal targets per
family, and the selected-minor incidence Jacobian and singularity relation.
The result is `PASS_EXACT_RATIONAL_CONTROLS`, exit 0, with empty stderr.
These finite checks support the analytic reconstruction; they do not replace
the proofs of smooth convergence, Sard, area, Borel identification or genericity.

The explicit classical imports remain imports. No external primary source,
licensed book or complete classical theorem was newly read in this focused
review. The author read-extent metadata was inspected, and no primary-read
credit is inferred from an index, abstract, bounded pointer or earlier review.
In particular smooth finite charts/partitions, smooth Sard and the weighted
equal-dimensional area formula are premises with their stated scopes. The
named Morse/flow/handle package belongs to the consumed deterministic H0
argument and the integrated review. This review does not pretend to prove
those foundational classical results from the new control program.

There are no must-fix findings and no requested source amendment within the
focus. Acceptance covers the exact frozen bytes only. It does not include
arbitrary non-Gaussian covariance classes, weakly supported Gaussian laws,
uniform constants over degenerating spectra/metrics/dimensions, an effective
window, higher homology, point-process convergence, numerical field validation,
blind-50 credit, Lean compilation/kernel evidence, source adoption, publication
or scientific promotion. The full project goal remains ACTIVE / UNMET.
