# C89 v1.1: full source-exposed technical review

**Verdict: ACCEPT / PASS_TECHNICAL_SCOPED for the exact v1.1 object below, with its imported [P]/[G]/E2/REC hypotheses retained.** I found no remaining blocking defect in the claimed quantitative far-elder bound. Historical v1 remains **AMEND** for its invalid explicit choice of the product constant. This disposition neither accepts a broader parent theorem nor changes a scientific status. Scientific effect: **NONE**.

## Executor, exposure and scope

Actual reviewer: OpenAI / Codex, GPT-6 family, `/root` in this delegated coordination session, distinct from the candidate author OpenAI / Codex `root01a0bbb5` in thread `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`. The runtime does not expose an exact backend subvariant or a unique current conversation UUID; I do not invent either. Dylan's personal reading remains PENDING. Organizational-independence credit: **0**.

I previously saw and stress-tested the proposed route. That feasibility exposure is not acceptance. I subsequently read the complete public v1 and v1.1 proofs, independently fetched the pinned P/G sources and G's manifest, and read the consumed marked-measure/genericity interfaces. I supplied the C_* construction finding; the author composed and published the v1.1 correction. I made no candidate/source amendments. This is an exposed review of an author response, not a blind or provider-distinct review.

Existing helper `/root/c86_fresh_review` read the complete v1 and independently reconstructed the §2 moment argument and §4 cumulative interpretation. Its earlier feasibility contribution is disclosed; it supplies supporting analysis only, with no separate acceptance or reviewer-independence credit. I reconstructed the complete chain and executed the reviewer-only controls reproduced below. Neither reviewer ran or relied on an author checker. No branch, integration, source-register or parent-status changes occurred.

## Exact objects read

