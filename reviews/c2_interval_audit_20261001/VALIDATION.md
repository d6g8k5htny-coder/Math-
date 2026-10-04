# Reviewer-side execution record

Actual performer OpenAI / GPT-6 Astra Pro, numerical reviewer of #223.
This record is not an independent human review and not a source-author replay.

The initial six mathematical tests failed on the deliberate no-op scaffold, then
passed after implementation. Expanded25-method tests found one failure: an
untyped cache key admitted a float alias after caching a Fraction. The reproducer
showed a cache hit for0.5 after Fraction(1,2). Typed cache keys and a new exact
regression produced26 passing mathematical tests. The source/packet11-method
scaffold separately produced14 failures before implementation, then all11 passed.

Final suite:37 tests PASS in each normal and optimized Python mode. The serialized
oracle output is identical in both modes and matches RESULTS.json. All9 exact
rational enclosures are strictly inside the original published endpoints; their
internal widths are <10^-45. There is no binary floating arithmetic in evaluation.
The published40-decimal displays use exact outward integer floor/ceiling.

The cache repair belongs to this new oracle, not the peer library. The exact
Fraction output path was unchanged. Tests of false endpoint shrinkage and omitted
cone terms explicitly reject those assertions; they are not mutations of the
source Gaussian proof. No model-dependent coefficient is numerically integrated.

This reviewer read ia.py, elem.py, gam.py, certificate.py, NOTE.md and RESULTS.json
through the GitHub connector at exact head59a06b65d138994119551059fa336919c07188bf.
It did not locally replay the original source exact.py/pseries derivation or its
full certificate command. DNS prevented an upstream checkout. Local verification
therefore marks historical_sources_checked=false; the hosted workflow must perform
actual source authentication and literal output-binding comparison. No hosted
outcome is anticipated by this author-time record. The real-Git fixtures test
this behavior on temporary repositories rather than fabricate project inputs.

No source branch, source proof, scientific register, prize or formal-scope file was
changed. The numerical review accepts exact expression enclosures, not their
identification with a full persistence law or a finite-lifetime error bound.
