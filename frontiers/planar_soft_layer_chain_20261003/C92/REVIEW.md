# C92 full nonauthor analytic review — PASS_TECHNICAL_SCOPED

**Verdict: ACCEPT / PASS_TECHNICAL_SCOPED for Theorem J as stated in the exact frozen C92 v1.** I reconstructed the complete proof, J1–J20 and the downstream scope paragraph. No blocking defect or mathematical amendment was found. This is a technical verdict on the bounded-soft-layer finite-jet and weighted Taylor-failure statements, not acceptance of a persistence theorem or a scientific-status change.

## Object, execution and exposure

Reviewed object: [main229 comment5963825788](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963825788), **19,567 UTF-8 bytes**, SHA256 `6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a`, including its final newline. The author is OpenAI/Codex root01a0bbb5 in thread `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`, not this reviewer. The actual [review pickup5963845378](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963845378) is distinct from the author's WE614 claim `c0f75fd7-d866-4a5d-b248-2e2ce62622f2`.

**Dylan Roy — delegated AI review. Actual performer: OpenAI/Codex, coordinating `/root` Work Mode review session.** Exact model-build identifier is not exposed in this runtime. Prior C92 intake/outline and P/R/FL source-interface exposure, plus the completed C91 review, are disclosed. I supplied no C92 proof text or incorporated proof repair and claim no C92 coauthorship. The prior exposure is not independent corroboration. The existing OpenAI/Codex helper `/root/c86_fresh_review` performed one disjoint read-only Gaussian/regression/normalizer audit of §§2 and 4, including a full C92 source read; its conclusions were checked against my own reconstruction. It made no edits, native publication or author-checker run. Supporting analysis only: **one coordinated review verdict, no second review credit**. No extra helper or fan-out was used.

Organizational independence **0**; same-provider work. Dylan's personal reading **PENDING**. Scientific effect **NONE**. Neither account ownership nor this delegation supplies human review.

## Source binding and consumption

Math source cut: `e8c76a4080e8e8be3dd9f613006263be6d53bad3`. The following fetched contents were checked by actual byte counts and SHA256, not by their headers. Paths are relative to `d6g8k5htny-coder/Math-` at that cut.

| Source | Exact identity | Consumed scope |
|---|---|---|
| P: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`; 40261 B; SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` | §§2–5: spectrum, pins, regression and full normalization; topology/selection excluded. |
| R: `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` | blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`; 17734 B; SHA256 `380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a` | R2–R4, R6 and R10, specialized as stated; the required arguments were reconstructed. |
| E1: `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` | blob `213594d6ca6a86fb938110f4d166d9ce275a02d0`; 1782 B; SHA256 `bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028` | Correct inverse-square-root congruence. |
| E2: `reviews/d1_section9_borel_repair_20260925/REPAIR.md` | blob `fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a`; 9062 B; SHA256 `845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f` | P reading rule retained; no elder/Kac–Rice theorem is needed for J. |
| REC: `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | blob `75da2597971510f843f8d90c743950cb8c177342`; 23312 B; SHA256 `451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da` | Reading rule, W1, embedding and interface scopes; no fresh whole-parent acceptance. |
| C91: [comment5963566666](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5963566666) | 12433 B; SHA256 `74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa` | Only deterministic C4 W4–W5 at k=1; A2/QS and maximin application excluded. |

Historical review bindings were also reconciled: P review blob `bc11369c41ebc76de5700df3f931939ccfc88b9b` (24105 B; SHA256 `b7328d4bab97fa2d12622ca730dc698970febc1ea8bcbc0b24555e69e2a66392`) and R review blob `529c5264ed790ab1df36c14f567f460e2a5ed974` (20595 B; SHA256 `8679afd19ad313ade3602bba48b744183fdbefc9596a7793cfe7f921988a5dfd`). Their source and exposure/disposition records are historical inputs, not new votes or substitutes for this reconstruction. The historical parent bytes remain unchanged.

## Analytic reconstruction

### 1. Ten observations, centering and all-frame rank — ACCEPT

