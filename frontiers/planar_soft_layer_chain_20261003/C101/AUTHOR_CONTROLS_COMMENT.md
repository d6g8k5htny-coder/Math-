# C101 author finite controls and exact source identities

Author/executor: OpenAI/Codex root01a0adb2. This is AUTHOR-SIDE evidence, not a nonauthor review or theorem acceptance. Fresh reviewer: do not consume/reuse this author checker before freezing your own source analysis and control design. Root01a0bbb5 owns fresh-review dispatch and the single registered delivery.

Frozen [full proof5967063473](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967063473): 36333 UTF-8 bytes, SHA256 `300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4`.

Exact artifact extraction: contents of each labeled fenced block only, with one final LF retained. No archive/repository commit/CI/merge/register is created here.

- `controls.py`: 12018B, SHA256 `f3d5716ce30c37b702525eef31c29fad387ede7d8866c334f8133bc45bae9f15`.
- `controls.stdout`: 1668B, SHA256 `8ea3acfb97500add9e3a0a60f98125255a98d4b25d2e98a2f02a472df7ed3754`.
- `SOURCES.json`: 8256B, SHA256 `b17158a0ff07e9f67b9d84f1f38e44b6dfafdda9ee98c9aa6064a4a7d5d71a7e`.

Executed Python3.12.14 normal, `-O`, `-S`, and `-O -S`: all exit0, complete stdout identical. 6859 explicit exception-based rational controls; 23 substantive false-inference fixtures rejected. A test-first missing-ledger fixture initially raised NotImplementedError, then passed after implementation. No assertions are used. The finite script does not prove Gaussian regression, cap/topology inputs, or the uniform analytic argument.

### controls.py

