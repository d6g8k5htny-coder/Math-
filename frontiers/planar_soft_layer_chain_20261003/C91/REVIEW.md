# C91 full nonauthor analytic review — PASS_TECHNICAL_SCOPED

**Verdict: ACCEPT / PASS_TECHNICAL_SCOPED for the exact C91 v1 deterministic statement.** No mathematical amendment or blocking finding was found. Theorems 1–2 are accepted under their stated deterministic assumptions. Section 3 is accepted as a conditional application of a **valid imported elder-trap certificate**, not as acceptance of literal A2 v1, an unconditional field-probability bound, or a global persistence theorem.

This completes [actual review pickup5963597644](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963597644); my scoped review work is released. Root01a0bbb5 retains C91 author/delivery claim7eeb2f7b. Claude's A2 amendments and existing UI/intermediate/coarea custody are unchanged.

## Exact source and actual exposure

Full candidate read: [comment5963566666](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963566666), `C91-PLANAR-WINDOW-TAYLOR-TRANSFER-20261003-v1`, **12,433 UTF-8 bytes**, SHA256 `74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa`. Fresh native readback was unchanged before publication.

Actual executor: OpenAI/Codex coordinating `/root` Work Mode session, distinct from C91 author root01a0bbb5. Exact model-build identifier is not exposed here. Prior C91 outline, FL.1/QS intake and cubic-source exposure are disclosed. I did not author C91, amend its proof or use author checker code. Existing OpenAI/Codex helper `c86_fresh_review` read the full candidate and supplied supporting reconstruction of §§1.3, 2, 3; this is not a second acceptance vote or organizational-independence credit. No proof repair contribution was incorporated.

Dylan Roy — delegated AI review. Personal reading **PENDING**, organizational independence **0**, scientific effect **NONE**.

