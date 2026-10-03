# Cusp coefficient transfer to every torus side L >= 10

OpenAI / GPT-6 Astra Pro. Author-side proof candidate; nonauthor review OPEN.
Scientific effect NONE. No self-merge or change to any source proof/status register.

This recovers the interrupted covariance-transfer calculation on Math-#219.
The reference numerical author added its own Lemma S for L>=24 during the
interruption. That overlapping method is credited, not counted twice. The
present extension covers d=1,2,3, every frame and every real L>=10, using the
birth-MARGINAL jet and a proved covariance floor1/3. No source quadrature is rerun.

The theorem bounds the CU.2 coefficient EXPRESSION for the exact normalized
periodic kernel, not the finite-lifetime density or the correctness of Theorem CU.
For each dimension, the relative difference from the Gaussian reference is at most:

| d | L>=10 | L>=24 |
|---|---|---|
| 1 | 6.89628366587e-9 | 3.29775477012e-109 |
| 2 | 1.32408646215e-6 | 6.33168915861e-107 |
| 3 | 4.90170601596e-5 | 2.34396164673e-105 |

Read PROOF.md for the order-eight image estimate, the birth-marginal floor,
nonnegative homogeneous density-slice sandwich and exact rational rounding.
All bounds cover arbitrary orthonormal frames, without imposing GOE independence
on the torus jets. Correlations induced by integrating birth are explicitly retained.
The coefficient is not equated to its reference value.

`conditional_absolute_c1` values in RESULTS.json consume the reference interval
table of PR219 conditionally. They are not independent certification of its
Mellin transform, Gauss quadrature or special-function code. A tiny transfer error
does not create more accurate reference digits or a finite-lifetime error bound.

## Replay

From this standalone packet:

    python -B -S -m unittest discover -v
    python -B -O -S -m unittest discover -v
    python -B -S transfer.py
    python -B -S verify_sources.py --local-only

The last command checks packet identities and reports no historical-source
verification. In a full checkout with the pinned source commits use:

    python -B -S frontiers/cusp_torus_transfer_20261001/verify_sources.py

All mathematical code is standard-library Python. The suite has33 methods,
including reused real-Git custody fixtures; eight semantic variants must reject
in both modes. Exact exponential Taylor tails replace untrusted transcendental
calls. The covariance matrix is reconstructed from derivative multi-indices.
There is no Lean formalization of the new integral comparison.

## Review and coordination

Original pickup219/5930612079; recovery and overlap reconciliation219/5932010316.
The prior R.1-only review5378866830 was actually delivered before interruption;
this conversation does not issue it again or count it as acceptance here.

A: birth marginalization/homogeneity and the exact covariance floor.
B: normalized all-frame order-eight image estimate and Gaussian sandwich.
C: rational enclosures, inherited reference intervals and scope boundaries.

The current user continuation authorizes this foreground research/recovery under
main/governance/OP-WORKFLOW-20260930.md. No stopped agent, watch or timer is
restarted. The targeted PR workflow is an execution check, not a scientific vote.
The author remains exposed to the earlier OpenAI source chain and will not self-merge.
