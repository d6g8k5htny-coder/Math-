# Nonauthor review — shrinking witness pairs, divided-difference m=2 bound

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It does not edit main pull request 125. It does not infer pin-neighborhood, intermediate-annulus, elder-pairing, or global RN / 24-jet closure.

## Pickup

One bounded nonauthor review of the shrinking-witness note. No child agent was launched.

## Claim

| Field | Value |
|---|---|
| Object | main pull request 125, `RN-SHRINKING-WITNESS-M2-20260926` |
| Immutable commit | `00c9d08a146c60cfc026f2167c5a1d9e5678e34d` |
| Path | `docs/rn_d5_shrinking_witness_20260926.md` |
| Blob | `d29d00f205f12ee9619651165ee588422d777fd4` |
| Size | 12367 bytes |
| SHA256 | `dc9000136ecab9a0d0269c4760b44400dca8e2f6882d136679b822f07c220333` |
| Companion test blob | `8112f93b340e75945caea442bd0ba81c6a07996a`, 5016 bytes, SHA256 `99ed5aeadc1a90e14370932cbf7c486a0e6351a1ad3f9d2072ad796dca7a6206` |
| Author of the object | Cursor Agent, co-authored with Dylan Roy, on main pull request 125 |
| Scope | Ordered index-`j` pairs inside the fixed remote region `D_ρ`, between-pin window of length `k r^3`, separation in `[η, δ_*]` with `δ_*≤ρ/4` fixed and `η` allowed to approach 0 |
| Interfaces | Divided-difference Jacobian, contact covariance floor, determinant soft factors, shared height-window cubic, separation integral, transition from the fixed-`η` bound |
| Excluded | Pin neighborhoods, the intermediate annulus, elder pairing, a sharp collision kernel, a matching lower bound, and global RN / 24-jet closure |
| State | Delivery record on publication of this file |