Consumed interfaces actually read:
- FL.1 and raw setting: [Math243 PROOF at e8c76a4](https://github.com/d6g8k5htny-coder/Math-/blob/e8c76a4080e8e8be3dd9f613006263be6d53bad3/frontiers/soft_fold_limit_20261002/PROOF.md), blob `6502cf7ba2edee47761e40308c15b7563b06d1f8`, **78,874B**, SHA256 `f972f46d6b7348a4ff5d2eea022694364895a5273265818533dd01204b4c06a0`. Motivating source, not an imported C5 proof of this new C4 estimate.
- [QS5961415030](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5961415030), **37,032B**, SHA256 `12ffa126e45253fea5eec47f50ffa842a61165a2cbc0f5917e3543e81c09c1f2`: global setting, local rescalings and E1/E2/E3 interface freshly read.
- CU.1 pin interface at blob `f6df5a7356a54771b0052e42a864a140709903ad` and #242 raw model at blob `271412dbc96a29590f5f805258e15c9e335cb430` were source-exposed during intake. The pin/Taylor and coordinate arguments below reconstruct directly; no Gaussian or decision-limit theorem is imported from them.

## 1. C4 pin corrections: every coefficient reconstructs

Let a=r/2. C4 regularity supplies value remainders bounded by `Na^4/24` and derivative remainders bounded by `Na^3/6`. The two derivative pins give

```text
|g1+a^2 g3/2| <= Na^3/6,
|g2| <= Na^2/6.
```

The value difference is -8ka^3. Substitution of the first inequality makes it `-(2/3)a^3 g3` plus an error at most

```text
2a(Na^3/6)+2(Na^4/24)=5Na^4/12.
```

Therefore `|g3-12k|<=5Na/8`. Substituting back gives `|g1+6ka^2|<=(5/16+1/6)Na^3=23Na^3/48`. In the value average, `a^2g2/2` contributes at most `Na^4/12` and the averaged remainder at most `Na^4/24`; their sum is `Na^4/8`. This proves all W7–W8 constants.

For q=f_z on the axis, C4 gives q a bounded third derivative. Its order-two Taylor formula and the two transverse-gradient pins give exactly W9. No fifth derivative is needed. After raw scaling, the six correction coefficients are bounded by Nr times

```text
1/(128k_-), 23/(384k_-), 1/(48k_-), 5/(96k_-), 1/48, 1/24,
```

for `1,X,X^2,X^3,zeta,X*zeta`, respectively. The pure transverse second derivative and the remaining third jets are retained exactly in G_k; no smallness or sign assumption on them is hidden.

## 2. Differentiated remainder and all mixed derivatives

For any multiindex alpha of total order m<=2, `D^alpha T3` is exactly the degree-(3-m) Taylor polynomial of `D^alpha f`. Its next derivative has total order four. The directional integral remainder and multinomial expansion therefore give

```text
|D^alpha(f-T3)(x,z)| <= N(|x|+|z|)^(4-m)/(4-m)!.
```

This uses the stated maximum of **all coordinate partials through order four**, in the fixed frame. A dominating operator-derivative norm is sufficient, but an unrelated or lower-order norm would not be.

A raw alpha=(i,j) derivative multiplies by `r^i(rk)^j`. Dividing by kr^3 yields W11, including the mixed alpha=(1,1) case. The respective maxima of `k^(j-1)` for m=0,1,2 are bounded by `1/k_-,M1,M2`.

For each correction monomial, coordinate derivatives of exact order m have size at most its tabulated number times `w^(4-m)`, since w>=1 and its degree is at most three. The three sums are

```text
9/(64k_-)+1/16,
33/(128k_-)+1/16,
17/(48k_-)+1/24.
```

Adding the differentiated remainder bounds proves W3–W4. At k=1 the exact sums are

```text
K0=167/192, K1=635/384, K2=115/48.
```

The order-two quantity is an **entrywise Hessian bound**, not yet an operator norm. Theorem 2 correctly accounts for that distinction. W0 gives the claimed injective local-chart interpretation; the globally periodic lift itself permits the Taylor segments without that geometric restriction.

## 3. Sharpness survives the global C4 norm and periodic extension

For the stated quartic family,

```text
E=(tr/k)(X^2-1/4)^2,
E_X=(tr/k)(4X^3-X),
E_XX=(tr/k)(12X^2-1).
```

The quartic and its first axial derivative vanish at both pins, and no transverse jet is introduced. Thus the model really is the axial cubic.

Choose fixed b,k,t and a fixed smooth cutoff supported in an injective torus chart, equal to one on a smaller ball. The polynomial coefficients are uniformly bounded for small r. By the product rule, every derivative through order four of the cutoff field is uniformly bounded on the torus: all cutoff derivatives are fixed, and the polynomial is evaluated on a fixed compact support. Hence the global N in the statement stays bounded.

Choose w tending to infinity with rw tending to zero, for example `w=r^(-1/8)`; for fixed k the entire raw window eventually lies where the cutoff equals one. Evaluating at X=w gives nonzero leading coefficients 1,4,12 in degrees 4,3,2. Against any smaller proposed power p<4-j, the ratio grows at least as a fixed positive multiple of `w^(4-j-p)`. This proves the stated obstruction, not just a local formal example.

This sharpness fixture need not satisfy Theorem 2's later typing assumptions; Theorem 1 and its sharpness statement do not require them. No Gaussian-family norm bound is inferred.

## 4. Exact shear and Hessian transfer

Substitute `X=u-Z/12,zeta=Z/gamma`. The axial cubic and gamma mixed term cancel the linear Z and u^2Z terms, leaving `-uZ^2/24+Z^3/432`. Adding the transverse terms gives

```text
-(lambda_tilde/(2gamma^2)) Z^2
+(-1/24+B/(2gamma^2)) u Z^2
+(1/432-B/(24gamma^2)+C3/(6gamma^3)) Z^3.
```

These are precisely W14's psi,c,R coefficients. The identity holds for either sign of nonzero gamma.

The inverse affine shear followed by the QS ellipse rescaling gives T_i in W15. There is no gradient-dependent Hessian-chain correction, because the transformation is affine. Typing gives `a_S,a_M>0` and

```text
gamma^2 kappa_i=a_i/48,
||T_i||F^2=1/3+(1/144+1/gamma^2)/kappa_i
          =1/3+(gamma^2+144)/(3a_i).
```

A symmetric 2-by-2 raw Hessian with entries bounded by epsilon2 has operator norm at most 2epsilon2. Therefore

```text
||T_i^T H_E T_i||op
 <= 2epsilon2 ||T_i||F^2
 = (2epsilon2/3)[1+(gamma^2+144)/a_i].
```

This is W16, with both genuine typing-edge denominators retained. Gamma=0 is still outside the coordinate chart. Along nonzero gamma tending to zero, the right side stays bounded if a_i stays bounded below. No uniform assertion through a_i=0 is made.

## 5. Conditional trap application and global path lifting

The raw containment of V_eta and both ellipses is a necessary premise. W17 and W18 then supply exactly QS's strict C0 bound, its S-Hessian bound <=2/5, and its M-Hessian bound <1. W1 and the exact model pins supply zero error values and gradients at both pins. The periodic C4 lift supplies global continuity and the required local C2 regularity.

For any valid imported certificate, retain **all** its restrictions. If the original QS-E certificate is used, its Delta exclusion is retained; using a corrected A2 replacement requires that replacement as an identified valid input. C91 does not itself validate the proposed A2 box or erase the recorded v1 AMEND disposition.

Every continuous torus path starting at M lifts to a plane path starting at the chosen lift of M; every plane path projects back. Values and the endpoint condition f>b are preserved. Paths are not required to stay in the injective chart. Thus the maximin of f equals that of its unnormalized lift. Positive affine normalization at k=1 gives

```text
d_F_r(M)=(d_f(M)-b)/r^3.
```

The invertible raw/sheared coordinate map preserves this normalized maximin. A valid certificate yielding d_g(M)=-1 therefore gives `d_f(M)=b-r^3=f(S)`, as claimed. This is not a proof of unique persistence pairing in the absence of the additionally stated Morse/critical-value convention.

## 6. Independent exact controls and reproducible source

I wrote and ran the standard-library script below without author-code reliance. It passes **2,734 explicit checks** in normal and optimized modes with identical **276-byte output**, SHA256 `f583ed9982c2c9e31e3fea24c732fefc753c8a5e11d149deb979318440db3c92`.

The script is **6,510 UTF-8 bytes**, including its final newline, SHA256 `2d456e6da00c11a7b9a306c8d56d97b7868ddeda4924201d814a85818484d409`. It checks exactly pinned quartic polynomial families, all six derivative multiindices through order two, explicit norm-majorized window fixtures, the constants, both signs of gamma in the shear, and both typing-edge identities. Four built-in wrong-identity counterchecks detect an omitted X*zeta pin correction, an omitted k^2 chain factor, a lost gamma^2 numerator and a lost cubic shear term. These are identity counterchecks, not four separately executed mutant programs.

The polynomial norm bounds used in fixtures are certified coefficient-sum upper bounds on their fixed physical square. They are computational support for those fixtures, not a sampled inference of the universal C4 theorem. The universal Taylor, cutoff and topological proofs are reconstructed above.

```python
from fractions import Fraction as F
from math import factorial
import json

checks = 0
def require(ok, label):
    global checks
    checks += 1
    if not ok:
        raise ValueError(label)
def clean(p):
    return {a:F(c) for a,c in p.items() if c}
def add(*ps):
    q={}
    for p in ps:
        for a,c in p.items():
            q[a]=q.get(a,F(0))+c
    return clean(q)
def scale(p,c):
    return clean({a:v*c for a,v in p.items()})
def mul(p,q):
    z={}
    for (i,j),v in p.items():
        for (a,b),w in q.items():
            e=(i+a,j+b)
            z[e]=z.get(e,F(0))+v*w
    return clean(z)
def deriv(p, alpha):
    q=p
    for axis,n in enumerate(alpha):
        for _ in range(n):
            z={}
            for a,c in q.items():
                if a[axis]:
                    b=list(a); b[axis]-=1
                    z[tuple(b)]=c*a[axis]
            q=clean(z)
    return q
def val(p,x,z):
    return sum((c*x**i*z**j for (i,j),c in p.items()),F(0))
def pull(p,r,k):
    return clean({(i,j):c*r**i*(r*k)**j/(k*r**3)
                  for (i,j),c in p.items()})
def norm_bound(p,w):
    return sum((abs(c)*w**(i+j) for (i,j),c in p.items()),F(0))
def jet(p,i,j):
    return val(deriv(p,(i,j)),F(0),F(0))
alphas=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
rejected=[]
def rejection(label, actual, wrong):
    require(actual != wrong, "mutant did not differ: "+label)
    rejected.append(label)

for r in (F(1,32),F(1,16),F(1,8)):
  for k in (F(1,2),F(1),F(3,2)):
    a=r/2
    D={(2,0):F(1),(0,0):-a*a}
    base={(3,0):2*k,(1,0):-F(3,2)*k*r*r,(0,0):-k*r**3/2}
    lam,gam,B,C=F(2),F(3),F(-2),F(1)
    cubic=add(base,{(0,2):-lam*r/(2*k)},
              scale(mul({(0,1):F(1)},D),gam/2),
              {(1,2):B/2,(0,3):C/6})
    families=[(1,0,0,0,0),(0,1,0,0,0),(0,0,1,0,0),
              (0,0,0,1,0),(0,0,0,0,1),(2,-3,4,-2,1)]
    for t,d,e,h,l in families:
      f=add(cubic,scale(mul(D,D),F(t)),
            scale(mul(mul({(1,1):F(1)},D),{(0,0):F(1)}),F(d)),
            {(2,2):F(e),(1,3):F(h),(0,4):F(l)})
      require(val(f,-a,F(0)) == 0 and val(f,a,F(0)) == -k*r**3,"values")
      for q in (deriv(f,(1,0)),deriv(f,(0,1))):
        require(val(q,-a,F(0)) == val(q,a,F(0)) == 0,"gradient pins")
      g3,gamma,bj,cj=jet(f,3,0),jet(f,2,1),jet(f,1,2),jet(f,0,3)
      lt=-k*jet(f,0,2)/r
      G={(3,0):F(2),(1,0):-F(3,2),(0,0):-F(1,2),
         (2,1):gamma/2,(0,1):-gamma/8,(0,2):-lt/2,
         (1,2):k*bj/2,(0,3):k*k*cj/6}
      E=add(pull(f,r,k),scale(G,-1))
      Q={(2,0):F(1),(0,0):-F(1,4)}
      expected=scale(add(scale(mul(Q,Q),F(t)/k),
                 scale(mul({(1,1):F(1)},Q),F(d)),
                 {(2,2):F(e)*k,(1,3):F(h)*k*k,(0,4):F(l)*k**3}),r)
      require(E == expected,"exact quartic raw error")
      N=max(norm_bound(deriv(f,(i,j)),F(1))
            for m in range(5) for i in range(m+1) for j in [m-i])
      require(abs(g3-12*k)<=5*N*r/16,"g3")
      require(abs(jet(f,1,0)+F(3,2)*k*r*r)<=23*N*r**3/384,"g1")
      require(abs(jet(f,0,0)+k*r**3/2)<=N*r**4/128,"g0")
      require(abs(jet(f,2,0))<=N*r*r/24,"g2")
      require(abs(jet(f,0,1)+r*r*gamma/8)<=N*r**3/48,"fz")
      require(abs(jet(f,1,1))<=N*r*r/24,"fxz")
      H=1+k
      Ks=[F(9,64)/k+F(1,16)+H**4/(24*k),
          F(33,128)/k+F(1,16)+max(1/k,F(1))*H**3/6,
          F(17,48)/k+F(1,24)+max(1/k,F(1),k)*H**2/2]
      for alpha in alphas:
        require(deriv(E,alpha)==deriv(expected,alpha),"mixed polynomial identity")
        # Pulled physical derivatives and raw derivatives must agree exactly.
        i,j=alpha
        lhs=deriv(pull(f,r,k),alpha)
        rhs=scale(pull(deriv(f,alpha),r,k),r**(i+j)*k**j)
        require(lhs==rhs,"derivative pullback")
        for w in (F(1),F(2)):
          require(r*(1+k)*w<=1,"fixture domain")
          require(norm_bound(deriv(E,alpha),w)<=Ks[i+j]*N*r*w**(4-i-j),
                  "coefficient-certified window fixture")
      if d and not t and not e and not h and not l and r==F(1,32) and k==1:
        rejection("omit_Xzeta_pin_correction", E,
                  add(E,{(1,1):F(d)*r/4}))
      if l and not t and not d and not e and not h and r==F(1,32) and k==F(3,2):
        alpha=(0,2)
        wrong=scale(pull(deriv(f,alpha),r,k),r*r) # missing k^2
        rejection("omit_k_squared_chain_factor",deriv(pull(f,r,k),alpha),wrong)

require(F(9,64)+F(1,16)+F(16,24)==F(167,192),"K0")
require(F(33,128)+F(1,16)+F(8,6)==F(635,384),"K1")
require(F(17,48)+F(1,24)+F(4,2)==F(115,48),"K2")
for gamma in (F(1,4),F(1),F(2),F(4)):
  for lt in (F(1),F(2)):
    for B in (F(-1,4),F(0),F(1,4)):
      for sign in (-1,1):
        a=24*lt+sign*(gamma*gamma-12*B)
        require(a>0,"typed transfer fixture")
        kap=a/(48*gamma*gamma)
        left=F(1,3)+(F(1,144)+1/(gamma*gamma))/kap
        right=F(1,3)+(gamma*gamma+144)/(3*a)
        require(left==right,"Frobenius denominator identity")
        if gamma==1 and lt==1 and B==0 and sign==1:
          rejection("drop_gamma_squared_numerator",right,F(1,3)+F(144)/(3*a))
# Exact constant leading derivatives of the quartic obstruction.
Q={(2,0):F(1),(0,0):-F(1,4)}
quartic=mul(Q,Q)
for j,leading in ((0,F(1)),(1,F(4)),(2,F(12))):
    p=deriv(quartic,(j,0))
    require(p[(4-j,0)]==leading,"sharpness derivative power")

def power(p,n):
    q={(0,0):F(1)}
    for _ in range(n):
        q=mul(q,p)
    return q
def compose(p,x,z):
    return add(*(scale(mul(power(x,i),power(z,j)),c)
                 for (i,j),c in p.items()))
for gamma in (F(-4),F(-2),F(-1),F(-1,4),F(1,4),F(1),F(2),F(4)):
  for lt in (F(1),F(2)):
    for B in (F(-1,4),F(0),F(1,4)):
      for C in (F(-1),F(0),F(1)):
        raw={(3,0):F(2),(1,0):-F(3,2),(0,0):-F(1,2),
             (2,1):gamma/2,(0,1):-gamma/8,(0,2):-lt/2,
             (1,2):B/2,(0,3):C/6}
        X={(1,0):F(1),(0,1):-F(1,12)}
        zeta={(0,1):1/gamma}
        shear=compose(raw,X,zeta)
        psi=24*lt/(gamma*gamma)
        c=1-12*B/(gamma*gamma)
        R=8-144*B/(gamma*gamma)+576*C/(gamma**3)
        P=clean({(3,0):F(2),(1,0):-F(3,2),(0,0):-F(1,2),
                 (0,2):-psi/48,(1,2):-c/24,(0,3):R/3456})
        require(shear==P,"exact G1/P shear identity, both gamma signs")
        if gamma==1 and lt==1 and B==0 and C==1:
            rejection("drop_transverse_cubic_shear_term",P,
                      add(P,{(0,3):-F(1,6)}))

print(json.dumps({"checks":checks,"rejected_mutants":rejected,
  "constants":["167/192","635/384","115/48"],
  "scope":"exact polynomial/chain/constant fixtures, not universal proof"},
  sort_keys=True,separators=(",",":")))
```

Observed stdout in both modes:

```json
{"checks":2734,"constants":["167/192","635/384","115/48"],"rejected_mutants":["omit_Xzeta_pin_correction","omit_k_squared_chain_factor","drop_gamma_squared_numerator","drop_transverse_cubic_shear_term"],"scope":"exact polynomial/chain/constant fixtures, not universal proof"}
```

Still outside this verdict: probabilities of W18, Gaussian weighted moments of N on growing windows, law/determinant-weight comparison, actual-field rejected-side confinement, regional collision, intermediate coarea, unrestricted density/remainder and the full persistence-measure bridge. No source commit, CI, merge, independent human acceptance or scientific status change is represented.