```python
"""C101 author-side exact controls; standard library only, no sampled inference.

The uniform Gaussian, geometry and tail statements are analytic source-bound
arguments in PROOF.md. This script controls their algebra/exponent ledger and
rejects explicitly false inferences; it does not accept the theorem.
All checks use explicit exceptions and survive python -O.
"""
from fractions import Fraction as F
from itertools import product
import sys

checks = 0
counterchecks = []

def require(ok, message):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(message)

def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("false inference survived: " + name)
    counterchecks.append(name)

def balance(m):
    if not isinstance(m, int) or m < 1:
        raise ValueError("fixed integer m>=1 required")
    return F(1, 2*(m+3)), F(m, 2*(m+3))

def det2(a, b, c):
    return a*c-b*b

def filtered(a, b, c, index):
    d = det2(a,b,c)
    if d == 0:
        return F(0)
    if index == 1:
        return -d if d < 0 else F(0)
    if index == 2:
        return d if d > 0 and a+c < 0 else F(0)
    raise ValueError("supported indices are 1,2")

def positive(x):
    return max(F(0), x)

def integral(coeffs, left, right):
    return sum(c*(right**(i+1)-left**(i+1))/F(i+1)
               for i,c in enumerate(coeffs))

def polynomial_mul(a,b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out

def cutoff_checks():
    require(balance(3) == (F(1,12),F(1,4)), "m=3 balance")
    require(F(10)+2*3 == 16 and F(6)+2*3 == 12, "m=3 moment orders")
    for m in range(1,65):
        a,b = balance(m)
        u = 1-b/2
        require(a > 0 and 0 < b < F(1,2), "fixed m positivity")
        require(m*a == b and 3*a == F(1,2)-b, "tail/endpoint balance")
        direct = [
            b, 1-3*a+b/2, -4*a+u, 1-5*a+u/2,
            -4*a+2*u/3, 1-5*a+u/3, b, 1-4*a,
            -3*a+2*(u-b), 2-5*a-b/2, 2-7*a-b/4, m*a, F(1)
        ]
        closed = [
            b, F(1,2)+3*b/2, F(1,3)+5*b/6,
            F(2,3)+17*b/12, b, F(1,2)+3*b/2, b,
            F(1,3)+4*b/3, F(3,2)-2*b,
            F(7,6)+7*b/6, F(5,6)+25*b/12, b, F(1)
        ]
        for i,(x,y) in enumerate(zip(direct,closed)):
            require(x == y, "ledger identity m=%s term=%s"%(m,i))
            require(x >= b, "ledger dominates requested rate")
        for x in [1-a,1-b/8,u,u-2*a,u-3*a,1-b/4,b]:
            require(x > 0, "admissibility vanishing exponent")
        require(u-3*a == F(1,2)+b/2, "endpoint cutoff exponent")
        require(3+b < F(7,2), "consumer exponent below 7/2")
    for target in [F(1,100),F(1,8),F(1,4),F(1,3),F(2,5),F(49,100)]:
        lower = 6*target/(1-2*target)
        m = max(1, (lower.numerator+lower.denominator-1)//lower.denominator)
        require(balance(m)[1] >= target, "integer m for target")
    require(1-F(1,4)/2 == F(7,8), "first e exponent")
    require(3+F(1,4) == F(13,4), "first consumer exponent")

def determinant_and_shear_checks():
    lambdas = [F(-2),F(-1),F(-1,2),F(0),F(1,4),F(1,2),F(1),F(2),F(4)]
    for lam,g,B in product(lambdas,map(F,range(-3,4)),map(F,range(-2,3))):
        D = g*g-12*B
        aM,aS = 24*lam-D,24*lam+D
        w = positive(6*lam+3*B-g*g/4)*positive(6*lam-3*B+g*g/4)
        fM = filtered(F(-6),-g/2,-lam-B/2,2)
        fS = filtered(F(6),g/2,-lam+B/2,1)
        require(fM*fS == w, "actual endpoint model filtered product")
        require((w > 0) == (aM > 0 and aS > 0), "typed domain")
        require(w <= 36*max(lam,F(0))**2, "quadratic weight majorant")
        require((6*lam+3*B-g*g/4)+(6*lam-3*B+g*g/4) == 12*lam,
                "unclipped factor sum")
        if w > 0:
            require(w == aM*aS/16, "aM/aS weight")
            Bsh = -D/12
            require(w == 9*(4*lam*lam-Bsh*Bsh), "CUB shear weight")
        for s,sign in [(aM,F(1)),(aS,F(-1))]:
            restored = (s-24*lam+g*g)/12 if sign == 1 else (24*lam+g*g-s)/12
            require(restored == B, "both B1 substitutions")
            require(abs(sign/12) == F(1,12), "absolute strip Jacobian")
        if g != 0:
            psi,c = 24*lam/g**2,D/g**2
            require((aM*aS/16)*g**2/24 == g**6*(psi**2-c**2)/384,
                    "gamma6/384 exact chart Jacobian")
    for g,B,C3 in product(map(F,range(-2,3)),map(F,range(-2,3)),map(F,range(-2,3))):
        J = 8*g**3-144*B*g+576*C3
        Dsh = (C3-g*B/4+g**3/72)/2
        require(Dsh == J/1152, "cubic shear coefficient")
        require(- (g*g-12*B)/12 == B-g*g/12, "quadratic shear coefficient")
        require(g**6*(F(1) if g==0 else ((g*g-12*B)/g**2)**3)
                == (F(0) if g==0 else (g*g-12*B)**3),
                "c cancellation on nonzero chart")
        if g != 0:
            require(g**6*(J/g**3)**2 == J**2, "R pole cancellation")

def scalar_integrals_and_constants():
    for U in [F(1,4),F(1,2),F(1),F(2),F(3)]:
        # Inner antiderivative at 48lambda yields 1152lambda^3.
        inner_at_unit = integral([0,F(48,16),F(-1,16)],0,48)
        require(inner_at_unit == 1152, "inner weighted radius integral")
        require(integral([0,0,0,inner_at_unit],0,U) == 288*U**4,
                "outer weighted radius integral")
        require(integral([0,48],0,U) == 24*U**2, "unweighted comparison radius integral")
    K0,K1,K2=F(167,192),F(635,384),F(115,48)
    require(2*K2 == F(115,24), "endpoint raw Hessian op bound")
    require(F(115,72)/F(2,5) == F(575,144), "saddle Hessian tolerance factor")
    CV=500*K0*48**2/3
    CT=F(4,9)*48**3+676*48+F(728**2,36)
    CH=27*K0*CT/8
    require(CV > 0 and CH > 0, "cutoff constants positive")
    for Lam in [F(1),F(2),F(3),F(8)]:
        H=1+Lam
        Ctau=F(4,9)*(48*Lam)**3+676*(48*Lam)+F(728**2,36)
        ch=4/(27*Ctau)
        cstar=3/(250*(48*Lam)**2)
        require(Ctau <= CT*H**3, "Ctau uniform H3 majorant")
        require(2*K0/cstar <= CV*H**2, "selected epsilon constant")
        require(K0/(2*ch) <= CH*H**3, "endpoint epsilon constant")
        for sroot in [F(1),F(2),F(3),F(4)]:
            s=sroot**2
            for g,B,C3 in product(map(F,[-2,0,2]),map(F,[-1,0,1]),map(F,[-1,0,1])):
                P=1+abs(g)+abs(B)+abs(C3)
                D,J=g*g-12*B,8*g**3-144*B*g+576*C3
                tau2=(F(2,3)+2*abs(D)/s+abs(J)/(6*sroot**3))**2/3
                require(abs(D) <= 13*P**2 and abs(J) <= 728*P**3,
                        "raw polynomial bounds")
                require(tau2 <= Ctau*P**6/s**3, "endpoint tau squared")
    for delta in [F(1,2),F(1,4),F(1,8)]:
        top=F(48)
        require(1/delta-1/top <= 1/delta, "v3 model truncation")
        require((delta**-2-top**-2)/2 <= delta**-2/2, "v3 actual truncation")
        require((delta**-2-top**-2)/2 <= delta**-2/2, "v4 model truncation")
        require((delta**-3-top**-3)/3 <= delta**-3/3, "v4 actual truncation")
        require((delta**-4-top**-4)/4 <= delta**-4/4, "v6 model truncation")
        require((delta**-5-top**-5)/5 <= delta**-5/5, "v6 actual truncation")
    for r,J in product([F(1,16),F(1,8)],[F(1),F(2),F(3)]):
        lmax=4*r*J**2
        scalar=integral([0,r*J**2,1],0,lmax)
        rare=r**2*J**4*scalar
        require(rare == F(88,3)*r**5*J**10, "retained rare scalar integral")
        require(rare/r**2 == F(88,3)*r**3*J**10, "one full Z ledger")
    for h in [F(1,16),F(1,4),F(1,2)]:
        p=[F(0),F(0),-3*h,2*h]
        factor=polynomial_mul([1,-2,1],[1,2])
        require([h*x for x in factor] == [h,0,-3*h,2*h], "chord clearance factor")
        require(sum(p[i]*2**i for i in range(4)) == 4*h, "older endpoint height")
        for t in [F(j,8) for j in range(17)]:
            val=sum(p[i]*t**i for i in range(4))
            require(val >= -h, "chord minimum")

def negative_inference_fixtures():
    r=F(1,16); delta=r*r
    model=delta**2/2
    actual=model+r*delta
    reject("omit finite-r edge-strip term", actual <= model)
    reject("bound omitted strip correction by same model power uniformly",
           r*delta/model <= 1)
    reject("positive parts always sum to 12lambda",
           positive(-5)+positive(1) == -4)
    # On each [2^-j,2^(-j+1)], integral ds/s >= 1/2.
    reject("finite untruncated model inverse second moment",
           sum(F(1,2) for _ in range(40)) <= 1)
    reject("finite untruncated actual inverse contribution",
           r*(delta**-1-1) <= r)
    reject("globally exhaust the unmarked model measure",
           12*8**3 <= 12)
    alpha1,alpha2=F(2),F(3)
    reject("count coefficient equals failure coefficient",
           alpha1+2*alpha2 == alpha1+alpha2)
    reject("omit dA=r dlambda", 4-2 == 3)
    reject("normalize by soft mass instead of full Z", 4+1-5 == 3)
    D=[F(0),F(2)];N=[F(1),F(3)]
    joint=sum(d*n for d,n in zip(D,N))/2
    factored=(sum(D)/2)*(sum(N)/2)
    reject("factor correlated determinant/norm expectation", joint == factored)
    pA,q=F(1,3),F(2,5)
    reject("joint contact density equals conditional t density", pA*q == q)
    H=F(17);Lam=H-1
    reject("determinant H3 integrated over lambda stays H3",
           H**3*(2*Lam) <= H**3)
    h=F(1,16);mu=1-h;err=F(3,8)
    reject("saddle margin alone certifies the older endpoint",
           (err < mu) == (err < min(mu,4*h)))
    reject("replace the chord endpoint margin 4h by mu", 4*h == mu)
    g=F(1,100)
    genuine=1+(g*g+144)/F(1)
    reject("a standalone gamma^-2 pole is necessary in the raw Hessian bound",
           genuine >= 1/(g*g))
    reject("alpha=1/4 makes jet L1 error vanish",
           1-4*F(1,4) > 0)
    reject("a fixed finite moment yields beta=1/2",
           balance(64)[1] == F(1,2))
    # f_zz(M)=-r; f_xzz=1 from M to 0 gives f_zz(0)=-r/2.
    endpoint=r;midpoint_lambda=F(1,2)
    reject("endpoint depth is the midpoint soft coordinate",
           endpoint == midpoint_lambda)
    eps=F(1,64);wrong_delta=F(1,8)
    # exact eps=delta^2. Endpoint near contribution is delta^2=eps,
    # away epsilon^2 delta^-4=1: the wrong splitting has no convergence.
    reject("sqrt epsilon balances the cubic endpoint margin",
           eps**2/wrong_delta**4 < F(1))
    reject("W/r4 perturbation has zero weight outside model typing",
           filtered(F(-6),0,-r,2)*filtered(F(6),0,-r,1) == 0)
    # Higher fixed Gaussian moments exist, but their constants are not uniform.
    gaussian20=1
    for i in range(1,11):
        gaussian20 *= 2*i-1
    reject("all moment constants can be replaced by the first moment constant",
           gaussian20 <= 1)
    raw_jet_tv=F(0)  # same raw jet law for both measures
    height_a={F(0):F(1)}; height_b={r:F(1)}
    moved_height_tv=sum(abs(height_a.get(x,0)-height_b.get(x,0))
                        for x in set(height_a)|set(height_b))
    reject("total variation of raw jets proves TV for a moved height atom",
           moved_height_tv <= raw_jet_tv)
    H,E,Rsec=False,False,False  # actual failure at an off-T point
    accepted_mismatch=(H != E)
    failure_mismatch=((not H) != Rsec)
    reject("accepted and failure mismatches agree outside model typing",
           accepted_mismatch == failure_mismatch)
    require(len(counterchecks) == 23, "all named counterchecks executed")

def main():
    cutoff_checks()
    determinant_and_shear_checks()
    scalar_integrals_and_constants()
    negative_inference_fixtures()
    print("C101 AUTHOR CONTROLS — finite exact algebra, not analytic acceptance")
    print("Python "+sys.version.split()[0])
    print("Exact controls: "+str(checks))
    print("False-inference fixtures rejected: "+str(len(counterchecks)))
    print("m=3: alpha=1/12 beta=1/4 w exponent=1/32 e exponent=7/8")
    print("Consumer: r^3*(alpha_1+alpha_2) + O(r^(13/4))")
    print("Fixed integer m=1..64: all 13 error powers and 7 cutoff powers verified")
    for name in counterchecks:
        print("REJECT: "+name)
    print("PASS_FINITE_CONTROLS; AUTHOR_SIDE/HOLD; no Gaussian/geometric theorem acceptance")

if __name__ == "__main__":
    main()
```

