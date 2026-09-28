# D5 short-edge determinant bound and endpoint-coordinate correction

Object: OA-D5-SHORT-EDGE-20260928-v1. Author: OpenAI / ChatGPT.
Disposition: AUTHOR-SIDE PROOF AND SOURCE REVIEW; nonauthor review requested.
Scientific effect: NONE. No D5, RN, lifetime, status, graph, or prize promotion.

This is a bounded response to Math- issue #58. Its administrative closed state is not a mathematical certificate. The historical Cursor assignments in that issue are not reactivated. No frozen source is changed.

## 1. Exact sources and the gap being addressed

All four source paths below are in `d6g8k5htny-coder/Math-` at commit
`78d36001cfdd7dcb636ba927e973a2fd731527c2`:

| Source | Git blob | Role here |
|---|---|---|
| `reviews/d5_pin_microdisk_20260927/NOTE.md` | `ac09361caac76d07f878c51ebddf6d2bea3f565f` | Finite cubic witness equations and explicit unresolved nested-axis moment |
| `reviews/pin_micro_covariance_20260926/NOTE.md` | `36cc6cfcc0ab776bc22e5f1f480d4d264b1294a6` | Author-side covariance/density proposal; not accepted as a premise without review |
| `reviews/d5_pin_neighborhood_20260926/REVIEW.md` | `11a6b8d0d9a3b57f3c391975a524bf6bdabd3b8e` | Inner-disk AMEND and geometric collar gap |
| `imports/transverse_contact_library_20260927/GEOMETRY_AND_CUBIC_INDEX.md` | `58fbeb8f5180104361938253203b9dfb576af2d9` | Existing Taylor/simplex mechanism, including its scaled-shape limitation |

The new specialization retains two powers of the short edge as a third critical point approaches one endpoint at an angle bounded away from zero. It does not apply the fixed-shape simplex estimate with a collapsing smallest singular value. No global novelty claim is made: Taylor interpolation and critical-point determinant suppression are established methods.

## 2. A coordinate correction in the finite cubic note

Use physical coordinates `x=-r/2+rp`, `z=rq`. The retained cubic note writes

```
f_x/r^2 = 6k p(p-1) + T q(p-1/2) + (C/2)q^2,
f_z/r   = A q + r[T p(p-1)/2 + Cq(p-1/2) + (D/2)q^2].
```

Differentiation in physical z gives

```
f_zz(x,z) = A + rC(p-1/2) + rDq.
```

Therefore, in this polynomial model,

```
f_zz(M) = A-rC/2,     f_zz(midpoint) = A.
```

The note's label `A=f_zz(M)` is inconsistent with its displayed polynomial whenever `C` is nonzero. A consistent naming is `A_0` for the displayed coefficient and `S_0=f_zz(M)=A_0-rC/2`. This is a coordinate-label correction, not evidence that the polynomial determinant formulas themselves fail. For a non-cubic field the analogous midpoint/endpoint conversion has a Taylor remainder; no exact full-field jet identity is asserted here.

On the transverse line `p=0`, `q!=0`, the witness equations give

```
T=Cq,     A_0=r(C-Dq)/2,     S_0=-rDq/2.
```

Direct differentiation and substitution then reproduce the retained determinants:

```
det H_M = q r^2 (3kD-C^2 q/4),
det H_X = q r^2 (-3kD-C^2 q/4+CD q^2/2),
det H_S = r^2 (6kC-3kDq-C^2 q^2/4).
```

Thus the two soft factors in the finite cubic model survive this correction. The line `p=0` is transverse to the endpoint axis; it must not be confused with the unresolved axial approach `q=0`. Here q is dimensionless and physical transverse distance is `r|q|`. In particular, `r^6 q^2` equals `r^4 z^2`, not `r^6 z^2`. The different physical-q estimate in issue #58 is not adjudicated by a notational conversion alone.

## 3. Deterministic short-edge triangle lemma

**Lemma (author-side proof).** Let f be C^{2,1} on an open neighborhood of a convex set K in R^2. Write H for its Hessian and assume

```
||H(x)-H(y)||_op <= L |x-y|,   x,y in K.
```

Let A,B,C lie in K, with all three gradients zero. Suppose

```
|B-A|=r>0,     0<|C-A|=d<=r/4,
|sin angle(B-A,C-A)| >= 1/2.
```

Then

```
|det H_A det H_B det H_C|
    <= (2025/1024) L^6 r^4 d^2
    < 2 L^6 r^4 d^2                    (when L>0).
```

The non-strict upper bound with constant 2 holds also for L=0. The Lipschitz bound must cover the entire triangle, including the segment joining the two original endpoints; a bound only on the tiny ball around A does not suffice for this proof.

### Proof

For two critical points U,V at distance ell and e=(V-U)/ell, the fundamental theorem of calculus yields

```
0 = grad f(V)-grad f(U)
  = ell H_U e + integral_0^ell [H(U+te)-H_U]e dt.
```

Consequently `||H_U e|| <= L ell/2`. The same estimate holds at V by reversing the segment. This is a deterministic identity and bound; no Gaussian conditioning, numerical tolerance, endpoint index, or prescribed height is used.

At A put u=(B-A)/r, v=(C-A)/d, and sigma=|det[u,v]|>=1/2. The two column estimates imply

```
|det H_A| sigma = |det[H_A u,H_A v]|
               <= (Lr/2)(Ld/2),
|det H_A| <= L^2 rd/2.                              (1)
```

For any unit vector w=alpha u+beta v, Cramer's rule gives `|alpha|,|beta|<=1/sigma<=2`. Therefore

```
||H_A||_op <= L(r+d) <= 5Lr/4.
```

Transporting to B using the Lipschitz bound and using `|det H|<=||H||_op^2` in dimension two gives

