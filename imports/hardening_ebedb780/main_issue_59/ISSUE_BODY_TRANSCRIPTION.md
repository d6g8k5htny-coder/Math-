# Archival transcription — main issue 59

This file is a transcription of a GitHub issue body. It is not a git blob, not a Drive download, and not the original bytes. The span between the begin and end markers is the REST API `body` field exactly, including its lack of a trailing newline. The header, the markers, and the comment identities were added here and are not part of that body.

| Field | Value |
|---|---|
| Repository | `d6g8k5htny-coder/main` |
| Issue | 59 |
| Title | P15: exact matroid palette specialization and optimal 816-label six-block witness |
| HTML URL | https://github.com/d6g8k5htny-coder/main/issues/59 |
| API URL | https://api.github.com/repos/d6g8k5htny-coder/main/issues/59 |
| Issue id | 5569087824 |
| Node id | I_kwDOQpeC2s8AAAABS_GJUA |
| State | closed |
| State reason | completed |
| Author | d6g8k5htny-coder |
| Closed at | 2026-09-25T12:30:12Z |
| Updated at | 2026-09-25T12:30:12Z |
| Body characters | 4686 |
| Body UTF-8 bytes | 4692 |
| Body SHA256 | `a1ef86f92c3d236c3190f78a1e1f3b68df599860c376c0a4e151d50de78ded87` |
| Retrieved | 2026-09-26 from the GitHub REST API issues resource above |

Comment identities are listed so the closing comment can be found. Comment text is not part of the proof span.

| Role | Comment id | Node id | URL | Created at | Author |
|---|---:|---|---|---|---|
| comment | 5815779899 | `IC_kwDOQpeC2s8AAAABWqXCOw` | https://github.com/d6g8k5htny-coder/main/issues/59#issuecomment-5815779899 | 2026-09-24T14:12:29Z | d6g8k5htny-coder |
| comment | 5819456999 | `IC_kwDOQpeC2s8AAAABWt3d5w` | https://github.com/d6g8k5htny-coder/main/issues/59#issuecomment-5819456999 | 2026-09-24T18:04:27Z | d6g8k5htny-coder |
| closing comment | 5832385281 | `IC_kwDOQpeC2s8AAAABW6MjAQ` | https://github.com/d6g8k5htny-coder/main/issues/59#issuecomment-5832385281 | 2026-09-25T12:30:10Z | d6g8k5htny-coder |

Scientific effect: NONE. This transcription does not accept the matroid-specialization argument, close a prize, or change `lemma_closed`, premises, or `claims/LANDING_CLAIMS.json`.

----- BEGIN GITHUB ISSUE BODY -----
## Separate combinatorics continuation — OpenAI / ChatGPT, author-side

This extends the existing P15-PALETTE-OPTIMIZER-20260924-v1 rather than rebuilding its general DP or single-edge formula. It is mathematically separate from the SIDE24 work in #58. No unrestricted prize closure or novelty of matroid coloring is claimed.

### Exact additional structure

P15-B requires palettes P_i of sizes at least d_i such that every crossing minimal original witness has block support e with intersection_{i in e}P_i empty. The complete support hypergraph's independent sets determine allowed color incidences.

If these independent sets form a LOOPLESS MATROID M, the new source-bound application gives

K*=max_{nonempty A subset[n]} ceil(sum_{i in A}d_i/rank_M(A)).

Each color contributes at most rank(A) incidences in A, giving the lower bound. Replace each i by d_i parallel COLOR-DEMAND copies. For every copy subset U, |U|<=d(supp U)<=K rank_M(supp U). Edmonds' classical partition theorem yields K independent classes and therefore palettes of the required distinct labels. These copies do not clone the original random coordinates or introduce probabilistic independence.

Primary theorem: Jack Edmonds, Minimum Partition of a Matroid Into Independent Subsets, J.Res.NBS69B(1965), Theorem1, printedp69. The PDF and theorem page were inspected: https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p67_A1b.pdf . This is established mathematics explicitly reused, not a new theorem attributed to our project.

A maximizing subset A supplies exact dual weights y_i=1/rank(A) on A, zero elsewhere. The fractional palette optimum is the maximum ratio R; the integral optimum is ceil(R). This integer-rounding property is not asserted for general hypergraphs.

### Uniform-rank construction, with no large-demand enumeration

If ALL (rank+1)-subsets are crossing supports, then

K*=max(max_i d_i,ceil(sum_i d_i/rank)).

Consecutive demand segments in the cyclic sequence 0,...,K-1 give a direct integral coloring. Each block uses distinct labels because d_i<=K; each label occurs in at most ceil(sum d_i/K)<=rank blocks. The implementation outputs at most2n+1compressed constant-incidence intervals.

For six blocks of demand408 and all15four-block crossing supports, K*=816. A complete witness is408labels on{0,2,4}and408other labels on{1,3,5}; the full-set rank lower bound is2448/3=816. Pairwise-disjoint palettes would use2448. Under ACTUAL compatible local408-demand covers and complete crossing-support identification, P15-B transfers this to its816-color hazard/obstruction-cover conclusion. The code does not prove those application hypotheses.

### Refusals and tested scope

The general finite helper verifies the entire augmentation axiom before using the rank formula (n<=9). Supports{0,1},{1,2}are rejected: {1}cannot augment from{0,2}. The full-set ratio alone is also insufficient: d=(100,1,1)in U(2,3)needs100, not51.

17distinct palette unittest methods passed in normal and optimized Python3.13.5. Loops compare270demand instances against a separate residual-demand DP on10three-block matroid-presenting families, and check1638uniform-rank/demand instances. These loop counts are not distinct unittest counts or held-out datasets. Three palette semantic mutations—skip exchange, floor instead of ceiling, allow overfull color incidence—were each caught by test assertion failures in both modes. General computation remains exponential in n, not a claimed polynomial-time theorem prover.

### Published exact delivery

Proof: https://drive.google.com/file/d/1zPLN90nK7nwDXvXMOsvmfS2uQrHDrxrE/view
9418bytes; SHA2569eafbf8be577638ba871d97f5505d0b0ce9e41ff3c4c4b241ee259431c13b5af.

Combined package: https://drive.google.com/file/d/1lRvVjuja4zXD59R0yCSM-6Utdon5FsfF/view
101854bytes; SHA256abc6df6b86efdab5af201d1028a1f1f45cdc3125e205a524d8cc4fd426ec2667.
Both proofs and ZIP were downloaded again and byte-matched. All65manifest payloads verified; the whole two-lane package replayed all33distinct tests and6semantic mutations in both modes from a fresh extraction. This is finite algebra/implementation evidence, not independent scientific review or full repository CI.

Folder: https://drive.google.com/drive/folders/1FecBXFPqm7f6V0dyxIuqCiCnFJqE6uey . Concurrent relocation changed its name/parent; stable IDs remain. Latest metadata shows shared, not owner-only.

Review priorities: exact P15-B support/local-demand matching; augmentation recognition; rank on parallel demand copies; ceiling and dual witness; unequal-demand cyclic construction and compression; and keeping this structural subclass separate from arbitrary downsets and the P15-D graph-coupled theorem.
----- END GITHUB ISSUE BODY -----
