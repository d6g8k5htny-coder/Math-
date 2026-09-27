# Nonauthor review — PR25 typed contact coefficient and marked transfer

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It is not permission to promote the candidate.

## Claim

| Field | Value |
|---|---|
| Object | Math- pull request 25, issue 29 interfaces R1, R2, R3 |
| Immutable commit | `ad35e46d15c2815c36746442808a1626a9724e8a` |
| Path | `reviews/collision_mechanism_20260925/NOTE.md` |
| Blob | `3ee3082911f4e8ebee93805633a326940aee17bf` |
| Size | 16243 bytes |
| SHA256 | `530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e` |
| Author of the object | OpenAI / ChatGPT |
| Scope | Sections B, C, and D of that note, on the fixed chart already stated there |
| Excluded | Section A as an acceptance target, axis, thin belt, `η→0`, pin or witness collision, intermediate scales, dimension three, numerical enclosure, historical 24-jet closure, elder-defect lower bound, whole-annulus synthesis, pull request 22 |
| Also excluded | Any edit of the author note, and any angular-tail session outside this commit |
| State | ACTIVE on publication of this file. The 120-minute stale-claim convention runs from this commit's author timestamp. |
| Write scope | `reviews/pr25_typed_transfer_nonauthor_20260925/` only |

Issue 29 asked for an acknowledgment on the issue. Issue-comment writes are not available to this agent. This file is the claim and the result.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (run id `grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-89801c5e-c9d7-4f44-9bbb-2bbfe745bebc` |
| Run URL | https://cursor.com/agents/bc-89801c5e-c9d7-4f44-9bbb-2bbfe745bebc |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is **not awarded**. A distinct Cursor session is not organizational independence. The shared workspace account does not separate this run from the account that committed the OpenAI text.

Provider independence is different from that organizational fact. The candidate's author is OpenAI. This reviewer is xAI Grok, not an OpenAI session, so the dispositions below are a nonauthor technical review rather than an OpenAI self-review.

## Source exposure

Read in full, at the immutable commit above: `reviews/collision_mechanism_20260925/NOTE.md`, `README.md` (SHA256 `feb62c5c74eb48f9d1a613f3a3607bbb45ff4a4041563ef24451fae18cfc999e`), and `exact_checks.py` (SHA256 `e51a5bda5b00abe947b4af84e90165ddf9ad8190b459b046112cb4d113b1af0a`). The author unittest was not executed. Its 24 methods are not evidence for these dispositions.

Also read, as coordination rather than as proof: Math- issue 29, the pull request 25 title, and the open pull request 31 body. Pull request 31 is a different xAI session (`bc-e46e875d-e53f-42ac-93d9-0d16eadab00c`) recording a Sections B–C review with a different interface split, and it excludes Section D. That body was not used as analytic evidence. Its `REVIEW.md` and algebra script were not read. The merged pull request 26 review was read only to match the artifact layout; its ACCEPT of the earlier fixed-transverse upper bound is not an acceptance of this kernel or of Section D.

No child agent was spawned. No angular-tail draft was opened or waited on.

## Method

Sections B and C were rederived from the six-pin cubic and from the change-of-variables ledger in the note. Section D was checked as a pushforward, including a sharp-constant counterexample for the cumulative paragraph. Separately, `algebra_check.py` expands the cubic identities in exact Laurent arithmetic over `Q`. A passing run checks those finite identities only.

```sh
python3 -B -S -m unittest reviews.pr25_typed_transfer_nonauthor_20260925.algebra_check -v
```

## Dispositions

| Interface | Disposition |
|---|---|
| R1 six-pin cubic determinant identity and endpoint type interval | **ACCEPT** |
| R2 positive saddle kernel, zero extrema kernels, and the factor `24k/(z_0\|v\|^6)` | **ACCEPT** |
| R3 marked lifetime transfer, with the cumulative hypothesis made explicit | **AMEND_REQUIRED** |

R1 and R2 accept the stated fixed-chart interfaces. They do not accept a probability lower bound, an elder-defect lower bound, or a whole-annulus theorem. R3 accepts the density statement (D1), the derivative counterexample, and the small-mark phase diagram, and it requires an amendment of the cumulative statement (D2).

## R1 — ACCEPT

A polynomial of total degree at most three has ten coefficients. On the axis `t=0`, the value and `s`-derivative determine the four axial coefficients, and `P_t(±1/2,0)=0` forces the coefficient of `s t` to vanish and ties the coefficient of `t` to the coefficient of `s^2 t`. Row reduction over `Q` leaves a four-dimensional solution space, with free monomials `t^2`, `s^2 t`, `s t^2`, and `t^3`. The unique axial solution of the six pins is

`P(s,0) = -k/2 - (3k/2) s + 2 k s^3`

for `k>0`. Extending by the four free jets produces (B1). The constant `-1/4` in the mixed term is the condition `P_t(±1/2,0)=0`, not an extra modeling choice.

Differentiating (B1) gives

`P_ss = 12 k s + q t`, `P_st = q s + c t`, `P_tt = A + c s + d t`,

which is (B3) at `M=(-1/2,0)`, `S=(1/2,0)`, and `X=(u,v)`. Imposing `∇P(X)=0` and `P(X)=-k θ` leaves `q` free and fixes

`c = -12 k D / v^2 - 2 q u / v`,

`d = 12 k (L_c + θ) / v^3 + 3 q D / v^2`,

`A = (12 k u + 6 k + q v - 12 k θ) / (2 v^2)`,

with `D=u^2-1/4` and `L_c=2u^3-3u/2-1/2`. These are (B2). The combination `P-(v/2)P_t` cancels `A` and `c`, which is why `d` is fixed by the height and the transverse derivative together. Exact expansion in the Laurent ring then gives (B4):

`det B_M = (9 k^2 / v^2) [4θ - (w+1)^2]`,

`det B_S = (9 k^2 / v^2) [4(1-θ) - (w-1)^2]`,

`det B_X = -(9 k^2 / v^2) [(w+1-2θ)^2 + 4θ(1-θ)]`,

where `w=(q v + 12 k u)/(6k)`. For `θ∈(0,1)` the bracket in `det B_X` is at least `4θ(1-θ)>0`, so `det B_X<0`. In dimension two that is a nondegenerate saddle. An intermediate-height noncollinear third critical point of a six-pin cubic is therefore a nondegenerate saddle. The note's limit on smooth fields, that this is a leading-contact conclusion, stays in force: R1 does not forbid finite-`r` extrema of a non-cubic field.

The `(1,1)` entries are `(B_M)_11=-6k<0` and `(B_S)_11=6k>0` for every free jet. For a symmetric `2×2` matrix, `det>0` and a negative diagonal entry means both eigenvalues are negative, because `det>0` puts them in the same sign class and a negative diagonal entry forbids positive-definiteness. Thus `M` is a nondegenerate maximum exactly when `det B_M>0`, and `S` is a nondegenerate saddle exactly when `det B_S<0`.

`det B_M>0` is the interval `-1-2√θ < w < -1+2√θ`. `det B_S<0` is the union of `w<1-2√(1-θ)` and `w>1+2√(1-θ)`. The right-hand branch misses the maximum interval because `√θ≤1` and `√(1-θ)≥0`, hence

`-1+2√θ ≤ 1 ≤ 1+2√(1-θ)`,

with both comparisons strict for `θ∈(0,1)`. The surviving upper bound is the smaller of `-1+2√θ` and `1-2√(1-θ)`. These satisfy

`1-2√(1-θ) ≤ -1+2√θ`

because `√θ+√(1-θ)≥1`. Both sides of that comparison are positive, and

`(√θ + √(1-θ))^2 = 1 + 2√(θ(1-θ)) ≥ 1`,

with equality only at `θ∈{0,1}`. The lower bound `-1-2√θ` stays strictly below `1-2√(1-θ)` on `θ∈(0,1)`, because `(1+√θ)^2 = 1+2√θ+θ > 1-θ`. Therefore `M` is a maximum and `S` is a saddle precisely on

`-1 - 2√θ < w < 1 - 2√(1-θ)`,

which is (B5). The endpoint `w=-1` lies in that interval and produces determinant values `+36 k^2 θ/v^2`, `-36 k^2 θ/v^2`, `-36 k^2 θ/v^2`. The sample `(u,v,k,θ,q)=(2,1,1,1/2,-30)` has `w=-1`, jets `A=-3`, `c=75`, `d=-363/2`, and determinants `18,-18,-18`, with `(B_M)_11=-6`.

## R2 — ACCEPT

Two scalings are present, and the note assigns each one to the correct slot.

Under the endpoint law only, the axial second derivatives at the pins are asymptotic to `-6 k r` and `6 k r`, the mixed entries are `O(r)`, and the transverse entry tends to the unscaled jet `a=f_zz(0)`. Then

`det H_M / r → -6 k a`, `det H_S / r → 6 k a`,

so the product of absolute determinants, divided by `r^2`, tends to `36 k^2 a^2`. For small `r` and `a<0`, `H_M` is negative definite and `H_S` has index one. For `a>0` the endpoint weight `F_2(H_M)F_1(H_S)` vanishes. The null set `a=0` does not affect the Gaussian integral. Uniform integrability of the quotient follows from the bounded conditional moments of the rescaled pin transform: the quotient converges in probability to `36 k^2 a^2 1_{a<0}` and is bounded in `L^{1+δ}`. Hence

`Z_r / r^2 → z_0 = 36 k^2 E[a^2 1_{a<0} | U_0]`.

On the stated compact marks, frames, and gaps `k`, the conditional law of `a` is a nondegenerate Gaussian with variance bounded below and mean bounded, so `z_0` has a positive minimum. This is the full endpoint normalizer in (C3). It is the unscaled-`a` limit. Dividing by `r^4` would describe a different, fully blown-up transverse scaling, and that is not the endpoint law.

After the further conditioning `J_r=(0,0,-kθ)`, the second component `f_z(X)/r → a v` forces the unscaled limit `a→0`. The next-order transverse curvature `a_r/r` tends to the chart coefficient `A` in (B2), which depends on the free jet `q` and is nonzero on the positive witness (`A=-3` in the sample, while the density coordinate is `a=0`). Taylor expansion at scale `r` then sends `(H_M/r,H_S/r,H_X/r)` to `(B_M,B_S,B_X)`, and the transverse entry of `B_X` is `A+c u+d v`, the full chart entry. The matrices in `T_j` therefore use `A(q)`. The Gaussian density is evaluated at the unscaled point `a=0`, on the slice `c=c(q)`, `d=d(q)`. Those are different limits, and (C5) keeps them apart.

The witness map on the unscaled jets,

`J_0 = (6 k D + q u v + c v^2/2, a v, k L_c + q D v/4 - d v^3/12)`,

has partial Jacobian in `(a,c,d)` equal to the matrix

`[[0, v^2/2, 0], [v, 0, 0], [0, 0, -v^3/12]]`,

with determinant `v^6/24`. On `|v|≥η` the absolute value is at least `η^6/24`. For the fixed periodized covariance, every dual-lattice mode has positive mass, and the symbols `1`, `ξ`, `ξ^2`, `ξ^3`, `η`, `ξη` in the pin frame are linearly independent polynomials. The conditional covariance of `(a,q,c,d)` given `U_0` is therefore positive definite for every orthonormal frame. It is continuous in the frame, so its smallest eigenvalue has a positive minimum on the circle. The same minor keeps the covariance of `J_r` bounded below for small `r`, uniformly on the compact chart and on `θ∈[0,1]`.

The raw map from `(f_x,f_z,f-b)` to `J_r` is triangular of determinant `r^{-6}`; the height shear `-(r v/2) f_z` does not change that determinant. At a critical point of height `b-k r^3 θ` the target is `(0,0,-kθ)`, and `dh=k r^3 dθ`. Area scales by `r^2`. The three filtered physical determinants scale by `r^6` once the witness conditioning has put every Hessian at order `r`. Division by `Z_r∼z_0 r^2` produces the power

`2 + 3 - 6 + 6 - 2 = 3`.

The slice formula for the limiting density contributes the reciprocal minor `24/|v|^6`. Collecting the height slope `k` gives

`Λ_j = 24 k / (z_0 |v|^6) ∫_0^1 ∫_R g(0, q, c(q), d(q)) T_j(q) dq dθ`,

which is (C5). Here `T_j=F_2(B_M)F_1(B_S)F_j(B_X)`, and `g` is the four-dimensional conditional density given `U_0`, correlations retained. The factor `24/|v|^6` is that reciprocal absolute minor, multiplied by `k` from `dh`.

`F_j` is continuous on all symmetric matrices when it is defined to be zero on the determinant-zero locus, because `|det|` vanishes there, and it has quadratic growth. Uniform conditional derivative moments give uniform integrability of the normalized triple product, so the conditional expectations converge to the expectations of `T_j`. By (B4), `T_0=T_2=0` identically on `0<θ<1`, while `T_1` is strictly positive on a neighborhood of `w=-1`, `θ=1/2`, where `g>0`. Thus `Λ_0=Λ_2=0` and `Λ_1>0`, uniformly for the stated compact parameters, chart, and frames. The saddle mean is of exact order `r^3` on positive-area subsets of `K`. The extrema means are `o(r^3)`.

This accepts (C1)–(C5) on that chart. It does not accept an adjacency event, a collision of the witness with a pin, a vanishing transverse coordinate, or a lower bound on the probability of an elder defect.

## R3 — AMEND_REQUIRED

The density theorem (D1) holds under the four hypotheses written in Section D.

Let `β=(α+1)/m` and let `r=R(ℓ,z)` be the inverse of `ℓ=h(r,z)`. The local density is

`ν_local(ℓ) = ∫ R^α b(R,z) / h_r(R,z) dλ`,

with the integrand omitted where no inverse lies in `(0,r_0)`. The assumptions `h/(κ r^m)→1` and `h_r/(m κ r^{m-1})→1` give

`R^α / h_r ∼ ℓ^{β-1} / (m κ^β)`.

The uniform bounds `c_0 κ r^m ≤ h ≤ C_0 κ r^m` and `h_r ≥ c_1 κ r^{m-1}` dominate the normalized integrand by a constant multiple of `G κ^{-β}`, which is integrable by hypothesis 2. Dominated convergence yields (D1). The coefficient must be shown positive before a positive asymptotic law is claimed; the note already says this.

The derivative counterexample is correct. For `h(r)=r^3(1+r sin(1/r))` on `(0,1/4)`,

`h'(r)=r^2 [3 - cos(1/r) + 4 r sin(1/r)]`,

and `3-cos+4 r sin ≥ 1`, so `h'>0`. Also `h(r)/r^3→1`. The normalized density along `h(r)` equals

`[1+r sin(1/r)]^{1/3} / [3 - cos(1/r) + 4 r sin(1/r)]`,

which tends to `1/2` along `r=1/(2π n)` and to `1/4` along `r=1/((2n+1)π)`. No density coefficient exists. The cumulative integral `∫_0^R r dr = R^2/2` still satisfies `N(ℓ)∼ℓ^{2/3}/2` because the ratio hypothesis holds. Dropping the derivative limit while keeping `h/(κ r^m)→1` is the right separation.

The product phase diagram is correct. For `dμ=r^α κ^q dr dκ` on `(0,1)^2` and `ℓ=κ r^m`,

`ν(ℓ)=ℓ^{β-1}/m ∫_ℓ^1 κ^{q-β} dκ`.

With `δ=q+1-β` this is `ℓ^{β-1}(1-ℓ^δ)/(m δ)` for `δ≠0` and `ℓ^{β-1} log(1/ℓ)/m` for `δ=0`. For `α=1`, `m=3`, `q=-1/2`, one has `δ=-1/6` and `ν(ℓ)=2(ℓ^{-1/2}-ℓ^{-1/3})`. At `ℓ=1/64` the value is `8`, while a pure multiple of `ℓ^{-1/3}` does not reproduce that value. The general theorem's envelope `∫ G κ^{-β} dλ<∞` excludes this small-mark regime. The selection rule in D3 is the same power count: a factor `r^γ` replaces `α` by `α+γ`. For `α=1`, `m=3` and a positive pairing limit, `C=(1/3)∫ a_0 p_0 κ^{-2/3} dλ` gives `ν∼C ℓ^{-1/3}` and `N∼(3/2) C ℓ^{2/3}`, since `∫_0^ℓ t^{-1/3} dt = (3/2) ℓ^{2/3}`.

The cumulative statement (D2) needs an explicit retained hypothesis `h/(κ r^m)→1`. The paragraph that introduces (D2) drops "the derivative hypotheses" and invokes "monotonicity and the same comparison/envelope assumptions." Comparison bounds do not fix the constant. If `h=2 κ r^m`, then `c_0=1` and `C_0=3` are legal, `h_r/(m κ r^{m-1})=2`, and both ratio limits fail. For `α=1`, `m=3`, `κ=b=1`, and `R=1/2`,

`ℓ=1/4`, `N=R^2/2=1/8`, `N^3=1/512`,

while the displayed constant `ℓ^{2/3}/2=2^{-7/3}` has cube `1/128`. The sharp constant is off by `2^{-2/3}`. The written proof passes from `∫_0^R r^α b dr ∼ b_0 R^{α+1}/(α+1)` to (D2) without the equivalence `R^{α+1}∼ℓ^β κ^{-β}`, which is exactly `(h(R)/(κ R^m))^β→1`.

Amendment required in the cumulative paragraph, and only there:

- Retain `h(0+,z)=0`, monotonicity, `b(r,z)→b_0(z)`, the envelope `∫ G κ^{-β} dλ<∞`, and the limit `h/(κ r^m)→1`.
- Retain a domination hypothesis that bounds `R^{α+1}` by a multiple of `(ℓ/κ)^β`. The existing lower comparison `h≥c_0 κ r^m` is enough for that bound.
- The derivative limit `h_r/(m κ r^{m-1})→1` and the lower bound on `h_r` are not required for (D2). They remain required for (D1).
- Insert the equivalence `R^{α+1}∼(ℓ/κ)^β` in the proof, before the constant `1/(α+1)` is identified with (D2).

With that sentence restored, (D2) matches (D1) on the overlap of the hypotheses, because `∫_0^ℓ C t^{β-1} dt = C ℓ^β / β` and `1/(α+1)=1/(m β)`. As written, (D2) does not yet say this, so the interface is **AMEND_REQUIRED**. The rest of Section D does not need a change of mathematical statement.

## Boundary of this review

The fixed chart `K` with `|v|≥η>0` and `A_0≤√(u^2+v^2)≤B<∞` is the whole geometric domain of the R2 acceptance. The minor `v^6/24` vanishes on the axis. Nothing here accepts pull request 22, a two-scale annulus, a shrinking gap, or a program-level closure.

## What this review does not do

- It does not edit `reviews/collision_mechanism_20260925/`.
- It does not treat `exact_checks.py`, or the pull request 31 body, as the proof.
- It does not award organizational independence.
- It does not flip a scientific status bit.
- It does not spawn a child agent or consume a separate angular-tail session.

## Computation record

`python3 -B -S -m unittest reviews.pr25_typed_transfer_nonauthor_20260925.algebra_check -v` exited 0 (12 tests). Script SHA256: `f645c6f87714acb9c84b5163ffd05a008dc0f8b5d19e4b374f7e01a3c7342e0d`. The passing identities are the six-pin null-space dimension and axial solution, the (B2) critical-point equations, the three determinant identities (B4), the sign of the witness minor `v^6/24`, the endpoint quotient `36 k^2 a^2`, the separation of chart `A` from unscaled `a=0`, the power `2+3-6+6-2=3`, the cubes `1/512≠1/128` for `h=2 r^3`, the density limits `1/2` and `1/4`, and the small-mark value `2(8-4)=8` at `ℓ=1/64`.
