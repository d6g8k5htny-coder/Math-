#!/usr/bin/env python3
"""Bounded exact author controls for C107; not a proof or acceptance checker."""
from fractions import Fraction as F
from dataclasses import dataclass
from itertools import product
from math import factorial
import sys


class Failure(Exception):
    pass


counts = {}
mutants = []


def require(ok, label):
    if not ok:
        raise Failure(label)


def check(ok, group):
    require(ok, group)
    counts[group] = counts.get(group, 0) + 1


def reject(name, operation):
    try:
        operation()
    except Failure:
        mutants.append(name)
    else:
        raise Failure("mutant survived: " + name)


# Bivariate physical polynomials, keyed by (t degree, z degree).
def pvalue(p, t, z, dt=0, dz=0):
    out = F(0)
    for (i, j), a in p.items():
        if i >= dt and j >= dz:
            out += a * F(factorial(i), factorial(i-dt)) * F(
                factorial(j), factorial(j-dz)) * t**(i-dt) * z**(j-dz)
    return out


def endpoint_poly(data, r, mutant=None):
    a, b, c, d, e, g = map(F, data)
    return {
        (0, 0): a - (0 if mutant == "constant" else r*r*c/8),
        (1, 0): b - (0 if mutant == "linear" else r*r*d/24),
        (2, 0): c/2, (3, 0): d/6, (0, 1): e, (1, 1): g,
    }


def endpoint_obs(p, r):
    z = F(0)
    if r == 0:
        return tuple(pvalue(p,z,z,i,j) for i,j in
                     ((0,0),(1,0),(2,0),(3,0),(0,1),(1,1)))
    a, c = -r/2, r/2
    fa, fc = pvalue(p,a,z), pvalue(p,c,z)
    da, dc = pvalue(p,a,z,1), pvalue(p,c,z,1)
    za, zc = pvalue(p,a,z,0,1), pvalue(p,c,z,0,1)
    return ((fa+fc)/2,(fc-fa)/r,(dc-da)/r,
            6*(da+dc-2*(fc-fa)/r)/(r*r),(za+zc)/2,(zc-za)/r)


def witness_poly(data, delta, mutant=None):
    a, b, c, d, h, w = map(F, data)
    correction = 0 if mutant == "quadratic" else 6*delta*w
    cubic = 2*w if mutant == "sign" else -2*w
    return {(0,0):h,(1,0):a,(0,1):b,(2,0):(c+correction)/2,
            (3,0):cubic,(1,1):d}


def witness_obs(p, delta, contact=F(-1,12)):
    z = F(0)
    if delta == 0:
        return (pvalue(p,z,z,1),pvalue(p,z,z,0,1),
                pvalue(p,z,z,2),pvalue(p,z,z,1,1),pvalue(p,z,z),
                contact*pvalue(p,z,z,3))
    g0 = (pvalue(p,z,z,1),pvalue(p,z,z,0,1))
    g1 = (pvalue(p,delta,z,1),pvalue(p,delta,z,0,1))
    y0, y1 = pvalue(p,z,z),pvalue(p,delta,z)
    return (*g0,(g1[0]-g0[0])/delta,(g1[1]-g0[1])/delta,y0,
            (y1-y0-delta*(g0[0]+g1[0])/2)/delta**3)


def basis(n):
    return [tuple(F(int(i==j)) for i in range(n)) for j in range(n)]


def controls_observations():
    data = basis(6) + [(F(2),F(-3),F(5),F(7),F(-11),F(13))]
    for r, a in product((F(0),F(1,2),F(1,8),F(1,64)), data):
        check(endpoint_obs(endpoint_poly(a,r),r)==a,"endpoint_inverse")
        check(witness_obs(witness_poly(a,r),r)==a,"witness_inverse")
    r=F(1,8)
    for name, index in (("constant",2),("linear",3)):
        a=basis(6)[index]
        reject("endpoint_"+name+"_correction", lambda a=a,name=name:
               require(endpoint_obs(endpoint_poly(a,r,name),r)==a,"U inverse"))
    a=basis(6)[5]
    for name in ("quadratic","sign"):
        reject("witness_"+name, lambda name=name:
               require(witness_obs(witness_poly(a,r,name),r)==a,"V inverse"))
    reject("contact_D_wrong_constant",
           lambda: require(witness_obs(witness_poly(a,0),0,F(-1,6))==a,
                           "contact D"))


