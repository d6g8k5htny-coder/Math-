# Collision geometry and marked lifetime transfer — research delivery

OpenAI / ChatGPT, 25 September 2026. Author-side mathematical derivations; separate analytic review pending. No change to scientific-status registers or acceptance of a global persistence/RN theorem.

## Read in order

1. `GEOMETRY_AND_CUBIC_INDEX.md`: quantitative critical-simplex Hessian theorem, approximate-critical-point error, sharpness/flattening counterexamples, and exact six-pin cubic intermediate-saddle identity.
2. `TRANSVERSE_CONTACT_ASYMPTOTIC.md`: proposed refinement of the fixed two-dimensional transverse count bound into a positive saddle-contact density and vanishing leading extrema densities. All frame/mark/chart bounds and exclusions are stated.
3. `COLLISION_TRANSFER_THEOREM.md`: marked collision-to-lifetime transfer with exact coefficient and proof; cumulative version; derivative oscillation counterexample; exact small-gap phase diagram; selection and multi-stratum effects.

The new type identity is

    det B_X = -(9 k^2/v^2) [(w+1-2 theta)^2+4 theta(1-theta)] < 0,
    w=(qv+12ku)/(6k), 0<theta<1.

It is an exact statement about the pin-compatible cubic model, not a claim that finite-radius smooth fields cannot have other types. The Gaussian leading-kernel application is a separate author-side theorem candidate.

The original informal universality claim needs additional hypotheses. The derived coefficient is

    C=(1/m) integral a0(z) p0(z) kappa(z)^(-(alpha+1)/m) dlambda(z).

Small kappa can make this moment diverge and change the exponent or add a logarithm. Merely having h(r)~kappa r^m does not guarantee a density asymptotic without derivative control.

## Exact checks

    python -B -S exact_checks.py
    python -B -O -S exact_checks.py

The local suite has 24 distinct methods and passes in both modes on Python3.13.5. The GitHub version passed the same 24 methods in both modes on Python3.11.16. These are exact finite algebra/Schur-complement and counterexample checks, not a continuum proof checker. False variants within tests are not counted as a separate semantic-mutation suite.

`diagnostic_kernel.py` is an OPTIONAL unperiodized Bargmann-Fock quadrature prototype using only the standard library. `DIAGNOSTIC.json` contains its refinement ladder. This is not an interval enclosure, is not the finite-torus coefficient, and supplies no scientific acceptance.

## GitHub publication and evidence

Draft Math- PR25: https://github.com/d6g8k5htny-coder/Math-/pull/25
Branch: chatgpt/collision-mechanism-transfer-20260925
Source: ad35e46d15c2815c36746442808a1626a9724e8a
Repository note: reviews/collision_mechanism_20260925/NOTE.md

The repository NOTE.md is a consolidated proof note. These three local Markdown files are expanded expositions, not byte-identical copies of NOTE.md. Likewise the local exact-check script contains some extra explanatory comments; do not confuse its hash with the distinct GitHub script hash.

Hosted run36189883478, Python3.11.16, test-merge1baa51a44c18990c435b52789a0f3c9183b6d4b8, passed 24 tests in normal and optimized modes. Artifact10888045590 was downloaded, SHA256/ZIP-CRC verified, and both complete logs/report inspected. The ZIP in `evidence/` preserves the actual hosted evidence and tested source identities.

The older source proofs and other agents' branches are unchanged. The exact deterministic geometry and transfer results have written proofs; the new Gaussian contact asymptotic is explicitly pending separate-agent analytic review. No global RN/elder claim, thin-belt/collision completion, or worldwide novelty claim is made.

## Prior-art boundary

Taylor/linear algebra and change of variables are established tools. Related primary work: Gass–Stecconi on multi-point interpolation and critical-point moments (arXiv:2305.17586); Armentano–Azais–Leon on marked Kac-Rice (arXiv:2304.07424); Muirhead on shrinking height windows (arXiv:1901.11336); Denisov–Zwart on Breiman-type product asymptotics (DOI10.1239/jap/1197908822). The potentially distinctive component is the exact pin-compatible typed kernel and its application, not invention of these tools.