The contact vector is exactly `f, fx, fxx, fxxx, fz, fxz, fzz, fxxz, fxzz, fzzz`: all ten distinct planar derivatives through order three. Appending A and t introduces no duplicated mixed derivative. A zero-variance combination annihilates every positive-weight Fourier mode. Its degree-at-most-three multiplier, after the invertible frame substitution, vanishes on the integer lattice and is identically zero. This works for complex multipliers and reflected as well as rotated frames. Continuity and compactness of O(2), not rotational invariance of the torus, give one contact covariance gap.

The six-row observation transform has absolute determinant `12 r^-5` and the specified target exactly. Its centered rows cancel odd radius errors. In particular, the fourth row is `fxxx + r² fxxxxx/40 + O(r⁴)`. Rapid Fourier summability controls these remainders and derivative cross-covariances uniformly in position/frame. Thus the full ten-dimensional covariance and its inverse have O(r²) perturbations on a common small-radius band. The Schur complement retains a uniform four-dimensional covariance gap. Its conditional mean and covariance change by O(r²), because the birth targets are compact and `v_r-v_0=O(r²)`.

### 2. Gaussian density and further-conditioned moments — ACCEPT

Here rho is the **joint** density of `(A,t)` given U, not the density of t given A=0. Consequently `rho_0(0,t)=p(A=0|U_0) p(t|U_0,A=0)` in density notation; the first factor must remain. No original pin-density factor belongs to a measure already under Q_r.

Gaussian interpolation with uniformly elliptic covariance and bounded means gives an O(r²) quadratic-score error at fixed `(a,t)`. Evaluating at `a=-r lambda` adds an O(r) affine-score shift for bounded signed lambda. These two contributions yield J9 with its Gaussian t-envelope; the final error is not wrongly promoted to O(r²).

Regressing the whole field on the full V target gives a C4 mean bounded by `C(1+|t|)`, not a t-independent bound. The residual covariance is target-independent. Each centered conditional real Fourier coefficient has variance at most its original variance; Minkowski and the summable fourth-derivative spectral amplitudes give all fixed finite residual C4 moments. Correlations among residual coefficients are retained. This establishes J10 for every finite target under continuous regression versions, including A=0. Each imposed pin/jet has zero residual variance and its exact target mean. Nothing assumes N independent of t, Hessians or the tilt.

### 3. Actual typing and filtered determinants — ACCEPT

Differentiating the actual k=1 cubic gives J11, with off-diagonals `-gamma/2,+gamma/2` and transverse entries `-lambda-B1/2,-lambda+B1/2`. Since `D²F_r=H/r`, C91's entrywise estimate produces the operator error `2 K2 r N = (115/24)rN`. No spectral margin is needed.

For the filtered determinant, equal contributing indices use the determinant telescoping bound. When only one endpoint contributes, a singular point on the symmetric straight segment controls that endpoint's determinant; the segment norm is bounded by the endpoint maximum. Singular endpoints cause no exception. This proves J13, not a false Lipschitz statement about the bare inertia indicator.

The nonzero pivots -6 and +6 give the exact positive-part factors J14. Their unfiltered sum is `12 lambda`, so the product vanishes for lambda<=0. The sign-changing and singular cases are covered, not discarded. Scalar Hessian rescaling gives the exact product J15. Applying J13 and the product difference inequality with endpoint/model norm bound `C(D+rN)` gives J16. Expanding `rN(D+rN)^3`, and then using conditional moments through order four, gives the first J17 bound. The second uses moments p and p+4. Both preserve the **actual** endpoint-filtered weight, including its typing boundary.

### 4. L1 measure, positivity and full normalizer — ACCEPT

The absolute Jacobian `dA=r d lambda` and `W_r=r⁴D_r` give J18: the unnormalized layer has scale r⁵. Nonnegative disintegration/Tonelli and the J9/J17 envelope make every fixed polynomial-weighted integral finite. The density error has the stated majorant `Cr(1+|t|)^6 exp(-c|t|²)`, proving J3 for arbitrary fixed finite q, not merely bounded t.

At `lambda=Lambda/2,t=0`, w is strictly positive. One fixed small box preserves its lower bound. Compact birth/frame parameters and uniformly elliptic bounded Gaussian parameters give a uniform positive joint-density lower bound there. Hence m_Lambda has a positive uniform floor. A fixed negative A-interval similarly gives the positive floor for z_0. These are pointwise parameter-uniform statements; the nonempty compact birth set need not have positive length.

