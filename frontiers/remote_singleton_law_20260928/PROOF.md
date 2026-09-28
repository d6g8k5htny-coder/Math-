# Remote rare critical points: the single-point configuration law

Object: OA-D5-REMOTE-SINGLETON-LAW-20260928-v1.
Author: OpenAI / ChatGPT, foreground continuation.
Disposition: AUTHOR-SIDE COROLLARY; NONAUTHOR REVIEW REQUIRED.
Scientific effect: NONE. No governing status, proof index, graph, prize or source body is changed.

## 1. Intent and exact source dependencies

The fixed-remote mean and second factorial moment say more than that a window
critical point is rare: when one appears, its complete remote configuration is
usually a singleton, and its location/index distribution can be identified. This
note makes that consumption explicit. It proves an elementary general probability
lemma and applies only already specified fixed-remote estimates. It introduces no
new Gaussian covariance argument and no global witness-collision assertion.

Repository: `d6g8k5htny-coder/Math-`.

1. `frontiers/remote_window_20260924/PROOF.md`, Theorem A, read at commit
   `541d4e9daf3f2ca8b5a485d6e96ecf3dbf958f17`, blob
   `b383bfcc88ec4ad497dff01fb6640e429ba24a84`. This gives the uniform fixed-remote
   mean density expansion, not by itself a matching event-probability law.
2. `frontiers/remote_collision_20260928/PROOF.md`, Corollary D, v4 at commit
   `66437d90f3b7222256b2b8aed62400c42a78a08a`, 26,002 bytes, SHA-256
   `b9b8b58fd8266db7ffe6537078003888ef138b445d3289ec5588f116af9050c2`, blob
   `7b48a88e2af54e759e89a8c8219573bb450a65ea`. This gives the second factorial
   moment with BOTH witnesses in the same fixed remote region. OpenAI's
   source-exposed review 5343164624 of that source is not a review of this note.

The application below is conditional on the mathematical validity of these
precise inputs. Publication or merger is not an additional proof premise. The
exact generic lemma in Sections 2-4 is proved here. No earlier verdict is
inherited for the new application. Math-#107's planar global first moment is
NOT an input: the present statement is remote in every fixed d>=2.

## 2. A finite point-process lemma with an exact error identity

Let S be a standard Borel space. Give the space of finite counting measures on S
its counting-map sigma algebra. A point is represented by its unit mass delta_x;
the singleton embedding and its inverse on singleton configurations are
measurable. Multiplicities are allowed in this lemma.

Let Xi be a random finite counting measure, N=Xi(S), and

    mu(A)=E Xi(A),  m=mu(S)<=1,
    q=E[N(N-1)]<infinity,
    h=E[N; N>=2].                                      (S1)

Define Ber(mu) as a random counting measure: it is empty with probability 1-m,
and assigns singleton delta_x with subprobability measure mu(dx). When m>0 this
means sample a Bernoulli(m) indicator and, if nonempty, sample x from mu/m. For
m=0 it is the deterministic empty configuration. The condition m<=1 is necessary
for this definition; it is not silently replaced by min(m,1).

Use probability total variation

    dTV(P,Q)=sup_A |P(A)-Q(A)|=(1/2)||P-Q||_var,

where || ||_var is the full mass norm of a signed measure.

**Lemma 1 (exact identity).**

    dTV(Law Xi, Ber(mu)) = h <= q.                       (S2)

**Proof.** Define the singleton submeasure sigma on S by

    sigma(A)=P(N=1 and the unique point belongs to A),

and the nonnegative multiple-point mean measure eta by

    eta(A)=E[Xi(A); N>=2].

Then mu=sigma+eta, sigma(S)=s:=P(N=1), and eta(S)=h. Put
alpha=P(N>=2) and p=P(N>=1)=s+alpha. Thus m=s+h and
m-p=h-alpha>=0. On the three disjoint parts of configuration space:

- empty: Law Xi minus Ber(mu) has mass m-p=h-alpha;
- singletons: Ber(mu) minus Law Xi is the pushforward of eta, of mass h;
- configurations of size >=2: Law Xi minus Ber(mu) has mass alpha.

The full variation is (h-alpha)+h+alpha=2h, proving equality in (S2).
Finally n<=n(n-1) for integers n>=2 gives h<=q. This also shows all relevant
measures are finite. No point independence, stationarity, Poisson hypothesis,
Gaussian conditioning or pair-density formula is used. QED.

The constant one in h<=q is sharp: take Xi=delta_a+delta_b with probability
epsilon<=1/2, otherwise empty. Then m=h=q=2epsilon and dTV=2epsilon.
The points can coincide in the generic example; choosing distinct a,b gives a
simple-process example as well.

