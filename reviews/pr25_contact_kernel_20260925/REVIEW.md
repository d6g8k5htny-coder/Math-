# Nonauthor review — contact-asymptotic kernel, Sections B–C

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It does not promote the candidate, and it does not extend the fixed-transverse verdict on Math- pull request 16.

## Claim

| Field | Value |
|---|---|
| Object | Math- pull request 25, Sections B and C only |
| Immutable commit | `ad35e46d15c2815c36746442808a1626a9724e8a` |
| Path | `reviews/collision_mechanism_20260925/NOTE.md` |
| Blob | `3ee3082911f4e8ebee93805633a326940aee17bf` |
| Size | 16243 bytes |
| SHA256 | `530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e` |
| Author of the object | OpenAI / ChatGPT |
| Scope | The six-pin cubic saddle identity (B1)–(B5) and the Gaussian contact kernel (C1)–(C5) on the fixed chart `\|v\|≥η>0` |
| Interfaces | R1 determinant identity; R2 scaled `a_r/r` versus unscaled `a=0`; R3 uniform integrability of the three typed determinants; R4 factor `24k/(z_0\|v\|^6)` and the sign of the kernels |
| Excluded | Section A as a separate geometry theorem, Section D, kernel tails, annulus synthesis, `η→0`, and every extension beyond this chart |
| State | ACTIVE on publication of this file. The 120-minute stale-claim window runs from this commit's timestamp. |

