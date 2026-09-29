# Targeted SARD-G completion candidate

**Author-side successor; nonauthor analytic review required. Scientific effect NONE.**

[A2_FIXED_FRAME.md](A2_FIXED_FRAME.md) replaces the invalid moving-eigenframe and
C1-into-C1 assertions of #137 v1. It proves only what the downstream proof uses:
joint Frechet C1 evaluation, continuous C1 arc dependence and local derivative
bounds. It uses fixed-origin/splitting bounded trajectories; a separate weighted
argument proves decay but is not differentiated.

[NONVANISHING_AND_CLOSURE.md](NONVANISHING_AND_CLOSURE.md) supplies an explicit
interior scalar-potential perturbation, a Fourier-density route to a nonzero
Cameron-Martin derivative, elementary full-measure genericity, and an assembly
with #135's actual robust charts. Its qualitative planar no-saddle-connection
statement is not a conditional-field or regional C103 estimate.

[AUTHOR_CORRECTION.md](AUTHOR_CORRECTION.md) records exactly what was wrong and
what is preserved. Original #137 proof bytes are not rewritten or accepted.

Run from this directory:

    python -B -S verify.py --output /path/to/new-output
    python -B -O -S verify.py --output /path/to/other-output

Both entry modes check the full flat packet and execute 18 tests plus 9 intended
semantic negatives in each Python mode. Outputs and source identities must agree.
The tests are finite exact illustrations, not invariant-manifold, support, or
measure-theoretic proofs. All implementation uses the Python standard library.

The only imported source-level geometry is the pinned robust-chart manuscript
in SOURCE_MAP.json. Claude's A2 note is credited and reviewed separately; its
classical references are not silently used to validate our corrected contraction.
Old AMEND, C103, RN/JETMOD, 3D and registry statuses remain unchanged by publication.
