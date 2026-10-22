# Higher configurations for the normalized Gaussian square truncations

16 October 2026 UTC. **Local conventional mathematical proposal; pending separate nonauthor review.** Authors: OpenAI/Codex `/root/core_theorem_audit_20261015`, with Root's problem selection and steering, and the author-side dual-floor attack by `/root/core_theorem_audit_20261015/dual_gaussian_floor_attack`. Same-provider organizational-independence credit **0**. The latter contribution is an author check, not a nonauthor review. No source/native/remote/runtime/Lean edit, ownership change, source admission, theorem-register change or scientific-status transition occurs here. All previously frozen artifacts remain unchanged.

The substantive new step is an explicit Hermite interpolation construction for the Euclidean covariance `exp(-|h|^2/2)`. It gives, for each fixed p, a `7p` contact covariance floor `c_p eta^(8p-2)` at arbitrary planar configurations with minimum separation eta. Its constants do not depend on the configuration diameter or on comparable collision scales. This avoids assuming a higher-configuration analytic-distance certificate. A torus clustering argument transfers the floor to the declared finite Gaussian family. The remaining sections derive the `6p`-pin kernel bounds, account for near configurations with a p-dependent cutoff, identify the compact marked intensity, and use Bonferroni inequalities to obtain every compact Laplace functional. This is a proposed conventional proof for **local endpoint candidates in one specified changing Gaussian law**, not a theorem about global persistence bars or arbitrary normalized spectra.

## 1. Exact inputs and the new declaration

All repository references below are pinned to Main `85b928b326ff0586715a56ae91f51d3fbd89557a`; no assertion that this is the latest live head is made.