def hermite(f0, f1, d0, d1, y0, y1, h, mutant=False):
    a3 = (d1+d0)/h**2 - (1 if mutant else 2)*(f1-f0)/h**3
    a2 = 3*(f1-f0)/h**2 - (2*d0+d1)/h
    return (f0,d0,a2,a3,y0,(y1-y0)/h)


def hpoly(c):
    return dict(zip(((0,0),(1,0),(2,0),(3,0),(0,1),(1,1)),c))


def controls_hermite():
    for m,h in product(range(9),(F(1,2),F(1,16),F(1,256))):
        p={(m,0):F(1),(m,1):F(2)}
        f0,f1=pvalue(p,0,0),pvalue(p,h,0)
        d0,d1=pvalue(p,0,0,1),pvalue(p,h,0,1)
        y0,y1=pvalue(p,0,0,0,1),pvalue(p,h,0,0,1)
        c=hermite(f0,f1,d0,d1,y0,y1,h)
        q=hpoly(c)
        for t,dt,dz in product((F(0),h),range(2),range(2)):
            if dt+dz <= 1:
                check(pvalue(p,t,0,dt,dz)==pvalue(q,t,0,dt,dz),
                      "hermite_jet_match")
        integral_a3=F(0) if m<3 else (m-2)*h**(m-3)
        integral_g2=F(0) if m<2 else m*h**(m-1)
        check(c[3]==integral_a3,"hermite_integral_cancellation")
        check(c[2]==integral_g2/(2*h)-F(3,2)*h*c[3],
              "hermite_integral_cancellation")
        integral_mixed=F(0) if m==0 else 2*h**m
        check(c[5]==integral_mixed/h,"hermite_integral_cancellation")
    q=hpoly(hermite(F(0),F(1),F(0),F(3),F(0),F(0),F(1),True))
    reject("hermite_cubic_difference_factor",
           lambda: require(pvalue(q,1,0)==1 and pvalue(q,1,0,1)==3,
                           "Hermite endpoint"))