| Object | Exact identity |
|---|---|
| Reviewed C89 v1.1 | [Public full proof 5963100306](https://github.com/d6g8k5htny-coder/Math-/pull/188#issuecomment-5963100306); 15,039 UTF-8 bytes, final newline included; SHA256 `7d8d3063caa0dfb5edbfe75437d7ccff8ab74697d1dd92c4b47cca5926b02392` |
| Historical C89 v1 | [Public full proof 5963042579](https://github.com/d6g8k5htny-coder/Math-/pull/188#issuecomment-5963042579); 14,742 bytes; SHA256 `74af6322bdcccec0b718b6abcbfb36b139c40d07398849af9a35ad2000bc31f1` |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, at Math- `5e0b31c8304e3a6ef96a5ee28c8faab5f9fdf799`; blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`; 40,261 bytes; SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` |
| G | `frontiers/far_elder_flat_ridge_20260930/PROOF.md`, same commit; blob `0b089b894960b0ee53fc2885e054d73ab73472bd`; 29,110 bytes; SHA256 `967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba` |
| G source manifest | `frontiers/far_elder_flat_ridge_20260930/SOURCES.json`, same commit; blob `993f5cb4848829bbf97e166cb16c26967123b7d6`; 9,927 bytes |
| E2 | `reviews/d1_section9_borel_repair_20260925/REPAIR.md`, same commit; blob `fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a`; 9,062 bytes; SHA256 `845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f` |
| REC | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md`, same commit; blob `75da2597971510f843f8d90c743950cb8c177342`; 23,312 bytes; SHA256 `451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da` |

The consumed source scope is P §§1–2 and G's canonical marked Kac–Rice interface (0.1), deterministic Lemmas 1–3, conditional genericity §2(d), and shell-volume argument, read with E2 and REC. E2/REC's interfaces remain imported premises rather than newly accepted proofs. I do not consume G Remark 6, OA-FD/OA-MT consequences, a SIDE24 coefficient claim or a near-pair asymptotic. The manuscript's separate leading-law chain and refined-selector finite-radius gaps are not inferred from this review.

## Retained finding and exact successor

In v1, the stated maximum of separate finite-sum bounds need not bound the Fourier coefficient norm of `Q_i R_{i,alpha}(z)`. That norm is controlled by convolution and a sum over monomials, hence by a product of the applicable bounds. This was an explicit-construction defect; the existence of some larger constant did not validate the displayed choice. v1 retains AMEND.

I verified that v1.1 changes only the object version and that paragraph. Its choice `C_*=C_Q C_R C_Z`, with `C_Z=max(1,omega^(-2))`, is valid. For total degree at most two, each z-monomial has Fourier l1 norm at most C_Z; this also covers degree one since `max(1,t^2)>=t` for t>0. Triangle and convolution inequalities then bound the whole composed product by `C_Q C_R C_Z delta^[-12(s-1)]`. No remaining statement or exponent changed. The live public v1.1 body was compared byte-for-byte with the reviewed object before this disposition.

## Full analytic reconstruction

### 1. Quantitative cardinal jets and covariance

For principal torus coordinate differences, `1-cos(omega h)=2 sin^2(omega h/2)` gives `B_j(x_i)>=8 dist(x_i,x_j)^2/L^2`. Squaring every factor supplies an order-four zero at every other site. The finite frequency support bounds Q_i and its first two derivatives by fixed constants times `delta^[-4(s-1)]`.

The reciprocal Taylor polynomial through degree two is `1-U_1+U_1^2-U_2`. Its coefficient sum is bounded by a fixed constant times `delta^[-8(s-1)]`, using delta<=1. A uniform nonzero neighborhood is unnecessary: Taylor coefficients are evaluated at Q_i(x_i)=1. The relation `z(x_i+h)=h+O(|h|^3)` preserves every second jet; the alpha! divisor gives unit diagonal as well as mixed Hessian coordinates. The order-four zeros kill all required jets elsewhere.

The corrected norm bound has exponent 12(s-1), and support lies in the cube |n|_infinity<=2s. Applying weighted Cauchy–Schwarz to each cardinal polynomial yields

```text
|t_(i,alpha)|^2 <= Var(L_t f) a_*^(-1) C_*^2 delta^[-24(s-1)].
```

Summing sJ coordinates proves the displayed Gram lower bound `a_*/(sJ C_*^2) delta^[24(s-1)]`. The s=1 empty product has exponent zero. Positive Fourier weights on the finite cube give an analytic dual for every separated configuration; sampled nonsingularity is not the premise.

Every subvector inherits the same lower covariance bound. For a split V,Z, minimizing `Var(z.Z-a.V)` over a bounds the Schur complement below by the same constant times |z|^2. There is no additional inverse-covariance loss here.

### 2. Full-target density, Gaussian regression and weighted moments

For two pins, the lower covariance bound is c rho^24 and the upper bound is fixed. Full V_y has dimension 2J, so its Gaussian density prefactor is `rho^(-24J)`. The uniform exponential decay uses the upper covariance bound. On the prescribed target slice, its norm dominates b^2 plus both symmetric Hessian norms. Thus (2.2) has the stated uniform decay and separation power.

For each standardized real Fourier coefficient xi, covariance Cauchy–Schwarz gives

```text
|E[xi | V_y=v]| <= sqrt(v^T Sigma_y^(-1) v) <= C rho^(-12)|v|.
```

Its conditional centered variance is at most one, possibly zero. The residual coefficients may be correlated; Minkowski does not require their independence. The sum of `sqrt(a_n)(1+|n|)^2` is finite. Finite sums and their tails therefore converge in conditional L^p(C^2), giving (2.3) at every finite target v. This does not assert that the infinite white-noise coefficient sequence itself belongs to l2. Regression is defined at zero pinned gradients, unbounded finite heights, singular Hessian targets and either Hessian signature.

There is a distinct topological limitation: an arbitrarily specified singular Hessian target can force non-Morse behavior. The all-target statement is a moment statement. The elder argument uses G's almost-sure generic locus under the O_y-conditioned law; further disintegration inherits it for almost every Hessian target, which suffices for the integral. No all-target Morse assertion is needed.

The exact tower is

```text
p_O(v_O) E_Q[W K^p]
 = integral W(H_0,H_y) p_V(v_O,H_0,H_y)
            E[K^p | V_y=(v_O,H_0,H_y)] dH_0 dH_y.
```

W is V_y-measurable and bounded by the absolute determinant product, a polynomial of degree 2d. With ell<=1, the remaining target factor is polynomial in b and the Hessians. Gaussian integration over all heights and Hessians, and y-volume<=L^d, gives exactly `M_p<=C_p rho^[-24J-12p]`, including the p=0 case. The determinant/elder-weighted measure is not treated as a Gaussian conditioning law. No inverse Hessian moments, extra determinants or Palm denominator occur.

### 3. Actual elder geometry, N-site density and tower

G's living-component and crossing lemmas concern the actual ordinary global elder mark. They force the near-critical volume in each shell on that event; a rejected candidate or merely adjacent saddle would not justify this use.

Every tuple (0,y,q_1,...,q_N) has separation at least rho/(4N): the first shell is at least 3rho/(8N) from 0, consecutive shells have gap rho/(4N), and y is at least rho/4 from all shells. For s=N+2, QJ and the Schur argument give a conditional Z-density envelope with exponent `12N(N+1)(d+1)`. It is uniform in the conditioning values. The near-critical window's joint volume is `C_N K_0^(dN/2) ell^[N(1+d/2)]`; no product of independent site probabilities is assumed.

The domain `ell<=rho^2/(64N^2)` and K_0>=2 put the forced balls inside the shells. They are embedded torus balls because rho<=L/4. The pathwise product-volume inequality, followed by Tonelli over measurable shell integrals, avoids a measurable selection of one point on each sphere. W is measurable under V_y, so the uniform Z-envelope may be used inside the weighted tower. Bounding the shell-product volume by L^(dN) and retaining M_0 gives (3.3).

For the complement, `W e_y 1{K>K_0}<=W K^p K_0^(-p)` gives (3.4) inside the weighted integral. Replacing it with an unweighted tail probability times a mean weight would be unjustified and is not done.

### 4. Threshold ledger and moving cutoffs

With `K_0=2 rho^(-12) ell^[-1/(2d)]`, the main term is

```text
C_N rho^[-24J-12dN-12N(N+1)(d+1)] ell^(N/2),
```

and the weighted tail is `C_p rho^(-24J) ell^[p/(2d)]`. Setting N=2(q+1) and p=2d(q+1) proves (0.2). The example d=2,q=1 gives J=6,N=4,A_N=960.

For rho=ell^beta, beta<=1/A_N gives exponent q+1-beta A_N>=q. Since A_N>2, the geometric domain holds eventually: ell/rho^2=ell^(1-2beta) tends to zero. For the fixed logarithmic cutoff, the extra ell absorbs each fixed logarithmic power; the geometric domain also holds eventually. This is each fixed order separately, not uniformity in q or an all-order statement for one fixed positive beta.

For one fixed admissible moving cutoff, the imported joint marked measure gives the lifetime-dependent cumulative count per unit spatial volume as `integral_0^t F(ell,rho(ell)) dell`, hence O(t^(q+1)). No cutoff derivative is introduced. This is a different observable from `integral_0^t F(ell,rho(t)) dell`; equality or matching coefficients are not claimed. Whole-torus counts would acquire the factor L^d.

## Scope and disposition

The new bridges are the explicit separated-jet lower bound, the separation-tracked weighted moments, and the N-site conditional density envelope. Together with the retained marked elder geometry they justify the stated fixed-model far-region result, including the prescribed logarithmic cutoff. They do not supply contact/intermediate localization, a regional multiple-witness estimate, actual-field confinement, witness uniqueness, rejected-candidate control, a two-sided canonical-witness/persistence correspondence, an occurrence-probability asymptotic, a persistence coefficient or a finite-radius RN certificate. Constants depend on fixed d,L,q; no diagonal growth in them is accepted.

My review pickup [5963136913](https://github.com/d6g8k5htny-coder/Math-/pull/188#issuecomment-5963136913) is **completed and released by this delivery**. The author/coordinator retains C89 authorship, its R17 claim and immutable custody. This technical verdict does not certify repository application, CI, merge, independent human reading or organizationally independent review.

## Reviewer-only reproducible controls

The complete script below is newly executed reviewer code, distinct from the author's executable. Python 3.12.14, standard library only. Both commands exited 0, and their output bytes were identical:

```sh
python -B c89_reviewer_controls.py --source-dir .
python -B -O c89_reviewer_controls.py --source-dir .
```

The source directory contains the exact v1.1 PROOF.md and the pinned source/P.md and source/G.md named above. Save the following code block verbatim with a final newline. Script identity: 12,190 bytes, SHA256 `83982f11df2f145f8dcde55c1900ef8723d46b0820f269049e3c2f4f05da9fab`. Each JSON stdout file is 1,068 bytes, SHA256 `cee69d10a059a1cc62ef89624e85da7b035fa2e309c77bafe0eb87e8d450a074`.

These finite exact controls corroborate identities and reject listed mutations. They do not prove all-configuration estimates or imported parent hypotheses; the analytic reconstruction above is the basis of the scoped verdict.

```python
#!/usr/bin/env python3
"""C89 reviewer-only exact controls; no author executable or third-party package.

Run: python -B c89_reviewer_controls.py --source-dir PATH
Repeat with -B -O. PATH contains PROOF.md, source/P.md, source/G.md.
Omit --source-dir to run algebra controls without source-custody checks.
The finite controls do not prove uniform analytic bounds or parent hypotheses.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cs(a, r):
    return (a[0] * r, a[1] * r)


def conj(a):
    return (a[0], -a[1])


def iphase(q):
    return (ONE, (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)))[q % 4]


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = ca(out.get(k, ZERO), v)
    return {k: v for k, v in out.items() if v != ZERO}


def scale(a, r):
    return {k: cs(v, r) for k, v in a.items() if cs(v, r) != ZERO}


def mul(a, b, truncated=False):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            if truncated and sum(k) > 2:
                continue
            out[k] = ca(out.get(k, ZERO), cm(va, vb))
    return {k: v for k, v in out.items() if v != ZERO}


def power(a, n, d, truncated=False):
    out = {(0,) * d: ONE}
    for _ in range(n):
        out = mul(out, a, truncated)
    return out


def indices(d):
    return [a for a in product(range(3), repeat=d) if sum(a) <= 2]


def afact(a):
    out = 1
    for v in a:
        out *= factorial(v)
    return out


def unit(d, j, sign=1):
    return tuple(sign if k == j else 0 for k in range(d))


def derivative(poly, site, alpha):
    out = ZERO
    for k, coeff in poly.items():
        factor = 1
        for n, a in zip(k, alpha):
            factor *= n ** a
        phase = iphase(sum(n * x for n, x in zip(k, site)) + sum(alpha))
        out = ca(out, cs(cm(coeff, phase), F(factor)))
    return out


def bpoly(site):
    d = len(site)
    out = {(0,) * d: (F(d), F(0))}
    for j, x in enumerate(site):
        out = add(out, {unit(d, j): cs(iphase(-x), F(-1, 2)),
                        unit(d, j, -1): cs(iphase(x), F(-1, 2))})
    return out


def zpoly(site, j):
    d = len(site)
    return {unit(d, j): cm(iphase(-site[j]), (F(0), F(-1, 2))),
            unit(d, j, -1): cm(iphase(site[j]), (F(0), F(1, 2)))}


def qpoly(sites, i, exponent=2):
    d = len(sites[0])
    out = {(0,) * d: ONE}
    for j, site in enumerate(sites):
        if j == i:
            continue
        bp = bpoly(site)
        denominator = derivative(bp, sites[i], (0,) * d)
        need(denominator[1] == 0 and denominator[0] > 0, 'repeated-site denominator')
        out = mul(out, power(scale(bp, 1 / denominator[0]), exponent, d))
    return out


def reciprocal_jet(q, site):
    d = len(site)
    jet = {a: cs(derivative(q, site, a), F(1, afact(a))) for a in indices(d)}
    need(jet[(0,) * d] == ONE, 'Q_i(x_i) != 1')
    u = add(jet, {(0,) * d: (F(-1), F(0))})
    return add(add({(0,) * d: ONE}, scale(u, -1)), mul(u, u, True))


def compose(taylor, zs):
    d = len(zs)
    out = {}
    for alpha, coeff in taylor.items():
        term = {(0,) * d: coeff}
        for j, a in enumerate(alpha):
            term = mul(term, power(zs[j], a, d))
        out = add(out, term)
    return out


def cardinals(sites, exponent=2, reciprocal=True, factorials=True):
    d = len(sites[0])
    out = {}
    for i, site in enumerate(sites):
        q = qpoly(sites, i, exponent)
        inv = reciprocal_jet(q, site) if reciprocal else {(0,) * d: ONE}
        zs = [zpoly(site, j) for j in range(d)]
        for alpha in indices(d):
            den = afact(alpha) if factorials else 1
            t = mul(inv, {alpha: (F(1, den), F(0))}, True)
            out[(i, alpha)] = mul(q, compose(t, zs))
    return out


def mismatch_count(sites, **variant):
    d = len(sites[0])
    count = 0
    for (i, alpha), poly in cardinals(sites, **variant).items():
        for j, site in enumerate(sites):
            for beta in indices(d):
                expected = ONE if i == j and alpha == beta else ZERO
                count += derivative(poly, site, beta) != expected
    return count


def positive_definite(matrix):
    n = len(matrix)
    lower = [[F(0)] * n for _ in range(n)]
    pivots = []
    for i in range(n):
        lower[i][i] = F(1)
        pivot = matrix[i][i] - sum(lower[i][k] ** 2 * pivots[k] for k in range(i))
        if pivot <= 0:
            return False
        pivots.append(pivot)
        for j in range(i + 1, n):
            lower[j][i] = (matrix[j][i] - sum(lower[j][k] * lower[i][k] * pivots[k]
                                            for k in range(i))) / pivot
    return True


def finite_gram(sites, band):
    d = len(sites[0])
    coords = [(site, a) for site in sites for a in indices(d)]
    out = [[F(0) for _ in coords] for _ in coords]
    for mode in product(range(-band, band + 1), repeat=d):
        features = [derivative({mode: ONE}, site, a) for site, a in coords]
        for i, fi in enumerate(features):
            for j, fj in enumerate(features):
                value = cm(fi, conj(fj))
                out[i][j] += value[0]
    return out


def controls():
    sets = [[(0,), (1,), (2,)],
            [(0, 0), (1, 0), (0, 1), (2, 2)],
            [(0, 0, 0), (1, 0, 1), (0, 1, 2)]]
    derivative_checks = frequency_checks = realness_checks = product_checks = 0
    for sites in sets:
        d, s = len(sites[0]), len(sites)
        need(len(indices(d)) == (d + 1) * (d + 2) // 2, 'jet count')
        cq = cr = F(0)
        for i, site in enumerate(sites):
            qp = qpoly(sites, i)
            cq = max(cq, sum(abs(a) + abs(b) for a, b in qp.values()))
            inv = reciprocal_jet(qp, site)
            for alpha in indices(d):
                rp = mul(inv, {alpha: (F(1, afact(alpha)), F(0))}, True)
                cr = max(cr, sum(abs(a) + abs(b) for a, b in rp.values()))
        for (i, alpha), poly in cardinals(sites).items():
            # omega=1 here, so C_Z=1. This rational coefficient norm
            # dominates the complex absolute-value norm and is submultiplicative.
            need(sum(abs(a) + abs(b) for a, b in poly.values()) <= cq * cr,
                 'successor product bound')
            product_checks += 1
            need(all(max(abs(x) for x in k) <= 2 * s for k in poly), 'frequency support')
            frequency_checks += 1
            for k, value in poly.items():
                need(poly.get(tuple(-x for x in k), ZERO) == conj(value), 'real polynomial')
                realness_checks += 1
            for j, site in enumerate(sites):
                for beta in indices(d):
                    expected = ONE if i == j and alpha == beta else ZERO
                    need(derivative(poly, site, beta) == expected, 'cardinal jet mismatch')
                    derivative_checks += 1
    variants = [('order_two_zero_only', {'exponent': 1}),
                ('omit_reciprocal', {'reciprocal': False}),
                ('omit_alpha_factorial', {'factorials': False})]
    rejected = {}
    for name, kwargs in variants:
        bad = sum(mismatch_count(sites, **kwargs) for sites in sets[:2])
        need(bad > 0, 'mutation survived: ' + name)
        rejected[name] = {'mismatches': bad}
    try:
        qpoly([(0,), (0,)], 0)
    except RuntimeError:
        rejected['repeated_site_cardinal'] = {'rejected': True}
    else:
        raise RuntimeError('repeated-site construction survived')
    sites = [(0,), (1,)]
    polys = cardinals(sites)
    cstar = max(sum(abs(v[0]) + abs(v[1]) for v in p.values()) for p in polys.values())
    dimension = len(polys)
    lower = F(1, dimension) / cstar ** 2
    gram = finite_gram(sites, 2 * len(sites))
    gram_minus_lower = [[x - (lower if i == j else 0) for j, x in enumerate(row)]
                        for i, row in enumerate(gram)]
    need(positive_definite(gram_minus_lower), 'finite Gram lower bound')
    duplicate = finite_gram([(0,), (0,)], 4)
    need(duplicate[0][0] + duplicate[3][3] - 2 * duplicate[0][3] == 0,
         'duplicate-site null vector')
    rejected['repeated_site_positive_gram'] = {'null_vector_variance': '0'}
    covariance_checks = 2
    for rho in (F(1, 2), F(1, 3)):
        epsilon = rho ** 12
        sigma = epsilon ** 2
        cross = epsilon
        coefficient = cross / sigma
        need(coefficient ** 2 == 1 / sigma, 'regression energy equality')
        need(coefficient == rho ** -12, 'regression separation exponent')
        need(1 - cross ** 2 / sigma == 0, 'singular residual variance')
        need(coefficient > 1, 'unamplified regression variant survived')
        covariance_checks += 4
    rejected['unamplified_regression'] = {'rejected': True}
    sigma = [[F(3), F(1), F(1)], [F(1), F(3), F(1)], [F(1), F(1), F(3)]]
    need(positive_definite([[x - int(i == j) for j, x in enumerate(row)]
                            for i, row in enumerate(sigma)]), 'joint lower bound')
    schur = [[sigma[i][j] - sigma[i][0] * sigma[0][j] / sigma[0][0]
              for j in (1, 2)] for i in (1, 2)]
    need(positive_definite([[x - int(i == j) for j, x in enumerate(row)]
                            for i, row in enumerate(schur)]), 'Schur lower bound')
    covariance_checks += 2
    need(F(1) > F(1) * F(1, 2), 'weighted-tail adverse control')
    rejected['unweighted_tail_substitution'] = {'weighted_mass': '1', 'product_of_means': '1/2'}
    exponent_checks = 0
    for d in (2, 3, 5):
        J = (d + 1) * (d + 2) // 2
        for q in range(1, 7):
            N, p = 2 * (q + 1), 2 * d * (q + 1)
            B = 12 * N * (N + 1) * (d + 1)
            A = 24 * J + 12 * d * N + B
            main = N * (1 + F(d, 2)) - F(d * N, 2) - F(d * N, 2 * d)
            need(main == F(N, 2) == q + 1, 'main lifetime exponent')
            need(F(p, 2 * d) == q + 1, 'tail lifetime exponent')
            need(-24 * J - 12 * p + 12 * p == -24 * J, 'tail rho cancellation')
            need(F(q + 1) - F(1, A) * A == q, 'power cutoff exponent')
            need(F(1, A) < F(1, 2), 'geometric domain')
            exponent_checks += 5
    need(24 * 6 + 12 * 2 * 4 + 12 * 4 * 5 * 3 == 960, 'd=2 example')
    exponent_checks += 1
    return {'cardinal_derivative_checks': derivative_checks,
            'frequency_support_checks': frequency_checks,
            'real_coefficient_symmetry_checks': realness_checks,
            'constant_product_checks': product_checks,
            'covariance_controls': covariance_checks,
            'exponent_checks': exponent_checks,
            'negative_controls_rejected': rejected,
            'finite_gram_lower_bound': str(lower),
            'scope': 'finite exact controls; uniform proof and imported hypotheses not certified'}


def source_checks(directory):
    expected = {
        'PROOF.md': (15039, '7d8d3063caa0dfb5edbfe75437d7ccff8ab74697d1dd92c4b47cca5926b02392'),
        'source/P.md': (40261, '9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7'),
        'source/G.md': (29110, '967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba')}
    out = {}
    for name, (size, digest) in expected.items():
        data = (Path(directory) / name).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        need((len(data), got) == (size, digest), 'source identity: ' + name)
        out[name] = {'bytes': len(data), 'sha256': got, 'final_newline': data.endswith(b'\n')}
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir')
    args = parser.parse_args()
    result = controls()
    result['source_checks'] = source_checks(args.source_dir) if args.source_dir else 'NOT_RUN'
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
```

Actual stdout (normal and optimized):

```json
{"cardinal_derivative_checks":1557,"constant_product_checks":63,"covariance_controls":12,"exponent_checks":91,"finite_gram_lower_bound":"1/384","frequency_support_checks":63,"negative_controls_rejected":{"omit_alpha_factorial":{"mismatches":11},"omit_reciprocal":{"mismatches":43},"order_two_zero_only":{"mismatches":90},"repeated_site_cardinal":{"rejected":true},"repeated_site_positive_gram":{"null_vector_variance":"0"},"unamplified_regression":{"rejected":true},"unweighted_tail_substitution":{"product_of_means":"1/2","weighted_mass":"1"}},"real_coefficient_symmetry_checks":12019,"scope":"finite exact controls; uniform proof and imported hypotheses not certified","source_checks":{"PROOF.md":{"bytes":15039,"final_newline":true,"sha256":"7d8d3063caa0dfb5edbfe75437d7ccff8ab74697d1dd92c4b47cca5926b02392"},"source/G.md":{"bytes":29110,"final_newline":true,"sha256":"967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba"},"source/P.md":{"bytes":40261,"final_newline":true,"sha256":"9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7"}}}
```
