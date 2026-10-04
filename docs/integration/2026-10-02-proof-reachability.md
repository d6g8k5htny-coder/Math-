# Proof reachability on `main`: every `frontiers/*/PROOF.md` at one cut

Cut: `0fda855b8ee0c26d597bb033e0b4cdfb6d07e5e6` (Math- `main`, 2 October 2026; the integration of #246).

**Scope: source availability only.** This table records where each frontier proof lives at the cut, its exact git blob, the pull request that introduced it, and the first-parent commit on `main` that integrated it. It contains no verdict, grade, summary or quotation of any review. It changes no claim, graph node, STATUS row, register or disposition. A merge, a passing check or a row here is **not** mathematical acceptance. Each packet's own `README.md`, `SOURCES.json` and pull-request conversation carry its status and its review records.

It continues the navigation refresh of #163, which covers the packets integrated from 26 to 29 September, and it was picked up in #163 comment 5961771586. `PROOF_INDEX.md` is left unchanged; at the cut it names 11 of the 62 proofs below, and the other 51 are reachable from here.

## How each row is derived

- **Blob:** `git rev-parse <cut>:frontiers/<packet>/PROOF.md`.
- **Integration commit:** the last line of `git log <cut> --first-parent --diff-filter=A -- <path>`, the first-parent commit of `main` that added the path; its committer date is shown.
- **Introduced by:** the pull request that GitHub associates with the commit that first added the path.
- **In `PROOF_INDEX.md`:** whether `PROOF_INDEX.md` at the cut names the packet folder.

`tools/check_proof_reachability.py` re-derives every column except "Introduced by" from git; that column comes from GitHub's association of commits with pull requests. The checker also verifies that every `frontiers/*/PROOF.md` at the cut appears exactly once; that the rows follow the integration order below; that the commit and blob prefixes in the second table agree with the first; and that no row of either table carries a verdict word.

## The table (in order of integration)

Rows are ordered by the position of their integration commit in `git rev-list --first-parent --reverse <cut>`, the order in which `main` received them. Packets integrated by the same commit are listed alphabetically. A committer date can be earlier than a date in an earlier row; the position, not the date, sets the order.

| Packet | `PROOF.md` blob at the cut | Introduced by | Integration commit (date) | In `PROOF_INDEX.md` |
|---|---|---|---|---|
| [`price_budget_20260924`](../../frontiers/price_budget_20260924/PROOF.md) | `9b17d179d2408dae9ea497d3c6e5c6538d2c3b8b` | [#4](https://github.com/d6g8k5htny-coder/Math-/pull/4) | `f3a6e5540c21` (2026-09-24) | yes |
| [`full_price_20260924`](../../frontiers/full_price_20260924/PROOF.md) | `582180e41dca0ad815ad0f18574df42040912149` | [#5](https://github.com/d6g8k5htny-coder/Math-/pull/5) | `a0cd46d22ffe` (2026-09-24) | yes |
| [`remote_window_20260924`](../../frontiers/remote_window_20260924/PROOF.md) | `b383bfcc88ec4ad497dff01fb6640e429ba24a84` | [#6](https://github.com/d6g8k5htny-coder/Math-/pull/6) | `593adcaa89a2` (2026-09-24) | yes |
| [`axial_density_20260925`](../../frontiers/axial_density_20260925/PROOF.md) | `a72418d78fd3c1ec96260dbf19f9a2f3f4ca35ba` | [#21](https://github.com/d6g8k5htny-coder/Math-/pull/21) | `c3cee9bbdeee` (2026-09-25) | yes |
| [`rn_annulus_bridge_20260925`](../../frontiers/rn_annulus_bridge_20260925/PROOF.md) | `6f317515b3d417661f86e2fed09bc7d950899c2b` | [#28](https://github.com/d6g8k5htny-coder/Math-/pull/28) | `f2899d8f4983` (2026-09-25) | yes |
| [`rn_thin_tube_20260925`](../../frontiers/rn_thin_tube_20260925/PROOF.md) | `338d92d1f6be01da01950c853aaecbffa4231c47` | [#22](https://github.com/d6g8k5htny-coder/Math-/pull/22) | `760340e921ac` (2026-09-25) | yes |
| [`rn_mesoscopic_20260925`](../../frontiers/rn_mesoscopic_20260925/PROOF.md) | `0ef068fe7cc17a7c3405536be04a02fc964c2494` | [#7](https://github.com/d6g8k5htny-coder/Math-/pull/7) | `c021278be89b` (2026-09-27) | no |
| [`intermediate_window_20260928`](../../frontiers/intermediate_window_20260928/PROOF.md) | `f53a527ce0204fda271f24730b62b4223a5e43ec` | [#107](https://github.com/d6g8k5htny-coder/Math-/pull/107) | `541d4e9daf3f` (2026-09-28) | no |
| [`remote_collision_20260928`](../../frontiers/remote_collision_20260928/PROOF.md) | `7b48a88e2af54e759e89a8c8219573bb450a65ea` | [#114](https://github.com/d6g8k5htny-coder/Math-/pull/114) | `5a5b97d2c518` (2026-09-28) | yes |
| [`remote_singleton_law_20260928`](../../frontiers/remote_singleton_law_20260928/PROOF.md) | `2b01956978d7f1d917e929a955f2588263a87426` | [#115](https://github.com/d6g8k5htny-coder/Math-/pull/115) | `4b2aa45b2f99` (2026-09-28) | no |
| [`p15_bipartite_overlap_20260928`](../../frontiers/p15_bipartite_overlap_20260928/PROOF.md) | `8ad826ecb374cc733e3a547bdba0ba63cad10c08` | [#124](https://github.com/d6g8k5htny-coder/Math-/pull/124) | `d39dbbc25c25` (2026-09-28) | no |
| [`p15_tail_load_20260928`](../../frontiers/p15_tail_load_20260928/PROOF.md) | `8187908dfd220cb833b94f82c451ef4c0e45e367` | [#124](https://github.com/d6g8k5htny-coder/Math-/pull/124) | `d39dbbc25c25` (2026-09-28) | no |
| [`remote_height_decoupling_20260928`](../../frontiers/remote_height_decoupling_20260928/PROOF.md) | `4d7af587db20515955585732d8150d912c89c0e4` | [#124](https://github.com/d6g8k5htny-coder/Math-/pull/124) | `d39dbbc25c25` (2026-09-28) | no |
| [`elder_dimension_lift_20260928`](../../frontiers/elder_dimension_lift_20260928/PROOF.md) | `7303bd791a68a1139251f0f6e403a9f7cc89b006` | [#129](https://github.com/d6g8k5htny-coder/Math-/pull/129) | `e7f8aca41c30` (2026-09-28) | no |
| [`remote_inverse_separation_20260928`](../../frontiers/remote_inverse_separation_20260928/PROOF.md) | `1b24d0f6d07f84706a0a8e9b25e111e6eff93a2b` | [#131](https://github.com/d6g8k5htny-coder/Math-/pull/131) | `0b0b281989db` (2026-09-29) | no |
| [`remote_mixed_inverse_20260929`](../../frontiers/remote_mixed_inverse_20260929/PROOF.md) | `975d8211a30be05cb337c81036a0c8de8a9f4264` | [#134](https://github.com/d6g8k5htny-coder/Math-/pull/134) | `5bd924969bb2` (2026-09-29) | no |
| [`unrestricted_selection_difference_20260929`](../../frontiers/unrestricted_selection_difference_20260929/PROOF.md) | `5a55b179a974a90c65d257f3f93765cc6fb30bb8` | [#134](https://github.com/d6g8k5htny-coder/Math-/pull/134) | `5bd924969bb2` (2026-09-29) | no |
| [`sard_g_a2_parameter_20260929`](../../frontiers/sard_g_a2_parameter_20260929/PROOF.md) | `36bbc0c30a451eb8d568717552bb462c0f96685c` | [#139](https://github.com/d6g8k5htny-coder/Math-/pull/139) | `e947ade51def` (2026-09-29) | no |
| [`sard_g_a2_regularity_20260929`](../../frontiers/sard_g_a2_regularity_20260929/PROOF.md) | `8ea2c35375085905986a144c44b522a0b397cee7` | [#139](https://github.com/d6g8k5htny-coder/Math-/pull/139) | `e947ade51def` (2026-09-29) | no |
| [`sard_g_pinned_transfer_20260929`](../../frontiers/sard_g_pinned_transfer_20260929/PROOF.md) | `314e38c6f5f2bd78da79e423f30a341a3d45e22c` | [#139](https://github.com/d6g8k5htny-coder/Math-/pull/139) | `e947ade51def` (2026-09-29) | no |
| [`sard_g_robust_charts_20260929`](../../frontiers/sard_g_robust_charts_20260929/PROOF.md) | `7e2237063a8dd0120e9d5bd15a3caaa32e8495fa` | [#139](https://github.com/d6g8k5htny-coder/Math-/pull/139) | `e947ade51def` (2026-09-29) | no |
| [`c6_factorial_moment_20260929`](../../frontiers/c6_factorial_moment_20260929/PROOF.md) | `f5bd013b7134be9efd246fc9bbb8d18ad5a728bc` | [#140](https://github.com/d6g8k5htny-coder/Math-/pull/140) | `e7d975f446c0` (2026-09-29) | no |
| [`c6_sharpened_20260929`](../../frontiers/c6_sharpened_20260929/PROOF.md) | `70ba19726a9114bfceae04d021095e6c8eed5026` | [#142](https://github.com/d6g8k5htny-coder/Math-/pull/142) | `bf7c45f5e180` (2026-09-29) | no |
| [`c6_count_cap_boundary_20260929`](../../frontiers/c6_count_cap_boundary_20260929/PROOF.md) | `3d4c28a4ca8784b6c71c13ca804a817a6cb52e6f` | [#146](https://github.com/d6g8k5htny-coder/Math-/pull/146) | `52ed202a094e` (2026-09-29) | no |
| [`c6_fourier_cutoff_20260929`](../../frontiers/c6_fourier_cutoff_20260929/PROOF.md) | `1d9177a259654df0fb7c558fcb803685e09608d2` | [#148](https://github.com/d6g8k5htny-coder/Math-/pull/148) | `4d062e2a976a` (2026-09-29) | yes |
| [`d5_dimension_lift_20260929`](../../frontiers/d5_dimension_lift_20260929/PROOF.md) | `9d82c707fdb17d3072a8930f26dabedf59e456fc` | [#141](https://github.com/d6g8k5htny-coder/Math-/pull/141) | `e1ca400b3414` (2026-09-29) | yes |
| [`c6_palm_route_20260929`](../../frontiers/c6_palm_route_20260929/PROOF.md) | `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` | [#145](https://github.com/d6g8k5htny-coder/Math-/pull/145) | `820d4435c5f1` (2026-09-29) | yes |
| [`elder_lower_all_d_20260929`](../../frontiers/elder_lower_all_d_20260929/PROOF.md) | `7f41c9e315be0a7985d4c770a11a2cdf717bd46a` | [#149](https://github.com/d6g8k5htny-coder/Math-/pull/149) | `21244e5ea0b0` (2026-09-29) | no |
| [`c7_total_bounded_20260929`](../../frontiers/c7_total_bounded_20260929/PROOF.md) | `28748b086ec6761ef467dc67cba475fbdf8b7455` | [#150](https://github.com/d6g8k5htny-coder/Math-/pull/150) | `7f438fca8b7f` (2026-09-29) | no |
| [`side24_periodization_20260929`](../../frontiers/side24_periodization_20260929/PROOF.md) | `1a84f215c53d62918f37517300c350693da62586` | [#144](https://github.com/d6g8k5htny-coder/Math-/pull/144) | `0cd0b821972e` (2026-09-29) | no |
| [`c6_rare_cluster_laws_20260929`](../../frontiers/c6_rare_cluster_laws_20260929/PROOF.md) | `2ab625cedfc2e47575c4a7fa4853413418c532da` | [#153](https://github.com/d6g8k5htny-coder/Math-/pull/153) | `190cf2bd4f31` (2026-09-29) | yes |
| [`side24_periodization_remainder_20260929`](../../frontiers/side24_periodization_remainder_20260929/PROOF.md) | `0329156897fc59b4bb88ad0228eaaade15f3d687` | [#156](https://github.com/d6g8k5htny-coder/Math-/pull/156) | `8ba851fb2add` (2026-09-29) | no |
| [`c7_zero_gap_limit_20260929`](../../frontiers/c7_zero_gap_limit_20260929/PROOF.md) | `5b6328ea3d6afcbeb731698b3834e536f72d1bcb` | [#155](https://github.com/d6g8k5htny-coder/Math-/pull/155) | `7a1cb09a9d58` (2026-09-29) | no |
| [`local_cluster_tightness_20260929`](../../frontiers/local_cluster_tightness_20260929/PROOF.md) | `adffa6916d0fb57fede0486b5eb3bc6afc127c07` | [#161](https://github.com/d6g8k5htny-coder/Math-/pull/161) | `5c484bfd4b15` (2026-09-29) | no |
| [`planar_cubic_cluster_20260929`](../../frontiers/planar_cubic_cluster_20260929/PROOF.md) | `bb446d08db8a944537a743ad550b88c1c2ad5758` | [#158](https://github.com/d6g8k5htny-coder/Math-/pull/158) | `aa288385af93` (2026-09-29) | no |
| [`c6_marked_fourier_20260929`](../../frontiers/c6_marked_fourier_20260929/PROOF.md) | `efb702f601eb0c0a24dad6d125061158158867b9` | [#157](https://github.com/d6g8k5htny-coder/Math-/pull/157) | `2479a7c2bcad` (2026-09-29) | no |
| [`c6_cluster_law_20260929`](../../frontiers/c6_cluster_law_20260929/PROOF.md) | `ba492c8e62e58bfc055fc8254c790e893d346ba5` | [#159](https://github.com/d6g8k5htny-coder/Math-/pull/159) | `98fdb54954a2` (2026-09-29) | no |
| [`cluster_exponential_weight_20260930`](../../frontiers/cluster_exponential_weight_20260930/PROOF.md) | `bf1268b9c18ec05561fd9b14c645ef0b8e530484` | [#164](https://github.com/d6g8k5htny-coder/Math-/pull/164) | `7d0c89a5bb77` (2026-09-29) | no |
| [`spectral_cluster_closure_20260929`](../../frontiers/spectral_cluster_closure_20260929/PROOF.md) | `16c56821b52fd76b0be791622b9c3809eafde75a` | [#162](https://github.com/d6g8k5htny-coder/Math-/pull/162) | `358f2562efbc` (2026-09-29) | no |
| [`lifetime_moment_boundary_20260930`](../../frontiers/lifetime_moment_boundary_20260930/PROOF.md) | `d5ee8abee120a8bec2f6c470e517ff9db4645183` | [#177](https://github.com/d6g8k5htny-coder/Math-/pull/177) | `dda8991f18cb` (2026-09-30) | no |
| [`radial_rate_20260930`](../../frontiers/radial_rate_20260930/PROOF.md) | `65f24b1f9a7b80522a2ee059f5f6877c9f970f0d` | [#176](https://github.com/d6g8k5htny-coder/Math-/pull/176) | `7ca3eb00534d` (2026-09-30) | no |
| [`extreme_cluster_sampling_20260930`](../../frontiers/extreme_cluster_sampling_20260930/PROOF.md) | `19a6044f2066643b5baab34ce5b6b6efb431e84a` | [#169](https://github.com/d6g8k5htny-coder/Math-/pull/169) | `f430fdecbb1d` (2026-09-30) | no |
| [`fixed_r_inverse_lifetime_20260930`](../../frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md) | `0d4018777d13672c1de1696525512e80b23b7c3c` | [#182](https://github.com/d6g8k5htny-coder/Math-/pull/182) | `2a10ed34e037` (2026-09-30) | no |
| [`local_elder_geometry_20260930`](../../frontiers/local_elder_geometry_20260930/PROOF.md) | `ef2aa57959ea9f721bbf2316ce94cf616c1c9113` | [#170](https://github.com/d6g8k5htny-coder/Math-/pull/170) | `fa2e9909d8cc` (2026-09-30) | no |
| [`concave_fibre_elder_20260930`](../../frontiers/concave_fibre_elder_20260930/PROOF.md) | `923d3236b5291a29bd162937f172190db84dcef5` | [#175](https://github.com/d6g8k5htny-coder/Math-/pull/175) | `eb659bd37d61` (2026-10-01) | no |
| [`elder_partner_extremes_20260930`](../../frontiers/elder_partner_extremes_20260930/PROOF.md) | `91f88e392fb8aa947dac4fc81c2b45f783fa66cd` | [#181](https://github.com/d6g8k5htny-coder/Math-/pull/181) | `443212fb4d84` (2026-10-01) | no |
| [`remainder_vanishing_20260930`](../../frontiers/remainder_vanishing_20260930/PROOF.md) | `441152dfc1d8d00cb268cebdb0394212a5bfacdb` | [#191](https://github.com/d6g8k5htny-coder/Math-/pull/191) | `955654747c0e` (2026-10-01) | no |
| [`elder_selected_extremes_20260930`](../../frontiers/elder_selected_extremes_20260930/PROOF.md) | `1310dc11bae684a9889548d1e764e83381b39d57` | [#179](https://github.com/d6g8k5htny-coder/Math-/pull/179) | `6e5f36d7641b` (2026-10-01) | no |
| [`remainder_rate_20260930`](../../frontiers/remainder_rate_20260930/PROOF.md) | `abfb98ae41d66a86d3cb094162db6547d0f29e7e` | [#198](https://github.com/d6g8k5htny-coder/Math-/pull/198) | `124c37d92181` (2026-10-01) | no |
| [`far_elder_rate_20260930`](../../frontiers/far_elder_rate_20260930/PROOF.md) | `072601145601a1021037a2e91bf8826c1c971ecc` | [#187](https://github.com/d6g8k5htny-coder/Math-/pull/187) | `c2f1270d2819` (2026-10-01) | no |
| [`short_bar_endpoint_law_20261001`](../../frontiers/short_bar_endpoint_law_20261001/PROOF.md) | `0d47dbc1d92863d8c51b918aa47d1fa8b605cfdc` | [#221](https://github.com/d6g8k5htny-coder/Math-/pull/221) | `f166ef52e5ca` (2026-10-01) | no |
| [`c2_finite_jet_transfer_20261001`](../../frontiers/c2_finite_jet_transfer_20261001/PROOF.md) | `54cc4a1ae274842bc2c01f9c207549e7b07de7bc` | [#232](https://github.com/d6g8k5htny-coder/Math-/pull/232) | `7fe06b01489a` (2026-10-01) | no |
| [`cusp_second_order_20261001`](../../frontiers/cusp_second_order_20261001/PROOF.md) | `f6df5a7356a54771b0052e42a864a140709903ad` | [#207](https://github.com/d6g8k5htny-coder/Math-/pull/207) | `566b1a143ec2` (2026-10-01) | no |
| [`candidate_third_order_20261001`](../../frontiers/candidate_third_order_20261001/PROOF.md) | `70ca57ef05199e75417d7d57928c1e1c93bf944e` | [#218](https://github.com/d6g8k5htny-coder/Math-/pull/218) | `fb6ee97bc791` (2026-10-01) | no |
| [`elder_third_order_20261001`](../../frontiers/elder_third_order_20261001/PROOF.md) | `c8767ddecf1041d234f685e95af582073a7be393` | [#220](https://github.com/d6g8k5htny-coder/Math-/pull/220) | `0d797780c2e3` (2026-10-01) | no |
| [`third_order_rate_20261001`](../../frontiers/third_order_rate_20261001/PROOF.md) | `110ed33a57902bef11873807e722fde3888b59fb` | [#229](https://github.com/d6g8k5htny-coder/Math-/pull/229) | `6f74f7a77bae` (2026-10-01) | no |
| [`elder_cusp_parity_20261002`](../../frontiers/elder_cusp_parity_20261002/PROOF.md) | `16a1db0658918057ff741df888c13702763d9919` | [#240](https://github.com/d6g8k5htny-coder/Math-/pull/240) | `7636cae5c386` (2026-10-02) | no |
| [`separated_fold_multiplicity_20261002`](../../frontiers/separated_fold_multiplicity_20261002/PROOF.md) | `026cf5237510018d466380683b7679c2de977845` | [#239](https://github.com/d6g8k5htny-coder/Math-/pull/239) | `240a9bfa06af` (2026-10-02) | no |
| [`subpin_collision_20261002`](../../frontiers/subpin_collision_20261002/PROOF.md) | `4d903d0f834fb2077257104cd91822fe253dde8d` | [#245](https://github.com/d6g8k5htny-coder/Math-/pull/245) | `2d8616ef1b45` (2026-10-02) | no |
| [`soft_rejected_pairs_20261002`](../../frontiers/soft_rejected_pairs_20261002/PROOF.md) | `271412dbc96a29590f5f805258e15c9e335cb430` | [#242](https://github.com/d6g8k5htny-coder/Math-/pull/242) | `54c6759e8434` (2026-10-02) | no |
| [`soft_fold_limit_20261002`](../../frontiers/soft_fold_limit_20261002/PROOF.md) | `6502cf7ba2edee47761e40308c15b7563b06d1f8` | [#243](https://github.com/d6g8k5htny-coder/Math-/pull/243) | `fa8b0d219e41` (2026-10-02) | no |
| [`soft_closed_form_20261002`](../../frontiers/soft_closed_form_20261002/PROOF.md) | `c69f92b1076399fb9f8917bb273e15348b0a497e` | [#244](https://github.com/d6g8k5htny-coder/Math-/pull/244) | `07320089a9c6` (2026-10-02) | no |

Some integration commits brought several packets at once: `d39dbbc` (#124, three packets), `5bd9249` (#134, two packets) and `e947ade` (#139, four packets).

## The soft fold-scale chain #242 → #243 → #244 (integrated 2 October)

| Packet | PR | Integration commit | `PROOF.md` blob | Landing receipt on main#229 |
|---|---|---|---|---|
| `soft_rejected_pairs_20261002` | #242 | `54c6759e8434` | `271412dbc96a` | 5959229499 |
| `soft_fold_limit_20261002` | #243 | `fa8b0d219e41` | `6502cf7ba2ed` | 5959530308 |
| `soft_closed_form_20261002` | #244 | `07320089a9c6` | `c69f92b10763` | 5959837508 |

Limits, stated so that the chain is not over-read:
- **What they concern.** The three packets concern the soft fold-scale model of #242: its rejected set, its fold-scale limit, and its closed form.
- **What they do not establish.** They do not establish the finite-`r` transfer of the model decision to the actual field, which Conjecture 7 needs.
- **Later model-level work.** It lives in issue comments on main#229, not in repository sources, so it is not indexed here. This includes the signed elder margin (5959038812, amended in 5961281898), exact-pin decision stability (5961415030), and the signed-coordinate and level-band bounds (5957815904, 5959878294, 5959920397).
- **Where the status lives.** Review records and status are in each PR's conversation and disposition block.

<!-- post-c126:start -->
## Post-C126 supplement — 3 October 2026

Post-C126 cut: `bbe85e270f2c8b747f2d5d9477c86e86e323fe15`.

The original document above, including its 62-row inventory and statements about
then-available sources, is preserved byte for byte from #247 v1.1 (`ee087cea`).
This supplement records availability at the later cut where #261 incorporated
C124. It does not update the mathematical scope of any historical statement.
The [69-packet historical record](https://github.com/d6g8k5htny-coder/Math-/blob/4ff4f1dacd8ab4f22c8e5307fb5eba69cbacf2ba/docs/integration/2026-09-29-navigation-refresh.md)
and the [proof availability index](../../PROOF_INDEX.md) are separate reading routes.

One-level inventory: 68 paths; 62 retained; 6 added; 0 removed.

The rule is exactly `frontiers/<one directory>/PROOF.md`. All 62 retained proof
blobs are unchanged between the two cuts. Nested files, `sources/` copies,
coefficient packets, files with other names, and issue-only payloads are outside
this count. A path count is not a count of distinct theorems or accepted results.
Rows below pin the later commit in their links and record the full Git blob and
SHA-256 of each proof. Their order is lexical by path, not integration order.

### Six additional one-level proof paths

| Source path at the later cut | Git blob | SHA-256 |
|---|---|---|
| [source: `frontiers/cusp_torus_transfer_20261001/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/cusp_torus_transfer_20261001/PROOF.md) | `de3d85fdcf65487adc982bae7318246c1b8f016c` | `6b818bdc34c6908505c6b2ad65584f740254a8525ddc8a45197d560386243bb0` |
| [source: `frontiers/moving_remote_collision_20261003/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/moving_remote_collision_20261003/PROOF.md) | `596782786a200412a58169440b45d4f5bb36aadf` | `d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df` |
| [source: `frontiers/ordinary_short_bar_occurrence_20261001/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/ordinary_short_bar_occurrence_20261001/PROOF.md) | `69ff20a6c514629373f3ad12eb2db2a2596777d6` | `16d2c5f6c1fe45dd6ce8f6b69455db4908b8e6319e57d58c4ad7c9d1881bdd4d` |
| [source: `frontiers/replacement_bar_occurrence_20261001/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/replacement_bar_occurrence_20261001/PROOF.md) | `724258d33408f754ffc21848196e1fdd80c8bf6a` | `b49f2ea5975dc05270f51fea4a3574093f726258cdab94888742507c2caa275f` |
| [source: `frontiers/strict_unique_replacement_coefficient_20261003/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/strict_unique_replacement_coefficient_20261003/PROOF.md) | `eff422d197fcc1ff41c155c783bfeca101330a20` | `2b8949f7be425861275db49563c9dc81fee20d7118e5c6703f25f9d40e4f4188` |
| [source: `frontiers/unique_replacement_bar_intensity_20261001/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/unique_replacement_bar_intensity_20261001/PROOF.md) | `9c79a672f5d81e04972032b2f1faf185f4664fa5` | `ba1901cbb4bac037befb21d648172ac3ba04aa370f5377a2919c0da988572552` |

### Nested records, counted separately

Nested inventory: 14 proof paths in the two named collections below.

The [soft-layer collection README](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/README.md)
routes to C91–C99, C101–C103 and C124, their full reviews, source crosswalk and
checkers. The [A4 collection README](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_rejected_endpoint_margin_20261003/README.md)
routes to A4, its full review and exposure correction. These 13 plus 1 proof
records are not added to the 68 one-level paths. C100 and C104 are outside the
soft-layer collection. Copied dependencies elsewhere in `sources/` are not
new entries in either inventory. The linked proof statements and reviews govern;
this route adds no review verdict or extension to small-gap/global-bar claims.

| Nested source path at the later cut | Git blob | SHA-256 |
|---|---|---|
| [source: `frontiers/planar_rejected_endpoint_margin_20261003/A4/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_rejected_endpoint_margin_20261003/A4/PROOF.md) | `f1a71b2a0db6fc43636583af6c9f471d6c040488` | `acd172c5f8626aa3b7be5ac691786eefa6d6f243a32909502dfdbd79c8066a7c` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C101/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C101/PROOF.md) | `6dcbdf68db9d10014f1a1fe09104e3397480d229` | `300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C102/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C102/PROOF.md) | `0e35fe954fedf144baa647103d303efcd4ffab7e` | `1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C103/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C103/PROOF.md) | `b9920348bef731b1fcaaa9e5aa6cadaed77ec837` | `652e66f8645eb1a34c28a85900b05405d424bb0e282b86a7d5597f10b8f9c8e3` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C124/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C124/PROOF.md) | `d99cec53ecabfe3fb9d4a1e4a085cd026134fd5c` | `90148657397dcce31e8039afa9015c022f74b2ed0d41e75f2f2339074a8a520f` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C91/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C91/PROOF.md) | `92c9c4797081d884080622c276c6c7fe6c843533` | `74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C92/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C92/PROOF.md) | `4f6598a15dd9a64b26b5b8c6904ec4be45152409` | `6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C93/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C93/PROOF.md) | `204fd6f3d3a1bb04945dc3e1556bd1ee8e7af35e` | `f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C94/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C94/PROOF.md) | `a9f2695b4b2c45a3fa059ee3e2f889647374bffa` | `0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C95/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C95/PROOF.md) | `25faf41278c5b0f52603fbca8287b4b0c047b5da` | `c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C96/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C96/PROOF.md) | `93e3734279f024a7d253076a7d93712def5779ab` | `0758b5de8f4d9e4658ca3c6cf3e52c23d8e12f77999e9c3668ef0bedb15a05f5` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C97/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C97/PROOF.md) | `49e304440987e19ec4c1a407271093d2fc879f0a` | `acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C98/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C98/PROOF.md) | `ae0def45e3109f13b917f85b5d617f582cc5d0e2` | `3ca1622197bf22cf71ab64f2938ecc0b022ed09487b691d50ae8d2ad1f46d198` |
| [source: `frontiers/planar_soft_layer_chain_20261003/C99/PROOF.md`](https://github.com/d6g8k5htny-coder/Math-/blob/bbe85e270f2c8b747f2d5d9477c86e86e323fe15/frontiers/planar_soft_layer_chain_20261003/C99/PROOF.md) | `f8a68df60da33d59fac617267f5ab66f94fb856d` | `55eb6c33105190da4194e63d90ceeb40f3434b14b92803700ab840df67e9295e` |

This is a bounded dated inventory, not an exhaustive index of every proof format
or later repository addition. The checker verifies the retained prefix, the two
cut relationship, exact one-level delta, unchanged retained blobs, the named
nested inventory, and every listed byte identity and immutable link.

Supplement author: OpenAI/Codex, assisting the original Anthropic/Claude proposal
under Dylan Roy's explicit authorization. Scientific effect: NONE.
<!-- post-c126:end -->
