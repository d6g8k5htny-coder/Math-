# Contact-kernel tails and whole-annulus synthesis

Read **KERNEL_TAILS_AND_SMALL_GAP.md** for the new kernel results and **ANNULUS_ASYMPTOTIC_BRIDGE.md** for the conditional annulus implication. This is OpenAI-authored research for separate review, not a status register.

The exact type integral is `27392/315`. After the full endpoint normalization, the fixed-angle small-gap contact kernel has order `k^6/|v|^13`, with an explicit model coefficient. For fixed positive k the same kernel is exponentially suppressed at the axis; a stronger one-sided penalty is derived. These limits must not be interchanged. The Gaussian integration over the free jet reduces to seven truncated moments and one remaining height integral.

The existing PR22 finite-r two-scale estimates, combined with PR25's fixed-chart candidate limit, imply a sharp saddle-resolved whole-fixed-annulus limit under explicit pending analytic interfaces. This does not reproduce or claim independent acceptance of either source.

Run:

```sh
python -B -S -m unittest -v test_contact_tools
python -B -O -S -m unittest -v test_contact_tools
python -B -S run_validation.py --output /tmp/contact-tail-new-run
```

Use a new output outside this directory. There are24 finite test methods and7 deliberate broken variants, checked in both modes. Most checks use exact rational polynomials. Two numerical quadrature/moment checks are diagnostic floating-point comparisons, not enclosures. The original test-first and corrected expected-value logs are retained separately as provenance.

Author-side novelty, proof correctness, review provenance and execution evidence remain different axes. Review assignments remain on the existing GitHub queue; no source status is changed.
