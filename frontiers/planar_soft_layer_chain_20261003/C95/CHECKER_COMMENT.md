# C95 fresh helper's independent controls — complete source and exact stdout

This accompanies the [full named mathematical review5965062739](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965062739) by OpenAI/Codex `/root/c95_fresh_review`. It is not another review or acceptance vote. The coordinating root only relays/verifies publication artifacts and receives zero C95 mathematical acceptance credit.

Target: C95 native5964938563, 16185 UTF-8 bytes, SHA256 `c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1`.
Full helper review: 25080 UTF-8 bytes, SHA256 `350be6dc7699b7fc377074e1217937ceb53022f2de5d3cdb9c85f499d35bcaf6`; exact native readback verified.

The helper independently authored the following Python-standard-library checker without C95 author code or prior-checker reuse. Actual Python3.12.14 normal, `-O` and `-S` runs each exited0, with9270 positive exact controls and22 rejected false-inference fixtures; stdout was byte-identical. These are repeated runs of one suite, not independent votes. Coordinator replay of the supplied artifact in the same three modes matched the code/output identities and counts; that is execution/custody verification, not independent mathematical authorship.

Checker10566 UTF-8 bytes, SHA256 `179d64b556b337ddf966ba5f4f274d59910a6c045a242b26fff957f3167951d2`.
Each stdout1691 UTF-8 bytes, SHA256 `484e9d61c77fcd6394ad97cae20e628e4ccb6c3163d7ff900fdd4ee0836c37f5`.
The final newline inside each fence is included in these identities. Explicit checks survive optimization.

## Complete independently authored checker