**Why a first moment alone is insufficient.** The same example with
epsilon=r^3/2 has m=r^3 but dTV=r^3, not O(r^5). The factorial input is essential
to the stronger approximation asserted below.

## 3. Conditional laws and single-witness location

Suppose m>0. Necessarily p>0 since Xi is nonnegative. Denote by Delta(nu) the law
of a singleton at an S-valued point with probability distribution nu.

**Lemma 2.**

    dTV(Law(Xi | N>=1), Delta(mu/m)) <= h/m <= q/m.       (S3)

If s=P(N=1)>0, then also

    dTV(Law(unique point | N=1), mu/m) <= h/m.           (S4)

**Proof.** The common submeasure Delta(sigma/m) is dominated by both laws in
(S3). In the first law the singleton part is Delta(sigma/p), and p<=m; in the
second it is Delta((sigma+eta)/m). Its total mass is s/m, so the probability-TV
distance is at most 1-s/m=h/m. This domination argument proves the claim for
arbitrary measurable configuration events, not just events determined by N.
For (S4), write mu/m=(s/m)(sigma/s)+eta/m; the usual mixture difference has
TV at most h/m. This argument identifies the unique point, not an arbitrary
selection rule from a configuration with several points. QED.

The elementary count inequalities also give

    0<=m-p=E[(N-1);N>=2]<=q/2,
    P(N>=2 | N>=1)<=q/(2p),
    s=m-h>=m-q.                                        (S5)

The factors 1/2 arise from 1<=n(n-1)/2 and n-1<=n(n-1)/2 for n>=2. Thus
q=o(m) ensures both a positive singleton event and conditional uniqueness with
probability tending to one. All these claims count multiplicity, not merely
distinct occupied sites.

## 4. Replacing the exact mean measure by a leading approximation

Let mu_0 be another nonnegative measure with 0<m_0=mu_0(S)<=1. Set
D=||mu-mu_0||_var. Disjoint empty and singleton parts yield the exact formula

    dTV(Ber(mu),Ber(mu_0))=(|m-m_0|+D)/2 <= D.           (S6)

For m,m_0>0, direct normalization gives

    dTV(mu/m,mu_0/m_0)<=D/m.                            (S7)

Indeed mu/m-mu_0/m_0=(mu-mu_0)/m+mu_0(1/m-1/m_0), whose variation mass is at
most (D+|m-m_0|)/m<=2D/m. Combining with (S2)-(S4),

    dTV(Law Xi,Ber(mu_0)) <= q+D,
    dTV(Law(Xi|N>=1),Delta(mu_0/m_0)) <= (q+D)/m.        (S8)

The unique-point version has the same upper bound when s>0. These bounds retain
the normalization denominator. An absolute O(r^4) mean error becomes O(r)
after conditioning on an event of order r^3; it does not remain O(r^4).

## 5. Exact Gaussian application, keeping the remote scope

Use exactly the normalized periodized field and original endpoint law in the
source Theorem A. In particular d>=2, L and 0<rho<L/4 are fixed, marks b lie in
a fixed compact interval, 0<k_-<=k<=k_+, frames range over O(d), and

    M=-(r/2)u, S=(r/2)u,
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0,
    W_r=F_d(H_M)F_(d-1)(H_S), Z_r=E_Qr W_r,
    dQ_r^W=(W_r/Z_r)dQ_r.

Q_r has the original 2(d+1) observations (six only when d=2). No adjacency
condition, second normalizer, or endpoint Jacobian is introduced. The law Q_r^W
need not be Gaussian; Lemmas 1-2 apply to any probability law.

Let E be a deterministic Borel subset of D_rho={dist(x,0)>=rho}. Define Xi_r on
S_E=E x {0,...,d} by placing one atom (x,j) at each nonsingular index-j critical
point with height in I_r=(b-k r^3,b). Thus N_r=Xi_r(S_E) is the TOTAL window count
on E. Positions and indices are joint marks; their independence is not assumed.
The height is restricted and then discarded as a mark. This note makes no claim
about the height's conditional distribution.

The mean input and factorial input, summing finitely many indices where needed,
are

    mu_r(dx,{j}) = [k r^3 Lambda_j(x;b,k,u)+e_(r,j)(x)] dx,
    |e_(r,j)(x)| <= C r^4 almost everywhere,
    q_r:=E_(Q_r^W)[N_r(N_r-1)] <= C r^5 |E|.            (S9)

Theorem A already states the mean-density formulation. Alternatively its error
bound for every Borel set implies absolute continuity and the stated a.e. density
bound. Do not infer that statement from a single value of E. The factorial
estimate is Corollary D, including its uniform-in-E absorption of the separated
Cr^6|E|^2 term using finite torus volume and bounded small r.

