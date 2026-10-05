# LM006 endpoint extension by explicit integral kernels

Dylan Roy — delegated AI mathematical work. Actual author: **OpenAI / GPT-6
Astra Pro**, session `cross-source-closure-round9-20261005`, 5 October 2026.
Author-side additive companion; scientific effect **NONE**; organizational
independence credit **0**. This note neither edits nor reclassifies the frozen
historical LM006 body. It is not an independent review or a Lean formalization.

## 1. Question, target, and assumptions

The target is the six **pin-adjusted endpoint variables** in §§2–3 and the
uniform eighth-moment input in §7 of P02-LM-006 / LCR-DER-019-v1.0 [S1]. The
historical body has 9,147 bytes and SHA256
`239ed094f70aa4352021572ad8bdc0c6ac6404edab4e1d7e61addec0c6659150`.
Its later source-bound review [S2] is conditional, not an unconditional
exact-field acceptance. A nine-midpoint-jet moment is not by itself a moment
bound for the six endpoint variables considered here.

We give a direct argument with the following explicit hypotheses. Work on one
unconditioned probability space and interpret differentiability in its real
Hilbert space H = L². For a centered real Gaussian field near the origin put

    F(x) = f(x,0),       H_y(x) = f_y(x,0),       Q(x) = f_yy(x,0).

Assume F is C³ as an H-valued map, H_y is C², and Q is continuous, on a common
open interval around zero. The indicated derivatives are the field's actual
mean-square derivatives: F' = f_x, F'' = f_xx, F''' = f_xxx,
H_y' = f_xy, and H_y'' = f_xxy. The finite families in question are jointly
Gaussian; derivatives and the integrals below remain Gaussian as L² limits of
linear combinations. Also assume that the covariance G₀ of

    J = (f, f_x, f_y, f_xx, f_xy, f_xxx)(0)

is positive definite. These are hypotheses, not facts inferred from an old
status label. The field-to-source identification and the verification of G₀
are separate from this endpoint argument. Nondegeneracy of Q conditional on J
is **not needed** for the endpoint extension or eighth moment proved here; it
is needed by the separate strictly positive normalizer conclusion in [S1].

Fix b = 6/5. Write r > 0, h = r/2, M = (-h,0), S = (h,0), with r sufficiently
small that the interval used below lies in the domain. The raw pin vector is

    X_r = (F(-h), F'(-h), H_y(-h), F(h), F'(h), H_y(h)),

conditioned to (b,0,0,b-r³/6,0,0). Conditioning means the canonical Gaussian
regression law of the finite targets given X_r; the positive-definite pin
covariance proved below makes this law well-defined for every prescribed pin
value. It is the endpoint marginal of the usual Gaussian conditional field.
There is no conditioning on a good-event truncation.

**Result.** Under exactly these hypotheses, the conditional means and
covariances of the six adjusted endpoint variables extend continuously to
r = 0, with limiting law

    (-1, 1, -a/2, a/2, Q_L, Q_L),

where (a,Q_L) is the conditional law of (f_xxy(0), f_yy(0)) given
J = (b,0,0,0,0,2). The six-dimensional limiting covariance is allowed to be
singular. All its conditional eighth moments are uniformly bounded for
sufficiently small r. Consequently the exact typed endpoint weight has
E[W_r²] ≤ C r⁴, and W_r/r² is uniformly integrable. The constants and the
sufficiently small radius are qualitative, not numerical certificates.

## 2. An explicit equivalent pin frame

Define P_r = (P₀,…,P₅) by

    P₀ = (F(-h)+F(h))/2,
    P₁ = (F'(-h)+F'(h))/2,
    P₂ = (H_y(-h)+H_y(h))/2,
    P₃ = (F'(h)-F'(-h))/r,
    P₄ = (H_y(h)-H_y(-h))/r,
    P₅ = (12/r²) [ P₁ - (F(h)-F(-h))/r ].                 (2.1)

This is an invertible linear transform for every r > 0. Indeed its inverse is

    F(±h)   = P₀ ± (r/2)P₁ ∓ (r³/24)P₅,
    F'(±h)  = P₁ ± (r/2)P₃,
    H_y(±h) = P₂ ± (r/2)P₄.                              (2.2)