| Pinned source | Bytes | SHA-256 |
|---|---:|---|
| [finite_gaussian_contact/PROOF.md](https://github.com/d6g8k5htny-coder/main/blob/85b928b326ff0586715a56ae91f51d3fbd89557a/experiments/universality/finite_gaussian_contact/PROOF.md) | 25367 | `7fea2656e11d986e1a5d6bfb0a05c8421bd93262d28051b8cfef05320595f474` |
| [finite_candidate_lifetime/PROOF.md](https://github.com/d6g8k5htny-coder/main/blob/85b928b326ff0586715a56ae91f51d3fbd89557a/experiments/universality/finite_candidate_lifetime/PROOF.md) | 29190 | `ed31f562f0ffaaf6d4bd2ceb1ae3d234798e983a55d55c6983b128fce27133f5` |
| [iid_short_bar_process/PROOF.md](https://github.com/d6g8k5htny-coder/main/blob/85b928b326ff0586715a56ae91f51d3fbd89557a/experiments/universality/iid_short_bar_process/PROOF.md) | 30935 | `320bc988c468bea4938bb777a2d05952c6ab8e0a384f33725b50de847aeec1eb` |

The exact source supplies the ideal real coefficient law, the six divided-difference rows and target, per-pair observation determinant `12 r^-5`, endpoint congruence correction, coefficient-space area formula and once-inserted Hessian determinants. Its fixed-law theorem does not by itself give the uniform changing-law result below. Its iid process is not substituted for the field in this proposal.

The following local accepted inputs are consumed only within their reviewed scope. The bytes and hashes were read again, without rerunning their controls.

| Frozen author input | SHA-256 | Corresponding ACCEPT_SCOPED review SHA-256 |
|---|---|---|
| `QUANTITATIVE_FOLD_ISOLATION_PROPOSAL.md` | `827c82953845eb12005542ff6a4e1c99886b68d1ea9f1aeae16f981622ac6a30` | `f06c61e3f3e60c795a1a14e824640f1689d4143dba4f6698cada7a41929eec90` |
| `FINITE_FOURIER_CRITICAL_COUNT_DIAGONAL_ROUTE.md` | `621cee96854aa440498cecf5452a8d1e23f90a4458779c3286c18eba106fe138` | `16152427f7013822ac1bba81142429800334e6bf0f354a6439b23a1997bc4524` |
| `UNIFORM_LOCAL_NORM_DIAGONAL_PROPOSAL.md` | `8e1eefca9888d43824a9fd9caca34c44d2de4bf8e30c668b474fa2097491c76b` | `ff552dfacadede53405530a219302c1163dca8ba97d518f02d407970d3de3c1c` |
| `JET_NONDEGENERACY_FACTORIZATION_OBSTRUCTION.md` | `0dfdddfbcac47b2fd07449f4152b7f5d935f92aed15272fb8333ed9cc60b5766` | `531b9d9a16831383f2f217e61bad7dea84aca941a934e4bcaa771bedcc4e73af` |

In particular the last review accepts the finite-radius twofold `m^-14` and `sqrt(r)m^-16` estimates, their source-row/area-formula joins, and the Gaussian truncation/image estimates. It expressly leaves higher configurations, changing-source adoption and full process convergence open. The present note supplies new arguments for those analytic and candidate-process steps; the old acceptance does not review these new arguments.

Declare the following family, rather than claiming that an existing catalogue law already has it. For t decreasing to zero let

```text
L=L(t),       L t^(1/3) -> ell_* in (0,infinity),
Lambda_*(t)^2 ~ B log(1/t),       B>0,
K=ceil(L Lambda_*/(2pi)),       Lambda=2pi K/L,
q_(t,n)= exp(-|(2pi/L)n|^2/2)
             / sum_(|m|infinity<=K) exp(-|(2pi/L)m|^2/2),
|n|infinity<=K.                                             (1)
```

Use precisely the source's independent standard real Gaussian sine/cosine coordinates, with DC variance q_0 and each nonzero pair's amplitudes `sqrt(2q_n)`. Every weight is positive and symmetric and their sum is one. Write `V=L^2`, `v_*=ell_*^2=lim V t^(2/3)`. No numerical PRNG implementation is identified with this ideal law.

The accepted Gaussian grid comparison gives, eventually in this family,

```text
sum q_n=1,    sum q_n |(2pi/L)n|^12 <= M12 < infinity,
delta_6 <= C exp(-Lambda^2/64),
sup_(|alpha|<=6) |D^alpha R_t(h)|
     <= C[exp(-dist_T(h,0)^2/8)+delta_6].                    (2)
```

The normalized infinite image covariance is

`R_inf,L(h)=sum_j exp(-|h+Lj|^2/2)/sum_j exp(-|Lj|^2/2)`.

On lifted distances at most p times `O(sqrt(log(1/t)))`, the finite covariance derivatives through order six differ from the Euclidean Gaussian derivatives by `C_p[delta_6+exp(-cL^2)]`. Indeed every noncentral image is at least `L-pR` away; `pR=o(L)`. This is the same image estimate as the accepted bounded-distance argument, applied on this explicitly growing region. The denominator differs from one by `O(exp(-cL^2))`. Normalization, not M12 alone, controls the DC and lower spectral moments.

## 2. Exact candidate process and the proposed conclusion

Fix `v=Ju`, with J the positive quarter-turn. A candidate is an ordered pair `(M,S)` of critical points, M a nondegenerate local maximum and S a nondegenerate index-one saddle, with positive gap `ell=F(M)-F(S)`. Choose the shortest torus displacement `S-M=ru`; at cut-locus ties choose a fixed Borel convention. Its center is `x=M+ru/2`, and its recorded marks are

```text
s=ell/t,   b=F(M),   k=ell/r^3,   A=F_vv(M),   y=M/L,   u.
```

The mark space is

`E=(0,infinity)_s x R_b x (0,infinity)_k x (-infinity,0)_A x T_1^2_y x S^1_u`.

Let Xi_t place one atom for every such ordered candidate. A maximum has A<0 for every u. Compact subsets of E have fixed bounds `s<=s_+`, `k>=k_->0`, `A<=-a_-<0`, bounded b,k,A and s bounded away from zero. Thus every candidate seen by a compact test has

`r<=r_t=(s_+t/k_-)^(1/3)`. The cut locus is eventually irrelevant there. Candidate identity is the endpoint pair, not an independently chosen saddle incidence. Distinct candidates may share endpoints; Section 6 handles this rather than ignoring those factorial terms.

Let `J_infty,u=(F,F_u,F_uu,F_uuu,F_v,F_uv,F_vv)` have the Euclidean covariance `exp(-|h|^2/2)`, and let `p_Jinfty,u` denote its seven-dimensional density. The proposed intensity is

```text
nu(ds db dk dA dy d sigma(u))
 = v_* 144 s^(-1/3) k^(4/3) A^2
       p_Jinfty,u(b,0,0,12k,0,0,A)
           ds db dk dA dy d sigma(u),       A<0.             (3)
```

Here dy is unit-volume Haar measure and `d sigma` is unnormalized circle arclength, of mass `2pi`. There is no extra `1/2`. The measure is Radon on E and strictly positive on every nonempty open mark box. The claim to be justified conventionally below is, for each **fixed** integer p and `f_i in C_c(E)`,

```text
E integral product_i f_i(z_i) Xi_t^[p](d(z_1,...,z_p))
                  -> product_i integral f_i d nu,           (4)
E exp(-Xi_t(f)) -> exp[-integral(1-exp(-f))d nu],
                  f in C_c(E), f>=0.                        (5)
```

`Xi^[p]` is the ordered factorial measure: the sum over ordered p-tuples of distinct candidate atoms. There is **no `1/p!` in (4)**. That factor occurs once in the inclusion-exclusion series in Section 9. These are compact local-mark statements; no unbounded-mark integration, global elder indicator or actual persistence interval is being asserted.

## 3. Constructive Euclidean full-jet floor

This is the new analytic lemma. For p distinct points `x_i in R^2`, assume `|x_i-x_j|>=eta`, `0<eta<=1`. Let Sigma_raw be the covariance of all `10p` raw derivatives `D^beta F(x_i)`, `|beta|<=3`, for `R(h)=exp(-|h|^2/2)`. Then

`Sigma_raw >= c_p eta^(8p-2) I`, with `c_p>0` depending only on p.       (6)

There is no bound on the diameter or on ratios of separations. The proof is explicit. Use the unitary two-dimensional Fourier convention

```text
hat g(xi)=(2pi)^(-1) integral exp(-ix.xi)g(x) dx,
mu(dxi)=(2pi)^(-1) exp(-|xi|^2/2) dxi,
||g||_*^2=(2pi)^(-1) integral exp(|xi|^2/2)|hat g(xi)|^2 dxi.
```

For `L_a=sum_(i,beta) a_(i,beta) D^beta|_(x_i)`, Fourier inversion and Cauchy-Schwarz give

`|L_a g|^2 <= Var(L_a F) ||g||_*^2`.                       (7)

Let `h_ij=x_j-x_i`, and work in the **centered** variable `s=x-x_i`. Define

```text
q_ij(s)=|s-h_ij|^2/|h_ij|^2
       =1-2h_ij.s/|h_ij|^2+|s|^2/|h_ij|^2,
B_i(s)=product_(j!=i) q_ij(s)^2,
P_i,beta(s)=T_<=3 [ s^beta / (beta! exp(-|s|^2/4)B_i(s)) ],
g_i,beta(x)=exp(-|s|^2/4) B_i(s) P_i,beta(s).              (8)
```

`T_<=3` is the total-degree-three Taylor polynomial at s=0, and `beta!=beta_1! beta_2!`. Because B_i(0)=1, that Taylor expression exists. At every other center its factor `|s-h_ij|^4` kills all derivatives through degree three. At its own center its Taylor polynomial is `s^beta/beta!`. Therefore

`D^gamma g_i,beta(x_j)=1{j=i,gamma=beta}` for all `|gamma|<=3`.       (9)

The polynomial `Q_i,beta=B_i P_i,beta` has degree at most `D=4p-1`. A coefficient bound independent of diameter follows from the submultiplicative norm `||Q||_eta=sum |Q_alpha| eta^|alpha|`. With `u=q_ij-1`,

```text
||u||_eta <=2sqrt(2)eta/|h_ij|+2eta^2/|h_ij|^2 <=5,
||q_ij^2||_eta <=36,
||T_<=3 q_ij^-2||_eta
 <=1+2(5)+3(5^2)+4(5^3)=586,
||T_<=3 exp(|s|^2/4)||_eta <=3/2.
```

Truncated power-series multiplication has the same norm bound. Consequently

```text
||Q_i,beta||_eta <= C_p^(0)=(3/2)21096^(p-1),
sum_alpha |Q_alpha| <= C_p^(0) eta^(-D).                  (10)
```

Far h makes the nonconstant coefficients smaller, not larger; expansion in global coordinates is unnecessary. This is the place where a naive bounded-diameter analytic compactness proof could lose uniformity.

The Fourier transform of `exp(-|s|^2/4)` is `2exp(-|xi|^2)`. Polynomial multiplication gives Gaussian derivatives. Define the finite number

```text
A_D=max_(|alpha|<=D) [ (2pi)^(-1) integral exp(|xi|^2/2)
                |D_xi^alpha(2exp(-|xi|^2))|^2 dxi ]^(1/2).
```

Its integrands are polynomials times `exp(-3|xi|^2/2)`. Translation only multiplies the Fourier transform by a unit phase. Hence

`||g_i,beta||_* <= A_D C_p^(0) eta^-D`.

Apply (7) to all the duals (9) and sum. This gives

```text
||a||_2^2 <= Var(L_aF) 10p A_D^2(C_p^(0))^2 eta^(-2D),
c_p=[10p A_(4p-1)^2(C_p^(0))^2]^-1.                     (11)
```

This proves (6), including an explicit finite constant defined by finitely many ordinary Gaussian integrals. No infinite-dimensional Gaussian-Hilbert assertion, arbitrary finite-support jet assertion, analytic-distance exponent or numerical eigenvalue extrapolation is used.

For the contact rows in independent arbitrary orthonormal frames, first weight the full raw jet by

`W=diag(1; 1,1; 1,sqrt(2),1; 1,sqrt(3),sqrt(3),1)`.

These are Frobenius coordinates for the symmetric derivative tensors. Frame changes, including reflections, are orthogonal on these weighted tensors. Since `W^2>=I`, the same lower floor holds after weighting and rotation. Selecting the raw contact tuple `(F,F_u,F_uu,F_uuu,F_v,F_uv,F_vv)` then has selection Gram matrix bounded below by `I/2`; only F_uv has the `1/sqrt(2)` scale. Thus the `7p` contact covariance satisfies

`Gamma_p >= (c_p/2) eta^(nu_p) I`, `nu_p=8p-2`.           (12)

The author-side attack independently checked the Fourier normalization, coefficient bounds, tensor metric and /2 factor and found no obstruction. Its finite rational checks support selected interpolation/rotation identities, not the all-parameter analytic proof.

## 4. Transfer to a growing torus without an equal-scale assumption

Fix p. Put `R_t=sqrt(A0 log(1/t))`, with any fixed `A0>0`. Form a graph on the p centers, joining a pair when its torus distance is at most R_t. Assume the centers have pairwise torus separation at least eta. Every graph component has q<=p vertices.

For small t, `pR_t<L/2`. Lift a component to R^2 along a spanning tree. Each tree displacement is the unique short torus displacement, and every lifted difference has length at most `(q-1)R_t<L/2`. Its Euclidean difference is therefore also a shortest torus displacement; consistency across an extra graph edge follows because a cycle has total length less than L and cannot wind by a nonzero lattice vector. All lifted pair separations are at least eta. This includes components straddling either torus seam.

Within each lifted component use (12). Its diameter may diverge as R_t and its internal distances may have arbitrarily many different scales; (12) has no diameter dependence. The block diagonal Euclidean covariance, one block per component, has floor `c'_p eta^(nu_p)`. For singleton blocks use the fixed positive one-contact floor; since eta<=1 this also implies the same weaker power floor.

Within blocks, the finite/periodic covariance error is `C_p[delta_6+exp(-cL^2)]` by (2). Between components every torus distance exceeds R_t, so their entries are at most `C_p[exp(-R_t^2/8)+delta_6]`. Operator norms cost only a p-dependent constant. Consequently

```text
||Gamma_p,t - blockdiag(Gamma_component,Euclidean)||
 <= C_p Delta_t,
Delta_t=delta_6+exp(-cL^2)+exp(-R_t^2/8).                 (13)
```

If eta is any inverse logarithmic scale, (1) gives `Delta_t=o(eta^(nu_p))`: both cutoff and far errors decay as a positive power of t, and image errors are faster. Weyl's inequality yields

`Gamma_p,t >= m_p(t) I`, `m_p(t)=c''_p eta^(nu_p)`.        (14)

This is uniform over **all** configurations with minimum torus separation eta and all p frames. It does not compare a fixed nonzero cross-block error to a vanishing floor: (13) is explicitly o of that floor. If all separations exceed R_t, every component is a singleton and the floor improves to a constant `m0/2` for small t. These statements hold for each fixed p; no floor uniform in p is claimed.

## 5. Literal 6p-pin kernels and their powers

Write the source six-row observations for each candidate as U_ri at its center/frame, and concatenate them into U_r of dimension 6p. The targets are exactly

`v_ri=(b_i-k_i r_i^3/2, -k_i r_i^2, 0, 12k_i, 0, 0)`.

Suppose the joint `7p` contact covariance has floor `0<m<=1`. Under (2), the coefficient rows of U_r have uniformly bounded Hilbert-Schmidt norms and differ from contact rows by `O_p(r)`, `r=max_i r_i`. Their covariance error is `O_p(r)`. Thus for `r<=c_p m` the finite pin covariance has floor m/2.

For each endpoint use the regular rows

```text
alpha_M#=[F_uu(M)-(F_u(S)-F_u(M))/r]/r
        =-integral_0^1(1-s)F_uuu(M+sru) ds,
alpha_S#=[F_uu(S)-(F_u(S)-F_u(M))/r]/r
        = integral_0^1 s F_uuu(M+sru) ds,
beta_M#, beta_S#: the same formulas with F_v and F_uuv,
A_M=F_vv(M), A_S=F_vv(S).                               (15)
```

Under the exact gradient pins alpha# and beta# equal `F_uu/r` and `F_uv/r`; unconditionally these regular rows have bounded L2 norms. Their coefficient errors from their contact limits are O(r). There is no assumption that unpinned `F_uu/r` has bounded covariance.

Represent U_r=L_r Z in the actual finite real coefficient space. With a fresh standard Gaussian Z' in that same finite space, a canonical conditional coupling is

```text
c_r=L_r^T(L_rL_r^T)^-1 v_r,
P_r=I-L_r^T(L_rL_r^T)^-1L_r,
E_r|U_r=v_r = L_E,r c_r + L_E,r P_r Z'.                 (16)
```

The row dimension of E_r is fixed by p. Inverse perturbation gives `||c_r-c_0||+||P_r-P_0||<=C_p r m^-2`. The conditional row moments of each fixed order are bounded by `C_p m^-1`; their coupled differences by `C_p r m^-2`. These constants are independent of the growing number of Fourier coefficients. They use the bounded row Hilbert-Schmidt norms and Gaussian moment bounds in a fixed row dimension, not the norm of the entire coefficient vector. The conditional E covariance may be singular.

The correct endpoint Hessian congruence is

`Htilde=[[alpha#,sqrt(r) beta#],[sqrt(r) beta#,A]]`.

Its determinant is the physical Hessian determinant divided by r, and inertia is preserved. Under (16), at M and S it is within `C_p sqrt(r)m^-2` in every fixed Lq of `diag(-6k,A_0)` and `diag(6k,A_0)`, respectively. Define

`V_i=|det H_Mi det H_Si|/r_i^2` times the maximum/saddle type indicators.

Equivalently V_i is the product of the maximum weight on Htilde_M and saddle weight on Htilde_S. These weights are continuous locally Lipschitz functions with quadratic growth: use the product of negative eigenvalue parts for a maximum and `(-det)_+` for a saddle. The product for p folds has degree 4p and Lipschitz growth degree `4p-1`. It follows, for bounded Lipschitz **local** marks w_i on fixed compact b,k,s,u,A,y windows, that

```text
E[product V_i | pins] <=C_p m^(-4p),
|E[product V_i w_i|pins_r]-E[product V_0i w_0i|pins_0]|
 <= C_p[sqrt(r)m^(-(4p+1))+r m^(-(4p+2))]
 <= C_p sqrt(r)m^(-(4p+2)).                              (17)
```

The second term retains the separate error from Lipschitz A marks multiplying the full degree-4p product. The birth position y=M/L differs from center/L by O(r/L), which is also controlled because L is bounded below. Fixed b,k,s,u targets do not change in this comparison. Hard A-window indicators need boundary anti-concentration for a rate; continuous tests suffice below.

The `6p`-dimensional Gaussian pin density is at most `C_p m^-3p`, and its compact-target perturbation is at most `C_p r m^(-(3p+2))` by differentiated Gaussian density. Define

```text
K_p^r =12^p p_Ur(v_r) E[product_i V_i w_i | U_r=v_r].
```

Then conservative bounds, including all marks just specified, are

```text
|K_p^r| <= C_p m^(-7p),
|K_p^r-K_p^0| <= C_p sqrt(r)m^(-(7p+2)).                 (18)
```

For p=2 these give exactly the reviewed powers 14 and 16. The factors in the error are: density error `r m^(-(7p+2))`, unmarked determinant error `sqrt(r)m^(-(7p+1))`, and mark error `r m^(-(7p+2))`. No physical Hessian inverse or inverse normalizer appears.

On configurations with all 2p endpoints distinct, finite pin rank implies rank of the original 6p value/gradient observations via the source's invertible per-pair transforms. In particular the 4p gradient rows are independent. The source coefficient-space area formula extends literally: cover position configurations by invertible 4p gradient coefficient minors, choose a disjoint Borel partition subordinate to this cover, solve for those Gaussian coefficients, and apply the equal-dimensional area formula in the 4p endpoint positions. The position derivative is block diagonal in the 2p physical Hessians. Integrating remaining coefficients and disintegrating values gives the joint Borel identity. No block-independence assumption is needed. The determinant product occurs once. Null critical degeneracies can be removed using the finite law's a.s. Morse property; the accepted algebraic count bound also holds a.s. At each fixed t this is a finite-dimensional argument. No theorem for an infinite carrier is imported.

The per-pair ledger is precisely

```text
(r dr d sigma)(r^3 db dk)(12r^-5 pin_density)(r^2 V)
             = r dr db dk d sigma (12 pin_density V).
```

For `s=ell/t=k r^3/t`,

`r dr = t^(2/3) s^(-1/3) ds/(3 k^(2/3))`.               (19)

Hence a p-fold compact-lifetime integral has the factor `t^(2p/3)`, with no factorial divisor. This is the cumulative short-lifetime scale. It does not replace the separate density statement `ell^(-1/3)` by `t^(-1/3)` counts.

## 6. Near configurations, including shared endpoints

Fix p>=2 and enlarge the finitely many test supports to one compact mark window. The accepted uniform local-norm result gives constants C,c,rho,eta_cap>0, depending on its fixed lower a_-,k_- and uniform moment bound, such that

```text
P(exists two distinct window candidates with centers <=eta,
                         radii <=rho eta)
 <= C(1+L)^2 exp(-c/eta),       eta<=eta_cap.             (20)
```

This is an unconditional deterministic-cover estimate, not a conditional field norm at a selected maximum. It allows the radii to exceed the actual center separation. It includes shared maxima by the chart's at-most-two-critical-points conclusion, shared saddles by maximum uniqueness, and excludes identical candidates. Cross-role equality is impossible. The frozen isolation falsifiers remain: no full height barrier, mixed-cubic shortcut or global pairing is inferred.

The accepted finite full-square Bézout argument gives `Ncrit<=16K^2` a.s. Therefore the total number of ordered p-tuples of distinct candidates is at most `(16K^2)^(2p)`. The count of tuples with some center pair at distance <=eta is bounded by this cap times the event in (20), once `r_t<=rho eta`. Choose the **proof cutoff for this fixed p** as

```text
H_p(t)=4p log K +2log(1+L)+4log(1/t),
eta_p(t)=c/H_p(t).                                      (21)
```

Then eta_p<=eta_cap eventually and `r_t/eta_p->0` in (1). Direct cancellation gives

```text
E[number of near ordered p-tuples]
 <= C 16^(2p) K^(4p)(1+L)^2 exp(-c/eta_p)
 = C 16^(2p) t^4 ->0.                                  (22)
```

This retunes the cutoff for p; it does **not** multiply an already fixed twofold error by an explosive cap. Each p is held fixed before t goes to zero, so different eta_p in separate factorial proofs change no process definition. No cutoff uniform over all p is needed by Section 9.

If two distinct candidates share any endpoint, their centers are at distance at most `(r_i+r_j)/2<=r_t<eta_p`. Thus every factorial incidence with shared endpoints lies in this already controlled region. This accounts for the terms that a 2p-distinct-endpoint Rice formula would otherwise miss. Outside the near region all endpoints are distinct, since each is within r_t/2 of its center.

## 7. Middle configurations and arbitrary clusters

Use eta=eta_p from (21) and R_t from Section 4. The middle region has all pair separations >eta but at least one pair separation <=R_t. Its positional volume is at most

`C_p V^(p-1) R_t^2`: choose one of at most `p(p-1)/2` close pairs, its anchor in volume V, its relative displacement in a torus ball of area at most `pi R_t^2`, and all remaining centers arbitrarily. Overcounting here only increases an upper bound.

The global cluster floor (14) and (18) imply

```text
middle factorial contribution
 <= C_p V^(p-1) R_t^2 t^(2p/3) eta^(-7p nu_p)
 = O_p(t^(2/3) log(1/t)^(1+7p(8p-2))) ->0.              (23)
```

Compact integrations in s,b,k,u and dropping bounded A marks only cost constants. The finite-radius rank requirement holds because `r_t/m_p(t)->0`. No finite-radius error needs to be integrated here; its upper bound suffices. The p-dependent logarithmic exponent, though large, is finite. All multiscale cluster patterns are covered by (14) rather than treated as independent folds.

The product of one-fold kernels on the omitted positional region is uniformly bounded and contributes at most `C_p V^(p-1)R_t^2 t^(2p/3)=O_p(t^(2/3)log(1/t))`, which also vanishes. The same estimate covers its near subset. This permits replacing the far product integral by its unrestricted product when computing (4).

## 8. Far factorization and the one-point compact limit

On the far region all center separations exceed R_t. The joint contact covariance is the block diagonal one-contact covariance plus an operator error at most

`C_p d_t(R_t)`, `d_t(R)=exp(-R^2/8)+delta_6`.

Both the block diagonal and joint covariances have a constant floor, and a uniform upper bound. Interpolate linearly between them. In fixed dimension 7p the derivative of the Gaussian density is the density times one trace term and one quadratic form. Its absolute value is bounded by `C_p d_t(R_t)(1+|z|^2)exp(-c_p|z|^2)`. Integrate the exact local contact weights

```text
12^p 36^p product_i k_i^2 A_i^2 1{A_i<0} w_i
```

at the pins `(b_i,0,0,12k_i,0,0,A_i)`. This proves

`|K_p^0-product_i K_1i^0|<=C_p d_t(R_t)`.

Together with (18), now with a constant floor, it gives

```text
|K_p^r-product_i K_1i^ri|
 <= C_p[d_t(R_t)+sqrt(r_t)].                            (24)
```

The integrated error is at most `(Vt^(2/3))^p` times this vanishing quantity. This factors local jet kernels only. A field-wide elder-selection indicator is not among the w_i and cannot be added by this density argument.

For p=1 the finite-radius coupling has a constant floor. The one-contact covariance converges uniformly in the frame to its Euclidean value by (2), so the same density comparison and coupling prove uniform compact convergence of the actual one-fold marked kernel. At contact,

```text
K_1^0 =12*36 k^2 integral_(A<0) A^2 w
                 p_Jinfty,u(b,0,0,12k,0,0,A) dA.
```

Combine this with (19), `dx=V dy`, and `Vt^(2/3)->v_*`. The coefficient is `12*36/3=144`, proving the compact intensity limit (3) and the p=1 case of (4). The finite-r error is O(t^(1/6)) on Lipschitz compact tests; the covariance error is O(delta_6+exp(-cL^2)), with an additional deterministic convergence error from `Vt^(2/3)`. No rate for this last convergence was assumed.

Near (22), middle (23), far (24) and the one-fold limit prove (4) initially for bounded Lipschitz compact tests. Every continuous compact test can be approximated uniformly by Lipschitz functions supported in a slightly larger compact subset of E. The same estimates with a compact envelope bound all the corresponding fixed factorial moment masses uniformly, so the approximation error goes to zero uniformly in t. This proves (4) for `C_c(E)`. It is not an all-mark tail theorem. In particular no passage to k=0 or A=0 is supplied by compactness.

## 9. All compact Laplace functionals, with a single factorial normalization

Let `f>=0` be continuous with compact support, and `g=1-exp(-f)`, so `0<=g<=1` has compact support. Every finite Xi_t satisfies

`exp(-Xi_t(f))=product_(z in Xi_t)(1-g(z))`.

For each nonnegative integer n put

`S_n(t)=sum_(p=0)^n (-1)^p/p! integral g^tensor p d Xi_t^[p]`.

Bonferroni inequalities give `S_(2m+1)(t)<=exp(-Xi_t(f))<=S_(2m)(t)`. One proof is to introduce, conditional on this finite configuration, independent Bernoulli variables with success probabilities g(z), and apply finite inclusion-exclusion to their no-success probability. This auxiliary algebra does not replace the spatial field by independent copies.

For each fixed m, (4) gives `E S_n(t)->sum_(p=0)^n(-1)^p mu^p/p!`, with `mu=integral g dnu`. Sending m to infinity squeezes both limits to `exp(-mu)`, proving (5). No uniform-in-p covariance floor, factorial bound, exponential moment of the candidate count, random infinite-series interchange, or simultaneous p,t limit is assumed.

The conventional point-process interpretation uses bounded primary imports. [Last and Penrose, *Lectures on the Poisson Process*, version 21 August 2017](https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf), Proposition 2.10 and Theorem 3.9, give Laplace uniqueness and the displayed Poisson Laplace characterization. [Bovier, *From spin glasses to branching Brownian motion — and back?*, Prague 2013 notes](https://www.math.ucla.edu/~biskup/Prague-school-2013/figs/Anton-notes.pdf), Appendix Theorem 4.11, printed p51 / PDF p57, states that convergence of Laplace functionals on nonnegative compact continuous tests implies weak convergence of point processes on Euclidean space. Only those bounded statements were read, not complete proofs of the books or their original cited theorems.

To apply the latter Euclidean statement literally, embed E properly as the closed subset `R^4 x (S^1)^3` of `R^10`, using `(log s,b,log k,log(-A))` and the two unit-torus circle coordinates and the u circle. Restrict any `C_c^+(R^10)` test to this closed copy; it is a compact test on E, so (5) applies. The intensity (3), pushed forward and set to zero off this copy, is Radon. The criterion therefore yields the corresponding vague point-process convergence for this **candidate** sector. This last sentence is an application of the named classical criterion; the quantitative work is (4)-(5). It is still a pending-review author conclusion, not project scientific acceptance or source admission.

## 10. Falsification, remaining scope and exact evidence

The following attacks were considered before accepting this proposed route.

* **Multiple collision scales or a very distant third center:** a compact analytic argument could hide a diameter constant. Here every normalized distance factor has nonconstant coefficients bounded using `eta/|h|`; (10) is independent of the largest distance. The separate author checks include close-plus-far and multiscale configurations. These finite checks do not replace (8)-(11).
* **Arbitrary frames:** raw unweighted third-jet rotations are not orthogonal. The explicit symmetric-tensor weights and `1/2` contact loss in (12) repair this; claiming an unweighted orthogonal action would be false.
* **Torus seams or winding clusters:** the lifting argument requires `pR_t<L/2`, satisfied for fixed p in (1), and includes the cycle check. It would not justify uniform growing-p configurations.
* **An exponentially ill-conditioned middle kernel:** its floor is an inverse logarithmic power with finite p-dependent exponent. The surviving factor `t^(2/3)` in (23) beats that power. Substituting a fixed small error without (13) would fail.
* **A coarse count cap after pair control:** retaining the p=2 cutoff and multiplying by `K^(4p-8)` can fail for large p. Equation (21) retunes the cutoff before estimating the actual p-count. No repeated accepted-control execution was used.
* **Shared endpoints:** all such distinct-candidate tuples lie in the near event and are bounded by (22); the area formula is only used after endpoints are distinct. Identical candidates are excluded by the factorial convention.
* **U alone, or U plus one-contact rank:** the accepted repeated-spectrum counterfamily remains a counterexample to a universal nonzero candidate Poisson law. It violates the new source-specific covariance approximation/far decay. The present theorem cannot be exported to arbitrary positive full-square weights, concentrated atoms or approximate periods.
* **Infinite or much faster carriers:** the algebraic count cap is finite K only; (21) needs `t^(1/3)[log K+log(1+L)] ->0`. Uniform M12 alone does not imply this growth condition. There is no increasing-p theorem, infinite-carrier count cap or quantitative numerical window here.
* **Soft marks and global topology:** fixed positive k_- and a_- are used in (20). Compact convergence gives no small-k/small-transverse-curvature complement. Candidate incidence is not a global bar-selection theorem, essential-class theorem, Hk theorem or elder-selector localization. Jet decorrelation cannot factor an elder indicator. The previous full-height-barrier and mixed-cubic counterexamples are retained unchanged.

The new finite controls check the factorial/near/middle exponent ledger and Bonferroni normalization exactly. The retained author-side dual checks use rational polynomial arithmetic on finite configurations and a rational frame rotation. Neither is a numerical proof of all-parameter analytic estimates, an evaluated intensity, a field experiment, a Rice integral, a Gaussian draw, a simulation of a Poisson process or a Lean proof. The source covariance and norm-tail controls accepted earlier were **not rerun**.

The precise new result proposed for review is the constructive covariance floor (6)-(12), its torus transfer (13)-(14), the fixed-p generalization (15)-(18), and their joined compact factorial/Laplace argument (19)-(24), for the family (1) and process defined in Section 2. The next action is a separate nonauthor mathematical review of these frozen bytes, especially the dual norm, torus lift, all-Borel 2p-endpoint join and p-dependent near accounting. No further author amendment is implied before such a finding. The full persistence/universality goal remains unmet.
