# Weighted absolute Gaussian series: moments and exponential upper tails

Frozen before code,25October2026. OpenAI/Codex root and
/root/normalizer_palm_research. Scientific effect NONE.

Sole new GaussianWeightedMajorants.lean. For any probability P, countable index
I, measurable real U_i with HasLaw U_i N(0,1), and nonnegative summable real
weights w_i, define Gamma=sum' i,w_i*abs(U_i), W=sum' i,w_i. No independence
of U_i is assumed. Derive a.e. absolute series convergence, measurability/
integrability, and for each positive NATURAL n the sharp bound
integral Gamma^n <= W^n * integral abs(z)^n under N(0,1), with integrability
and standard reference integrability derived. Include zero weights; n=0 may
be a separate probability identity. Do not assert this sharp constant for
real0<p<1, where it is generally false.

Also prove actual exponential integrability and
integral exp(t*Gamma) <= 2*exp(t^2*W^2/2) for t>=0 (all real t if convenient).
This is a separate exponential theorem, not a consequence inferred from
finiteness of all moments. One direct route: normalize finite weights by W,
add the missing mass at zero, apply finite Jensen to exp, use
exp(s*abs(z))<=exp(s*z)+exp(-s*z) and the exact standard Gaussian MGF, then
nonnegative Fatou with proved a.e. series convergence. W=0 is the zero series.
For W>0,R>=0 derive P.real{Gamma>=R}<=2*exp(-R^2/(2*W^2)) by exponential
Markov with t=R/W^2. These are upper-tail bounds, not a zero-mean assertion
about the nonnegative Gamma variable. Never assume desired convergence,
moments, exponential integrability or concentration as a premise.

The application is the original standard Gaussian NOISE under smoothLaw,
before posteriorSample pushforward. Posterior coordinates are neither
standard nor independent; their mean/correction must be handled explicitly.
Existing source/API notes weighted_gaussian_majorant_api_notes.md and the
source Gaussian moment/MGF/Lp APIs may be reused. Narrow imports only.

Check only this new module with genuine correlated/zero-weight/nonunit-weight
controls and wrong-range/concentration counterexamples where useful. Preserve
failures and actual commands/exits. Root owns integration/different-family
review; no old baseline verification is repeated.
