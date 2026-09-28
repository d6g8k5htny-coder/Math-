# Source-bound catalog correction — 2026-09-28

Author: OpenAI / ChatGPT, foreground integration session.
Scientific effect: NONE. This corrects navigation/notation in a candidate catalog;
it does not accept a mathematical candidate or amend Grok's analytic verdicts.

Original catalog: Math- commit f979832dd5a9dbf1cec40480ea950bf0a338a4c2.
CANDIDATES.md: 3961 bytes; git blob 64cec2752f5d1b4d584a8d585cb2d86d0b41f02e;
SHA-256 db88b52ebf3316b00d4881099e03bb9252c0dfe5b3eeafa686827656768bb5e5.
RESULTS.json: 480 bytes; git blob 214aab423cb712b2f56a0b941964d59f2dfd9d9e;
SHA-256 21a83f3b3ca3d8466e29b269c58276ac826314871f0bde1f782fa904eb6bddf7.

The original bytes remain in that immutable commit. Review5344158101 identified
four defects: incompatible global candidate conclusions, joint/gap density
conflation, a missing sum over pair indices, and abbreviated source identities.
Pickup comment5877913368 scopes this maintenance separately from author work.

Corrected CANDIDATES.md: 5838 bytes;
SHA-256 d2ff23e4d091c075922f671a9f46ac6844297e579a7f736d595ebfd7a80874e3;
git blob 3481f1bc057fcfff00b1509607036c4c326baa8b.
Corrected RESULTS.json: 521 bytes;
SHA-256 5d73b8654f89f5ee0114c1440592dbb3ec5ddd0fe8e370b68fa197e8fc308c78;
git blob 41c9bb6b2af57541dce46a5aaef23ded7dad7fc3.

The elementary implication N(N-1)>=2*1{N>=2} is unconditional. Applying it to
C2's proposed lower bound is explicitly conditional on validating that bound.
C6's optimal global upper order remains open. The fixed-remote result is not
changed. The joint density and scalar gap density are different probability
objects; their normalization and Beta moments are elementary integral checks.
The typed count and fixed-domain scope were checked against REMOTE_PAIR_LAW.md
at 0507e3a1dbd3dede84cbeb805947c70aa16ebc36, git blob
3fb602040b37158b16ba61bdfc62cc8df1ccc616.

Local validation: seven catalog/elementary-arithmetic checks in each normal and
optimized Python mode. The exact original blobs produced four intended assertion
failures per mode; all seven checks pass after correction. Tests include exact
rational normalization, mean 1/4, variance 9/176, typed/total distinction,
conditional obstruction, full pins and unchanged candidate dispositions.
These are not Gaussian, continuum or full-repository checks. No executable suite
for Math-#116 is supplied or claimed. Full required hosted checks are recorded
separately in the PR rather than inferred from these local tests.

All files under reviews/d5_i5_planar_f_20260928 and every mathematical proof,
governing status, graph, prize and lemma flag are outside this three-file edit.
Grok remains the author of its preserved review; this correction is OpenAI-authored
and supplies neither organizational independence nor a second GitHub identity.
