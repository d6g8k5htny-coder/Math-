# Cap I4: explicit d=3 spectral adapter

**Author-side analytic proposal; not a new Lean proof. Scientific/status effect NONE.**

The transverse matrix is 2x2. An entry-coordinate density bound
`p(B)<=C0 exp(-c||B||_F^2)` gives the positive ordered-eigenvalue upper density
`pi C0 (Lambda-lambda)exp(-c(lambda^2+Lambda^2))` by two linear changes and planar polar coordinates. The proof fixes the often-hidden entry-volume/Frobenius-volume factor sqrt(2). It needs neither matrix-law isotropy nor measurable eigenvectors.

Keeping one hard-eigenvalue factor gives a depth numerator bounded by

    C_depth r^5,
    C_depth=256 pi C0 [K^2(1+K)/4] [D^3/3+ED^2/2]
      * [M9 sqrt(pi)/(4c^(3/2))+60/c^6],
    D=4K^2/(3k_floor), E=3K/2, M9>=E[J^9].

This is a sufficient ninth-moment envelope, not an optimality claim or an evaluated field constant. The full normalizer, actual density/residual inputs, measurable cap implication and weighted fourth-derivative moment remain explicit. The source field's compact-family inputs come from P; no unrestricted k,L,d statement is added.

`PROOF.md` gives the complete ordinary proof, source identities, a concrete proposed Lean measure-domination signature, and the exact already-existing polar API at the project mathlib pin. `SOURCES.json` authenticates this packet's mathematical/test files; hashes establish identity, not acceptance. The original Cap branch, its separate engineering child, the formal manifests, and the active integration queue are untouched.

## Replay

```sh
python -B -S replay.py --mode normal
python -B -O -S replay.py --mode optimized
```

Each mode authenticates packet membership and hashes, executes all 14 finite-algebra tests, then executes five altered-formula controls and requires the exact intended failed-test set with no test errors. Wrong exit, malformed result, skipped/missing tests, duplicate JSON keys, or an unexpected rejection reason is not success. Outputs are deterministic JSON summaries; source hashes are read again after execution. Run from this directory or pass the script's full path. Standard library only.

The tests do not prove the continuum source, and the proposed Lean signature has not been implemented/compiled. The original kernel-checked CapI4 consumer remains conditional. No self-merge or independent mathematical acceptance is claimed. Actual author: OpenAI / GPT-6 Astra Pro, session `cap-i4-explicit-d3-adapter-20261005`; Dylan Roy delegated work. Pickup main#229/6006586304.
