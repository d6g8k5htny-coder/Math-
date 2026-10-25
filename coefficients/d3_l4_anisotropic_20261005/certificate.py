#!/usr/bin/env python3
"""Outward d=3,L=4 evaluation of the pinned Eq.(15.2) coefficient.
Standard library only. This is an author-side arithmetic/proof candidate,
not independent review, Lean verification, or acceptance of the parent theorem.
See PROOF.md for the cone reduction and all-direction error estimates.
"""
import argparse
import decimal
import json
import math
import sys
from fractions import Fraction

D=decimal.Decimal
PREC=60
decimal.getcontext().prec=PREC
DOWN=decimal.Context(prec=PREC,rounding=decimal.ROUND_FLOOR)
UP=decimal.Context(prec=PREC,rounding=decimal.ROUND_CEILING)
NEAR=decimal.Context(prec=PREC,rounding=decimal.ROUND_HALF_EVEN)


def dec(x):
    if isinstance(x,(float,bool)):
        raise TypeError('floating/bool inputs are not certificate inputs')
    z=x if isinstance(x,D) else D(x)
    if not z.is_finite(): raise ValueError('finite input required')
    return z


def positive_integer_power(x,n,ctx):
    result=D(1)
    while n:
        if n&1: result=ctx.multiply(result,x)
        n//=2
        if n: x=ctx.multiply(x,x)
    return result


class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        if isinstance(lo,I):
            self.lo,self.hi=lo.lo,lo.hi; return
        self.lo=dec(lo); self.hi=dec(lo if hi is None else hi)
        if self.lo>self.hi: raise ValueError('reversed interval')
    def __add__(self,y):
        y=I(y); return I(DOWN.add(self.lo,y.lo),UP.add(self.hi,y.hi))
    __radd__=__add__
    def __neg__(self): return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,y): return self+-I(y)
    def __rsub__(self,y): return I(y)+-self
    def __mul__(self,y):
        y=I(y)
        p=[(self.lo,y.lo),(self.lo,y.hi),(self.hi,y.lo),(self.hi,y.hi)]
        return I(min(DOWN.multiply(a,b) for a,b in p),max(UP.multiply(a,b) for a,b in p))
    __rmul__=__mul__
    def reciprocal(self):
        if self.lo<=0<=self.hi: raise ZeroDivisionError('interval includes zero')
        return I(DOWN.divide(D(1),self.hi),UP.divide(D(1),self.lo))
    def __truediv__(self,y): return self*I(y).reciprocal()
    def __rtruediv__(self,y): return I(y)*self.reciprocal()
    def __pow__(self,n):
        if not isinstance(n,int) or isinstance(n,bool): raise TypeError('integer power required')
        if n<0: return (self**(-n)).reciprocal()
        if n==0: return I(1)
        if n%2==0:
            lo=D(0) if self.lo<=0<=self.hi else min(self.lo.copy_abs(),self.hi.copy_abs())
            hi=max(self.lo.copy_abs(),self.hi.copy_abs())
            return I(positive_integer_power(lo,n,DOWN),positive_integer_power(hi,n,UP))
        lo=(positive_integer_power(self.lo,n,DOWN) if self.lo>=0 else
            positive_integer_power(self.lo.copy_abs(),n,UP).copy_negate())
        hi=(positive_integer_power(self.hi,n,UP) if self.hi>=0 else
            positive_integer_power(self.hi.copy_abs(),n,DOWN).copy_negate())
        return I(lo,hi)
    def sqrt(self):
        if self.lo<0: raise ValueError('negative sqrt interval')
        lo=NEAR.sqrt(self.lo); hi=NEAR.sqrt(self.hi)
        return I(D(0) if self.lo==0 else NEAR.next_minus(lo),NEAR.next_plus(hi))
    def exp(self):
        return I(NEAR.next_minus(NEAR.exp(self.lo)),NEAR.next_plus(NEAR.exp(self.hi)))
    def ln(self):
        if self.lo<=0: raise ValueError('positive log input required')
        return I(NEAR.next_minus(NEAR.ln(self.lo)),NEAR.next_plus(NEAR.ln(self.hi)))
    def power23(self):
        if self.lo<=0: raise ValueError('positive power input required')
        return (self.ln()*I(2)/3).exp()
    def widen(self,e):
        e=I(e).hi
        if e<0: raise ValueError('negative error')
        return self+I(e.copy_negate(),e)
    def abs_upper(self): return max(self.lo.copy_abs(),self.hi.copy_abs())
    def mid(self): return NEAR.divide(NEAR.add(self.lo,self.hi),D(2))
    def pair(self): return [str(self.lo),str(self.hi)]


def need(condition,message):
    if not condition: raise ValueError(message)


