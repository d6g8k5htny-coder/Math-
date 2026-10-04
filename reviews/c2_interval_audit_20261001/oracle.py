"""Independent rational enclosure of PR223's nine numerical outputs.

No source numerical engine is imported. Fractions and integers only; all interval
rounding is outward to 2^-240. Log/exp are bounded by explicit power-series tails;
Gamma uses the positive-real Stirling remainder, not float Gamma or quadrature.
This evaluates supplied closed forms, not their Gaussian/persistence derivation.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial, isqrt
import json

BITS=240
SCALE=1<<BITS
PUBLISHED={
'1.c':('0.1101103789590410','0.1101103789590625'),
'1.c2':('0.2300445802661503','0.2300445802661998'),
'1.ratio':('2.089217950577392','2.089217950578207'),
'2.c':('0.07340691930602738','0.07340691930604167'),
'2.c2':('0.2215244106266632','0.2215244106267110'),
'2.ratio':('3.017759261945122','3.017759261946299'),
'3.c':('0.04177593184059426','0.04177593184060272'),
'3.c2':('0.1612340491269447','0.1612340491269810'),
'3.ratio':('3.859496174547095','3.859496174548665')}

def q(x):
    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')
    return F(x)

def floor(x):return x.numerator//x.denominator

def ceil(x):return -((-x.numerator)//x.denominator)

def enclosure(a,b=None):
    a=q(a);b=a if b is None else q(b)
    if a>b:raise ValueError('reversed interval')
    return F(floor(a*SCALE),SCALE),F(ceil(b*SCALE),SCALE)

def plus(a,b):return enclosure(a[0]+b[0],a[1]+b[1])
def minus(a,b):return enclosure(a[0]-b[1],a[1]-b[0])
def times(a,b):
    p=[x*y for x in a for y in b];return enclosure(min(p),max(p))
def over(a,b):
    if b[0]<=0<=b[1]:raise ValueError('division by interval containing zero')
    p=[x/y for x in a for y in b];return enclosure(min(p),max(p))
def power(a,n):
    if type(n) is not int:raise TypeError('integer power required')
    if n<0:return over((F(1),F(1)),power(a,-n))
    out=(F(1),F(1))
    for _ in range(n):out=times(out,a)
    return out

def atan_inv(n,terms=100):
    x=F(1,n)
    s=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(terms)),F(0))
    tail=x**(2*terms+1)/(2*terms+1)
    return enclosure(s-tail,s+tail)

@lru_cache(None, typed=True)
def pi_bounds():return minus(times((F(16),F(16)),atan_inv(5)),times((F(4),F(4)),atan_inv(239)))

def _log_small(t,terms=100):
    u=(t-1)/(t+1)
    if not 1<=t<=2:raise ValueError('reduced logarithm range')
    s=2*sum((u**(2*j+1)/(2*j+1) for j in range(terms)),F(0))
    rem=2*u**(2*terms+1)/((2*terms+1)*(1-u*u))
    return enclosure(s,s+rem)

@lru_cache(None, typed=True)
def log_bounds(t):
    t=q(t)
    if t<=0:raise ValueError('positive logarithm input')
    e=0
    while t<1:t*=2;e-=1
    while t>=2:t/=2;e+=1
    return plus(_log_small(t),times((F(e),F(e)),_log_small(F(2))))

def log_iv(a):return log_bounds(a[0])[0],log_bounds(a[1])[1]

def exp_bounds(t):
    t=q(t)
    if t<0:return over((F(1),F(1)),exp_bounds(-t))
    n=0
    while t>F(1,2):t/=2;n+=1
    # Positive Taylor series: bound all omitted terms by the first omitted
    # term times a geometric series with ratio <= t/(K+2).
    K=100
    s=sum((t**j/F(factorial(j)) for j in range(K+1)),F(0))
    tail=t**(K+1)/factorial(K+1)/(1-t/F(K+2))
    ans=enclosure(s,s+tail)
    for _ in range(n):ans=times(ans,ans)
    return ans

def exp_iv(a):return exp_bounds(a[0])[0],exp_bounds(a[1])[1]

def _int_nroot(n,k):
    if k==2:return isqrt(n)
    lo,hi=0,1<<((n.bit_length()+k-1)//k)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<=n:lo=mid
        else:hi=mid
    return lo

def root_bounds(t,n):
    t=q(t)
    if t<0 or type(n) is not int or n<1:raise ValueError('nonnegative input and positive integer root')
    k=_int_nroot(floor(t*SCALE**n),n)
    lo=F(k,SCALE)
    return lo,lo if lo**n==t else F(k+1,SCALE)

def root_iv(a,n):return root_bounds(a[0],n)[0],root_bounds(a[1],n)[1]

@lru_cache(None, typed=True)
def bernoulli(n):
    B=[F(1)]
    for j in range(1,n+1):B.append(-sum((F(comb(j+1,k))*B[k] for k in range(j)),F(0))/F(j+1))
    return B[n]

@lru_cache(None, typed=True)
def lngamma_bounds(x):
    x=q(x)
    if x<=0:raise ValueError('positive rational Gamma input')
    N,K=40,20;y=x+N
    ans=minus(times((y-F(1,2),y-F(1,2)),log_bounds(y)),(y,y))
    ans=plus(ans,times((F(1,2),F(1,2)),log_iv(times((F(2),F(2)),pi_bounds()))))
    corr=sum((bernoulli(2*j)/(2*j*(2*j-1)*y**(2*j-1)) for j in range(1,K+1)),F(0))
    rem=abs(bernoulli(2*K+2))/((2*K+2)*(2*K+1)*y**(2*K+1))
    # For positive y, the real log-Gamma Stirling remainder is bounded by
    # the first omitted term. See NIST DLMF 5.11(ii). Symmetric use is safe.
    ans=plus(ans,enclosure(corr-rem,corr+rem))
    prod=F(1)
    for j in range(N):prod*=x+j
    return minus(ans,log_bounds(prod))

@lru_cache(None, typed=True)
def gamma_bounds(x):return exp_iv(lngamma_bounds(x))

@lru_cache(None, typed=True)
def coefficients():
    pi=pi_bounds();p32=times(pi,root_iv(pi,2));p52=times(pi,p32)
    sixth=root_bounds(F(12),6)
    lead=over(gamma_bounds(F(1,6)),sixth)
    corr=times(gamma_bounds(F(5,6)),sixth)
    s6=root_bounds(F(6),2)
    c3=minus((F(29,72),F(29,72)),times((F(1,12),F(1,12)),s6))
    d3=times((F(5,48),F(5,48)),minus((F(33),F(33)),times((F(7),F(7)),s6)))
    out={}
    for d,lc,dc,pden in ((1,(F(1,6),)*2,(F(3,4),)*2,p32),(2,(F(1,9),)*2,(F(13,18),)*2,p32),(3,c3,d3,p52)):
        c=over(times(lc,lead),pden);c2=over(times(dc,corr),pden)
        out[f'{d}.c']=c;out[f'{d}.c2']=c2;out[f'{d}.ratio']=over(c2,c)
    return out

def decimal_pair(iv,places=40):
    den=10**places
    vals=[floor(iv[0]*den),ceil(iv[1]*den)]
    return [('-' if z<0 else '')+str(abs(z)//den)+'.'+f'{abs(z)%den:0{places}d}' for z in vals]

def results():
    out={}
    for key,a in coefficients().items():
        ref=tuple(map(F,PUBLISHED[key]))
        if not ref[0]<a[0]<=a[1]<ref[1]:raise ArithmeticError('published containment failed: '+key)
        out[key]={'independent_rational_interval':decimal_pair(a),'published_interval':PUBLISHED[key],'strictly_inside':True}
    return {'scope':'independent numerical certification of the nine supplied closed forms only',
            'scientific_effect':'NONE','source_analytic_derivation_revalidated':False,
            'binary_float_used':False,'dyadic_bits':BITS,'Gamma_shift':40,'Gamma_terms':20,
            'values':out}

if __name__=='__main__':print(json.dumps(results(),indent=2,sort_keys=True))
