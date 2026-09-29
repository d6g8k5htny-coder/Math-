# Addendum: an extra nearby critical point forces a soft transverse jet

Object: OA-PLANAR-CUBIC-CLUSTER-20260929-D1.
Author: OpenAI / GPT-6 Astra Pro, 29 September 2026.
Disposition: author-side deterministic proof candidate; nonauthor review OPEN.
Scientific effect NONE. This addendum leaves PROOF.md unchanged. It discharges the deterministic part of the follow-up proposed in Math-#157 comment5900564419; the weighted Gaussian derivative-tail estimate in that comment is NOT established here.

## Statement

Fix R>=1, k>0 and K>0. Let f be C^4 on a neighborhood of the closed square [-Rr,Rr]^2, with every coordinate derivative of orders one through four bounded in absolute value by K. Retain exactly the two pins

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Assume r>0 and

    r K <= k/(4R),
    A=f_zz(0,0),       L_R=8RK+56RK^2/k.                   (D1)

**Lemma D.** If A < -L_R r, the square contains no critical point other than M,S. Consequently, if H_f(M) is negative definite and ANY additional critical point lies in that square, then

    -L_R <= A/r < K/2,
    |f_xxz(0)|, |f_xzz(0)|, |f_zzz(0)| <= K.               (D2)

The conclusion concerns all additional critical points, not only window points. No global Morse assumption or Gaussian probability estimate is used.

## Proof

Suppose lambda=-A>L_R r. The derivative bound gives, throughout the square,

    f_zz(x,z) <= -lambda+2RK r <= -lambda/2.                (D3)

For g(x)=f_z(x,0), the two gradient pins give g(-r/2)=g(r/2)=0 and |g''|<=K. The two-node interpolation remainder, also for x outside the pin interval but within [-Rr,Rr], yields

    |g(x)| <= (K/2)|x-r/2||x+r/2| <= KR^2 r^2.             (D4)

This follows directly by subtracting the quadratic with the same value at x and applying Rolle's theorem twice, with repeated nodes handled by continuity. Rolle applied once to the two pin zeros also supplies xi in (-r/2,r/2) with g'(xi)=0, so

    |f_xz(x,0)| <= K(R+1/2)r <= (3/2)RK r.                 (D5)

Put rho=4R^2 K r^2/lambda. Since lambda>8RK r, rho<Rr/2. Equations (D3)-(D4) imply f_z(x,-rho)>0 and f_z(x,rho)<0 for every x in [-Rr,Rr]. Strict decrease in z therefore gives a unique zero z=zeta(x), with |zeta(x)|<rho. The implicit-function theorem makes zeta C^3. Every critical point anywhere in the square must lie on this graph; uniqueness holds in the full vertical segment by (D3). At both pins zeta=0.

Along the graph write B=f_zz<0, C=f_xz and t=C/B. From (D5), |f_xz(x,zeta)| <= 2RK r, so

    |t| <= 4RK r/lambda < 1/2.                             (D6)

Let psi(x)=f(x,zeta(x)). Since f_z=0 and zeta'=-C/B,

    psi'=f_x,
    psi''=f_xx-C^2/B,
    psi'''=f_xxx-3f_xxz t+3f_xzz t^2-f_zzz t^3.           (D7)

These identities are differentiated on the graph, with all field derivatives evaluated at (x,zeta(x)); no mixed term is dropped. For |t|<=1,

    |psi'''-f_xxx| <= K(3|t|+3|t|^2+|t|^3)
                    <= 7K|t| <= 28RK^2 r/lambda < k/2.   (D8)

The one-dimensional Hermite interpolant to f(x,0) at the two pins is

    H(x)=b+kr^3[2(x/r)^3-3(x/r)/2-1/2].

Its values and first derivatives at both pins agree exactly with f. Generalized Rolle, or three successive applications counting the endpoint double zeros of f-H, gives a point eta in (-r/2,r/2) with f_xxx(eta,0)=H'''=12k. The C^4 bound, |x|<=Rr and |zeta|<Rr/2 yield

    |f_xxx(x,zeta)-12k| <= K(|x-eta|+|zeta|)
                          <= 2RK r <= k/2.               (D9)

Combining (D8)-(D9), psi'''>=11k>0. Hence psi' is strictly convex on [-Rr,Rr]. It already has zeros at -r/2 and r/2. A strictly convex function cannot have three distinct zeros: the middle would lie strictly below the chord joining the outer two. Thus psi' has only those two zeros, and the graph contains only M,S as critical points. This proves the first assertion.

For the consequence, the existence of an additional critical point implies A>=-L_R r by contraposition. Negative definiteness at M gives f_zz(M)<0, while |f_zz(0)-f_zz(M)|<=Kr/2, so A/r<K/2. The remaining coordinates in (D2) are bounded directly by the derivative norm. QED.

## What this gives the Gaussian continuation, and what it does not

For fixed R,K,k and sufficiently small r, the extra-point event on ||f||_{C^4}<=K is contained in the fixed compact jet rectangle

    Theta_r=(f_zz/r,f_xxz,f_xzz,f_zzz)
       in [-L_R,K/2] times [-K,K]^3.                       (D10)

This rectangle need not be strictly inside the typed CUBIC domain at finite r. Approaching that domain's boundary still needs control when applying PROOF.md's compact-sector theorem; finite-r field types cannot be silently replaced by strict limiting cubic types.

In particular (D10) does NOT itself bound the scaled Gaussian mass outside the rectangle. A sufficient probabilistic input would be

    E_{Q_r^W}[N_r(1+||f||_{C^4})^p] <= C_p r^3             (D11)

for fixed p, using the original full tilt/normalizer. If separately proved, (D2) and (D11) imply, with N_{r,R} the local count and the rectangle of (D10),

    limsup_{r->0} r^-3 E[N_{r,R}; Theta_r outside rectangle]
        <= C_p(1+K)^(-p).                                 (D12)

The pointwise containment is applied only when N_{r,R}>0; otherwise the counted integrand is zero. The global count N_r bounds the local count. This explains exactly how the proposed derivative-weighted insertion would supply a missing rare-intensity tail, without dividing an unconditioned Gaussian tail by r^3.

(D11) is an OPEN input, not a consequence asserted from the new count-exponential candidate #157. Further spatial and mixed local/remote estimates remain separate. Neither (D10) nor the conditional implication (D12) establishes uniqueness of the global cluster law.

## Finite checks

The companion test_deep_exclusion.py checks the constants of (D3)-(D9) over an exact rational grid, the graph sign bracket, and (D7) against explicitly reducible polynomial potentials. These are finite checks of the displayed algebra, not a formal proof of the implicit-function or convexity argument. Review requested: all of Lemma D and the conditional-only interpretation of (D11)-(D12).