def pi_interval():
    def arctan(q):
        x=I(1)/q; s=I(0)
        for k in range(100): s+=((-1)**k)*(x**(2*k+1))/(2*k+1)
        return s.widen((x**201)/201)
    return 16*arctan(5)-4*arctan(239)

PI=pi_interval()


def sincos(x):
    x=I(x); need(x.lo>=0 and x.hi<2,'trig range must be [0,2)')
    xx=x*x; ts=x; tc=I(1); s=ts; c=tc
    for k in range(1,60):
        ts=-ts*xx/((2*k)*(2*k+1)); tc=-tc*xx/((2*k-1)*(2*k))
        s+=ts; c+=tc
    # Uniform Taylor remainder on [0,2]; first omitted terms.
    return s.widen(I(2)**121/math.factorial(121)),c.widen(I(2)**120/math.factorial(120))


def moments(L=4,N=10):
    th={0:I(1),2:I(-1),4:I(3),6:I(-15)}
    for n in range(1,N+1):
        z=I(L*n)**2; e=2*(-z/2).exp()
        for j,p in {0:I(1),2:z-1,4:z*z-6*z+3,6:z**3-15*z*z+45*z-15}.items():
            th[j]+=p*e
    x=I(L*(N+1))
    need(x.lo>=10,'image-tail Hermite range')
    tail=8*x**6*(-x*x/2).exp()
    ratio=(I(N+2)/(N+1))**6*(-I(L)**2*(2*N+3)/2).exp()
    need(ratio.hi<D("0.5"),"geometric image-tail ratio failed")
    return -th[2]/th[0],th[4]/th[0],-th[6]/th[0],tail


def diagonal_cone(lam,mu):
    return (3*lam**2-4*lam*mu+8*mu**2-8*mu**2*(mu/(lam+mu)).sqrt())/2


def parameters(L=4,reference=False):
    if reference: a,m4,m6,tail=I(1),I(3),I(15),I(0)
    else:
        need(L==4,'this certificate is scoped to L=4 or the reference')
        a,m4,m6,tail=moments(L)
    b=a*a; k=m4-3*b; k6=m6-15*m4*a+30*a**3
    h=k6-k*k/a; A=9*a*k; base=6*a**3
    if reference: k=I(0); k6=I(0); h=I(0); A=I(0)
    c1=1/b; kap=k/(2*b*(2*b+k)); c0=c1-4*b/((2*b+k)*(5*b+k))
    bt=c0-2*kap; bs=c1-2*kap
    if reference: Tmin=Tmax=I(6)
    else:
        need(k.lo>0 and h.hi<0 and (A+h).hi<0 and (A+2*h/3).hi<0,
             'uniform tau extremum hypotheses failed')
        Tmin=base+A+h; Tmax=base+A/3+h/9
    need(bt.lo>0 and bs.lo>0,'uniform precision positivity failed')
    if not reference:
        need((a+16*tail).hi<1 and (m4+16*tail).hi<4 and (m6+16*tail).hi<15,
             'coordinate-moment image comparison hypotheses failed')
        varmax=15*a**3+15*a*k
        need(k6.hi<0 and (a*Tmin/(a+varmax)).lo>D('0.2') and (2*b).lo>D('0.2'),
             'joint covariance lower bound failed')
        need((216000*tail).hi<D('0.001'),'image covariance perturbation too large')
    detH=b**3*(2*b+k)**2*(5*b+k)
    Dref=I(29)/6-I(6).sqrt()
    const=2*I(3).sqrt()/(a*a.sqrt()*detH.sqrt()*I(6).power23()*Dref)
    Rmax=const*Tmax.power23()*diagonal_cone(1/bt,1/bs)/(bt*bs**2).sqrt()
    if reference:
        M1=M2=I(0)
    else:
        # |S4'|<=2, |S6'|<=3 (variance <=1/4);
        # |S4''|<=16, |S6''|<=36, for either rotation coordinate.
        t1=(2*A+3*(-h))/Tmin; t2=(16*A+36*(-h))/Tmin
        q1=8*kap/bt; q2=32*kap/bt
        m1=I(2)*t1/3+I(7)*q1/2
        m2=I(2)*t2/3+I(2)*t1*t1/9+I(14)*t1*q1/3+I(63)*q1*q1/4+I(7)*q2/2
        M1=Rmax*m1; M2=Rmax*m2
    return dict(a=a,m4=m4,m6=m6,b=b,k=k,k6=k6,h=h,A=A,base=base,
                c0=c0,c1=c1,kap=kap,Bmin=bt,Bsmin=bs,Tmin=Tmin,Tmax=Tmax,
                detH=detH,const=const,Rmax=Rmax,M1=M1,M2=M2,tail=tail,
                reference=reference)


