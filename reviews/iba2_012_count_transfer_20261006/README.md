# Count-weighted IBA2-012 transfer

**Author:** OpenAI / GPT-6 Astra Pro, `iba2-count-weight-transfer-r6-20261006`, for Dylan Roy.
**Initial disposition:** conditional proof candidate; nonauthor mathematical review and actual test execution required.
Scientific effect NONE. This packet adds no scientific status register or formal target.

Read [PROOF.md](PROOF.md) and its [exact bindings](SOURCES.json). From the landed
finite-radius multi-soft event estimate and the C6 fixed-order factorial moments,
Holder gives

    E[K^a N_R^p; S] <= C r^3 Xi^(1-p/m),
    Xi = product_(j=2..q+1)(eta_j+r)^(j+2), m>=2, m>p>0.

All field, dimension, observation radius and positive-compact-mark hypotheses stay
fixed. The proof localizes the ordinary count moment before applying Holder; it
does not silently insert a first-moment premise or assume independence. Shrinking
thresholds give o(r^3) for every fixed polynomial or factorial local-count weight.
A precise abstract rare-spike family rules out loss-free O(r^3 Xi) as a consequence
of these inputs alone, even with every fixed factorial order available.

## Replay

From this directory, with Python 3.11 or newer and no third-party packages:

```sh
python3 -B -S test_count_transfer.py
python3 -B -O -S test_count_transfer.py
python3 -B -S test_count_transfer.py --mutant M1
python3 -B -S test_count_transfer.py --mutant M2
python3 -B -S test_count_transfer.py --mutant M3
python3 -B -S test_count_transfer.py --mutant M4
```

Baseline contract: 13 methods, exit0, JSON ok=true, empty failures/errors; stdout
must agree between normal and optimized modes. Each named mutant must exit1 with
one or more intended assertion failures and an empty errors array. M1 drops the
common radial factor; M2 removes Holder's exponent loss; M3 reverses the unequal
weights; M4 omits the constant in the factorial envelope. Repeat in optimized mode.
An unknown label must exit2. A crash, missing dependency, syntax error, or unrelated
failure is not evidence that a mathematical mutant was correctly rejected.

At publication, the author's execution tools fail before starting a command, so
these are **instructions and unexecuted author test source**, not a claim of local
passes. Read later PR receipts for actual execution and reviewer provenance.
The existing general CI does not automatically discover this standalone suite.

## Offline preservation and handoff

Save the four packet files plus the three source files at the full source-cut
commit in SOURCES.json. Preserve relative paths in a new directory, record Git
blobs and SHA-256 locally, and retain test stdout, stderr, exit codes and the actual
Python version outside the frozen packet. A source checkout is not a claim of
installed Lean, model weights, full Git history or laptop readiness. Do not modify
the already sealed R5 offline kit or overwrite any laptop worktree.

For a bounded review, read PROOF sections2–5 against the consumed source interfaces,
try the N=1 and remote-only countercases, and inspect the all-threshold rare-spike
models. Report exact source identity, actual executions, PASS_SCOPED or actionable
AMEND and residual scope. Required integration checks and separate eligible merge
execution remain necessary after review. General IBA2-012 and IBA2-009 remain open.
