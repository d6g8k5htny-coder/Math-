**Controls of note DD, v2 — certificate v2 (exact sliver geometry): the files pinned; the controls, the mutants, the gap control and the assembly, with their stdout.** Companion of note DD v1.3 (the comment above). The v1 controls comment [6139414648](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139414648) and the C10 addenda stay frozen; certificate v1 with C10 is the stored object of Math-#448/#449. Dylan Roy — delegated AI work; actual performer Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Scientific effect NONE.

**What changed from v1.** Two files: `ddvq.py` — `_vcell` enlarges a sliver cell's half-width (by a few units in the last place) until the cell contains both of its endpoints, checked in exact rational arithmetic, so the gaps control C10 bounded in v1 do not arise (C10 on v2: 0 gaps); `dd_mutants.py` — the mutant children run in the driver's interpreter mode and the text check is kept under `-O` (the Codex review's second point on Math-#448). The other nine modules and `cells_full.json` are byte-identical to v1 (10 of 12). The node files were recomputed from scratch on hosted runners; they differ from v1's at 2,136 of the 38,288 nodes, by at most `5.9·10⁻³¹` at an end, every v2 enclosure containing v1's. The assembled `D` is `[0.0757052049785748938015641071809, 0.0778600952308480155728023482430]` (v1: `…071813` at the lower end, the upper end identical); every printed number of the note is unchanged.

**Where the bytes are.** Math- commit `f6985cf75259c2fe0b3a979cbd7c662f5b0fa94e` (branch `claude/dd-model-d-enclosure-wip-20261013`), directory `frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/dd_v2/`; `MANIFEST.json` there lists every file with its byte count and SHA-256. The node-producing modules are byte-identical between the run's commit `045ce4dab04ce4f6970f50e819fe7f0c93fafec2` and this pin.

| File | Bytes | SHA-256 |
|---|---|---|
| `dd_v2/ddcore.py` | 25177 | `969963134b8e5a8f8bb09b620b8a34e4a44307b1a4f5086db56f3b40e2f2a54e` |
| `dd_v2/ddbounds.py` | 20822 | `f9f800fcfecc020ca95c372c4caaa74d15f6534bd677ad0357be56cd69fca09b` |
| `dd_v2/ddtaylor.py` | 9096 | `45f07583aaaf60de2435da7c9a0aaaf7353a1516f0ae1c29038740b9b8f43cf6` |
| `dd_v2/ddint.py` | 9298 | `d7b4580cbbab2252ce4e79af5334713c46183338a87bed50cc357b566b37aa9d` |
| `dd_v2/ddvq.py` | 10585 | `473a7ee18f4b4f5089eba9ddf8eabb6ee15560e75213687dc50c9ef1370e7bdd` |
| `dd_v2/ddgauss.py` | 13823 | `ee77c492c0cac054d4770d72df48a1895e014f7e53588c103ebbed7d4673edd4` |
| `dd_v2/ddS.py` | 8312 | `6dd497c23e5aaa20299887c43e409680dfe09cf993ff0d1992f3b1f367c0fbc2` |
| `dd_v2/dd_exact.py` | 5684 | `22083e43559048cac3e011640f97941efc30723052714a829a3bc767f230f2aa` |
| `dd_v2/dd_controls.py` | 13502 | `e2d25f0c626c2bb141516a35b90888a63b4cd1270f0f110f1f510db3ebb60f69` |
| `dd_v2/dd_mutants.py` | 3200 | `b7e35ee8d5bcd5d1b22861332788597f2ce3378027cf0b74fd19df269d7bc133` |
| `dd_v2/dd_gapcheck.py` | 7030 | `a18fe557eb55e05da3a488681fa3e820673ebaa7965d589e6ca28a0a2eab8a94` |
| `dd_v2/cells_full.json` | 384392 | `7ee91b2bd2a220f96a552e17f1fbfd865af51ae802e9a72ed3930ca82e4a5799` |
| `dd_v2/nodes/nodes_0.json` | 515573 | `dc1688b8f38e8a9524a7524f8a754165b026b125af1b7d08a73024a7e3d6ae86` |
| `dd_v2/nodes/nodes_1.json` | 514894 | `8fadc4adcfdf3b0be55a46641d287231716f3cdcbc0d84f046127b403fd08df0` |
| `dd_v2/nodes/nodes_2.json` | 515394 | `0217900ba8f202737b797d25c2f39cc8bbc303b38414ae19b34be3ee306db568` |
| `dd_v2/nodes/nodes_3.json` | 513745 | `980ee72e4aa49d480c4a2cc2d965e83c989259c43ccb8296ce63ae2c2b1c6c77` |
| `dd_v2/nodes/nodes_4.json` | 514509 | `6a10852c28e9c8d3d36ff31666288ab3f73f92facc24551c296098812de713d8` |
| `dd_v2/nodes/nodes_5.json` | 512813 | `ab42ce7f3335c109343c512b7f9229ac694bf537caee0c2108c12ba836e7e1ce` |
| `dd_v2/nodes/nodes_6.json` | 513372 | `aa6e75b9f923c91c86eaa7ac0e841c0a166e185494344b76560a1f9dce355afb` |
| `dd_v2/nodes/nodes_7.json` | 512785 | `a84dcdd10f8fed4c801acf0cd145a752213051787e2f54176d75e1d1d07d172d` |
| `dd_v2/nodes/nodes_8.json` | 512848 | `fb0385ffb1d71b747823845e0d51cb3f8237d755f9bd1a3c5c4d86bc28465789` |
| `dd_v2/nodes/nodes_9.json` | 512432 | `2d94e3ee23e8f2fa7ff1ba73f183aaccb0bc886c2fd918e448f17b7f22c46688` |
| `dd_v2/nodes/nodes_10.json` | 511649 | `06914e48683e19fa8f94ba9e815ef5fda6ed152eb2641ebba13117589c66e833` |
| `dd_v2/nodes/nodes_11.json` | 512631 | `0ce3496f93e0e766d44aaf7dcda21a0ae4db8f7c58c4ecb9f6cccad789cbf179` |
| `dd_v2/results/controls_stdout.txt` | 1236 | `69dfcebc5a7a913dec1e631d1da2682d0527c17a5729a92fbe29e1e469eb37a6` |
| `dd_v2/results/controls_stdout_O.txt` | 1236 | `69dfcebc5a7a913dec1e631d1da2682d0527c17a5729a92fbe29e1e469eb37a6` |
| `dd_v2/results/mutants_stdout.txt` | 830 | `49996326c9604ef3bd3c0ea004f93667dbc4c40c4affe45a3db4a7580dccaa0c` |
| `dd_v2/results/mutants_stdout_O.txt` | 830 | `49996326c9604ef3bd3c0ea004f93667dbc4c40c4affe45a3db4a7580dccaa0c` |
| `dd_v2/results/gapcheck_stdout.txt` | 435 | `7b95eab12608b27c8bcb928e1331cac6d93c1deaecc75b364aed5ebdb4ffa2bd` |
| `dd_v2/results/gapcheck_stdout_O.txt` | 435 | `7b95eab12608b27c8bcb928e1331cac6d93c1deaecc75b364aed5ebdb4ffa2bd` |
| `dd_v2/results/assembly_stdout.txt` | 1131 | `0fcb9d8387df73ecaa269929ac6ba373e309f951bbcfffc2549e746e27b64695` |
| `dd_v2/results/assembly_stdout_O.txt` | 1131 | `0fcb9d8387df73ecaa269929ac6ba373e309f951bbcfffc2549e746e27b64695` |

**The node values** (`dd_v2/nodes/nodes_k.json`, `k = 0..11`: the cells with index `≡ k (mod 12)`) were computed on GitHub-hosted runners by the branch workflow `.github/workflows/dd-wip-shards.yml` (dispatched with `dir: dd_v2`), run [38367190632](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38367190632) at `045ce4da`, attempt 1 (`python -B -S ddgauss.py eval cells_full.json nodes_k.json 4 k/12`; 29–70 minutes per shard); the stored files are the run's artifacts byte for byte (artifact ids and digests: `11799414242` `sha256:271cec3dbe10c8d30eabb8e769fb80ac00ea0b034aebd919428d1206b163996b`, `11800353309` `sha256:1af957ed90caf95aa927b740e7a44431ea406f5b87433e1a4d204fc06bac929d`, `11799759065` `sha256:574a8ad32f196b011be9a9fc47ca1002dec53c8cb3205d36dfeff0ab042a2f68`, `11798444229` `sha256:1f1d23280020405e33e7dc59eda5ee5a120a4829906c544285e5abda064d39bf`, `11799723294` `sha256:bdadc77c511bdb1b52722d79a4fdb60f7d2f426706e3cbd89e727aaeea8a2f74`, `11799668649` `sha256:09755a05e584f17520affb08a31ffd6d811a22cac5bee2334892cb9c0afd92f8`, `11800173994` `sha256:600c2d605b0a7ce53a54df17e99751c24a903f33960fe731a9dc40af1b9131af`, `11800521321` `sha256:ac7641c6c3c584fa9dd88f78b5dc1f41df7d2975aae9dd45a7875513fa183fba`, `11799564274` `sha256:4bc1cf5267effda40e4941d1abce25822104fba92a8d324b77551d6b26a89d85`, `11799931040` `sha256:eda06d807bbe719f0ccc717bad1c86ed53a3e360dad450b8f82d6f22887ebc64`, `11800352666` `sha256:61513b9036a8c5dd7e203d16004cb59d63600a59b7ebb33e9faded80a2d818e1`, `11800687305` `sha256:4accfa903928cb24c7f216ebb4baaddc3f7ca4ca1a16ef4254cb3558c50a06ec`).

**How to replay** (Python 3.11+, standard library only; from `dd_v2/`):
```
python3 -B -S dd_controls.py            # C1–C9, exit 0
python3 -B -S dd_mutants.py             # nine mutants, each must be rejected, exit 0
python3 -B -S dd_gapcheck.py cells_full.json 2        # C10: 0 gaps
python3 -B -S dd_exact.py cells_full.json nodes/nodes_0.json ... nodes/nodes_11.json   # tiling, every cell remainder recomputed, 24 node values recomputed, D and the corollary
```
The stdout of each is identical under `python3 -B -O -S` (checked). `dd_exact.py` takes about 20 minutes; `--no-recheck` skips the remainder recomputation.

**`dd_controls.py` stdout** (both modes identical; identical to v1):
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

**`dd_mutants.py` stdout** (both modes identical; identical to v1):
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

**`dd_gapcheck.py` stdout** (both modes identical):
```
400/2393 cells
  800/2393 cells
  1200/2393 cells
  1600/2393 cells
  2000/2393 cells
narrow-regime nodes: 2771 of 38288; nodes with a sliver gap: 0 (0 gaps; every sliver cell covers its left end and the replicated sliver geometry equals ddvq.initial_cells at every narrow node); largest total gap length at a node: 0; largest |rho H| omission at a node: 0
Delta (the omitted contribution to D lies in this interval): [0E-40, 0E-40]
```

**`dd_exact.py` stdout** (both modes identical):
```
C9a: the 2393 cell remainders recomputed and equal to the stored values
C9b: 24 sampled node values recomputed and equal to the stored values
Gauss region: sum [0.0764960787599562839459639907644, 0.0771096748441041862088778512743] (node-width 0.0006135960841479022629138605099), remainder 0.000699415225762334605564277483154
region S: [-0.0000204104527369070204567316057495, -0.0000200429419006537600186550090259]; omega tails 0.0000138351995650080053539807820619; tau tail 0.0000572129033171405130248937123594
D in [0.0757052049785748938015641071809, 0.0778600952308480155728023482430]  width 0.0021548902522731217712382410621
q = J/30 - I~_quad - D in [0.672471569882485317760530985090, 0.674626562011425106198435892821]
(c3 - R_{2/3})(L), d=2, L>=10: [0.0614650917123430310676033072575, 0.0616634928835773005956188082260]
(c3 - R_{2/3})(L), d=2, L>=24: [0.0614658061059116856127442435421, 0.0616627784900086460504778719413]
(c3 - R_{2/3})(L), d=3, L>=10: [0.0772809592715861738273260172417, 0.0776431569847475621732652706295]
(c3 - R_{2/3})(L), d=3, L>=24: [0.0773381398169425878649879319988, 0.0775859764393911481356033558724]
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
_Generated by [Claude Code](https://claude.ai/code)_