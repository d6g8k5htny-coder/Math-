# P15 bipartite-overlap capacity candidate

Scientific effect NONE. Author-side theorem; nonauthor review required.

[Full proof](PROOF.md): shared original coordinates, exact capacity coloring,
same global palette K=max d_i>=4, and transformed-price hazard factor
2/[5-log(5e-4)]<3/4. Inactive smaller demands are permitted. No arbitrary
macro-clutter, arbitrary read-two, sharp-factor, or unrestricted P15 claim.

The triangle counterexample shows why read-two incidence alone is insufficient;
the overlap probability example shows why the old independence step is invalid.

Run from this directory:

    python -B -S run_validation.py
    python -B -O -S run_validation.py

The self-contained standard-library runner verifies exact source membership,
checks the stored deterministic summary, runs the finite tests in both modes,
and rejects the semantic mutants. It is not a continuum or Lean proof checker.

[Source map](SOURCE_MAP.json) and [reconnaissance](RECONNAISSANCE.md) distinguish
project inputs, classical facts, and neighboring literature. No blocked source
from the other mathematical packet has been republished or reconstructed here.

[Even-capacity extension](EVEN_CAPACITY_EXTENSION.md): for arbitrary read-two
block incidence with all capacities even, the same exact palette and cover
formula holds without bipartiteness. A proved entropy hazard inequality gives
the stronger factor 2/log(512/25)<2/3. Neither factor is claimed optimal.