```python
"""Fresh C95 exact diagnostic. Stdlib only; no imported proof/checker files.

This does not prove compact separation, covering-space lifting, Gaussian
estimates, or uniform asymptotic assertions. Those require written reasoning.
Checks deliberately raise exceptions rather than using optimizable asserts.
"""
from fractions import Fraction as Q
from itertools import product

counts = {}
rejections = []


def check(section, condition):
    if not condition:
        raise RuntimeError('failed exact control: ' + section)
    counts[section] = counts.get(section, 0) + 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError('false inference escaped: ' + name)
    rejections.append(name)


def A(u):
    return 2 * (u + Q(1, 2)) ** 2 * (u - 1)


def P(u, z, psi, c, R):
    return A(u) - (psi + 2*c*u)*z*z/48 + R*z**3/3456


def derivatives(u, z, psi, c, R):
    pu = 6*u*u-Q(3, 2)-c*z*z/24
    pz = -(psi+2*c*u)*z/24+R*z*z/1152
    huu, huz, hzz = 12*u, -c*z/12, -(psi+2*c*u)/24+R*z/576
    return pu, pz, huu, huz, hzz


def raw(X, z, lam, gamma, B, C):
    return (2*X**3-Q(3, 2)*X-Q(1, 2)
            +gamma*(X*X-Q(1, 4))*z/2-lam*z*z/2+B*X*z*z/2+C*z**3/6)


def mass(a, x):
    return Q(0) if x <= a else x**3/3-a*a*x+2*a**3/3


a0, b0, k0 = Q(599,250), Q(277,250), Q(256,125)
K = b0+k0*a0
switch = a0/K
check('G1-G3 constants', K == Q(187969,31250))
check('G1-G3 constants', switch == Q(74875,187969))
check('G1-G3 constants', 1-k0*switch == b0/K == Q(34625,187969))
check('G1-G3 constants', 0 < switch < 1/k0 < Q(1,2))
check('G1-G3 constants', 3*Q(128,125)**2-Q(3,4) == Q(149733,62500) < a0)
check('G1-G3 constants', K < Q(121,20))
check('G1-G3 constants', 144*Q(121,20) < Q(148,5)**2 < 30**2)
check('G1-G3 constants', 48*Q(121,20) < Q(171,10)**2)
for n in range(1,1000):
    omega = Q(n,2000)
    if omega <= switch:
        check('piecewise bound', 1-k0*omega > 0)
        check('piecewise bound', b0/(1-k0*omega) <= K)
    else:
        check('piecewise bound', a0/omega <= K)
    check('piecewise bound', a0/omega > 0)
reject('unsafe reciprocal at 49/100', b0/(1-k0*Q(49,100)) >= 0)
reject('reciprocal defined at 125/256', 1-k0*Q(125,256) != 0)
check('old-domain witnesses', 1-k0*Q(49,100) == Q(-11,3125))
# Independent admissibility of the unsafe-domain point at R=0.
c, psi, eta = Q(49,100), Q(1), Q(1,1000)
uc = -psi/(2*c)
mu = A(uc)+1
tau_s_sq = Q(4,27)*(1+3*c/(psi+c))**2
tau_m_sq = Q(4,27)*(1+3*c/(psi-c))**2
check('old-domain witnesses', 0 < eta < min(-mu,Q(2,125)/tau_s_sq,Q(1,8)/tau_m_sq,1))
reject('literal old minimum bounds F(M)', min(a0/c,b0/(1-k0*c)) >= 1+eta)

m = Q(1,1000)
check('sharpness admissibility', 64 < 75)  # 8/(6 sqrt(3)) < 5/6
check('sharpness admissibility', Q(72,3125)>m and Q(9,50)>m)
previous = Q(0)
for n in range(100,500):
    t = 1-Q(1,n)
    H = 3*t*t-2*t**3
    eta = (1+m)*H-1
    height_sq = 144*t*t*(1+m)/(1+eta)
    check('G4-G6 first root', 0 < eta < m and 0 < t < 1)
    check('G4-G6 first root', 6*t*(1-t)>0)
    check('G4-G6 first root', height_sq == 144/(3-2*t) < 144)
    check('G4-G6 first root', height_sq > previous)
    previous = height_sq
    # The scaled restriction substitutes Z=t Zs, R Zs=48,
    # Zs^2=144(1+m), without numerically approximating a radical.
    restricted = -Q(3)*(1+m)*t*t+2*(1+m)*t**3
    check('G4-G6 first root', restricted == -1-eta)
    check('G4-G6 first root', -(1+m) < -1-eta)
reject('saddle belongs to strict trap', -(1+m)>-1-m/2)
reject('universal sharp constant 11', previous <= 11**2)
q = Q(11999,1000)
t = 1-Q(1,1000000)
reject('universal sharp constant 11.999', 144/(3-2*t) <= q*q)

for a, x in product([Q(i,3) for i in range(10)], [Q(i,7) for i in range(1,40)]):
    value = mass(a,x)
    check('G7-G8 typed integral', 0 <= value <= x**3/3)
    check('G7-G8 typed integral', value == (0 if x<=a else (x-a)**2*(x+2*a)/3))
    if x>a:
        primitive = lambda v: v**3/3-a*a*v
        check('G7-G8 typed integral', value == primitive(x)-primitive(a))
for gamma, rho, a in product([Q(-3),Q(-1,2),Q(1,10),Q(2)], [Q(1,3),Q(2),Q(7)], [Q(0),Q(1),Q(100)]):
    x = 25*(abs(gamma)+12)**2/(4*gamma*gamma*rho*rho)
    bound = Q(25,4)**3*(abs(gamma)+12)**6/(3*rho**6)
    check('G7-G8 cancellation', gamma**6*x**3/3 == bound)
    check('G7-G8 cancellation', gamma**6*mass(a,x)<=bound)
reject('reversed primitive equals empty integral', mass(Q(2),Q(1)) == Q(1,3)-4+Q(16,3))
gamma, rho = Q(1,10), Q(1)
x = 25*(gamma+12)**2/(4*gamma*gamma)
reject('omit gamma-six weight cancellation', x**3/3 <= Q(25,4)**3*(gamma+12)**6/3)

# Exact rational substitutions exercise the polynomial identities without
# numerical tolerances. Their universal proof is the written derivation.
for u,z,psi,c,R in product([Q(-2),Q(-1,2),Q(1,2),Q(3,2)],
                          [Q(-3),Q(0),Q(2)], [Q(2)], [Q(-1),Q(0),Q(1)], [Q(-4),Q(0),Q(5)]):
    theta=psi+2*c*u
    pu,pz,huu,huz,hzz=derivatives(u,z,psi,c,R)
    check('retained cubic identities', pz==z*(R*z-48*theta)/1152)
    check('retained cubic identities', P(u,z,psi,c,R)-A(u)+theta*z*z/144 == z*z*(R*z-48*theta)/3456)
    check('retained cubic identities', P(u,z,psi,c,R)-A(u)+theta*z*z/48 == R*z**3/3456)
    check('axis identity', A(u)+1 == 2*(u-Q(1,2))**2*(u+1))
    if R:
        zl=48*theta/R
        pu,pz,huu,huz,hzz=derivatives(u,zl,psi,c,R)
        phi2=12*u-384*c*c*theta/(R*R)
        check('critical-line identity', P(u,zl,psi,c,R)==A(u)-16*theta**3/R**2)
        check('critical-line identity', phi2*hzz==huu*hzz-huz*huz)

for sigma,z in product([Q(-2),Q(-1),Q(-1,2),Q(0),Q(1),Q(2)], [Q(-12),Q(6),Q(24)]):
    c=36*(sigma*sigma-1)/(z*z)
    psi=abs(c)+1
    R=48*(psi-c*sigma)/z
    u=-sigma/2
    pu,pz,huu,huz,hzz=derivatives(u,z,psi,c,R)
    check('CUB guarded extras', pu==pz==0)
    check('CUB guarded extras', P(u,z,psi,c,R)==(sigma-1)/2-psi*z*z/144)
    det=huu*hzz-huz*huz
    check('CUB guarded extras', det==(c-sigma*psi)/4)
    if det>0:
        check('CUB guarded extras', sigma<0 and huu>0)

for n in range(-199,200):
    om=Q(n,200)
    for sign in [-1,1]:
        numerator=1+sign*om
        denominator=1+sign*om+3*abs(om)
        check('ellipse box ratios', numerator>0 and denominator>0)
        check('ellipse box ratios', numerator<=denominator**2)
check('ellipse box constants', Q(27,100)/3==Q(3,10)**2)
check('ellipse box constants', Q(27,16)/3==Q(3,4)**2)
check('ellipse box constants', 48*Q(27,100)==Q(324,25) and 48*Q(27,16)==81)
check('ellipse box constants', -1-Q(2,9)*Q(27,250)>Q(-5,4))

for gamma,B,C,lam in product([Q(-2),Q(-1,3),Q(1,2),Q(3)], [Q(-1),Q(1,12)], [Q(-2),Q(0),Q(1)], [Q(1,4),Q(2)]):
    psi=24*lam/gamma**2
    c=(gamma**2-12*B)/gamma**2
    R=(8*gamma**3-144*B*gamma+576*C)/gamma**3
    for X,z in product([Q(-1),Q(0),Q(3,2)], [Q(-2),Q(0),Q(1)]):
        check('actual raw identity', raw(X,z,lam,gamma,B,C)==P(X+gamma*z/12,gamma*z,psi,c,R))
    aM,aS=24*lam-gamma**2+12*B,24*lam+gamma**2-12*B
    check('actual typing algebra', aM+aS==48*lam)
    check('actual typing algebra', gamma**2*(psi-c)==aM and gamma**2*(psi+c)==aS)
    if aM>0 and aS>0:
        for ai in [aM,aS]:
            kappa=ai/(48*gamma**2)
            check('Hessian transfer', Q(1,3)+(Q(1,144)+1/gamma**2)/kappa==Q(1,3)*(1+(gamma**2+144)/ai))
        check('joint-density Jacobian', (aM*aS/16)*(gamma**2/24)==gamma**6*(psi**2-c**2)/384)
reject('pointwise chart at gamma zero', Q(0)!=0)

# Path-value fixtures test scaling, not planar separation or path lifting.
paths = [[Q(0),Q(-1),Q(4)], [Q(0),Q(-2),Q(3)], [Q(0),Q(-3,2),Q(2)]]
dg=max(map(min,paths))
for b,r in product([Q(-4),Q(0),Q(5,2)],[Q(1,16),Q(1,3),Q(2)]):
    transformed=[[b+r**3*v for v in p] for p in paths]
    check('positive affine maximin', max(map(min,transformed))==b+r**3*dg)
    check('positive affine maximin', all(p[-1]>b for p in transformed))
reject('negative scale preserves maximin', max(min(-v for v in p) for p in paths)==-dg)
reject('drop higher-endpoint restriction', max(dg,Q(0))==dg)
for gap in [Q(1,100),Q(1,3),Q(2)]:
    eps=gap/3
    check('strict witness robustness', gap-eps>0)

for Lambda in [Q(1,100),Q(1,3),Q(1),Q(12)]:
    lam=Lambda/2; gamma=Q(1); B=(1+6*Lambda)/12; C=(1+18*Lambda)/144
    J=8*gamma**3-144*B*gamma+576*C
    psi,c=24*lam,1-12*B
    aM,aS=24*lam-gamma**2+12*B,24*lam+gamma**2-12*B
    check('positive sector witness', J==0 and psi==12*Lambda and c==-6*Lambda)
    check('positive sector witness', aM==18*Lambda and aS==6*Lambda)
    check('positive sector witness', 64*c*(psi**2-c**2)==-41472*Lambda**3<0)
    check('positive sector witness', 0<lam<Lambda and psi>abs(c) and psi>2*c)
    check('positive sector witness', aM*aS/16==Q(27,4)*Lambda**2>0)
    astar=48*Lambda
    cstar=Q(3,250)/astar**2
    check('tolerance floor', cstar*astar**2==Q(3,250)<Q(27,512))

beta,delta_power,p=Q(1,16),Q(1,2),2
e=1-4*beta
ledger=[8*beta,1+4*beta,e,1+e/2,delta_power,Q(1),p*(e-delta_power),2-4*beta]
check('rate ledger', ledger==[Q(1,2),Q(5,4),Q(3,4),Q(11,8),Q(1,2),Q(1),Q(1,2),Q(7,4)])
check('rate ledger', min(ledger)+3==Q(7,2))
check('rate ledger', Q(7,2)-3==Q(1,2) and 1-beta>0)
for r in [Q(1,16),Q(1,64),Q(1,256)]:
    z0=Q(2); zr=z0+r; sector_mass=Q(3,7)
    unweighted_numerator=r**5*sector_mass
    fullZ=r*r*zr
    probability=unweighted_numerator/fullZ
    check('full actual normalization', probability==r**3*sector_mass/zr)
    check('full actual normalization', abs(probability-r**3*sector_mass/z0)<=r**4*sector_mass/(z0*z0))
    fail=r**4*sector_mass/(2*zr)
    check('event subtraction', (probability-fail)/probability==1-r/2)
    reject('restricted normalizer at r='+str(r), unweighted_numerator/unweighted_numerator==probability)
    reject('omit full normalizer r-square at r='+str(r), unweighted_numerator/zr==probability)
reject('r4 dominates r7/2', Q(1,256)**4 >= Q(1,256)**3*Q(1,16))
r=Q(1,256); rho=Q(256)
reject('discard actual radius residual', r*rho**-4 <= rho**-8)
sector=r**4; fail=sector/2
check('uniform positivity obstruction', fail<=r**3*Q(1,16))
reject('conditional convergence without sector floor', fail/sector <= Q(1,16))
reject('unconditional good probability tends to one', r**3*Q(3,7)/(2+r)>Q(1,2))
reject('growing Lambda inherits fixed constants', (1/r)**8*r**Q(1,1) < 1)

print('C95 fresh stdlib exact controls')
for name in sorted(counts):
    print(name + ': ' + str(counts[name]))
print('positive controls: ' + str(sum(counts.values())))
print('false-inference controls rejected: ' + str(len(rejections)))
for name in rejections:
    print('REJECT ' + name)
print('No finite-control claim proves topology, Gaussian inputs, or uniform limits.')
```