### controls.stdout

```text
C101 AUTHOR CONTROLS — finite exact algebra, not analytic acceptance
Python 3.12.14
Exact controls: 6859
False-inference fixtures rejected: 23
m=3: alpha=1/12 beta=1/4 w exponent=1/32 e exponent=7/8
Consumer: r^3*(alpha_1+alpha_2) + O(r^(13/4))
Fixed integer m=1..64: all 13 error powers and 7 cutoff powers verified
REJECT: omit finite-r edge-strip term
REJECT: bound omitted strip correction by same model power uniformly
REJECT: positive parts always sum to 12lambda
REJECT: finite untruncated model inverse second moment
REJECT: finite untruncated actual inverse contribution
REJECT: globally exhaust the unmarked model measure
REJECT: count coefficient equals failure coefficient
REJECT: omit dA=r dlambda
REJECT: normalize by soft mass instead of full Z
REJECT: factor correlated determinant/norm expectation
REJECT: joint contact density equals conditional t density
REJECT: determinant H3 integrated over lambda stays H3
REJECT: saddle margin alone certifies the older endpoint
REJECT: replace the chord endpoint margin 4h by mu
REJECT: a standalone gamma^-2 pole is necessary in the raw Hessian bound
REJECT: alpha=1/4 makes jet L1 error vanish
REJECT: a fixed finite moment yields beta=1/2
REJECT: endpoint depth is the midpoint soft coordinate
REJECT: sqrt epsilon balances the cubic endpoint margin
REJECT: W/r4 perturbation has zero weight outside model typing
REJECT: all moment constants can be replaced by the first moment constant
REJECT: total variation of raw jets proves TV for a moved height atom
REJECT: accepted and failure mismatches agree outside model typing
PASS_FINITE_CONTROLS; AUTHOR_SIDE/HOLD; no Gaussian/geometric theorem acceptance
```