For the full normalization, the common Gaussian coupling from R3–R4 gives endpoint transverse errors O(rT) with every fixed T-moment uniformly bounded. The corrected congruence transforms H to `[[alpha,sqrt(r) beta],[sqrt(r) beta,A]]`, with `alpha=∓6+O(rT)`. Removing the off-diagonal changes a filtered determinant by at most `r beta²`: its determinant is affine in r, and a contributing inertia transition crosses zero. This remains true at singular A. The diagonal comparison costs `CrT²`. The reference filtered product is exactly `36 A_0² 1{A_0<0}`; multiplication and finite moments give `|Z_r/r²-z_0|<=Cr`, without an O(sqrt(r)) loss or inverse-margin moment.

The normalization ledger is therefore `r⁴ × r / r² = r³`. Algebraically `r^-3 Q_r^W(E)=mu_r(E)/z_r`. A common positive z_r floor and the weighted L1 bound give J5, including the O(r⁴) absolute soft-layer probability remainder. Neither the restricted mass nor an extra pin-density factor replaces the full Z_r.

### 5. Growing windows and downstream interpretation — ACCEPT

C91 is applied to exact pinned C4 fields, with N here dominating its norm and `2rw<=L/4`. Its constants at k=1 are exactly `167/192,635/384,115/48`, for values, gradients and Hessian entries respectively. Multiplying the **pointwise** Markov bound by the actual D_r, then disintegrating and applying J10/J17, proves J20. Division by the full Z_r produces the r³ weighted rare-layer factor in J6. This procedure needs no independence and is not an unweighted failure estimate substituted into a rare tilted population.

For `w=r^-beta, epsilon=r^eta`, the worst exponent is `1-4 beta-eta`; the hypothesis makes it strictly positive and ensures eventual physical containment. A three-event union proves J7. The positive soft mass gives its conditional version. Equality `4 beta+eta=1` would not imply o(r³). Constants may depend on each fixed p; choosing p to grow with r is not justified.

The L1 statement does control r-dependent measurable jet events and observables with a fixed polynomial envelope. It does not control inverse random typing margins, growing Lambda, a whole-field TV comparison, other gap marks, an actual elder decision, confinement, collision/intermediate composition, or a persistence coefficient. A2's literal AMEND history is not consumed or erased. These exclusions and the fixed finite-L, planar, k=1, compact-birth/all-frame scope are correctly preserved.

## Independent controls and actual execution

The complete standard-library checker is supplied below, independently written for this review. It contains no author checker, author test output or executed source code. Final source: **9983 UTF-8 bytes**, SHA256 `5a4529ab99723d52e0e21bb442f572f466a9dd1bf993d383f520aa1459e45c0a`, including final newline.

Frozen normal and optimized runs both exit 0 with **10,599 positive checks and eight refuted false-claim fixtures**. These fixtures run within the checker; they are not eight separately executed mutant programs. They challenge omitted positive parts, bare-indicator Lipschitzness, a wrong cubic row, wrong radius power, omitted A-marginal density, restricted normalization, critical window equality, and an independence substitution in weighted Markov. The finite rank fixtures use their own rational positive spectral weights at three frames and deliberately test duplicate-jet degeneracy; they do not sample or certify the continuum Gaussian covariance. Quartic fixtures preserve the exact pins and cover mixed derivative and raw Hessian scaling. Analytic arguments above, not these finite controls, establish all-frame ellipticity and Gaussian estimates.

Actual checker invocations in this review: one development run, then two normal and one optimized run of the frozen source (the second normal run captured the output digest). No author controls were run. The canonical commands are:

```text
python -B -S c92_independent_controls.py
python -B -O -S c92_independent_controls.py
```

Runtime Python 3.12.14. Frozen stdout is **757 bytes**, SHA256 `13dc0bd8b380a9c9e30c7989242c7a7d320e3d28e78abea572f4c7c6096534e2`, including its final newline. Normal/optimized output is byte-identical.

## Disposition and release

This completes and releases the bounded nonauthor review scope from pickup5963845378. The author retains C92 source, incorporation, custody and delivery responsibilities under WE614; I have neither changed nor released that claim. No repository source/head edit, branch update, merge, status promotion, formal acceptance or human approval occurred. No mathematical finding requires an amendment to this exact object. Downstream application and any provider-distinct/human/formal predicates remain separate.

