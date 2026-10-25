# C271 — DD v1.4 analytic reduction, domination and tail: bounded nonauthor review

**Disposition: PASS_ANALYTIC_REDUCTION_SUPPORT_SLICE, with two nonblocking prose/interface clarifications below.** No mathematical defect was found in DD §§1.1–1.3, Lemmas 1–2 and 5, or the inspected supporting formulas, under the explicitly retained source hypotheses. This is a mathematical review of this precise slice, not acceptance of the full numerical Theorem DD, Corollary DD1 or the project's finite-bar theorem.

Dylan Roy — delegated AI work. Actual lead reviewer and publisher: OpenAI / Codex, `/root`, task `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`. Supporting readers: `/root/c270_patch_semantics` (analytic reconstruction), its child `/root/c270_patch_semantics/dd_tail_crosscheck` (tail check), and `/root/c267_next_task_triage` (independent exact algebra checker). All are nonauthors of the exact Anthropic Claude DD note, but source-exposed and aware of prior project work/discussion; the root previously reviewed persistence/interface and engineering material. Provider distinction from the author is disclosed; these same-team subreads are not mutually independent providers, blind reconstruction, organizational independence, or human review. Organizational-independence credit 0. Dylan did not personally perform this review.

The author's fresh offer is [main#307/6145199105](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145199105). The accepted scope and exclusions are [pickup6145296480](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145296480). R17 claim `d135b0b5-4154-42ce-9138-7720c742ebab` is actually at Work Events row1931, start2026-10-13T12:13:35Z, lease14:13:35Z. The original pickup's incorrect row1930 is retained as history and corrected by [6145301318](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145301318); all14 actual claim fields were read back. No source or branch ownership was taken.

## 1. Frozen sources and inherited scope

All files below were read at Math- commit `a115feebd861119d90a1ea1f9344f685d9535d0e`, the landed result of Math-#450. Native contents and Git tree identities were checked against unchanged local UTF-8 bytes. The full hashes are included so this review cannot float to a later note.

