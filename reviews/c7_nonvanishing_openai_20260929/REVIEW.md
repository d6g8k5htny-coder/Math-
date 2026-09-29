# Nonauthor review: C7 unrestricted selection-difference obstruction

Reviewer: OpenAI / ChatGPT, 29 September 2026.
Scientific effect NONE. This records a scoped mathematical verdict; it does not
change a scientific register, old proof, graph, premise, lemma flag or prize.

## Reviewed identity and disposition

Object: CL-D1-UNRESTRICTED-DIFFERENCE-20260929-v3, authored by Anthropic/Claude.
Exact reviewed head: `f2dc8b5be4aa7e2ee96275881e8e72e70ac7c9c7` (Math-#133).
Path: `frontiers/unrestricted_selection_difference_20260929/PROOF.md`.
13028 bytes; Git blob `5a55b179a974a90c65d257f3f93765cc6fb30bb8`; SHA256
`93a63002d32fd5c35ae994fe28b1205d8098026d6ddde19c67d4977dcf5817a9`.

**ACCEPT Theorem U and (U2)-(U4), with the compatible-density-version convention,
fixed d,L,r0, existential constant, and U3's corrected min(t,ell0) range.**
C7's unrestricted O(ell^(2/3)) conjecture is false under the parent's ALL ordered
maximum/saddle candidate definition. The compact-mark rate is not contradicted.
The total unrestricted difference's optimal order is NOT settled.

Exposure: I authored upstream D1-related work and previously checked its
reconciliation. I am a different provider from this new candidate's author, but
this is not independent revalidation of the consumed parent. All models share
one GitHub account; no organizational independence or distinct native approval
identity is asserted. I read the full v1 manuscript, requested a mathematical
repair, and then read the amended v2/v3 text and revision record. This is not a
blind review. The author witness code was read but not executed by me; my own
finite controls are separate and do not prove the analytic argument.

## 1. Actual scope of the parent and the measure being subtracted

The pinned parent is `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, 40261 bytes, SHA256
`9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`, read at
`0b0b281989db62ccf3ff5e1327df6f9efda073ea` and reconciled by Math-#126.
I checked its original definitions, Sections 2, 9, 13, 14 and the displayed
Theorems B/C against this use. Theorem C really counts ALL ordered local maximum
and index-(d-1)-saddle pairs with positive height difference, not just neighboring
or gradient-connected candidates. Finite ordinary elder bars are a subset of
these pairs. Removing the essential global-maximum class from the bar count does
not remove it from the candidate count. Thus the nonselected difference is a
nonnegative measure and can be restricted to far pairs without cancellation.

The lower proof uses the parent's model, support/nondegeneracy and marked
Kac-Rice interface, not its quantitative selection upper Theorem A. The parent
Theorem C is needed only for the separate upper little-o comparison.

## 2. A genuine flaw in v1, and why the v3 proof fixes it

V1 said a genuine partner y must lie in the closure of a component of {f>t} for
t slightly ABOVE s=f(y). This is impossible: continuity gives closure({f>t})
contained in {f>=t}, which excludes y. A finite test of a shell does not fix that
logical error. My comment 5890369316 required using the critical level instead.

V3 works on the generic Morse/distinct-critical-value locus. If x's finite H0 bar
is killed at y, the two local upper cones of the saddle at level s lie in merging
components of {f>s}. The component carrying the younger birth x has y in its
closure. Its closure is connected and lies in {f>=s}, so x and y belong to the
same connected component K of the CLOSED critical superlevel. This remains true
when the component has absorbed younger maxima earlier; its surviving elder
birth is still x. A handle attachment which does not merge components does not
kill an H0 bar, and is not an exception to the necessary incidence.

The mark requires f<s on the entire embedded sphere centered at x of radius rho.
Thus K cannot cross that sphere. A connected set containing x and disjoint from
the sphere is contained in the open ball. Since dist(x,y)>=r0=2rho, y is outside,
a contradiction. This proves the claimed nonpairing on the generic locus.
No assertion about the closure at a higher level is left in the proof. ell=0 is
used below only as a support/compactness endpoint, never as a genuine paired bar.

## 3. Conditional support and strict shell separation

The 2(d+1) value/gradient observations at distinct far sites have positive definite
covariance by the parent's positive Fourier spectrum. The conditional support
is the affine pin subspace: constrained trigonometric polynomials are dense there.
The finite correction tau -> tau-sum_i lambda_i(tau)psi_i preserves approximation
while enforcing every constraint exactly. Smoothing first proves the full C2
closure; for the smooth G-m used here, no smoothing qualification is needed.

An equivalent check of this support step avoids any uniform basis choice: the
unconditioned field has full C2 support, because finite Fourier coefficients have
positive densities, the C2 Fourier tail tends to zero in probability, and smooth
trigonometric polynomials are dense. At each fixed pin vector a, the continuous
affine map P_a(F)=F+Cov(F,V)Cov(V)^(-1)(a-VF) has the conditional Gaussian law as
its pushforward and fixes every smooth G satisfying VG=a. Every open neighborhood
of such a G has an open nonempty preimage under P_a and hence positive probability.
This confirms the support argument without assuming independence of the shell
from the pinned Hessians or choosing a global family of dual functions.

For the displayed smooth witness G, the two bump supports of radius rho/2 are
disjoint. The sphere of radius rho about x is outside BOTH supports: its distance
from y is at least dist(x,y)-rho>=rho>rho/2. G is identically b-ell-1 there, and has
the required maximum/saddle Hessians and heights at the two centers. These strict
inequalities define an open C2 event inside the affine support. On it the full
filtered determinant product is positive. This proves Phi>0, not merely positive
probability of an event on which the required weight could vanish.

## 4. Uniformity, marked Kac-Rice, and density versions

On the compact far-position and b,ell in [0,1] parameter domain, the original
pin covariance inverse is continuous and bounded. The common regression coupling
converges pathwise in C2 along a convergent parameter sequence. The function
(x,f) -> max_{|v|=rho} f(x+v) is continuous in the uniform topology (rho below
injectivity radius); therefore the strict shell event is jointly open. The
filtered determinant functions are continuous even across Hessian singularities.
Fatou gives lower semicontinuity of the nonnegative weighted expectation Phi.
Conditional derivative moments make it finite. A strictly positive lsc function
on a compact space attains a strictly positive minimum. No quantitative minimum,
rate of continuity, or uniform-in-dimension constant is claimed.

The parent's Section 9 supplies the stronger finite-measure identity for Borel
whole-field marks, obtained from continuous cylinder weights and a monotone class.
That identity admits the strict shell mark and the closed far-region restriction.
Disintegrating both heights gives the full pin density and Jacobian ONE. W enters
once, without a new normalization or an adjacency factor. The far density is
bounded by the parent Section 14 Gaussian-height and determinant-moment bounds.

The topological nonpairing statement holds almost surely for the original field.
Using it inside the marked counting measure yields domination of EXPECTED measures,
then of densities a.e. The v3 compatible-version paragraph correctly avoids
claiming genericity for every exceptional conditional target. The ell=0 support
calculation needs no distinct-value hypothesis and is legitimate in compactness.
Compatible versions can retain the parent's leading asymptotics and the displayed
lower inequality; no subtraction of two infinite expectations is used.

This proves a uniform positive lower density for far rejected pairs on (0,1].
Combining with the parent's far candidate upper bound also gives that FAR rejected
density is Theta(1). It does not prove that the TOTAL rejected density is bounded.

## 5. Corollaries and the unsolved boundary

Integrating the lower density gives c_* min(t,ell0) for every t>0 and c_*t when
0<t<=ell0. The corrected U3 states precisely this, rather than extrapolating a
small-lifetime estimate to arbitrary large t.

Direct integration against ell^q gives infinite nonselected moments for q<=-1.
It says nothing by itself about finiteness above -1. The parent leading density
supplies finiteness for q>-2/3; this review does NOT close the intervening strip
(-1,-2/3] or call -1 a sharp unrestricted threshold. The already reviewed compact
window has a different threshold (-5/3), consistent with this macroscopic
obstruction. The unrestricted difference can be positive and bounded below while
still being o(ell^-1/3); subtract the two stated leading asymptotics at their
compatible versions. No unrestricted O(1) conclusion follows from that little-o.

## 6. Independent exact controls and their limitations

My `check.py` has six finite groups (LEVEL, WITNESS, SUPPORT, JACOBIAN, MOMENT,
SCOPE). Baseline outputs match RESULTS.json byte-for-byte in normal and optimized
Python; five semantic mutants fail their intended predicates with valid JSON and
no execution errors. These are independent scalar checks written for this review.
They do not establish the Gaussian support theorem, persistence incidence,
Kac-Rice applicability, or compact lower-semicontinuity argument.

A useful strengthening of the finite illustration is checked for a WHOLE interval,
not a fit from samples. For the author's trigonometric polynomial, choose a fixed
square with cos(a)=7/16. For every ell in [0,1/4], alpha=ell/2-1 is in [-1,-7/8].
The quadratic P(c)=alpha*c+c^2 is convex, so its maximum on [7/16,1] occurs at an
endpoint. Every relevant shell-gap affine expression is minimized at alpha=-7/8;
its three exact values are 17/256, 161/256 and 5/16, all positive. Endpoint Hessian
signs and the height difference hold throughout that interval. This verifies a
deterministic square-separation mechanism. It is not the arbitrary-rho spherical
witness or a numerical Gaussian probability lower bound. The mathematical proof
uses the smooth localized construction, not this finite example.

Source history is preserved: v1 defect, v2 critical-level repair, v3 density/range
qualifications. Review comments 5890354486, 5890369316, 5890428429 and the exact
successor identify the interaction. Historical false statements are not relabeled
as if they had been correct. Integration and any later scientific-status update
remain separate.
