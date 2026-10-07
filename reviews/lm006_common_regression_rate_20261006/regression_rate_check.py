"""Exact finite polynomial-Gaussian regression; NOT the infinite periodic law.

Twelve independent standard-normal jet coefficients are represented by rows
of rational numbers, not sampled. All diagnostic covariance arithmetic is exact.
"""
import argparse
from fractions import Fraction as F
import json
from math import factorial

BASIS = tuple((i, j) for j, n in ((0, 6), (1, 4), (2, 2)) for i in range(n))


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def mv(a, x):
    return [sum((u*v for u, v in zip(row, x)), F(0)) for row in a]


def sub(a, b):
    return [[x-y for x, y in zip(row, other)] for row, other in zip(a, b)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def norm2(a):
    return sum((x*x for row in a for x in row), F(0))


def inv(a):
    n = len(a)
    if not n or any(len(row) != n for row in a):
        raise ValueError('nonempty square matrix required')
    work = [[F(x) for x in row] + ident for row, ident in zip(a, eye(n))]
    for i in range(n):
        pivot = next((j for j in range(i, n) if work[j][i]), None)
        if pivot is None:
            raise ValueError('singular pin covariance')
        work[i], work[pivot] = work[pivot], work[i]
        scale = work[i][i]
        work[i] = [x/scale for x in work[i]]
        for j in range(n):
            if j != i:
                factor = work[j][i]
                work[j] = [x-factor*y for x,y in zip(work[j],work[i])]
    return [row[n:] for row in work]


def rank(a):
    work = [[F(x) for x in row] for row in a]
    k = 0
    for col in range(len(work[0])):
        pivot = next((j for j in range(k,len(work)) if work[j][col]), None)
        if pivot is None:
            continue
        work[k], work[pivot] = work[pivot], work[k]
        scale = work[k][col]
        work[k] = [x/scale for x in work[k]]
        for j in range(k+1,len(work)):
            factor = work[j][col]
            work[j] = [x-factor*y for x,y in zip(work[j],work[k])]
        k += 1
        if k == len(work):
            break
    return k


def jet(dx, dy, x):
    return [x**(i-dx)/factorial(i-dx) if j==dy and i>=dx else F(0)
            for i,j in BASIS]


def combine(*terms):
    return [sum((factor*row[i] for factor,row in terms), F(0)) for i in range(12)]


def model(radius):
    r = F(radius)
    if r<0 or r>1:
        raise ValueError('diagnostic radius must lie in [0,1]')
    if r:
        h=r/2
        raw=[jet(0,0,-h),jet(1,0,-h),jet(0,1,-h),
             jet(0,0,h),jet(1,0,h),jet(0,1,h)]
        p0=combine((F(1,2),raw[0]),(F(1,2),raw[3]))
        p1=combine((F(1,2),raw[1]),(F(1,2),raw[4]))
        p2=combine((F(1,2),raw[2]),(F(1,2),raw[5]))
        p3=combine((1/r,raw[4]),(-1/r,raw[1]))
        p4=combine((1/r,raw[5]),(-1/r,raw[2]))
        p5=combine((12/r**2,p1),(-12/r**3,raw[3]),(12/r**3,raw[0]))
        pins=[p0,p1,p2,p3,p4,p5]
        v=[combine((1/r,jet(2,0,-h)),(-1/r,p3)),
           combine((1/r,jet(2,0,h)),(-1/r,p3)),
           combine((1/r,jet(1,1,-h)),(-1/r,p4)),
           combine((1/r,jet(1,1,h)),(-1/r,p4)),jet(0,2,-h),jet(0,2,h)]
        physical=[combine((1/r,jet(2,0,-h))),combine((1/r,jet(2,0,h))),
                  combine((1/r,jet(1,1,-h))),combine((1/r,jet(1,1,h))),
                  jet(0,2,-h),jet(0,2,h)]
    else:
        pins=[jet(i,j,F(0)) for i,j in ((0,0),(1,0),(0,1),(2,0),(1,1),(3,0))]
        v=[combine((-F(1,2),pins[5])),combine((F(1,2),pins[5])),
           combine((-F(1,2),jet(2,1,F(0)))),combine((F(1,2),jet(2,1,F(0)))),
           jet(0,2,F(0)),jet(0,2,F(0))]
        raw=physical=None
    target=[F(6,5)-r**3/12,F(0),F(0),F(0),F(0),F(2)]
    g=mm(pins,tr(pins))
    c=mm(v,tr(pins))
    regression=mm(c,inv(g))
    mean=mv(regression,target)
    factor=sub(v,mm(regression,pins))
    covariance=sub(mm(v,tr(v)),mm(regression,tr(c)))
    field_regression=mm(tr(pins),inv(g))
    return {'P':pins,'V':v,'target':target,'mean':mean,'factor':factor,
            'G':g,'C':c,'regression':regression,'covariance':covariance,
            'raw_pins':raw,'physical':physical,
            'field_mean':mv(field_regression,target),
            'field_factor':sub(eye(12),mm(field_regression,pins))}


def error2(q, p):
    return (sum(((x-y)**2 for x,y in zip(q['mean'],p['mean'])),F(0))
            + norm2(sub(q['factor'],p['factor'])))


def monomial_integral(n):
    return (F(1,2)**(n+1)-F(-1,2)**(n+1))/(n+1)


def kernel_constants():
    return {'pin5_mass':6*(F(1,4)*monomial_integral(0)-monomial_integral(2)),
            'pin5_second_half':3*(F(1,4)*monomial_integral(2)-monomial_integral(4)),
            'average_second_half':monomial_integral(2)/2,
            'endpoint_abs_first':F(1,2)*(2*F(1,2)**2/2)}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def run(mutant=None):
    q0=model(F(0))
    require(rank(q0['covariance'])==2,'contact rank')
    k=kernel_constants()
    require(k['pin5_second_half']==F(1,40),'pin-kernel second-order constant')
    mean_error=error2({'mean':[F(2)],'factor':[[F(0)]]},
                      {'mean':[F(0)],'factor':[[F(0)]]})
    require((F(0) if mutant=='omit-mean' else mean_error)==4,'mean error is indispensable')
    factor_error=error2({'mean':[F(0)],'factor':[[F(1)]]},
                       {'mean':[F(0)],'factor':[[F(-1)]]})
    require((F(0) if mutant=='covariance-only' else factor_error)==4,
            'equal marginal covariances do not fix a coupling')
    rows=[]
    for j in range(7):
        r=F(1,2**j);q=model(r)
        want=[F(6,5),0,0,F(6,5)-r**3/6,0,0]
        if mutant=='reverse-gap':
            want[3]=F(6,5)+r**3/6
        require(mv(q['raw_pins'],q['field_mean'])==want,'exact height-gap orientation')
        require(norm2(mm(q['raw_pins'],q['field_factor']))==0,'pins retain zero residual')
        require(mm(q['factor'],tr(q['factor']))==q['covariance'],'Schur covariance')
        require(norm2(mm(q['factor'],tr(q['P'])))==0,'residual orthogonality')
        e2=error2(q,q0)
        scale=r**4 if mutant=='quadratic-endpoints' else r**2
        require(e2<=2*scale,'first-order endpoint error, not second-order')
        require(rank(q['covariance'])==6,'positive-radius rank')
        rows.append({'r':str(r),'e2_over_r2':str(e2/r**2)})
    return {'scope':'finite polynomial Gaussian diagnostic, not periodic-field or Lean evidence',
            'rungs':rows,'contact_rank':2,'positive_radius_rank':6,'passed':True}


def main():
    p=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--mutant',choices=['omit-mean','covariance-only','reverse-gap','quadratic-endpoints'])
    args=p.parse_args()
    try:
        out=run(args.mutant)
    except ValueError as exc:
        print('REGRESSION_RATE_FAIL: '+str(exc))
        return 1
    print(json.dumps(out,sort_keys=True))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
