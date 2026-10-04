# C97 independent checker and exact deterministic stdout

Paired evidence for the full review by OpenAI/Codex `/root/c95_fresh_review`, Dylan Roy — delegated AI review. This is supporting algebra/execution evidence, not an additional mathematical review. Personal reading PENDING; organizational independence0; scientific effectNONE.

Actual Python3.12.14 executions: normal, -O and -S, all exit0; stdout byte-identical. Per run11000 exact rational controls,214 rational rejected-saddle fixtures,21 rejected false-inference fixtures. Standard library only; no author/feasibility code imported. Finite tests do not establish Gaussian estimates, topology, H0 identification or uniform limits.

Save the first fence including its final newline as checker.py. It is10559 UTF-8 bytes, SHA256 `863f0f80edc144e394e5e23149d0d048ff5c09a802a3086cafcaaeeceee3c334`. The second fence's exact stdout including final newline is1737 UTF-8 bytes, SHA256 `41f5d16c4dd0ad6ed90b7d18b1ba9a41c37a9feb3ab5ad214813918dd12cdb72`.

## Full independent source

```python
"""Independent C97 rational controls; no author/feasibility/prior-checker imports.
Finite controls do not establish Gaussian, topology, H0 or uniform-limit facts.
"""
from fractions import Fraction as F
from itertools import product

counts = {}
negatives = []


def verify(group, value):
    if not value:
        raise RuntimeError('exact control failed: ' + group)
    counts[group] = counts.get(group, 0) + 1


def falsify(name, proposition):
    if proposition:
        raise RuntimeError('false inference survived: ' + name)
    negatives.append(name)


def cubic(u, z, psi, c, R):
    return 2*u**3-F(3,2)*u-F(1,2)-(psi+2*c*u)*z*z/48+R*z**3/3456


def jet(u,z,psi,c,R):
    pu=6*u*u-F(3,2)-c*z*z/24
    pz=-(psi+2*c*u)*z/24+R*z*z/1152
    det=12*u*(-(psi+2*c*u)/24+R*z/576)-(c*z/12)**2
    return pu,pz,det


# Build exact critical points from the conic, rather than a floating solver.
rejected = 0
for sigma,z,gap in product([F(i,4) for i in range(-12,17)],
                            [F(-24),F(-12),F(-3),F(3),F(12),F(24)],
                            [F(1,100),F(1,10),F(1),F(2)]):
    c=36*(sigma*sigma-1)/(z*z)
    psi=abs(c)+gap
    R=48*(psi-c*sigma)/z
    u=-sigma/2
    pu,pz,det=jet(u,z,psi,c,R)
    h=-cubic(u,z,psi,c,R)
    axial=u+F(1,2)
    kappa=(psi-c)/48
    rho2=3*axial*axial+kappa*z*z
    T3=2*axial**3-c*axial*z*z/24+R*z**3/3456
    verify('critical and Euler identities', pu==pz==0)
    verify('critical and Euler identities', det==(c-sigma*psi)/4)
    verify('critical and Euler identities', 3*T3==2*rho2 and h==rho2/3>0)
    verify('critical and Euler identities', -h==(sigma-1)/2-psi*z*z/144)
    coefficient=(R*R-64*c**3)/2304
    verify('finite branch polynomial', coefficient*z*z-psi*R*z/24+psi*psi-c*c==0)
    disc=(psi*R/24)**2-4*coefficient*(psi*psi-c*c)
    verify('finite branch polynomial', disc==c*c*(R*R+64*c*(psi*psi-c*c))/576)
    for t in [F(0),F(1,3),F(1),F(3,2),F(2)]:
        verify('exact chord restriction', cubic(-F(1,2)+t*axial,t*z,psi,c,R)==h*(2*t**3-3*t*t))
    if det<0 and 0<h<1:
        rejected += 1
        x=psi*z*z/144
        verify('rejected saddle radius', (sigma-1)**2<4*h and -1<sigma<3)
        verify('rejected saddle radius', 0<x<2 and abs(u)<F(3,2))
        verify('rejected saddle radius', psi*z*z<288)
        verify('rejected saddle radius', abs(2*u+F(1,2))<F(5,2) and psi*(2*z)**2<34**2)
        # Independent raw-coordinate reconstruction; Lambda is fixed per fixture.
        for gamma in [F(-2),F(1,2)]:
            lam=psi*gamma*gamma/24
            B=gamma*gamma*(1-c)/12
            C=(R*gamma**3-8*gamma**3+144*B*gamma)/576
            D=gamma*gamma-12*B
            J=8*gamma**3-144*B*gamma+576*C
            pj=1+abs(gamma)+abs(B)+abs(C)
            s=24*lam-gamma*gamma+12*B
            astar=96*lam
            ct=F(4,9)*astar**3+676*astar+F(728**2,36)
            ch=F(4,27)/ct
            verify('endpoint lower bound', D==c*gamma*gamma and J==R*gamma**3)
            verify('endpoint lower bound', 0<s<astar and abs(D)<=13*pj**2 and abs(J)<=728*pj**3)
            verify('endpoint lower bound', h>=ch*s**3/pj**6)
verify('nonempty rational coverage', rejected>0)

# Explicit exceptional branches, not an implicit genericity restriction.
c,psi,R=F(1),F(2),F(8)  # degree drop R^2=64 c^3
az=(R*R-64*c**3)/2304
z=(psi*psi-c*c)/(psi*R/24)
sigma=(psi-R*z/48)/c
verify('exceptional branches', az==0 and psi*R!=0 and z!=0)
verify('exceptional branches', jet(-sigma/2,z,psi,c,R)[:2]==(0,0))
falsify('quadratic division at degree drop', az!=0)
c,psi,R=F(-1),F(5,4),F(6)  # exact tangency
verify('exceptional branches', R*R+64*c*(psi*psi-c*c)==0)
z=(psi*R/24)/(2*(R*R-64*c**3)/2304)
sigma=(psi-R*z/48)/c
verify('exceptional branches', jet(-sigma/2,z,psi,c,R)==(0,0,0))
falsify('count tangency as nondegenerate saddle', jet(-sigma/2,z,psi,c,R)[2]<0)
for psi,R in product([F(1,8),F(1),F(3)],[F(-16),F(2),F(8)]):
    z=48*psi/R
    verify('exceptional branches', jet(-F(1,2),z,psi,0,R)==(0,0,-psi/4))
    verify('exceptional branches', cubic(-F(1,2),z,psi,0,R)==-16*psi**3/R**2)
verify('exceptional branches', jet(F(0),F(1),F(2),F(0),F(0))[1]!=0)

# Endpoint clearance is separate from saddle clearance.
h,mu=F(1,16),F(15,16)
endpoint_error=-F(1,2)
verify('two margins', abs(endpoint_error)<mu)
falsify('mu-only error ensures higher chord endpoint', 4*h+endpoint_error>0)
for h in [F(i,40) for i in range(1,40)]:
    mu=1-h
    eps=min(mu,4*h)/3
    verify('two margins', -h-eps>-1 and 4*h-eps>0)
    verify('two margins', min(mu/2,2*h)==min(mu,4*h)/2)
    for t in [F(i,10) for i in range(21)]:
        verify('two margins', h*(2*t**3-3*t*t)>=-h)
falsify('endpoint margin bounded below on rejected sector', 4*F(1,10**6)>=F(1,10))

# Rationalize sqrt(s), keeping the exact 1/sqrt(3) factor squared.
for gamma,lam,sroot,Bextra,C in product([F(-3),F(1,2)], [F(1),F(3)],
                                      [F(1,3),F(1),F(2)], [F(0)], [F(-2),F(0),F(4)]):
    s=sroot*sroot
    B=(s-24*lam+gamma*gamma)/12+Bextra
    D=gamma*gamma-12*B
    J=8*gamma**3-144*B*gamma+576*C
    psi=24*lam/gamma**2; c=D/gamma**2; R=J/gamma**3
    kappa=s/(48*gamma**2)
    # sqrt(3) tau from raw cancellation and from each original term.
    tau_scaled=F(2,3)+2*abs(D)/s+abs(J)/(6*sroot**3)
    term2=abs(c)/(24*kappa)
    # sqrt(3)/(3456*kappa^(3/2)) = abs(gamma)^3/(6*sroot^3).
    term3=abs(R)*abs(gamma)**3/(6*sroot**3)
    verify('tau chart cancellation', tau_scaled==F(2,3)+term2+term3)
    tau_sq=tau_scaled*tau_scaled/3
    numerator=F(4,9)*s**3+4*D*D*s+J*J/36
    verify('tau bound constants', tau_sq<=numerator/s**3)
    pj=1+abs(gamma)+abs(B)+abs(C)
    astar=48*(2*lam)
    ct=F(4,9)*astar**3+676*astar+F(728**2,36)
    verify('tau bound constants', numerator<=ct*pj**6 and 0<s<astar)
falsify('pointwise inverse chart at gamma zero', F(0)!=0)

# A rectangle containing every chord; its corner norm controls the rectangle.
for sqrtpsi,gamma in product([F(1,3),F(1),F(5)], [F(-4),F(-1,3),F(1,2),F(3)]):
    sqrt24lam=sqrtpsi*abs(gamma)
    rch=F(5,2)+3*(abs(gamma)+12)/sqrt24lam
    for u,z in product([F(-5,2),F(5,2)],[-34/sqrtpsi,34/sqrtpsi]):
        X=u-z/12; zz=z/gamma
        verify('raw radius corners', X*X+zz*zz<=rch*rch)
    verify('raw radius corners', F(17,6)<3 and 4*288<34**2)
    rho=3*(abs(gamma)+12)/sqrt24lam
    lam=sqrt24lam**2/24
    H=F(3,8)*(abs(gamma)+12)**2
    verify('radius event algebra', lam==H/rho**2)

for U,r in product([F(1,100),F(1,2),F(3)],[F(1,1000),F(1,5)]):
    # integrate s(48lambda-s)/16 in s then lambda, independently.
    lambda_integral_coefficient=(48**3/F(2)-48**3/F(3))/16
    leading=lambda_integral_coefficient*U**4/4
    remainder=r*48*U*U/2
    verify('actual radius integration', leading==288*U**4 and remainder==24*r*U*U)
    verify('actual radius integration', leading/12==24*U**4 and remainder/12==2*r*U*U)
falsify('drop B1 Jacobian as equality', F(288)==24)
r,rho=F(1,100),F(100)
falsify('remove actual radius residual', r*rho**-4<=rho**-8)

for d,astar,r in product([F(1,100),F(1,8),F(1,2)], [F(1),F(3)], [F(1,100),F(1,2)]):
    primitive=lambda s:-F(1,4)*s**-4-F(1,5)*r*s**-5
    exact=primitive(astar)-primitive(d)
    upper=d**-4/4+r*d**-5/5
    verify('endpoint integral primitives', 0<exact<upper)
    verify('endpoint integral primitives', exact==(d**-4-astar**-4)/4+r*(d**-5-astar**-5)/5)
    eps=d**3
    estimate=d*d+r*d+eps*eps*upper
    verify('endpoint optimized split', estimate==F(5,4)*d*d+F(6,5)*r*d)
falsify('inverse-six integrand has inverse-three primitive', F(1,4)*(F(1,2)**-4-1)==F(1,3)*(F(1,2)**-3-1))
r=F(1,100); d=r*r
falsify('drop finite-r typing strip', d*d/2+r*d<=d*d)
verify('correlated moment fixture', (F(1)*1+F(3)*9)/2 != ((F(1)+3)/2)*((F(1)+9)/2))
falsify('factor weight and norm moments', (F(1)*1+F(3)*9)/2 == ((F(1)+3)/2)*((F(1)+9)/2))

for mu,e0,d in product([F(1,20),F(1,3),F(9,10)],
                      [F(0),F(1,50),F(1,4),F(2)], [F(1,100),F(1,8)]):
    h=1-mu
    if e0>=min(mu/2,2*h):
        verify('event unions', e0>=mu/2 or e0>=2*h)
    if e0>=mu/2:
        verify('event unions', 0<mu<=2*d or e0>=d)

beta=F(1,16); margin=F(1,2); p=2; e=1-4*beta
ledger=[8*beta,1+4*beta,F(2,3)*e,1+e/3,margin,F(1),p*(e-margin)]
verify('complete exponent ledger', ledger==[F(1,2),F(5,4),F(1,2),F(5,4),F(1,2),F(1),F(1,2)])
verify('complete exponent ledger', min(ledger)+3==F(7,2) and F(7,2)-3==F(1,2))
verify('complete exponent ledger', 1-beta>0 and e>0)
falsify('p=1 retains claimed half exponent', (e-margin)>=F(1,2))
falsify('endpoint power improves to e', F(2,3)*e>=e)

# Positive sector witness with radicals eliminated by R^2=32 psi^3.
for Lambda in [F(1,100),F(1,3),F(1),F(20)]:
    lam=Lambda/2; psi=12*Lambda; gamma=F(1); B=F(1,12)
    Rsq=32*psi**3
    h=16*psi**3/Rsq
    aM=24*lam-gamma*gamma+12*B
    aS=24*lam+gamma*gamma-12*B
    verify('positive sector witness', aM==aS==12*Lambda>0 and h==F(1,2))
    verify('positive sector witness', -psi/4<0 and 0<lam<Lambda)
    verify('positive sector witness', aM*aS/16==9*Lambda**2)
    # J=8-144/12+576*(R+4)/576=R, for all R.
    verify('positive sector witness', 8-144*B+4==0)

for r in [F(1,16),F(1,64),F(1,256)]:
    mr,z0=F(2,7),F(3)
    zr=z0+r
    numerator=r**5*mr; fullZ=r*r*zr
    prob=numerator/fullZ
    verify('full normalizer ledger', prob==r**3*mr/zr)
    verify('full normalizer ledger', abs(prob-r**3*mr/z0)<=r**4*mr/z0**2)
    falsify('soft-layer renormalization '+str(r), numerator/numerator==prob)
    falsify('omit r-square normalizer '+str(r), numerator/zr==prob)
    loss=prob*r
    verify('mass subtraction', prob-loss==prob*(1-r))
r=F(1,256); sector=r**4; failure=sector/2
verify('uniform sector floor obstruction', failure<=r**3/F(16))
falsify('conditional rate without uniform sector floor', failure/sector<=F(1,16))
falsify('fixed-Lambda bounds allow Lambda=r^-1', F(100)**6/F(100)<1)

# Exact set identity behind R24; no claim that E union R exhausts T.
universe=set(range(8)); E={0,1}; Rsec={2,3,4}; H={0,2,5,7}
verify('limited sector union', (E|Rsec)&(H^E)==(E-H)|(Rsec&H))
verify('limited sector union', not E&Rsec)
falsify('union exhausts full domain', E|Rsec==universe)

print('C97 independent standard-library exact controls')
for name in sorted(counts):
    print(name+': '+str(counts[name]))
print('rational rejected-saddle fixtures: '+str(rejected))
print('positive controls: '+str(sum(counts.values())))
print('false-inference fixtures rejected: '+str(len(negatives)))
for name in negatives:
    print('REJECT '+name)
print('No finite test proves Gaussian estimates, covering topology, H0, or uniform limits.')
```

