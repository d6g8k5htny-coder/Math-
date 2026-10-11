Exact repaired-source transformation from PR415 bb3c92.

The new CompactSourceCutoffProof.lean is the exact14614-byte candidate SHA25675be8f6bb1b6915b4ab4bb15d89c99050b68944491ba68665caa71a977f8ca0a reviewed at Math1936110556341 (PASS_NONAUTHOR_STATIC_MINIMAL_REPAIR / NOT_COMPILED). Relative to prior14601-byte proof fe26104f209cb63ef78b48a9a7540c9d56e6bb2f729726febde38cff5a1689be, exactly line138 changes:
old:      (hM.isClosed.isOpen_compl.mem_nhds hxM).mono (by
new:      Filter.eventually_of_mem (hM.isClosed.compl_mem_nhds hxM) (by
All other bytes,21fields,both endpoint headers/premises/witnesses,5private helpers and6inherited literal diagnostics are preserved.

The earlier baseline namespace fixture5936B/6d85955aab50429251c441358a26f4cb6e670ea8f6560b5caaf026d697ede0cd established both exact empty-proof targets and genuine hosted two-goal RED; F2 filled those bodies but encountered the actual line138 compile error. The current repair adds no hypothesis or statement weakening. It addresses only that reported error; other errors may become visible. Full proof/control/kernel/axiom gates remain NOT_RUN at freeze. The unreviewed later anisotropic fragment is excluded and partial controls retain their disclosed different-point limitation.
