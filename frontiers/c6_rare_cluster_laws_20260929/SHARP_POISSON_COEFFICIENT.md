# Addendum: the optimal Poisson error coefficient and the cost of mean matching

**Object:** OA-C6-RARE-CLUSTER-20260929-A1. **Author:** OpenAI / ChatGPT, 29 September 2026.
**Disposition:** author-side conditional candidate, nonauthor review OPEN. Scientific effect NONE. This is an additive sharpening of PROOF.md Section 3, not a rewrite of that file or of a source. It imports the definitions and H1/H2 interface of PROOF.md; Hq is used only for the subsequential statement below.

## 1. A universal finite-r inequality

For ANY nonnegative integer-valued random variable N with finite mean, write

    p=P(N>0), beta=P(N>=2), mu=E N, h=E[N; N>=2].

No Gaussian hypothesis is needed for the following inequalities:

    beta-2p^2 <= inf_{lambda>=0} dTV(Law N,Pois(lambda)) <= beta+p^2. (A1)

The infimum upper bound is achieved as a bound by the trial rate lambda=p; this does not assert that p is an exact minimizing rate.

**Proof.** The occurrence-matched Bernoulli(p) distribution has the same zero mass as N, exceeds N's singleton mass by beta, and has no multiple counts. Hence their TV distance is beta. Triangle inequality and dTV(Bern(p),Pois(p))=p(1-exp(-p))<=p^2 prove the upper bound.

For the lower bound split ALL rates, not only near-minimizers. If lambda<=2p, testing {n>=2} gives

    dTV >= beta-P(Pois(lambda)>=2) >= beta-lambda^2/2 >= beta-2p^2.

If lambda>2p, testing {n>0} and 1-exp(-x)>=x-x^2/2 gives

    dTV >= 1-exp(-lambda)-p >= p-2p^2 >= beta-2p^2.

These inequalities remain valid when the displayed lower bound is negative. They also handle p=0: the infimum is zero, attained at lambda=0. This proves (A1).

## 2. Mean matching has a different leading coefficient

Whenever mu<=1, the Bernoulli(mu) law is defined and

    dTV(Law N,Bern(mu)) = h,
    |dTV(Law N,Pois(mu))-h| <= mu^2.                              (A2)

**Proof.** Since mu>=p, the difference Law N minus Bern(mu) has mass mu-p on zero, mass -h on one, and positive total mass beta on counts >=2. The identity h=mu-p+beta makes its full variation 2h. Applying the reverse triangle inequality and dTV(Bern(mu),Pois(mu))<=mu^2 proves (A2). The Bernoulli identity is the count version of the earlier in-project [LOCAL, Section 7] identity; only its Poisson comparison is added here.

Under H1/H2, p,mu<=A r^3 and beta>=a r^3, so (A1) and (A2) imply

    inf_lambda dTV(Law N_r,Pois(lambda)) = beta_r + O(r^6),
    dTV(Law N_r,Pois(mu_r)) = h_r + O(r^6).                       (A3)

The first remainder is between -2A^2 r^6 and A^2 r^6; the second has absolute value at most A^2 r^6. Since h>=2beta, for sufficiently small r the denominator below is positive and

    dTV(Law N_r,Pois(mu_r)) / inf_lambda dTV(Law N_r,Pois(lambda))
       >= 2 - 3 A^2 r^3/a.                                      (A4)

Indeed use numerator >=2beta-mu^2, denominator <=beta+p^2, and subtract 2. Thus the liminf ratio is at least two. This is a statement about TV fit: it does not say that discarding mean matching is appropriate for tasks whose objective is preserving the mean. The canonical compound law of PROOF Section 4 matches the mean and is more accurate, but still requires the unknown full conditional mark law.

## 3. Limiting rate interval along the weighted-l1 subsequences

Along a subsequence of PROOF Theorem S let nu_r->nu, lambda_*=sum_{n>=1}nu(n), b_*=sum_{n>=2}nu(n), and v_1=nu(1). For EACH fixed c>=0,

    r^-3 dTV(Law N_r,Pois(c r^3))
        -> ( |lambda_*-c| + |v_1-c| + b_* )/2.                   (A5)

To prove this, use the exact signed expansion (6.2) and

    Pois(c e) = delta_0 + c e (delta_1-delta_0) + O_TV(e^2),

where e=r^3 and c is fixed. The latter follows by comparison with Bern(c e) for sufficiently small e. Full l1 convergence in (6.1) then gives (A5), with the TV factor 1/2 retained.

The minimum of the right side is b_* and its minimizing interval is

    v_1 <= c <= lambda_*.                                       (A6)

This follows directly from |lambda_*-c|+|v_1-c|>=lambda_*-v_1=b_*. Equations (A1) and (6.1) independently justify passing to the optimized leading error; no unjustified interchange of infimum and pointwise limit is used. The limiting mean coefficient is m_*=sum n nu(n), which exceeds lambda_* when b_*>0. Its error coefficient is sum_{n>=2}n nu(n), not b_*. Under H2, b_*>=a>0, so the mean-matched coefficient is at least twice the optimal one.

No unique nu, numerical coefficient for the Gaussian field, or convergence rate of nu_r is established. The assertion is uniform finite-r bounds plus a conditional subsequence characterization. Review requested particularly on the all-lambda split, the signs in (A2), and the infimum/limit distinction in (A5)–(A6).
