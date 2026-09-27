# A uniform endpoint-Hessian covariance floor under six linear BF pins

Object: OA-BF-SIX-PIN-HESSIAN-20260926-v1. Author: OpenAI / ChatGPT.
Disposition: AUTHOR_DERIVATION / REVIEW_REQUIRED. Scientific effect: NONE.
This separately named proof preserves the earlier scalar package unchanged.
It does not alter any existing scientific verdict or claim register.

## 1. Exact law and conclusion

Let f be the centered Gaussian field on R^2 with covariance
K(x,y)=exp(-|x-y|^2/2). Coordinates are (t,s), M=(0,0), S=(r,0), r>0.
Let P=(f(M),f_t(M),f_s(M),f(S),f_t(S),f_s(S)). All conditioning below is the
Gaussian regular conditional law for these six LINEAR observations.
The prescribed values can be arbitrary; conditional covariances do not depend
on their values. No determinant weighting or nonlinear type selection is made.

For V_r=(f_tt(M)/r^2, f_ts(M)/r, f_ss(M)), simultaneously for all real
0<r<=1/40,

    Cov(V_r | P) = diag(a(r), b(r), 2),
    1/7 <= a(r) <= 1/5,
    1599/3200 <= b(r) <= 1/2.

In particular, in the Euclidean coordinate norm,

    (1/7) I_3 <= Cov(V_r | P) <= 2 I_3.

This is the complete Hessian-coordinate covariance AT ONE ENDPOINT, not a
covariance floor for a two-endpoint block or a block including an extra witness.
The unscaled Hessian covariance has entries (r^4 a(r), r^2 b(r), 2) and does
not have a radius-independent positive floor.

## 2. Exact independence, not diagonal-variance inference

Write c=exp(-r^2/2). Split P into longitudinal observations
V=(f(M),f_t(M),f(S),f_t(S)) and transverse observations U=(f_s(M),f_s(S)).
Odd total transverse derivative order makes all cross-covariances between
these groups vanish. The jointly Gaussian groups are independent.

The variable Z=f_ss(M)+f(M) is independent of P, f_tt(M), and f_ts(M).
Indeed, for every derivative involving only t at a point of the t-axis,
Cov(f_ss(M),derivative)=-Cov(f(M),derivative), by separability of K.
The remaining cross-covariances vanish by transverse parity. At M,
Var(f_ss)=3, Cov(f_ss,f)=-1, Var(f)=1, so Var(Z)=2.
Once f(M) is pinned, the residual of f_ss(M) is exactly Z.

The pair (f_ts(M),U) is independent of (f_tt(M),V). Together with the preceding
Z independence, this proves conditional independence of the three Hessian
residuals. Thus the off-diagonal entries really vanish; positive marginal
variances alone would not suffice to infer the matrix floor.

## 3. Mixed component

Var(f_ts(M))=1, Cov(f_ts(M),U)=(0,rc), Cov(U)=[[1,c],[c,1]].
The determinant 1-c^2 is positive for r>0. Gaussian regression gives

    b(r) = [1-r^2/(exp(r^2)-1)]/r^2.

For x=r^2 in (0,1), exp(x)-1-x >= x^2/2 and
exp(x)-1 <= x/(1-x), hence b(r)>=(1-x)/2.
The absolutely convergent series

    x(exp(x)-1)/2 - (exp(x)-1-x)
      = sum_(n>=3) (n-2)x^n/(2 n!) >= 0

gives b(r)<=1/2. Therefore b(r)>=1599/3200 on the stated radius interval.
This repeats the short argument so the present proof does not assume that the
unreviewed scalar PR has acquired acceptance.

## 4. Axial regression and its singular orders

In the order V above, the covariance G and cross-vector u are

    G = [[1,0,c,-rc],
         [0,1,rc,(1-r^2)c],
         [c,rc,1,0],
         [-rc,(1-r^2)c,0,1]],
    u = (-1,0,(r^2-1)c,r(3-r^2)c).

Var(f_tt(M))=3. The leading principal minors of G are 1, 1,
1-(1+r^2)c^2, and

    det G = 1-(2+r^4)c^2+c^4.

The third is positive since exp(x)>1+x. Put E=exp(x), and define

    D(x) = (E-1)^2-x^2 E,
    A(x) = 2E^2-4E+2-4xE+4x+x^2E+x^2-x^3E.

Then det G=exp(-2x)D(x). The positivity of D is proved below, so Sylvester's
criterion makes G invertible and positive definite for r>0.
The finite polynomial adjugate calculation gives

    3 det G - u adj(G) u^T
      = 2+(-r^6+r^4-4r^2-4)c^2+(r^4+4r^2+2)c^4
      = exp(-2x) A(x).

