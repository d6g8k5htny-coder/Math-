# Marked Fourier cluster candidate

Author-side publication successor v1.1; actual nonauthor analytic review required.
Scientific effect NONE. No prior proof or status register is changed.

PROOF.md proposes E[N exp(theta N^(2/d))]<=C r^3 in the original fixed-d,
compact-mark pinned/tilted model. It extends Fourier truncation under the actual
witness kernels, then inserts an exponential mark into the landed Palm regional
proof. In d=2 the cluster control is exponential; in d>2 stretched exponential.
The prefactor under arbitrary witness conditioning is retained, not suppressed.

The independent-replica argument is already present in merged #153 and is
credited explicitly. New exponential-weight compactness is separate. No unique
cluster law, spatial Poisson theorem, numerical constants or higher-factorial
lower bounds are claimed. Prior handoff bytes stay in their original delivery;
this is a documented successor, not a recovery of missing historical code.

Run from this directory:

    python -B -S verify.py --output /path/to/new-output
    python -B -O -S verify.py --output /path/to/other-new-output
    python -B -S -m unittest -v test_sources
    python -B -O -S -m unittest -v test_sources

Each full verifier runs 17 finite mathematical controls and eight intended
semantic variants in BOTH Python modes. The ten additional custody controls use
synthetic local sources; they are not Gaussian checks or full upstream replays.
With a complete historical repository checkout, additionally run:

    python -B -S source_check.py --repo /path/to/repository

That checks six current and historical proof/reading-rule identities, including
the credited prior result. The hosted workflow executes it with fetch-depth:0.
Passing finite or formal-scalar checks cannot accept the new analytic argument.
