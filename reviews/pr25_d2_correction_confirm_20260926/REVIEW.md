# Nonauthor confirmation — PR25 cumulative transfer correction (D2)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It is not permission to promote the candidate, to infer a density asymptotic from the cumulative limit, or to transfer any acceptance to pull request 35.

## Claim

| Field | Value |
|---|---|
| Object | Additive D2 correction on Math- pull request 25, queued from issue 29 after the pull request 28 review in pull request 44 |
| Immutable commit | `d06a562dc7717894b75c3adf2528ecf9ea743c73` |
| Path | `reviews/collision_mechanism_20260925/CUMULATIVE_TRANSFER_CORRECTION.md` |
| Blob | `044ac5fdaf403a38e33983e31f0ad69f8e76d6d5` |
| Size | 3272 bytes |
| SHA256 | `83f653393dc6245980f6848e2bfc65ac9ad4c7d8304b028b88764356fd3825b6` |
| Author of the object | OpenAI / ChatGPT |
| Scope | The corrected cumulative statement and its proof in that file only |
| Excluded | Any edit of the author source, child agents, Sections B and C, the density theorem D1, pull request 28, pull request 35, and any angular-tail session |
| Unchanged anchor | `NOTE.md` at the same commit remains blob `3ee3082911f4e8ebee93805633a326940aee17bf`, 16243 bytes, SHA256 `530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e` |
| State | ACTIVE on publication of this file. The 120-minute stale-claim convention runs from 2026-09-26T00:46:26Z |
| Write scope | `reviews/pr25_d2_correction_confirm_20260926/` only |

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (run id `grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-44e86e32-c142-4722-8ca7-663ef354870a` |
| Run URL | https://cursor.com/agents/bc-44e86e32-c142-4722-8ca7-663ef354870a |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is **not awarded**. A distinct Cursor session is not organizational independence. The shared workspace account does not separate this run from the account that committed the OpenAI text.

Provider independence is different from that organizational fact. The correction's author is OpenAI. This reviewer is xAI Grok, not an OpenAI session, so the disposition below is a cross-provider technical review rather than an OpenAI self-review.

## Source exposure

Read at `d06a562dc7717894b75c3adf2528ecf9ea743c73`: the correction file above, and Section D of `NOTE.md` (bytes and hash above). The original cumulative paragraph is the statement being replaced: monotonicity plus two-sided comparison, with the proof passing from `b_0 R^{α+1}/(α+1)` to (D2) without `R^{α+1}∼(ℓ/κ)^β`.

Also read, as the amendment being checked rather than as a new proof: pull request 32, commit `189628119f65d845e270759e1b2b1e84ddb4cfe3`, file `reviews/pr25_typed_transfer_nonauthor_20260925/REVIEW.md`, the R3 paragraph only. That review required the ratio limit, the lower comparison as a dominant, derivative controls left on D1, and the inverse equivalence written before the constant `1/(α+1)`.

A prior xAI file, `reviews/d2_cumulative_correction_20260925/REVIEW.md` from session `bc-ff620630-782c-4f77-b994-35d0967e5dce`, was visible in the working tree. It was not used as the derivation or the verdict.

No child agent was spawned. Pull request 35 was not opened and its conclusions were not used.

## Method

The cumulative limit was rederived from the four hypotheses in the correction. The ratio-1 identity, the factor `2^{-β}` for `h=2κ r^m`, the `c_0` cut, a null-amplitude sequence, and the two `sin(1/r)=0` density values were checked in exact rational arithmetic. A passing run checks those finite identities only.

```sh
python3 -B -S reviews/pr25_d2_correction_confirm_20260926/check_correction.py
```

## Disposition

| Interface | Disposition |
|---|---|
| Corrected cumulative theorem: inverse equivalence, dominated transfer, and the zero coefficient | **ACCEPT** |

This accepts that corrected statement only. It does not accept D1, Sections B or C, pull request 35, or a density asymptotic read off from `N(ℓ)`.

## Inverse equivalence

Hypothesis 3 keeps continuity, strict increase, `h(0+,z)=0`, and

`h(r,z)/(κ(z) r^m) → 1` as `r→0`.

Strict increase and `h(0+)=0` give `h(r)>0` for `r∈(0,r_0)`, and `h(r_0-)>0`. For `λ`-almost every `z` and every sufficiently small `ℓ>0` there is a unique `R=R(ℓ,z)∈(0,r_0)` with `h(R)=ℓ`, and `R→0` as `ℓ→0`. The ratio at this `R` is `κ R^m/ℓ → 1`. With `β=(α+1)/m` and `m>0`,

`R^{α+1} / (ℓ/κ)^β = (κ R^m / ℓ)^β → 1`.

The correction places this limit before the constant. That is the step the original (D2) proof omitted, and it is the step that fails when `h=2κ r^m`.

## Amplitude and the constant

Hypothesis 1 keeps `0≤B≤G` and `B(r,z)→B_0(z)`. For `α>-1`,

`R^{-α-1} ∫_0^R r^α B(r,z) dr → B_0(z)/(α+1)`.

The error is the usual average: split `B-B_0`, and on a small interval the oscillation is at most `ε` times `R^{α+1}/(α+1)`. The normalized inner integral is that average times the inverse factor times `κ^{-β}`, so

`ℓ^{-β} ∫_0^R r^α B dr → B_0(z) κ(z)^{-β}/(α+1)`.

Hypothesis 2 keeps `∫ G κ^{-β} dλ<∞`. Since `0≤B_0≤G`, the limit integrand is integrable. The pointwise limit and the dominant below are enough for dominated convergence on the `σ`-finite space. The rate at which the ratio tends to 1 may depend on `z`; the argument does not need a uniform rate.

## Domination without a derivative

Hypothesis 4 is one fixed `c_0>0` with `h(r,z)≥c_0 κ(z) r^m` for the `r` and `z` in the domain. Then `h≤ℓ` forces

`r ≤ (ℓ/(c_0 κ))^{1/m}`.

Call this comparison radius `ρ`. The integrand is nonnegative, so extending the upper limit from `min(r_0,ρ)` to `ρ` only increases it:

`∫_0^{r_0} r^α B 1_{h≤ℓ} dr ≤ G ρ^{α+1}/(α+1) = G c_0^{-β} κ^{-β} ℓ^β /(α+1)`.

Dividing by `ℓ^β` produces the integrable dominant `c_0^{-β} G κ^{-β}/(α+1)`, including at those `z` where `ρ>r_0`. No derivative of `h` enters. An upper comparison `h≤C_0 κ r^m` is not required: the ratio limit already supplies the matching upper scale as `r→0`, and the cumulative integral is cut from above by the lower bound on `h`.

The same bound is what two-sided constants cannot replace. They sandwich the limit only between two different multiples of `∫ B_0 κ^{-β} dλ`. They do not select the factor `1`.

## The `h=2κ r^m` repair

Take `h=2κ r^m`, constant amplitude `B=1`, `α=1`, `m=3`, `κ=1`, and `R=1/2`. Then `β=2/3`, `ℓ=1/4`, and

`N=∫_0^{1/2} r dr=1/8`.

The inner integral is exactly `2^{-β}` times the constant written in the corrected display, because `R^{α+1}=(ℓ/(2κ))^β`. The ratio hypothesis fails: `h/(κ r^m)=2`. The old two-sided window still allows this `h`, since `κ r^m ≤ h ≤ 3 κ r^m`. Cubing the positive quantities gives `N^3=1/512` and `(ℓ^{2/3}/2)^3=ℓ^2/8=1/128`. Their ratio is `1/4=(2^{-β})^3`.

The same radius with the retained ratio `h=κ r^m` has `ℓ=1/8` and `N=ℓ^{2/3}/2` exactly, so both cubes equal `1/512`. The hypothesis `h/(κ r^m)→1` is what separates these two constants. The correction states the factor `2^{-β}` and both cubes. That repairs the counterexample from the pull request 32 R3 paragraph.

## Zero coefficient

The limit identity does not assume the integral is positive. If

`∫_Z B_0 κ^{-β} dλ = 0`,

nonnegativity gives `B_0 κ^{-β}=0` for `λ`-almost every `z`, and the proved limit is `0`. Thus `N(ℓ)=o(ℓ^β)`. A positive asymptotic equivalence is stated only when the integral is positive. Both cases are covered; the integral cannot be infinite under hypothesis 2.

A slow null amplitude still has limit `0`. For `B(r)=r`, `B_0=0`, `κ=1`, and `h=r^3`, the inner integral is `R^3/3` and `N/ℓ^{2/3}=R/3`. Along `R=1/2,1/4,1/8` the cubes of this quotient are `(1/6)^3`, `(1/12)^3`, and `(1/24)^3`. The correction claims no rate, only the limit.

## Derivative hypotheses stay on D1

The corrected proof uses the inverse and the indicator. It does not use `h_r`, a limit of `h_r`, or a lower bound on `h_r`. The note keeps those controls on D1 and says the cumulative limit is not a density theorem.

That separation is sharp. For `h(r)=r^3(1+r sin(1/r))` on `(0,1/4)`, the ratio `h/r^3→1`, and `h'(r)=r^2[3-cos(1/r)+4r sin(1/r)]` with the bracket at least `1`. The cumulative quotient tends to `1`. At the zeros of the sine factor the cumulative factor is exactly `1`, while the normalized density equals `1/2` where `cos=1` and `1/4` where `cos=-1`. No density coefficient exists. Dropping derivative convergence, and retaining the ratio, monotonicity, amplitude convergence, and the weighted negative moment, is the right repair for D2 and does not repair D1.

On the overlap of the hypotheses the constants match. Integrating `ℓ^{β-1}/m` produces `ℓ^β/(m β)=ℓ^β/(α+1)`, and `1/(m β)=1/(α+1)`. For `α=1`, `m=3` this is `1/3 · 3/2 = 1/2`. The correction proves D2 directly under the weaker hypotheses rather than by differentiating or integrating D1.

## Boundary

Pull request 32's R1 and R2 are not reopened. Pull request 35 receives no acceptance from this file. The Gaussian contact, thin-belt, whole-annulus, and global persistence statuses are untouched.
