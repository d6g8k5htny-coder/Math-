# C98 independent checker and exact stdout

Paired supporting evidence for the full review by OpenAI/Codex `/root/c95_fresh_review`, Dylan Roy — delegated AI review. This is algebra/execution evidence, not an additional review. Personal reading PENDING; organizational independence 0; scientific effect NONE.

Actual Python 3.12.14: normal, -O and -S each exited 0; stdout byte-identical. Each run: 717 positive exact controls and 21 rejected false-inference fixtures. No author, feasibility or prior-checker code imported. Finite tests do not prove nullity, Gaussian inputs, topology or universal TV rates.

First fence, final LF included: checker.py, 9334 UTF-8 bytes, SHA256 `f42b2a8c090cfb1cbb0cc30da6517db150712997ffa9fe815a1c740e5a681f3a`.
Second fence, final LF included: stdout, 1859 UTF-8 bytes, SHA256 `9ddcf06779eab02446f29015ffff7d46c058022aeb15ff519b02490244184796`.

## Independent source

```python
"""C98 independent stdlib algebra/finite-measure controls, not universal proof.
No author, feasibility, prior-checker, or external source file is imported.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt

counts = {}
negatives = []


def check(group, proposition):
    if not proposition:
        raise RuntimeError('control failed: '+group)
    counts[group] = counts.get(group, 0)+1


def reject(name, false_proposition):
    if false_proposition:
        raise RuntimeError('false inference survived: '+name)
    negatives.append(name)


def sqrt_exact(v):
    if v < 0:
        raise ValueError('negative rational square')
    n,d=isqrt(v.numerator),isqrt(v.denominator)
    if n*n!=v.numerator or d*d!=v.denominator:
        raise ValueError('fixture is not a rational square')
    return Q(n,d)


def roots(a,b,c):
    if not a:
        return [] if not b else [-c/b]
    disc=b*b-4*a*c
    if disc<0:
        return []
    s=sqrt_exact(disc)
    return sorted(set([(-b-s)/(2*a),(-b+s)/(2*a)]))


def extras(c,psi,R):
    if not c:
        pairs=[] if not R else [(Q(1),48*psi/R),(Q(-1),48*psi/R)]
    else:
        zs=roots((R*R-64*c**3)/2304,-psi*R/24,psi*psi-c*c)
        pairs=[((psi-R*z/48)/c,z) for z in zs]
    result=[]
    for sigma,z in pairs:
        if not z:
            raise RuntimeError('extra root at zero')
        value=(sigma+1)/2-psi*z*z/144
        det=(c-sigma*psi)/4
        check('critical identities', sigma*sigma-c*z*z/36==1)
        check('critical identities', R*z==48*(psi-c*sigma))
        result.append((sigma,z,value,det))
    return result


def classify(c,psi,R):
    points=extras(c,psi,R)
    values=[v for _,_,v,det in points if det<0]
    # None encodes minus infinity, not zero.
    mu=max(values) if values else None
    negative=mu is None or mu<0
    sector=(psi>=2*c and R*R<=16*(psi-2*c)**2*(psi+c) and negative)
    check('exact selected-sector coverage', sector==negative)
    if negative:
        check('strict necessity', psi>2*c and R*R<16*(psi-2*c)**2*(psi+c))
    if mu==0:
        check('neutral inclusion', R*R==16*(psi-2*c)**2*(psi+c))
    return mu,points


# Rational parametrizations of the hyperbola/circle produce independent
# exact quadratic-root checks, including both signs of R and all finite roots.
for c,y,t in product([Q(1),Q(-1)],[Q(5,4),Q(2),Q(3),Q(6)],
                     [Q(1,5),Q(1,3),Q(1,2),Q(2,3),Q(3,4)]):
    psi=abs(c)*y
    if c>0:
        sigma=(1+t*t)/(1-t*t); z=12*t/(1-t*t)
    else:
        sigma=(1-t*t)/(1+t*t); z=12*t/(1+t*t)
    R=48*(psi-c*sigma)/z
    plus=classify(c,psi,R)
    minus=classify(c,psi,-R)
    check('reflection', plus[0]==minus[0])
for c,psi,R in [(Q(1),Q(5,4),Q(0)),(Q(1),Q(2),Q(0)),
                (Q(1),Q(3),Q(0)),(Q(1),Q(2),Q(8)),
                (Q(-1),Q(5,4),Q(0)),(Q(-1),Q(5,4),Q(6)),
                (Q(0),Q(1),Q(0)),(Q(0),Q(1),Q(2)),
                (Q(0),Q(1),Q(4)),(Q(0),Q(1),Q(8))]:
    # R0,c>0 may have irrational Z; choose y with rational y^2-1 below.
    if R==0 and c>0 and psi in [Q(2),Q(3)]:
        mu=-(psi-2)*(psi+1)**2/4
        check('R0 positive-c formula', (mu<0)==(psi>2))
    else:
        classify(c,psi,R)
mu,pts=classify(Q(-1),Q(5,4),Q(6))
check('tangency/no-saddle', mu is None and len(pts)==1 and pts[0][3]==0)
reject('tangency counted as saddle', pts[0][3]<0)
reject('empty saddle maximum equals zero', mu==Q(0))
mu,pts=classify(Q(1),Q(2),Q(8))
check('degree drop finite root', len(pts)==1)
reject('divide by quadratic coefficient on degree drop', (Q(8)**2-64)/2304!=0)

# Rational squared arc functions and derivative numerators; no radicals.
for y in [Q(5,4),Q(3,2),Q(2),Q(3),Q(5)]:
    for fraction in [Q(1,10),Q(1,3),Q(1,2),Q(9,10)]:
        sigma=1+fraction*(y-1)
        r2=64*(y-sigma)**2/(sigma*sigma-1)
        v=(sigma+1)*(2-y*(sigma-1))/4
        check('positive-c arc', 1<sigma<y and 1-y*sigma<0 and r2>0)
        if v<0:
            check('positive-c arc', y>2 and sigma>1+2/y)
            check('positive-c arc', r2<16*(y-2)**2*(y+1))
        sigma=-1/y+fraction*(1+1/y)
        r2=64*(y+sigma)**2/(1-sigma*sigma)
        v=(sigma+1)*(2-y*(1-sigma))/4
        check('negative-c arc', -1/y<sigma<1 and 1+y*sigma>0)
        if v<0:
            check('negative-c arc', sigma<1-2/y and r2<16*(y+2)**2*(y-1))
    rt2=64*(y*y-1); q2=16*(y+2)**2*(y-1)
    check('tangency gap', q2-rt2==16*y*y*(y-1)>0)
    star=1-2/y
    check('negative-c boundary', -1/y<star<1)
    check('negative-c boundary', 64*(y+star)**2/(1-star*star)==q2)
    if y>2:
        star=1+2/y
        check('positive-c boundary', 1<star<y)
        check('positive-c boundary', 64*(y-star)**2/(star*star-1)==16*(y-2)**2*(y+1))

def raw_polynomial(lam,gamma,B,C):
    D=gamma*gamma-12*B
    J=8*gamma**3-144*B*gamma+576*C
    return J*J-16*(24*lam-2*D)**2*(24*lam+D)


for lam,gamma,B,C in product([Q(-1),Q(0),Q(1,8)],
                            [Q(-2),Q(0),Q(1,3)],[Q(-1),Q(1,12)],[Q(-2),Q(0),Q(3)]):
    fp=raw_polynomial(lam,gamma,B,C+1)
    fm=raw_polynomial(lam,gamma,B,C-1)
    f=raw_polynomial(lam,gamma,B,C)
    check('raw polynomial leading coefficient', (fp-2*f+fm)/2==576**2)
    if gamma:
        D=gamma*gamma-12*B; J=8*gamma**3-144*B*gamma+576*C
        psi=24*lam/gamma**2; c=D/gamma**2; R=J/gamma**3
        check('raw neutral clearing', f==gamma**6*(R*R-16*(psi-2*c)**2*(psi+c)))

# This neutral-surface point is deliberately NOT mu0: psi<2c permits
# a below-designated boundary root while another saddle has positive margin.
c,psi,R=Q(1),Q(5,4),Q(9,2)
mu,pts=classify(c,psi,R)
lam=psi/24; gamma=Q(1); B=(1-c)/12; C=(R-8+144*B)/576
check('surface not equality', raw_polynomial(lam,gamma,B,C)==0 and mu>0)
reject('F0 implies mu0', mu==0)
# A genuinely neutral example, including R0 without division by R.
check('R0 neutral algebra', Q(0)==16*(Q(2)-2*Q(1))**2*(Q(2)+1))
reject('psi2c R0 belongs to negative sector', -(Q(2)-2)*(Q(2)+1)**2/4<0)

# Finite measure fixtures test B19-B21's exact algebra, not Gaussian laws.
def l1(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))


for q in [Q(1,8),Q(1,16),Q(1,32)]:
    r=q*q
    model=[Q(2,5),Q(3,5),Q(0)]  # last point is outside T
    actual=[model[0]+r,model[1]-r/2,r/2]
    mark=[1,0,0]
    flip=[q/10,q/20,r/2]
    joint=[]; target=[]
    for mass,m0,h,bad in zip(actual,model,mark,flip):
        check('joint fixture validity', 0<=bad<=mass)
        joint.extend([bad if h else mass-bad,mass-bad if h else bad])
        target.extend([Q(0) if h else m0,m0 if h else Q(0)])
    mismatch=sum(flip)
    check('Boolean total variation bound', l1(joint,target)<=2*mismatch+l1(actual,model))
    ar,a0=sum(joint),sum(target)
    normalized=[x/ar for x in joint]
    normalized0=[x/a0 for x in target]
    check('conditional normalization', l1(normalized,normalized0)<=l1(joint,target)/ar+abs(ar-a0)/ar)
    check('full-law rare scale', r**3*mismatch/r**3==mismatch)
    check('outside-T retained', r/2>0 and model[-1]==0)
    reject('model outside-T null means actual outside-T null '+str(r), actual[-1]==0)
    # Exact mark flip with unchanged jets saturates the factor2.
    one=[q,1-q]; zero=[Q(0),Q(1)]
    check('factor two necessary', l1(one,zero)==2*q)
    reject('omit factor two '+str(r), l1(one,zero)<=q)
    # Full weighted normalizer versus restricted layer normalizer.
    numerator=r**5*ar; fullZ=r*r*Q(3)
    probability=numerator/fullZ
    check('full normalizer', probability==r**3*ar/3)
    reject('replace full normalizer by layer mass '+str(r), numerator/numerator==probability)

# A singular atomic law on F0 disproves transferring model nullity alone.
atom_mass=Q(1)
reject('Lebesgue-null polynomial set is null for every law', atom_mass==0)
# Exact nullity supplies no neighborhood rate: uniform law on [-eps,eps].
eps=Q(1,10000)
neighborhood_mass=2*eps/(2*eps)
reject('nullity alone gives sqrt-eps neighborhood rate', neighborhood_mass<=Q(1,100))
# A continuous mark can move by eps and still have total variation norm2.
pointmass0=[Q(1),Q(0)]; pointmasseps=[Q(0),Q(1)]
reject('small location displacement implies small TV', l1(pointmass0,pointmasseps)<=eps)

universe=set(range(7)); E={0,1}; Rsec={2,3}; outside={4,5}; neutral={6}
H={0,2,4}
mis=universe&(H^E)
check('full layer set ledger', mis<=(E-H)|(Rsec&H)|outside|neutral)
reject('sector comparison covers T-complement without charge', mis<=(E-H)|(Rsec&H))
check('rate ledger', Q(7,2)-3==Q(1,2) and Q(4)-3==1)
reject('full-layer mismatch is O(r4) from given bounds', Q(7,2)>=4)

# Positive masses bound the limiting ratio away from both0 and1.
for me,mr in product([Q(1,10),Q(1,3),Q(2)],[Q(1,8),Q(1,2),Q(3)]):
    total=me+mr; ratio=me/total
    check('positive mass partition', 0<ratio<1 and 1-ratio==mr/total)
    check('positive mass partition', me<=total and mr<=total)
reject('limiting conditional probability is one', Q(2,5)==1)
reject('conditional target normalized by z0 instead of mLambda', Q(2,5)/Q(3)==Q(2,5))

print('C98 independent exact algebra and finite-measure controls')
for name in sorted(counts):
    print(name+': '+str(counts[name]))
print('positive controls: '+str(sum(counts.values())))
print('false-inference fixtures rejected: '+str(len(negatives)))
for name in negatives:
    print('REJECT '+name)
print('Finite controls do not prove nullity, Gaussian inputs, topology, or universal TV rates.')
```

