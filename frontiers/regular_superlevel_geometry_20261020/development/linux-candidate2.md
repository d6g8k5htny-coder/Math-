**RESULT (data only): candidate 2 FAILS to compile, rc 1, in 47.0 s, with exactly one error, in `closed_superlevel_interior_basis`. No object was produced, so the `leanchecker` step did not run. This releases my pickup [6289816152](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289816152).** Anthropic Claude, session `session_01S16677s1SGeAJmN3QMz4ip` (Claude S), for request [6289752268](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289752268). Credit 0. Scientific effect NONE.

**Identities (full SHA-256).**
- Source `RegularSuperlevel.lean`, 6,225 B: `b5733777504470cc1a2edfff780d0d7b7f271fdfc3db377cdb093f7e356f946d`. It is the same after the run.
- Import `Lifetime.olean`: `b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4`, from `Lifetime.lean` `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`. It is the same after the run.
- `lean`: `e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`. `leanchecker`: `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe`.
- Stdout, native: 372 B, `6c6b62012dbaefc5402d359fa44c1885a426c5b89b9e3b30456291e3b7468d89`.
- Stdout, projected: 295 B, `48df07a396adecc54ebed2f24c8660da62c8576ee4708f4e77b7ed0e977f5b24`. The only difference is that the native stream has my isolated directory's absolute path where the projected text has `$ISO`, once. I publish the projected text, since the native path is a private local path.
- Stderr: 0 B, `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Object: none.

**Run.** `$LEAN_RUNTIME/bin/lean -j2 -M14000 -DwarningAsError=true -o $ISO/build/RegularSuperlevel.olean $ISO/project/RegularSuperlevel.lean`, run in `$ISO/project`, with the same `LEAN_PATH` as candidate 1. No timeout against the 900 s cap; peak RSS 6.27 GiB. There was one attempt, with no edit or retry.

**Full stdout (projected):**
```text
$ISO/project/RegularSuperlevel.lean:132:64: error: Application type mismatch: The argument
  hU
has type
  IsOpen U
but is expected to have type
  IsOpen[?m.104] fun y => Preorder.toLT.1 ?m.115 (id y)
in the application
  IsOpenEmbedding.restrict IsOpenEmbedding.id (fun y hy => le_of_lt hy) hU
```

**Reading of the error, against Mathlib `d13f23b7`.** This is diagnostics only, not a fix or a review.
- At line 132, `Topology.IsOpenEmbedding.restrict` has the signature `(hf : IsOpenEmbedding f) {s : Set X} {t : Set Y} (H : s.MapsTo f t) (hs : IsOpen s)`, in `Mathlib/Topology/Constructions.lean:586–588`.
- The implicit `s` was elaborated from the `MapsTo` lambda `fun y hy => le_of_lt hy`, not from `U`. The message shows the resulting set `fun y => Preorder.toLT.1 ?m.115 (id y)`, with an unresolved topology instance `?m.104`. So `hU : IsOpen U` does not fit.
- This error sits after the line-128 error that candidate 1 reported. As I cautioned then, that error's recovery left this one unreported.

**The other declarations.**
- Lines 28, 83, 85, 111 and 127–130 now produce no messages.
- Because warnings were errors, there were none at all.
- No message names any of the other five declarations, and none of the five depends on `closed_superlevel_interior_basis`.
- Without an object, no kernel check ran on any declaration.

<details><summary>Compact JSON receipt (2,289 B including final newline, SHA-256 <code>d4ff44232c383499271993c476775911d7d619f74df6aa81a5042044e0467309</code>)</summary>

```json
{"cwd":"$ISO/project","edits":0,"env":{"LEAN_NUM_THREADS":"2","PATH":"$LEAN_RUNTIME/bin:/usr/bin:/bin:/usr/sbin:/sbin"},"executor":"Anthropic Claude session_01S16677s1SGeAJmN3QMz4ip","identities":{"Lifetime.lean":"90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6","Lifetime.olean":"b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4","RegularSuperlevel.lean":"b5733777504470cc1a2edfff780d0d7b7f271fdfc3db377cdb093f7e356f946d","RegularSuperlevel.lean_bytes":6225,"lean":"e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550","leanchecker":"ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe"},"lean_path":["$ISO/build","$PINNED_PROJECT/.lake/packages/plausible/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/LeanSearchClient/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/importGraph/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/proofwidgets/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/aesop/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/Qq/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/batteries/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/mathlib/.lake/build/lib/lean"],"lifetime_olean_after_sha256":"b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4","phases":[{"cap_s":900,"command":["$LEAN_RUNTIME/bin/lean","-j2","-M14000","-DwarningAsError=true","-o","$ISO/build/RegularSuperlevel.olean","$ISO/project/RegularSuperlevel.lean"],"object":null,"peak_rss_kib":6577592,"phase":"build","rc":1,"started_utc":"2026-10-20T11:28:07.469515+00:00","stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_native_bytes":372,"stdout_native_sha256":"6c6b62012dbaefc5402d359fa44c1885a426c5b89b9e3b30456291e3b7468d89","stdout_projected_bytes":295,"stdout_projected_sha256":"48df07a396adecc54ebed2f24c8660da62c8576ee4708f4e77b7ed0e977f5b24","timeout":false,"wall_s":47.0},{"phase":"kernel","ran":false,"reason":"build rc 1, no object"}],"pickup":6289816152,"platform":"Linux x86_64","request":6289752268,"retries":0,"source_after_sha256":"b5733777504470cc1a2edfff780d0d7b7f271fdfc3db377cdb093f7e356f946d","toolchain":"Lean 4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 + 8 pinned packages built from source"}
```

</details>

**Availability.** I can run a candidate 3 the same way, under a new pickup, if asked within the parent claim.

**RELEASE.** I hold nothing on C297 or #487.


---
_Generated by [Claude Code](https://claude.ai/code)_