## Exact stdout in all three modes

```text
C95 fresh stdlib exact controls
CUB guarded extras: 63
G1-G3 constants: 8
G4-G6 first root: 2400
G7-G8 cancellation: 72
G7-G8 typed integral: 1068
Hessian transfer: 66
actual raw identity: 432
actual typing algebra: 96
axis identity: 108
critical-line identity: 144
ellipse box constants: 4
ellipse box ratios: 1596
event subtraction: 3
full actual normalization: 6
joint-density Jacobian: 33
old-domain witnesses: 2
piecewise bound: 2794
positive affine maximin: 18
positive sector witness: 20
rate ledger: 3
retained cubic identities: 324
sharpness admissibility: 2
strict witness robustness: 3
tolerance floor: 4
uniform positivity obstruction: 1
positive controls: 9270
false-inference controls rejected: 22
REJECT unsafe reciprocal at 49/100
REJECT reciprocal defined at 125/256
REJECT literal old minimum bounds F(M)
REJECT saddle belongs to strict trap
REJECT universal sharp constant 11
REJECT universal sharp constant 11.999
REJECT reversed primitive equals empty integral
REJECT omit gamma-six weight cancellation
REJECT pointwise chart at gamma zero
REJECT negative scale preserves maximin
REJECT drop higher-endpoint restriction
REJECT restricted normalizer at r=1/16
REJECT omit full normalizer r-square at r=1/16
REJECT restricted normalizer at r=1/64
REJECT omit full normalizer r-square at r=1/64
REJECT restricted normalizer at r=1/256
REJECT omit full normalizer r-square at r=1/256
REJECT r4 dominates r7/2
REJECT discard actual radius residual
REJECT conditional convergence without sector floor
REJECT unconditional good probability tends to one
REJECT growing Lambda inherits fixed constants
No finite-control claim proves topology, Gaussian inputs, or uniform limits.
```

Finite controls do not prove topology, Gaussian estimates, path lifting or uniform limits; the named helper's written argument and retained source hypotheses supply those premises. Original A2v1 remains AMEND. The complete G1–G18 technical verdict does not identify an H0 persistence event, all-bar converse, rejected-side/chord, regional collision, intermediate/coarea or global density/remainder.

The distinct review pickup5964966168 is COMPLETE/RELEASED with this paired substantive delivery. Author claim `f4597887-706f-4b57-b493-475875214c5f` / WE623 is untouched. Same-provider organizational independence0; Dylan personal reading PENDING; scientific effect NONE. No branch/source edit, incorporation, CI, merge, formal or human acceptance is claimed.
