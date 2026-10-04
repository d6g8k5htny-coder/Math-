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