| Source | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `frontiers/lifetime_dd_model_d_20261013/DD/PROOF.md` v1.4 | 28074 | `04830e68151933f7be73f79c53ec3570174852f3c94be70edfffd553e7feb051` | `7c852d1fef3507804eca034ce964510caee87d5c` |
| `frontiers/lifetime_dd_model_d_20261013/certificate_v2/ddbounds.py` | 20822 | `f9f800fcfecc020ca95c372c4caaa74d15f6534bd677ad0357be56cd69fca09b` | `5b3faa4547ce3c806f8107f69c13145ae8d55bca` |
| `frontiers/lifetime_dd_model_d_20261013/certificate_v2/ddint.py` | 9298 | `d7b4580cbbab2252ce4e79af5334713c46183338a87bed50cc357b566b37aa9d` | `3c123c55792593e91ec8859fd8bf9eae55f080e9` |
| `frontiers/soft_closed_form_20261002/PROOF.md` (#244) | 58898 | `dd9b436a58d5d58f706ca59ddcf3eb31519866ea9e0a854e168036a8c21e1eaf` | `c69f92b1076399fb9f8917bb273e15348b0a497e` |
| `frontiers/v24_dc_two_thirds_sign_20261007/V24/PROOF.md` | 52200 | `32677f024747cccf8a87e7ded6b6716666376a0f409381d38f21fafa18930c03` | `670e7370a8951af8039516f429726be88eb98003` |
| `frontiers/v24_dc_two_thirds_sign_20261007/DC/PROOF.md` | 32514 | `1fcc3ea335516095308aeaf83280dda8e484b6d484eb7d3b4ffc7115dd4455f4` | `734f34913d44042e33445da29333169ccc72b24c` |

The identification of the elder rejection integral `I` with `Phi` inherits #244 Theorem A's stated hypotheses: #170 Theorem E(1), [CUB] Theorem C, and [CUB] height identities (C8)–(C11), including its B=0 paragraph. Those upstream theorems are not re-proved here. The excluded algebraic curve in #244 has zero measure under the nondegenerate Gaussian laws used at fixed positive scales; the explicit continuous `Phi` model can be assigned there. Bounds on `Phi` are algebraic model statements; interpreting them as the elder integral retains the hypotheses. V24 Lemma K is an imported global residual bound used below, with its supplied elementary proof sanity-checked rather than a new review of the full V24 transfer theorem. DC supplies the definition and normalization convention for D. No dimension/side-length transfer bound is silently broadened.

For clarity use `h(t,chi)=I(t,chi)-I_quad(t,chi)` for the residual and `g=|gamma|` for the positive scale. DD uses g for both in different locations.

## 2. Root identity and both branches

Put `c=1-t`, `R=8-12t+chi`. In #244 let `psi_e>=max(2c,-c)` satisfy `16(psi_e-2c)^2(psi_e+c)=R^2`. Set `r=psi_e-2c>=0` and `v=sqrt(psi_e+c)`. Then `v^2=r+3c` and `|R|=4vr=4v^3-12cv`.

For c>0 the permitted half-line begins at sqrt(3c), and for c<=0 it begins at0. The cubic is continuous, strictly increasing from0 to infinity there: its derivative is12(v^2-c), positive in the interior (the c=0,v=0 endpoint causes no extra root). Thus it has exactly the physical largest root used by DD. With `delta=psi_e-|c|=v^2-c-|c|`, the closed form `|c|delta^2+delta^3/3` becomes

```
Phi = v^6/3-c v^4+(4/3)c^3       (c>0),
Phi = v^6/3+|c|v^4              (c<=0).
```

Both branches agree at c=0. At R=0 their values are4c^3/3 for c>0 and0 for c<=0, agreeing with the relevant root. Symmetry is in R; h need not be even in chi. Exact expansion also agrees with #244 (2.7). This establishes the claimed transformation at the stated model/conditional scope, without using a sampled root plot as proof.

## 3. Full Gaussian normalization and legitimate exchanges

Start with

```
D=(1/2400) integral_0^infinity k^(-8/3)e^(-12k^2)
     E[gamma^6 h(12kB/gamma^2,576k^2 C3/gamma^3)] dk,
(gamma,B,C3) independent with variances (2,2,6).
```

Absolute integrability must be justified before exchanging this signed integral. Lemma1 alone has a nonzero constant and is not sufficient for that purpose near k=0. The imported V24 Lemma K states

```
|h(t,chi)| <= 324(t^2+|t|^3+|chi|+chi^2).
```

For gamma!=0, multiplication by gamma^6 cancels all negative gamma powers in this bound. The four expectations are respectively

```
576 k^2,
1728 k^3 E|B|^3,
576 k^2 E|gamma|^3 E|C3|,
576^2 k^4 E C3^2.
```

They yield the explicit majorant

```
E[gamma^6|h|] <= 324[(576+9216 sqrt(3)/pi)k^2
                         +(13824/sqrt(pi))k^3+1990656 k^4].
```

After the factor k^(-8/3), the powers at zero are -2/3,1/3,4/3, all integrable; the factor e^(-12k^2) controls infinity. Assigning arbitrary values on gamma=0 changes no expectation. Tonelli applied to the absolute value therefore supplies Fubini for the signed expression. This is a convergence justification for the change of measure, conditional on the imported K bound, not a certification of DD Lemma6's quantitative numerical tail sizes.

For each gamma!=0 set k=tau gamma^2. Then

```
gamma^6 k^(-8/3) dk=|gamma|^(8/3)tau^(-8/3)d tau.
```

The factor2 when folding gamma to g>0 follows from the measure-preserving transformation `(gamma,C3)->(-gamma,-C3)` of the product Gaussian law, which leaves both t and chi unchanged. Equivalently use C3 symmetry after conditioning; do not assume h is even in chi. The gamma density is exp(-g^2/4)/sqrt(4pi). At fixed tau,g>0, t and chi are independent centered Gaussians with standard deviations

```
sigma_t=12 sqrt(2) tau,    sigma_chi=s=576 sqrt(6) tau^2 g.
```

Finally u=ln(tau), omega=ln(g) contributes d tau d g=tau g du d omega. Thus

```
D=integral rho(u,omega) H(u,omega) du d omega,
rho=c0 tau^(-5/3)g^(11/3)exp(-12tau^2 g^4-g^2/4),
c0=2/(2400sqrt(4pi))=1/(2400sqrt(pi))=24sqrt(pi)/(57600pi),
H=E h(sigma_t Z1,sigma_chi Z2).
```

All density factors and scale powers agree with DD(1.2) and DC's A3. The sequence is fixed positive conditional scales, then changes of variables in the absolutely integrable expression. No interchange of a small-bar or field-size limit is supplied by this calculation.

## 4. Support, absolute Jacobian, completed square and moments

For fixed positive tau,g, split the (t,chi) plane into R>0 and R<0; R=0 is a null affine line. On either sign branch the inverse is

```
chi_±(t,v)=±(4v^3-12v+12vt)-8+12t.
```

The open support v>sqrt(3(1-t)_+) is equivalent to v>0 and t>1-v^2/3. The signed derivative in v is ±12(v^2-1+t); its **absolute** value is12(v^2-1+t)>0 in the interior. Thus both branch integrals enter with positive Jacobian. There is no orientation cancellation, omitted negative branch, or additional symmetry factor2. The formula written as dchi in the note must be read as the unsigned integration measure; its P± implementation does that.

The t density contributes `(24 tau sqrt(pi))^(-1)exp[-t^2/(576tau^2)]`; the chi density contributes `(s sqrt(2pi))^(-1)exp[-chi^2/(2s^2)]`. Write lambda=12(1±v), mu=±(4v^3-12v)-8 and a=1/(576tau^2). With Delta=2as^2+lambda^2>0,

```
alpha=Delta/(2s^2)>0, t_c=-lambda mu/Delta,
-a t^2-(lambda t+mu)^2/(2s^2)
   =-a mu^2/Delta-alpha(t-t_c)^2.
```

The minus branch at v=1 has lambda=0 and remains regular because2as^2>0. Split the t integral at1. On each interval the residual times the Jacobian is polynomial of degree at most4 in t. `ddint.poly_in_t` matches that polynomial on both signs and both t branches. `F_core` uses the displayed Delta, center, prefactor and limits. These formula comparisons do not audit the interval/Taylor primitives it calls.

For J_n(x)=integral_x^infinity z^n exp(-alpha z^2) dz, J0 is sqrt(pi)/(2sqrt(alpha)) times erfc(sqrt(alpha)x), J1=exp(-alpha x^2)/(2alpha). For n>=2, integration by parts gives

```
2alpha J_n=(n-1)J_(n-2)+x^(n-1)exp(-alpha x^2).
```

The boundary at infinity vanishes for every fixed finite n, alpha>0. This also applies for negative x; odd moments over such a half-line must not be replaced by absolute moments. The recurrence agrees with `moments_halfline`. At v=0 or on support boundaries the measure-zero convention is harmless. This supplies the analytic closed form, not the numeric erfc enclosure.

## 5. Pointwise majorization and Gaussian-kernel differentiation

Direct subtraction gives

```
I_quad-R^2/48=16/3-16t+(5/9)chi+(43/3)t^2-(5/6)t chi+(23/3888)chi^2.
```

For c>0, r=v^2-3c>=0 satisfies R^2=16(r+3c)r^2>=16r^3, and `Phi-R^2/48=c r^2+3c^2r+4c^3/3`. For c<=0 put q=v^2, b=|c|. Then R^2=16q(q+3b)^2>=16q^3 and `Phi-R^2/48=-b q^2-3b^2q`. Both yield DD Lemma1 by the triangle inequality, with r or q bounded by `(R^2/16)^(1/3)`.

The monomial relaxation uses subadditivity of the2/3 power and `(x+y+z)^(4/3)<=3^(1/3)(x^(4/3)+y^(4/3)+z^(4/3))`. The factor3^(1/3) is present. `sharper_terms` has precisely the6 polynomial,4 cubic-binomial,9 first-root-power and6 second-root-power terms,25 nonnegative entries before merging. Their total degree is at most3, so the residual has a global majorant C(1+|t|+|chi|)^3.

For a Gaussian density N_sigma(x), L=sigma partial_sigma gives LN=(z^2-1)N, Lz=-z, hence

```
p0=1, p_(k+1)=(z^2-1)p_k-z p_k',
Q_(a,b)=sum_(j=0)^a binom(a,j)2^(a-j)p_j(Z1)p_(a-j+b)(Z2).
```

The factor2 is from partial_u log(sigma_chi)=2. Operators on the two independent density factors commute. Work in fixed physical variables (t,chi) to differentiate the density, not the possibly nonsmooth residual. On a compact rectangle about any finite(u,omega), both standard deviations have positive lower and finite upper bounds. Every kernel derivative of a fixed order K has a common bound

```
C_K(1+|t|+|chi|)^(2K)
   exp[-t^2/(2M_t^2)-chi^2/(2M_chi^2)].
```

Multiplying by the residual majorant is integrable. Difference quotients on a smaller rectangle are dominated by a next derivative on the larger rectangle, so induction and dominated convergence justify all finite mixed derivatives and continuity. This is local smoothness for positive scales, not uniform control at scales0 or infinity.

The complete moment identity `E|Z|^p=2^(p/2)Gamma((p+1)/2)/sqrt(pi)` holds for p>-1; all used powers are nonnegative. Replacing |Q| by its coefficientwise absolute polynomial gives an upper sum of independent moments. `kernel_abs` and `EgQ_plain` implement that safe triangle bound with scales sigma_t^r sigma_chi^s for each residual monomial; the kernel's standardized variables do not introduce additional scale powers.

## 6. General tail argument and implementation formulas

Let v1>=3, T=v1^2/6-1>=1/2 and X=2v1^3-8-12T=2v1^3-2v1^2+4>=40. If v>=v1 and |t|<T, then3c<=v1^2/2. For c>0,

```
|R|=4v(v^2-3c)>=2v1^3;
```

for c<=0 the stronger4v1^3 bound holds. Therefore |chi|>=|R|-8-12|t|>=X. Equality |t|=T is already covered by the t event. The union inclusion in Lemma5 holds for every admissible point, including v=v1, not just a numerical grid. Bounding |h| by its nonnegative monomial majorant and using independence termwise gives exactly the two tail-moment products in `vtail_bound`; double counting the intersection is an upper bound.

For Y=sigma Z, p>=0 and B>0,

```
E[|Y|^p 1{|Y|>B}]=sigma^p 2^(p/2)
     Gamma((p+1)/2,B^2/(2sigma^2))/sqrt(pi).
```

It is nondecreasing in sigma by coupling with the same |Z|. The zero-scale limit has empty tail for B>0. At positive scale the boundary has zero Gaussian mass, so the implementation's strict `>` and the lemma's `>=` agree for these expectations. For a>0,x>0, substituting t=x+u in Gamma(a,x) gives its exponential integral representation; bounding `(1+u/x)^(a-1)` by1 when a<=1 or exp((a-1)u/x) when a>1,x>a-1 gives the source's two incomplete-gamma upper bounds. Otherwise the full Gamma is an upper bound. These justify the formulas subject to the excluded interval primitives returning valid enclosures. The current caller meets the positive cutoff/nonnegative power assumptions.

## 7. Actionable clarification requests to the source owner

**C271-Q1 — exact inequality wording, nonblocking.** DD Lemma2 says the expectation with `g_tilde |Q|` “is an explicit sum” of absolute moments. Insert the two upper bounds explicitly: first replace g_tilde by its nonnegative monomial majorant M, then use `|Q|<=Q_abs`. The resulting expectation `E[M Q_abs]` is the explicit moment sum. The inspected implementation already follows this route. This is a prose clarification, not a counterexample to the claimed upper bound.

**C271-Q2 — finite implementation domain, nonblocking.** Document that the stored P table supports nonnegative integer a,b with a+b<=10. The declared four-point Gauss rule requests orders through8 and is covered. The mathematical recurrence and local differentiation statement support every finite order, but the table should not be described as an unrestricted implementation. Similarly, “integer p exact” in the moment docstring means a closed formula: even moments are rational; odd moments require the sqrt(2pi) enclosure. No failure in the stated caller was found.

Next useful task: the DD source owner can append or incorporate Q1/Q2 with exact new source identity and a bounded delta read. A separately claimed full numerical/interval certificate review, if still needed by the author, remains outside this delivery. The preferred finite ordinary-bar bridge remains in its existing owner lanes; this supporting D review does not replace it.

## 8. Boundaries that remain open

Excluded: DD Lemmas3–4/6 as complete quantitative proofs; interval primitives, directed rounding and transcendental enclosures; Taylor remainder and tensor/sliver quadrature implementation audit;38,288-node replay; full numerical D enclosure and Corollary DD1 certification; upstream #170/CUB theorem acceptance; actual finite ordinary persistence bars and once-counted bar transfer; field-first sampling, all-small-bars converses and regional shrinking multiple-witness collisions. Global factorial bounds cannot discharge that regional collision node. Elder pairing remains distinct from branch adjacency. No finite-bar asymptotic, new limit interchange or theorem completion is inferred from polynomial checks, model agreement, merge history, custody or hosted CI.

The scientific status is unchanged. This bounded audit does not complete the project-wide audit. Frozen sources, prior reviews, claims, scoped stops and source owners remain preserved.

## 9. Final exact support and execution evidence

The applicable narrow master verification ran once on final stable inputs at 2026-10-13T12:28:05–12:28:06Z under CPython3.9.6. Normal and optimized modes each exited0 with514 positive checks and18 rejected negative controls; stderr was empty, every positive result and rejection was parsed, and all six source identities plus frozen review inputs remained unchanged. The two result objects agree except for their optimization-mode flag. The reviewer checker imports no author module or controls; it executes only the four explicitly extracted pure arithmetic definitions listed in its source. The root reviewed those definitions and the independent Fraction polynomial engine before final execution.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| `exact_checks.py` | 16309 | `541bb247b2c02bd51c83abfcc2e95d1ab3dd32364640a770d383120864663278` |
| `verification/normal.json` | 76471 | `acccfafe26defea54671b5fac107792627054657630196ac4adfcf9bf7a8c4ce` |
| `verification/optimized.json` | 76470 | `a3a70b1f9e67faf9b572b9268480ecf7113fe8c49100058dc39c54c20fec0e8c` |
| `verification/RESULTS.json` | 4664 | `264defc54a71816f00e833cab2879574f28dbda36e9005308c53a6be632b368a` |
| `KERNEL_TAIL_REVIEW.md` | 15804 | `4e0d2b16197ab0aef0eb663d46183688a4640cd6878db7ca8a2be7320a99cdc8` |

Coverage: both Phi branches and their join; residual polynomial; both inverse signs and absolute Jacobian; four sign/branch implementation polynomials; normalization coefficients/powers; denominator-cleared completed square;12 moment integration-by-parts identities;110 kernel-moment cases through kernel order10 and even moment degree20;45 mixed orders through total8;210 rational tail cases. Finite checks support the general arguments in sections2–6; they do not establish those arguments by enumeration.

The18 deliberate expression/hypothesis controls reject: missing positive-branch constant, wrong nonpositive-branch sign, wrong minus inverse, omitted Jacobian, signed instead of absolute Jacobian, omitted negative-R branch, missing gamma symmetry factor, missing logarithmic measure power, missing t density normalizer, reversed completed-square center, omitted square residual constant, wrong moment recurrence coefficient, omitted moment boundary term, reversed kernel derivative sign, missing chi log-scale factor2, each omitted tail event, and a threshold outside v1>=3. The last control detects failure of the positive-threshold premise at v1=1 (T=-5/6), not a counterexample to a set inclusion that becomes vacuous. These are expression-level controls, not a production-module mutation campaign.

Explicit tail witnesses at v1=v=3 are (t,chi)=(0,64) for losing the chi event and(-1,16) for losing the t event. The missing negative branch witness is v=2,t=0,R=-8,chi=-16; the positive inverse instead giveschi=0. Exact nonzero polynomial residuals and every finite case are preserved in the one private raw-evidence bundle.

Source landing CI was freshly observed separately: [run38393986888](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38393986888), completed/success on exact landed commit a115feebd861119d90a1ea1f9344f685d9535d0e. This is the source's hosted run, not a hosted run of C271, a new commit, or theorem certification. The38,288-node DD certificate was not replayed in this slice; no new review CI was represented as passing. Full interval enclosure review remains outside the scope.

## 10. Reproducible exact checker (complete source)

Save the six frozen files under the input names in the identity table; the checker consumes DD_PROOF.md, SOFT_CLOSED_FORM_PROOF.md, ddbounds.py and ddint.py in an inputs directory beside it. Execute `python3 -B -E -S exact_checks.py --output result.json`, then add `-O` for optimized mode. The complete checker below is unchanged from the hashed file. Its output carries all exact residuals/witnesses, source hashes and counts. The separate master additionally checks the six source Git-blob identities and immutable input hashes.


```python
#!/usr/bin/env python3
"""C271: source-exposed exact support checks, not theorem certification.

Standard library only. The polynomial engine and expected expressions are new
reviewer code. No author module or author control is imported. Four explicitly
named pure arithmetic definitions are extracted from the pinned source ASTs to
compare implementation expressions with independent polynomial identities.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import sys

NAMES = ("v", "c", "t", "chi", "a", "s2", "lam", "mu", "z", "w")
DIM = len(NAMES)
ZERO_EXP = (0,) * DIM


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {ZERO_EXP: F(terms)}
        self.terms = {m: F(c) for m, c in terms.items() if c}

    def __add__(self, other):
        d = dict(self.terms)
        for m, c in Poly(other).terms.items():
            d[m] = d.get(m, F(0)) + c
        return Poly(d)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        d = {}
        for m, c in self.terms.items():
            for n, e in Poly(other).terms.items():
                k = tuple(x + y for x, y in zip(m, n))
                d[k] = d.get(k, F(0)) + c * e
        return Poly(d)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (F(1) / F(scalar))

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Only nonnegative integer polynomial powers")
        out = Poly(1)
        for _ in range(n):
            out = out * self
        return out

    def derivative(self, index):
        out = {}
        for m, c in self.terms.items():
            if m[index]:
                n = list(m)
                n[index] -= 1
                out[tuple(n)] = c * m[index]
        return Poly(out)

    def substitute(self, replacements):
        out = Poly(0)
        for m, c in self.terms.items():
            term = Poly(c)
            for i, power in enumerate(m):
                term = term * replacements.get(i, variables()[i]) ** power
            out = out + term
        return out

    def evaluate(self, **values):
        supplied = {NAMES.index(k): F(v) for k, v in values.items()}
        total = F(0)
        for m, c in self.terms.items():
            term = c
            for i, n in enumerate(m):
                if n:
                    term *= supplied[i] ** n
            total += term
        return total

    def record(self):
        return [{"powers": {NAMES[i]: n for i, n in enumerate(m) if n},
                 "coefficient": str(c)} for m, c in sorted(self.terms.items())]


def variables():
    return tuple(Poly({tuple(int(i == j) for i in range(DIM)): F(1)})
                 for j in range(DIM))


v, c, t, chi, a, s2, lam, mu, z, w = variables()
positive = []
negative = []


def check(name, predicate, detail=None):
    if not predicate:
        raise RuntimeError("Positive check failed: " + name)
    positive.append({"id": name, "status": "PASS", "detail": detail})


def equal(name, lhs, rhs):
    delta = Poly(lhs) - rhs
    check(name, not delta.terms, {"method": "exact rational polynomial identity",
                               "residual": delta.record()})


def reject(name, residual, witness=None):
    residual = Poly(residual)
    if not residual.terms:
        raise RuntimeError("Negative control survived: " + name)
    negative.append({"id": name, "status": "REJECTED",
                     "nonzero_polynomial_residual": residual.record(),
                     "witness": witness})


def witness_rejection(name, detail):
    if not detail.pop("rejects"):
        raise RuntimeError("Negative witness failed: " + name)
    negative.append({"id": name, "status": "REJECTED", "witness": detail})


def iq(T, C):
    return F(20, 3) - 20*T + F(8, 9)*C + F(52, 3)*T*T - F(4, 3)*T*C + F(13, 486)*C*C


def extract_functions(path, names, environment):
    """Run only these supplied top-level definitions; never run author imports."""
    tree = ast.parse(path.read_text())
    chosen = [node for node in tree.body
              if isinstance(node, ast.FunctionDef) and node.name in names]
    if {node.name for node in chosen} != set(names):
        raise RuntimeError("Source definition inventory mismatch")
    for node in chosen:
        if node.decorator_list or any(isinstance(x, (ast.Import, ast.ImportFrom,
                ast.Global, ast.Nonlocal, ast.ClassDef)) for x in ast.walk(node)):
            raise RuntimeError("Unexpected effects in arithmetic definition")
    namespace = {"Fr": F, "math": math, **environment}
    exec(compile(ast.Module(body=chosen, type_ignores=[]), path.name, "exec"), namespace)
    return namespace


def gaussian_moment(n):
    return F(0) if n % 2 else F(math.prod(range(n - 1, 0, -2)))


def expected_under_standard_gaussians(poly):
    total = F(0)
    for m, coeff in poly.terms.items():
        if any(m[i] for i in range(DIM) if i not in (8, 9)):
            raise ValueError("Only z,w Gaussian expectations are supported")
        total += coeff * gaussian_moment(m[8]) * gaussian_moment(m[9])
    return total


def kernel_operator(poly, which):
    X = (z, w)[which]
    return (X*X - 1)*poly - X*poly.derivative(8 + which)


def run_checks(inputs):
    # Phi from source (2.5), using psi_e=v^2-c, versus the stated v forms.
    psi = v*v - c
    R = 4*v**3 - 12*c*v
    pos_phi = v**6/F(3) - c*v**4 + F(4, 3)*c**3
    neg_phi = v**6/F(3) - c*v**4
    for label, abs_c, claimed in (("positive", c, pos_phi), ("nonpositive", -c, neg_phi)):
        delta = psi - abs_c
        equal("phi_from_2_5_"+label, abs_c*delta**2 + delta**3/F(3), claimed)
        y = psi - c
        equal("phi_from_2_7_"+label,
              R**2/F(48) + c*y*(y+c) + F(2,3)*abs_c**3 - F(4,3)*c**3, claimed)
    equal("cubic_substitution", 16*(psi-2*c)**2*(psi+c), R**2)
    rho = z
    equal("lemma1_positive_residual",
          (pos_phi-R**2/F(48)).substitute({0: v}).substitute({1: c}),
          c*(v*v-3*c)**2 + 3*c*c*(v*v-3*c) + F(4,3)*c**3)
    equal("lemma1_nonpositive_residual", neg_phi-R**2/F(48), c*v**4-3*c*c*v*v)
    rbase = 8-12*t+chi
    iqdiff = F(16,3)-16*t+F(5,9)*chi+F(43,3)*t*t-F(5,6)*t*chi+F(23,3888)*chi*chi
    equal("iquad_minus_R_squared", iq(t,chi)-rbase*rbase/F(48), iqdiff)
    equal("branch_join_c_zero", pos_phi.substitute({1:Poly(0)}), neg_phi.substitute({1:Poly(0)}))
    reject("omit_positive_phi_constant", c*(psi-c)**2+(psi-c)**3/F(3)-(pos_phi-F(4,3)*c**3))
    reject("use_wrong_nonpositive_phi_sign", neg_phi-(v**6/F(3)+c*v**4))

    # Both inverse branches and the unsigned area element; comparison with source's pure polynomial function.
    src = extract_functions(inputs/"ddint.py", {"poly_in_t"}, {})
    Rtv = 4*v**3 - 12*(1-t)*v
    jac = 12*(v*v-1+t)
    for sign in (-1,1):
        inverse = sign*Rtv-8+12*t
        declared = 12*(1+sign*v)*t + sign*(4*v**3-12*v)-8
        equal("inverse_branch_"+str(sign), inverse, declared)
        equal("signed_derivative_"+str(sign), inverse.derivative(0), sign*jac)
        for branch in ("A","B"):
            phi = v**6/F(3)-(1-t)*v**4+(F(4,3)*(1-t)**3 if branch=="A" else 0)
            oracle = (phi-iq(t,inverse))*jac
            coeffs = src["poly_in_t"](v, sign, branch, Poly(1))
            supplied = sum((coef*t**n for n,coef in enumerate(coeffs)), Poly(0))
            equal("source_poly_in_t_"+str(sign)+"_"+branch, supplied, oracle)
            check("degree_at_most_4_"+str(sign)+"_"+branch,
                  max((m[2] for m in oracle.terms),default=0)<=4)
    reject("wrong_minus_inverse_sign", (-Rtv-8+12*t)-(Rtv-8+12*t))
    reject("omit_jacobian", jac-1, {"v":"2","t":"0","correct_absolute_jacobian":"36","mutant":"1"})
    reject("signed_instead_of_absolute_minus_jacobian", -jac-jac)
    # v=2,t=0 gives R=8. The minus inverse chi=-16 is missed by a plus-only map.
    witness_rejection("drop_negative_R_branch", {"rejects": (-8-8)!= (8-8),
                      "v":"2","t":"0","R_minus":"-8","chi_minus":"-16","chi_plus":"0"})
    for V,T in ((F(2),F(0)),(F(1),F(2)),(F(3),F(-1)),(F(1,2),F(1)),(F(4),F(-4))):
        check("support_and_jacobian_"+str(V)+"_"+str(T), V>0 and T>1-V*V/3 and 12*(V*V-1+T)>0)

    # c0 is represented as its rational coefficient of 1/sqrt(pi); no floating pi approximation.
    c0_symmetry = F(1,2400)*2/F(2)
    c0_alt = F(24,57600)
    check("gaussian_full_normalizer", c0_symmetry==c0_alt==F(1,2400),
          {"basis":"1/sqrt(pi)","coefficient":str(c0_symmetry)})
    exponents = {"gamma_after_k_substitution":F(6)-F(16,3)+2,
                 "tau_log_density":-F(8,3)+1,
                 "g_log_density":F(6)-F(16,3)+2+1}
    check("density_power_ledger", list(exponents.values())==[F(8,3),-F(5,3),F(11,3)],
          {k:str(x) for k,x in exponents.items()})
    check("conditional_variance_t", 12**2*2==288)
    check("conditional_variance_chi", 576**2*6==1990656)
    check("t_density_prefactor", (12**2*2)*2==24**2,
          {"meaning":"sqrt(2*pi)*sigma_t=24*tau*sqrt(pi)"})
    reject("omit_gamma_symmetry_factor", F(1,4800)-c0_symmetry)
    reject("omit_log_measure_tau_g", (-F(8,3))-(-F(5,3)))
    reject("omit_t_gaussian_normalizer", 1-F(1,24),
           {"formal_basis":"1/(tau*sqrt(pi))","correct_coefficient":"1/24","mutant_coefficient":"1"})

    # Completed square after clearing the positive denominators 2*s2*Delta.
    D = 2*a*s2 + lam*lam
    original = D*(2*a*s2*t*t+(lam*t+mu)**2)
    completed = 2*a*s2*mu*mu+(D*t+lam*mu)**2
    equal("completed_square_denominator_cleared", original, completed)
    reject("wrong_completed_square_center_sign", original-(2*a*s2*mu*mu+(D*t-lam*mu)**2))
    reject("omit_completed_square_constant", original-(D*t+lam*mu)**2)

    # Integration-by-parts identity: derivative of x^(n-1)*exp(-a*x^2), with exponential factored out.
    for n in range(1,13):
        boundary = z**(n-1)
        derivative = boundary.derivative(8)-2*a*z*boundary
        expected = ((n-1)*z**(n-2) if n>1 else 0)-2*a*z**n
        equal("gaussian_IBP_n"+str(n), derivative, expected)
    reject("moment_recursion_wrong_n_coefficient", (3-1)*z**(3-2)-3*z**(3-2))
    reject("moment_recursion_missing_boundary", z**(4-1))

    # Kernel recursion independently checked through Gaussian moments of all even monomials up to degree 20.
    ps = [Poly(1)]
    for k in range(1,11):
        ps.append(kernel_operator(ps[-1],0))
        for m in range(0,21,2):
            got = expected_under_standard_gaussians(ps[k]*z**m)
            check("kernel_moment_k"+str(k)+"_m"+str(m), got==F(m**k)*gaussian_moment(m),
                  {"actual":str(got),"expected":str(F(m**k)*gaussian_moment(m))})
    source = extract_functions(inputs/"ddbounds.py", {"_p_next","kernel_signed","kernel_abs"}, {})
    supplied_ps = [{0:1}]
    for k in range(1,11):
        supplied_ps.append(source["_p_next"](supplied_ps[-1]))
        equal("source_kernel_recurrence_k"+str(k),
              sum((coef*z**j for j,coef in supplied_ps[k].items()),Poly(0)), ps[k])
    source["P"] = supplied_ps
    for A in range(9):
        for B in range(9-A):
            op = Poly(1)
            for _ in range(B): op = kernel_operator(op,1)
            for _ in range(A): op = kernel_operator(op,0)+2*kernel_operator(op,1)
            claimed = sum((math.comb(A,j)*2**(A-j)*ps[j]*ps[A-j+B].substitute({8:w})
                           for j in range(A+1)),Poly(0))
            equal("mixed_kernel_formula_"+str(A)+"_"+str(B), op, claimed)
            imp = source["kernel_signed"](A,B)
            equal("source_mixed_kernel_"+str(A)+"_"+str(B),
                  sum((coef*z**i*w**j for (i,j),coef in imp.items()),Poly(0)),claimed)
            bound = source["kernel_abs"](A,B)
            check("source_absolute_kernel_coefficients_"+str(A)+"_"+str(B),
                  all(coef>=0 for coef in bound.values()) and
                  all(bound.get((m[8],m[9]),0)>=abs(coef) for m,coef in claimed.terms.items()))
    bad_p2 = (z*z-1)*ps[1]+z*ps[1].derivative(8)
    reject("kernel_derivative_sign_reversed",bad_p2-ps[2],
           {"E_mutant_p2":str(expected_under_standard_gaussians(bad_p2)),"expected_zero":"0"})
    reject("omit_chi_log_scale_two", (z*z-1)+(w*w-1)-((z*z-1)+2*(w*w-1)))

    # Exact tail witnesses, no floating cube roots: parameterize by v,t,sign and recover chi.
    cases=0
    for V1 in (F(3),F(7,2),F(4),F(6),F(10)):
        T1=V1*V1/6-1
        X1=2*V1**3-8-12*T1
        check("positive_tail_threshold_"+str(V1),T1>0 and X1>0)
        for V in (V1,V1+F(1,7),2*V1):
            for T in (-2*V1*V1,-T1,-T1+F(1,100),F(0),T1-F(1,100),T1,F(1),2*V1*V1):
                if V*V < 3*max(1-T,0): continue
                r=4*V**3-12*(1-T)*V
                if r<0: continue
                for sign in (-1,1):
                    C=sign*r-8+12*T
                    check("tail_inclusion_case_"+str(cases),abs(T)>=T1 or abs(C)>=X1)
                    cases+=1
    witness_rejection("omit_chi_tail_event", {"rejects":abs(F(0))<F(1,2),
                      "v1":"3","v":"3","t":"0","chi":"64","T1":"1/2","X1":"40"})
    witness_rejection("omit_t_tail_event", {"rejects":abs(F(16))<40,
                      "v1":"3","v":"3","t":"-1","chi":"16","T1":"1/2","X1":"40"})
    witness_rejection("drop_v1_at_least_3_domain", {"rejects":F(1)**2/6-1<=0,
                      "v1":"1","T1":"-5/6","meaning":"refutes positive-threshold premise, not the set inclusion (which becomes vacuous)"})
    return {"tail_rational_cases":cases,"kernel_moment_cases":110,
            "mixed_kernel_orders":45,"source_definitions_executed":["ddint.poly_in_t","ddbounds._p_next","ddbounds.kernel_signed","ddbounds.kernel_abs"]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    inputs=root/"inputs"
    names=("DD_PROOF.md","ddbounds.py","ddint.py","SOFT_CLOSED_FORM_PROOF.md")
    hashes={name:{"bytes":len((inputs/name).read_bytes()),"sha256":hashlib.sha256((inputs/name).read_bytes()).hexdigest()} for name in names}
    inventory=run_checks(inputs)
    unchanged=all(hashlib.sha256((inputs/name).read_bytes()).hexdigest()==value["sha256"] for name,value in hashes.items())
    if not unchanged: raise RuntimeError("Input changed during checks")
    result={"schema":"C271-exact-support-v1","status":"PASS_EXACT_SUPPORT_ONLY",
            "performer":"OpenAI/Codex /root/c267_next_task_triage, delegated work for Dylan Roy",
            "exposure":"source-exposed nonauthor support; same root team; organizational-independence credit 0",
            "python":sys.version,"optimized":bool(sys.flags.optimize),
            "source_inputs":hashes,"inputs_unchanged":unchanged,
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "positive_count":len(positive),"negative_count":len(negative),"coverage_inventory":inventory,
            "positive_checks":positive,"negative_controls":negative,
            "limits":["Polynomial identities and finite rational witnesses do not establish theorem completion.",
                      "No author control imported; only four named pure source definitions executed.",
                      "No general differentiation-under-integral or global domination proof.",
                      "No fractional Gaussian-moment gamma evaluator or interval-arithmetic validation.",
                      "No tail integral bound, certificate replay, node recomputation, CI or scientific promotion.",
                      "The tail grid is finite support; general inclusion remains a mathematical review obligation.",
                      "Source (2.5)/(2.7) conditional mathematical hypotheses remain inherited."]}
    encoded=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    print(encoded,end="")


if __name__=="__main__":
    main()

```
