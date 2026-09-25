# Reconnaissance and source boundary

Date: 25 September 2026. Task OA-D5-ANNULUS-BRIDGE-20260925.

Primary sources actually opened: Armentano, Azais and Leon, arXiv:2304.07424v3, HTML Theorems 2.2 and 7.1, Remark 8 and section 8.1 (https://arxiv.org/html/2304.07424v3); Stecconi, arXiv:2103.10853 abstract (https://arxiv.org/abs/2103.10853); NIST DLMF section 3.3 (https://dlmf.nist.gov/3.3). Search queries included both arXiv identifiers and confluent divided differences. Unrelated search results were not used.

The first paper supplies a Gaussian expected-count formula and a nonnegative weighted extension under continuity/lower-semicontinuity conditions. Here the nonnegative endpoint filtered determinants and witness type mark are treated in Section 7, with fixed-r nondegeneracy supplied by positive Fourier spectrum. This reference is not evidence for the new uniform annulus estimate. The Stecconi abstract is related background only; its uninspected proof is not imported. DLMF is interpolation context, not a novelty or correctness certificate.

The source work inspected through GitHub was PR22's released two-scale addendum at b2e1652f1374c3b45759324a1ad1fd4177458500 and PR16's transverse candidate at32b80ee085dc6a40113d1e46e333cda50d57ba21. Their exact declared scope and unaccepted status are retained. A pickup and a revised design were posted on PR22 before implementation; no existing proof branch was edited. The initial proposed shrinking cutoff was replaced by the simpler exact crossover |v|=r once full conditional C3 moments were combined with deterministic three-Hessian suppression.

No comprehensive literature novelty audit or priority claim is made. The actual contribution is an author-side combination/extension of the project sources with a complete explicit argument, not a new Kac-Rice theorem. Numerical tests, same-provider overlap, repository publication and hosted CI do not provide independent analytic acceptance.

Local cloning of the public Math repository failed at DNS resolution; no credential workarounds were attempted. Source publication uses the authorized connector. The existing hosted full-gate workflow provides a separate regression surface, whose result must be checked before any green claim. Vault99 and private sandbox content were not used.
