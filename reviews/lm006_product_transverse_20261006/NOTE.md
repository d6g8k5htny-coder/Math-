# LM006: exact transverse conditioning for an axial product covariance

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, `lm006-product-residual-r21a-20261006`. Scientific effect NONE.
Additive analytic companion; not a Lean proof, numerical certificate or status
change. Gaussian orthogonal regression and separable kernels are prior methods;
no general novelty or complete literature search is claimed.

## 1. Scope and source identities

Assume a centered real jointly Gaussian field has the ACTUAL covariance

    C((x,y),(s,t)) = rho(x-s) kappa(y-t), rho(0)=kappa(0)=1,      (1)

with real even factors and enough mean-square derivatives for every displayed
observation. Write F(x)=f(x,0), H(x)=f_y(x,0), Q(x)=f_yy(x,0), and

    m2=-kappa''(0), m4=kappa''''(0), g=m4-m2^2>0.

The primary result is finite-radius, and only requires the F derivatives
through order2, H through order1 and Q through transverse order2 that occur
below. Existence/continuity of higher contact jets is stated separately where
used. No finite fourth moment is silently relabeled a tenth spectral moment.

P is `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
read at `91821f9262b30ce7684b8ec5f1b4742893dac3d7`, blob
`dfed3b8d318a3ab1950957f393307733a4bef3f2`, sections1-2 ONLY as model/pin
source. Its global selection and lifetime theorem candidates are not premises.
E is #301 NOTE at `e31b6ad8356e0760c8a7fb6e816ff640c45176c9`, blob
`551aa563562bc88a19e33d146259c03aa2d318f6`: adjusted endpoint convention.
N is #315 NOTE at `5e027afcae8c7bd42a6df8ae2025f82105b3e586`, blob
`5790aaa0332bd8e79b276be1577e4c5f3502eed6`: exact typed weight/normalization.
B is #341 NOTE at `771913a7dffdc1283e491166d0faa9ec53e1f06a`, blob
`88dae06c5eefd102239f976513eb5e97c4ac7580`: prior general sign-band theorem
and eleven-observation density interface. That proof and review are unchanged;
this is a PRODUCT specialization, not a replacement for its general spectrum.

All formulas concern coordinate-axis separation. A rotated separable torus
covariance need not remain separable in the rotated coordinates. This note
does not assert arbitrary-orientation identities or independence after tilting.

## 2. Independent transverse residual process

Define R(x)=Q(x)+m2 F(x). Differentiating (1) gives for every x,s

    Cov(F(x),F(s))=rho(x-s),
    Cov(H(x),F(s))=Cov(Q(x),H(s))=0,
    Cov(Q(x),F(s))=-m2 rho(x-s),
    Cov(H(x),H(s))=m2 rho(x-s),
    Cov(Q(x),Q(s))=m4 rho(x-s).

The zero mixed terms use kappa'(0)=kappa'''(0)=0, not independence guessed
from a marginal covariance. Hence

    Cov(R(x),F(s))=Cov(R(x),H(s))=0,
    Cov(R(x),R(s))=g rho(x-s).                              (2)

Every finite family of R evaluations is independent of every finite family
of F,H evaluations. This is the jointly Gaussian zero-cross-covariance rule.
Taking mean-square limits preserves orthogonality and Gaussianity, so the
same independence holds with any existing F,H derivative observations. The
claims below need only finite such families; no path-space conditioning theorem
is required. In particular, axial and mixed Hessian observations provide no
additional information about R once their F,H families have been separated.

## 3. Exact conditional law after all eleven observations

Let M=-r/2, S=r/2 and c=rho(r), with -1<c<1. Put

 B=(F(M),F'(M),F''(M),F(S),F'(S),F''(S),
                      H(M),H'(M),H(S),H'(S)).

Assume Cov(B) is positive definite. This makes the canonical Gaussian law
well-defined at every finite prescribed B value. Under (2), B is independent
of (R(M),R(S)), whose covariance is g[[1,c],[c,1]]. Let

    J=R(S)-R(M), W=[R(S)+R(M)]/2.