def inverse3(B):
    a,b,c=B[0]; _,d,e=B[1]; _,_,f=B[2]
    cof=[[d*f-e*e,c*e-b*f,b*e-c*d],
         [c*e-b*f,a*f-c*c,b*c-a*e],
         [b*e-c*d,b*c-a*e,a*d-b*b]]
    det=a*cof[0][0]+b*cof[0][1]+c*cof[0][2]
    need(a.lo>0 and cof[2][2].lo>0 and det.lo>0,'matrix positivity not certified')
    return [[x/det for x in row] for row in cof],det


def positive_eigenvalue(C,detB):
    s1=C[0][0]-C[1][1]-C[2][2]
    s2=-(C[0][0]*C[1][1]-C[0][1]**2)-(C[0][0]*C[2][2]-C[0][2]**2)+(C[1][1]*C[2][2]-C[1][2]**2)
    s3=1/detB
    def p(x): return ((x-s1)*x+s2)*x-s3
    def dp(x): return 3*x*x-2*s1*x+s2
    need(p(I(1)).hi<0 and p(I(2)).lo>0,'positive eigenvalue bracket failed')
    need((6*I(1)-2*s1).lo>0 and dp(I(1)).lo>0,'positive derivative proof failed')
    # A nearest-rounded predictor is not evidence: the residual enclosure below is.
    a,b,c=s1.mid(),s2.mid(),s3.mid(); x=D('1.5')
    with decimal.localcontext(NEAR):
        for _ in range(9): x-=(((x-a)*x+b)*x-c)/(3*x*x-2*a*x+b)
    need(1<x<2,'Newton predictor outside proved bracket')
    # Division for a bound is outward, not the nearest-rounded line above.
    radius=UP.divide(p(I(x)).abs_upper(),dp(I(1)).lo)
    bracket=I(x).widen(radius)
    bracket=I(max(D(1),bracket.lo),min(D(2),bracket.hi))
    for _ in range(2):
        x=bracket.mid()
        derivative=dp(bracket)
        need(derivative.lo>0,'interval Newton derivative failed')
        updated=I(x)-p(I(x))/derivative
        bracket=I(max(bracket.lo,updated.lo),min(bracket.hi,updated.hi))
    need(bracket.hi-bracket.lo<D('1e-45'),'positive eigenvalue not sufficiently enclosed')
    return bracket,s1,s3


def choose(alpha,n):
    s=Fraction(1)
    for i in range(n): s*=Fraction(alpha-i,i+1)
    return s

K=8
COEFF=[]
for j in range(K+1):
    # P_j(t)=sum_i binom(5/2,i)binom(-1/2,2j-i)t^(2j-i).
    cs=[choose(Fraction(5,2),i)*choose(Fraction(-1,2),2*j-i) for i in range(2*j+1)]
    COEFF.append([I(q.numerator)/q.denominator for q in cs])
CIRCLE=[I(math.comb(2*j,j))/(4**j) for j in range(K+1)]


def cone(B):
    C,detB=inverse3(B)
    lam,s1,s3=positive_eigenvalue(C,detB)
    m=(lam-s1)/2
    d2=m*m-s3/lam
    need(d2.hi>=0,'negative squared eigenvalue separation')
    # This intersection uses the proved real spectrum / positive inertia of C^(1/2)JC^(1/2).
    d2=I(max(D(0),d2.lo),d2.hi)
    delta2=d2/(m*m); rho=delta2.sqrt()
    need(rho.hi<D('0.5') and m.lo>0,'cone series domain failed')
    t=m/(lam+m)
    need(t.lo>0 and t.hi<1,"cone scale outside (0,1)")
    Eh=I(0); power=I(1)
    for j,cs in enumerate(COEFF):
        poly=I(0)
        for c in cs: poly=poly*t+c
        Eh+=power*CIRCLE[j]*poly
        power*=delta2
    # |binom(5/2,i)|<=3, |binom(-1/2,j)|<=1.
    # Bound the entire omitted series, including the odd terms that actually integrate to zero.
    n=2*K
    rr=I(rho.hi)
    tail=3*rr**(n+1)*((n+2)-(n+1)*rr)/(1-rr)**2
    fac=4*m*m*t.sqrt()
    out=I(3)*lam*lam/2-2*lam*m+4*m*m+2*d2-fac*Eh
    error=fac*tail
    need(out.lo-error.hi>0,'cone lower bound failed')
    return out,error,dict(detB=detB,rho=rho,lambda_positive=lam,negative_mean=m,
                          negative_split_squared=d2,C=C)


def direction(theta,phi,p):
    st,ct=sincos(theta); sp,cp=sincos(phi)
    return direction_trig(st,ct,sp,cp,p)