```
||H_B||_op <= 9Lr/4,
|det H_B| <= 81 L^2 r^2/16.                         (2)
```

Let ell=|B-C|<=r+d<=5r/4. The sine of the angle at C equals `r sigma/ell`, by equality of the two triangle-area formulas. Applying the critical-segment estimate in its two directions gives

```
|det H_C| <= (Ld/2)(Lell/2)/(r sigma/ell)
          = L^2 d ell^2/(4r sigma)
          <= 25 L^2 rd/32.                         (3)
```

Multiplying (1), (2), and (3) gives constant `(1/2)(81/16)(25/32)=2025/1024<2`, as claimed. For L=0 the three estimates give zero directly. QED.

The coarser constant is deliberate; no optimality is claimed. A slightly stronger B-column estimate is possible but unnecessary for the distance powers.

## 4. Full-field deterministic transverse-cone consequence

Put `M=(-r/2,0)`, `S=(r/2,0)`, and `X=M+r(p,q)`. On

```
0 < p^2+q^2 <= 1/16,      |p|<=|q|,
```

we have `d=r sqrt(p^2+q^2)<=r/4`, `sigma=|q|/sqrt(p^2+q^2)>=1/sqrt(2)`, and `d^2<=2r^2 q^2`. The lemma therefore gives, pathwise at the three exact critical points,

```
|det H_M det H_S det H_X| <= 4 L^6 r^6 q^2.          (4)
```

Unlike a finite cubic calculation, (4) applies to every C^{2,1} field satisfying the hypotheses. It retains both short-distance factors without imposing `|q|>=kappa r`. It therefore remains valid inside the nested microdisk **on this transverse cone**. It does not cover approaches with `|p|>|q|`, in particular the axial direction `q=0`.

## 5. Conditional Kac-Rice implication, not a discharged Gaussian lemma

For the original six endpoint pins let Q_r be their Gaussian regression law. Let

```
W_r=|det H_M det H_S| 1_{specified endpoint types},
Z_r=E_{Q_r}[W_r].
```

Assume the relevant Kac-Rice identity is valid and, uniformly on the cone of Section 4 and compact stated marks, that

```
p_{grad f(X) | endpoint pins}(0) <= C_p/(r^3 q^2),
E_{Q_r}[L^6 | grad f(X)=0] <= C_6,
Z_r >= c_Z r^2 > 0.                                 (5)
```

These are explicit application hypotheses. This note does not prove them for the periodized six-pin field. In particular, a random L cannot be discarded outside the conditional expectation, a finite cubic covariance cannot replace the full covariance, and a moment bound under unweighted endpoint regression alone is not automatically the bound after adding the witness constraint.

By (4), endpoint typing costs at most one, so the determinant-weighted witness intensity is bounded by

```
[p_{grad f(X)|pins}(0)/Z_r]
 E_{Q_r}[W_r |det H_X| | grad f(X)=0]
 <= (4 C_p C_6/c_Z) r.                             (6)
```

Physical area is `dX=r^2 dp dq`. Thus, **conditional on (5) and the Kac-Rice identity**, the fixed transverse cone has expected count O(r^3). Its intersection with `p^2+q^2<=kappa^2 r^2`, for fixed kappa, has expected count O(r^5). No height-window factor was inserted; this is an all-height conditional implication on the specified cone, not an all-height theorem on the entire pin neighborhood.

Remaining work: establish the required uniform regression/density and conditional sixth-moment controls; handle angular sectors not covered by (4), especially the nested axial regime; prove the collar to the reviewed annulus; address intermediate scales and shrinking multiple-witness collisions separately. Neither the old covariance note's Section 5 target nor global D5 is declared closed.

## 6. Finite controls and review request

`finite_controls.py` uses only exact Fraction arithmetic. It checks 48 cubic coordinate/determinant cases, 54 separable critical-cubic triangle examples, the rational constant product, and a quadratic noncritical counterexample showing that the critical-point hypothesis cannot simply be dropped. These are finite controls, not a proof over arbitrary C^{2,1} functions.

Reproduction:

```
python -B -S finite_controls.py
python -B -O -S finite_controls.py
python -B -S finite_controls.py --mutant endpoint-label
python -B -S finite_controls.py --mutant omit-soft-factor
python -B -S finite_controls.py --mutant zero-bound
```

The two baseline outputs are byte-identical to `RESULTS.json`. Each mutant exits 1 in both interpreter modes. `SOURCE_FILES.json` hashes these three local files, excluding itself. The scripts check neither Gaussian regression nor the candidate proof's continuum quantifiers. No archived research program was executed.

Requested nonauthor review: independently differentiate the retained cubic, verify the critical-segment bound and triangle constants, check the cone/physical-coordinate conversion, and assess the exact remaining uniform Gaussian hypotheses. The general C^{2,1} lemma and the stochastic implication have separate scopes. Shared owner identity or a green CI run earns neither organizational independence nor scientific acceptance.

## 7. Reconnaissance memo and novelty boundary

Consensus discovery located Beliaev, Cammarota and Wigman, *No repulsion between critical points for planar Gaussian random fields*, arXiv:1911.03455 (2019 preprint; published in Electronic Communications in Probability in 2020, DOI 10.1214/20-ECP362). The fetched abstract concerns stationary isotropic planar critical-point correlations and index dependence. It is context for determinant/density cancellation, not a theorem covering this periodized, multiply conditioned Palm problem. Only the abstract and bibliographic identity were inspected here; no theorem from it is imported into (5).

Primary record: https://arxiv.org/abs/1911.03455 . The local source in Section 1 already contains the elementary Taylor/simplex mechanism. This note claims a useful short-edge specialization and a source-label correction, not discovery of critical-point repulsion or a worldwide-first interpolation theorem.
