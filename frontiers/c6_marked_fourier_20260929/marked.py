"""Exact finite controls for the marked Fourier candidate, not a continuum prover."""
from fractions import Fraction as F
from math import prod
MUTANT=None

def alpha(d):
 if type(d) is not int or d<2:raise ValueError('fixed dimension d>=2 required')
 return F(1) if MUTANT=='exponential-every-d' else F(2,d)

def admissible_rate(c,theta):
 c,theta=F(c),F(theta)
 return c>0 and theta>0 and (theta if MUTANT=='forget-holder-two' else 2*theta)<c

def regression_second(var,cov,obsvar,target,base_mean):
 var,cov,obsvar,target,base_mean=map(F,(var,cov,obsvar,target,base_mean))
 if var<0 or obsvar<=0 or cov*cov>var*obsvar:raise ValueError('invalid joint covariance')
 mean=base_mean+cov*target/obsvar
 return var-cov*cov/obsvar+(0 if MUTANT=='drop-mean' else mean*mean)

def exponential_moment_bound(c,u,A):
 c,u,A=map(F,(c,u,A))
 if not (0<u<c and A>=1):raise ValueError('positive rate gap and A>=1 required')
 return 1+(1 if MUTANT=='drop-prefactor' else A)*u/(c-u)

def cutoff_rates(d,a):
 alpha(d);a=F(a)
 if a<=0:raise ValueError('positive rate required')
 return 2*a,a*F(2*d+1,4*d),a/F(2*d)

def check_law(p,n):
 p=list(map(F,p));n=list(n)
 if len(p)!=len(n) or not p or any(x<0 for x in p) or sum(p)!=1 or any(type(k) is not int or k<0 for k in n):raise ValueError('finite probability count law required')
 return p,n

def weighted_mark(p,n,w,b):
 p,n=check_law(p,n);w=list(map(F,w));b=F(b)
 if len(w)!=len(p) or min(w)<0 or b<=1:raise ValueError('nonnegative weights and b>1 required')
 Z=sum(x*y for x,y in zip(p,w))
 if Z<=0:raise ValueError('positive normalizer required')
 return sum(x*(y*y if MUTANT=='duplicate-weight' else y)*(1 if MUTANT=='drop-count-mark' else k)*b**k for x,y,k in zip(p,w,n))/Z

def nonempty(p,n):
 p,n=check_law(p,n);mass=sum(x for x,k in zip(p,n) if k>0)
 if not mass:raise ValueError('nonempty event must have positive mass')
 return [x/mass if k else F(0) for x,k in zip(p,n)]

def sizebiased(p,n):
 p,n=check_law(p,n)
 if MUTANT=='nonempty-is-palm':return nonempty(p,n)
 mean=sum(x*k for x,k in zip(p,n))
 if not mean:raise ValueError('positive count mean required')
 return [x*k/mean for x,k in zip(p,n)]

def tail_bound(M,epsilon,n,b):
 M,epsilon,b=map(F,(M,epsilon,b))
 if M<0 or epsilon<0 or type(n) is not int or n<1 or b<=1:raise ValueError('invalid tail parameters')
 return M*epsilon/((1 if MUTANT=='drop-tail-count' else n)*b**n)

def factorial_power(d,p):
 a=alpha(d)
 if type(p) is not int or p<2:raise ValueError('integer moment p>=2 required')
 return F(p-1)/a

def levy_exponent(p,n,epsilon,z):
 p,n=check_law(p,n);epsilon,z=F(epsilon),F(z)
 if epsilon<=0 or not 0<=z<=1:raise ValueError('positive epsilon and real pgf domain required')
 return sum(x*(z**k-1)/epsilon for x,k in zip(p,n) if k>0)

def factorial_mean(p,n,q):
 p,n=check_law(p,n)
 if type(q) is not int or q<1:raise ValueError('positive integer order required')
 return sum(x*prod(k-j for j in range(q)) for x,k in zip(p,n) if k>=q)