Put

    Lambda(x,j)=Lambda_j(x;b,k,u),
    A_E=sum_j integral_E Lambda_j(x;b,k,u) dx,
    mu_(0,r)(dx,{j})=k r^3 Lambda_j(x;b,k,u) dx.

The fixed-remote Lambda_j are continuous, uniformly positive and bounded on the
source's compact parameter ranges. Consequently for |E|>0 and sufficiently small
r, uniformly over these deterministic E,

    c r^3 |E| <= m_r=mu_r(S_E) <= C r^3 |E| <=1,
    D_r:=||mu_r-mu_(0,r)||_var <= C r^4 |E|,
    q_r/m_r <= C r^2.                                  (S10)

The cutoff ensuring m_r<=1 uses |E|<=L^d and is uniform in E. Reducing it further
gives q_r<m_r and m_(0,r)<=1. For |E|=0 the source mean is zero, so Xi_r is empty
a.s.; the conditional assertions are deliberately not made in that case.

**Corollary 3 (complete remote configuration).**

    dTV(Law_(Q_r^W) Xi_r,Ber(mu_r)) <= C r^5 |E|,
    dTV(Law_(Q_r^W) Xi_r,Ber(mu_(0,r))) <= C r^4 |E|.    (S11)

The first is a complete-configuration approximation at the exact mean; the second
uses the explicit leading contact intensity. Neither assumes point independence.

**Corollary 4 (location/index given a rare occurrence).** For |E|>0 define

    nu_E(dx,{j}) = Lambda_j(x;b,k,u) dx / A_E.

Then

    Q_r^W(N_r=1 | N_r>=1) >= 1-C r^2,
    dTV(Law(Xi_r | N_r>=1),Delta(mu_r/m_r)) <= C r^2,
    dTV(Law(Xi_r | N_r>=1),Delta(nu_E)) <= C r.          (S12)

The distribution of the unique point conditional on N_r=1 obeys the same Cr
bound to nu_E. Equations (S11)-(S12) follow directly from (S2)-(S10), and their
constants have exactly the fixed d,L,rho and compact-mark dependencies of the
inputs. Conditional uniqueness uses p_r>=m_r-q_r/2 and q_r/m_r=O(r^2).

These bounds hold uniformly even for positive-volume deterministic E=E_r shrinking
inside the SAME D_rho, since |E| cancels from (S10). They do not permit a random
region chosen from the realized field, or rho=rho(r) tending to zero.

The joint density nu_E need not factor into an independent spatial law and index
law. Restricting to one chosen index gives its corresponding single-type version;
it is not necessary to pretend that several indices occur independently.

## 6. What this contributes and what remains open

The new output is a usable rare-event configuration and conditional spatial/index
law, obtained from source-bound mean and pair estimates. It can compare a sampled
remote witness distribution with the normalized contact profile; it cannot certify
an elder-pairing law or the location of a globally selected persistence partner.

It does not prove a torus-wide second factorial moment, control pairs with either
witness near the pins or at intermediate distances, remove the height window,
produce numerical constants, change any governing status, or prove a nondegenerate
Poisson limit. Ber(mu_r) itself tends to the empty configuration; (S12), obtained
after conditioning on a rare occurrence, is the nontrivial spatial statement.
No Poisson approximation theorem is imported or needed here.

No mathematical proof is inferred from test counts. Sections 2-4 provide complete
measure-theoretic proofs of the probability statements; Section 5 spells out
exactly which analytic inputs are still required from the Gaussian sources.
Nonauthor review should check the TV convention, empty/single/multiple signed
measure split, normalization factors, arbitrary-Borel mean-error implication,
index marking, and fixed-remote versus global boundaries.

## 7. Finite controls and limited reconnaissance

The standard-library test suite computes exact rational probability laws on two
atoms with up to three-point configurations, retaining multiplicities. It checks
(S2)-(S8), sharpness, invalid mean>1 and zero conditioning events, the failure of
first-moment-only inference, and an explicit r-dependent family with r^3 mean,
r^5 factorial moment and r-sized leading conditional correction. Deliberate
mutations distinguish h from P(N>=2), mean from event probability, and TV from
the full variation norm. None of this tests Gaussian field simulation or infinite
configuration spaces.

Consensus discovery query in this session concerned total variation, factorial
moments and rare single-point processes. A fetched record was Breton--Privault,
*Factorial moments of point processes*, Stochastic Processes and their Applications
124, 3412-3428 (record lists 2013). The fetch supplied metadata only, not an abstract
or theorem. No result from it is consumed. This note's generic probability proof
is elementary, and no novelty or priority claim is made for it. The contribution
claimed here is the explicit, correctly scoped application to the project's remote
critical-point inputs, not invention of Bernoulli approximations.
