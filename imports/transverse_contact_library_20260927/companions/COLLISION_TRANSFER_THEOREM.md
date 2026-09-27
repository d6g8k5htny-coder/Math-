# Marked collision-to-lifetime transfer: theorem, coefficient and failure regimes

Object: OA-MARKED-TRANSFER-20260925-v1. Author: OpenAI / ChatGPT.
Disposition: author-side theorem with complete proof under stated hypotheses; application to any particular Gaussian persistence population remains separately gated.

## 1. What the exponent formula actually requires

The substitution ell~kappa*r^m is not, by itself, a density theorem. One needs (i) a precise marked pair intensity, (ii) actual-pair selection rather than arbitrary candidate pairs, (iii) derivative control on the lifetime map for pointwise densities, (iv) an integrable small-kappa envelope, and (v) control of other ways to produce short bars.

The basic pushforward calculation is standard measure theory, with close analogues in regular variation/product-tail theory (e.g. Denisov–Zwart, 2007). The scientific content is verifying the hypotheses for a nontrivial persistence-collision family. We do not claim invention of change of variables.

## 2. Density transfer theorem

Let (Z,lambda) be sigma-finite. For 0<r<r0, let the candidate-pair intensity be

    dmu = r^alpha a(r,z) dr dlambda(z),  alpha>-1, a>=0.

Let p(r,z) in [0,1] be the actual-persistence selection weight at the same intensity level. It need not be independent of the marks; all such dependence is included in a(r,z)p(r,z). Set

    b(r,z)=a(r,z)p(r,z),   beta=(alpha+1)/m,  m>0.

Suppose for almost every z:

1. b(r,z)->b0(z)>=0 as r->0.
2. 0<=b(r,z)<=G(z), with integral G(z) kappa(z)^(-beta) dlambda(z)<infinity and kappa(z)>0.
3. h(r,z) is continuous, strictly increasing and C1 in r; h(0+,z)=0;

       h(r,z)/(kappa(z) r^m)->1,
       h_r(r,z)/(m kappa(z) r^(m-1))->1.

4. Uniform comparison bounds hold for 0<r<r0:

       c0 kappa(z) r^m <= h(r,z) <= C0 kappa(z) r^m,
       h_r(r,z) >= c1 kappa(z) r^(m-1),

   for fixed c0,C0,c1>0.

Define the pushforward of b(r,z)r^alpha dr dlambda under ell=h(r,z), restricted to 0<r<r0. Then it has a density nu_local for ell>0, and

    lim_(ell->0) nu_local(ell)/ell^(beta-1)
       = (1/m) integral b0(z) kappa(z)^(-beta) dlambda(z).   (2.1)

If the displayed integral is positive, the limit is a positive finite coefficient and (2.1) is an asymptotic equivalence. Zero coefficient gives only o(ell^(beta-1)), not a positive universal law.

### Proof

For ell<h(r0,z), let R(ell,z) be the unique inverse radius. Extend the next integrand by zero for ell>=h(r0,z). The one-dimensional change-of-variables formula and Tonelli give

    nu_local(ell)=integral [R^alpha b(R,z)/h_r(R,z)] dlambda(z). (2.2)

For fixed z, R~(ell/kappa)^(1/m), so

    ell^(1-beta) R^alpha b(R,z)/h_r(R,z)
       -> b0(z) kappa(z)^(-beta)/m.

For domination, R is comparable to (ell/kappa)^(1/m) with constants independent of z. Moreover

    R^alpha/h_r <= c1^-1 kappa^-1 R^(alpha-m+1).

Since alpha-m+1=m(beta-1), the normalized expression is at most a constant times G(z)kappa(z)^(-beta). This is integrable by hypothesis2. Dominated convergence proves (2.1). QED.

## 3. The cumulative theorem needs less regularity

Assume the same intensity, envelope, monotonicity and two-sided h bounds, but omit differentiability and the h_r assumptions. Then

    N_local(ell):=mu_actual{0<h<=ell}
       ~ [1/(alpha+1)] ell^beta
          integral b0(z)kappa(z)^(-beta) dlambda(z),        (3.1)

provided the integral is positive.

Proof. Integrate r^alpha b(r,z) from0 to min(r0,R). For fixed z, the integral divided by R^(alpha+1) tends to b0(z)/(alpha+1), by an elementary rescaling on [0,1]. The upper bound is G(z)/(alpha+1) times (ell/(c0*kappa))^beta. Apply dominated convergence. QED.

A cumulative asymptotic cannot simply be differentiated without additional assumptions.

### Explicit density counterexample

Take alpha=1, m=3, a=p=kappa=1 and, for small r>0,

    h(r)=r^3 [1+r sin(1/r)].

Then h/r^3->1 and

    h'(r)=r^2[3-cos(1/r)+4r sin(1/r)]>0

for 0<r<1/4. The pushforward density satisfies

    nu(h(r)) h(r)^(1/3)
      = [1+r sin(1/r)]^(1/3) / [3-cos(1/r)+4r sin(1/r)].

