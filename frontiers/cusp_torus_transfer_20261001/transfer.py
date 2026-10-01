"""Rational certificates for a birth-marginal cusp covariance transfer.

This checks finite covariance algebra and outward rational bounds. The analytic
Gaussian-slice theorem is proved in PROOF.md, not inferred from finite tests.
"""
import argparse
from fractions import Fraction as F
from math import factorial
import json

MUTANTS = ('order6','wrong-floor','retain-birth-pin','drop-gamma-degree',
           'omit-entry-count','omit-normalization','reverse-sandwich','wrong-f4-variance')
_MUTANT = None


def rational(x):
    if type(x) not in (int, F): raise TypeError('exact int/Fraction required')
    return F(x)


def dimension(d):
    if type(d) is not int or not 1 <= d <= 12: raise ValueError('dimension 1..12 required')
    return d


def multi(d, *axes):
    out = [0]*d
    for i in axes: out[i] += 1
    return tuple(out)


def jet_labels(d, birth=False):
    d = dimension(d)
    pins = [multi(d,i) for i in range(d)] + [multi(d,0,i) for i in range(d)] + [multi(d,0,0,0)]
    free = [multi(d,i,j) for i in range(1,d) for j in range(i,d)]
    free += [multi(d,0,0,i) for i in range(1,d)] + [multi(d,0,0,0,0)]
    return ([multi(d)] if birth else []) + pins + free


def covariance(a,b):
    if len(a)!=len(b) or any(type(x) is not int or x<0 for x in (*a,*b)):
        raise ValueError('matching nonnegative multi-indices required')
    powers = [x+y for x,y in zip(a,b)]
    if any(x%2 for x in powers): return F(0)
    result = (-1)**(sum(b)+sum(powers)//2)
    for n in powers:
        for j in range(1,n,2): result *= j
    if _MUTANT=='wrong-f4-variance' and sum(a)==sum(b)==4 and a==b:
        result = 15
    return F(result)


def matrix(d,birth=False):
    labels = jet_labels(d,birth)
    return [[covariance(a,b) for b in labels] for a in labels]


def ldlt(mat):
    n = len(mat)
    if not n or any(len(row)!=n for row in mat): raise ValueError('nonempty square matrix required')
    A = [[rational(x) for x in row] for row in mat]
    if any(A[i][j]!=A[j][i] for i in range(n) for j in range(n)):
        raise ValueError('symmetric matrix required')
    L = [[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        pivot=A[j][j]-sum((L[j][k]**2*D[k] for k in range(j)),F(0))
        if pivot<=0: raise ValueError('matrix is not positive definite')
        D.append(pivot)
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),F(0)))/pivot
    return L,D


