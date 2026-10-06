## A3.3 S2 finding — the advertised K5 negative-branch witness violates the ordered-eigenvalue domain

Dylan Roy — delegated AI mathematical review; actual performer OpenAI / GPT-6 Astra Pro, session `github-rules-and-closure-round2-20261005`, pickup5999558095. This is a concrete interim finding, not the final S2 verdict and not a counterexample to W3.

**A33-S2-C1 (control-scope AMEND).** Note5998500022 §2 requires `lambda1 <= lambda2`, with `lambda1 = r*lambda_tilde/k`. In controls5998502385 `k5`, the advertised negative-branch example sets `k=1`, `r=1/10000`, `lambda_tilde=1`, `G=100` and `lambda2=-G^2*r^2/144`. Thus **lambda1=1/10000 > lambda2=-1/1440000**. Every nonpositive-lambda2 grid point likewise has positive lambda1. These are valid algebraic-frame controls but not examples in the ordered #243/A3.3 domain; sorting the frame changes which direction and parameter is called lambda2. They cannot establish that K5 exercised the theorem's negative-largest-transverse-eigenvalue branch. I am not rejecting the pathwise inequality: its proof appears to avoid ordering as well as inverse eigenvalues.

**Minimal repair:** label the old off-domain tests honestly and add a correctly ordered, nonzero actual-weight witness, or explicitly state that the ordered negative branch has not been exercised. Keep the old output/history; do not silently relabel it.

**Concrete replacement supplied for the author's consideration.** On the local polynomial chart, take

`f(x,y,z) = b - k*r^3/2 + 2*k*x^3 - (3/2)*k*r^2*x + (1/2)*(2*r^2-12*x^2)*y^2 + (1/2)*(r^2-8*x^2)*z^2`.

At the two pins, heights are b and b-k*r^3, both gradients vanish, and
`H_M = diag(-6*k*r,-r^2,-r^2)`, `H_S = diag(6*k*r,-r^2,-r^2)`.
At the midpoint the **strictly ordered** transverse eigenvalues of -A are `lambda1=-2*r^2 < lambda2=-r^2 < 0`; gamma=B=Y=0 and `lambda_tilde=-2*k*r`. Consequently **W_r/r^4=36*k^2*r^6>0** while the model weight is zero. This really exercises an ordered negative-lambda2 case.

I independently differentiated that polynomial and checked all identities with exact Fraction arithmetic for12 cases, r in {1/100,1/1000,1/10000}, k in {1/2,1,3/2,2}; normal and -O runs agree. The same finite-jet proxy gives N_f=25 and satisfies the author's stronger test form with C0=2 in those cases. This is a local polynomial/finite-control calculation, **not a global torus C^5 norm certificate or a numerical theorem constant**. My separate diagnostic SHA256 is `3e5f814993221081ff5b1cb365255a5acbf1c44f4694851fe03da0c7246211fb`; it is not the author's a33_exact.py, which I have not claimed to replay in full.

S1/S3 reviewers: preserve your scopes; a full replay can still pass while this domain issue remains. If the replacement control is incorporated, it is an OpenAI contribution and needs another reader's delta validation, not my self-approval. The analytic W3/TE reconstruction is still being finalized here. Scientific effect NONE; no source or status mutation.