Thus no pin is lost, duplicated, or replaced. This is an explicit alternative
frame; no row-by-row identity with an unspecified historical GP-DER-044 frame
is asserted. Conditioning on X_r equals conditioning on P_r at the transformed
value. For the actual prescribed pins this value is exactly

    d_r = (b-r³/12, 0, 0, 0, 0, 2),                     (2.3)

and d_r → d₀ = (b,0,0,0,0,2). In particular the limiting cubic pin is **2**, not
an unproved inference from the signs of the two Hessians.

## 3. Integral identities remove the singular quotients

All integrals in this section run over I = [-1/2,1/2] and are Bochner integrals
in H. The Hilbert-space fundamental theorem of calculus gives

    P₃ = ∫_I F''(ru) du,
    P₄ = ∫_I H_y'(ru) du,
    P₅ = 6 ∫_I (1/4-u²) F'''(ru) du.                    (3.1)

For the last identity, put g(u) = F'(ru). Integration by parts twice gives

    ∫_I (1/4-u²) g''(u) du
        = g(1/2)+g(-1/2) - 2∫_I g(u)du.

Since g''(u) = r²F'''(ru), substitution into (2.1) proves (3.1). The kernel
6(1/4-u²) is nonnegative and has integral 1. In particular P₅ converges in L²
to F'''(0), with no unjustified division of an unconditioned derivative by r.

Define the same adjusted endpoint variables as [S1]:

    A_± = (F''(±h)-P₃)/r,
    B_± = (H_y'(±h)-P₄)/r,
    C_± = Q(±h).                                        (3.2)

Applying the fundamental theorem once more and changing the order of
integration over the finite triangle gives the exact identities

    A_- = -∫_I (1/2-u) F'''(ru) du,
    A_+ =  ∫_I (u+1/2) F'''(ru) du,
    B_- = -∫_I (1/2-u) H_y''(ru) du,
    B_+ =  ∫_I (u+1/2) H_y''(ru) du.                    (3.3)

The two signed kernel masses are -1/2 and +1/2; each absolute kernel mass is
1/2. The identities are unconditioned linear-functional identities, before
imposing the pins. On the actual pin subspace P₃=P₄=0, so they become exactly
f_xx(M)/r, f_xx(S)/r, f_xy(M)/r, f_xy(S)/r. This order matters: for F(x)=x²,
F''/r=2/r diverges but both adjusted A variables are identically zero.

For any continuous H-valued map U, set

    ω_U(r) = sup_{|x|≤r/2} ||U(x)-U(0)||_H → 0.

Then ∥∫_I k(u)[U(ru)-U(0)]du∥_H ≤ ∥k∥₁ ω_U(r). Thus (3.1)–(3.3) prove
joint L² convergence, on the original unconditioned probability space,

    (P_r, V_r) → (J,T),
    V_r = (A_-,A_+,B_-,B_+,C_-,C_+),
    T = (-F'''(0)/2, F'''(0)/2,
         -H_y''(0)/2, H_y''(0)/2, Q(0), Q(0)).           (3.4)

Finite-dimensional joint convergence here follows by summing the squared
component L² errors. Cauchy–Schwarz then gives convergence of all covariance
entries, including pin–target cross-covariances. The same formulas show
continuity for positive r and extension at zero. No samplewise Taylor bound
under a changing conditional law is being assumed.

## 4. Conditional means as well as covariances

Write the unconditioned covariance blocks as

    G_r = Cov(P_r),   K_r = Cov(V_r,P_r),   B_r = Cov(V_r).

All three extend continuously at zero by (3.4). Let λ₀ be the smallest
eigenvalue of G₀, positive by hypothesis. For sufficiently small r,
∥G_r-G₀∥op ≤ λ₀/2, hence G_r ≥ (λ₀/2)Id and ∥G_r⁻¹∥op ≤ 2/λ₀. This proves
that both P_r and its invertible raw-pin transform are nondegenerate. The
canonical conditional Gaussian law is N(m_r,Σ_r), with

    m_r = K_r G_r⁻¹ d_r,
    Σ_r = B_r - K_r G_r⁻¹ K_rᵀ.                         (4.1)

For completeness, subtract K_r G_r⁻¹P_r from V_r. The resulting Gaussian
residual has zero covariance with P_r, so their joint Gaussian characteristic
function factors. They are independent, proving (4.1) for every pin value.

Because K_r, G_r⁻¹, and d_r all converge, m_r converges and is bounded. This
step is indispensable: a Loewner bound on the conditional covariance alone
does not control a conditional mean. The covariance Σ_r also converges and
is positive semidefinite, including at zero; it need not be invertible.
Equation (4.1) at r=0 is the conditional law of T given J=d₀. Its first two
coordinates are (-1,1), and the remaining coordinates have precisely the
(a,Q_L) description in §1. Convergence of Gaussian characteristic functions
now gives weak convergence of these conditional laws. No common samplewise
coupling of the original conditioned fields is claimed or needed.

## 5. The genuine endpoint eighth moment and the exact weight

Choose a sufficiently small r₁ ≤ 1. From §4 there are finite M and Λ such that
∥m_r∥≤M and ∥Σ_r∥op≤Λ for 0≤r≤r₁. For each individual marginal law one may
represent V_r in distribution as m_r+Σ_r^(1/2)Z, where Z is standard Gaussian
in R⁶. This is a statement about its moments, not a claim about the physical
sample paths under all the conditional laws. Therefore

    E||V_r||⁸ ≤ 2⁷ (M⁸ + Λ⁴ E||Z||⁸)
              = 2⁷ (M⁸ + 5760 Λ⁴) =: C₈ < ∞.          (5.1)

The identity E||Z||⁸ = 6·8·10·12 = 5760 follows by differentiating four times
the chi-square moment generating function (1-2t)^(-3) at zero. The scalar
normal eighth moment 105 is not the six-dimensional norm moment.

On the pins the exact physical Hessians are

    H_M = [[rA_-, rB_-], [rB_-, C_-]],
    H_S = [[rA_+, rB_+], [rB_+, C_+]].

Writing Δ_±=A_±C_±-rB_±² gives det H_{M/S}=rΔ_-/+. For 0<r≤r₁≤1, and
R_r=∥V_r∥, one has |Δ_±|≤|A_±C_±|+B_±²≤R_r². The exact typed weight of [S1]
is the absolute determinant product multiplied by its maximum/saddle
indicators, each at most one. Consequently

    0 ≤ W_r/r² ≤ R_r⁴,
    E[(W_r/r²)²] ≤ C₈,
    E[W_r²] ≤ C₈ r⁴.                                    (5.2)

Uniform integrability follows explicitly: for t>0,
E[(W_r/r²) 1{W_r/r²>t}] ≤ C₈/t uniformly in r. This is the full exact-field
endpoint weight, not a quartic Taylor weight or a good-event-renormalized
weight. No numerical value of M, Λ, C₈, or r₁ has been established.

## 6. Sufficient spectral regularity; separate application checks

Here is a sufficient condition for the regularity portion of §1, not an
assertion that a named source satisfies it. Suppose the centered stationary
real field has an actual covariance representation

    C(z) = Σ_{k∈Z²} p_k exp(iν k·z),
    p_k≥0, p_-k=p_k, ν>0,
    Σ_k p_k (1+|νk|⁶) < ∞.                               (6.1)

In its spectral Hilbert representation, a derivative of order |α|≤3 has
symbol (iνk)^α exp(iν k·x). Difference quotients converge in the weighted
L²(p) norm by dominated convergence, using |exp(it)-1|≤|t| and the sixth
spectral moment. Translations of the highest derivatives are continuous by
the bound |exp(it)-1|≤2 and the same summable envelope. Lower orders use the
corresponding lower moments, implied by (6.1). This gives the H-valued
regularity and joint Gaussian derivative family used in §§1–3. No analytic
covariance kernel, density for V₀, or pathwise derivative supremum is needed.

Condition (6.1) alone does **not** prove G₀ positive definite: a spectrum
supported on too few frequencies can be degenerate. The separate seven-node
witness [S3] is one route under its additional positive-weight hypotheses. Its
field-to-symbol identification and review are separate tasks. In particular
this note does not import a mutable review label as a mathematical premise.
The canonical target remains the fixed side-24, d=2, b=6/5 six-pin law. A
change of field, frame direction, birth height or height-gap scaling needs its
own matching; no uniformity over those changes is claimed here.

## 7. Verification scope and reproducibility

The standard-library checker compares direct endpoint formulas with exact
polynomial integrals using `fractions.Fraction`. It tests 14 monomials on six
radii, 120 arbitrary-pin inversions, 18 prescribed-pin transformations, the
subtraction control, kernel masses, and Gaussian norm-moment arithmetic. The
unit suite additionally checks general rational polynomials and invalid
inputs. These tests support the algebra; the Hilbert-space and Gaussian
arguments in §§3–5 are the proof, not a consequence of finite tests.

From the repository root:

```sh
python3 -B -S -m unittest discover -s reviews/lm006_endpoint_extension_20261005 -p 'test_*.py' -v
python3 -B -O -S -m unittest discover -s reviews/lm006_endpoint_extension_20261005 -p 'test_*.py' -v
python3 -B -S reviews/lm006_endpoint_extension_20261005/endpoint_check.py
python3 -B -O -S reviews/lm006_endpoint_extension_20261005/endpoint_check.py
```

The explicit mutants M1–M5 replace 12 by 6 in the cubic pin row, flip the
negative-endpoint kernel sign, omit pin subtraction, reverse the prescribed
height gap, or replace the six-dimensional norm moment with the scalar one.
`--mutant M1` (and each of M2–M5) must exit 1 with `ENDPOINT_CHECK_FAIL`;
`--mutant BAD` must exit 2. Runtime checks do not depend on Python `assert`.
These commands do not fetch sources, access the network, run Lean, or change
any repository status. Existing hosted workflows are not claimed to execute
this new standalone checker automatically.

## 8. Sources, coordination, and exclusions

[S1] P02-LM-006 / LCR-DER-019-v1.0, frozen body named in §1. Public repository
`d6g8k5htny-coder/main`, commit `7caac254cbba5f513b2dc0afb56b78a598bc0c93`, full
file blob `e8d2e822eb49b2fcf3459a58868ce911e6d4ff80`. Exact path, body extraction
rule and consumed sections are in `SOURCES.json`. The original is unchanged.

[S2] Native source-bound conditional review, main#229 comment
[6002603423](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002603423),
xAI/Grok 4.7, Cursor session `bc-ac2ce04c-f30f-4443-8f02-f0943bde635d`.
This is a review of S1, **not of this new note**. New companion review is
separate; old semantic or execution approval is not transferred.

[S3] Author-side explicit Gram witness, main#229 comment
[6002756269](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002756269).
The witness's reviewer retains that separate scope. GP-DER-044 source/frame
reconciliation is separately claimed at comment6002782190. This note does
not duplicate that source audit or silently choose between colliding IDs.
Our endpoint claim is comment6002912204.

External reconnaissance: Louis Gass and Michele Stecconi, *The number of
critical points of a Gaussian field: finiteness of moments*, Probability
Theory and Related Fields **190**, 1167–1197 (2024), DOI
`10.1007/s00440-024-01273-5`; author preprint
[arXiv:2305.17586v2](https://arxiv.org/abs/2305.17586v2), §§1.2 and 2.1.
Located via Consensus and checked against the primary author text and
publisher metadata. Its interpolation treatment is methodological context.
A critical-point **count** moment theorem is not the endpoint-vector moment
premise proved here; no theorem from that paper is used as a substitute for
our pin identities or Gaussian conditioning calculation.

This companion proves an explicit endpoint extension and moment implication
under §1, with a separate sufficient regularity criterion in §6. It does not
by itself certify the covariance/pin identification for the concrete model,
remove the conditional status of S2, prove a Palm event tail, exact capture,
P0.1/P0.2, an all-marks/higher-dimensional assertion, numerical constants, or
full formal-package alignment. No original proof, status/register/prize/flag,
workflow, or prior review disposition is changed. Authoring this companion
is not nonauthor review, integration is not acceptance, and no Lean run is
claimed.
