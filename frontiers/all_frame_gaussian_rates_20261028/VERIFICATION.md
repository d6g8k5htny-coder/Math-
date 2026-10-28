# Actual checks, internal critique and retained limits

28 October 2026. Authorship: OpenAI/Codex GPT-6 `/root`, with construction,
Gaussian translation, exact-control and source-analysis support from
`essential_template`, `essential_gaussian_cost` and `next_marked_hypothesis`.
Those contributors are authors, not scientific reviewers of their own work.

## Actual finite runs

With Python 3.12.14 and the standard library only, both commands exited zero:

```sh
python -B -S frontiers/all_frame_gaussian_rates_20261028/check_exact.py
python -B -S -O frontiers/all_frame_gaussian_rates_20261028/check_exact.py
```

The retained `CHECK_NORMAL.json` and `CHECK_OPTIMIZED.json` are byte-identical.
They record six full-cube contact/right-inverse cases, two insufficient-cube
counterexamples, the exact global-margin identity, twelve projection cases,
twenty-four formal pin-discrepancy cases, twenty-four wrong-gradient-factor
counterexamples and twelve remote-margin cases. Critical-window controls add
six augmented-jet rank cases, twelve exact scalar pin cases, 144 rational
Schur/adjugate/type cases, eighteen quartic-threshold cases and six completed
square/margin cases. Thirteen source identities are checked as well.

Final checker SHA256:
`0bc66147bc2457d5156dcbd115f10f1f295528710126ee2729713236efb88053`.
Both reports bind the final proof, appendix, checker and source-manifest
digests. Controls use rational arithmetic and formal coefficients, without
floating-point inequalities or Python assertions. The finitely sampled
rational frames do not prove uniformity over orientations; that argument
is the analytic polynomial-rank/compactness proof in the text. Likewise
the continuum geometry and Gaussian probability results are not certified
by this finite script.

## Exact source identity checks

`SOURCES.json` pins thirteen consumed or comparison files by repository,
commit, path, byte count, SHA256 and Git blob identity. Root compared eight
base inputs directly with their Git objects at
`7d63d08f6cfadfd9c2ef28039a370d741126f9a0`. Five predecessor files were
fetched from their exact GitHub publication commits and compared byte for
byte with the locally consumed files: UPPER, UPPER_SOURCES, AXIS,
AXIS_SOURCES and AXIAL. All matched. Their draft scientific status is not
transferred as acceptance.

The main proof reconstructs its Gaussian estimates for the wider declared
spectral class. The critical-window appendix consumes CU.3 only as the
existing self-contained deterministic C2 window decision. Its other cusp
citations attribute the prior model, weight and small-kappa integral. It
does not silently transfer the predecessor field's smoothness, positivity
outside the finite cube or stochastic conclusions to a new covariance.

## Fresh same-family internal mathematical critique

Three separate nonconstructing OpenAI/Codex readers inspected the proof.
These checks provide error detection; they do not supply the project's
required different-family scientific review or organizational independence.

`all_frame_main_check` read main §§1--9 at SHA256
`d30923c97c883fb43ce5c9bf5dfacf2601750043cb96aed2d529cdb3efcb1402`,
cross-checked the sharp axial source and observation/normalizer construction,
and ran the then-current finite checker. It found no substantive blocker
within the fixed compact-gap claims. It requested two literal corrections:
the inverse sine chart needs its inner factor omega, and the sine vector
must not reuse the physical pin name S. Root applied both; the reader
confirmed them at `c49fbd7bbe2ac10109e3b4278dfee34f2bdae18729f2ea5abf17956d81e8cc95`.
The sole later main-proof edit is in §10, outside this reader's scope.

`gap_and_genericity_check` read the same initial main proof, concentrating
on §§10--11 and their dependencies in §§2--8. It checked the inverse-free
determinant bound, full normalizer floor without independence, scaled
template/noise Schur bounds, moment powers, small-gap obstruction, finite
Fourier jet filters, Gaussian mesh dimensions and the conventional C4/H0
interpretation. It found one literal bound needing a smaller coefficient:
after arbitrary bounded noise, the older remote height is at least
`b+beta q_p^2/2`, not the unperturbed `b+beta q_p^2`. Root fixed it. The
reader confirmed the correction and no remaining blocker at final main
proof SHA256
`26c41fb4df2bc7d1efac25dbfaab4822dbf2b17ebc7f77a108975a8a35e36d20`.

`critical_global_check` read the full critical-window appendix, needed main
definitions and cusp CU.2--CU.4 plus Remark 8.1. It checked the C4 regression
coupling, contact determinant constants, off-contact level-b genericity,
ridge C4 regularity, fixed-neighborhood Hermite bound, Gaussian support,
finite-versus-essential split and moment divergence. Root made explicit
that §6's surrounding sphere is inside the ridge chart. Its bounded final
readback found no concrete blocker at appendix SHA256
`16d15a49b5c484205c85b00d10b26c173072c946ee5be7f7da2c1d3a4ce97b17`.
The consumed cusp proof SHA256 is
`cffc1b83ac364da58bd650c3c301ea1babd38e19af54f74010bdc120edce38a8`.

## Mathematical scope and delivery

The result removes the coordinate-axis restriction, proves matching finite
long-lifetime lower tails, supplies a declared finite-spectrum/C4 extension,
and controls both the moderate-gap wedge and every fixed positive critical
ratio. The cube-four corollary derives conditional Morse/distinct values
and the ordinary-H0 reading at each fixed target; it does not instantiate
an all-orders smooth formal interface.

The essential/finite critical-window split adds a global distinction that
the existing local cusp theorem explicitly leaves open. No priority is
claimed for that theorem's quartic model, typed weight, normalizer or cubic
small-kappa integral. Pending review of existing conventional marked-law
or inverse-moment proofs is not relabeled as a missing theorem.

This is an additive packet stacked on PR523's exact head
`de872d97fa54eb11c0834b8f532543222900d165`. Existing proof bytes, workflow
files, registers, prizes and premise flags are unchanged. No Lean run,
hosted CI or full-repository suite result is claimed. PR522 retains the
separate old Python-3.11 publication-verifier limitation; it is not weakened
or silently counted as passing here. Required different-family scientific
review remains pending; this packet is not Ready or merge-cleared.

The current proofs do not determine optimal exponential coefficients,
probability prefactors, joint small-tau limits of the global essential
share, or cross-spectrum/dimension/volume uniformity. No general counting
intensity is inferred from fixed-pin tail statements.
