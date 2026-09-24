"""Exact finite controls for three analytic candidates; not a continuum prover.
Standard library only. All matrices and probabilities use rational arithmetic.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb
import json


def rational(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError('exact rational input required')
    if not isinstance(value, (int, Q)):
        raise ValueError('exact rational input required')
    return Q(value)


def matrix(rows):
    a=tuple(tuple(rational(x) for x in row) for row in rows)
    if len(a)>7 or any(len(row)!=len(a) for row in a):
        raise ValueError('square matrix of order at most seven required')
    return a


def det(rows):
    a=[list(row) for row in matrix(rows)]
    out=Q(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:
            return Q(0)
        if pivot!=k:
            a[pivot],a[k]=a[k],a[pivot]; out=-out
        p=a[k][k]; out*=p
        for i in range(k+1,len(a)):
            scale=a[i][k]/p
            for j in range(k+1,len(a)):
                a[i][j]-=scale*a[k][j]
    return out


def det_permutations(rows):
    a=matrix(rows); n=len(a)
    if n>5:
        raise ValueError('permutation oracle limited to order five')
    out=Q(0)
    for perm in permutations(range(n)):
        v=Q((-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n): v*=a[i][perm[i]]
        out+=v
    return out


def inertia(rows):
    """Exact symmetric congruence elimination, including 2x2 zero-diagonal pivots."""
    a=matrix(rows)
    if any(a[i][j]!=a[j][i] for i in range(len(a)) for j in range(len(a))):
        raise ValueError('symmetric matrix required')
    neg=zero=pos=0
    while a:
        n=len(a)
        pivot=next((i for i in range(n) if a[i][i]),None)
        if pivot is not None:
            order=[pivot]+[i for i in range(n) if i!=pivot]
            a=tuple(tuple(a[i][j] for j in order) for i in order)
            p=a[0][0]; neg+=p<0; pos+=p>0
            a=tuple(tuple(a[i][j]-a[i][0]*a[0][j]/p for j in range(1,n)) for i in range(1,n))
        else:
            edge=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
            if edge is None:
                zero+=n; break
            i,j=edge; order=[i,j]+[k for k in range(n) if k not in (i,j)]
            a=tuple(tuple(a[i][j] for j in order) for i in order)
            b=a[0][1]; neg+=1; pos+=1
            a=tuple(tuple(a[i][j]-(a[i][0]*a[1][j]+a[i][1]*a[0][j])/b
                          for j in range(2,n)) for i in range(2,n))
    return neg,zero,pos


def filtered_det(rows,index):
    a=matrix(rows)
    if type(index) is not int or not 0<=index<=len(a):
        raise ValueError('invalid negative index')
    neg,zero,_=inertia(a)
    return abs(det(a)) if zero==0 and neg==index else Q(0)


def adjugate_quadratic(a,beta):
    a=matrix(a); beta=tuple(rational(x) for x in beta); n=len(a)
    if len(beta)!=n or not n:
        raise ValueError('nonempty block/vector size mismatch')
    return sum((beta[i]*beta[j]*(-1)**(i+j)*det(tuple(tuple(a[x][y] for y in range(n) if y!=i)
                for x in range(n) if x!=j)) for i in range(n) for j in range(n)),Q(0))


def block(alpha,beta,a,sqrt_t):
    a=matrix(a); beta=tuple(rational(x) for x in beta)
    alpha=rational(alpha); q=rational(sqrt_t)
    if q<0 or len(beta)!=len(a):
        raise ValueError('invalid block dimensions or square root')
    return ((alpha,)+tuple(q*x for x in beta),)+tuple((q*beta[i],)+a[i] for i in range(len(a)))


def block_index_bound(a,beta,r):
    r=rational(r)
    if r<0: raise ValueError('negative radius')
    return r*abs(adjugate_quadratic(a,beta))


def contact_rows(coefficients,r):
    """Exact centered axial rules on a polynomial sum coefficients[j]*x^j."""
    r=rational(r)
    if r<=0: raise ValueError('positive radius required')
    c=tuple(rational(x) for x in coefficients)
    def f(x): return sum((v*x**i for i,v in enumerate(c)),Q(0))
    def fp(x): return sum((i*c[i]*x**(i-1) for i in range(1,len(c))),Q(0))
    a=-r/2; b=r/2
    return ((f(a)+f(b))/2,(f(b)-f(a))/r,(fp(b)-fp(a))/r,
            6/r**2*(fp(a)+fp(b)-2*(f(b)-f(a))/r))


def radial_power(d):
    if type(d) is not int or d<2: raise ValueError('dimension at least two required')
    return (d-1)+3-(d+3)+2


def rate_ledger(split=Q(1,6)):
    split=rational(split)
    if not 0<split<Q(1,4): raise ValueError('split must make r/k small on outer branch')
    return {'inner_contact':Q(7,3)*split,'outer_loss':1-Q(11,3)*split,
            'outer_delta':Q(1,3)-Q(4,3)*split,'lower_cutoff':Q(1,3),
            'density_absolute_error':Q(0),'count_error':Q(1)}


def holder_exponent(p,beta=0):
    p=rational(p); beta=rational(beta)
    if p<=1: raise ValueError('Holder exponent must exceed one')
    return (3*(p-1)-beta)/p


def rare_count(n,p=1):
    """r=2^-n, N=n on an event of probability r^3; exact abstract counterexample."""
    if type(n) is not int or n<1 or type(p) is not int or p<1:
        raise ValueError('positive integer indices required')
    probability=Q(1,8**n)
    return {'radius':Q(1,2**n),'probability':probability,
            'mean':n*probability,'moment':n**p*probability,'conditional_mean':n}


def _positive_ints(values):
    vals=tuple(values)
    if not vals or any(type(x) is not int or x<1 for x in vals):
        raise ValueError('positive integers required')
    return vals


def canonical_edges(b,edges):
    rows=tuple(frozenset(e) for e in edges)
    if any(len(e)<2 or any(type(i) is not int or not 0<=i<b for i in e) for e in rows):
        raise ValueError('crossing edges must have at least two valid macro-indices')
    if len(set(rows))!=len(rows) or any(e<f for e in rows for f in rows):
        raise ValueError('distinct clutter edges required')
    return tuple(sorted((sum(1<<i for i in e) for e in rows)))


@dataclass(frozen=True)
class Model:
    capacities: tuple
    demands: tuple
    edges: tuple

    def __post_init__(self):
        a=_positive_ints(self.capacities); d=_positive_ints(self.demands)
        if len(a)!=len(d) or len(a)>10: raise ValueError('invalid block dimensions')
        edges=canonical_edges(len(a),self.edges)
        sizes=tuple(x*y+1 for x,y in zip(a,d))
        if sum(sizes)>10000: raise ValueError('original-coordinate representation limit exceeded')
        blocks=[]; start=0
        for n in sizes:
            blocks.append(((1<<n)-1)<<start); start+=n
        object.__setattr__(self,'capacities',a); object.__setattr__(self,'demands',d)
        object.__setattr__(self,'edge_masks',edges); object.__setattr__(self,'sizes',sizes)
        object.__setattr__(self,'blocks',tuple(blocks)); object.__setattr__(self,'n',start)
        object.__setattr__(self,'full',(1<<start)-1)

    def valid(self,mask):
        if type(mask) is not int or mask<0 or mask&~self.full: raise ValueError('invalid original-coordinate subset')

    def good(self,mask):
        self.valid(mask)
        support=0
        for i,(block,a) in enumerate(zip(self.blocks,self.capacities)):
            k=(mask&block).bit_count()
            if k>a: return False
            if k: support|=1<<i
        return not any(support&e==e for e in self.edge_masks)

    def avoids_cover(self,mask):
        self.valid(mask)
        return all(mask&b!=b for b in self.blocks)

    def exhaustive_limit(self):
        if self.n>11: raise ValueError('exhaustive checks restricted to at most eleven original coordinates')

    def actual_minimal_forbidden(self):
        self.exhaustive_limit()
        return frozenset(m for m in range(1,self.full+1) if not self.good(m)
                         and all(self.good(m^(1<<i)) for i in range(self.n) if m>>i&1))

    def structural_forbidden(self):
        total=sum(comb(n,a+1) for n,a in zip(self.sizes,self.capacities))
        for e in self.edge_masks:
            count=1
            for i,n in enumerate(self.sizes):
                if e>>i&1: count*=n
            total+=count
        if total>20000: raise ValueError('use the proved compressed witness counts, not enumeration')
        vertices=[tuple(i for i in range(self.n) if b>>i&1) for b in self.blocks]
        out=set()
        for vs,a in zip(vertices,self.capacities):
            for chosen in combinations(vs,a+1): out.add(sum(1<<i for i in chosen))
        for e in self.edge_masks:
            for chosen in product(*(vertices[i] for i in range(len(vertices)) if e>>i&1)):
                out.add(sum(1<<i for i in chosen))
        return frozenset(out)

    def chromatic_table(self):
        self.exhaustive_limit()
        good=[self.good(m) for m in range(self.full+1)]
        @lru_cache(None)
        def colors(m):
            if m==0: return 0
            if good[m]: return 1
            bit=m&-m; best=m.bit_count(); sub=m
            while sub:
                if sub&bit and good[sub]: best=min(best,1+colors(m^sub))
                sub=(sub-1)&m
            return best
        return tuple(colors(m) for m in range(self.full+1))


def palette_optimum(demands,edges):
    d=_positive_ints(demands); b=len(d)
    if b>8 or sum(d)>30: raise ValueError('finite palette optimizer input limit exceeded')
    es=canonical_edges(b,edges)
    allowed=tuple(s for s in range(1,1<<b) if not any(s&e==e for e in es))
    @lru_cache(None)
    def solve(state):
        if not any(state): return 0
        active=sum(1<<i for i,x in enumerate(state) if x)
        return 1+min(solve(tuple(x-((s>>i)&1) for i,x in enumerate(state)))
                     for s in allowed if s&active==s)
    return solve(d)


def uniform_palette(demands,rank):
    d=_positive_ints(demands)
    if type(rank) is not int or not 1<=rank<=len(d): raise ValueError('invalid rank')
    k=max(max(d),(sum(d)+rank-1)//rank)
    if sum(d)>100000: raise ValueError('explicit witness limit exceeded')
    out=[]; offset=0
    for size in d:
        out.append(frozenset((offset+j)%k for j in range(size))); offset+=size
    return k,tuple(out)


def local_generator_cost(prices):
    value=Q(1)
    for p in prices:
        p=rational(p)
        if not 0<=p<=1: raise ValueError('price outside unit interval')
        value*=p
    return value


def probability_of(model,probabilities,predicate):
    model.exhaustive_limit(); probs=tuple(rational(p) for p in probabilities)
    if len(probs)!=model.n or any(not 0<=p<=1 for p in probs): raise ValueError('invalid probability vector')
    result=Q(0)
    for m in range(model.full+1):
        if predicate(m):
            mass=Q(1)
            for i,p in enumerate(probs): mass*=p if m>>i&1 else 1-p
            result+=mass
    return result


def budget_certificate(model,probabilities,prices):
    probs=tuple(rational(p) for p in probabilities); cs=tuple(rational(c) for c in prices)
    if len(probs)!=model.n or len(cs)!=model.n or any(not 0<=c<=p<=1 for c,p in zip(cs,probs)):
        raise ValueError('this theorem requires the same original-coordinate prices c<=p')
    qs=[]; costs=[]; goodproduct=Q(1)
    for block,a in zip(model.blocks,model.capacities):
        qi=probability_of(model,probs,lambda m: (m&block).bit_count()>a)
        cost=local_generator_cost(tuple(cs[i] for i in range(model.n) if block>>i&1))
        qs.append(qi); costs.append(cost); goodproduct*=1-qi
    mu=probability_of(model,probs,model.good)
    return {'cost':sum(costs,Q(0)),'sum_local_failures':sum(qs,Q(0)),
            'good_probability':mu,'product_local_good':goodproduct,
            'local_cost_le_failure':all(c<=q for c,q in zip(costs,qs))}


def large_example():
    n=409; pden=40900
    bad=Q(6*comb(n,2),pden**2)+Q(15,100**4)
    return {'original_vertices':6*n,'internal_minimal_pairs':6*comb(n,2),
            'crossing_minimal_quadruples':15*n**4,'cover_generators':6,
            'cover_palette_optimum':816,'whole_ground_chromatic_number':818,
            'disjoint_palette_count':2448,'failure_upper':str(bad),
            'failure_below_3_over_10000':bad<Q(3,10000),
            'positive_cover_cost':'6/(40900^409)',
            'enumerated_large_witnesses':False}


def output():
    return {'object':'THREE-FRONTS-20260924-v1','scientific_acceptance':False,
            'lifetime':{'candidate_absolute_remainder':'O(1)','nonselected_density':'O(1)',
                        'finite_bar_absolute_remainder':'O(1)','relative_remainder':'O(ell^(1/3))',
                        'numeric_constants_evaluated':False,
                        'scope':'fixed d>=2,L>0; all marks and separations; parent interfaces conditional'},
            'rate_ledger':{k:str(v) for k,v in rate_ledger().items()},
            'rn':{'uniform_L2_only_exponent':str(holder_exponent(2)),
                  'uniform_L4_only_exponent':str(holder_exponent(4)),
                  'all_fixed_moments_do_not_imply_cubic':True,'triple_integral_evaluated':False},
            'p15':large_example()}


if __name__=='__main__':
    print(json.dumps(output(),indent=2,sort_keys=True))
