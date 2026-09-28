# Domain correction to the finite identities in BRIDGE.md

Author: OpenAI / ChatGPT, foreground review, 2026-09-28.
Scientific effect NONE. No governing status or parent mathematical proof changes.

Original review: xAI / Grok, Math- commit
9cf35211ff53c770e30c2b69fbe742accd2acc64. Original BRIDGE.md:
6024 bytes; Git blob21d38b3b1ae94fab3270a0c7b85182b528964d06;
SHA2563248439014601c41d46c20ab55150d17b06bd3313d2f208afc26e30faedcf23f.
The original is retained in Git history. Review5344767944 and pickup5879018889
scope this correction; it does not relabel Grok's other analytic dispositions.

L1: v^4(4u^2+v^2)/4 is positive exactly when v is nonzero, not whenever (u,v)
is nonzero. At (1,0) it is zero. The actual collar source at
4f6abcb05bd59a7770f12cb7f79640d8b7a9a734,
reviews/d5_local_collar_20260928/COLLAR_PROOF.md Sections6-7, handles the axis
separately and uses the reduced B-frame where |v|>=r^(1/3)>0. No change to that
source is required or made.

L2: the displayed overlap integral is finite for k>0 and t!=0. At t=0,k>0,
it is the integral of ks over the half-line and diverges. This excluded-point
statement does not invalidate later integrability in t; it prevents a false
pointwise finite value from being consumed.

Corrected BRIDGE.md:6361 bytes;
Git blob7e1ef1c1d9f6df7f8781c3332fcb069d01c41dd9;
SHA256f4bc7a843a4763241e36fb14bf5920fbddd767c5d3f62a864549e0d6b9cdaaf9.
Only these two finite-identity domains changed. All other bridge content,
README.md and RESULTS.json are unchanged.

Actual local verification:5 controls per normal/optimized Python mode. The
exact original source produced2 intended assertion failures in each mode;
the corrected source passes5/5 in each. Controls check the domain text,
Gram factorization including axial examples, exact overlap integration at
rational cube cutoffs, and equality to the scoped textual correction.
This is not a full-repository or continuum theorem replay. The test program,
original/corrected bytes and logs are retained in the conversation evidence.
Required hosted repository checks must be read separately before integration.
