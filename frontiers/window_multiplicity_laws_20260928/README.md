# Window multiplicity and elder-loss laws — author-side proof packet

Author: OpenAI / ChatGPT, 28 September 2026. **Nonauthor analytic review required.**
Scientific effect: NONE. No existing proof, scientific verdict, graph, or prize
is changed. These are new written arguments, not accepted theorems by virtue of publication.

## Mathematical modules

| Read | Proposed result | Scope boundary |
|---|---|---|
| [Direct elder lower bound](ELDER_LOWER_AND_DENSITY_GAP.md) | Uniform planar `1-p_r >= c r^3` via an explicit path above the proposed death height to a point above birth. With the separately named parent upper/radial inputs: `Theta(r^3)` selection loss and `Theta(ell^(2/3))` compact-window density loss. | No numerical constant/cutoff, historical q/p substitution, or unrestricted-mark density-loss claim. |
| [Local multiplicity](LOCAL_MULTIPLICITY.md) | Two local window saddles occur with probability `Theta(r^3)`. Global conditional uniqueness and an `O(r^5)` global factorial extension are impossible. | Planar only; no global factorial upper bound. The count event alone is not an elder obstruction. |
| [Remote pair law](REMOTE_PAIR_LAW.md) | Exact positive leading `r^5` factorial coefficient, adjacent-index support, pair-weighted `Beta(2/3,2)` height-gap limit. | Both witnesses stay in a fixed remote region. Pair-mean weighting is not event-conditioned pair sampling. |
| [Distance moments](REMOTE_DISTANCE_MOMENTS.md) | Distance moment transition at `p=1`; two positive `r^6` contributions there. Scaled-distance limit has tail `R^-7`, yet its first moment does not capture rare macroscopic-pair contributions. | Fixed remote set. Total variation does not control unbounded moments. |
| [Single height mark](HEIGHT_MARKS.md) | Remote singleton location/index/height is `O(r)` in TV from the contact location/index profile times a uniform window height. | Uses the actual pre-height-integrated source kernel; not a persistence-partner law. |

The common local cubic is

    G_k(X,Z)=k(2X^3-3X/2-1/2-3Z^2/4-XZ^2).

Its extra saddles have height `-7k/32`. A rational polygonal path reaches
`+17k/64` while staying above `-7k/32`. Physical jet-box mass `r`, endpoint weight
`r^4`, and full normalizer `r^2` give a tilted event of order `r^3`. The whole-field
remainder is controlled AFTER conditioning on the rare physical jet box.

The remote overlap integral is

    integral_0^infinity s(k-s^3|t|)_+ ds = (3/10) k^(5/3)|t|^(-2/3).

It yields a contact Gaussian coefficient and an ordered pair-height density
`(5/9)|a-b|^(-1/3)`. The normalized gap has mean `1/4`, variance `9/176`, and
ordered heights have correlation `2/7`. These are pair-weighted critical-point
marks, not a new lifetime distribution.

## Source identities and an explicit code-publication limitation

[SOURCE_MAP.json](SOURCE_MAP.json) pins four consumed sources by repository,
40-character commit, bytes, SHA-256 and Git blob. The parallel singleton-law PR115
is context-only; elementary mixture identities are proved again where needed.
[SOURCE_FILES.json](SOURCE_FILES.json) enumerates every document in THIS public
packet. This directory is deliberately proof-and-provenance only.

The complete local delivery also contains `algebra.py`, `test_algebra.py`,
`run_validation.py`, a targeted workflow, manifests and original execution logs.
The GitHub connector blocked the attempt to create `algebra.py` with the message
that it could not determine the safety status. That body was not retried through
another path, encoding, or write route. No mathematical objection was supplied
by that tool response. The local tested code is included in the owner's separate
conversation evidence bundle, NOT claimed present in this repository packet.

Actual local execution: **30 tests in each of normal and optimized Python; 13
semantic mutants in each mode rejected on their exact intended assertions, with
no execution errors; baseline and mutant outputs identical between modes.**
Initial missing-implementation tests failed before implementation. The complete
local packet-only runner passed and source bytes remained unchanged. Separate
negative controls rejected a changed document, an unlisted member, duplicate JSON
keys, and a full-checkout replay with missing dependencies.

Those local facts are reported in [PUBLICATION.json](PUBLICATION.json). They are
not a claim that the code can be replayed from THIS GitHub directory. The four
full-checkout dependency bytes were not locally downloaded/replayed in the container;
source texts were read through the connector and exact identities pinned. No new
hosted mathematical runner is installed by this proof-only PR. Existing repository
CI, if it runs, remains separate and cannot prove the new analytic arguments.

## Review focus

Review the direct elder obstruction and rare-jet conditional moment argument
first. The upper selection theorem is an explicit separate input. Then review
the collision-conditioned determinant limits, fixed-Borel translation argument,
coefficient constants, beta pushforward, distance-moment diagonal estimate, and
`p=1` two-cutoff limit. The height-mark module has a smaller source-consumption
obligation. Each manuscript records its own dependencies and exclusions.

No nonauthor acknowledgment, provider independence, numerical Gaussian coefficient,
all-small-r numerical cutoff, global collision upper bound, higher factorial
moment, event-probability asymptotic from factorial means, Poisson limit, or priority
claim is invented. [RECONNAISSANCE.md](RECONNAISSANCE.md) records the limited external
search and distinguishes primary theorem reading from abstract-level discovery.
