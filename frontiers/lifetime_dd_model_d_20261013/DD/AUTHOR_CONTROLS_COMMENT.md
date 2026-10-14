**Controls of note DD — the certificate's files, pinned; the controls, the mutants and the assembly, with their stdout.** Companion of the note comment [6139410118](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139410118). Dylan Roy — delegated AI work; actual performer Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Scientific effect NONE.

**Where the bytes are.** The certificate is too large for one comment (eleven files, about 140 KB). It is pinned at Math- commit `35ae8fbb431a49a3ea15e5bcee299b83360a6348` (branch `claude/dd-model-d-enclosure-wip-20261013`, draft PR Math-#446), directory `frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/`; `MANIFEST.json` there lists every file with its byte count and SHA-256. The files that matter for the reads:

| File | Bytes | SHA-256 |
|---|---|---|
| `dd/ddcore.py` | 25177 | `969963134b8e5a8f8bb09b620b8a34e4a44307b1a4f5086db56f3b40e2f2a54e` |
| `dd/ddbounds.py` | 20822 | `f9f800fcfecc020ca95c372c4caaa74d15f6534bd677ad0357be56cd69fca09b` |
| `dd/ddtaylor.py` | 9096 | `45f07583aaaf60de2435da7c9a0aaaf7353a1516f0ae1c29038740b9b8f43cf6` |
| `dd/ddint.py` | 9298 | `d7b4580cbbab2252ce4e79af5334713c46183338a87bed50cc357b566b37aa9d` |
| `dd/ddvq.py` | 9922 | `79a750d3b8abd7ee6b5088e61313c542c7cea3314b340e8ecaff246859dde74b` |
| `dd/ddgauss.py` | 13823 | `ee77c492c0cac054d4770d72df48a1895e014f7e53588c103ebbed7d4673edd4` |
| `dd/ddS.py` | 8312 | `6dd497c23e5aaa20299887c43e409680dfe09cf993ff0d1992f3b1f367c0fbc2` |
| `dd/dd_exact.py` | 5684 | `22083e43559048cac3e011640f97941efc30723052714a829a3bc767f230f2aa` |
| `dd/dd_controls.py` | 13502 | `e2d25f0c626c2bb141516a35b90888a63b4cd1270f0f110f1f510db3ebb60f69` |
| `dd/dd_mutants.py` | 2954 | `946bc6bffdd80511d6a35df647d2d8ae1163c097338ddd6e7720a9d2d08a0595` |
| `dd/cells_full.json` | 384392 | `7ee91b2bd2a220f96a552e17f1fbfd865af51ae802e9a72ed3930ca82e4a5799` |
| `dd/nodes/nodes_0.json` | 515573 | `bbccebed02243f44a4ffdcb60e42702c2f56ff5ce6245ae1b95fe8c17d64fc62` |
| `dd/nodes/nodes_1.json` | 514894 | `d4eaba682db6b0e52af73425738f57910e08c6448586ef7303055a5878ef3216` |
| `dd/nodes/nodes_2.json` | 515394 | `6dbd0b3651b6a1032ec852c5aa89f31eaf659533ab27bdd743e192e090793f8e` |
| `dd/nodes/nodes_3.json` | 513745 | `332b7087ada03321f8be8b3feeb2c4c7244339f8ec6ddab9e5249eec1383cf5a` |
| `dd/nodes/nodes_4.json` | 514509 | `af9e62f0bad1eb0bbabf30b75222bfe8d1aef84bb74cb9c8c037f606937f04ef` |
| `dd/nodes/nodes_5.json` | 512813 | `7981884f25595ba1ad5b7cf5dc9426bac53207be12eae4877e52355d136bf112` |
| `dd/nodes/nodes_6.json` | 513372 | `07c046145752f06d538de1fb2bd47c6cc7f46945022b9f541768cb3e23b220dc` |
| `dd/nodes/nodes_7.json` | 512785 | `ee11a8363794237e10a108b35f1cd460173d2c5ae75f3970e60d2f4ecab17c0e` |
| `dd/nodes/nodes_8.json` | 512848 | `7f288910d6e60e61e8e8e629f0ff9d45fd366b3ade318346a0fef2b2f2db3f2a` |
| `dd/nodes/nodes_9.json` | 512432 | `da5d2f40075c9faa2c41e53f1fce0527d3f32a1c3fd3bce5e42c2dd034201acd` |
| `dd/nodes/nodes_10.json` | 511649 | `e1f7be65093098cb3a09e21ad7ee5cb1d3d5f68626eb253d03d9321cdbc3e2c4` |
| `dd/nodes/nodes_11.json` | 512631 | `b8c8fc65113af94668dcd5fb7e6d85275d0d19589d1e0cfdd59a6fecd7304c34` |

**The node values** (`dd/nodes/nodes_k.json`, `k = 0..11`: the cells with index `≡ k (mod 12)`) were computed on GitHub-hosted runners by the branch workflow `.github/workflows/dd-wip-shards.yml`, run [38347192184](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38347192184) (`python -B -S ddgauss.py eval cells_full.json nodes_k.json 4 k/12`); the stored files are the run's artifacts byte for byte (artifact ids and digests: `11791621287` `sha256:67053c42b0c5a18f2aade128018d58da568e1f231eabeb9f8293589d0994d2d2`, `11790638150` `sha256:7d46021e4eeb3098aa6643eeeccd85c083b595f523647c92b305b0231eaa92ba`, `11791028629` `sha256:8455f95e8717cb6a9e1b6fd39807c79b8076cb7cda82e6722c0fadc20d8d0b9d`, `11790549514` `sha256:f28988d463d4cee35b6e7d57b4f0874878b10b7b16d13a3655cef496020f8407`, `11791615327` `sha256:331f8dc4fc9a607c577cfbe3d9a224d0977fe467bd52b6676433cd731529c86d`, `11791188253` `sha256:daf485e961ce00bd612d348a43af86c6ea854d30ad4e9f8a9746e10fc65a5b9c`, `11791716094` `sha256:a19cd79fdb60a625749edece584fa7353ee9b669964cdb3c2bac7220ef532021`, `11791655107` `sha256:e38e9271fe507b2a7ab239098325bde86ca71c44131837e84ce37ccd4a1f0fea`, `11790871599` `sha256:0b771d857c35ec14d6fddb66a1645a22c353ec720ee31da8f51c4f1a41362892`, `11790968764` `sha256:2ebae84d17c1f1d104c1fc8828a5535d6666650947a1bd72e01ca20ba967182f`, `11791237139` `sha256:cd5d236d1a19389b6c75dd2c568c2d68d9efa7da07a8e5da73804c5bee30c618`, `11790511456` `sha256:e9e52ae9f5d5570f1c8a7cd746c2f42f227878befcba097ce604a2f19a67b39f`). Anyone can recompute any node: `python3 -c "import ddgauss as G, json; ..."` as in `dd_exact.py`'s sample check, or the whole shard (26–75 minutes on four cores).

**How to replay** (Python 3.11+, standard library only; from `dd/`):
```
python3 -B -S dd_controls.py            # C1–C9, exit 0
python3 -B -S dd_mutants.py             # nine mutants, each must be rejected, exit 0
python3 -B -S dd_exact.py cells_full.json nodes/nodes_0.json ... nodes/nodes_11.json   # tiling, every cell remainder recomputed, 24 node values recomputed, D and the corollary
```
The stdout of each is identical under `python3 -B -O -S` (checked). `dd_exact.py` takes about 20 minutes (the remainder recomputation); `--no-recheck` skips it.

**`dd_controls.py` stdout** (both modes identical):
```
PASS C1a Phi(c>0) v-form 
PASS C1b (2.7) with c > 0 equals the v-form 
PASS C1c (2.7) with c <= 0 equals the v-form 
PASS C1f (2.5) with c > 0 equals the v-form 
PASS C1g (2.5) with c <= 0 equals the v-form 
PASS C1h g_c(psi_e) = (4v^3 - 12cv)^2 
PASS C1d c>0: Phi - R^2/48 = c rho^2 + 3 c^2 rho + 4/3 c^3 
PASS C1e c<=0: Phi - R^2/48 = -m v^4 - 3 m^2 v^2 
PASS C2 c0 = 24 sqrt(pi)/(57600 pi) 0.000235078993144898452895033104821
PASS C2b c0 = 1/(2400 sqrt(pi)) 
PASS C3a half-line moments vs Riemann sums 
PASS C3b completing the square: log pre = -a mu^2/Delta 
PASS C4 I_quad - R^2/48 identity 
PASS C5 |g| <= g~ at 6140 points max ratio 0.9935
PASS C5b I(0, 0) = 20/3 
PASS C6a p1, p2 
PASS C6b E[Z^m p_k(Z)] = m^k E[Z^m] 
PASS C6c Bell polynomials vs finite differences 
PASS C7a C_12(3/10, 1) = 404.1... 404.06565982280193
PASS C7b T_11 has no terms of degree <= 2 
PASS C7c degree 3-4 terms of T_11 
PASS C7d localization: v_lo - eps > sqrt(1 + Bt), E_max <= eps Gmin 
PASS C8a nodes are roots of P4 
PASS C8b weights sum to 2 
PASS C8c rule integrates x^6 exactly (2/7) 
PASS C8d K_4 = 2^9 24^4/(9 (8!)^3) 
PASS C9 v-tail bound: enclosures with v1 = 3 and automatic v1 intersect (tails of relative size O(1)) 
controls: ALL PASS
```

**`dd_mutants.py` stdout:**
```
M1 Gauss weight: REJECTED (exit 1) FAIL C8b weights sum to 2 ; FAIL C8c rule integrates x^6 exactly (2/7) 
M2 kernel recursion: REJECTED (exit 1) 
M3 I_quad coefficient: REJECTED (exit 1) FAIL C7b T_11 has no terms of degree <= 2 
M4 c0: REJECTED (exit 1) FAIL C2 c0 = 24 sqrt(pi)/(57600 pi) 0.000225284035097194350691073392121; FAIL C2b c0 = 1/(2400 sqrt(pi)) 
M5 pointwise bound constant: REJECTED (exit 1) FAIL C5 |g| <= g~ at 6140 points max ratio 1.0877
M6 Gauss error constant: REJECTED (exit 1) FAIL C8d K_4 = 2^9 24^4/(9 (8!)^3) 
M7 Bell polynomial: REJECTED (exit 1) FAIL C6c Bell polynomials vs finite differences 
M8 moment recursion: REJECTED (exit 1) FAIL C3a half-line moments vs Riemann sums 
M9 half-space bound in Lemma 1: REJECTED (exit 1) FAIL C5 |g| <= g~ at 6140 points max ratio 2.1683
mutants: ALL REJECTED
```

**`dd_exact.py` stdout** (both modes identical):
```
C9a: the 2393 cell remainders recomputed and equal to the stored values
C9b: 24 sampled node values recomputed and equal to the stored values
Gauss region: sum [0.0764960787599562839459639907648, 0.0771096748441041862088778512743] (node-width 0.0006135960841479022629138605095), remainder 0.000699415225762334605564277483154
region S: [-0.0000204104527369070204567316057495, -0.0000200429419006537600186550090259]; omega tails 0.0000138351995650080053539807820619; tau tail 0.0000572129033171405130248937123594
D in [0.0757052049785748938015641071813, 0.0778600952308480155728023482430]  width 0.0021548902522731217712382410617
q = J/30 - I~_quad - D in [0.672471569882485317760530985090, 0.674626562011425106198435892820]
(c3 - R_{2/3})(L), d=2, L>=10: [0.0614650917123430310676033072575, 0.0616634928835773005956188082259]
(c3 - R_{2/3})(L), d=2, L>=24: [0.0614658061059116856127442435421, 0.0616627784900086460504778719413]
(c3 - R_{2/3})(L), d=3, L>=10: [0.0772809592715861738273260172417, 0.0776431569847475621732652706293]
(c3 - R_{2/3})(L), d=3, L>=24: [0.0773381398169425878649879319988, 0.0775859764393911481356033558722]
```

**Author-side referee round** (clean context, same session, before posting): lemmas PASS; implementation BLOCK + AMEND as listed in the note's Remark 4, all applied before the final run. Not review evidence.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
_Generated by [Claude Code](https://claude.ai/code)_