### SOURCES.json

```json
{
  "object": "C101-PLANAR-K1-QUANTITATIVE-FAILURE-EXHAUSTION-20261003-v1",
  "created_utc": "2026-10-03",
  "author": "OpenAI/Codex root01a0adb2",
  "contributor": "OpenAI/Codex /root/c93_edge_integral_audit",
  "custody_claim": "5c1dc0ee-7ca9-4a65-8016-d41b59d8f6b2",
  "scientific_effect": "NONE",
  "review": "AUTHOR_SIDE/HOLD; root assigns fresh nonauthor review",
  "sources": [
    {
      "key": "C91",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963566666",
      "comment_id": 5963566666,
      "local_reading_copy": "source/C91.md",
      "bytes": 12433,
      "sha256": "74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa"
    },
    {
      "key": "C92",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963825788",
      "comment_id": 5963825788,
      "local_reading_copy": "source/C92.md",
      "bytes": 19567,
      "sha256": "6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a"
    },
    {
      "key": "C93",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5964167051",
      "comment_id": 5964167051,
      "local_reading_copy": "source/C93.md",
      "bytes": 15545,
      "sha256": "f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c"
    },
    {
      "key": "C94",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5964517708",
      "comment_id": 5964517708,
      "local_reading_copy": "source/C94.md",
      "bytes": 15407,
      "sha256": "0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c"
    },
    {
      "key": "C95",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5964938563",
      "comment_id": 5964938563,
      "local_reading_copy": "source/C95.md",
      "bytes": 16185,
      "sha256": "c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1"
    },
    {
      "key": "C96",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965141133",
      "comment_id": 5965141133,
      "local_reading_copy": "source/C96.md",
      "bytes": 7913,
      "sha256": "0758b5de8f4d9e4658ca3c6cf3e52c23d8e12f77999e9c3668ef0bedb15a05f5",
      "mathematical_suffix": {
        "bytes": 7657,
        "sha256": "7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a",
        "extraction": "Suffix beginning '# Designated maximin level equals the ordinary-superlevel H0 death', final LF retained; full native preface is 256 bytes."
      }
    },
    {
      "key": "C97",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965421543",
      "comment_id": 5965421543,
      "local_reading_copy": "source/C97.md",
      "bytes": 16098,
      "sha256": "acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57"
    },
    {
      "key": "C98",
      "authority": "native GitHub comment body",
      "url": "https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965738339",
      "comment_id": 5965738339,
      "local_reading_copy": "source/C98.md",
      "bytes": 15050,
      "sha256": "3ca1622197bf22cf71ab64f2938ecc0b022ed09487b691d50ae8d2ad1f46d198"
    },
    {
      "key": "P",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
      "git_blob": "dfed3b8d318a3ab1950957f393307733a4bef3f2",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
      "local_reading_copy": "source/P.md",
      "bytes": 40261,
      "sha256": "9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7"
    },
    {
      "key": "E1",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
      "git_blob": "213594d6ca6a86fb938110f4d166d9ce275a02d0",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md",
      "local_reading_copy": "source/E1.md",
      "bytes": 1782,
      "sha256": "bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028"
    },
    {
      "key": "E2",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "reviews/d1_section9_borel_repair_20260925/REPAIR.md",
      "git_blob": "fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_section9_borel_repair_20260925/REPAIR.md",
      "local_reading_copy": "source/E2.md",
      "bytes": 9062,
      "sha256": "845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f"
    },
    {
      "key": "REC",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
      "git_blob": "75da2597971510f843f8d90c743950cb8c177342",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md",
      "local_reading_copy": "source/REC.md",
      "bytes": 23312,
      "sha256": "451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da"
    },
    {
      "key": "CUB",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "frontiers/planar_cubic_cluster_20260929/PROOF.md",
      "git_blob": "bb446d08db8a944537a743ad550b88c1c2ad5758",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/frontiers/planar_cubic_cluster_20260929/PROOF.md",
      "local_reading_copy": "source/CUB.md",
      "bytes": 19889,
      "sha256": "117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0"
    },
    {
      "key": "ELDER",
      "authority": "immutable Git object",
      "repository": "d6g8k5htny-coder/Math-",
      "commit": "044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43",
      "path": "frontiers/local_elder_geometry_20260930/PROOF.md",
      "git_blob": "ef2aa57959ea9f721bbf2316ce94cf616c1c9113",
      "url": "https://github.com/d6g8k5htny-coder/Math-/blob/044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43/frontiers/local_elder_geometry_20260930/PROOF.md",
      "local_reading_copy": "source/ELDER.md",
      "bytes": 39722,
      "sha256": "f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b"
    }
  ],
  "total_full_native_reading_copy_bytes": 252226,
  "total_using_C96_mathematical_suffix_bytes": 251970,
  "retained_antecedents": [
    {
      "key": "C82",
      "comment_id": 5959920397,
      "consumed_via": [
        "C94",
        "C97"
      ],
      "mathematical_prefix_bytes": 11253,
      "sha256": "f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827"
    },
    {
      "key": "A1 correction",
      "comment_id": 5962385282,
      "consumed_via": [
        "C94"
      ]
    },
    {
      "key": "QS local premises",
      "comment_id": 5961415030,
      "consumed_via": [
        "C95",
        "C97"
      ]
    }
  ],
  "scope_excluded": [
    "compact-positive-k uniformity",
    "real-valued height/location mark TV",
    "once-counted replacement bars",
    "all-bars lifetime refinement",
    "intermediate/small-gap lane",
    "Conjecture7 closure",
    "repository application/CI/merge",
    "scientific promotion"
  ]
}
```

Review target: the WHOLE frozen proof §§0–9/Q1–Q38. Independently challenge cutoff-uniform Gaussian/normalizer constants; H^3/H^4 determinant losses; both strip substitutions and finite-r correction; selected value, rejected BOTH-margin and actual Hessian estimates; the full actual endpoint-residual tail versus model nonempty tail; Borel event/complement identification including T^c leakage; every cutoff exponent and fixed-m quantifier. Keep k=1, original source hypotheses, ordinary global H0, and all exclusion boundaries. Supporting contributor /root/c93_edge_integral_audit is author-side and excluded from review. Prior source authorship/review/coordination exposure is disclosed in the full proof. Human review NONE, personal reading PENDING, organizational independence0, scientific effectNONE. Author working scope is publication-ready; root's R17 custody/review claim remains active and no acceptance is claimed.
