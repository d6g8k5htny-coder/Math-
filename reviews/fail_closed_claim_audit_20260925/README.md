# Fail-Closed Claim Audit — 2026-09-25

**Object:** FC-CLAIM-AUDIT-20260925-v2  
**Audited Math- commit:** `760340e921ac4ceda296b8118da936f1133e956e`  
**Scientific effect:** NONE. Source-first referee ledger; no theorem/status promotion.

## Method

Started at `Math-/README.md` and `main/docs/RESEARCH_INDEX.md`, opened every result path those pages advertise, then read the hardening status pages only to identify live/open dependency gates. Prior reviews were read **after** the source-first ledger was written. Merges, badges, green tests, hashes and praise were not treated as proof. External Drive parents are unresolved imports in a checkout-only audit.

## Live-claim dispositions

| ID | Object | Disposition | Load-bearing reason |
|---|---|---|---|
| FC-01 | SIDE24 d2/d3 coefficient expression, `coefficients/side24_v1/PROOF.md` | HOLD-WITH-DOMAIN as expression evaluation; FAIL-CLOSED as finite-bar lifetime coefficient | Parent #63 Eq15.2/proof is external to checkout. |
| FC-02 | Unrestricted lifetime remainder theorem, `LIFETIME_REMAINDER.md` | **FAIL-CLOSED** | Imports external matrix-cap/elder/Kac-Rice and marked-cylinder-cap interfaces; #63/#67 review still open. |
| FC-03 | RN probability-to-count interface | HOLD-WITH-DOMAIN | Logical implications/counterexamples are present; Gaussian N7 integral is a target, not discharged. |
| FC-04 | RN fixed-remote height-window theorem | HOLD-WITH-DOMAIN | Written proof exists only for fixed positive spatial exclusion and positive-gap compact; #76 analytic review still open. |
| FC-05 | P15 realized-cover theorem / 816 vs 818 | HOLD-WITH-DOMAIN | Exact realized capacity/clutter family only; no arbitrary-P15 extension. |
| FC-06 | Demand-one transformed-price counterexample | HOLD-WITH-DOMAIN exact falsifier | Falsifies only the stated same-palette extension; does not refute d>=2 successor. |
| FC-07 | Restricted transformed-price theorem (16/27) | HOLD-WITH-DOMAIN | Depends on FC-05 setwise cover plus T3/T6; no independent review found. |
| FC-08 | Full-price theorem with `rho*=1/[3-log(3e-2)]` | HOLD-WITH-DOMAIN | Full probability cube **inside the realized d>=2 family**; #74 analytic review remains open. |
| FC-09 | Downstream hard gate | HOLD-WITH-DOMAIN as local integrity checker; FAIL-CLOSED as repository-wide promotion firewall | Repo-local sources can be byte-bound, but external/https sources are recorded unresolved and #90 remains open. |
| FC-10 | D5 source/status graph | **FAIL-CLOSED — BLOCKING** | `GRAPH.json` names nonexistent `frontiers/rn_mesoscopic_20260925/PROOF.md`; default branch now contains a different reviewed fixed-annulus successor. |
| FC-11 | Active work-queue navigation | **FAIL-CLOSED packaging defect** | Math README and main Research Index still advertise closed #61; open downstream queue is #86. |
| FC-12 | Landing as current result map | HOLD for its listed claims; FAIL-CLOSED as complete current map | Reviewed fixed-annulus height-window result is now in default Math main but is absent from the landing. |

## Exact source identities