Their covariance is zero, so they are independent Gaussian variables with

    Var(J)=2g(1-c), Var(W)=g(1+c)/2.

The eleven observations in B's sign-band setting are precisely B together
with G=Q(S)-Q(M). For fixed B,

    J=G+m2[F(S)-F(M)],
    Q(S)=W+G/2-m2[F(S)+F(M)]/2.

W is independent of (B,J), hence of (B,G). Consequently

 Q(S) | (B,G) ~ N(G/2-m2[F(S)+F(M)]/2, g[1+rho(r)]/2).     (3)

This proves the mean AND variance, with no eleven-by-eleven inverse or
coalescing-coordinate estimate. B's positive Gram and g(1-c)>0 also give a
positive eleven-observation Gram; the target has positive residual since c>-1.

On E's actual six pins F(M)=b_M,F(S)=b_S,F'=H=0, the adjusted coordinates
are a_±=F''(±r/2)/r, b_±=H'(±r/2)/r, c_±=Q(±r/2). Thus conditioning first
on the pins and then on (a_-,a_+,b_-,b_+,G) is exactly the conditioning in (3):
the missing four observations are recovered by multiplying by r, while the
original pins are retained. Neither Q(S)/r nor an extra Jacobian is introduced.
The conditional density cap is exactly

    D_r = [pi g(1+rho(r))]^(-1/2).                           (4)

If rho(r)>=0, D_r<=1/sqrt(pi g). For a general product covariance this
last uniform bound REQUIRES that extra sign condition. Positive definiteness
only gives |rho|<=1, not rho>=0. A negative-correlation control is retained.

Under the six pins ALONE, the transverse pair is a translate of the same
R pair, independent of the four axial/mixed endpoint coordinates, with

    E G=m2(b_M-b_S), Var(G)=2g[1-rho(r)],
    E G^2=m2^2(b_M-b_S)^2+2g[1-rho(r)].                    (5)

This independence is under the original Gaussian pin law, not the law tilted
by the product of Hessian determinants. The tilted density couples coordinates.

## 4. Contact variance, limiting normalizer, and direct G bound