# Exact Gaussian-rational complex numbers and two-variable Laurent polynomials.
@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def of(x):
        return x if isinstance(x,Q) else Q(F(x),F(0))

    def __add__(self, other):
        o=Q.of(other)
        return Q(self.re+o.re,self.im+o.im)
    __radd__=__add__

    def __neg__(self):
        return Q(-self.re,-self.im)

    def __sub__(self,other):
        return self+-Q.of(other)

    def __rsub__(self,other):
        return Q.of(other)+-self

    def __mul__(self,other):
        o=Q.of(other)
        return Q(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__

    def inv(self):
        n=self.re**2+self.im**2
        return Q(self.re/n,-self.im/n)

    def __truediv__(self,other):
        return self*Q.of(other).inv()

    def __rtruediv__(self,other):
        return Q.of(other)*self.inv()

    def __pow__(self,n):
        if n<0:
            return self.inv()**(-n)
        out=Q(F(1))
        for _ in range(n):
            out=out*self
        return out

    def conj(self):
        return Q(self.re,-self.im)


ZERO=Q()
ONE=Q(F(1))
IM=Q(F(0),F(1))


def lclean(p):
    return {n:Q.of(a) for n,a in p.items() if Q.of(a)!=ZERO}


def ladd(*polys):
    out={}
    for p in polys:
        for n,a in p.items():
            out[n]=out.get(n,ZERO)+a
    return lclean(out)


def lscale(p,a):
    return lclean({n:Q.of(a)*b for n,b in p.items()})


def lmul(p,q):
    out={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            n=(i+k,j+l)
            out[n]=out.get(n,ZERO)+a*b
    return lclean(out)


def lpow(p,n):
    out={(0,0):ONE}
    for _ in range(n):
        out=lmul(out,p)
    return out


def leval(p,point,der=(0,0)):
    out=ZERO
    for (i,j),a in p.items():
        out+=a*(IM*i)**der[0]*(IM*j)**der[1]*point[0]**i*point[1]**j
    return out


def lreal_eval(p,point,der=(0,0)):
    z=leval(p,point,der)
    require(z.im==0,"expected real Laurent evaluation")
    return z.re


def phase(t):
    t=F(t)
    return Q((1-t*t)/(1+t*t),2*t/(1+t*t))


def psi(point):
    # omega=1 fixture: 2-cos(z1-p1)-cos(z2-p2).
    out={(0,0):Q(F(2))}
    for j in range(2):
        e=(1,0) if j==0 else (0,1)
        ne=(-e[0],-e[1])
        out[e]=-point[j].inv()/2
        out[ne]=-point[j]/2
    return out


def separator(points):
    q={(0,0):ONE}
    for p in points:
        q=lmul(q,psi(p))
    return q


def sinechart(center):
    out=[]
    for j in range(2):
        e=(1,0) if j==0 else (0,1)
        ne=(-e[0],-e[1])
        out.append({e:center[j].inv()/(2*IM),ne:-center[j]/(2*IM)})
    return out


def quotient_chart_jet(point,center,q,target,mutant=None):
    value,dx,dy=map(F,target)
    q0=lreal_eval(q,point)
    require(q0!=0,"surviving site separated from killed sites")
    out=[value/q0]
    for j,d in enumerate((dx,dy)):
        qd=lreal_eval(q,point,(1,0) if j==0 else (0,1))
        physical=d/q0
        if mutant!="quotient":
            physical-=value*qd/(q0*q0)
        chart_derivative=(point[j]/center[j]).re
        require(chart_derivative!=0,"local sine chart nonsingular")
        out.append(physical if mutant=="chart" else physical/chart_derivative)
    return tuple(out)


def periodic_pair_dual(survivors,killed,targets,mutant=None):
    c=survivors[0]
    q=separator(killed)
    s=sinechart(c)
    chord=tuple(lreal_eval(p,survivors[1]) for p in s)
    a,b=chord
    n2=a*a+b*b
    require(n2!=0,"local chart distinct surviving sites")
    # Rational secant basis: physical chart w=v*t+v_perp*y/|v|^2.
    tp=lscale(ladd(lscale(s[0],a),lscale(s[1],b)),1/n2)
    yp=ladd(lscale(s[0],-b),lscale(s[1],a))
    jets=[quotient_chart_jet(p,c,q,v,mutant)
          for p,v in zip(survivors,targets)]
    (f0,gx0,gy0),(f1,gx1,gy1)=jets
    d0,d1=a*gx0+b*gy0,a*gx1+b*gy1
    y0,y1=(-b*gx0+a*gy0)/n2,(-b*gx1+a*gy1)/n2
    coeff=hermite(f0,f1,d0,d1,y0,y1,F(1))
    pp={}
    for n,z in enumerate(coeff[:4]):
        pp=ladd(pp,lscale(lpow(tp,n),z))
    pp=ladd(pp,lscale(yp,coeff[4]),lscale(lmul(tp,yp),coeff[5]))
    return lmul(q,pp)


def periodic_singleton_dual(site,killed,target,mutant=None):
    q=separator(killed if mutant!="drop_killed" else killed[:-1])
    f,gx,gy=quotient_chart_jet(site,site,q,target)
    sx,sy=sinechart(site)
    p=ladd({(0,0):Q(f)},lscale(sx,gx),lscale(sy,gy))
    return lmul(q,p)


def jets_match(poly,sites,targets):
    return all(lreal_eval(poly,site,der)==F(want)
               for site,target in zip(sites,targets)
               for der,want in zip(((0,0),(1,0),(0,1)),target))


def check_laurent(poly,degree):
    check(all(abs(i)+abs(j)<=degree for i,j in poly),"finite_fourier_support")
    check(all(a==poly.get((-i,-j),ZERO).conj()
              for (i,j),a in poly.items()),"real_fourier_symmetry")


def controls_fourier():
    zero=(F(0),F(0),F(0))
    for small in (F(1,16),F(1,64)):
        pins=((phase(-small),ONE),(phase(small),ONE))
        w0=(phase(F(1,2)),phase(F(1,3)))
        w1=(w0[0]*phase(small),w0[1]*phase(2*small))
        sites=(*pins,w0,w1)
        for chosen in range(12):
            target=[tuple(F(int(chosen==3*i+j)) for j in range(3))
                    for i in range(4)]
            if chosen<6:
                poly=periodic_pair_dual(pins,(w0,w1),target[:2])
            else:
                poly=periodic_pair_dual((w0,w1),pins,target[2:])
            check(jets_match(poly,sites,target),"periodic_pair_dual")
            check_laurent(poly,5)
        for name in ("quotient","chart"):
            target=(zero,(F(1),F(2),F(-3)))
            poly=periodic_pair_dual((w0,w1),pins,target,name)
            reject("pair_"+name+"_chain_rule_"+str(small),
                   lambda poly=poly,target=target:
                   require(jets_match(poly,sites,(zero,zero,*target)),
                           "exact periodic pair jets"))
    # Distant witness phases share the same global sine coordinates:
    # sin(theta)=sin(pi-theta); each local singleton chart is still regular.
    pins=((phase(F(-1,32)),ONE),(phase(F(1,32)),ONE))
    p=(Q(F(3,5),F(4,5)),Q(F(5,13),F(12,13)))
    other=(Q(F(-3,5),F(4,5)),Q(F(-5,13),F(12,13)))
    global_s=sinechart((ONE,ONE))
    check(all(leval(s,p)==leval(s,other) for s in global_s),
          "global_sine_collision_fixture")
    sites=(*pins,p,other)
    for who in (2,3):
        for j in range(3):
            target=[zero for _ in sites]
            target[who]=tuple(F(int(i==j)) for i in range(3))
            killed=tuple(s for i,s in enumerate(sites) if i!=who)
            poly=periodic_singleton_dual(sites[who],killed,target[who])
            check(jets_match(poly,sites,target),"periodic_singleton_dual")
            check_laurent(poly,4)
    target=(F(1),F(0),F(0))
    poly=periodic_singleton_dual(p,(*pins,other),target,"drop_killed")
    reject("singleton_missing_third_separator",
           lambda: require(jets_match(poly,sites,(zero,zero,target,zero)),
                           "distant witness not killed"))
    q=separator((p,p))
    for i in range(4):
        for j in range(4-i):
            check(leval(q,p,(i,j))==ZERO,"confluent_order_four_zero")
    check(leval(q,p,(4,0))!=ZERO,"confluent_order_four_sharp")
    reject("single_separator_for_confluent_third_jet",
           lambda: require(leval(psi(p),p,(2,0))==ZERO,
                           "order-two contact derivative survives"))


def det(matrix):
    a=[list(map(F,row)) for row in matrix]
    out=F(1)
    for i in range(len(a)):
        pivot=next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot is None:
            return F(0)
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            out=-out
        value=a[i][i]
        out*=value
        for j in range(i+1,len(a)):
            ratio=a[j][i]/value
            for k in range(i,len(a)):
                a[j][k]-=ratio*a[i][k]
    return out


def raw_to_v(d,mutant=False):
    # Raw (gx,gy,gx',gy',h,h'), e=(1,0).
    hpower=2 if mutant else 3
    return [
        [1,0,0,0,0,0],[0,1,0,0,0,0],
        [-1/d,0,1/d,0,0,0],[0,-1/d,0,1/d,0,0],
        [0,0,0,0,1,0],
        [-d/(2*d**hpower),0,-d/(2*d**hpower),0,-1/d**hpower,1/d**hpower],
    ]


def controls_covariance_and_ledger():
    for rho in (F(1,2),F(1,4),F(1,16)):
        # Exact sharp scalar joint block Var xi=1, Var V=rho^14,
        # Cov(xi,V)=rho^7, so mean xi|V=1 is rho^-7.
        s=rho**14
        c=rho**7
        energy=1/s
        shift=c/s
        check(c*c/s==1,"regression_contraction")
        check(shift*shift==energy,"regression_square_root_energy")
        check((rho**-7)**8==rho**-56,"eighth_moment_exponent")
        check((s**6)==rho**84,"six_dimensional_covariance_determinant")
        check((rho**-42)**2==1/s**6,"six_dimensional_density_exponent")
        reject("covariance_floor_unsquared_"+str(rho),
               lambda s=s,rho=rho: require(s>=rho**7,"false rho^7 floor"))
        reject("regression_cost_understated_"+str(rho),
               lambda shift=shift,rho=rho: require(shift<=rho**-6,
                                                   "false rho^-6 regression"))
        reject("density_dimension_four_"+str(rho),
               lambda s=s,rho=rho: require((rho**-28)**2>=1/s**6,
                                           "six observations need rho^-42"))
    for d in (F(1,2),F(1,16),F(1,128)):
        check(det(raw_to_v(d))==d**-5,"raw_to_V_jacobian")
        reject("height_Jacobian_power_"+str(d),
               lambda d=d: require(det(raw_to_v(d,True))==d**-5,
                                   "missing height difference scale"))
    for q in (F(1,2),F(1,8),F(3,16)):
        a=q**3
        integral=q*q/2+a/q
        check(integral==F(3,2)*a/q,"radial_integral_split")
        check(integral==F(3,2)*q*q,"radial_integral_power")
    dual=2*2+3
    floor=2*dual
    density=floor*6//2
    moment=dual*8
    total=density+moment
    check((dual,floor,density,moment,total)==(7,14,42,56,98),
          "rho_exponent_ledger")
    check(1-5+3+2==1,"delta_power_ledger")
    check(2-2+3+2==5,"normalized_r_power")
    check(2+3+2==7,"unnormalized_r_power")
    check(2-2+3+3==6,"separated_r_power")
    check(F(2)-98*F(1,100)==F(51,50),"moving_rho_exponent")
    check(F(2)-98*F(1,49)==0,"moving_rho_threshold")
    reject("missing_second_small_witness_determinant",
           lambda: require(1-5+3+1==1,"radial power becomes zero"))
    reject("extra_full_normalizer",
           lambda: require(2-4+3+2==5,"normalized r power becomes three"))
    reject("one_height_window_in_separated_branch",
           lambda: require(2-2+3==6,"two height lengths required"))
    reject("claim_endpoint_alpha_as_decay",
           lambda: require(F(2)-98*F(1,49)>0,"threshold has zero decay"))
    for n in range(33):
        ordered=sum(1 for i in range(n) for j in range(n) if i!=j)
        check(ordered==n*(n-1),"ordered_factorial_count")
        check(F(int(n>=2))<=F(ordered,2),"pair_probability_integer_bound")
        check(n*int(n>=2)<=ordered,"multiple_witness_integer_bound")
    reject("ordered_count_divided_by_two",
           lambda: require(F(2*(2-1),2)==2,"two distinct points give two pairs"))


def main():
    controls_observations()
    controls_hermite()
    controls_fourier()
    controls_covariance_and_ledger()
    print("C107 author finite controls; exact arithmetic; no theorem acceptance")
    print("Python "+sys.version.split()[0])
    for name in sorted(counts):
        print("PASS "+name+": "+str(counts[name]))
    for name in mutants:
        print("REJECTED "+name)
    print("TOTAL checks="+str(sum(counts.values()))+" mutants="+str(len(mutants)))
    print("LIMIT: finite controls do not certify continuum, Gaussian, or Kac-Rice steps.")


if __name__=="__main__":
    main()
