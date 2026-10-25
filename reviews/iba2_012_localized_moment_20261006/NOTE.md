# IBA2-012 addendum: localize before taking the count moment

Object: IBA2-012-LOCALIZED-MOMENT-20261006-v1.
Author: OpenAI / GPT-6 Astra Pro, `iba2-count-weight-transfer-r6-20261006`,
for Dylan Roy — delegated AI work. Source-exposed; organizational credit0;
scientific effect NONE. **Conditional author-side addendum; delta review required.**

## 1. Parent, scope and provenance reconciliation

The count-transfer theorem, shrinking-sector negligibility and the all-fixed-order
obstruction to loss-free transfer are ALREADY recorded by merged Math-#319. They
are not new claims of this addendum. Its canonical five-file packet remains
unchanged. This note extracts only a useful input reduction and a fixed-order
sharpness result from the conflicting #324 draft at af85f05fdfcb810e0973e829d838ecb35946390a.
That draft and its review6007975992 remain historical evidence, not a replacement
for #319 and not an independent second discovery of its core theorem.

Read these exact sources at cut `75ce4eab431e487a163cc4ebb30c5d2386a0e887`:

| Tag | Path | Full Git blob | Slice |
|---|---|---|---|
| CT | `reviews/iba2_012_count_transfer_20261006/PROOF.md` | `752bc9da5e49af3d0724d80c91cffc0dde35a2d8` | Entire parent; especially first-moment input in sections2–3, scope/denominators and section6 obstruction |
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | Sections3–5/8, finite-r derivative-weighted event bounds |
| CP | `frontiers/c6_palm_route_20260929/PROOF.md` | `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` | Sections1.1–1.3, one fixed-order instance of Theorem Q and all inherited qualifications |
| ERR | `reviews/d5_dimension_lift_erratum_20261005/ERRATUM.md` | `23df87bbe4ffd3b2d786cd695fb9f5448cfa1d05` | Entire additive correction, read with unchanged originals |

Removing an independently consumed first-moment input at this transfer step does
NOT remove DL from CP's own proof ancestry, resolve an ancestor review gap, or
prove the field count bounds independently. All field applications remain
conditional on the stated source interfaces. No old proof or status is revised.

## 2. One factorial order is enough after event localization

Work on one probability space with N a nonnegative integer-valued count, K>=1,
a measurable event E, a small scale rho>0 and 0<Xi<=C0. Fix a>=0, 0<p<m and an
integer m>=2. Put theta=1-p/m. Assume only

    E[(N)_m] <= B_m rho,
    E[K^t 1_E] <= A_t rho Xi   for t=0 and t=a/theta.       (L-input)

Constants are independent of rho and Xi in the stated parameter range. Then

    E[K^a N^p 1_E]
       <= [m^m(A_0 C0+B_m)]^(p/m) A_(a/theta)^theta
          rho Xi^theta.                                  (L)

**Proof.** For every integer n>=0,

    n^m <= m^m[1+(n)_m].                                  (1)

For n<m the constant suffices. For n>=m each of the m factors n-i is at least
n/m, since n-m+1>=n/m. Thus (n)_m>=(n/m)^m. Apply (1) only on E:

    E[N^m 1_E] <= m^m(P(E)+E[(N)_m])
                <= m^m(A_0 C0+B_m)rho.                    (2)

Finite mth factorial moment also excludes N=infinity, or one may start with
truncations. Holder on this same probability measure gives

    E[K^a N^p 1_E]
      <= (E[N^m 1_E])^(p/m)
         (E[K^(a/theta) 1_E])^theta.                      (3)

Insert the two bounds. The exponents of rho add to p/m+theta=1, proving (L).
No independence of N,K,E is used. The indicator belongs in BOTH finite moments.
The term1 in (1) cannot be removed: n=1 annihilates every factorial order m>=2.

A global first moment is genuinely not forced by L-input. Abstractly, let N=1
almost surely, K=1 and P(E)=rho Xi with rho Xi<=1. Then all m>=2 factorial moments
are0 and the localized assumptions hold, but E[N]=1 is not O(rho). This is not a
Gaussian-field counterexample. It shows why replacing (2) by an unproved global
O(rho) ordinary moment would impose an unnecessary additional premise.

## 3. Apply the lemma without changing the parent theorem's meaning

Use FR and CP on their SAME full-normalizer tilted pin law P_r=Q_r^W. Keep fixed
d>=3,L>0, observation radius R>=1, compact birth heights and strictly positive
compact gap marks, exactly as in CT and FR. Let N be the torus-wide between-pin
count, N_R its local subcount, and K FR's C4 control. For 1<=q<=d-2 set

    S = {h_j<=eta_j for j=2,...,q+1},
    E = {N_R>0} intersect S,
    Xi = product_(j=2..q+1)(eta_j+r)^(j+2).

The h_j are FR's ordered midpoint transverse eigenvalues. For ordered thresholds
0<=eta_2<=...<=eta_(q+1)<=1 and r<=1, Xi<=2^beta, beta=q(q+7)/2. FR-mixed supplies
the two event bounds in L-input with rho=r^3; one chosen instance of CP Theorem Q
supplies the factorial bound. Consequently

    E[K^a N^p 1_E] <= C r^3 Xi^(1-p/m),
    E[K^a N_R^p 1_S] <= C r^3 Xi^(1-p/m).                 (4)