Consequently

    Var(f_tt(M) | P)=A(x)/D(x),
    a(r)=A(x)/(x^2 D(x)).

The executable checks the determinant, adjugate identity and Schur numerator
as integer polynomials in formal variables r,c, not at sampled radii.

## 5. All-order signs and uniform remainder bounds

Direct expansion of the entire exponential series yields

    D(x)=sum_(n>=4) d_n x^n/n!,
    d_n=2^n-2-n(n-1),
    A(x)=sum_(n>=6) a_n x^n/n!,
    a_n=2^(n+1)-n^3+4n^2-7n-4.

Here d_4/4!=1/12 and a_6/6!=1/72. All earlier coefficients vanish.
In particular D is of order x^4=r^8, not order r^6. The denominator
x^2 E-(E-1)^2 is negative and asymptotic to -r^8/12.
A is of order x^6=r^12. Their quotient is asymptotic to r^4/6.

For completeness, positivity is an all-n argument. With Delta denoting forward
difference, (d_4,Delta d_4,Delta^2 d_4)=(2,8,14) and
Delta^3 d_n=2^n>0. Induction down the differences gives d_n>0 for n>=4.
Similarly (a_6,Delta a_6,Delta^2 a_6,Delta^3 a_6)=(10,46,94,122) and
Delta^4 a_n=2^(n+1)>0. Thus a_n>0 for n>=6.
Also d_n<=2^n and a_n<=2^(n+1), since
n^3-4n^2+7n+4=n^2(n-4)+7n+4>0 for n>=6.

For 0<x<=b=1/1600, divide out the vanishing powers FIRST:

    1/12 <= D(x)/x^4 <= D_plus(b),
    D_plus(b)=1/12+(4/15)b/(1-b/3),
    1/72 <= A(x)/x^6 <= A_plus(b),
    A_plus(b)=1/72+(16/315)b/(1-b/4).

These tails cover infinitely many terms. In the D tail, starting at n=5,
the positive majorant 2^n x^(n-4)/n! starts at (4/15)x; successive ratios
are 2x/(n+1)<=x/3. In the A tail, starting at n=7, the majorant
2^(n+1)x^(n-6)/n! starts at (16/315)x; successive ratios are <=x/4.
The geometric-series bounds are therefore valid uniformly down to x=0+.
No subtraction of nearly equal floating-point exponentials is used.

Since the denominators are positive, exact rational arithmetic gives

    1/7 < 1/[72 D_plus(b)] = 23995/144258
        <= a(r) <= 12 A_plus(b) = 224477/1343790 < 1/5.

Combining Sections 2, 3 and 5 proves Section 1 for every real radius in its
stated interval. The all-order proof is analytic; finite test loops are not
being substituted for induction or uniformity.

## 6. A limited centered-residual determinant corollary

Let H be the Hessian at M and H0=H-E[H|P]. The independent centered Gaussian
coordinates X=H0_tt/r^2, Y=H0_ts/r, Z=H0_ss have variances a(r),b(r),2.
Thus det H0=r^2(XZ-Y^2). Using Gaussian fourth moments,

    E[(det H0)^2 | P] = r^4[2a(r)+3b(r)^2] <= (23/20)r^4.

This is NOT a bound for the uncentered det H, nor a bound for a product of
endpoint and witness determinants. Mean terms must be restored before using
it in any weighted count. In particular it gives no Palm normalizer floor.

## 7. Evidence and reuse boundary

Run from the Math- repository root:

    python3 -B -S certificates/bf_six_pin_hessian_20260926/hessian_certificate.py
    python3 -B -S certificates/bf_six_pin_hessian_20260926/hessian_certificate.py --check certificates/bf_six_pin_hessian_20260926/CERTIFICATE.json
    python3 -B -S -m unittest discover -s certificates/bf_six_pin_hessian_20260926 -p 'test_*.py' -v
    python3 -O -B -S -m unittest discover -s certificates/bf_six_pin_hessian_20260926 -p 'test_*.py' -v

Finite controls cover kernel-derivative polynomial identities, exact cancellations,
initial forward-difference data, rational tail endpoints, domain and scope refusal.
The executable is not a Lean/Coq/Isabelle proof, a verifier of Gaussian regular
conditioning, or an all-order series proof checker. Nonauthor review is required.

No statement here covers SIDE24, higher dimensions, determinant-weighted Palm
laws, the coupled two-endpoint Hessian block, additional witness constraints,
pin microdisk/collar counts, SARD-G, RN-UNIF, elder selection, or P0.1 closure.
Those applications need separate, exact-scope arguments. No novelty claim is made.
