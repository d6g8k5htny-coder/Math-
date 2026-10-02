# Citing this research

Cite the specific proof, calculation, or review you used. This repository brings
together research notes, programs, imported originals and review records with
different recorded contributors. Its hosting account is not a substitute for
the attribution in each artifact.

## Cite an artifact

Include its exact title or object ID, path, full commit SHA and a permanent link.
Retain the author or model lane actually recorded in the source; keep reviewer,
recovery and publication-preparer credits separate. If the source leaves an
author unknown, preserve that uncertainty.

For example, the following identifies a particular source without assigning
authorship to the whole collection:

> OpenAI / ChatGPT (recorded source author). “SIDE24 coefficient in dimensions
> two and three.” Object `SIDE24-COEFFICIENT-D23-20260924-v1`.
> `coefficients/side24_v1/PROOF.md`, Math-, commit
> `de54d1da2f6cdde59df3c34bb50ecd85c25ca333`.
> [Permanent source link](https://github.com/d6g8k5htny-coder/Math-/blob/de54d1da2f6cdde59df3c34bb50ecd85c25ca333/coefficients/side24_v1/PROOF.md).

Use the commit you actually consulted. When discussing a reviewed result, cite
the applicable review as well as the source and preserve its hypotheses and
scope. An original file can retain historical review language; later reviews
are separate records. [Proof availability](PROOF_INDEX.md) helps locate them.

For an imported or recovered artifact, also include its original carrier
identity from the linked manifest or source binding: source repository and
commit/path, or source ID, together with the recorded hash. For example, the
[lifetime-parent manifest](imports/lifetime_parent_20260925/MANIFEST.json)
identifies the original Drive files separately from their repository mirrors.

## Cite a repository snapshot

For a reference to the collection rather than an individual result:

> *Math-: Mathematics — proofs, calculations, and open reviews.* Repository
> snapshot, commit `de54d1da2f6cdde59df3c34bb50ecd85c25ca333`.
> [Permanent snapshot link](https://github.com/d6g8k5htny-coder/Math-/tree/de54d1da2f6cdde59df3c34bb50ecd85c25ca333).

This snapshot reference supplies no collection-wide author list. A citation,
source hash or repository merge does not broaden a mathematical claim or its
recorded review scope.

## Provenance and reuse metadata

Source records distinguish several kinds of material:

- Research notes and calculations record their own author/model lanes and
  dependencies. External mathematical literature cited within them remains
  separately attributed; a literature citation alone does not identify a copied
  source file.
- Imported originals retain their carrier identities: see the
  [hardening-copy ledger](imports/hardening_ebedb780/README.md),
  [contact-exposition binding](imports/transverse_contact_library_20260927/SOURCE_BINDING.json)
  and [Stage E recovery](imports/upper2d_stage_e_20260926/README.md).
- Some original attribution remains unresolved. The pinned
  [GP-DATA-114 source record](https://github.com/d6g8k5htny-coder/Math-/blob/de54d1da2f6cdde59df3c34bb50ecd85c25ca333/imports/gp_data_114_embedded_20260930/SOURCES.json#L6-L8)
  records the original author as unknown and names the recovery author
  separately. The pinned
  [H5 review](https://github.com/d6g8k5htny-coder/Math-/blob/de54d1da2f6cdde59df3c34bb50ecd85c25ca333/imports/upper2d_h5_ledgers_20260926/REVIEW.md#L3-L7)
  records unknown original model/provider provenance.

No project-wide license file is present in the snapshot cited above. The source
records do not provide a complete collection-wide account of creators and reuse
terms. This guide adds citation information and declares no new license terms.

The [README calculation commands](README.md#run-a-calculation) use the Python
standard library. Historical imported numerical scripts have a different
dependency set: [Stage E](imports/upper2d_stage_e_20260926/README.md#numerical-sources-remain-unverified)
records NumPy, SciPy, mpmath and SymPy without locked versions; the
[GP-DATA-114 recovery note](imports/gp_data_114_embedded_20260930/README.md#historical-scope-and-limits)
also identifies its original program's mpmath dependency. The separate
[Lean package](formal/README.md) preserves originals and documented compiler
repairs, with [Lean](formal/lean-toolchain), [mathlib](formal/lakefile.toml) and
[transitive dependencies](formal/lake-manifest.json) pinned. Those dependency
identities do not supply license terms for this collection's research material.