def inverse(mat):
    n=len(mat);A=[[rational(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(mat)]
    if not n or any(len(row)!=2*n for row in A):raise ValueError('square matrix required')
    for j in range(n):
        candidates=[i for i in range(j,n) if A[i][j]]
        if not candidates:raise ValueError('singular matrix')
        i=candidates[0];A[j],A[i]=A[i],A[j];p=A[j][j];A[j]=[x/p for x in A[j]]
        for i in range(n):
            if i!=j:
                q=A[i][j];A[i]=[x-q*y for x,y in zip(A[i],A[j])]
    return [row[n:] for row in A]


def floor_pivots(d):
    C=matrix(d);floor=F(1,2) if _MUTANT=='wrong-floor' else F(1,3)
    return ldlt([[x-(floor if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(C)])[1]


def even_floor_schur(d):
    d=dimension(d)
    return F(417*d+2018,15*(3*d+5))


def pin_regression(d):
    C=matrix(d,True);q=2*d+2
    P=[row[:q] for row in C[:q]];Inv=inverse(P)
    V=[row[:q] for row in C[q:]]
    B=[[sum((row[k]*Inv[k][j] for k in range(q)),F(0)) for j in range(q)] for row in V]
    S=[[C[q+i][q+j]-sum((B[i][k]*V[j][k] for k in range(q)),F(0)) for j in range(len(V))] for i in range(len(V))]
    det=F(1)
    for x in ldlt(P)[1]:det*=x
    return [row[0] for row in B],S,det,Inv[0][0]


def homogeneous_degree(d):
    degree=2*(dimension(d)-1)+F(7,4)
    return degree-F(7,4) if _MUTANT=='drop-gamma-degree' else degree


def slice_exponent(d):
    q=2*d+1+int(_MUTANT=='retain-birth-pin')
    return (homogeneous_degree(d)-q)/2


def matching_count(q):
    if type(q) is not int or not 0<=q<=8:raise ValueError('derivative order 0..8 required')
    return sum(factorial(q)//(2**j*factorial(j)*factorial(q-2*j)) for j in range(q//2+1))


def exp_negative_interval(x):
    x=rational(x)
    if not 0<=x<=2048:raise ValueError('exponent argument in [0,2048] required')
    if x==0:return F(1),F(1)
    n=2*((x.numerator+x.denominator-1)//x.denominator)+64
    total=term=F(1)
    for k in range(1,n+1):
        term*=x/k;total+=term
    nxt=term*x/(n+1);tail=nxt/(1-x/F(n+2))
    return 1/(total+tail),1/total


def image_derivative_order():
    return 6 if _MUTANT=='order6' else 8


def normalization_allowance():
    return 0 if _MUTANT=='omit-normalization' else 105


def image_bound(d,side):
    if dimension(d)>3:raise ValueError('uniform image theorem here covers d=1,2,3')
    side=rational(side)
    if not 10<=side<=64:raise ValueError('implemented side threshold in [10,64] required')
    p=matching_count(image_derivative_order())
    norm=normalization_allowance()
    return 3*d*3**(d-1)*(p*d**4*side**8+norm)*exp_negative_interval(side*side/2)[1]


def relative_covariance_bound(d,side):
    n=1 if _MUTANT=='omit-entry-count' else len(jet_labels(d))
    return 3*n*image_bound(d,side)


def error_bound(d,side):
    delta=relative_covariance_bound(d,side)
    if delta>F(1,10000):raise ValueError('outside proved linearization range')
    return 13*delta


def sandwich_eighth_powers(d,delta):
    delta=rational(delta)
    if not 0<=delta<1:raise ValueError('relative covariance error in [0,1) required')
    n=len(jet_labels(d));a,b=4*n-5,4*n
    lo=(1-delta)**a/(1+delta)**b
    hi=(1+delta)**a/(1-delta)**b
    return (hi,lo) if _MUTANT=='reverse-sandwich' else (lo,hi)


def scientific_upper(x,digits=12):
    x=rational(x)
    if x<0 or type(digits) is not int or digits<2:raise ValueError('nonnegative value and >=2 digits required')
    if x==0:return '0'
    exponent=len(str(x.numerator))-len(str(x.denominator))
    ten=F(10)**exponent
    if x<ten:exponent-=1
    scale=F(10)**(digits-1-exponent);z=x*scale
    n=-((-z.numerator)//z.denominator)
    if n>=10**digits:n//=10;exponent+=1
    s=str(n).rjust(digits,'0')
    return s[0]+'.'+s[1:]+'e'+str(exponent)


def decimal_enclosure(interval,digits=16):
    out=[]
    for i,v in enumerate(interval):
        v=rational(v)*10**digits
        q=v.numerator//v.denominator if i==0 else -((-v.numerator)//v.denominator)
        sign='-' if q<0 else '';q=abs(q)
        out.append(sign+str(q//10**digits)+'.'+str(q%10**digits).zfill(digits))
    return out


def inherited_interval(d,side):
    # Exact transcription of the outward table in the pinned peer NOTE, not a
    # recomputation or independent acceptance of its quadrature certificate.
    source={1:('-0.22760635877558','-0.22760635877504'),
            2:('-0.269398825674','-0.269398825672'),
            3:('-0.211848347','-0.211848346')}
    lo,hi=map(F,source[d]);eta=error_bound(d,side)
    return lo*(1+eta),hi*(1-eta)


def checks():
    if matching_count(8)!=764 or covariance((4,),(4,))!=105:
        raise ValueError('order-eight Gaussian derivative identity')
    needed=max(sum(a)+sum(b) for a in jet_labels(3) for b in jet_labels(3))
    if image_derivative_order()<needed:raise ValueError('image derivative order below required covariance order')
    if normalization_allowance()<covariance((4,),(4,)):
        raise ValueError('normalization allowance below the origin derivative bound')
    for d in (1,2,3):
        floor_pivots(d)
        if slice_exponent(d)!=F(-5,8):raise ValueError('birth marginal/homogeneity exponent')
        n=len(jet_labels(d))
        if n!=3*d+1+d*(d-1)//2:raise ValueError('jet dimension')
        for L in (10,24):
            E=image_bound(d,L);delta=relative_covariance_bound(d,L)
            if delta!=3*n*E:raise ValueError('entrywise-to-operator norm factor')
            eta=error_bound(d,L)
            lo8,hi8=sandwich_eighth_powers(d,delta)
            if not lo8<=1<=hi8 or lo8<(1-eta)**8 or hi8>(1+eta)**8:
                raise ValueError('Gaussian slice sandwich direction or linearization')
    if not error_bound(3,10)<F(5,10**5):raise ValueError('L>=10 target')
    if not error_bound(3,24)<F(3,10**105):raise ValueError('SIDE24 target')


def result():
    checks()
    data={'scientific_effect':'NONE','mathematical_acceptance':False,
          'scope':'rational checks of explicit transfer; not CU proof or reference quadrature',
          'derivative_order':8,'matching_count':764,'covariance_floor':'1/3',
          'slice_covariance_scaling':'-5/8','dimensions':{}}
    for d in (1,2,3):
        data['dimensions'][str(d)]={'marginal_jet_dimension':len(jet_labels(d)),
            'floor_ldlt_pivots':[str(x) for x in floor_pivots(d)],
            'side_bounds':{}}
        for L in (10,24):
            data['dimensions'][str(d)]['side_bounds'][str(L)]={
                'entry_error_upper':scientific_upper(image_bound(d,L)),
                'relative_covariance_upper':scientific_upper(relative_covariance_bound(d,L)),
                'relative_c1_error_upper':scientific_upper(error_bound(d,L)),
                'conditional_absolute_c1':decimal_enclosure(inherited_interval(d,L))}
    return data


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mutant',choices=MUTANTS)
    args=p.parse_args();global _MUTANT;_MUTANT=args.mutant
    try:ans=result()
    except (ValueError,TypeError) as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True));raise SystemExit(1)
    print(json.dumps(ans,indent=2,sort_keys=True))

if __name__=='__main__':main()
