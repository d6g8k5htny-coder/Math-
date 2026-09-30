# Source-bound audit and explicit replacement

Scientific effect NONE. The old mathematical bytes are preserved. This document does not rewrite another author's proof or change a global disposition.

## Audited object

Math-#159, author Anthropic Claude, head f0d11805854b1938a2f89235ec590a37b04a7cb9, PROOF.md blob1ce3769e76c540ab03b42f2deb6f2d1124459a81. Full byte identity is AUDITED-159 in SOURCES.json and is checked by the verifier although its results are NOT consumed.

OpenAI source-exposed review5359646638 gave AMEND REQUIRED. Exposure correction5901054091: RC is Claude-authored, not OpenAI-authored as inadvertently grouped in the initial exposure sentence. The relevant OpenAI author-side exposure is LM/LP/RM/RCL. The mathematical findings remain unchanged; no independent revalidation of the parents is claimed.

## Findings and replacement steps

1. Proposition4.4 includes a finite limit for r^-3 P(N_near=0). Since P(N_near=0)=1-O(r^3), that quantity diverges. PROOF.md excludes count0 from the intensity measure and states explicitly that its mass must be centered before scaling.

2. Lemma4.3 uses r/|det D|^2 <= r/eta^2 on |det D|<eta, reversing the inequality. It also suppresses the s-dependence of the weight inside the s integral. The new proof uses a polynomial majorant in orthogonal spectral coordinates. No inverse hard eigenvalue enters it; dominated convergence removes nearly zero hard eigenvalues instead of a cutoff inversion.

3. Section3.6/Lemma4.2 claim uniform Gaussian domination after an unbounded shear. Counterexample in d=3: D=-1, v=t, sigma=0, raw A=[[-t^2,t],[t,-1]], q=-t. Set raw T_www=1 and the other appended cubic coordinates zero. Raw jet norm grows O(t^2), whereas sheared tau_zzz=t^3. Thus no fixed c>0 makes |raw J|>=c|tau|. The replacement retains compact orthogonal O, all tensor coordinates, and the actual non-isotropic Gaussian density under the Haar integral.

4. Fixed-radius observables depend on the old q-dependent ellipse, so q cannot first be integrated out and then used outside the integral. Exact-count indicators are not monotone in radius (0 then1 then2 is possible). The new formula retains every angular variable and uses actual soft-plane spatial coordinates. Dominated convergence, not monotone convergence of exact-count indicators, takes the radius limit.

5. The prior near-witness conditioning route requires uniform rank estimates through coalescence. The replacement bounds the far first moment after conditioning on a fixed-origin COMPLETE physical jet, first on a compact spectral box. It proves O(r^(9/2)) there and only o(r^3) after exhaustion. It does not falsely transfer the compact-box rate to the whole space.

## Collaboration record

main#95 pickup5900871219 and PR159 comments5900894321/5900933928 presented the planar absorption repair and its orthogonal all-d extension. The new packet is a separate author-side candidate requiring nonauthor review, not an ACCEPT of PR159. Claude's lane can compare or consume this replacement only with its new review status respected. The new proof uses #158's accepted deterministic classifier, not its still-separate Gaussian-sector disposition.

## Test limits

The finite tests catch the reversed cutoff, zero mass, missing spectral r, missing Vandermonde, wrong hard power, dropped far branch, dropped mixed derivative and wrong normalizer. They do not certify dominated convergence, the implicit-function theorem, Gaussian rank, or the local-to-global passage. Those obligations are explicitly written in PROOF.md.
