# Collisions below the pin scale have vanishing weighted mass

Object OA-SUBPIN-COLLISION-20261002-v1. Author-side conditional corollary,
OpenAI/Codex, 2 October 2026. Scientific effect NONE. This is a deduction from
the exact imported results below, not a new acceptance of their proofs.

## 1. Observable and source boundary

Fix a dimension d >= 2 and a torus side L > 0. Use the centered variance-one
periodized Gaussian field, the pin pair M = -ru/2, S = ru/2 with heights
b and b-kr^3, k > 0, and both gradients zero. Q_r is the canonical regression
on these pins. Retain the original typed determinant weight and FULL normalizer

    W_r = F_d(H_M) F_(d-1)(H_S),
    Z_r = E_Qr W_r,             P_r = (W_r/Z_r) Q_r.

F_j is the absolute Hessian determinant times its index-j indicator. Let N_r
count all additional critical points in the open window (b-kr^3,b), excluding
M and S. All distances below are torus geodesic distances. The count is finite
almost surely under the imported regularity and moment statements.

Let epsilon:(0,r_*) -> (0,infinity) be deterministic and Borel measurable, with
epsilon(r) -> 0. Define the ORDERED distinct-pair count

    C_r = sum_(x != y, additional window critical points)
                         1{dist_T(x,y) <= r epsilon(r)}.          (1)

There is no adjacency, persistence or gradient-connection condition on x,y.
The endpoints of (1) are additional witnesses, not the original pins.

All source identities and exact consumed portions are in SOURCES.json, at
Math- commit a808ba25de9db22110db8b7555a64852f38e031d:

- [TS] TWO_SCALE_LAW.md, Theorems T and L, (T5), (T7), (L1), (L3).
  Its complete configuration-space limit and ordered-pair law are needed;
  convergence of the one-point intensity alone would not suffice.
- [SC] spectral_cluster_closure/PROOF.md, as consumed by TS: finite nonempty
  cubic measure, pointwise simple roots, and the first/count-moment bounds.
- [C6] c6_palm_route/PROOF.md, Theorem Q: the original weighted factorial
  moments of orders q >= 2, uniform on compact b,k and frames. The uniform
  first-moment upper bound is [DL](1.7), explicitly used in the proof of C6
  Section 7, Corollary P. With that first moment, the Stirling expansion gives
  E_Pr N_r^q <= C_q r^3 for every positive integer q on such compact sets.
- [DL] d5_dimension_lift/PROOF.md, Theorem G_d (1.7), with its stated
  dimension-lift/regional dependencies retained. This is the compact-uniform
  first-moment interface; SC's pointwise statement alone is not substituted.
- [P] the lifetime parent, read with its required reconciliation/errata and
  replacement Section 9. We use its full normalizer Z_r/r^2 -> z_0 > 0,
  its marked Kac-Rice identity, and (10.2)-(11.2), including the compact-uniform
  bound on A_r. The original parent Section 9 is not an unrepaired premise.

TS has a source-bound nonauthor acceptance in review5360227991 and its current
REVIEW_RECORD.md. That acceptance remains conditional on the exact SC/CUB/RM/C6/P
interfaces stated in TS. We neither remove those conditions nor re-review them.
No conclusion here is conditional on the open PR242, PR243 or PR244.

## 2. The sub-pin-scale theorem

**Theorem D.** For every fixed b, k > 0, frame, d and L, and every epsilon above,
for each fixed nonnegative integer p,

    E_Pr [N_r^p C_r] = o(r^3),
    P_r(C_r > 0) = o(r^3),
    E_Qr [W_r N_r^p C_r] = o(r^5).                         (2)

N_r^0 is defined to be 1, including at N_r = 0. The little-o is pointwise in
the fixed marks. No uniform little-o, algebraic rate, numerical constant,
growing dimension/volume, or k -> 0 assertion is supplied.

**Proof: remove pairs outside the microscopic component.** Choose a deterministic
cutoff delta_r = sqrt(r) for small r; only delta_r -> 0 and delta_r/r -> infinity
are used. Let N_in count the points at distance < delta_r from the pin midpoint.
TS(L1), with q = 2, gives

    E_Pr [(N_r)_2 - (N_in)_2] = o(r^3).                   (3)

Every ordered pair not wholly inside that ball, including close pairs far from
the pins, is counted in (3). Thus no near-diagonal covariance bound uniform in
the midpoint location is being silently assumed.

