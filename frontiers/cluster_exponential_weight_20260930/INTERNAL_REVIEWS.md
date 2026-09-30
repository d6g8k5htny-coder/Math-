# Internal challenges, exposure and unresolved review

Target in both mathematical slices: PROOF.md, 12576 bytes, Git blob
`bf1268b9c18ec05561fd9b14c645ef0b8e530484`, SHA256
`3f32fdd744350a15359451bbbee6c6bcc71af47e4f57f6110d7afb4978e941ee`.
The target was not amended after either mathematical review.

Root authored the proof. The two OpenAI agents below made no proof edits and
were noncontributors to this implication; both had the root's draft and source
copies as exposure. Same-provider work supplies **zero organizational
independence**. Exact model version was not independently verified. These are
internal challenge results, not external organizational review or acceptance
of either upstream theorem. Public nonauthor review of this packet remains
required; its disposition is AUTHOR_SIDE / CONDITIONAL.

## Slice A: endpoint tails and normalization (agent exp_weight_tail_review)

**ACCEPT — §§1–3, conditional on MF1 and SC(3). No amendment required.**

The declared input interfaces agree: original variance-one periodized field,
endpoint regression, typed determinant weight, full endpoint-only normalizer,
and all-index additional count in the open height window with both pins
excluded. Setting T=L resolves the side-length notation. A fixed admissible
positive gap lies inside a compact family with positive gap floor. No extra
conditioning or size bias enters E1–E2.

E1 gives sum n w(n)nu_r(n)<=C; retaining n yields the endpoint tail
sum_(n>M)w(n)nu_r(n)<=C/(M+1). Fatou gives the same bound for the limit.
Finite-coordinate convergence then proves EW1 at theta itself. Since w>=1,
a_r->a>0. Centering at zero gives E4; positive conditioning correctly uses
the denominator a_r. For q and theta'<theta, the factor
n^(q-1)exp(-(theta-theta')n^alpha) tends to zero. This proves EW2 and the
size-biased passage with the different denominator nu1+2nu2.

E9 defines genuine probability laws for sufficiently small r, satisfies E1–E2,
and has endpoint intensity error exactly 1/m. Its size-biased escaping mass
has endpoint weighted value tending to 1/3. Thus the stronger endpoint
size-bias conclusion is false. Dropping the retained n defeats the tail
argument; changing the full tilt or count breaks interface compatibility.

## Slice B: weighted convolution and replica bound (agent exp_weight_replica_review)

**ACCEPT — §§4–5 with §6 scope limits, conditional on the inputs.**

For 0<alpha<=1, w(n+k)<=w(n)w(k). Absolute summation proves E11;
weighted l1 is a complete unital commutative convolution algebra. E5 implies
||nu_r||_w<=C and a_r<=C, hence ||H_r||_w<=B=2C; the same holds for H.
The exponential remainder is at most delta² B² exp(delta B)/2.
Telescoping m factors contributes at most
m delta² B² exp(m delta B)/2 <= t delta B² exp(tB)/2.
The exponential derivative identity E15 is valid in the algebra and gives
the stated Lipschitz constant. Flooring costs at most delta B exp(tB), and
replacing H_r by H costs at most 2t epsilon_r exp(tB). These give E12.

For s>=0, exp(-s a_r) sum_j s^j nu_r^{*j}/j! is nonnegative with mass one;
the comparisons therefore use genuine compound-Poisson laws. Independence
supplies the convolution power of the one-copy law. m=0, t=0 and T=0 are
handled. For alpha=1, absolute weighted convergence controls PGFs uniformly
on the closed disk of radius exp(theta), with analyticity in the interior
and continuity at the boundary. For alpha<1, the proposed
n^-3 exp(-2theta n^alpha) contamination obeys the premise but yields
prelimit radius exactly one. No larger disk follows.

Excluded stronger claims have concrete falsifiers: all replicas equal to
the same N_r defeats the compound-Poisson limit; a coefficient perturbation
1/|log r| defeats an automatic O(r³) replica rate and O(r6) one-copy
limiting-mark error; alpha>1 defeats E11 using two unit atoms.

Custody caveat at the first read: SOURCES.json was not yet present and the
historical Git objects were unavailable locally. The root later supplied
SOURCES.json and separately verified the source identities through the
public GitHub connector. This is not attributed to the first reviewer as
a historical-tree replay.

## Custody challenge, repair and separate re-review (agent exp_weight_tail_review)

Initial verifier SHA256 `45bddfbdd3e4c8b9cf5dd7311f46db870856f28c93c3d6a2bbbf9d4a3ecc78bb`:
**AMEND**. Eight controls passed, but a tree could masquerade as a commit,
and local Git replacement refs could make absent paths pass under an empty
commit's identity. A boolean JSON schema also passed as integer 1.

Root reproduced all three defects with failing tests before repair. Every
Git read now uses --no-replace-objects; cat-file requires object type commit;
schema requires an actual integer. Repaired verifier SHA256
`0bc355e6b5bc4459d5395f1730456bca8bb26aa6220f94e657f6dd57f93d7784`:
**PASS — bounded custody re-review**, 11 controls in each Python mode.
The real manifest correctly fails locally when historical objects are absent.
This repair concerns custody code only, not a proof amendment or parent verdict.