Where the contact derivatives exist, the six original contact pins consist
of F,F',H,F'',H',F''' at0, with F=b and the remaining prescribed values as
in E. R(0) is independent of all those rows by (2), so

    Q_L ~ N(-m2 b,g).                                      (6)

This does not identify g with the normalizer. If the enlarged eleven contact
jets B discusses also exist, they add pure F and H derivatives and Q'(0).
Cov(R(0),Q'(0))=g rho'(0)=0. Thus its exact scalar residual variance is ALSO g,
not merely a positive unspecified Schur complement. Their joint Gram still
requires nondegeneracy if conditioning at arbitrary targets is intended.

For b>=0, the negative-part monotonicity gives

    z0=E[(Q_L)_-^2]>=g/2>0.                                (7)

An optional closed form follows by two integrations by parts of the standard
normal density phi: with a=m2 b/sqrt(g),

    z0=(g+m2^2 b^2)Phi(a)+m2 b sqrt(g)phi(a).               (8)

Indeed Q_L=sqrt(g)(Z-a), and integrals of Z phi and Z^2 phi on(-infinity,a]
are -phi(a) and Phi(a)-a phi(a). Formula (8) holds for any real b; (7) is
only claimed for b>=0. No numeric evaluation of these constants is supplied.

Suppose rho is an even spectral correlation with finite axial second moment
s2=-rho''(0). Since 1-cos u<=u^2/2, 1-rho(r)<=s2 r^2/2. Under the fixed
LM006 gap b_M-b_S=r^3/6, (5) yields

    E G^2<=g s2 r^2+m2^2 r^6/36
           <=Gamma r^2, Gamma=g s2+m2^2/36, 0<r<=1.        (9)

This is a direct same-law bound, not an assumed full-vector coupling rate.
Using the band integration already derived in B, or directly integrating
(gap-t)(r b_+^2+(a_+)_-t), Cauchy-Schwarz and Gaussian fourth/sixth moments give

 N_r=E[T_r 1_{c_+>=0}]
   <=D_r[(r/2)sqrt(3 K6) E G^2
                     +(1/6)sqrt(15 K4)(E G^2)^(3/2)],
 K4=E[a_-^2 a_+^2], K6=E[a_-^2 b_+^4].                    (10)

If K4<=C4,K6<=C6,z_r=E T_r>=z_*>0 and rho(r)>=0 on one interval, then

 nu_r{c_+>=0} <= min(1,
   [sqrt(3 C6)Gamma/2+sqrt(15 C4)Gamma^(3/2)/6]
                       r^3/[z_* sqrt(pi g)]).             (11)

The new identities supply D_r and Gamma, NOT the remaining uniform moment
bounds or a finite-r normalizer radius. Those are separate input obligations
before applying (11). In the smooth fixed model, E's established moment/UI
argument supplies such inputs on a sufficiently small interval; this note is
not a new review of that entire argument. The algebra of (10) uses no
independence under the tilted law and no physical-normalizer substitution.

## 5. Exact model match and scope failures

P's d=2 coordinate-axis covariance factors by its positive image sums as

    rho_L(x)=sum_n exp(-(x+Ln)^2/2)/sum_n exp(-(Ln)^2/2),
    K_L(x,y)=rho_L(x)rho_L(y).                              (12)

Hence kappa=rho_L, g=m4-m2^2 for its actual one-dimensional spectral moments.
All spectral moments are finite, g>0 because both zero and nonzero squared
frequencies have positive mass, and rho_L(r)>0 for every real r. Its full
lattice spectrum gives the positive Gram of the ten distinct observations B
at distinct sites. For 0<r<L, |rho_L(r)|<1: equality in the unit-modulus
spectral average would require all positive-mass character phases to agree;
the zero and first modes rule this out away from multiples of L. Thus (3)-(5)
and the uniform cap in (4) apply for every such positive separation, even
though raw observation conditioning deteriorates near collision. The exact
fixed LM006 target is b_M=6/5, b_S=6/5-r^3/6; its conditional mean in (3) is
G/2-m2(6/5-r^3/12). This is the unscaled physical f_yy(S).

We do not generalize (12) to arbitrary orientations or to nonseparable
spectra. A positive even joint spectrum proportional to product weights times
(1+k_x^2 k_y^2/100) has nonzero Cov(Q+m2F,F''); the checker exhibits it.
If g=0 the residual vanishes. If rho=-1 the target conditional variance is
zero. At period aliasing rho=1 some unequal-height pins can be incompatible.
All are excluded from the positive-density statement, not patched by formal
division by zero. Generic #341 remains useful where separability is absent;
its higher-jet sufficient condition is not declared false or superseded.

## 6. Reproduction, provenance, and limits

Run `python -B -S test_product_transverse.py` and its `-O` version. Twelve
methods check independent full 11-observation rational Schur regressions,
conditional mean values under varied nuisance observations, six-pin difference
laws, eleven contact jets, residual orthogonality/kernel, and explicit
nonproduct/negative-correlation/zero-gap/collision cases. The finite models
use 55 positive product spectral modes and three rational unit-circle phases.
Their direct covariance sums include derivative signs; the regression matrix
is constructed without using (2)-(5). This is not a sampled infinite covariance
or a periodic Gaussian numerical certificate. The 30-control standalone driver
has six deliberately incorrect alternatives with exact PRODUCT_FAIL reasons.
Both Python modes and invalid CLI handling are required. Test-first12 missing-
implementation assertion failures are preserved; no local Lean run is claimed.

This is an author-side result requiring its own nonauthor source-bound review.
No previous PASS is transferred. General orthogonal Gaussian regression and
product kernels are prior methodology. Wilson et al., JMLR22(105),2021,
publication abstract was checked as context only, not as a proof premise.
No full literature novelty, whole-field event identity, all-mark/orientation
uniformity, elder/capture/persistence closure, numerical constant/radius,
independent formal alignment or repaired production gate is asserted. Existing
scientific registers and the blocked #329 operation are unchanged.