The assigned subject was not retargeted. `frontiers/remote_window_20260924/PROOF.md` was not edited.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-4428875b-e5ff-4f79-a1bb-a0e107ee81c6` |
| Run URL | https://cursor.com/agents/bc-4428875b-e5ff-4f79-a1bb-a0e107ee81c6 |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is not awarded. This run is a different Cursor session from the session that wrote main pull request 125. A distinct session under the same application and workspace account is not organizational independence. The authoring model of pull request 125 was not available to this run, so provider separation is not claimed.

## Source exposure

Read in full: the immutable note above, and its companion test at the same commit.

Read as the cited outer boundary, at the identity named in the note: Math- `frontiers/remote_window_20260924/PROOF.md`, commit `191ea7d541a486736ba7bbddfd4eac25a6c4567b`, 18355 bytes, SHA256 `a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7`. The digest matches the local file. This review uses the Fourier nondegeneracy paragraph in §2, the endpoint comparison (6)–(11), the one-point numerator (14), and the fixed-separation factorial moment (15)–(16). It does not reopen those acceptances and does not extend them.

Author unit tests were not used as evidence. The Bargmann–Fock sampling figures in §5 of the note were not rerun and are not inputs to the bound.

## Method

The Jacobian, the singular-value comparison, the axial and height-gap coefficients, the radial exponent, and the model residual variance were rederived from the Taylor recipe and the Hermite evaluation of `exp(-t^2/2)`. Separately, `algebra_check.py` (standard library only) locks those rational identities and the arithmetic of the height-split ledger used in the transition section below. That ledger is a comparison of majorants. It is not a theorem about the periodized field and it does not replace the note's exponent.

Command:

```sh
python3 -B -S reviews/pr125_shrinking_witness_nonauthor_20260926/algebra_check.py
```

Script SHA256: `2ffe3a18ee0ee38eca0b5e5be749f21fd5b7cecdcdad22c4212be80475c4269f`. The run printed `all certificates passed`.

## Dispositions

| Interface | Disposition |
|---|---|
| Gradient divided-difference Jacobian `δ^d` | **ACCEPT** |
| Contact covariance floor for `(G_0, G_1)` | **ACCEPT** |
| Determinant soft factors, product `O(δ^2)` | **ACCEPT** |
| Shared height-window cubic `-μ δ^3/12` | **ACCEPT** |
| Separation integral `∫ s ds` near zero | **ACCEPT** |
| Exact transition to the fixed-`η` `O(r^6)` bound | **AMEND** |

Overall disposition: **AMEND**. The expectation bound on `T_{r,j,2}(η)` stands. The printed passage from that bound to a probability for every pair of separation at least `η`, and the sentence that locates the whole second-window loss at the mere permission for `η` to shrink, need the repair in the transition section. No interface is a counterexample.

## Jacobian — ACCEPT

On `(G_0, G_1) ∈ R^d × R^d` the map

`(G_0, G_1) ↦ (∇f(x), ∇f(y)) = (G_0, G_0 + δ G_1)`

has block matrix `[[I, 0], [I, δ I]]`. Its determinant is `δ^d` for every `d≥1` and every `δ≠0`. The recursive expansion agrees with `δ^d` on dimensions 2, 3, and 4. Because the map is linear and sends the origin to the origin,

`p_{∇f(x),∇f(y)}(0,0) = δ^{-d} p_{G_0,G_1}(0,0)`

exactly, wherever the law of `(G_0, G_1)` is nondegenerate. The factor is the change-of-variable determinant of the gradient coordinates. It is not an extra spatial Jacobian.

## Contact covariance floor — ACCEPT

`G_1 - H_x u = O(δ)` in every fixed `L^p`, uniformly for `x∈D_ρ` and `|u|=1`, by Taylor expansion with the Lagrange remainder. The contact vector is `(∇f(x), H_x u)`. The `d` gradient functionals and the `d` forms `H ↦ H u` are linearly independent: the second family is surjective on symmetric matrices for every unit `u`. Together with the pin jet `U_0` at distance at least `ρ/2`, these are distinct derivative-evaluation functionals. The Fourier argument in §2 of the outer-boundary note gives a positive-definite joint covariance. That covariance is continuous in `(x, u)` on the compact set `D_ρ × S^{d-1}`, and the conditional covariance of `(∇f(x), H_x u)` given `U_0` is the Schur complement of a positive-definite matrix, hence positive definite at each point. Compactness supplies a positive lower bound. For small `δ_*` and small `r`, the passage from `(U_0, ∇f, H u)` to `(U_r, G_0, G_1)` is a small covariance perturbation, so the conditional covariance of `(G_0, G_1)` given the endpoint pins stays uniformly positive definite.

The symbol `c_*/2` in the note is existence bookkeeping for that perturbed conditional gap. The gap that has room to be halved is the contact conditional gap. A Gaussian on `R^{2d}` whose covariance eigenvalues are at least that gap has density at the origin at most `(2π)^{-d}(det Σ)^{-1/2}`, and a nonzero conditional mean only decreases the density at `0`. Therefore

`p_{∇f(x),∇f(y)|U_r}(0,0) ≤ C δ^{-d}`,

with `C` depending on `d, L, ρ, δ_*, B, K` and independent of `δ` and `η`.

Adjoining `f(x)` keeps the same conclusion. The value is an order-zero functional, independent of the gradient and of `H u` as a jet. The enlarged observation `(U_r, G_0, G_1, f(x))` remains uniformly nondegenerate for small `δ` and `r`, so conditioning on a height in a fixed compact interval does not remove the divided-difference gap. On the Bargmann–Fock covariance `exp(-|z|^2/2)`, the model calculation is the integer identity `15 - 9 = 6`: the third axial derivative has variance 15, covariance `-3` with the first derivative, and zero covariance with `H u`. That model variance is an illustration. The periodized floor uses the jet argument above.

## Determinant soft factors — ACCEPT

For a symmetric matrix and a unit vector, `σ_min(H) ≤ ||H u||` and `σ_max(H) ≤ ||H||_F`, so

`|det H| ≤ ||H u|| ||H||_F^{d-1}`.

The square comparison holds on the three `2×2` samples in the note and on three further `3×3` samples with `u = e_1`.

Under `G_1 = 0`, the vector Taylor expansion gives

`H_x u = -(δ/2) ∇_u(H_x) u + O(δ^2)`.

The same expansion from `y` in the direction `-u` gives `||H_y u|| = O(δ)`. The third- and fourth-derivative factors stay bounded in every fixed `L^p` under the conditional law: the observation covariance is uniformly positive definite, the targets `(v_r, 0, 0, t)` stay bounded on the compact mark set, and Gaussian regression does not increase variances of fixed jets. Hölder therefore lifts the two vector bounds to

`E[ |det H_x|^p |det H_y|^p | U_r, ∇f(x)=∇f(y)=0, f(x)=t ]^{1/p} ≤ C_p δ^2`.

The endpoint identities `α_M = -6k + O(r M_4)` and `α_S = 6k + O(r M_4)` are consequences of the pins. Their fourth-derivative moments remain uniform under the added divided-difference and height conditioning by the same regression bound. The filtered-determinant comparison (8)–(10) of the outer boundary, applied to those uniform moments, gives `E[(W_r/r^2)^p | …] ≤ C_p`. One further Hölder step, using `F_j ≤ |det|`, gives

`E[ W_r F_j(H_x) F_j(H_y) | U_r, ∇f(x)=∇f(y)=0, f(x)=t ] ≤ C r^2 δ^2`.

`Z_r` remains the endpoint-only normalizer. Its accepted limit `Z_r/r^2 = z_0 + O(r)` with `inf z_0 > 0` is an endpoint statement, so for small `r` one has `Z_r ≥ c r^2` in the denominator of the pair formula. Remote pair conditioning changes the law of the numerator weight, which is the conditional expectation already estimated, and leaves that denominator in place.

The resulting Kac–Rice integrand, after one height disintegration of length `k r^3` and deletion of the second height indicator, is at most `C k r^3 δ^{2-d}`.

## Shared height-window cubic — ACCEPT

Let `φ(s) = f(x + s u)` and let `h = φ'`. Impose `h(0) = h(δ) = 0` on a degree-four axial derivative with `h''(0) = μ`, `h'''(0) = ν`, and `h''''(0) = ρ`. Solving for `h'(0)` and integrating produces the exact gap

`φ(δ) - φ(0) = -μ δ^3/12 - ν δ^4/24 - ρ δ^5/80`.

The same solve gives `h'(0) = -(δ/2) μ + O(δ^2)` and `h'(δ) = +(δ/2) μ + O(δ^2)`. A pure third derivative forces those axial curvatures to have opposite signs. The degree-four window `μ = -3δ`, `ν = 6` puts both scaled curvatures at `+1/2`; the same fourth derivative with `μ = 0` returns opposite signs. Both evaluations agree with the rational certificates.

Full vanishing of `∇f(x)` and `∇f(y)` implies vanishing of the axial derivatives, so the cubic applies on the critical-point set. For small `δ`, `||H u|| = O(δ)` in the whole ambient space, and the transverse block sees an axial Schur complement whose leading term is the axial curvature. When `μ` stays away from zero and the transverse Hessian stays a definite distance from the singular set, the indices differ by one. Same-index pairs require a further jet. The upper bound uses `F_j ≤ |det|` and does not need that jet.

The conditional size of the gap is of order `δ^3` when the third derivative stays of order one. In the Bargmann–Fock model the contact standard deviation is exactly `√6 / 12`, whose square is `1/24`. The note's printed diagnostic `0.204 δ^3` is the three-digit truncation of that coefficient: `(51/250)^2 = 1/24 - 19/375000`. This matches the illustration in §5. It is not an input to the pinned bound.

## Separation integral — ACCEPT

The radial calculation is an identity for every `d≥2`:

`∫_{η≤|h|≤δ_*} |h|^{2-d} dh = |S^{d-1}| ∫_η^{δ_*} s ds = |S^{d-1}| (δ_*^2 - η^2)/2`.

The exponent `(2-d)+(d-1)` equals 1. The integral increases to `|S^{d-1}| δ_*^2/2` as `η↓0` and remains finite. On the torus, `δ_* ≤ ρ/4 < L/16` keeps the ball inside an injectivity chart, so the Euclidean polar coordinate is the torus coordinate. Pairs that would leave `D_ρ` are a subset of this ball, and the ball integral remains an upper bound. Integrating the center over `D_ρ` contributes a constant multiple of `|D_ρ|`.

Combined with the integrand `C k r^3 δ^{2-d}` and with `Z_r ≥ c r^2`, this yields the expectation bound as stated for the count whose separation lies in `[η, δ_*]`:

`E_{Q_r^W}[T_{r,j,2}(η)] ≤ C k r^3`,

with `C` independent of `η∈(0, δ_*]`. The same majorant bounds the improper integral over `0<|x-y|≤δ_*`. The unnormalized numerator is `O(k r^5)`, the same power as the one-point numerator (14), because one endpoint product `W_r` and one window of length `k r^3` remain, and division by `Z_r` has not yet been taken.

## Transition to fixed-η `O(r^6)` — AMEND

Two repairs belong in §3 and §5. After them, the expectation bound above is unchanged.

**Probability quantifiers.** `T_{r,j,2}(η)` counts ordered pairs whose separation lies in `[η, δ_*]`. Markov's inequality gives

`P(an unordered index-j pair in the window, with separation in [η, δ_*]) ≤ E[T_{r,j,2}(η)] / 2`.

The printed event, "separation at least `η`", also contains pairs with separation greater than `δ_*`. Those pairs are estimated by (15) at the fixed separation `δ_*`, so their ordered expectation is `O((k r^3)^2)`. The repaired probability is

`P(separation at least η) ≤ E[T_{r,j,2}(η)]/2 + O((k r^3)^2)`.

On the compact mark set, `(k r^3)^2 / (k r^3) = k r^3` tends to 0 with `r`, uniformly for `k∈[k_-, k_+]`. For small `r_*` the second summand is absorbed, and the probability is at most `C k r^3`. The absorption uses the fixed-separation theorem at separation `δ_*`. It does not extend (15) down to `η=0`.

**Where the second window is lost.** A second factor `k r^3` remains available for every pair whose separation is bounded below by a positive constant independent of `r`. On that set `f(y)-f(x)` has conditional size of order one, and (15) supplies `O((k r^3)^2)`. The cubic gap `-μ δ^3/12` becomes smaller than the window when `δ = O((k r^3)^{1/3})`. That is the scale at which the second height stops producing an independent factor `r^3`. Letting the lower cutoff `η` tend to zero does not move the pairs with `δ` of order `δ_*` onto that scale.

The identity `∫_η^{δ_*} s ds → δ_*^2/2` is the integral of the majorant after the second height indicator has been deleted. Its positive limit is the reason that deleted-indicator estimate is `O(k r^3)` rather than `O(r^6)`. The mass of that integral sits at separations of order `δ_*`, where the deleted indicator is small and (15) restores a second window. The sentence in §5 that reads this positive limit as the reason a fixed-`η` order `O(r^6)` fails therefore describes the majorant, not the location of the transition.

A ledger that keeps the second height factor where `δ^3` exceeds the window, and uses the gap density bound coming from a third derivative of order one, integrates a radial piece of order `w^{5/3}` with `w = k r^3`. That arithmetic is certified in `algebra_check.py`. It is a comparison of majorants under those extra modeling assumptions. This review does not promote it to a proved exponent, and the note already leaves a matching lower bound open.

The fixed-`η` statement (15)–(16) remains the outer boundary for separations bounded below independently of `r`. Its probability `O(r^6)` is the bound in that regime. The divided-difference argument adds a uniform majorant `O(k r^3)` down to separation zero inside `D_ρ`. Uniformity is the gain. Sharpness is not claimed.

## What this review leaves open

The following stay outside the amended statement:

- the mesoscopic neighborhood of the pins and any witness within `O(r)` of `M` or `S`;
- the intermediate annulus, including `r ≪ |x| ≪ ρ`;
- remote critical points with no shrinking height window;
- legacy all-cell, 24-jet, and fixed-`r` inner-wedge selectors;
- a matching lower bound, a numerical constant, and a Poisson or factorial-moment limit for separations tending to zero;
- elder selection and any global RN closure.

Issue 76 being closed records the fixed-`ρ` / fixed-`η` review. That closure is not a closure of the six items above.
