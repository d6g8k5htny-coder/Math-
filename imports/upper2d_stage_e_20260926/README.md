# Recovered STAGE_E falsifier sources

Scientific effect: **NONE**. This packet preserves 11 original Dropbox files (five STAGE_E scripts, two historical transcripts, four dependency copies). Original `CERTIFIED` / `PASS` labels are historical text, not accepted conclusions. No proof body, claim manifest, `STATUS`, `PROOF_INDEX`, prize or `lemma_closed` value is changed.

## Read and replay the discrete counterexample

[attack_h4jc.py](raw/STAGE_E/attack_h4jc.py) tests the older H4-JC predicates implemented in a frozen discrete model. Its [B1 dependency](raw/B1_taxonomy/b1_falsifier.py) uses a 40×40 triangulated torus and lexicographic (binary floating-point height, vertex index) keys. In the constructed example one saddle meets both predicates, so `N_qual + N_loop = 2 > N_w = 1`.

On 2026-09-26, OpenAI/Codex replayed the unchanged script under CPython 3.12.14, normal and optimized modes. Both runs exited zero and reproduced the [historical transcript](raw/STAGE_E/t_attack_normal.txt) byte for byte. It reports 427 audited pairs, 175 A-pairs, 132 inequality violations and 1,612 two-cluster checks. The quiet witness and T2 witness use the same construction; they are not independent examples. See [the review](REVIEW.md) and [replay receipt](REPLAY.json).

From the repository root, using the Python standard library only:

```sh
python -B -S imports/upper2d_stage_e_20260926/verify.py
python -B -S imports/upper2d_stage_e_20260926/raw/STAGE_E/attack_h4jc.py > /tmp/stage-e-normal.txt
python -B -O -S imports/upper2d_stage_e_20260926/raw/STAGE_E/attack_h4jc.py > /tmp/stage-e-optimized.txt
cmp /tmp/stage-e-normal.txt /tmp/stage-e-optimized.txt
cmp /tmp/stage-e-normal.txt imports/upper2d_stage_e_20260926/raw/STAGE_E/t_attack_normal.txt
```

This finite replay does not certify a Gaussian continuum theorem, a Gaussian failure probability, any current repaired H4-JC successor, or a Palm rate. It preserves a failed historical formulation and its executable witness.

## Numerical sources remain unverified

| Source | Availability and limits |
|---|---|
| [certify_axis_break.py](raw/STAGE_E/certify_axis_break.py) | Original bytes recovered; claimed enclosure is not endorsed. Extra scale factor and rounded interval inputs require repair/review. |
| [isserlis_break.py](raw/STAGE_E/isserlis_break.py) | Original bytes recovered; list/tuple indexing defect and incomplete mean-shift bound block the printed certification claim. |
| [hunt_wedges.py](raw/STAGE_E/hunt_wedges.py) | Exploratory QMC search; additionally needs `H5_closure/h5_results_*.jsonl`, not included here. |
| [hunt_rim.py](raw/STAGE_E/hunt_rim.py) | Exploratory QMC search with hardcoded ledger constants; no fresh numerical replay claimed. |

Their local Python source dependencies are preserved in [C1_alpha_intensity](raw/C1_alpha_intensity/) and [H2_foundations](raw/H2_foundations/). They also require NumPy, SciPy, mpmath and SymPy; no versions are locked or installed by this import. These historical scripts are outside the repository's standard-library calculation route. Do not bulk-import them: the STAGE_E scripts execute work at import time. The discrete H4-JC replay above is self-contained; the numerical searches are not.

## Exact custody and coordination

[MANIFEST.json](MANIFEST.json) records source IDs/paths, byte counts, ordinary SHA-256, Dropbox content hashes and Git blob identities. [MANIFEST.sha256](MANIFEST.sha256) is a convenient raw-file checksum list. These are original binary downloads, not native-document exports or ChatGPT transcriptions. No temporary download URL is published.

The five script blob IDs were absent from the four complete Git trees recorded in the manifest and from the 358-row source-import manifest reading copy inspected on 2026-09-26. This is a bounded comparison, not an exhaustive claim about all Git history. Four dependency copies intentionally preserve the relative import layout; the parallel source-import lane retains its canonical import paths. The [scope claim](https://github.com/d6g8k5htny-coder/main/issues/86#issuecomment-5849955559) coordinates this additive path. The same-provider review supplies zero organizational-independence credit. Other missing research sources remain a separate recovery task.