**Proof: the microscopic limit puts no mass on coincident spatial positions.**
For the pairs wholly inside the delta_r ball, let nu_r be r^-3 times their
expected ordered-pair measure on

    E x E,        E = R^d x (0,1) x {0,...,d},

using positions x/r, downward normalized height, and index. TS(L3) gives weak
convergence of FINITE measures nu_r -> nu, including convergence of total mass.
The limiting measure is the integral, on two-root cubic configurations, of
the two ordered atoms (z_1,z_2) and (z_2,z_1) against the finite nonempty
spectral measure. The cubic roots have distinct spatial positions almost
everywhere on this measure. Therefore the spatial coincidence diagonal D has
nu(D) = 0. This is stronger than finite-r simplicity alone.

For eta > 0 define the bounded continuous cutoff on E x E

    phi_eta(z,z') = min(1, max(0, 2 - |pos(z)-pos(z')|/eta)).       (4)

It equals 1 when the distance is <= eta and vanishes at distance >= 2 eta.
Eventually epsilon(r) <= eta. Also 2 delta_r < L/2, so the torus distance
between any two points in the delta_r ball equals the Euclidean distance
between their chosen local lifts. Consequently

    limsup_(r->0) r^-3 E_Pr [C_r with both points inside]
        <= lim_(r->0) integral phi_eta dnu_r
         = integral phi_eta dnu.                              (5)

As eta decreases to zero, phi_eta tends to 1_D. Finiteness of nu and dominated
convergence give integral phi_eta dnu -> 0. Combining (3) and (5) proves
E_Pr C_r = o(r^3). The order of limits is r -> 0 first for fixed eta, then
eta -> 0. No finite-r density estimate, spatial total variation, or choice of
root ordering is needed.

**Proof: multiplicities and the original numerator.** C_r is either zero or
at least two, since both orientations of a close pair are included. Hence

    P_r(C_r > 0) <= E_Pr C_r/2 = o(r^3).                  (6)

Pathwise, N_r^p C_r <= N_r^(p+2) 1{C_r>0}. Cauchy-Schwarz and the imported
ordinary moment of order 2p+4 give

    r^-3 E_Pr[N_r^p C_r]
      <= (r^-3 E_Pr N_r^(2p+4))^(1/2)
                                      (r^-3 P_r(C_r>0))^(1/2) -> 0.  (7)

This is why an event probability alone is not substituted for counted mass.
Finally the definition of P_r is an exact identity:

    E_Qr[W_r N_r^p C_r] = Z_r E_Pr[N_r^p C_r].            (8)

Since Z_r/r^2 -> z_0, (8) proves the o(r^5) numerator. There is exactly one
endpoint determinant weight and one full normalizer. QED.

## 3. Compact-mark lifetime consequence in the actual intensity units

Fix compact intervals B in R and K = [k_-,k_+] with k_- > 0, a fixed d,L,
and all directions u in S^(d-1). Define

    m_p(r,b,k,u) = E_Pr[N_r^p C_r].

The mark is jointly Borel: on a compact spatial domain away from the pin and
pair diagonals, critical-point counts with the Borel distance/height indicator
are measurable under the canonical regression kernels; exhaust these domains.
The inherited weighted marked Kac-Rice identity extends by monotone truncation
to this nonnegative count mark. Its integrability follows from C6's ordinary
moment bound. This uses the repaired [P] Section 9, not continuity of C_r.

Per unit midpoint volume, the candidate intensity carrying this multiplicity is

    d beta_p = r A_r(b,k,u) m_p(r,b,k,u) dr db dk d sigma(u),       (9)
    A_r = 12 pi_r (Z_r/r^2).

Thus every pin density, spatial/height Jacobian and original determinant
normalization is already present in (9). sigma is ordinary spherical surface
area, not normalized Haar probability. The pin roles order the maximum/saddle
pair; there is no new factor 1/2. C_r itself counts ordered witness pairs.

**Corollary E.** Under the exact height-gap map ell = k r^3, beta_p has a
Lebesgue density satisfying

    rho_p(ell) = o(ell^(2/3)),
    beta_p{0 < ell <= t} = o(t^(5/3)).                     (10)

This statement concerns the collision-marked candidate measure (9). Its
submeasure obtained by inserting the actual global elder indicator satisfies
the same estimates. It is not an identification of another proxy population
with the persistence bars, nor a claim that all selection failures satisfy (10).

