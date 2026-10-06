# Cap I4: spectral pushforward domination and an explicit envelope bound

Object: CAP-I4-ADAPTER-ENVELOPE-20261005-v1. Author: OpenAI / GPT-6 Astra Pro, session cap-i4-adapter-envelope-audit-20261005, delegated by Dylan Roy. Author-side analytic derivation; not a Lean proof, independent alignment disposition, or scientific promotion. Scientific effect NONE.

## Bound source and purpose

P is `Math-/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, read at `f4079f65a3e5e95c9993e51ac5995a54344d4130`. Consumed: density (3.5), full-field residual (4.2)-(4.3), full normalizer (5.5), typed determinant (6.2), and (7.1)-(7.7). Its scaling sentence in section 5 is consumed only with the existing congruence erratum: diag(r^(-1/2),I), not diag(sqrt(r),I).

The existing companion `CapI4.lean`, blob `4769930d132a485f88b75c4f4d901a3c4db7d43e`, consumes `MatrixDepthTransport`, a uniform integrable envelope and the full normalizer. This note reduces the source-facing transport requirement to a *measure domination*, so a formal implementation need not choose measurable eigenvectors or construct an exact non-isotropic eigenvalue density. It also makes the required envelope bound explicit. These are sufficiency arguments, not a claim that the missing concrete Lean interface is already implemented.

## 1. Precise input and the smaller spectral interface

Fix m>=2, n=m-1, a probability law Q, 0<r<=1 and k>=k_->0. Let B=-A_M be a measurable real symmetric m by m matrix and let e(B)=(lambda_1,...,lambda_m) be its increasingly ordered eigenvalues. Let J>=1 be measurable, independent of the *entire* B, with E_Q J^p<=M_p, p=2m+6. Let W>=0 be integrable, with W=0 off typed support T. On T, B>0, h=M3>=0, h<=K(J+Lambda), K>0, Lambda=lambda_m, and P(6.2) holds. W, h and the eigenvalues are NOT assumed mutually independent. All statements may hold Q-almost everywhere.

For C_m={0<lambda_1<=...<=lambda_m}, Delta(lambda)=product_(i<j)(lambda_j-lambda_i), and ordinary coordinate Lebesgue measure d lambda, define

    sigma_m(d lambda) = C_sp exp(-c sum_i lambda_i^2)
                        Delta(lambda) 1_C_m d lambda, c>0.

The required generic spectral interface is precisely

    e_* (Law_Q(B) restricted to {B>0}) <= sigma_m          (S)

as measures: every nonnegative measurable spectral test has the corresponding integral inequality. The matrix law is restricted before pushing it forward. It is a finite subprobability on the left, not a claim that sigma_m is normalized.

P(3.5) plus its symmetric-matrix Lebesgue change of variables in section 7 supplies (S) analytically: push forward the measure inequality

    Law_Q(B) <= C_0 exp(-c ||B||_F^2) dB.

The reference upper density is invariant even when Law_Q(B) is not. Weyl integration is needed only for this reference measure. C_sp includes C_0 and the angular/multiplicity/Jacobian normalization exactly once. Its value depends on the convention for symmetric-matrix Lebesgue coordinates; it is NOT set to one. Ordered eigenvalues are continuous; no eigenbasis or eigenvector sign convention enters (S). Repeated-eigenvalue strata cause no selection problem here.

Because J is independent of B, the joint positive-cone pushforward is Law(J) product e_*(Law(B)|{B>0}); monotonicity gives domination by Law(J) product sigma_m. Independence of eigenvalues has not been introduced. Marginal density bounds without this joint product domination would not suffice.

## 2. Derive the existing pre-integration transport, not its desired conclusion

Set

    U=J+Lambda,
    D=4K^2/(3k_-), E=3K/2,
    A_m=K^2(1+K)^(m-1)/4,
    v=m(m-1)/2.

On typed support, the depth event lambda_1<=4r h^2/(3k) implies lambda_1<=DrU^2. In P(6.2), for j>=2 and r<=1,

    lambda_j(lambda_j+rh) <= (1+K)U^2,
    h^2/4 <= K^2 U^2/4.

Consequently

    W 1_depth <= A_m r^2 U^(2m) lambda_1(lambda_1+ErU)
                 1_{C_m, lambda_1<=DrU^2}.               (1)

This is a pointwise domination by a function of J and the eigenvalues, even when W itself depends on the entire residual and eigenvectors. Thus no conditional independence of W is used.

Apply joint measure domination. On the ORIGINAL ordered domain Delta<=Lambda^v. Apply this bound before enlarging the lambda_1 interval, and drop exp(-c lambda_1^2)<=1. Since m>=2, Lambda is among the remaining coordinates and is fixed during the lambda_1 integral. The actual interval [0,min(lambda_2,DrU^2)] can then be enlarged to [0,DrU^2], with a nonnegative integrand. Tonelli gives

    E_Q[W;depth] <= integral_(J,x in T_n)
      r^2 P(x) U^(2m) integral_0^(DrU^2) t(t+ErU) dt
      dLaw(J) dx,                                       (2)

where T_n={0<x_1<=...<=x_n}, Lambda=x_n,

    P(x)=C_sp A_m Lambda^v exp(-c ||x||^2).

Equation (2) is exactly the existing MatrixDepthTransport conclusion, with Xi=R times R^n and nu=Law(J) product (Lebesgue restricted to T_n). It is not the desired r^3 probability assumed as an input. There is no inverse-eigenvalue power or lower cutoff on x_1. All multiple-soft neighborhoods, and all repeated-eigenvalue limits, remain in the integration.

## 3. Explicit uniform envelope constant

For n>=1, s>=0 and c>0, define

    G(n,s,c) = pi^(n/2) Gamma((n+s)/2)
               / [2^n n! Gamma(n/2) c^((n+s)/2)].        (3)

This is exactly the integral of ||x||^s exp(-c||x||^2) over T_n. Proof: the radial integrand assigns equal mass to the 2^n orthants and the n! coordinate-order chambers; their boundaries are Lebesgue null. Polar integration gives sphere area 2 pi^(n/2)/Gamma(n/2), while substitution y=c rho^2 contributes the factor 1/2 and Gamma((n+s)/2). These factors give (3). The 2^n n! factor applies AFTER radial domination; it is not a second factor in C_sp.

Since Lambda<=||x|| and (J+Lambda)^p<=2^(p-1)(J^p+Lambda^p), Tonelli and the probability normalization of Law(J) give

    E integral_Tn (J+Lambda)^p Lambda^v exp(-c||x||^2) dx
      <= 2^(p-1) [M_p G(n,v,c)+G(n,v+p,c)].              (4)

Every term is finite. This proves integrability as well as an upper bound; a totalized divergent Bochner integral is not being used.

The companion's exact primitive is

    integral_0^(DrU^2) t(t+ErU) dt
       = r^3[(D^3/3)U^6+(ED^2/2)U^5].

As U>=1, its spectral envelope is bounded using the single residual moment p=2m+6. A sufficient explicit constant is

    C_depth = C_sp A_m (D^3/3+ED^2/2) 2^(p-1)
              [M_p G(n,v,c)+G(n,v+p,c)].                (5)

Then E_Q[W;depth] <= C_depth r^5. If Z=E_Q W>=c_Z r^2 with c_Z>0, the actual weighted probability satisfies

    Q^W(depth) <= (C_depth/c_Z) r^3.                    (6)

Uniformity follows when K,k_-,C_sp,c,M_p,c_Z are uniform over the fixed-dimension, fixed-torus, compact-mark and compact-frame family. Merely having an unevaluated finite M_p(r) for every r does not supply this uniform result.

For m=2 (d=3), n=1,v=1,p=10, (4) specializes to

    512 [M_10/(2c)+60/c^6].                             (7)

This is an explicit reduction of the spectral envelope constant to the residual tenth moment and density constants. It is not a numerical radius, a certified value of C_depth, or the anisotropic lifetime coefficient c_(3,4).

## 4. Scalar m=1 must remain separate

Formula (3) is NOT used at n=0. With D=4K^2/(3k_-), P's depth implication is lambda<=Dr(J+lambda)^2. The companion proves the near/far split

    lambda<=4DrJ^2  OR  lambda>1/(4Dr).

On the near part h<=H J^2 with H=K(1+4D). Put E_s=3H/2. The bounded scalar density C_0 and independence of J from B imply

    E_Q[W;near depth] <= C_0 H^2/4
       * (64D^3/3+8E_s D^2) E J^10 r^5.                (8)

The far part is

    E_Q[W;far] <= (4D)^4 M_far r^6,
    M_far >= sup E_Q[(W/r^2)lambda^4].                  (9)

The latter is the original weighted joint moment from P(7.6), not an unweighted surrogate. After the full-normalizer division, (8)+(9) gives the retained r^3+r^4 bound. No statement in the matrix calculation discards this branch.

## 5. Measurability, typed support, and E4 assembly

The random scalar norms and ordered eigenvalues must be measurable. For each fixed radius/frame, C^4 norm restriction and supremum of continuous derivative-block norms on the compact cylinder are measurable; a jointly parameterized law or later intensity integral still requires its own measurable kernel. This note asserts no probability-one set common to uncountably many parameter laws.

The geometric cap implication need hold only Q-almost everywhere where W>0:

    W>0 and goodCap  =>  G_geometric.

For nonnegative W this implies pointwise, up to a Q-null set,

    W 1_(G_geometric^c) <= W 1_(goodCap^c).

Integrate and divide by the SAME positive full Z. This is the correct bridge from a typed-support deterministic statement; a global implication off weighted support is unnecessarily strong. Event measurability and integrability are retained.

For E4 use exactly P(7.7), with M_4joint bounding E_Q[(W/r^2)M4^4] uniformly:

    Q^W(E4) <= M_4joint/[c_Z(3k_-/10)^4] r^4.

The union then gives the source-model r^3+r^4 bound. Neither a raw Gaussian M4 fourth moment in place of its actual weighted moment, nor a normalization restricted to goodCap, is permitted.

## 6. Formal and audit disposition

The existing CapI4.lean still supplies the exact primitive, conditional transport consumer, same-law normalization, E4 specialization, and scalar split. No Lean theorem bytes were changed by this note. The source-to-Lean work can be divided into: (i) the generic eigenvalue pushforward domination (S), with a properly normalized Weyl reference measure; (ii) the actual residual independence and moment bounds; (iii) nonnegative integration and the explicit envelope above; (iv) measurable typed-support/geometric and full-normalizer instantiation. This note does not add (S) as an axiom or label it kernel-checked.

The accompanying test_adapter_envelope.py executes twelve finite exact-algebra methods in normal and optimized modes. It crosschecks radial moment ratios by independent Cartesian multinomial expansion, chamber factors, the determinant prefactor, the depth threshold, the double-soft r-power, ordered-domain extension, coupled-marginal counterexamples, weighted-support logic, and scalar/uniformity negative examples. These tests are not the Weyl theorem, Gaussian regression proof, or Lean execution. No new literature novelty claim is made.