- `README.md` blob `604abad0863737ae576ff5800f7b0c8cfb7a4fae`
- SIDE24 proof blob `44b66f04f89fcd87383b3603fa69f1feb64cdddd`
- lifetime remainder blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`
- RN count interface blob `371fd6d17920f2eb3b1c5ec30297acf6daf1d385`
- fixed-remote proof blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84`
- realized-cover proof blob `173881916ccd0e738bdb41279e835e78e520fcbc`
- price-boundary blob `1d6946658e00e2446d68e8a4884425d4bcec62fb`
- restricted-price proof blob `9b17d179d2408dae9ea497d3c6e5c6538d2c3b8b`
- full-price proof blob `582180e41dca0ad815ad0f18574df42040912149`
- hard-gate README blob `7f07316b733ab32aceeb982051c049d62fb1ef6f`
- graph blob `988d8693a0ae9fc572471bbbd975a7f44ff480d8`
- transition-audit blob `bdc43cd508a7c9a0a49fe4a06754025502c17dfd`

## Mandatory special findings

**Undefined sums / measure mismatch:** none identified in the inspected in-tree formulas. The lifetime parent normalization is external, so FC-01/02 cannot be fully checked as persistence-density objects from this checkout.

**Answers stored in a penalty:** none identified. `K_H(d)` is an optimization definition and 816 is derived later; `rho_*` is derived from the stated worst capacity and challenged by a sharpness construction.

**Statement/proof narrowing:** none found inside FC-05–FC-08. FC-04 explicitly assumes fixed `rho>0` and positive-gap compact and uses those hypotheses. Dropping them would be a theorem/proof mismatch.

**Zero-cost edges:** zero-price generators are retained for setwise coverage and do not select a palette. Demand one is an actual boundary excluded from FC-08.

**Fits leaving range:** none in the active landing corpus. Historical H5 fitted displays are explicitly not band certificates.

**Absent artifacts:** the D5 graph's local mesoscopic proof path is absent. External lifetime/cap parents are unresolved imports. Historical RN carriers remain explicitly ABSENT on the old reproduction route.

## Prior-review reconciliation

Only after the source-first ledger existed:

- #65 explicitly says coefficient evaluation does not accept parent #63: agrees with FC-01.
- #63/#67 still request nonauthor analytic review: agrees with FC-02 fail-closed.
- #76 still requests review of fixed-remote theorem at fixed scope: agrees with FC-04.
- #74 has formal sublemma evidence and an active review assignment, but no full analytic theorem acceptance in the inspected issue comments: agrees with FC-08.
- #90 prior engineering review independently identifies unresolved controlling-source binding as a blocker: agrees with FC-09.
- Default Math main now includes source-bound xAI/Grok ACCEPT for `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md` at immutable commit `2804dc1db27ef3b1fdef6bb350b486162692cc4a`, limited to fixed d=2 annulus, compact positive marks, between-pin height window. This **does not close global D5**. It does show that the current `GRAPH.json` is stale for that subregion.

## Required object changes

1. Mirror exact #63 parent and marked-cylinder cap as byte-bound immutable imports, then point FC-01/02 edges at those objects.
2. Replace the nonexistent D5 graph source with the actual immutable fixed-annulus source/review and mark only that reviewed subregion regionally superseded/nonblocking; leave the rest of D5 open.
3. Change active work-queue links from closed #61 to open #86, preferably through one machine-readable current-dispatch pointer.
4. Require structured immutable source bindings for every controlling external node; unresolved/missing/record-only controlling sources must fail closed at the transition boundary.
5. Add a machine-readable landing claim manifest: exact statement path, blob/commit, domain, measure, required dependencies, review object, and disposition. Reject missing local paths and closed advertised work queues.
6. Either add the reviewed fixed-annulus result to the landing with its exact scope or explicitly state that the table is nonexhaustive.

## Bottom line

The active landing is substantially more honest than the historical corpus, but four things remain load-bearing:

1. the unrestricted lifetime theorem and persistence interpretation of the coefficient cannot be discharged from checkout because parent proof objects are external;
2. the D5 machine map is stale and points to a nonexistent source;
3. the hard gate is not yet a complete repository-wide promotion firewall for external controlling sources;
4. the active work-queue link is stale (#61 closed; #86 open).

No global RN closure, unrestricted P15 prize, lifetime-parent acceptance, or `lemma_closed=true` is supported by the audited tree.
