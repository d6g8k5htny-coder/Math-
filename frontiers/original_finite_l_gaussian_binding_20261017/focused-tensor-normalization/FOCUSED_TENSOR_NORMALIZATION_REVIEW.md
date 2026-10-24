# Focused nonauthor tensor and normalization review

**Verdict: ACCEPT_SCOPED for the tensor, regressions and coefficient normalization in §§5–6 and8 of the exact new binding proof. No must-fix finding in this focused scope.** The hand derivation below verifies that, once the exact ideal Gaussian law has been admitted to the stated GAD theorem, GAD(27)/(28) specializes to the ORIGINAL algebraic coefficient with the displayed constants. This is input to the integrated review, not an independent acceptance of the entire new source-law/Borel-observable binding or a numerical qualification.

The exact new PROOF.md is22163bytes/445lines, SHA-256 **ad9ab5afea28062dfc661d0d19b43f20e67cfd67cb6910d3cc6c3fb8b81398d8**. I read it completely. The original source is24027bytes/SHAf38c085ab5b15368e6989a1fd6298490f3b671f5a6c3a01bcdc81b516022bc33. GAD is40231bytes/SHA8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319, with its exact38035-byte accepted scoped review. READ_EXTENT.json gives actual bounded rereads; no new full GAD/classical-source read is invented.

Actual reviewer: OpenAI/Codex /root/c261a_successor_preparation_review_20261016, nonauthor of the new binding proof, GAD and ORIGINAL. I have prior source preparation/custody exposure to GAD, exact finite-L method V1/V2 delta exposure and related asymmetric/formal-interface review exposure. Those are disclosed source contacts, not blind evidence. Shared provider/principal, organizational independence0, provider-distinct0, blind0, human0. I did not author or repair this proposal. The validation here is independent hand algebra/index contraction/Gaussian integration; only inert byte/hash work was executed.

## 1. Physical derivative tensor, including its signs

Write K(x-y)=E cos(Q·(x-y)), where the physical wave numbers are h m, h=2pi/L, and Q has the original full product lattice distribution. Termwise differentiation is justified by the supplied summable Fourier moments. For multiindices alpha,beta of even total order2r,

    Cov(partial^alpha F,partial^beta F)
      =(-1)^(|beta|+r) E Q^(alpha+beta);

odd total order gives zero. This is just the y-derivative sign together with the derivative of cosine at zero. It gives, in particular,

    Cov(D_i,D_j)=a delta_ij,
    Cov(F,H_ij)=-a delta_ij,
    Cov(D_i,H_jk)=Cov(T_ijk,H_lm)=0,
    Cov(D_i,T_jkl)=-M_ijkl,
    Cov(H_ij,H_kl)=M_ijkl,
    Cov(T_ijk,T_lmn)=M_ijklmn.

Here a=E Q_i², b=E Q_i⁴, c=E Q_i⁶. For the fourth tensor, coordinate parity leaves only one fourfold index or two equal pairs. Thus

    M_ijkl=a²(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)
             +kappa4 sum_s delta_is delta_js delta_ks delta_ls,
    kappa4=b-3a².

This gives b when all indices agree and a² for each two-distinct-pair case. It is the exact ORIGINAL(5), not an isotropic replacement. For completeness the sixth tensor is the sum of a³ over its15pairings, a*kappa4 over its15partitions into a fourfold block and a pair, and kappa6 on the all-equal index block. Here kappa6=c-15ab+30a³. The cumulants are those of the spectral coordinate Q, not an assumption that Q is Gaussian.

All these field jets are jointly Gaussian. Therefore the zero cross-covariance of the entire odd block(D,T_e) with H proves actual block independence. It does not prove independence between T_e and D; that correlation is explicitly retained. The nonzero Cov(F,H) also shows why common-height pinning cannot silently be added.

## 2. Independent contractions: B, R and the raw Schur complement

Put Y=He, so Y_i=sum_j H_ij e_j. Contracting the three pairings of M_i j k l against e_j e_l gives respectively a²delta_ik, a²e_i e_k and a²e_i e_k. The fourth-cumulant contraction is kappa4 delta_ik e_i². Hence

    B(e)=Cov(Y)=a²(I+2ee^T)+kappa4 diag(e_i²),

exactly ORIGINAL(6) and new(11).