**Proof.** For ell < k_- r_*^3, put R = (ell/k)^(1/3). Tonelli and the exact
one-variable change of variables give the density version

    rho_p(ell) = ell^(2/3)/3 * integral_(B x K x S^(d-1))
               k^(-5/3) A_R(b,k,u) [m_p(R,b,k,u)/R^3]
                                                db dk d sigma(u).       (11)

Indeed r dr/dell = k^(-2/3) ell^(-1/3)/3 and R^3 = ell/k.
For every fixed b,k,u the bracket in (11) tends to zero by Theorem D.
It is bounded uniformly on the compact mark domain because
m_p <= E_Pr N_r^(p+2) <= C r^3 there. A_R is also uniformly bounded by [P].
The remaining k^(-5/3) factor is integrable because k >= k_- and the domain
has finite measure. Dominated convergence proves the density assertion.
Integrating its absolute nonnegative bound gives the cumulative assertion:
for any a > 0, rho_p(ell) <= a ell^(2/3) for all sufficiently small ell for
this density version, so beta_p(0,t] <= (3a/5)t^(5/3).
Any other version obeys the corresponding almost-everywhere bound. QED.

Pointwise convergence in the marks plus this uniform integrable majorant is
enough; no compact-uniform little-o is being imported. The Borel epsilon is
the same function of r across the mark domain and need not be monotone.

## 4. What the hypotheses prevent

These are abstract marked-count examples, not counterexamples to the Gaussian
field. Their purpose is to make the logical boundaries testable.

1. **Moments alone do not remove subscale collisions.** With probability r^3
   place two witnesses at scaled positions 2 and 2+r, otherwise none. Then
   every fixed moment is 2^q r^3, but for epsilon(r)=sqrt(r), E C_r=2r^3.
   The limiting pair measure charges the diagonal. The simple limiting roots
   in TS(L3), not merely the global factorial bound, exclude this example.
2. **No algebraic rate follows from weak convergence.** In a rare event of
   probability r^3, place the two scaled points at 2 and 3 with probability
   1-a_r, and at 2 and 2+r with probability a_r, where a_r=1/log(1/r)
   for r<exp(-1). The finite pair measure converges to the simple unit-separated
   pair. Nevertheless E C_r=2r^3/log(1/r) for epsilon(r)=sqrt(r). This is
   o(r^3) and is not O(r^(3+gamma)) for any gamma>0.
3. **An event estimate alone does not control multiplicity.** Let r_n=2^-n,
   N_n=r_n^-1 with probability r_n^5 and zero otherwise, and cluster those
   witnesses within the distance cutoff. Then P(C_n>0)=r_n^5=o(r_n^3),
   but E C_n = r_n^3(1-r_n), which is not o(r_n^3). Its fourth count moment
   is r_n, violating the moment hypothesis used in (7).
4. **Scale-r doublets remain.** Replacing epsilon(r)->0 by a fixed positive
   cutoff can retain positive limiting pair mass. TS's positive two-root
   coefficient and all consequences about non-singleton clusters remain intact.

The exact controls check finite count inequalities, these examples' rational
arithmetic and the coarea exponents. They do not prove weak convergence,
Gaussian conditioning, the imported parent theorems, or mathematical acceptance.

## 5. Relation to the completion directive

The earlier proposed compact-mark O(r^3) task was already supplied by C6
pointwise in b,k and frame; [P](11.2) already uses height-disintegrated units.
The missing implication in a generic marginal example cannot be attributed to
these sources. Likewise the existing globally elder-marked endpoint route
identifies actual finite bars at its own conditional scope; it does not require
auxiliary-witness uniqueness. This note leaves that route and its review
requirements unchanged. It supplies the stricter sub-pin-scale conclusion (2).

This result removes subscale extra-witness collisions from a compact-mark
ell^(2/3) coefficient in any argument whose error is explicitly dominated by
the measure (9). It does not prove that every bad geometric configuration has
that domination. It supplies no O(ell^(3/4)) remainder, no uniform k->0 tail,
no rate in an expanding annulus, and no resolution of PR242 Conjecture 7.
It does not concern a witness colliding with a pin, shared endpoints between
different candidate pairs, or the whole class of scale-r doublets. No status,
historical predicate, normalizer, scientific gate or independence credit changes.