## Exact stdout in all three modes

```text
C98 independent exact algebra and finite-measure controls
Boolean total variation bound: 3
R0 neutral algebra: 1
R0 positive-c formula: 2
conditional normalization: 3
critical identities: 340
degree drop finite root: 1
exact selected-sector coverage: 91
factor two necessary: 3
full layer set ledger: 1
full normalizer: 3
full-law rare scale: 3
joint fixture validity: 9
negative-c arc: 28
negative-c boundary: 10
neutral inclusion: 3
outside-T retained: 3
positive mass partition: 18
positive-c arc: 30
positive-c boundary: 4
rate ledger: 1
raw neutral clearing: 36
raw polynomial leading coefficient: 54
reflection: 40
strict necessity: 23
surface not equality: 1
tangency gap: 5
tangency/no-saddle: 1
positive controls: 717
false-inference fixtures rejected: 21
REJECT tangency counted as saddle
REJECT empty saddle maximum equals zero
REJECT divide by quadratic coefficient on degree drop
REJECT F0 implies mu0
REJECT psi2c R0 belongs to negative sector
REJECT model outside-T null means actual outside-T null 1/64
REJECT omit factor two 1/64
REJECT replace full normalizer by layer mass 1/64
REJECT model outside-T null means actual outside-T null 1/256
REJECT omit factor two 1/256
REJECT replace full normalizer by layer mass 1/256
REJECT model outside-T null means actual outside-T null 1/1024
REJECT omit factor two 1/1024
REJECT replace full normalizer by layer mass 1/1024
REJECT Lebesgue-null polynomial set is null for every law
REJECT nullity alone gives sqrt-eps neighborhood rate
REJECT small location displacement implies small TV
REJECT sector comparison covers T-complement without charge
REJECT full-layer mismatch is O(r4) from given bounds
REJECT limiting conditional probability is one
REJECT conditional target normalized by z0 instead of mLambda
Finite controls do not prove nullity, Gaussian inputs, topology, or universal TV rates.
```
