# Uniform Gaussian eighth moments: source contract before implementation

Author OpenAI/Codex /root; scalar coauthor /root/uniform_jet_moment_sources.
Scientific effect NONE; source/correctness review must use another model family.
This new work responds to the owner's inclusion of remaining parent obligations.

## Exact sources and mathematical role

Math- base e75cb81e8961d178f43aa9967dddd11cd579dc8a preserves
imports/hardening_ebedb780/P02-LM-005/proof.md.export.txt, section 2 and section 6:
the exact physical midpoint nine-jet conditional law is Gaussian N(m_r,Sigma_r),
with uniformly bounded means and covariance upper bound on a small common interval;
section 6 deduces a uniform moment for R=1+sum of all nine absolute coordinates.
The radius ordering is q,a,w,z,c40,c31,c22,c13,c04, exactly as DM2.
Source export SHA256 0fe0fad5d8e5519cac0e57a42181aa53560bb38d94f23aea51b63be3f182df8b.

Recovered primary GP-DER-044: main commit7caac254cbba5f513b2dc0afb56b78a598bc0c93,
Git blob34e38cb003a3160c154c07d293d44690a6c8b718 (catalog sources-03.md).
It fixes torus side and height b. Pins are f(-r/2,0)=b, f(r/2,0)=b-r^3/6,
with both endpoint gradients zero. Its transformed prescribed vector is
(b-r^3/12,-r^2/6,0,0,0,2), and m=C G^-1 y, Sigma=S-C G^-1 C^T.
Means are generally nonzero; the side-24 q law is not the planar N(-b,2).
No uniformity over unbounded b is supplied. We inspected the primary source;
this does not transfer its historical reviews to new Lean code.

Landed DM2 implementation: DeterminantMoment.lean, proof commit
 dcfc89366f590342b4cd30b141a22c9ae2a562bb, source SHA256
661b73c3f21c6d2529f5e09ce426d89c01939ab27a5cc868db3802c7e66ea82d.
Its dm2_moment consumes genuine integrability and an upper bound on integral R^8.
This successor derives those premises from Gaussian coordinate laws and uniform
mean/variance bounds, instead of presupposing them.

## Frozen mathematical statement

Define C8=integral |z|^8 under gaussianReal 0 1. Prove its integrability and C8>=0.
For m,B,V real, v nonnegative real, B,V>=0, |m|<=B and v<=V, prove
integrability of |x|^8 under gaussianReal m v and
integral |x|^8 <=128*(B^8+V^4*C8).
All variances, including zero, are retained; no centered-law substitution.

For a probability measure mu, measurable J:Omega->Fin9->Real, and coordinate
laws HasLaw (fun x=>J x i) (gaussianReal (m i) (v i)) mu, with common B,V as
above, prove integrability and
integral dm2Radius(J)^8 <= M8(B,V),
M8(B,V)=10^7*(1+9*128*(B^8+V^4*C8)).
There is no independence or joint-Gaussian hypothesis. This is stronger than the
source's Gaussian-vector moment deduction and preserves all its noncentered laws.

A family theorem applies the same constants on 0<r<=r0, 0<r0<=1, and composes
dm2_moment to give one uniform determinant second-moment coefficient16*M8(B,V).
No R8 or determinant second-moment hypothesis may be added to pass the build.

## Implementation and verification plan

1. GaussianScalarMoments.lean exports gm8C8, gm8_standard_integrable,
   gm8_standard_nonneg, gm8_scalar_integrable_bound with the statement above.
2. GaussianJetMoments.lean proves the ten-term power bound, radius integrability
   and integral bound from actual coordinate HasLaw assumptions, and uniform DM2
   composition. Root alone updates the root module, manifest and source scope.
3. Reuse pinned Lean4.34.1/mathlib d13f23b723b8a846827a245b89c10fc7d3f11612
   and the retained gate/axiom allowlist/five controls. The new modules change
   the root's dependency closure and target inventory, warranting one final
   corresponding gate execution; old proofs are not rerun as separate campaigns.
   Preserve earlier evidence. Test new false hypotheses/constant omissions.
4. Publish exact source/receipt/diff and request different-family statement and
   proof review. OpenAI coauthors/technical readers are not qualifying reviewers.

## Still to discharge for the actual field and parent

The exact six-pin conditional measure, derivative-coordinate map, regression-law
identification and uniform mean/covariance bounds for the literal field are not
yet constructed in this Lean packet. The recovered primary provides their exact
analytic definitions for subsequent work. Existing unconditional smooth-source
point-evaluation Gaussian laws do not automatically identify conditioned derivative
jets. The current theorem discharges the moment step once those model interfaces
are supplied, not that remaining identification. Endpoint-object identification,
normalizer lower bound, actual typed Palm identification, event-tail/good-event
coverage, GT5, P0.2 and lifetime/persistence parents remain in the research scope.

## Source-driven generic and exact-endpoint extension, frozen before its code

The finite-sum argument will be generalized to Fin n: gm8Radius(j)=1+sum|j_i|,
gm8FiniteM8(n,B,V)=(n+1)^7*(1+n*128*(B^8+V^4*C8)).
gm8_finite_integrable_bound has the same actual marginal-law hypotheses above,
with Fin n replacing Fin9, and derives integrability plus this bound. Existing
fixed9 names remain specializations with their displayed exact M8.

Reason: GP-DER-043 calls the LM002 matrices QUARTIC endpoint Hessians and requires
an exact-field transfer; raw midpoint derivatives do not determine arbitrary
literal endpoint Hessians. The polynomial perturbation x^5(x²-r²/4)^2 preserves
pins and every midpoint derivative through4, but changes endpoint xx by ±r^7/16.
This blocks that naive identification, not the valid frozen LM002 algebra.

The correct actual-field moment route already appears in GP-DER-047 §13, primary
main commit7caac254cbba5f513b2dc0afb56b78a598bc0c93, blob
2ce4e18a0e4ee582e41d640144f1cacac5c855c7 (public sources-03 catalog). It uses
V=(fxx(M)/r,fxy(M)/r,fyy(M),fxx(S)/r,fxy(S)/r,fyy(S)), a distinct six-vector.
The new EndpointGaussianMoments.lean takes six real coordinates in THIS order,
builds HM=[[r*v0,r*v1],[r*v1,v2]], HS=[[r*v3,r*v4],[r*v4,v5]], and the literal
quadratic-form maximum/saddle typed determinant product. For0<r<=1, prove
W_endpoint²<=16*r^4*gm8Radius(v)^8, weight measurability, and from actual Gaussian
coordinate laws with common B,V derive integrability and integral W_endpoint²
<=16*gm8FiniteM8(6,B,V)*r^4. No polynomial endpoint identity is assumed.

Only the new endpoint coauthor file is delegated; root owns the generic API and
manifest. Physical smooth-field derivative Gaussianity, canonical regression and
uniform finite-r mean/variance estimates must still be connected, using the
actual6endpoint vector rather than substituting the raw9midpoint vector. This
is an author-side source clarification pending different-family review; historical
source/proof/review bytes and statuses remain unchanged.