def direction_trig(st,ct,sp,cp,p):
    u=[st*cp,st*sp,ct]; w=[ct*cp,ct*sp,-st]; v=[-sp,cp,I(0)]
    columns=[[1-z*z for z in u], [w[i]*w[i]-v[i]*v[i] for i in range(3)],
             [2*w[i]*v[i] for i in range(3)]]
    B=[[I(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            B[i][j]=(p['c0'] if i==j==0 else p['c1'] if i==j else I(0))-p['kap']*sum(columns[i][k]*columns[j][k] for k in range(3))
    T=p['base']+p['A']*sum(z**4 for z in u)+p['h']*sum(z**6 for z in u)
    d,e,meta=cone(B)
    scale=p['const']*T.power23()/meta['detB'].sqrt()
    meta.update(D=d,cone_error_D=e,tau2=T,precision=B)
    return scale*d,scale*e,meta


def integrate(N=64,reference=False,progress=False):
    need(isinstance(N,int) and N>=2,'at least two cells required')
    p=parameters(reference=reference)
    trig=[sincos(PI*(2*i+1)/(4*N)) for i in range(N)]
    edges=[sincos(PI*i/(2*N))[1] for i in range(N+1)]
    weights=[edges[i]-edges[i+1] for i in range(N)]
    total=I(0); errcone=I(0); maxrho=D(0); minD=None; maxD=None
    for i,(st,ct) in enumerate(trig):
        row=I(0); re=I(0)
        for sp,cp in trig:
            value,err,meta=direction_trig(st,ct,sp,cp,p)
            row+=value; re+=err
            maxrho=max(maxrho,meta['rho'].hi)
            low=DOWN.subtract(meta['D'].lo,meta['cone_error_D'].hi)
            high=UP.add(meta['D'].hi,meta['cone_error_D'].hi)
            minD=low if minD is None else min(minD,low)
            maxD=high if maxD is None else max(maxD,high)
        total+=weights[i]*row/N; errcone+=weights[i]*re/N
        if progress and (i+1)%8==0: print('angular rows %d/%d'%(i+1,N),file=sys.stderr,flush=True)
    step=PI/(2*N)
    # Weighted theta midpoint and ordinary phi midpoint, each with a global proof bound.
    angular=(PI/2)*step**2*(p['M1']/12+p['M2']/24)+step**2*p['M2']/24
    ratio=total.widen(UP.add(errcone.hi,angular.hi))
    # Recover the nonperiodic reference from the pinned SIDE24 interval and relative image bound.
    c24=I('0.04177593184059834334','0.04177593184059834335')
    cref=I(DOWN.divide(c24.lo,UP.add(D(1),D('1e-106'))),
           UP.divide(c24.hi,DOWN.subtract(D(1),D('1e-106'))))
    image=I(0) if reference else I(10**8)*p['tail']
    need((p['Rmax']*cref).hi<1,'image-error absolute scale bound failed')
    central=total*cref
    cone_abs=errcone*cref
    angle_abs=angular*cref
    enclosure=(ratio*cref).widen(image)
    return dict(object='D3-L4-ANISOTROPIC-20261005-v1',method='outward Decimal intervals + analytic cone series + proved angular midpoint error',
                source_commit='2f8d721e300850e36ab17464dc541c977b3ffcbf',
                L='infinity' if reference else 4,dimension=3,N_theta=N,N_phi=N,cone_series_degree=2*K,
                arithmetic_precision=PREC,scientific_acceptance=False,independent_review=False,
                quadrature_only_interval=central.pair(),ratio_quadrature_only=total.pair(),
                coefficient_interval=enclosure.pair(),ratio_interval=ratio.widen(image/cref).pair(),
                error_bounds=dict(image_sum_coefficient=str(image.hi),cone_integration_coefficient=str(cone_abs.hi),
                                  angular_coefficient=str(angle_abs.hi),angular_ratio=str(angular.hi),
                                  arithmetic_and_reference_interval_width=str(UP.subtract(central.hi,central.lo))),
                uniform_bounds={k:p[k].pair() for k in ['a','m4','m6','k','k6','h','Tmin','Tmax','Bmin','Bsmin','Rmax','M1','M2','tail']},
                node_diagnostics=dict(max_negative_eigenvalue_relative_split=str(maxrho),
                                      sampled_D_min=str(minD),sampled_D_max=str(maxD)),
                reference_interval=cref.pair(),side24_interval=c24.pair())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n',type=int,default=64)
    ap.add_argument('--reference',action='store_true')
    ap.add_argument('--progress',action='store_true')
    args=ap.parse_args()
    print(json.dumps(integrate(args.n,args.reference,args.progress),indent=2,sort_keys=True))

if __name__=='__main__': main()