The second line uses p>0 and N_R^p 1_S=N_R^p 1_E<=N^p 1_E. For p=0 keep the
nonempty event and use FR directly. Remote-only outcomes with N_R=0 are not
controlled by removing E from the first line. No additional normalization is
performed and no K under CP's witness regression is identified with FR's K.

This obtains the parent's count-transfer CONCLUSION using a narrower list of
explicit inputs at this inference step: one factorial order and two FR moment
orders. It does not require every factorial order or separately insert DL's first
moment. To make the exponent loss arbitrarily small, more fixed orders still need
to be available; constants are not uniform in m and m cannot vary with r here.

The same arguments include zero thresholds and the all-soft transverse case.
On thresholds eta_j=r^alpha_j ordered with alpha_2>=...>=alpha_(q+1)>0, (4) has
order r^[3+(1-p/m) sum_(j=2..q+1)(j+2)min(alpha_j,1)], hence o(r^3). This is a
restatement of the parent's scaling at the reduced input interface, not a second
sector closure. No new radial lifetime integration or all-mark conclusion follows.

## 4. The fixed-order exponent is sharp from these inputs

Fix an integer m>=2 and real 0<p<m. In the abstract d=3,q=1 case, let
r_n=2^(-mn), K=1. An ordinary atom has mass r_n^3, N_R=N=2,h_2=2; a rare atom has
mass r_n^7,N_R=N=2^(4n),h_2=r_n; the remaining mass has count0. Set h_1=r_n/2.
The probabilities sum to less than1 for n>=1.

For every eta in [0,1], E={N_R>0,h_2<=eta} is empty if eta<r_n and is the rare
atom otherwise. Thus E[K^t;E]<=r_n^3(eta+r_n)^4 for every t>=0. Also

    E[(N)_m] <= E[N^m] = (2^m+1)r_n^3.

At eta=r_n,

    E[N^p;E] = r_n^7 2^(4np)
              = r_n^3 r_n^[4(1-p/m)],
    Xi = (2r_n)^4.                                     (5)

The ratio to r_n^3 Xi^(1-p/m) is the nonzero constant16^[-(1-p/m)]. For any
larger Xi exponent, the ratio is unbounded as n increases. This proves sharpness
of 1-p/m from the listed single-order inputs. It is NOT a lower bound for the
actual Gaussian field. The next ordinary moment obeys

    E[N^(m+1)]/r_n^3 = 2^(m+1)+2^(4n),

so this family does not supply all higher O(r^3) moments. The parent's section6
already supplies the DIFFERENT all-fixed-orders obstruction to loss-free transfer;
that result is credited and not recopied here. The ordinary-atom constant in the
last display additively corrects its omission in review6007975992's discussion of
the first draft. Divergence and the reviewed sector identity were unaffected.

## 5. Positional tuple measures: a small consequence, not a convergence theorem

For a fixed integer s>=1, (N_R)_s<=N_R^s. Let nu_(r,s) be r^-3 times the expected
positive measure of ordered s-tuples of distinct local window points, with any
measurable location or rescaled-location coordinates. Let nu_(r,s)^keep delete
configurations in S. Their difference is a positive measure, and

    ||nu_(r,s)-nu_(r,s)^keep||_variation
      = r^-3 E[(N_R)_s 1_S] <= C Xi^(1-s/m), m>s,m>=2.   (6)

These measures are finite at each r by (1) and a fixed CP moment; no uniform global
first moment is needed merely for finiteness. The variation convention is total
mass of a positive measure, not half-L1 for probabilities. Signed tuple functions
bounded by K^a obey the corresponding absolute upper bound from (4).

This only controls deleted-sector mass. It provides no full point-process limit,
location law, correlation density, elder matching or rate for the remaining
measure. Conditional-on-local-occurrence or factorial Palm normalization still
needs its own positive lower denominator; none is inserted here.

## 6. Verification, exact preservation and remaining obligations

The supplied test_count_transfer.py is EXACTLY blob629ba742ee777e7da992cf0a975cb7384ad1763f
from the first draft, not a rewritten suite. The actual xAI/Grok4.7 reader of that
head ran its13methods in both Python3.12.3 modes, all passing; M1–M4 gave intended
assertion failures, no test errors, and unknown labels exited2. Baseline stdout
SHA256 d8a2efa940de518122ee6037ebf15c35f3908fb5264472351d3aa4936f69e425.
That is reviewer's execution, not local author execution. The single-order model
was separately checked algebraically in the same written review. The author's
execution tools remain unavailable before command startup.

Those tests cover finite algebra, not arbitrary probability spaces or source
validity. A changed-source delta read must check this note against the reviewed
draft sections3,5.1,4.2 and canonical CT. Do not transfer the old whole-text verdict
automatically. All five canonical CT files, FR, CP, ERR and scientific records must
remain byte-identical. General IBA2-012/IBA2-009, loss-free conditional sector
moments, escaping marks, growing R, actual moment-law construction and full formal
alignment remain open outside this additive scope.
