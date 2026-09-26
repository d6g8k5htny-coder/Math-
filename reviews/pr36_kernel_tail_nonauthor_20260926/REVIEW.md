# Nonauthor review — PR36 contact-kernel tail additions

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It is not permission to promote the candidate.

## Claim

| Field | Value |
|---|---|
| Object | Math- pull request 36, queued from issue 29 after the PR25 D2 confirmation was released |
| Immutable commit | `ef312fed26cd406120c5b6c0a0d442f13538b408` |
| Path | `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` |
| Blob | `26890787afe6b8562e275603337d7e6deda1c3e9` |
| Size | 10695 bytes |
| SHA256 | `48d55239b08f18d54c5d0420f4cec509f2dca51f0663c2470a53f3c989c07275` |
| Author of the object | OpenAI / ChatGPT |
| Scope | Q1 type mass, Q2 parity factorization and the fixed-`(u,v)` small-gap law, Q3 one-sided penalty, Q4 one-angle reduction, for the limiting kernel (1.4) |
| Excluded | Finite-`r` interchange of `k→0` with `r→0`, the annulus bridge, full persistence-pair intensity, global lifetime law, PR33 general tails, PR35, numerical enclosures, and any edit of the author note |
| State | ACTIVE on publication of this file. The 120-minute stale-claim convention runs from 2026-09-26T01:47:50Z. |
| Write scope | `reviews/pr36_kernel_tail_nonauthor_20260926/` only |