Let A^0_ab=sum_jk U_ja H_jk U_kb, where U^T U=I and U^T e=0. In Cov(A^0_ab,Y_i), the trace pairing gives a²delta_ab e_i. The other two pairings contain U_a·e or U_b·e and vanish. The fourth-cumulant term leaves

    R_ab,i=a²delta_ab e_i+kappa4 U_ia U_ib e_i.

Contracting all four tensor slots against U gives

    C_ab,cd=a²(delta_ab delta_cd+delta_ac delta_bd+delta_ad delta_bc)
               +kappa4 sum_i U_ia U_ib U_ic U_id.

Gaussian conditioning at the literal zero target therefore gives

    Gamma_e(ab,cd)=C_ab,cd-R_ab B(e)^(-1) R_cd^T.

This is precisely ORIGINAL(11) and new(13), including correlated diagonal/off-diagonal entries. The free indices a<=b are coordinate positions, not statistically independent Gaussian entries. No diagonalization or independence simplification of Gamma is permitted. In particular the free-entry Gaussian density is the ordinary N-dimensional density with N=(d-1)d/2; its Lebesgue element lists each A_ab once. There is no sqrt(2) Jacobian to insert into that original measure.

For positivity, a nonzero symmetric S gives a nonzero quadratic polynomial Q^T S Q. Full lattice support cannot annihilate that polynomial, so the full Hessian covariance is positive definite. The linear coordinate map H ->(He,U^THU) is invertible on Sym_d. Its jointly positive covariance implies B>0 and Gamma_e>0 by the Schur complement. The negative cone is nonempty open and the nondegenerate centered Gaussian density is positive there; determinant-square weight is positive off its zero hypersurface and has finite Gaussian moments. Thus F(e)>0 and finite. This argument does not replace the field by a finite spectral carrier.

## 3. Odd regression, independently expanded

Expanding E[Q_i(Q·e)^3] by coordinate multiplicity gives

    v_i=b e_i³+3a² e_i sum_(j!=i)e_j²
       =3a²e_i+kappa4 e_i³,
    Cov(T_e,D_i)=-v_i.

Write S4=sum_i e_i⁴ and S6=sum_i e_i⁶. The sixth directional moment, obtained either from the full sixth tensor or from its one/two/three-coordinate multiplicities, is

    E(Q·e)^6=15a³+15a*kappa4 S4+kappa6 S6.

Indeed the direct multiplicity expansion is c sum e_i⁶+15ab sum_(i!=j)e_i⁴e_j²+90a³ sum_(i<j<k)e_i²e_j²e_k², and sum e_i²=1 converts it to the displayed form. Also

    |v|²=9a⁴+6a²kappa4 S4+kappa4² S6.

Subtracting |v|²/a, as required by Cov(D)=aI, yields

    Var(T_e | D=0)
      =6a³+9a*kappa4 S4+(kappa6-kappa4²/a)S6=V(e).

This matches ORIGINAL(8) and new(10). At a coordinate axis it is c-b²/a. Omitting the regression instead gives c on that axis, a different positive expression. The cubic polynomial(Q·e)^3 cannot equal a linear polynomial on the full lattice for a unit e, so the residual variance is strictly positive. The conditional mean is zero at D=0.

Because (D,T_e) and H are independent blocks, their joint conditional density/kernel under D=0,He=0 remains the product of the two separately conditioned blocks. Thus A_e|He=0 is independent of T_e|D=0 at the exact zero targets, and p_(D,He)(0,0)=p_D(0)p_He(0). This is the extra special-law fact needed to factor GAD's generally coupled joint-jet invariant. It is not supplied by Gaussianity alone on an arbitrary manifold law.

## 4. Hand normalization ledger against GAD(27)/(28)

GAD(27) contains the positive third-jet part and full ordinary sphere area:

    12^(-1/3)/Vol integral_X integral_S
      p_(D,He)(0,0) E[(T_e)_+^(4/3)(det A_e)^2 1_A<0 | pins] d omega dx.

GAD(28) equivalently has |T_e|^(4/3) and prefactor1/(2*12^(1/3)*Vol). That half comes from antipodal averaging; it does not add an unordered-pair division after the original ordered maximum/death count. The accepted GAD review explicitly retains the coupled formula for general laws and this half/full-sphere convention. The present law has the separate parity/independence proof above, so the expectation factors here.

The two pin blocks each have d components. Their exact Gaussian zero-density product is

    p_D(0)p_He(0)
      =(2pi)^(-d) a^(-d/2) (det B(e))^(-1/2).

