# Endpoint exponential-weight closure

Read [the complete conditional proof](PROOF.md) and [the exact inputs](SOURCES.json).
The packet combines Math-#157 MF1 with Math-#162's fixed-parameter coefficient
limit. Neither parent is accepted or promoted by this combination.

It proves convergence of the nonempty count intensity in the endpoint norm
sum exp(theta n^(2/d))|nu_r(n)-nu(n)|, removes the subsequence from #157's
weighted consequence, and gives an explicit uniform finite-time replica bound.
Positive conditioning retains that endpoint weight. Size bias requires a
strictly smaller exponent; an exact escaping-mass counterexample preserves
this boundary. The replica construction uses independent copies of the field.

The earlier polynomial and ordinary-TV consequences remain credited to the
input packets. No spatial independence, new Gaussian theorem, convergence
rate for coefficients, uniformity in moving marks, or numerical enclosure
is introduced. The unchanged proof now has actual scoped nonauthor
**ACCEPT, CONDITIONAL** dispositions for Slice A (§§1–3) and Slice B (§§4–5).
The [source-bound review record](REVIEW_RECORD.json) preserves the actual native
bodies, original commit, exact proof identity and exposure. These reviews
retain MF1 and SC(3) as imported premises; they do not accept the parents or
establish engineering merge readiness. Scientific effect NONE.

The three recorded reviews are [Claude A+B](https://github.com/d6g8k5htny-coder/Math-/pull/164#pullrequestreview-5360109371),
[Codex A](https://github.com/d6g8k5htny-coder/Math-/pull/164#pullrequestreview-5360144037),
and [Codex B](https://github.com/d6g8k5htny-coder/Math-/pull/164#pullrequestreview-5360159070),
all on original commit `0e70540b70e5e3183df5ed1a6bd70a212b734c9c` and
proof SHA256 `3f32fdd744350a15359451bbbee6c6bcc71af47e4f57f6110d7afb4978e941ee`.
They use the same GitHub account and carry zero organizational-independence
credit. The original author-side [validation history](VALIDATION.json) and
the dated original section of [internal challenges](INTERNAL_REVIEWS.md)
remain historical snapshots; their pending-review language is not the current
disposition.

## Bounded plan and verification

1. Bind the two existing interfaces at exact commit/path/blob/SHA256 identities.
2. Prove endpoint tail tightness and retain the failure of endpoint size bias.
3. Prove the weighted convolution and floor/Euler/intensity error ledger.
4. Run independent finite rational controls and deliberate wrong variants.
5. Preserve the completed source-bound reviews of §§1–3 and §§4–5, including
   exact original source exposure, in REVIEW_RECORD.json.
6. Publish on an isolated additive branch; require real source-tree verification
   and current-head hosted checks before any engineering integration.

From the repository root, run the commands used by the packet workflow:

```sh
packet=frontiers/cluster_exponential_weight_20260930
python -B -S "$packet/verify_packet.py"
python -B -O -S "$packet/verify_packet.py"
python -B -S "$packet/finite_checks.py"
python -B -O -S "$packet/finite_checks.py"
python -B -S -m unittest discover -s "$packet" -p 'test_*.py' -v
python -B -O -S -m unittest discover -s "$packet" -p 'test_*.py' -v
python -B -S "$packet/verify_sources.py" --repo-root .
```

The two finite-control outputs must be byte-identical; they establish finite
arithmetic only. The packet guard enforces exact file membership and recorded
byte counts, SHA256 and Git blobs, excluding the manifest itself. It separately
binds VALIDATION.json and REVIEW_RECORD.json to the unchanged PROOF.md.
This checks custody, not remote review authenticity or mathematical acceptance.
VALIDATION.json is a historical record, not finite_checks.py output. Historical
source verification requires both pinned Git objects in a complete checkout;
connector-acquired copies do not substitute for that historical-tree check.

Publication adds this packet and its isolated workflow only. Existing sources,
root indexes, live integration branches and scientific registers stay under
their own owners. Internal OpenAI challenge reviews carry zero organizational
independence and never self-accept the author's amendments.
