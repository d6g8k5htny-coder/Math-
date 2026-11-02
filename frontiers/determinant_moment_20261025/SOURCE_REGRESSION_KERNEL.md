# Canonical Gaussian regression kernel: preimplementation source contract

OpenAI/Codex root and coauthor /root/regression_kernel. Scientific review must
use another model family. New research remains within the owner's original goal.

Source: GP-DER-044-v1.0 Exact-torus Gaussian regularity via confluent divided
differences, main commit7caac254cbba5f513b2dc0afb56b78a598bc0c93, Git blob
34e38cb003a3160c154c07d293d44690a6c8b718. Exact public path is catalogued by
main/docs/public-math/sources-03.md and SOURCE_GAUSSIAN_MOMENTS.md. Section4
uses joint Gaussian observations/targets, the independent Gaussian regression
residual, mean C G^-1 y and Schur covariance S-C G^-1 C^T to define the law
at each prescribed six-pin value. These are probability-zero conditioning events.

Generic condDistrib versions are unique only almost everywhere; substituting
an arbitrary version at the exact pin is not a valid source identification.
This target therefore constructs an explicit kernel, not just existential RCD.

Frozen target: for finite real-vector observations X and residual R on a common
probability space, joint Gaussianity and zero cross-covariance imply independence.
Given a continuous affine reconstruction F(x,r)=r+mY+B(x-mX), define
regressionKernel(x)=Law(R).map (fun r=>F(x,r)) at EVERY x. Prove the kernel is
Markov/measurable, its pointwise application equals that literal pushforward,
and HasCondDistrib (fun omega=>F(X omega,R omega)) X regressionKernel P.
No HasCondDistrib, target probability, residual independence or Palm conclusion
may be assumed in the final Gaussian theorem; independence must follow from
joint Gaussianity and zero covariance. A generic independent-residual helper is
permitted as a proved auxiliary. All finite dimensions, including degenerate
residual Gaussian laws, are retained; no residual covariance inverse is used.

This is the source's canonical conditional-law construction component. Concrete
application still requires jointly Gaussian derivative observations/targets,
positive pin covariance, regression/Schur block identities, correct prescribed
vector and physical jet map, and connection to the literal smooth field. Those
joins are not implied by generic conditioning, this kernel theorem or the already
landed unconditional evaluation-Gaussian constructor. The typed Palm weight and
parent geometric event identification remain separate research obligations.

Implementation: sole new GaussianRegressionKernel.lean, narrow pinned Mathlib
imports; retain source/failed probes; no oldproof/test campaigns. Root alone
updates manifest/root after stabilization. Existing successful verification is
reused where applicable; final gate tests the changed closure and new targets.

## Direct observed/target regression strengthening, frozen before code

The implementation may additionally derive the residual hypotheses from a
jointly Gaussian pair(X,Y). Let B be continuous linear and satisfy the coordinate
normal equations Cov(X_i,Y_j)=sum_l B(e_l)_j*Cov(X_i,X_l). Define
R=Y-mY-B(X-mX) using these ACTUAL random vectors. Prove joint Gaussianity of
(X,R), zero cross-covariance and hence HasCondDistrib Y X for the canonical
residual kernel. Do not assume residual joint Gaussianity, residual independence,
zero residual covariance or a conditional-law conclusion in this strengthened
theorem. Normal equations may be an explicit algebraic premise; in the concrete
source they come from B=C G^-1 and pin-covariance invertibility. Identifying those
blocks and literal field derivatives remains an application obligation.