The frame-valued Hessian column and the fixed physical He differ by an orthogonal d-dimensional transformation of absolute determinant one. Its zero density contributes no further determinant. There is no p_F(0): birth height has been integrated out, and the transverse law is conditioned only on He=0.

For Z~N(0,V), integrating both half-axes and setting y=t²/(2V) gives

    E|Z|^(4/3)=2^(2/3) Gamma(7/6) V^(2/3)/sqrt(pi),
    E(Z_+)^(4/3)=2^(-1/3) Gamma(7/6) V^(2/3)/sqrt(pi).

Stationarity makes the remaining x integrand constant in x. Its integral is the physical Vol=L^d, canceling GAD's inverse volume once. Now

    [1/(2*12^(1/3))]*2^(2/3)=24^(-1/3).

Substitution into GAD(28) gives exactly

    Gamma(7/6)/[24^(1/3)sqrt(pi)(2pi)^d a^(d/2)]
      integral_S F(e)V(e)^(2/3)/sqrt(det B(e)) d omega.

This is ORIGINAL(1), including every e-dependence. Using GAD(27) with the one-sided moment gives the identical scalar. No finite-L-to-continuum moment substitution, sphere-probability normalization, common-height density, extra L^(-d), pair half or off-diagonal measure factor was used.

## 5. Independent hand crosschecks and adverse alternatives

In d=2 with e along the first coordinate and U along the second, B=diag(b,a²), R=(a²,0) and C=b. Thus the raw transverse conditional variance is b-a⁴/b and F=(b-a⁴/b)/2. The separate one-half is a centered scalar Gaussian's negative-half second moment. It is not the antipodal averaging half. Meanwhile V=c-b²/a, checking that the two regressions are distinct.

As a purely algebraic isotropic reference, set kappa4=kappa6=0, not as a finite-L substitution. Then V=6a³ and B=a²(I+2ee^T). The conditional transverse tensor is a²(delta_ac delta_bd+delta_ad delta_bc+(2/3)delta_ab delta_cd), so d=2 gives variance8a²/3 and F=4a²/3. These expressions agree with the axis Schur result at b=3a². No coefficient digits or numerical integral are evaluated.

The wrong extra height condition is detectable even in that reference: Cov(F,A_ab | He=0)=-(2a/3)delta_ab, rather than zero. Conditioning further on F=0 therefore changes the transverse covariance. This refutes exchanging the height-integrated law with a height-pinned one.

Physical derivative units supply another independent ledger: p_D p_He has length exponent3d, F exponent-4(d-1), and V^(2/3) exponent-4; the product has exponent-d as a per-physical-volume density coefficient must. An extra L^(-d) double-counts volume. Scaling the field by a positive scalar zeta changes the pin density by zeta^(-2d), determinant square by zeta^(2(d-1)) and the fractional moment by zeta^(4/3); the coefficient therefore scales as zeta^(-2/3), agreeing with direct lifetime rescaling. An extra height density or pair half violates the respective ledger or the two equivalent GAD moment formulas.

## 6. Focused disposition and retained boundary

I find no incorrect sign, tensor contraction, Schur-conditioning target, measure conversion, scalar moment or half/sphere/volume factor in §§5–6 and8. Subject to the integrated review verifying the exact law's admission and whole-field/observable joins, their coefficient identity C_GAD=C_alg is valid. GAD(27)/(28) are actual theorem inputs under GAD's fixed Gaussian-series hypotheses and stated classical imports, not unrestricted Gaussian covariance formulas.

The independent overall author theorem, source-law equality and global ordinary-H0/density-representative bridge remain the integrated reviewer's responsibility; the limited review here does not manufacture a whole-proof PASS. It also does not retrospectively validate the original source's own global arguments, run V2's enclosure method or supply M31, an effective window, sampler/grid/count-transfer/confidence evidence, new field data, numerical coefficient, formal alignment or scientific promotion. The method and optional P3/P7 advisory are not mathematical premises of this new coefficient contraction.

All19 author freeze rows match unchanged. No original source/old seal was edited. No mathematical program, old control, Lean, field, quadrature, coefficient calculation, network mutation or native publication occurred. Only hand conventional reasoning and inert source/hash custody support this focused report. Scientific effect NONE; no continuing review reservation remains after delivery.