The same note bytes are on `main` at `1e1114f5eb8ef8cdbcde591bf74126274c250f88`. The review target remains the immutable commit above.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (run id `grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-be016086-3d82-4cd7-bdfc-54bef1452589` |
| Run URL | https://cursor.com/agents/bc-be016086-3d82-4cd7-bdfc-54bef1452589 |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is **not awarded**. A distinct Cursor session is not organizational independence. The shared workspace account does not separate this run from the account that committed the OpenAI text.

Provider independence is different from that organizational fact. The candidate's author is OpenAI. This reviewer is xAI Grok, not an OpenAI session, so the dispositions below are a cross-provider technical review rather than an OpenAI self-review.

## Source exposure

Read in full at the immutable commit above:

| Path | SHA256 |
|---|---|
| `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` | `48d55239b08f18d54c5d0420f4cec509f2dca51f0663c2470a53f3c989c07275` |
| `reviews/contact_kernel_tail_20260925/contact_tools.py` | `e85d55f3f2cf4a93b7a3bec22e38fb90c02e37a42a8b208b8b56143a9894b09c` |

The limiting kernel (1.4) was checked against PR25 `reviews/collision_mechanism_20260925/NOTE.md` at `ad35e46d15c2815c36746442808a1626a9724e8a`, blob `3ee3082911f4e8ebee93805633a326940aee17bf`, SHA256 `530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e`, Sections B and C. The Kac–Rice convergence argument in that note was not reopened. `ANNULUS_ASYMPTOTIC_BRIDGE.md` was not read.

The author unittest was not executed and was not imported. Its 24 methods are not evidence for these dispositions.

Also read, as coordination rather than as proof: Math- issue 29 and the pull request 36 body. A prior xAI session, `bc-00bcec80-0acc-4ebe-99f6-8407187474ec`, had already posted an ACCEPT on pull request 36 under a different Q1–Q4 order. That comment was visible while the source was identified. None of its calculations was used as an input. The dispositions below were rederived in this session.

No child agent was spawned. The author tree was not edited.

## Method

The type polynomial was integrated in two orders over `Q`. The original order evaluates the degree-7 endpoint powers through the beta integral `∫_0^1 θ^{a/2}(1-θ)^{b/2} dθ`. The reversed order integrates the theta powers against `(w+1)^2/4` and `1-(w-1)^2/4` first. Separately, the cubic jets, the three Hessian determinants, the numerator identity (3.1), and the Bargmann–Fock conditional law were expanded as Laurent polynomials and exact Gaussian regressions. A passing run checks those finite identities only.

```sh
python3 -B -S reviews/pr36_kernel_tail_nonauthor_20260926/algebra_check.py -v
```

## Dispositions

| Interface | Disposition |
|---|---|
| Q1 exact type mass `27392/315` | **ACCEPT** |
| Q2 parity factorization and the `k^6` small-gap law | **ACCEPT** |
| Q3 one-sided `\|v\|^{-6}` exponential penalty | **ACCEPT** |
| Q4 reduction of the free Gaussian-jet quadrature to one theta integral | **ACCEPT** |

These accept the stated interfaces for the limiting kernel. They do not accept a finite-`r` interchange, a numerical enclosure, a persistence-pair moment, or a global lifetime law.

## Q1 — ACCEPT

The open type interval (1.3) is exactly the set where `P_M>0` and `P_S>0`. Indeed `√θ+√(1-θ)≥1`, so the upper edge `1-2√(1-θ)` is at most the `P_M` upper edge `-1+2√θ`, and the right branch `w>1+2√(1-θ)` misses the open `P_M` interval. Reversing the inequalities gives the note's union

`-3<w<-1`, `(w+1)^2/4<θ<1`, and `-1<w<1`, `1-(w-1)^2/4<θ<1`.

The theta lengths integrate to `4/3` and `2/3`, so the region has area `2`.

On that region `P_X=(w+1-2θ)^2+4θ(1-θ)>0`. The three Hessian determinants, recomputed from (B3) after substituting (1.1), are exactly `(9k^2/v^2)P_M`, `-(9k^2/v^2)P_S`, and `-(9k^2/v^2)P_X`. The typed absolute product is therefore `(9k^2/|v|^2)^3 P`. The coefficient of `w^6` in `P` is `-1`, so the degree is exactly 6, while `P>0` throughout the open region.

Both integrations give the same value. The reversed order splits as

`77248/945 + 704/135 = 27392/315`.

The original-order beta evaluation has vanishing coefficient of `π` and the same rational value. At the interior sample `u=2`, `v=1`, `k=1`, `θ=1/2`, `w=-1`, the matrices give determinants `18`, `-18`, `-18`, matching `(9)(2,2,2)` with the sign pattern above.

## Q2 — ACCEPT

Even-total-order and odd-total-order derivatives at one point are uncorrelated because `K(h)=K(-h)` makes every odd derivative of `K` vanish at the origin. Joint normality separates the blocks in every frame. The pins split in the same way: `(f,f_xx,f_xz)=(b,0,0)` is even and `(f_x,f_xxx,f_z)=(0,12k,0)` is odd, while `a=f_zz` is even and `(q,c,d)` is odd. Conditioning on `U_0` therefore leaves `a` independent of `T=(q,c,d)`, with the law of `a` free of `k` and with `T~N(k m(E), Ω(E))`.

The solved jets are homogeneous of degree one in `k`, so `(q,c,d)=k j(u,v,w,θ)`. The conditional density at the unscaled point `a=0` is `p_a(0) C_odd exp(-k^2 Q_E/2)`.

The passage from PR25 (C5) to (1.4) is the product of three contributions: `24k/|v|^6` from the contact Jacobian and height factor, `6k/|v|` from `dq/dw`, and `729 k^6/|v|^6` from the three determinants. The numerator `24·6·9^3=104976` and the endpoint relation `z_0=36k^2 m_{2a}` cancel to `2916 k^6/(m_{2a}|v|^{13})`. That is (4.2).

For each fixed `(u,v)` with `v≠0`, `w` stays in `(-3,1)` and `Q_E` is bounded on the type domain. The integrand increases to `P` as `k↓0`, and `0≤exp(-k^2 Q_E/2)≤1`. The integral tends to `J=27392/315`, and

`2916 J = 8875008/35`.

Hence `Λ_1 ∼ C_L(b,E) k^6/|v|^{13}` with the displayed positive factor `C_L=(8875008/35) p_a(0) C_odd/m_{2a}`, independent of `(u,v)`. Positivity uses `m_{2a}>0` and `det Ω>0`, which is the nondegeneracy hypothesis of the input model.

On bounded `u` and `0<|v|≤1`, each component of `j` is `O(|v|^{-3})`, so `Q_E≤C_B|v|^{-6}`. Because `P≥0`,

`exp[-C_B k^2/|v|^6] ≤ Λ_1/(C_L k^6|v|^{-13}) ≤ 1`.

The ratio tends to `1` uniformly when `k^2/|v|^6→0`. For each fixed `k>0` the axis bound of Section 2 sends `Λ_1` to `0`. Those are different operations. This is a law for the already-defined limiting kernel.

For the unperiodized covariance `exp(-|h|^2/2)`, exact regression gives `a~N(-b,2)` and `(q,c,d)~N(0,diag(2,2,6))` after the pins, including a zero regression coefficient on `f_xxx=12k`. Then `p_a(0)C_odd=exp(-b^2/4)/(16√3 π^2)`. At `b=0`, `m_{2a}=1` and `C_L=184896√3/(35π^2)`, which equals `927.086705814` to the printed places. That diagnostic is not a finite-`L` substitute.

## Q3 — ACCEPT

Expanding `-2(u-1/2)^3+3(u^2-1/4)(w-1)-2(1-θ)` recovers (1.1) identically. For `u>1/2` on the open type region, `w<1` and `θ<1`, so the last two terms are nonpositive and the first is strictly negative. Therefore

`|R|≥2(u-1/2)^3`, `|d|≥12k(u-1/2)^3/|v|^3`.

Let `δ=12(u-1/2)^3/|v|^3` and let `λ` be the smallest eigenvalue of `Ω^{-1}`. Then `Q_E≥λ(|j_d|-|m_d|)^2`. The elementary bound `(|j_d|-|m_d|)^2≥δ^2/2-2|m_d|^2` and `δ^2=144(u-1/2)^6/|v|^6` give

`Q_E≥72λ(u-1/2)^6/|v|^6 - C_m`.

Half of that quadratic form produces the exponent coefficient `36λ`. For `k≤k_{max}` the additive `exp(C k^2)` is absorbed into the prefactor. On `u≥A_1>1` this is (3.2): the integrand carries `exp[-c k^2(u-1/2)^6/|v|^6]`. The constants may depend on the fixed model, the annulus, the birth compact, and `k_{max}`.

The same bound does not extend to `u<-1`. At `u=-2`, `θ=1/2`, `w=-76/45` one has `R=0`, while `w` lies strictly inside `I_{1/2}` and

`P=255214387799/8303765625>0`.

Thus `d=0` at a positive integrand point. The joint `(q,c)` bound remains: the identity `uvq+(v^2/2)c=-6k(u^2-1/4)` is exact, and Cauchy–Schwarz gives (2.2) whenever `|u|>1/2`.

## Q4 — ACCEPT

For fixed `θ`, `j=l w+h` with `l=(6/v, -12u/v^2, 18(u^2-1/4)/v^3)`. The first component is nonzero, and `Ω^{-1}` is positive definite, so `A=l^T Ω^{-1} l>0`. Completing the square writes `Q_E=A(w-μ)^2+D` with `D≥0`. The weight `exp(-k^2 Q_E/2)` factors into `exp(-k^2 D/2)` and `exp(-a(w-μ)^2)`, `a=k^2 A/2`.

`P` has degree 6 in `w`, so its translate about `μ` has seven coefficients. Their integrals are the truncated moments `M_0,…,M_6`. The base cases

`M_0=√π/(2√a)[erf(√a U)-erf(√a L)]`, `M_1=[exp(-a L^2)-exp(-a U^2)]/(2a)`

are the Gaussian integral and its first antiderivative. For `n≥2`, integration by parts with `d/dx exp(-a x^2)=-2a x exp(-a x^2)` is exactly the recurrence (5.1). The `(θ,w)` integral therefore collapses to one integral in `θ`. On `φ∈(0,π/2)`, `θ=sin^2 φ` replaces the endpoints by `-1-2sin φ` and `1-2cos φ`.

A floating-point Simpson comparison on one moderate interval agrees with `M_4` to `10^{-10}`. That comparison is not an enclosure. Extreme tails and short intervals can lose precision, and the note claims no numerical continuum certificate.

## Boundaries

Finite-`r` uniformity, the full persistence intensity, and a global lifetime law are outside this review. Section 4 of the note already withholds the interchange of `k↓0` with `r↓0`, and (4.6) already withholds the small-mark moment of the full persistence-pair intensity. Those sentences were not given a separate disposition.