## Exact stdout in all three modes

```text
C97 independent standard-library exact controls
actual radius integration: 12
complete exponent ledger: 3
correlated moment fixture: 1
critical and Euler identities: 2784
endpoint integral primitives: 24
endpoint lower bound: 1284
endpoint optimized split: 12
event unions: 22
exact chord restriction: 3480
exceptional branches: 23
finite branch polynomial: 1392
full normalizer ledger: 6
limited sector union: 2
mass subtraction: 3
nonempty rational coverage: 1
positive sector witness: 16
radius event algebra: 12
raw radius corners: 60
rejected saddle radius: 856
tau bound constants: 72
tau chart cancellation: 36
two margins: 898
uniform sector floor obstruction: 1
rational rejected-saddle fixtures: 214
positive controls: 11000
false-inference fixtures rejected: 21
REJECT quadratic division at degree drop
REJECT count tangency as nondegenerate saddle
REJECT mu-only error ensures higher chord endpoint
REJECT endpoint margin bounded below on rejected sector
REJECT pointwise inverse chart at gamma zero
REJECT drop B1 Jacobian as equality
REJECT remove actual radius residual
REJECT inverse-six integrand has inverse-three primitive
REJECT drop finite-r typing strip
REJECT factor weight and norm moments
REJECT p=1 retains claimed half exponent
REJECT endpoint power improves to e
REJECT soft-layer renormalization 1/16
REJECT omit r-square normalizer 1/16
REJECT soft-layer renormalization 1/64
REJECT omit r-square normalizer 1/64
REJECT soft-layer renormalization 1/256
REJECT omit r-square normalizer 1/256
REJECT conditional rate without uniform sector floor
REJECT fixed-Lambda bounds allow Lambda=r^-1
REJECT union exhausts full domain
No finite test proves Gaussian estimates, covering topology, H0, or uniform limits.
```
