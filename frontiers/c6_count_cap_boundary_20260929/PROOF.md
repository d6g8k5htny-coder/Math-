# What a rare first moment and a global count cap can—and cannot—prove

Object: OA-C6-COUNT-CAP-BOUNDARY-20260929-v1.
Author: OpenAI / ChatGPT, 29 September 2026.
Disposition: AUTHOR-SIDE MATHEMATICAL CANDIDATE; nonauthor review required.
Scientific effect NONE. No existing source, review, status, graph, lemma flag or
prize is modified. No novelty or Gaussian optimality claim is made.

## 1. Purpose and independence from the Gaussian candidates

The new C6 route bounds a rare window count N by a total critical-point cap Psi.
Claude's Math-#142 separately develops a Gaussian cap tail using a growing
complex Cauchy radius. This note does NOT duplicate that theorem. It proves an
abstract inference bound, an explicit example saturating it, and an exact
size-bias identity isolating the extra information needed for a log-free result.

No Gaussian covariance, Rouché theorem, invariant manifold or unreviewed
higher-dimensional first-moment statement is an input to the proofs below.
The existing project arguments motivate the hypotheses but are not proved or
accepted by this note. In particular, the example is NOT a Gaussian random
field and says nothing about the actual optimal order of C6.

Fix an integer d>=2. For each sufficiently small r>0, let Q_r be a probability
law, P_r a law with density R_r=dP_r/dQ_r, N_r a nonnegative integer-valued
random variable, and Psi_r a nonnegative measurable cap with N_r<=Psi_r.
Assume constants independent of r satisfy

    E_{P_r} N_r <= C_0 r^3,             ||R_r||_{L2(Q_r)} <= K,
    Q_r(Psi_r>x) <= C_1 exp(-c phi_d(x)),
    phi_d(x)=x^(1/d) log(2+x),            x>=0.                 (B1)

The laws and variables may otherwise depend on r. Constants may depend on d.
No independence between the cap, count and density is assumed. The cap-tail
hypothesis implies Psi_r<infinity almost surely under both laws. For integer
q>=1, (N)_q=N(N-1)...(N-q+1), with value zero when N<q.

**Theorem A (inference bound).** For every fixed integer q>=2, writing
L=log(1/r), (B1) implies

    E_{P_r}(N_r)_q <= C_q r^3 [L/log L]^{d(q-1)}               (B2)

for all sufficiently small r. It also implies a uniformly bounded small positive
exponential moment of phi_d(Psi_r), under Q_r and P_r.

**Theorem B (limit of these hypotheses).** There is an explicit family satisfying
(B1), even with P_r=Q_r and E N_r=r^3 on a sequence r_n decreasing to zero, such
that for every fixed q>=2

    E (N_{r_n})_q ~ r_n^3 [L_n/log L_n]^{d(q-1)}.              (B3)

Thus (B1) alone cannot imply an o of the right-hand side in (B2), or an O(r^3)
second factorial moment. This is an optimality statement for this ABSTRACT
class of inference, not for Gaussian critical points.

**Proposition C (the missing correlation).** Let m_r=E_{P_r}N_r>0 and define the
count-size-biased configuration law

    dP_r^sb = (N_r/m_r) dP_r.

Then the exact identity

    E_{P_r}(N_r)_q
      = m_r E_{P_r^sb}[(N_r-1)_{q-1}]
      <= m_r E_{P_r^sb}[Psi_r^{q-1}]                          (B4)

holds as an identity/inequality of nonnegative extended expectations. Therefore
uniform size-biased cap moments, not merely unconditional cap moments, suffice
for a log-free O(r^3) result. Count-size bias is NOT conditioning on N_r>=1.

## 2. Proof of the upper inference bound

The tail in (B1) gives every fixed polynomial cap moment uniformly:

    E_{Q_r}Psi_r^p
       = p integral_0^infinity t^(p-1) Q_r(Psi_r>t)dt <= C_p.

