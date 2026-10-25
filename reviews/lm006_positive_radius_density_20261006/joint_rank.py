"""Standard-library exact diagnostics for the two-site 12-jet Fourier witness.

Complex values are pairs of Fractions. Polynomial identities and selected unit
phases are exact; this program does not enclose Gaussian covariances or prove a
uniform small-r eigenvalue floor. See NOTE.md for the all-r analytic argument.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial, prod
import json


def qc(a=0, b=0, denominator=1):
    return F(a)/denominator, F(b)/denominator


def add(x,y): return x[0]+y[0], x[1]+y[1]
def sub(x,y): return x[0]-y[0], x[1]-y[1]
def mul(x,y): return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def divide(x,y):
    d=y[0]**2+y[1]**2
    if d==0: raise ZeroDivisionError('zero Gaussian rational')
    return (x[0]*y[0]+x[1]*y[1])/d, (x[1]*y[0]-x[0]*y[1])/d


def power(x,n):
    if type(n) is not int or n<0: raise ValueError('nonnegative integer exponent required')
    result=qc(1)
    while n:
        if n&1: result=mul(result,x)
        x=mul(x,x); n//=2
    return result


MODES=tuple([(n,0) for n in range(6)]+[(n,1) for n in range(4)]+[(n,2) for n in range(2)])
PHASES=(qc(-1),qc(0,1),qc(0,-1),qc(3,4,5),qc(-3,4,5),qc(3,-4,5),
        qc(5,12,13),qc(8,15,17),qc(9999,200,10001))


def witness(z):
    """Rows are MODES; columns are transverse falling-degree 0,1,2 blocks.

    In each transverse block put M columns then S columns, horizontal degrees
    0..2-b. All S entries acquire z**n. The degree-2 transverse symbol m(m-1)
    is an invertible triangular change from the normalized ordinary jet basis.
    """
    rows=[]
    for n,m in MODES:
        row=[]
        for b in range(3):
            transverse=(1,m,m*(m-1))[b]
            for site in range(2):
                for a in range(3-b):
                    row.append(mul(qc(transverse*n**a),power(z,n*site)))
        rows.append(row)
    return rows


def eliminate(matrix):
    """Exact row elimination, returning determinant (square only) and rank."""
    a=[list(row) for row in matrix]
    if not a or not a[0] or any(len(row)!=len(a[0]) for row in a):
        raise ValueError('nonempty rectangular matrix required')
    rows,cols=len(a),len(a[0]); rank=0; determinant=qc(1)
    for column in range(cols):
        pivot=next((i for i in range(rank,rows) if a[i][column]!=qc(0)),None)
        if pivot is None: continue
        if pivot!=rank:
            a[pivot],a[rank]=a[rank],a[pivot]
            determinant=mul(qc(-1),determinant)
        value=a[rank][column]; determinant=mul(determinant,value)
        for i in range(rank+1,rows):
            factor=divide(a[i][column],value)
            for k in range(column,cols): a[i][k]=sub(a[i][k],mul(factor,a[rank][k]))
        rank+=1
        if rank==rows: break
    if rows!=cols or rank<rows: determinant=qc(0)
    return determinant,rank


def block_polynomial(j):
    """Leibniz determinant of [n^k | n^k z^n], n=0..2j-1, k=0..j-1.

    Small j<=3 keeps this independent exact expansion bounded (at most720
    permutations). It does not use the expected confluent-Vandermonde formula.
    """
    if type(j) is not int or not 1<=j<=3: raise ValueError('j must be 1, 2 or 3')
    out={}
    for permutation in permutations(range(2*j)):
        inv=sum(permutation[i]>permutation[k] for i in range(2*j) for k in range(i+1,2*j))
        coefficient=(-1)**inv
        degree=0
        for n,column in enumerate(permutation):
            coefficient*=n**(column%j)
            if column>=j: degree+=n
        out[degree]=out.get(degree,0)+coefficient
    return {k:v for k,v in out.items() if v}


def expected_block(j):
    base=j*(j-1)//2; c=prod(factorial(k) for k in range(j))**2
    return {base+k:c*comb(j*j,k)*(-1)**(j*j-k) for k in range(j*j+1)}


def typed_weight(r,v):
    am,ap,bm,bp,cm,cp=map(F,v)
    minus=lambda x:max(-x,F(0))
    return max(minus(am)*minus(cm)-r*bm*bm,F(0))*max(r*bp*bp-ap*cp,F(0))


def require(condition,message):
    if not condition: raise ValueError(message)


def main():
    for j in (1,2,3): require(block_polynomial(j)==expected_block(j),'block polynomial mismatch')
    for z in PHASES:
        require(z[0]**2+z[1]**2==1 and z!=qc(1),'invalid selected unit phase')
        det,rank=eliminate(witness(z))
        require(rank==12 and det==mul(qc(16),mul(power(z,4),power(sub(z,qc(1)),14))),
                'full-rank determinant mismatch')
    collision=eliminate(witness(qc(1)))[1]
    require(collision==6,'collision falsely treated as full rank')
    omitted=eliminate(witness(qc(0,1))[:-1])[1]
    require(omitted==11,'missing-mode control failed')
    duplicate=witness(qc(0,1))
    for row in duplicate: row[-1]=row[-2]
    duplicate_rank=eliminate(duplicate)[1]
    require(duplicate_rank==11,'duplicate-jet control failed')
    print(json.dumps(dict(symbolic_blocks=3,full_rank_unit_phases=len(PHASES),
                         full_rank=12,collision_rank=collision,missing_mode_rank=omitted,
                         duplicated_jet_rank=duplicate_rank,arithmetic='exact Fraction pairs',
                         uniform_covariance_floor_claimed=False,scientific_effect='NONE'),sort_keys=True))

if __name__=='__main__': main()
