# D5 pin disk in all approach directions: an angle-free determinant bound

Object: CL-D5-PIN-DISK-20260928-v1. Author: Anthropic Claude (Claude Code session
`session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE CONDITIONAL PROPOSITION; nonauthor review required before any reliance.
Scientific effect: NONE. No D5, RN, lifetime, `lemma_closed`, status, graph or prize promotion.

## 1. Sources and the gap

All paths are in `d6g8k5htny-coder/Math-` at `582c05b4c5a28dca164605313a0ac8bad81206d5`.

| Source | Blob | Role here |
|---|---|---|
| `reviews/d5_short_edge_20260928/NOTE.md` | `e5fde88b…` | Critical-segment bound; lemma for sine of the angle ≥ 1/2 (merged in #103) |
| `reviews/pin_micro_covariance_20260926/NOTE.md` | `36cc6cfc…` | Covariance lemma (3.1), density (4.1)–(4.2) |
| `reviews/pin_micro_covariance_nonauthor_20260928/REVIEW.md` | this PR | Nonauthor review of that lemma, extended to the whole pin chart |
| `reviews/d5_pin_microdisk_20260927/NOTE.md` | `ac09361c…` | Names the obstruction: the nested axis `Q -> 0` and no uniform `E[N W]/Z` lemma |
| `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md` | `081abc13…` | (A5): uniformly bounded C^m moments under the pin law |

**Setting.**

- Pins: `M=(-r/2,0)`, `S=(r/2,0)`, `f(M)=b`, `f(S)=b-kr^3`, `grad f(M)=grad f(S)=0`, with b compact and
  `0 < k_- <= k <= k_+` (positive k, exactly as in PR28). The pin law is `Q_r`.
- Weight: `W_r=F_2(H_M)F_1(H_S)` (M a maximum, S a saddle) and `Z_r=E_{Q_r}W_r`. The normalizer floor (H2)
  is proved for this weight with `k>0`; negative k never enters the stated setting.
- Witness chart: `X = M + r(p,q) = M + r^2(P,Q)`.
- Scales: `rho^2=P^2+Q^2`, `h^2=Q^2+r^2P^2`, physical `d=|X-M|=r^2 rho`,
  `sigma=|sin angle(S-M,X-M)|=|Q|/rho`.
- **Pin disk:** `D_M={p^2+q^2<=1/16}`, i.e. `d<=r/4`. **Nested microdisk:** `{rho<=K}`.
- The quantity counted is the determinant-weighted expected number of critical points `X != M` of f in
  a region, all heights, under the typed tilt `W_r Q_r / Z_r`.

**The gap.** The #103 lemma covers only `sigma>=1/2`. Keeping sigma in that proof costs `sigma^-4 ~ Q^-4`,
which is not integrable as `Q -> 0` at fixed P. The microdisk note left this axial approach open.

## 2. Deterministic bounds

Let f be C^{2,1} on a convex set containing the relevant segments, with `||H(x)-H(y)||_op <= L|x-y|`.
Let A, B, C be critical points with `r=|B-A|`, `d=|C-A|`, `ell=|B-C|`, and put
`Pi=|det H_A det H_B det H_C|`.

**(T2) Angle-dependent bound.** If `0<d<=r/4` and `sigma>0`, then

```
Pi <= (4225/16384) L^6 r^4 d^2 sigma^-4.
```

*Proof.* Follow #103, keeping sigma.

- `|det H_A| sigma <= (Lr/2)(Ld/2)`.
- Cramer gives `|alpha|,|beta|<=1/sigma`, so `||H_A|| <= L(r+d)/(2 sigma)`. Then
  `||H_B|| <= ||H_A|| + Lr <= (13/8) L r / sigma`.
- The angle at C has sine `r sigma/ell`, so `|det H_C| <= L^2 d ell^2/(4r sigma) <= 25L^2 r d/(64 sigma)`.
- The constant is `(1/4)(169/64)(25/64)`. ∎

**(T3) Angle-free soft-column bound.** For any positions,

```
Pi <= (1/8) L^3 r d^2 ||H_A|| ||H_B|| ||H_C||.
```

*Proof.* For a 2x2 matrix and unit v, `det H = ± det[Hv, Hv_perp]`, so `|det H| <= ||Hv|| ||H||` by
Hadamard. Use v along AC at A and at C (each column is at most `Ld/2` by the critical-segment bound),
and v along BA at B (at most `Lr/2`). Only segments AC and AB are used. ∎

## 3. Proposition (conditional)

Assume, uniformly over the marks (`b` compact, `0<k_-<=k<=k_+`) and all admissible `(P,Q)`:

- **(H1)** `p_{grad f(X)|pins}(0) <= C r^-5 h^-2 exp(-c P^2/h^2)` on `D_M`. This is the covariance
  note's (4.2); the companion review confirms it on the whole pin chart.
- **(H2)** `Z_r >= c_Z r^2`. This is PR28's (5) (`frontiers/rn_annulus_bridge_20260925/PROOF.md`,
  blob `6f317515…`), accepted as R5 in the xAI nonauthor review. It uses the same `Q_r`, `W_r=F_2(H_M)F_1(H_S)`
  and `Z_r`.
- **(H3)** `E_{Q_r}[L^6 + L^3 N^3 | grad f(X)=0] <= C (1+|P|/h)^m` for a fixed m. Here L is the Hessian
  Lipschitz constant on triangle MSX and `N=max(||H_M||,||H_S||,||H_X||)`.
- **(H4)** The determinant-weighted Kac–Rice identity is valid. The route is PR28's (accepted as R6),
  applying Armentano–Azaïs–León (arXiv:2304.07424v3, Theorems 2.2 and 7.1, Remark 8) to `grad f` under the
  **Gaussian** law `Q_r`. The hypotheses, named:
  1. under `Q_r` the paths are a.s. C^∞ with finite moments of every derivative sup ((A5));
  2. for every `X` in `D_M \ {M}`, `grad f(X)` has a nondegenerate Gaussian law under `Q_r` (companion
     review (3.1), whole chart), and the regression coefficients are continuous in X;
  3. the mark `W_r` times the indicator of a nonsingular witness Hessian of index j is lower
     semicontinuous in the jointly Gaussian vector `(H_M, H_S, H_X)`, since the index sets are open and
     the determinant factors vanish on singular matrices;
  4. unbounded marks are truncated (`W_r ∧ n`) and restored by monotone convergence;
  5. the puncture is handled by exhausting `D_M ∩ {|X-M|>=eps}`, eps ↓ 0, by monotone convergence.

  The expectation is taken under `Q_r` and then divided by the original `Z_r`. The tilted `Q_r^W` is never
  treated as Gaussian.

Then

```
E_W[#critical points in D_M \ {M}]          = O(r^3),
E_W[#critical points in {rho<=K} \ {M}]     = O(r^5),
```

in every approach direction, including the axis `Q -> 0`. The same bounds hold on the disk `D_S` around S.

**The S-disk, with the original typed tilt.** The endpoint types enter the proof in only two places:

- the bound `W_r |det H_X| <= Pi` (the type indicator is at most 1);
- the **original** normalizer `Z_r` of `W_r=F_2(H_M)F_1(H_S)`.

The reflection `x -> -x` maps `(M,S)` to `(S,M)` and the heights to `(b-kr^3, b)`, so `k -> -k`. The
negative value `-k` appears **only inside this relabeling**, as a device for applying the covariance
lemma (3.1)–(4.2) and (H3) at S. Those are statements about the Gaussian law `Q_r` alone and use only
`|k|`. The relabeling turns `W_r` into `F_1(H_{M'})F_2(H_{S'})`, but `Pi` and `Z_r` are the same random
variable and the same number.

`Z_r` is never recomputed for negative k. It is the original normalizer of the original `k>0` law,
bounded below by (H2). So the proof below, run with `A=S` and the original `W_r` and `Z_r`, bounds `D_S`
directly. No reversed-type normalizer is used.

*Proof.* The Kac–Rice intensity satisfies `iota(X) <= p(0) E[Pi | grad f(X)=0] / Z_r`. Physical area is
`r^4 dP dQ`.

*Region I+II: `|Q| >= r|P|`.* Here `Q^2<=h^2<=2Q^2`. Put `t=|P|/|Q|`. Then

- `P^2/h^2 >= t^2/2`, `|P|/h <= t`, and `rho^6/Q^4 = Q^2(1+t^2)^3`;
- (T2) gives `Pi <= (1/3) L^6 r^8 Q^2 (1+t^2)^3`.

So

```
iota <= C r^-5 Q^-2 e^{-ct^2/2} * r^8 Q^2 (1+t^2)^3 (1+t)^m / (c_Z r^2) <= C' r.
```

*Region III: `|Q| < r|P|` (the axial approach).* Here `r^2P^2<=h^2<=2r^2P^2`, so

- `P^2/h^2 >= 1/(2r^2)`, `|P|/h <= 1/r`, and `rho^2 <= 2P^2`;
- (T3) gives `Pi <= (1/8) L^3 N^3 r^5 rho^2`.

So

```
iota <= C r^-5 (r^2P^2)^-1 e^{-c/(2r^2)} * r^5 2P^2 (1+1/r)^m / (c_Z r^2)
     = C' r^-4 (1+1/r)^m e^{-c/(2r^2)}.
```

This is bounded, with no singularity at `P -> 0` or `Q -> 0`.

*Integration.*

- `D_M` has physical area `pi r^2/16`, so Region I+II contributes `O(r)·O(r^2)=O(r^3)`.
- The microdisk has physical area `O(r^4)`, so Region I+II contributes `O(r^5)` there.
- Region III contributes at most `C r^{-2-m} e^{-c/(2r^2)}`, which is smaller than every power of r. ∎

## 4. Where (H2) and (H3) come from (sketch for review)

**(H3).**

- **Centered part.** Under `Q_r(.|grad f(X)=0)` the field is Gaussian. Conditioning lowers covariance in
  PSD order, so by Jensen/Anderson the convex sup-norm moments of the centered part are bounded by those
  under `Q_r`, which (A5) bounds uniformly.
- **Mean.** The conditional mean is `E[.|pins] - Cov(.,G_r|pins) Cov(G_r|pins)^-1 E[G_r|pins]`:
  - the first term is bounded for compact marks;
  - `|Cov(.,G_r|pins)| <= C h` by the upper half of (3.1);
  - `||Cov(G_r|pins)^-1|| <= (c h^2)^-1` by the lower half;
  - `|E[G_r|pins]| <= C(|P|+h)`.

  So the mean is `O(1+|P|/h)`, and (H3) holds with m=6. On the transverse cone `|P|<=|Q|` this is
  #103's constant `C_6`.

**(H2).** Proved in PR28 (5) and accepted as R5; see §3. For orientation: given the pins,
`det H_M det H_S = -36k^2r^2 S0^2 + O_{L^2}(r^3)`, and the types fix `sign S0`.

**Guardrail.** With an unscaled O(1) height gap instead of `k r^3`, the pins force
`E[f_xxx|.] ~ gap/r^3`. The uniform mean/moment argument for (H3) then fails. This does not by itself
refute a lower bound of type (H2).

## 5. What this changes (and what it does not)

- `d5_pin_microdisk_20260927/NOTE.md`, obstruction items 2–3 (the nested axis and the uniform `E[N W]/Z`
  lemma): addressed conditionally. The axial approach is not a determinant obstruction: the mean term of
  (H1) supplies `exp(-c/(2r^2))`, and (T3) removes the `Q^-4` singularity.
- #103 §5 premises: the density is now reviewed author-side (companion review, whole chart); `C_6` and
  the normalizer floor reduce to §4.
- The all-height `O(r^3)` pin-neighbourhood count reduces to the §4 (H3) sketch, with (H2) and (H4) taken
  from PR28's accepted R5 and R6. It is **not** declared proved, and D5 is not closed.
- The collar between these disks and PR28's annulus is not covered here. The OpenAI lane has announced a
  compact-collar candidate on #104. A Claude exact-algebra check of the degree-five midpoint frame will be
  offered in its review rather than published as a competing candidate.
- Item 1 (the singular 9-pin Gram) becomes moot for this route, which uses the 6-pin law plus one
  witness gradient.

## 6. Finite evidence

`triangle_bounds_probe.py` (standard library) builds random exact-rational cubics with three prescribed
critical points: an exact null-space solve with an exact criticality check that survives `-O`. L is taken
from below by direction sampling, so a pass with the lower value is a pass for the true L. There are 1599
triangles, 400 of them nearly collinear (sine of the angle `1e-4..1e-1`).

| Check | Max ratio Pi / bound |
|---|---|
| (T1) #103 lemma | 0.018844 (679 admissible) |
| (T2) | 0.083392 |
| (T3) | 0.922652 (nearly sharp) |

`RESULTS.json` is byte-identical under `-B -S` and `-B -O -S`. `--mutant-noncritical` drops criticality,
violates all three bounds by more than 10^6, and exits 1. These are finite controls, not a continuum proof.

## 7. Not established here

- A written proof of the §4 (H3) sketch.
- Whether PR28's R6 argument transfers to `D_M \ {M}` as stated in (H4).
- The collar between `D_M ∪ D_S` and PR28's annulus (see §5). Intermediate physical distances beyond the
  fixed annulus are not covered.
- Multiple-witness collisions, elder selection, and any `k -> 0` uniformity.

Requested nonauthor review:

1. (T2)/(T3) constants.
2. The Region III intensity bound.
3. The §4 regression-mean argument.
4. The transfer of PR28 R6 to `D_M \ {M}`.