This formula follows first for truncations and then by monotone convergence.
Since phi_d grows faster than log t, the integral is finite. In particular all
moments used below exist, independently of r.

For any cutoff lambda>0 and integer q>=2, pathwise

    (N)_q <= N Psi^{q-1}
           <= lambda^{q-1}N + Psi^q 1{Psi>lambda}.             (B5)

Take expectations under P_r. Cauchy–Schwarz with the actual density R_r, followed
by another Cauchy–Schwarz under Q_r, gives

    E_{P_r}[Psi^q 1_A]
      <= ||R_r||_2 (E_{Q_r}[Psi^{2q}1_A])^(1/2)
      <= K (E_{Q_r}Psi^{4q})^(1/4) Q_r(A)^(1/4)
      <= C_q exp(-c phi_d(lambda)/4),       A={Psi>lambda}.   (B6)

Both square roots matter. Neither (B5) nor (B6) factors an expectation of N and
Psi or assumes independence of R_r from the cap. In the application R_r=W_r/Z_r;
a uniform W_r/r^2 moment and a positive Z_r/r^2 floor are what bound its norm.
Those Gaussian facts are external premises, not consequences of this note.

Take lambda=(A L/log L)^d, A>=1, with L sufficiently large. For example,
log L>=2 implies 2loglog L<=log L; hence

    log lambda = d(log A+log L-loglog L) >= log L,
    phi_d(lambda) >= lambda^(1/d) log lambda >= A L.           (B7)

Choose A so cA/4>=4. The tail term in (B6) is at most C_q r^4. The first term in
(B5) is at most C_0 r^3 lambda^{q-1}. Since lambda>=1 for small r, the r^4 term is
absorbed, proving (B2). Each q is fixed; no uniform-in-q constant is asserted.

For the exponential-moment assertion, use that phi_d is continuous, strictly
increasing on [0,infinity), and unbounded. From (B1),
Q_r(phi_d(Psi_r)>t)<=C_1 e^{-ct}. Layer-cake integration gives

    E_{Q_r} exp(a phi_d(Psi_r))
      =1+ a integral_0^infinity e^{at}Q_r(phi_d(Psi_r)>t)dt
      <=1+C_1 a/(c-a),                       0<a<c.

Under P_r, Cauchy–Schwarz bounds the moment at a by K times the square root of
the Q_r moment at 2a. Thus any 0<a<c/2 works uniformly for both laws. This extra
unconditional integrability STILL does not eliminate the loss, as the example
shows.

## 3. Explicit family attaining the inference bound

For integers n>=3 define

    r_n=n^{-n},        K_n=n^d,        p_n=r_n^3/K_n.

Under P_n=Q_n, set N_n=K_n with probability p_n and N_n=0 otherwise. Put
Psi_n=N_n+2. This +2 models the harmless presence of two excluded prescribed
objects in a total cap; no pinning or Gaussian law is asserted. The density
R_n is identically one, so its L2 norm is one. Direct computation gives

    E N_n = p_n K_n = r_n^3,
    E(N_n)_2 = r_n^3(K_n-1),
    E(N_n)_q = r_n^3 product_{j=1}^{q-1}(K_n-j).               (B8)

For fixed q and n large, the last expression is asymptotic to
r_n^3 n^{d(q-1)}. These identities use falling factorials, not ordinary powers.

### A uniform cap-tail bound, not merely bounded moments

For x<2, Q_n(Psi_n>x)=1. For 2<=x<K_n+2 it is p_n, and for x>=K_n+2 it is zero.
For n>=3 and d>=2,

    (n^d+2)^(1/d)<=2n,       n^d+4<=n^{d+1},
    phi_d(K_n+2)<=2(d+1)n log n.

Let c_d=1/[2(d+1)]. Monotonicity gives, whenever 2<=x<K_n+2,

    p_n=exp(-(3n+d)log n)
       <=exp(-n log n)
       <=exp(-c_d phi_d(K_n+2))
       <=exp(-c_d phi_d(x)).                                 (B9)

