# Cap I4, d=3: an eighth-moment depth bound by a residual split

**Object:** CAP-I4-D3-M8-20261005-v1. **Author:** OpenAI / GPT-6 Astra Pro, `cap-i4-d3-followthrough-20261005`, for Dylan Roy. **Disposition:** author-side ordinary-mathematical proposal, not independently accepted or implemented in Lean. Scientific/status effect NONE; organizational-independence credit 0. Pickup main#229/6007108765. This is separate from frozen Math-#313 and does not change that packet or its review.

## 1. What is new, and exactly what is assumed

The ninth-moment sufficient envelope in Math-#313 is correct within its scope and explicitly does not assert optimality. Here an additional split at **r J^2 = 1** gives a sufficient **eighth** residual moment for the depth numerator. Both sides of the split are paid for under the original law. This does not claim a smaller numerical constant, a finite-radius certificate, or a new Gaussian-field construction.

P is `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, at Math- source cut `f4c33a98a982d50aa490e49ce9327c755682527c`; consume (3.5), (4.2)-(4.3), (5.5), (6.2), section 7. Its section 5 congruence must be read with erratum blob `213594d6ca6a86fb938110f4d166d9ce275a02d0`. P is the imported source, not newly certified by this note.

The explicit d3 spectral calculation is in Math-#313, source head `8e90773b28ecce66ed30458d58aef1b6cb83666a`, `reviews/cap_i4_d3_spectral_adapter_20261005/PROOF.md`, blob `c30e3f5ff600b058a30087ff794c7cf304e4aafc`. This note uses its spectral interface (not its ninth-moment conclusion): for the increasingly ordered eigenvalues 0<lambda<L of B>0, the positive-cone spectral sublaw is dominated by

    C_s (L-lambda) exp[-c(lambda^2+L^2)] d_lambda d_L,
    0<lambda<L, c>0.                                      (S)

For P's ordinary matrix-entry density bound C0 exp(-c||B||_F^2), C_s=pi C0. The factor follows from t=(a+d)/2, x=(a-d)/2, y=b: entry volume is 2 dt dx dy; polar coordinates contribute rho; t=(lambda+L)/2,rho=(L-lambda)/2 contributes 1/2. Thus entry volume is (L-lambda)/2 d_lambda d_L d_theta with -pi<theta<pi. Frobenius-orthonormal volume differs by sqrt(2). No eigenvector selection or invariance of the ACTUAL matrix law is assumed. Absolute continuity makes the repeated-eigenvalue line null, without deleting any of its neighborhoods.

Work under a probability law Q. J>=1 is measurable and independent of the WHOLE B under Q, with E[J^8]<=M8<infinity. Let 0<r<=1, k>=k_floor>0 and K>0. W is nonnegative, measurable and integrable, and vanishes outside positive typed support. On W>0 assume B>0, h>=0, h<=K(J+L), and the actual source envelope

    W <= (r^2 h^2/4) lambda(lambda+3rh/2) L(L+rh).          (W)

Define the measurable depth event A={lambda<=(4/(3k))r h^2}. Statements involving lambda off W>0 may use any measurable extension. Set

    U=J+L, D=4K^2/(3k_floor), E=3K/2,
    Bstar=D^3/3+E D^2/2, a=K^2/4.

Then W>0 and A imply lambda<=D r U^2. Constants must be uniform over the intended parameter family. For P that family has fixed d=3,L, compact birth and positive gap marks, all frames, and sufficiently small r. The residual field's internal correlations, and dependence of h/W on residuals and eigenvectors, remain allowed. We never condition independence on the typed event.

## 2. Gaussian notation

For an integer j>=0 put

    I_j(c) = integral_0^infinity L^j exp(-cL^2)dL
           = Gamma((j+1)/2)/(2 c^((j+1)/2)).

These are finite. In particular I2=sqrt(pi)/(4c^(3/2)), I3=1/(2c^2), I10=945sqrt(pi)/(64c^(11/2)), I11=60/c^6. Define, for q=2,3,4,

    H_q(c) = (1/2) sum_{j=0}^q binom(q,j) I_(8-q+j)(c).   (H)

The proof below derives the factor 1/2 by integrating the original spectral gap. It is not an additional angular multiplicity factor.

## 3. Low residual: keep rJ small before integrating lambda

Let B_lo={rJ^2<=1}; its complement is B_hi={rJ^2>1}. These include the equality boundary once, and exhaust the original probability space. On B_lo, J>=1 implies rJ<=1, whence

    rU <= 1+L,
    L(L+rh) <= L H(L), H(L)=K+(1+K)L.

The crucial point is that H no longer contains J. From (W),

    W 1_(A intersect B_lo)
      <= a r^2 U^2 lambda(lambda+ErU) L H(L)
            1_{0<lambda<=L, lambda<=DrU^2, B_lo}.

This pointwise nonnegative majorant is a function of J and the eigenvalues. Apply original-law independence and (S). On the ORIGINAL chamber first use L-lambda<=L and drop exp(-c lambda^2)<=1; only then extend lambda from [0,min(L,DrU^2)] to [0,DrU^2]. J and L are fixed during this integration because the transverse dimension is two. The exact primitive is

    integral_0^(DrU^2) lambda(lambda+ErU)d_lambda
       = r^3[(D^3/3)U^6+(ED^2/2)U^5].

After U^7<=U^8 and dropping the residual restriction from this now-positive upper integral,

    E[W;A intersect B_lo]
      <= C_s a Bstar r^5 E_J integral_0^infinity
                           L^2 H(L) (J+L)^8 exp(-cL^2)dL
      <= C_lo r^5,                                      (L)

where

    C_lo = 128 C_s a Bstar *
      { M8[K I2(c)+(1+K)I3(c)] + K I10(c)+(1+K)I11(c) }.

The last step is (J+L)^8<=128(J^8+L^8). Tonelli is used before the finite displayed bound supplies integrability. No positive lower bound on L is introduced. In particular the small-L and corank-two neighborhoods remain in the integral. The signed factor L-lambda is NOT carried to the enlarged interval where it could be negative.

## 4. High residual: use its eighth moment under the original law

On all typed support, expanding the two shifted soft factors in (W), using h<=KU, and then lambda<=L gives

    W <= a [ r^2 U^2 L^4 + (5K/2)r^3 U^3 L^3
                              + (3K^2/2)r^4 U^4 L^2 ].  (T)

For example, the middle factor is lambda L(lambda+3L/2)<=5L^3/2; omitting that term is invalid. Since J>=1, U^q<=[J(1+L)]^q. For q in {2,3,4} on B_hi,

    J^q <= r^((8-q)/2) J^8.

Therefore E[J^q;B_hi]<=M8 r^((8-q)/2). This is direct pointwise moment truncation followed by integration, NOT a Cauchy-Schwarz probability transfer.

To integrate the matrix factors retain their original ordered interval and use

    integral_0^L (L-lambda) exp(-c lambda^2)d_lambda <= L^2/2.

Consequently the matrix integral for the q-th term is bounded by C_s H_q(c), since its remaining factor is L^(6-q)(1+L)^q exp(-cL^2). Original-law J/B independence is used at this point, not under a tilted or typed conditional law. From (T),

    E[W;B_hi] <= C_s a M8 *
      [ H2(c) r^5 + (5K/2)H3(c) r^(11/2)
                         + (3K^2/2)H4(c) r^6 ]
      <= C_hi r^5,                                     (T8)

    C_hi = C_s a M8[H2(c)+(5K/2)H3(c)+(3K^2/2)H4(c)].

The fractional-power term is preserved before using r<=1. We bounded the full high-sector weight, so this also bounds its intersection with A. Both branches have now been charged.

## 5. Conclusion and the unchanged fourth-derivative obligation

Combining (L) and (T8) proves, under the explicit abstract hypotheses,

    E_Q[W;A] <= (C_lo+C_hi) r^5.                         (M8)

With the actual FULL normalizer Z=E_Q W>=cZ r^2, cZ>0, exactly one division gives

    Q^W(A) <= (C_lo+C_hi)/cZ * r^3.

For E4={3k/10<rM4}, keep the separate actual joint premise
E_Q[(W/r^2)M4^4]<=M4joint. It yields

    Q^W(E4) <= M4joint/[cZ(3k_floor/10)^4] r^4.

The measurable geometric cap implication, required only Q-a.e. on W>0, then yields the sum of these two same-law bounds for cap failure. This note does not itself construct that geometric event in Lean, identify an actual Gaussian/Palm law there, or promote a parent theorem.

**Related but separate:** the author's main#229/6007067368 corollary independently derives an explicit weighted E4 moment from E[J^8] when the ADDITIONAL source bound M4<=K4(J+L) is retained. That earlier corollary is credited, is not required for (M8), and is not silently treated as an accepted input here. Its combination with (M8) would give both cap tails from the same eighth residual moment after the additional M4 bound and its review are supplied. No claim about an unrelated M4 follows merely from a moment of J.

## 6. A fixed-law countermodel to using all lower moments alone

This tests only the ABSTRACT density/weight-domination class. It is not claimed to be the residual of the source Gaussian field or its actual Hessian determinant weight.

Let B have the full Gaussian entry density

    p(B)=(sqrt(2)/pi^(3/2)) exp(-||B||_F^2)

on symmetric 2x2 matrices. It is normalized in da db dd. Independently let J=2^n with probability

    p_n=(255/256)2^(-8n), n=0,1,... .

Thus J>=1, E[J^p]=(255/256)/(1-2^(p-8)) is finite for EVERY real p<8, while E[J^8]=infinity. In particular E[J^2]=85/84. Set h=J, k=4/3, K=1, and

    W_r=(r^2 J^2/4) lambda^2 L^2 1_{B>0}.

This weight is measurable and integrable and satisfies (W) because the shifted factors dominate lambda and L. Also h<=J+L on W>0. Its full normalizer is Z_r=z0 r^2 with

    z0=(E[J^2]/4) E[(det B)^2;B>0] in (0,infinity).

The depth event is lambda<=rJ^2. On 1<=L<=2, 0<lambda<=1/2 the exact spectral density is bounded below by

    gstar=(sqrt(2/pi)/2) exp(-17/4)>0.

Choose r_N=2^(-(2N+1)). For every n<=N, r_N J^2<=1/2. Restrict the numerator to these n and to the displayed spectral rectangle; using L^2>=1 and integrating lambda^2 to r_N J^2 gives

    E[W_(r_N);depth]
      >= (gstar/12) r_N^5 sum_{n=0}^N p_n 2^(8n)
       = (gstar/12)(255/256)(N+1) r_N^5.

Hence

    Q^W_(r_N)(depth)/r_N^3
      >= [gstar/(12z0)](255/256)(N+1) -> infinity.

There is no uniform cubic bound despite all strictly sub-eighth moments being finite. This shows why a hypothesis asserting only moments of order below eight cannot generally replace the eighth-moment assumption within this broad comparison class. It does NOT say every individual model with infinite eighth moment fails, nor that the actual source field needs a heavy-tail analysis: P already supplies all finite residual moments. The new argument is a moment-sufficiency refinement, not an assertion of new field physics or literature priority.

## 7. Formal boundary and verification

No new Lean file is supplied. Besides the concrete spectral map/product-law/model interfaces already open, the new formal steps are: a.e. weighted partition by rJ^2<=1; the low-sector hard-factor inequality; nonnegative interval extension followed by a U^8 envelope; original-law truncated moments for q=2,3,4; and the exact r^5,r^(11/2),r^6 ledger. The original compiled Cap consumer's U^(2m+6) envelope does not automatically prove this new theorem. A proof must provide the new nonnegative integration arguments, not assume (M8) as a premise and call that an adapter.

Run in this directory, with standard-library Python only:

    python -B -S test_bounds.py
    python -B -O -S test_bounds.py
    python -B -S test_mutations.py
    python -B -O -S test_mutations.py

Actual development evidence: the 12 primary methods were first run without bounds.py, producing 16 missing-helper assertion reports and no import errors; after implementation all 12 passed in each mode. The seven wrong-formula copies each exit 1 with their exact expected failed-test sets and no test errors in both modes. The mutation runner is one unittest method with seven labeled subcases. Output pairs are byte-identical. Checks cover partition/equality boundaries, low/hard factor, exact primitive and powers, all three high-sector terms, Gaussian coefficient recurrences, spectral-gap half factor, dyadic countermodel, full normalization and invalid domains. These finite rational checks do not prove continuous change of variables, Gaussian regression, or infinite-series convergence; the ordinary arguments above supply the claimed analytic reasoning pending nonauthor review.

No full repository checkout or local Lean executable was available; direct GitHub DNS in the working container failed. The new packet changes no prior proof, formal manifest, workflow or acceptance record. Consensus was attempted and returned its monthly quota error. Official mathlib polar-coordinate documentation was consulted only for background; the source-pinned formal interface remains the one recorded by #313. No external novelty claim is made.
