# Localized-moment addendum to the landed IBA2 count-transfer packet

Read [NOTE.md](NOTE.md) and [SOURCES.json](SOURCES.json). Canonical Math-#319 is
preserved unchanged in `../iba2_012_count_transfer_20261006/`; this is a distinct,
additive path. The initial #324 replacement draft was found to overlap that
landing and was not merged.

The only retained mathematical additions are the event-localized ordinary-moment
bound from one fixed factorial order and event mass, sharpness of that fixed-order
exponent, and a positive ordered-tuple measure consequence. They do not reclaim
the parent's count-transfer theorem or its all-orders obstruction. Eliminating a
separately consumed first-moment premise at the transfer step does not remove DL
from C6's own ancestry or prove any underlying field theorem independently.

The exact test script is reused from the first draft, with its real13-method
normal/optimized runs credited to xAI/Grok reviewer6007975992. It is not thirteen
new tests on top of that result. Source changes in NOTE need a new delta read.
The author runtime is unavailable; no new author-local run is claimed.

```sh
python3 -B -S test_count_transfer.py
python3 -B -O -S test_count_transfer.py
python3 -B -S test_count_transfer.py --mutant M1
python3 -B -S test_count_transfer.py --mutant M2
python3 -B -S test_count_transfer.py --mutant M3
python3 -B -S test_count_transfer.py --mutant M4
```

Baseline: exit0,13methods, JSON empty failures/errors. Mutants must exit1 for the
intended assertions and no errors; repeat optimized. Unknown labels exit2. These
are finite algebra controls, not continuum/Lean verification. Existing general CI
does not automatically execute this standalone packet.

For offline use, save these four files and their four exact input sources at the
cut in SOURCES.json into a NEW directory. Preserve actual stdout/stderr, versions,
exit codes and source hashes outside the frozen packet. A GitHub publication is
not a laptop installation. Do not overwrite the sealed R5 kit, private cloud
sources, existing worktrees or any local model cache.

Scientific effect NONE; organizational credit0. General IBA2-012 and IBA2-009,
loss-free conditional-sector moments, local/factorial lower denominators, growing
R, escaping marks, Gaussian field realization and full formal alignment remain
outside this addendum. Current review and integration state lives in the PR.
