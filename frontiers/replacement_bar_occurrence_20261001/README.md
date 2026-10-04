# When a rare replacement bar occurs

The previous result counts selected finite persistence bars in expectation.
This companion asks a different question: how often does a random field
contain such a bar, and what does that bar look like after conditioning on
its occurrence?

For the same fixed planar torus and fixed compact birth, gap and shrinking
distance bands, the conditional theorem proves

    E[N_h 1{N_h >= 2}] = o(h^5),
    P(N_h > 0) = L² C_U(1) h^5 + o(h^5).

Here N_h counts distinct selected actual bars, and C_U is the previously
identified, multiplicity-corrected coefficient. Given occurrence, there is
one selected bar with probability tending to one. Its weak mark law is
C_U(Phi)/C_U(1).

[Theorem and probability argument](PROOF.md) ·
[Global isolation proof](GLOBAL.md) · [Exact source identities](SOURCES.json)

The key new step uses the whole conditioned field. A generic local cubic
has only one strict maximum; a Taylor estimate excludes roots at intermediate
scales; the limiting field is Morse away from the forced contact, so its
remote critical points remain separated. A bounded event indicator then
fits into the existing weighted counting identity without assuming a
second moment or spatial independence.

The result is conditional on C50 and its seven retained analytic interfaces.
C50's consumed proof, root analysis and original source map are copied
unchanged under sources/c50 at their published commit because its separate
integration is pending. This is not acceptance of those premises.

No quantitative rate, factorial-moment bound, Poisson law, all-mark
exhaustion, higher-dimensional theorem, infinite-volume limit or complete
research-program proof is claimed.

From the repository root, run the finite exact controls:

    python3 -B -S frontiers/replacement_bar_occurrence_20261001/test_exact.py -v
    python3 -B -O -S frontiers/replacement_bar_occurrence_20261001/test_exact.py -v

They check source identity, rational count/probability distinctions, marked
sampling, and finite algebraic controls. They do not prove the continuum
Gaussian or limiting arguments. The proof requires substantive source review.

