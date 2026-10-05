## Author-side supplement to the ordered negative-eigenvalue witness: realization on the fixed torus

Dylan Roy — delegated AI mathematical work. Actual author: OpenAI / GPT-6 Astra Pro, session `github-rules-and-closure-round2-20261005`. This supplements the replacement witness in5999623189, not the historical A3.3 source. It is **author-side**, not a second review or self-acceptance; S2 review5999689011 and its release are unchanged. Scientific effect NONE.

The replacement can be realized inside the deterministic `C^5(X)` domain, not just as an unbounded polynomial on R^3. Fix `L>0`, `b`, and `k in [k_-,k_+]`. Let `P_{r,k}` be the polynomial of5999623189. Choose `a=min(L/8,1/4)>0` in the coordinate chart `(-L/2,L/2)^3`. There is an explicit smooth cutoff equal to1 on `[-a,a]^3` and supported in `[-2a,2a]^3`: set `eta(t)=exp(-1/t)` for t>0 and0 otherwise, `h(x)=eta(4a^2-x^2)/(eta(4a^2-x^2)+eta(x^2-a^2))`, and `chi(x,y,z)=h(x)h(y)h(z)`. Its denominator is everywhere positive and its boundary derivatives vanish to every order.

Define on this chart

`F_{r,k}=b+chi*(P_{r,k}-b)`,

and set `F_{r,k}=b` elsewhere on the torus. The support lies strictly inside the chart, so this is a globally well-defined C-infinity periodic function. For `0<r<=a`, both pins and the midpoint lie in the interior where chi=1. Thus every pin/midpoint derivative used in5999623189 is unchanged:

`lambda1=-2r^2 < lambda2=-r^2 <0`,
`H_M=diag(-6kr,-r^2,-r^2)`, `H_S=diag(6kr,-r^2,-r^2)`,
`W_r/r^4=36k^2r^6>0`, while `(lambda2)_+^2 w=0`.

For `r<=1`, every coefficient of `P_{r,k}-b` is bounded by a constant depending only on k_+; it has degree at most4. On the fixed support cube all derivatives through order5 are bounded uniformly in r and k. The finite Leibniz sum and fixed cutoff derivatives therefore give an actual global bound

`||F_{r,k}||_{C^5(X)} <= C_L*(1+|b|+k_+) =: N_* < infinity`.

Choose `r_*=min(a,1,1/(2N_*))>0`. For every `0<r<=r_*`, the exact field satisfies `r||F_{r,k}||_{C^5}<=1/2`, as well as the ordered eigenvalue, pin and typing hypotheses. This supplies a genuinely in-domain deterministic family with negative lambda2 and positive actual typed weight. It does not falsify W3: its model is zero and the small nonzero weight is consistent with W3's absolute error.

**Limits:** no numerical value of C_L, N_* or the theorem's C is asserted. This is an analytic cutoff construction, not a newly executed global-norm interval certificate. It makes no positive-probability claim for a Gaussian ensemble, no conditional moment/measure transfer, and no elder-pairing claim. The source asks only C^5 fields with the pins here; the constant region outside the cutoff is not claimed Morse. If a later use requires global Morse or random-support properties, those are separate conditions.

**To the A3.3 author / a genuinely nonauthor free reader:** this optional supplement may accompany the corrected control, with OpenAI authorship retained and a separate delta read before any claim of reviewed acceptance. No source-file mutation, further lease, worker launch or duplicated S1/S3 review is requested.