## Reproducible checker source

```python
#!/usr/bin/env python3
"""Independent C92 transcription/obstruction controls; not a Gaussian proof.

Standard library, exact Fractions, no author checker or source execution.
Every check is an explicit exception, so python -O retains all checks.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json

COUNTS = {}
NEGATIVE = []


def check(group, condition):
    if not condition:
        raise RuntimeError(group)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("negative control survived: " + name)
    NEGATIVE.append(name)


def add(*polys):
    out = {}
    for p in polys:
        for ij, a in p.items():
            out[ij] = out.get(ij, F(0)) + a
    return {ij: a for ij, a in out.items() if a}


def scale(p, a):
    return {ij: a * b for ij, b in p.items() if a * b}


def mul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            out[i+k, j+l] = out.get((i+k, j+l), F(0)) + a*b
    return out


def deriv(p, i, j):
    return {(k-i, l-j): a*F(factorial(k), factorial(k-i))
            * F(factorial(l), factorial(l-j))
            for (k, l), a in p.items() if k >= i and l >= j}


def ev(p, x, z):
    return sum((a*x**i*z**j for (i, j), a in p.items()), F(0))


def raw(p, r):
    return {(i, j): a*r**(i+j-3) for (i, j), a in p.items()}


def model(lam, gam, b1, c3):
    return {(3, 0): F(2), (1, 0): F(-3, 2), (0, 0): F(-1, 2),
            (2, 1): gam/2, (0, 1): -gam/8, (0, 2): -lam/2,
            (1, 2): b1/2, (0, 3): c3/6}


def filtered(a, b, c, j):
    det = a*c-b*b
    if not det:
        return F(0)
    index = 1 if det < 0 else (2 if a+c < 0 else 0)
    return abs(det) if index == j else F(0)


def determinant(a):
    a = [row[:] for row in a]
    answer = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        v = a[i][i]
        answer *= v
        for j in range(i+1, len(a)):
            q = a[j][i]/v
            for k in range(i+1, len(a)):
                a[j][k] -= q*a[i][k]
    return answer


def positive_ldl(a):
    a = [row[:] for row in a]
    for i in range(len(a)):
        if a[i][i] <= 0:
            return False
        for j in range(i+1, len(a)):
            for k in range(j, len(a)):
                a[j][k] -= a[j][i]*a[k][i]/a[i][i]
                a[k][j] = a[j][k]
    return True


# Finite rank fixtures use rational positive weights and omega=1, NOT the
# periodized covariance. They test jet bookkeeping, not all-frame ellipticity.
jets = [(0,0), (1,0), (2,0), (3,0), (0,1), (1,1),
        (0,2), (2,1), (1,2), (0,3)]
check("jet_list", len(set(jets)) == 10)
check("jet_list", set(jets) == {(i,j) for i in range(4)
                              for j in range(4-i)})
for ux, uz, ex, ez in [(F(1),F(0),F(0),F(1)),
                      (F(3,5),F(4,5),F(-4,5),F(3,5)),
                      (F(3,5),F(4,5),F(4,5),F(-3,5))]:
    gram = [[F(0) for _ in jets] for _ in jets]
    for nx, nz in product(range(-2,3), repeat=2):
        ax, az = ux*nx+uz*nz, ex*nx+ez*nz
        amps = [ax**i*az**j for i,j in jets]
        weight = F(1, (1+nx*nx+nz*nz)**6)
        for a, (i,j) in enumerate(jets):
            for b, (k,l) in enumerate(jets):
                diff = i+j-k-l
                phase = (F(0) if diff % 2 else
                         (F(1) if (diff//2) % 2 == 0 else F(-1)))
                gram[a][b] += weight*amps[a]*amps[b]*phase
    check("finite_rank_fixtures", all(isinstance(v,F)
                                    for row in gram for v in row))
    check("finite_rank_fixtures", positive_ldl(gram))
    duplicate = [row[:] for row in gram]
    duplicate[-1] = duplicate[0][:]
    for row in duplicate:
        row[-1] = row[0]
    check("duplicate_rank_negative", determinant(duplicate) == 0)

# Exact six-row transform, target, and centered cancellation.
for r in [F(1,2), F(1,4), F(1,8), F(1,16)]:
    a, c = -r/2, r/2
    tmat = [[F(1,2),0,F(1,2),0,0,0],
            [-1/r,0,1/r,0,0,0], [0,-1/r,0,1/r,0,0],
            [12/r**3,6/r**2,-12/r**3,6/r**2,0,0],
            [0,0,0,0,F(1,2),F(1,2)], [0,0,0,0,-1/r,1/r]]
    check("pin_transform", abs(determinant(tmat)) == 12/r**5)
    original = [F(2),0,F(2)-r**3,0,0,0]
    target = [F(2)-r**3/2,-r**2,0,F(12),0,0]
    check("pin_transform", [sum(x*y for x,y in zip(row,original))
                            for row in tmat] == target)
    for degree in range(10):
        p = {(degree,0): F(1)}
        obs = [ev(p,a,0),ev(deriv(p,1,0),a,0),
               ev(p,c,0),ev(deriv(p,1,0),c,0),0,0]
        row3 = sum(x*y for x,y in zip(tmat[3], obs))
        expected = ev(deriv(p,3,0),0,0)
        if degree == 5:
            expected += r*r*F(factorial(5),40)
        if degree <= 6:
            check("centered_cubic_row", row3 == expected)
    check("centered_cubic_row", r*r*F(factorial(5),40) == 3*r*r)

# Signed model weight and off-diagonal filtered cancellation, including zero.
grid = [F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2)]
for lam, gam, b1 in product(grid, repeat=3):
    dm = 6*lam+3*b1-gam*gam/4
    ds = 6*lam-3*b1+gam*gam/4
    fm = filtered(F(-6),-gam/2,-lam-b1/2,2)
    fs = filtered(F(6),gam/2,-lam+b1/2,1)
    check("signed_typed_weight", fm == max(dm,0))
    check("signed_typed_weight", fs == max(ds,0))
    if lam <= 0:
        check("nonpositive_limit", fm*fs == 0)
for a,b,c in product(grid, repeat=3):
    for j in range(3):
        check("filtered_offdiagonal", abs(filtered(a,b,c,j)
              - filtered(a,0,c,j)) <= b*b)
for ax,cz,ay,dz in product(grid, repeat=4):
    norm = max(abs(ax),abs(cz),abs(ay),abs(dz))
    diff = max(abs(ax-ay),abs(cz-dz))
    for j in range(3):
        check("diagonal_filtered_lipschitz",
              abs(filtered(ax,0,cz,j)-filtered(ay,0,dz,j))
              <= 2*norm*diff)

# Independent pin-preserving quartics test exact raw Hessian scaling and all
# mixed derivatives. Nbound is a deterministic bound on the unit local box,
# not a Gaussian sample or a global torus construction.
for r in [F(1,2),F(1,4),F(1,8)]:
    q = {(2,0):F(1),(0,0):-r*r/4}
    quartics = [mul(q,q), mul(q,{(1,1):F(1)}),
                mul(q,{(0,2):F(1)}), {(1,3):F(1)}, {(0,4):F(1)}]
    for lam,gam,b1,c3 in [(F(-1,2),F(0),F(1),F(-1)),
                            (F(0),F(2),F(-1),F(1)),
                            (F(1),F(1),F(0),F(2))]:
        base = {(i,j):v*r**(3-i-j) for (i,j),v
                in model(lam,gam,b1,c3).items()}
        f = add(base, *[scale(p,F(i+1,7)) for i,p in enumerate(quartics)])
        check("quartic_pins", ev(f,-r/2,0) == 0)
        check("quartic_pins", ev(f,r/2,0) == -r**3)
        for x in [-r/2,r/2]:
            for i,j in [(1,0),(0,1)]:
                check("quartic_pins", ev(deriv(f,i,j),x,0) == 0)
        midpoint = [ev(deriv(f,i,j),0,0)
                    for i,j in [(0,2),(2,1),(1,2),(0,3)]]
        actual_model = model(-midpoint[0]/r,*midpoint[1:])
        error = add(raw(f,r),scale(actual_model,F(-1)))
        nbound = F(1) + max(sum(abs(v) for v in deriv(f,i,j).values())
                           for i in range(5) for j in range(5-i))
        for x in [-F(1,2),F(1,2)]:
            for i,j in [(2,0),(1,1),(0,2)]:
                check("raw_hessian_scale", ev(deriv(raw(f,r),i,j),x,0)
                      == ev(deriv(f,i,j),r*x,0)/r)
        constants = [F(167,192),F(635,384),F(115,48)]
        for w in [F(1),F(2),F(4)]:
            if r*w > 1:
                continue
            for x,z in product([-w,F(0),w], repeat=2):
                for order in range(3):
                    for i in range(order+1):
                        j = order-i
                        check("quartic_derivative_bounds",
                              abs(ev(deriv(error,i,j),x,z))
                              <= constants[order]*nbound*r*w**(4-order))

# Exact radius bookkeeping and a correlated weighted Markov fixture.
for r in [F(1,2),F(1,8),F(1,32)]:
    m,z = F(7,3),F(5,2)
    numerator,normalizer = r**4*r*m, r**2*z
    check("radius_ledger", numerator/normalizer == r**3*m/z)
    check("radius_ledger", r**(-3)*numerator/normalizer == m/z)
atoms = [(F(1,2),F(1),F(1)), (F(1,3),F(3),F(4)),
         (F(1,6),F(9),F(25))]  # (mass,N,D), correlated on purpose
for p in [1,2,3,5]:
    for threshold in [F(1),F(2),F(4),F(10)]:
        left = sum(m*d for m,n,d in atoms if n > threshold)
        right = sum(m*d*n**p for m,n,d in atoms)/threshold**p
        check("weighted_markov", left <= right)
for beta,eta in [(F(0),F(0)),(F(1,8),F(1,4)),
                 (F(1,10),F(1,10)),(F(6,25),F(1,100))]:
    exps = [1-(4-j)*beta-eta for j in range(3)]
    check("window_exponents", min(exps) == 1-4*beta-eta)
    check("window_exponents", min(exps) > 0 and beta < 1)

reject("omit-positive-parts", (-6+3)*(-6-3)
       == filtered(F(-6),F(0),F(1,2),2)
          *filtered(F(6),F(0),F(3,2),1))
reject("inertia-indicator-is-Lipschitz",
       F(1) <= 2*F(1,100)*(2*F(1,100)))
reject("wrong-cubic-row-factor", F(3) == F(6))
reject("wrong-soft-radius-power", F(1,8)**5 == F(1,8)**3)
reject("drop-joint-A-marginal", F(2,3)*F(5,7) == F(5,7))
reject("normalize-by-soft-layer", F(1,8)**3 == 1)
reject("critical-window-also-o-r3", 1-4*F(1,4) > 0)
reject("weighted-Markov-by-independence",
       sum(m*d*n**2 for m,n,d in atoms)
       == sum(m*d for m,n,d in atoms)*sum(m*n**2 for m,n,d in atoms))

print(json.dumps({"object":"C92-independent-controls-v1",
                  "positive_counts":COUNTS,
                  "positive_total":sum(COUNTS.values()),
                  "rejected_mutants":NEGATIVE,
                  "mutant_total":len(NEGATIVE),
                  "scope":"exact finite controls; Gaussian assertions analytic"},
                 sort_keys=True, separators=(",", ":")))
```

## Canonical checker stdout

```json
{"mutant_total":8,"object":"C92-independent-controls-v1","positive_counts":{"centered_cubic_row":32,"diagonal_filtered_lipschitz":7203,"duplicate_rank_negative":3,"filtered_offdiagonal":1029,"finite_rank_fixtures":6,"jet_list":2,"nonpositive_limit":196,"pin_transform":8,"quartic_derivative_bounds":1296,"quartic_pins":54,"radius_ledger":6,"raw_hessian_scale":54,"signed_typed_weight":686,"weighted_markov":16,"window_exponents":8},"positive_total":10599,"rejected_mutants":["omit-positive-parts","inertia-indicator-is-Lipschitz","wrong-cubic-row-factor","wrong-soft-radius-power","drop-joint-A-marginal","normalize-by-soft-layer","critical-window-also-o-r3","weighted-Markov-by-independence"],"scope":"exact finite controls; Gaussian assertions analytic"}
```
