# Actual verification and retained scope

28 October 2026. Root proof/integration by OpenAI/Codex GPT-6 `/root`;
template and finite-control author support by `essential_template`, Gaussian
translation support by `essential_gaussian_cost`, and reuse-first source
corrections by `next_marked_hypothesis`. These contributors are not counted
as scientific reviewers of their own work.

## Actual finite runs

With Python 3.12.14, standard library only, both commands exited 0:

```sh
python -B -S frontiers/essential_gaussian_rate_20261028/check_exact.py
python -B -S -O frontiers/essential_gaussian_rate_20261028/check_exact.py
```

The byte-identical reports `CHECK_NORMAL.json` and `CHECK_OPTIMIZED.json`
record 12 exact rational-circle pin/Fourier cases, 24 invalid-template
counterexamples, three rigorous alternating-Taylor interval cases, eight
leading RKHS coefficient identities and seven source-identity checks.
The rational-circle cases check algebra independently of the relation
between tau and its trigonometric values; the three Taylor cases enclose
the actual sine and cosine at tau=1/8,1/16,1/32. No floating-point inequality
or simulation supplies the continuum theorem.

Final proof SHA256:
`8e75f467dfd91bbffce448b92e17af8a76c0c3f2f13616534973dffe437f4172`.

The checker validates source byte counts, SHA256 and Git blob identities.
Root additionally compared the inherited base inputs directly with their
Git objects and fetched both the upper proof and its source manifest from
publication commit `223293d9d26a7a4158026a4225523e8a683a8794`; the bytes
matched the local consumed files exactly.

No Lean execution, full-repository suite, hosted CI, Gaussian simulation,
qualifying scientific review or status promotion is claimed. The distinct
old Python-3.11 publication-verifier limitation remains in PR522's record.

## Internal technical critique and resolution

The fresh same-provider agent `essential_rate_critique` did not construct
this proof. It inspected the exact template, global margin, fixed C4
zero-pin stability, Hessian inertia/weight floor, finite-mode RKHS cost,
conditional projection, translation sign and symmetry, and full-normalizer
upper-bound dependence. It found no mathematical blocker within the stated
coordinate-axis scope and replayed the finite checker.

Its minor clarity finding was that template transverse coordinates must
explicitly be lattice coordinates. Root checked the periodicity requirement
and clarified §2. The reader then performed a bounded readback at the final
proof hash above and confirmed that the comment was resolved and the
unchanged mathematical argument retained its prior assessment.

These are same-family internal technical checks. They are not the project's
required different-family scientific review or organizational independence.

## Delivery and mathematical limits

This is a separate additive packet stacked on PR522's published head
`223293d9d26a7a4158026a4225523e8a683a8794`, not a modification of that head
or a takeover of its scientific review. Existing source files, reviews,
workflows, registers, prizes and premise flags remain unchanged.

The quantitative lower-bound question is answered here for coordinate-axis
pins and compact marks. Arbitrary axial directions, noncompact uniformity,
optimal rate coefficients, probability prefactors and parent-theorem
acceptance remain outside the result. A new Draft can expose this proof for
different-family review; it is not Ready or merge-cleared.
