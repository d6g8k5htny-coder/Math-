# Reconnaissance memo — scalar certification slice

Date: 2026-09-26 America/Chicago. Scientific effect: NONE.
Scope: a uniform scalar bound for the unperiodized planar Bargmann-Fock field
under six linear pins; not periodized SIDE24 or weighted-Palm convergence.

Primary sources inspected:

- Rivera and Vanneuville, *The critical threshold for Bargmann-Fock percolation*,
  arXiv:1711.05012, https://arxiv.org/abs/1711.05012. The abstract identifies the
  same planar centered Gaussian covariance exp(-|x-y|^2/2). Its percolation
  theorem is not imported as a persistence or pin-conditioning theorem.
- Python-FLINT's Arb documentation,
  https://python-flint.readthedocs.io/en/latest/arb.html. It describes rigorous
  midpoint/radius enclosures. No Arb code or dependency is needed for the
  present rational arithmetic; an optional backend remains a later decision.
- The existing Math- PR87 TS calculation at full commit
  0fab9330c017e78eb9ef6d928e04aba9f376a470 was read through the connected GitHub
  source. Other parts of that packet have unresolved review findings. This
  package rederives its TS identity and does not import those other assertions.

Decision: use a self-contained Gaussian-regression calculation followed by
positive-coefficient exponential inequalities. This provides an all-radius
analytic bound before computing rational endpoints, avoiding cancellation
near zero and avoiding the false inference that a finite radius grid is a
continuum certificate. Independent review is still requested. This limited
search is not a novelty audit and supports no claim of a new general theorem.