Along r_n=1/(2*pi*n), it is exactly1/2. Along s_n=1/((2n+1)*pi), it is exactly1/4. There is no single density coefficient, even though h~r^3 and the cumulative law is N(ell)~ell^(2/3)/2. This disproves the unrestricted inference from ell~kappa r^m to a pointwise density asymptotic.

## 4. The small-mark transition: an exact solvable countermodel

On (r,kappa) in (0,1)^2, take

    dmu=r^alpha kappa^q dr dkappa,  alpha>-1, q>-1,
    ell=kappa r^m,  beta=(alpha+1)/m.

Exact change of variables yields

    nu(ell)=(ell^(beta-1)/m) integral_ell^1 kappa^(q-beta) dkappa. (4.1)

Writing delta=q+1-beta,

    delta!=0: nu(ell)=ell^(beta-1)(1-ell^delta)/(m*delta),
    delta=0:  nu(ell)=ell^(beta-1)log(1/ell)/m.              (4.2)

Thus

- q+1>beta: ordinary collision law, nu~ell^(beta-1)/(m*(q+1-beta));
- q+1=beta: logarithmic correction, nu=ell^(beta-1)log(1/ell)/m;
- q+1<beta: small-mark dominated, nu~ell^q/[m*(beta-q-1)].

The effective density exponent in this exact product model is min(beta-1,q), with a logarithm at equality. This is not asserted for arbitrary dependent models without corresponding hypotheses.

For alpha=1,m=3 the transition is q=-1/3. In particular q=-1/2 gives

    nu(ell)=2[ell^(-1/2)-ell^(-1/3)] ~ 2ell^(-1/2),

not ell^(-1/3), despite exactly cubic splitting for every pair. A universality claim must control the negative moment of kappa, not just the radial exponent.

## 5. Selection changes and error transfer

If a(r,z)->a0(z) but selection is rare, p(r,z)=r^gamma ptilde(r,z), gamma>=0, with ptilde->p0 and a suitable envelope, repeat Theorem2 with alpha replaced by alpha+gamma. The exponent is

    (alpha+gamma+1)/m - 1.                                 (5.1)

Consequently a positive limiting pairing probability preserves the collision exponent; a vanishing pairing probability may change it. A fixed-transverse witness-count bound does not prove the global pairing probability has the required behavior.

For an exact h=kappa r^m on a compact mark range 0<kmin<=kappa<=kmax, if

    b(r,z)=b0(z)+O(r^delta G(z)),

uniformly with an integrable envelope, then

    nu_local(ell)=C ell^(beta-1)+O(ell^(beta-1+delta/m)).     (5.2)

For unbounded marks, (5.2) needs the stronger negative moment of order beta+delta/m and cutoff-tail control. The first-moment assumption of Theorem2 alone does not give a rate.

In particular an actual all-failure selection estimate 1-p=O(r^3), on compact marks with m=3, affects the density at relative order O(ell). One chart's third-witness bound is not an all-failure estimate.

## 6. Other strata and nonlocal mechanisms

For finitely many positive local contributions nu_s~C_s ell^(beta_s-1), the smallest beta_s dominates; tied exponents add coefficients. Degenerate mark populations may add the logarithmic regimes in Section4. No cancellation can hide a positive more-singular contribution.

A complete persistence population also has nu_other. To transfer the local theorem to the global density one must show

    nu_other(ell)=o(ell^(beta-1)).

A bounded nonlocal density O(1) is lower order when beta<1. It is NOT negligible when beta=1 and may dominate when beta>1. Local collision scaling alone therefore does not classify the entire diagram.

## 7. Specialization and normalization ledger

For alpha=1, m=3 and positive limiting selection,

    nu_local(ell) ~ C ell^(-1/3),
    C=(1/3) integral a0(z)p0(z) kappa(z)^(-2/3) dlambda(z),
    N_local(ell) ~ (3/2)C ell^(2/3).

Here kappa is defined by ell=kappa r^3 at leading order. Some historical project files instead use kappa_old=6ell/r^3. In that convention replace kappa by kappa_old/6; the coefficient gains the factor 6^(2/3). The intensity and mark measure must be transformed consistently. We do not mix these conventions.

If a d-dimensional *typed, height-resolved* close-pair intensity has spatial density r^(2-d), multiplication by the radial shell r^(d-1) yields r dr and alpha=1. This is a conditional explanation for dimension cancellation; it is not a proof that all Gaussian persistence populations have that typed intensity or pairing limit.

## 8. What is now a theorem, and what remains a universality program

The marked transfer statement is a theorem under explicit hypotheses, with the proof above. The unrestricted original formulation is false without small-mark and derivative controls. The next research problem is to verify a common hypothesis package across different covariance kernels and pairing types: local fold order, typed pair-intensity exponent, mark integrability, actual-pair selection, and negligibility of other strata.

The simplex/Hessian result can assist the selection module by controlling specified third-witness populations, but it does not establish the other modules automatically. No universal Gaussian persistence theorem or worldwide novelty claim is made here.