For x<2, use C_d=exp(c_d phi_d(2)) to extend the same bound. For larger x the
tail is zero. Therefore (B1) holds with constants independent of n. The example
also satisfies the uniform exponential-cap-moment conclusion of Theorem A.
A large rare cap cannot be excluded just by knowing all unconditional moments.

Finally

    L_n=log(1/r_n)=n log n,
    L_n/log L_n=n log n/(log n+loglog n) ~ n.                  (B10)

Combining (B8) and (B10) proves (B3). A family indexed by every small r can be
obtained by assigning this law at r_n and setting N_r=0,Psi_r=2 elsewhere;
(B1) still holds. No continuity in r is among the hypotheses. The subsequence
already disproves any purported universally stronger conclusion from (B1).

## 4. The exact extra input: size-biased configuration moments

For m_r>0 the formula in Proposition C defines a probability law because
E N_r/m_r=1. It assigns zero mass to N_r=0. At N_r>=1,

    (N_r)_q=N_r (N_r-1)_{q-1}.

Integrating proves the identity in (B4), including when the result is infinite.
Since (N-1)_{q-1}<=Psi^{q-1}, its upper bound follows. Thus

    sup_r E_{P_r^sb}Psi_r^{q-1}<infinity and m_r<=Cr^3
          imply E_{P_r}(N_r)_q<=C_q r^3.                     (B11)

For q=2 the exact ratio E[N(N-1)]/E N is E_{P^sb}(N-1). If E N is two-sided of
order r^3, boundedness of this size-biased mean is also necessary for an O(r^3)
second factorial moment. Boundedness of the possibly loose Psi under that law
is a sufficient, not necessary, replacement.

The distinction from conditioning on nonemptiness is elementary but essential.
Take P(N=0)=1/3, P(N=1)=1/2, P(N=3)=1/6. Then E N=1. Under count-size bias,
N=1 and N=3 each have probability 1/2. Under P(.|N>=1), their probabilities
are 3/4 and 1/4. They yield different expectations, even in a finite space.

In the family of Section 3, P_n^sb is concentrated entirely on the rare outcome
N_n=K_n. Consequently E_{P_n^sb}Psi_n=K_n+2 diverges, even though the original
cap has a uniform stretched-super-exponential tail. This isolates precisely the
correlation not controlled by (B1).

For an actual point process, disintegrating the N-weighted configuration law by
a tagged point is the appropriate entry to a Palm/marked-intensity argument.
The current Gaussian research route called M'/H aims to supply such conditional
marked control. This note neither proves that route nor assumes it to close C6.
It explains why a new marked estimate is genuinely additional information.

## 5. Verification and boundaries

The public finite checker uses exact rational probabilities and integer falling
factorials. It tests (B8), finite size-bias identities, the probability-tail
steps, algebra behind (B9), the pathwise cap split and the W/Z exponent ledger.
Its negative variants deliberately replace count-size bias by conditioning on
nonemptiness, use the wrong rare probability, replace falling factorials with
ordinary powers, lose the dimension, remove the +2 pin offset, or drop Z.

Those checks are NOT a proof of all real-parameter tail integrals or asymptotic
limits. The analytic arguments are the displayed derivations above. No numerical
Gaussian constant, actual Gaussian lower saturation, all-d D5 acceptance, or
independent formal alignment follows from the tests. No scientific register or
source proof is altered. Classical truncation, Hölder, size-bias and power-law
calculations are credited as such; there is no worldwide novelty claim.

Context only, not mathematical inputs: Math-#140, the separate Claude successor
#142, and the marked M'/H lane discussed in #140. Their exact context references
are recorded in SOURCE_MAP.json. This note does not depend on those drafts being
accepted or merged, and must not be used as their Gaussian verification.
