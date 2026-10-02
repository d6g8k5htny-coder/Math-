# Separated folds and multiple ordinary short bars

New author-side mathematical candidate by OpenAI / GPT-6 Astra Pro.
Universal Law is a research program initiated, directed and supported by Dylan Roy.
Read **PROOF.md**. Scientific-status effect NONE; nonauthor review pending.

For the original periodized Gaussian field, fixed d>=2,L>0 and any fixed n
pairwise disjoint nonempty regions, the manuscript constructs n actual ordinary
finite elder bars, each of lifetime between t/8 and t, with probability at least
c_n t^(2n/3). It uses finite Fourier coordinates and a fixed residual neighborhood,
not independent spatial regions or a shrinking Gaussian small-ball assumption.
Complete local exit barriers identify the global elder pairings.

For n=2, this gives an actual-field lower bound of order t^(4/3) for the
multiple-bar excess. Thus it cannot be O(t^(10/7)), and the three-term expected
count cannot automatically be transferred unchanged to occurrence probability.
The main theorem does not use the D1 density theorem, C52 isolation or Kac–Rice.
Only the separately labelled consequences use the pinned RATE/O interfaces.

Not supplied: a matching upper bound, exactly-two probability, asymptotic
coefficient, two-bar mark law, Poisson approximation, uniform large-volume
constants, numerical c_n, human review or full formalization. In particular a
count discrepancy is not a lower bound for the lifetime-only mark discrepancy.

## Reproduce finite controls

    python -B -S -m unittest -v
    python -B -O -S -m unittest -v
    python -B -S check.py
    python -B -O -S check.py
    python -B -S verify_sources.py --local-only

Each --mutant M1 through M5 must exit1 in both modes; an unknown label exits2.
These finite checks verify algebra and falsifiers, not the continuum proof.

In a project checkout containing both pinned commits:

    python -B -S frontiers/separated_fold_multiplicity_20261002/verify_sources.py

The non-local command authenticates three exact historical path/blob bindings.
Local-only explicitly does not claim that authentication. Source-helper code
reuses the existing c2-audit path/inventory implementation, with a small new
three-source caller and real-Git regression fixtures. No dependency is executed.

## Review

A: ridge/discriminant uniformity, exact root gap and every global cap face.
B: fixed Fourier approximation/tail event, correlated Gaussian conditional
   density, simultaneous parameter inversion, Jacobian and measurability.
C: count/sampling consequences and the exact optional source hypotheses.

The author will not self-merge. Original #235 files and reviewed source bodies
are unchanged; this is an isolated successor to pickup235/5943116501.
