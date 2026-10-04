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