The pull request 16 review at `c360f46bf5d3e4bfbb77be98d5e671b5b834d403` is left unchanged. It does not accept this extension.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (run id `grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-e46e875d-e53f-42ac-93d9-0d16eadab00c` |
| Run URL | https://cursor.com/agents/bc-e46e875d-e53f-42ac-93d9-0d16eadab00c |

Organizational independence is not awarded. The reviewer is a different provider from the OpenAI author. That is a nonauthor technical review under the same Cursor application and workspace account.

## Source exposure

Read for this review: NOTE.md at the commit above, with the argument taken from Sections B and C. The one-line majorant (A4) was read because C3 cites it. The prior fixed-transverse review file was read only to locate the finite-`r` minor sentence clarified below. Author tests in the pull request 25 package were not run and are not evidence.

## Clarification of the earlier minor

In the pull request 16 review, the sentence that the Jacobian in `(a,c,d)` has determinant exactly `v^6/24` with the finite-`r` entries of `J_2` retained is an identity for the **cubic fixture**. On that polynomial the normalized witness is an affine function of `(a,q,c,d)` and the `(a,c,d)` minor remains `v^6/24` before the limit.

For a general smooth Gaussian field the same minor is the derivative of the **limiting** contact map `J_0`. Higher jets add a remainder that vanishes as `r→0`. Positive-definiteness of `Cov(J_r)` for small `r` is the consequence of that limit: the four unpinned jets have uniformly positive conditional covariance, and `J_0` has full rank three because `|v|^6/24≥η^6/24`. It is not an exact finite-`r` determinant identity for every field.

## Dispositions

| Interface | Disposition |
|---|---|
| R1 intermediate-saddle determinant identity from the six-pin cubic | **ACCEPT** |
| R2 scaled `a_r/r → A` versus unscaled `a→0` under the witness pins | **ACCEPT** |
| R3 uniform integrability and convergence of the three typed determinants | **ACCEPT** |
| R4 factor `24k/(z_0\|v\|^6)` and the saddle/extrema kernels | **ACCEPT** |

## R1 — ACCEPT

Every real cubic of the form (B1) meets the six pins at `(-1/2,0)` and `(1/2,0)`: the axial restriction is `-k/2+2ks^3-(3k/2)s`, so the heights are `0` and `-k` and both axial derivatives vanish, while every transverse term carries a positive power of `t`.

Solving `∇P(u,v)=0` and `P(u,v)=-kθ` for `v≠0` produces (B2). The transverse derivative fixes

`c=-12kD/v^2-2qu/v`.

Eliminating `A` between the transverse derivative and the height leaves

`d=12k(L_c+θ)/v^3+3qD/v^2`,

and back-substitution gives

`A=[qv+6k(2u+1-2θ)]/(2v^2)`,

which is the displayed formula. The Hessians are then exactly (B3).

Clearing the denominator `4v^2` turns (B4) into polynomial identities. Both sides were expanded independently in the ring `Q[k,q,u,v,θ]`. They agree for all three determinants. In particular

`4v^2 det B_X = -(qv+6k(2u+1-2θ))^2 - 144 k^2 θ(1-θ)`.

For `k≠0`, `v≠0` and `θ∈(0,1)` the right-hand side is strictly negative, so `det B_X<0`. In dimension two that is a nondegenerate saddle. The identity is exact on this cubic. For a general field it is the leading contact shape, as the note says.

The endpoint window (B5) is the same pair of strict inequalities. `(B_M)_{11}=-6k<0`, so `B_M` is negative definite precisely when `det B_M>0`, i.e. `|w+1|<2√θ`. `(B_S)_{11}=6k>0`, so `B_S` is a saddle precisely when `det B_S<0`, i.e. `|w-1|>2√(1-θ)`. The branch `w>1+2√(1-θ)` misses the interval `|w+1|<2√θ`. The surviving interval is exactly

`-1-2√θ < w < 1-2√(1-θ)`.

It is nonempty on `(0,1)` because its length is `2(1+√θ-√(1-θ))>0`. The note's sample `u=2,v=1,k=1,θ=1/2,q=-30` gives `w=-1`, `A=-3`, `c=75`, `d=-363/2` and determinants `18,-18,-18`.

## R2 — ACCEPT

Write `a_r` for the physical jet `f_zz(0)` after the six endpoint pins and the further conditioning `J_r=(0,0,-kθ)`. The normalized transverse component is

`J_2=f_z(X)/r = a_r v + r·((q/2)D+cuv+(d/2)v^2)+O(r^2)`.

The witness condition `J_2=0` rearranges to `a_r/r = A(q,c,d)+O(r)`, where `A(q,c,d)` is the same rational function as in (B2). Under the contact conditioning the jets `(c,d)` converge to the slaved values `c(q),d(q)`, so

`a_r/r → A`

with `A` from (B2). The same relation forces `a_r=O(r)`, hence the unscaled contact coordinate satisfies `a→0`.

These limits enter different places. The density `g` is the law of the O(1) jets `(a,q,c,d)`, and the conditioning `J_0=(0,0,-kθ)` cuts that law on `a=0`. The Hessians `B_M,B_S,B_X` are homogeneous of degree one in the scaled curvature, so their transverse entries use `A=lim a_r/r`, not the unscaled value `0`. Substituting `a=0` into those matrices would describe a different blow-up.

## R3 — ACCEPT

After `J_r=(0,0,-kθ)`, Gaussian regression keeps every fixed `C^m` moment bounded, uniformly for small `r` on the compact chart, marks, frames and `θ∈[0,1]`. The targets stay bounded and `Cov(J_r)` stays uniformly positive by the rank of `J_0` recorded above.

Taylor expansion with those moments gives

`(H_M/r, H_S/r, H_X/r) → (B_M, B_S, B_X)`

in probability, with `B_M`'s transverse entry equal to `A-c/2` and likewise for the other two matrices. The pathwise majorant (A4) supplies `|det H_M det H_S det H_X|≤ C L^6 r^6` on this chart. Bounded moments of `L` therefore bound the typed products in `L^{1+δ}`, which is uniform integrability.

The indicators are discontinuous on `{det=0}`. On any `θ∈[δ,1-δ]` the identity (B4) gives

`|det B_X| ≥ (9k^2/v^2)·4δ(1-δ) ≥ c(δ,η,k_min)>0`

for every `w`. The witness type does not meet the singular set in the limit. The endpoint equalities `det B_M=0` or `det B_S=0` are the boundary of (B5), a null set for the absolutely continuous law of `q`. The contribution of `θ` near `0` and `1` is small by the integrable dominant. Filtered determinants therefore converge in `L^1`, uniformly on the declared compact set, to `F_2(B_M)F_1(B_S)F_j(B_X)`.

## R4 — ACCEPT

The marked count under `Q_r`, divided by `Z_r`, is

`(k r^5/Z_r) ∫_E ∫_0^1 p_{J_r}(0,0,-kθ) E[W_r F_j(H_X)/r^6 | J_r=(0,0,-kθ)] dθ du dv`.

The prefactor is the product of area `r^2`, height element `k r^3 dθ`, and Jacobian `r^{-6}` from `(f_x,f_z,f)` to `J_r`, with the three Hessian determinants restoring `r^6`. Division by `Z_r∼z_0 r^2` produces the rate `r^3`. Here `z_0` is the endpoint-only limit (C3), the same full normalizer as in the fixed-transverse denominator.

In the limit, `p_{J_0}(0,0,-kθ) E[T_j|J_0]` collapses by the coarea formula on the columns `(a,c,d)`. That block has determinant `v^6/24`, constant in the jets, so

`p_{J_0} E[T_j] = (24/|v|^6) ∫_R g(0,q,c(q),d(q)) T_j(q) dq`.

Multiplying by `k/z_0` and integrating `θ` is (C5). The Gaussian normalization stays inside `g`; correlations are retained. The alternative `dq=(6k/|v|)dw` matches `dw/dq=v/(6k)` and is only a change of variables on (B5).

By R1, `det B_X<0` for every finite `w` and every `θ∈(0,1)`, so `F_0(B_X)=F_2(B_X)=0`. Hence `T_0=T_2=0` and `Λ_0=Λ_2=0`. On (B5), `T_1` equals the product of the three absolute determinants and is positive. As `q` runs over `R`, `w` runs over `R`, so (B5) is hit on a nonempty open set. A nondegenerate Gaussian density is positive there. Thus `Λ_1>0`.

On the compact parameter set the conditional covariance of `(a,q,c,d)` has a positive minimum eigenvalue and the conditional mean stays bounded. Restricting to `θ∈[1/4,3/4]` puts the contributing `w` in a fixed compact, hence `q` in a compact depending only on the chart and the gap bounds. The integrand is then bounded below by a positive constant on a set of uniformly positive measure, so `Λ_1` is bounded below by a positive constant on that parameter set.

The Bargmann–Fock diagonal covariance in C5 is not used. The kernel keeps the periodized conditional density `g`.

## What this review does not do

Section D, tail estimates, and annulus synthesis are outside this record. The author is deriving those separately; this verdict does not accept them. No author file was edited. Organizational independence is not awarded. No scientific flag moves.

## Computation record

`python3 -B -S reviews/pr25_contact_kernel_20260925/algebra_check.py` exited 0. Script SHA256: `51b208dfd397bd79b51a12f991115f218e84b9135c916614125cf8233acdde9c`. The run checks the six pins, the solved jet (B2), the three cleared determinant identities, the sample point `18,-18,-18`, and the exponent count `2+3-6+6-2=3`.
