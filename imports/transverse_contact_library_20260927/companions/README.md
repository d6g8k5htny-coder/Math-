# Original collision-delivery companions

**Publication/custody only. Scientific effect: NONE.** Added 27 September 2026 after the two primary expositions were recovered by PR94. The original source files below are byte-preserved; this page is a new routing note, not part of the old proof.

## Readable source and correction boundary

[COLLISION_TRANSFER_THEOREM.md](COLLISION_TRANSFER_THEOREM.md) is the original expanded transfer exposition, distinct from the consolidated PR25 note. Its Section 3 must be read with the explicitly retained normalization `h/(kappa*r^m) -> 1`; two-sided comparisons alone do not give the sharp constant. The repository's [cumulative-transfer correction](../../../reviews/collision_mechanism_20260925/CUMULATIVE_TRANSFER_CORRECTION.md), blob `044ac5fdaf403a38e33983e31f0ad69f8e76d6d5`, explains that boundary for the consolidated source. This pointer does not amend the recovered original or transfer the correction's review to this expanded file.

[exact_checks.py](exact_checks.py) contains the original local 24-method finite algebra/Schur-complement suite, including the cubic pins, determinant identities, counterexamples and exponent arithmetic. It is not the different-comment hosted script identified in the old receipt. [diagnostic_kernel.py](diagnostic_kernel.py) and [historical/DIAGNOSTIC.json](historical/DIAGNOSTIC.json) are an uncertified, unperiodized numerical prototype and its historical output, not a finite-torus coefficient or error enclosure.

The [transverse exposition](../TRANSVERSE_CONTACT_ASYMPTOTIC.md) and [geometry companion](../GEOMETRY_AND_CUBIC_INDEX.md) remain at their existing PR94 paths. No duplicate source path or changed proof body is introduced for them.

## Original provenance

The source is the original 26,967-byte `COLLISION_GEOMETRY_AND_UNIVERSALITY_20260925.zip`, SHA256 `5c5ea46d7f6be9ecbbfc6712c6625691540621522c6b4b8bc4597a57fa5ba6e7`, Library ID `file_0000000070a881f5b99bf828e7626784`. Its [original manifest](historical/MANIFEST.json), [original delivery README](historical/ORIGINAL_DELIVERY_README.md), and [original verification receipt](historical/VERIFICATION.json) are unchanged bytes. The manifest retains original ZIP-relative paths; it is NOT a manifest of this reorganized Git directory. Match entries by original basename/full hash, with the two primary expositions one directory above. Historical logs and the nested hosted artifact remain in the [complete original archive in Drive](https://drive.google.com/file/d/1NZYSQBxsYp-FzILLO-A8Qtc8etCqKvm1/view). They are not claimed separately published here.

All thirteen original manifest payloads and ZIP CRC were checked again. Original receipt fields named `fresh_local_execution` refer to September 25; they are not current execution claims. The seven original files added in this companion subtree match their original manifest hashes (the manifest itself is bound by the source ZIP).

## Fresh bounded replay

On September 27, after reading the two Python sources, the unchanged local `exact_checks.py` was run in an isolated temporary directory under Python 3.13.5:

```
python -B -S exact_checks.py
python -B -O -S exact_checks.py
```

Both completed with 24 tests passing and exit code 0. [FRESH_REPLAY.json](FRESH_REPLAY.json) binds the script and output digests. The numerical diagnostic was not run. This is a fresh finite-algebra replay, not continuum proof verification, a complete repository test run, mathematical acceptance, or independent review. Hosted PR checks and actual nonauthor reviews remain separate.

The old R2 remainder is unchanged by this publication. Historical material does not activate policy or alter claims, premises, prizes, formal gates, or source-bound review dispositions.
